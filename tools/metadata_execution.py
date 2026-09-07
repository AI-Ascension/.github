"""Journaled metadata effects. No credentials, authorization, or generic API writes here."""
from __future__ import annotations

import copy
import hashlib
import re
import time
from pathlib import Path
from urllib.parse import quote


from metadata_journal import ExecutionError, Journal, canonical


def label_value(label):
    if label is None:
        return None
    if (not isinstance(label, dict) or type(label.get("id")) is not int or label["id"] < 1
            or not isinstance(label.get("name"), str) or not 1 <= len(label["name"]) <= 50
            or any(ord(x) < 32 or ord(x) == 127 for x in label["name"])
            or not isinstance(label.get("color"), str) or not re.fullmatch(r"[a-fA-F0-9]{6}", label["color"])
            or (label.get("description") is not None and (not isinstance(label["description"], str) or len(label["description"]) > 100))):
        raise ExecutionError("unknown or malformed stable label identity")
    return {"id": label["id"], "name": label["name"],
            "color": label["color"].lower(), "description": label.get("description") or "",
            "archived": bool(label.get("archived", False) or label.get("archived_at") is not None)}


def issue_value(issue):
    if not isinstance(issue, dict) or not isinstance(issue.get("id"), int) or "labels" not in issue:
        raise ExecutionError("unknown issue identity or label assignments")
    if not isinstance(issue["labels"], list):
        raise ExecutionError("unknown issue label collection")
    labels = []
    for label in issue["labels"]:
        if not isinstance(label, dict) or not isinstance(label.get("name"), str) or not label["name"]:
            raise ExecutionError("unknown issue label identity")
        label_id = label.get("id")
        if not ((isinstance(label_id, int) and not isinstance(label_id, bool) and label_id > 0) or label_id == "new"):
            raise ExecutionError("unknown issue label identity")
        labels.append({"id": label_id, "name": label["name"]})
    return {"id": issue["id"], "labels": sorted(labels, key=lambda x: (0, x["id"]) if isinstance(x["id"], int) else (1, x["id"]))}


def same(actual, expected):
    # A newly created label receives its stable ID from GitHub. Every later
    # effect and rollback uses the observed ID written into the journal.
    if isinstance(expected, dict) and expected.get("id") == "new":
        return isinstance(actual, dict) and {k: v for k, v in actual.items() if k != "id"} == {
            k: v for k, v in expected.items() if k != "id"}
    return actual == expected


def resolve_issue_value(assignment, definitions):
    """Resolve planner-only ``new`` IDs against the current label catalog.

    A plan cannot know the stable ID GitHub will return for a label created by
    an earlier operation.  Later sequential assignment snapshots therefore
    carry a symbolic ID.  Resolve it by the reviewed display name immediately
    before comparing or writing; never guess an ID or silently drop a label.
    """

    if not isinstance(assignment, dict) or not isinstance(assignment.get("labels"), list):
        raise ExecutionError("assignment plan lacks complete before label identities")
    by_name = {x["name"].casefold(): x for x in definitions}
    labels = []
    for value in assignment["labels"]:
        if not isinstance(value, dict) or not isinstance(value.get("name"), str):
            raise ExecutionError("assignment plan contains malformed label identity")
        label = dict(value)
        if label.get("id") == "new":
            current = by_name.get(label["name"].casefold())
            if current is None or current.get("archived"):
                raise ExecutionError("symbolic assignment label has no settled destination")
            label["id"] = current["id"]
            label["name"] = current["name"]
        labels.append(label)
    return issue_value({"id": assignment["issue_id"], "labels": labels})


class _MetadataWriter:
    """Private effect engine; only the guarded CLI is a supported caller."""
    def __init__(self, client, journal, *, state_dir=None, minimum_write_interval=1.0):
        self.client, self.path = client, Path(journal)
        self.log = None
        self.state_dir = state_dir
        self.minimum_write_interval = minimum_write_interval
        self.last_write = 0.0

    def api(self, repo, suffix="", **kwargs):
        path = "/".join(quote(x, safe="") for x in repo.split("/"))
        return self.client._run("repos/" + path + suffix, **kwargs)

    def pages(self, repo, suffix):
        value = self.api(repo, suffix, paginate=True)
        def flatten(items):
            if not isinstance(items, list):
                raise ExecutionError("paginated endpoint returned an unknown collection")
            result = []
            for item in items:
                if isinstance(item, list):
                    result.extend(flatten(item))
                elif isinstance(item, dict):
                    result.append(item)
                else:
                    raise ExecutionError("malformed paginated row")
            return result
        return flatten(value)

    def identity(self, target):
        repo = self.api(target["repository"])
        if (str(repo.get("id")) != str(target["repository_id"])
                or repo.get("full_name") != target["repository"]
                or repo.get("default_branch") != target["default_branch"]
                or repo.get("archived") is not False):
            raise ExecutionError("repository identity/default branch/archive drift; replan required")
        commit = self.api(target["repository"], "/commits/" + quote(target["default_branch"], safe=""))
        if commit.get("sha") != target["default_commit"]:
            raise ExecutionError("default-branch commit drift; replan required")
        if target.get("visibility") is not None and repo.get("visibility") != target["visibility"]:
            raise ExecutionError("repository visibility drift; replan required")

    def labels(self, repo):
        labels = self.pages(repo, "/labels?per_page=100")
        values = [label_value(x) for x in labels]
        if len({x["id"] for x in values}) != len(values) or len({x["name"].casefold() for x in values}) != len(values):
            raise ExecutionError("duplicate label identity")
        return values

    def usages(self, repo, label_id):
        issues = self.pages(repo, "/issues?state=all&per_page=100")
        result = []
        for issue in issues:
            value = issue_value(issue)
            if any(str(x["id"]) == str(label_id) for x in value["labels"]):
                result.append({"number": issue["number"], "issue_id": issue["id"]})
        return sorted(result, key=lambda x: x["number"])

    def read(self, effect):
        repo, kind = effect["repository"], effect["kind"]
        if kind == "topics":
            value = self.api(repo, "/topics")
            if not isinstance(value, dict) or not isinstance(value.get("names"), list):
                raise ExecutionError("topics were not queried successfully")
            return sorted(value["names"])
        if kind == "issue":
            return issue_value(self.api(repo, f"/issues/{effect['number']}"))
        labels = self.labels(repo)
        if kind == "create":
            return next((x for x in labels if x["name"].casefold() == effect["name"].casefold()), None)
        if kind == "definition":
            return next((x for x in labels if str(x["id"]) == str(effect["label_id"])), None)
        if kind == "rename":
            label = next((x for x in labels if str(x["id"]) == str(effect["label_id"])), None)
            return {"label": label, "usage": self.usages(repo, effect["label_id"])}
        raise ExecutionError("unsupported effect kind")

    def _state_owned(self, effect, actual):
        """Return whether a settled state is covered by this journal chain."""

        if self.log is None:
            return False
        key = effect.get("key")
        if key and (self.log.started(key) or self.log.owned(key)):
            return True
        # An earlier operation may be followed by another operation touching
        # the same issue or definition.  Its authenticated final projection
        # proves that this effect's final state is part of the reviewed plan.
        for event in self.log.events:
            if event.get("phase") not in {"verified", "reconciled", "rolled-back"}:
                continue
            candidate = event.get("effect")
            if not isinstance(candidate, dict) or candidate.get("repository") != effect.get("repository"):
                continue
            final = self._resolved_projection(candidate, candidate.get("final"))
            if final is not None and same(actual, final):
                return True
        return False

    def _operation_owned(self, op):
        if self.log is None:
            return False
        return any(
            event.get("phase") in {"intent", "verified", "reconciled"}
            and isinstance(event.get("effect"), dict)
            and event["effect"].get("operation_id") == op.get("id")
            for event in self.log.events
        )

    def _resolved_projection(self, effect, value):
        """Resolve symbolic issue-label IDs against the settled live catalog."""
        if effect.get("kind") != "issue" or value is None:
            return value
        try:
            return resolve_issue_value(value, self.labels(effect["repository"]))
        except ExecutionError:
            # A later reviewed create may not have settled yet.  The immediate
            # effect state remains authoritative until that operation runs.
            return None

    def _forward_match(self, effect, actual):
        if same(actual, effect["after"]):
            return True
        final = self._resolved_projection(effect, effect.get("final"))
        return final is not None and same(actual, final) and self._state_owned(effect, actual)

    def _read_assignment_state(self, effect, rows):
        if not rows:
            return []
        definitions = self.labels(effect["repository"])
        values = []
        for row in rows:
            issue = self.api(effect["repository"], f"/issues/{row['number']}")
            actual = issue_value(issue)
            expected = resolve_issue_value(row, definitions)
            values.append((actual, expected))
        return values

    def _assignment_match(self, effect, rows):
        return all(actual == expected for actual, expected in self._read_assignment_state(effect, rows))

    def _assignment_forward_match(self, effect):
        immediate = effect.get("assignments_after", [])
        if immediate and self._assignment_match(effect, immediate):
            return True
        final = effect.get("assignments_final", [])
        if final and self._assignment_match(effect, final):
            # Match the same ownership rule used by the primary effect state.
            if self.log is None:
                return False
            if self.log.started(effect.get("key")) or self.log.owned(effect.get("key")):
                return True
            return any(
                event.get("phase") in {"verified", "reconciled"}
                and isinstance(event.get("effect"), dict)
                and event["effect"].get("repository") == effect.get("repository")
                and event["effect"].get("assignments_final") == final
                for event in self.log.events
            )
        return not immediate and not final

    def mutate(self, effect, rollback=False):
        repo, kind = effect["repository"], effect["kind"]
        if kind == "topics":
            self.api(repo, "/topics", method="PUT", payload={"names": effect["before" if rollback else "after"]})
        elif kind == "rename":
            source = effect["after" if rollback else "before"]["label"]["name"]
            desired = effect["before" if rollback else "after"]["label"]
            self.api(repo, "/labels/" + quote(source, safe=""), method="PATCH",
                     payload={"new_name": desired["name"], "color": desired["color"], "description": desired["description"]})
        elif kind == "definition":
            desired = effect["before" if rollback else "after"]
            self.api(repo, "/labels/" + quote(desired["name"], safe=""), method="PATCH",
                     payload={"color": desired["color"], "description": desired["description"]})
        elif kind == "create":
            if rollback:
                raise ExecutionError("created label definitions are retained for manual review")
            self.api(repo, "/labels", method="POST", payload={k: effect["after"][k] for k in ("name", "color", "description")})
        elif kind == "issue":
            suffix = f"/issues/{effect['number']}/labels"
            if rollback:
                self.api(repo, suffix + "/" + quote(effect["destination"], safe=""), method="DELETE")
            else:
                # Add exactly one reviewed label; never replace the entire set.
                self.api(repo, suffix, method="POST", payload={"labels": [effect["destination"]]})
        else:
            raise ExecutionError("unsupported metadata mutation")

    def effect(self, effect, target, rollback=False):
        delay = self.minimum_write_interval - (time.monotonic() - self.last_write)
        if delay > 0:
            time.sleep(delay)
        self.identity(target)
        if effect["kind"] == "issue":
            definitions = self.labels(effect["repository"])
            destination = next((x for x in definitions
                                if x["name"].casefold() == effect["destination"].casefold()), None)
            expected = next(x for x in effect["after"]["labels"] if x["name"] == effect["destination"])
            if not destination or destination["id"] != expected["id"] or destination["archived"]:
                raise ExecutionError("assignment destination identity/archive changed before write")
            if not rollback:
                for guard in effect["definitions"]:
                    if next((x for x in definitions if x["id"] == guard["id"]), None) != guard:
                        raise ExecutionError("reviewed label definition changed before assignment")
        elif effect["kind"] == "rename" and effect.get("assignments_before"):
            if not self._assignment_match(effect, effect["assignments_before"]):
                # During reverse execution, later reviewed operations may
                # already have been rolled back.  The current issue state is
                # then this operation's immediate forward projection rather
                # than the complete final projection.  Accept that state only
                # for an owned effect; it is the exact state this rename is
                # authorized to reverse.
                immediate_forward = (effect.get("assignments_after")
                                      if rollback else None)
                immediate_ok = bool(immediate_forward) and self._assignment_match(effect, immediate_forward)
                final_ok = (bool(effect.get("assignments_final"))
                            and self._assignment_match(effect, effect["assignments_final"])
                            and self._state_owned(effect, True))
                if not immediate_ok and not final_ok:
                    raise ExecutionError(f"{effect['key']}: reviewed assignments changed before rename")
        actual = self.read(effect)
        before, after = (effect["after"], effect["before"]) if rollback else (effect["before"], effect["after"])
        if not rollback and self._forward_match(effect, actual):
            if not rollback and self.log.started(effect["key"]):
                self.log.append({"phase": "reconciled", "key": effect["key"], "effect": effect,
                                 "observed": actual, "owned": self.log.owned(effect["key"])})
            return False
        if not same(actual, before):
            raise ExecutionError(f"{effect['key']}: state drift; manual review/replan required")
        self.log.append({"phase": "rollback-intent" if rollback else "intent", "key": effect["key"], "effect": effect})
        try:
            self.last_write = time.monotonic()
            self.mutate(effect, rollback)
        except BaseException as exc:
            self.log.append({"phase": "rollback-uncertain" if rollback else "uncertain", "key": effect["key"], "error_type": type(exc).__name__})
            # Do not retry any write. An interrupted/uncertain intent is read
            # back through the same effect on explicit resume.
            raise
        observed = self.read(effect)
        assignments_ok = True
        if not rollback and effect["kind"] == "rename" and effect.get("assignments_after"):
            assignments_ok = self._assignment_forward_match(effect)
        if not same(observed, after) or not assignments_ok:
            self.log.append({"phase": "postcondition-conflict", "key": effect["key"], "observed": observed})
            raise ExecutionError(f"{effect['key']}: write postcondition not verified")
        self.log.append({"phase": "rolled-back" if rollback else "verified", "key": effect["key"],
                         "effect": effect, "observed": observed, "owned": not rollback})
        return True

    def base_effect(self, op, kind, **kwargs):
        return {"key": op["id"], "operation_id": op["id"], "repository": op["repository"], "kind": kind, **kwargs}

    def rename_effect(self, op):
        if "assignments" not in op:
            raise ExecutionError("rename plan has no complete assignment snapshot")
        usage = sorted([{"number": x["number"], "issue_id": x["issue_id"]} for x in op["assignments"]], key=lambda x: x["number"])
        effect = self.base_effect(op, "rename", label_id=op["label_id"],
                                  before={"label": label_value(op["before"]), "usage": usage},
                                  after={"label": label_value(op["after"]), "usage": usage})
        # Newer planner output records complete assignment transitions.  Keep
        # accepting older hand-authored plans used by callers/tests that only
        # supplied issue IDs for a rename.
        if all(isinstance(x, dict) and isinstance(x.get("labels"), list) for x in op["assignments"]):
            before_rows = copy.deepcopy(op["assignments"])
            after_rows = []
            for row in before_rows:
                value = copy.deepcopy(row)
                for label in value["labels"]:
                    if str(label.get("id")) == str(op["label_id"]):
                        label["name"] = op["to"]
                after_rows.append(value)
            effect["assignments_before"] = before_rows
            effect["assignments_after"] = after_rows
            if isinstance(op.get("final_assignments"), list):
                effect["assignments_final"] = copy.deepcopy(op["final_assignments"])
        return effect

    def definition_effect(self, op):
        if op["kind"] == "create_label":
            definition = op["after"]
            return self.base_effect(op, "create", name=definition["name"], before=None,
                after={"id": "new", "name": definition["name"], "color": definition["color"].lower(),
                       "description": definition.get("description") or "", "archived": False})
        before, after = label_value(op["before"]), label_value(op["after"])
        if before["id"] != after["id"] or before["name"] != after["name"] or before["archived"] != after["archived"]:
            raise ExecutionError("definition update must preserve label identity/name/archive")
        return self.base_effect(op, "definition", label_id=before["id"], before=before, after=after)

    def additive_effects(self, op):
        repo, source, destination = op["repository"], op["from"], op["to"]
        labels = self.labels(repo)
        src = next((x for x in labels if str(x["id"]) == str(op["source_label_id"])), None)
        dst = next((x for x in labels if x["name"].casefold() == destination.casefold()), None)
        if not src or src["name"] != source or src["archived"] or (dst and dst["archived"]):
            raise ExecutionError("additive source/destination identity or archive drift")
        source_definition = op.get("source_definition")
        if source_definition is None:
            raise ExecutionError("reviewed source label definition missing or changed")
        source_guard = label_value(source_definition)
        if source_guard != src:
            final_source = op.get("final_source_definition")
            if not (self._operation_owned(op) and final_source is not None and label_value(final_source) == src):
                raise ExecutionError("reviewed source label definition missing or changed")
            source_guard = src
        destination_guard = None
        if not op.get("create"):
            if "destination_definition" not in op:
                raise ExecutionError("reviewed destination label definition missing or changed")
            destination_guard = label_value(op["destination_definition"])
            if destination_guard != dst:
                final_destination = op.get("final_destination_definition")
                if not (self._operation_owned(op) and final_destination is not None and label_value(final_destination) == dst):
                    raise ExecutionError("reviewed destination label definition missing or changed")
                destination_guard = dst
        planned_usage = sorted([{"number": x["number"], "issue_id": x["issue_id"]} for x in op["assignments"]], key=lambda x: x["number"])
        if self.usages(repo, src["id"]) != planned_usage:
            raise ExecutionError("source assignments drifted; replan required")
        create = op.get("create")
        if create:
            expected = {"id": "new", "name": destination, "color": create["color"].lower(),
                        "description": create.get("description") or "", "archived": False}
            effect = self.base_effect(op, "create", name=destination, before=None, after=expected)
            effect["key"] += ":create"
            if dst and (not self.log.started(effect["key"]) or not same(dst, expected)):
                raise ExecutionError("destination appeared without this plan's creation intent")
            yield effect
            # Generator resumes after the create effect. For preflight, the
            # synthetic new ID is resolved only when actually executing.
            dst = next((x for x in self.labels(repo) if x["name"].casefold() == destination.casefold()), None)
            if dst is not None:
                labels = [x for x in labels if x["name"].casefold() != destination.casefold()] + [dst]
        elif not dst or str(dst["id"]) != str(op.get("destination_label_id")):
            raise ExecutionError("destination stable identity drift")
        for assignment in op["assignments"]:
            if "labels" not in assignment:
                raise ExecutionError("assignment plan lacks complete before label identities")
            before = resolve_issue_value(assignment, labels)
            if any(x["name"].casefold() == destination.casefold() for x in before["labels"]):
                actual = issue_value(self.api(repo, f"/issues/{assignment['number']}"))
                if actual != before:
                    raise ExecutionError("pre-existing destination assignment or unrelated labels drifted")
                continue  # Pre-existing destination assignments are never owned.
            if dst is None:
                raise ExecutionError("destination creation must settle before assignment")
            after = copy.deepcopy(before)
            after["labels"].append({"id": dst["id"], "name": dst["name"]})
            after["labels"].sort(key=lambda x: (0, x["id"]) if isinstance(x["id"], int) else (1, x["id"]))
            effect = self.base_effect(op, "issue", number=assignment["number"], destination=destination,
                                      before=before, after=after, definitions=[source_guard, destination_guard or dst])
            final_assignment = next((x for x in op.get("final_assignments", [])
                                     if x.get("issue_id") == assignment.get("issue_id")
                                     and x.get("number") == assignment.get("number")), None)
            if final_assignment is not None:
                # Keep planner-only ``new`` IDs in the journal projection.
                # Another reviewed operation may create that destination later
                # in this same ordered plan; comparisons resolve symbols from
                # the live catalog when the state has settled.
                effect["final"] = copy.deepcopy(final_assignment)
            effect["key"] += f":issue:{assignment['issue_id']}"
            yield effect

    def preflight(self, plan):
        """Validate the complete ordered state transition without writes.

        Checking each operation against the original API snapshot independently
        permits an early migration to hide a later conflict (or a later
        migration to invalidate an earlier assignment snapshot).  Keep a local
        virtual label/issue state and advance it in reviewed operation order.
        This also gives create-then-migrate plans a symbolic destination ID
        before the first network mutation.
        """

        for target in plan["targets"]:
            self.identity(target)
            topics_effect = self.base_effect(
                {**target, "id": f"topics:{target['repository_id']}", "repository": target["repository"]},
                "topics", before=[], after=[],
            )
            # Only query labels/issues when the plan uses them.  Topic-only
            # plans retain the inexpensive original preflight behavior.
            label_ops = [op for op in target["operations"] if op["kind"] != "replace_topics"]
            current_topics = None
            if any(op["kind"] == "replace_topics" for op in target["operations"]):
                topic_op = next(op for op in target["operations"] if op["kind"] == "replace_topics")
                topics_effect.update(before=sorted(topic_op["before"]), after=sorted(topic_op["after"]))
                current_topics = self.read(topics_effect)
                if current_topics not in (topics_effect["before"], topics_effect["after"]):
                    raise ExecutionError("topic drift; replan required")

            labels: list[dict] = self.labels(target["repository"]) if label_ops else []
            label_by_id = {str(row["id"]): row for row in labels}
            label_by_name = {row["name"].casefold(): row for row in labels}
            issue_by_id: dict[str, dict] = {}
            issue_by_number: dict[str, dict] = {}
            issue_number_by_id: dict[str, int] = {}
            if any(op["kind"] in {"rename_label", "additive_label_migration"} for op in label_ops):
                for raw_issue in self.pages(target["repository"], "/issues?state=all&per_page=100"):
                    value = issue_value(raw_issue)
                    issue_by_id[str(value["id"])] = value
                    if raw_issue.get("number") is not None:
                        issue_by_number[str(raw_issue["number"])] = value
                        issue_number_by_id[str(value["id"])] = raw_issue["number"]

            def operation_owned(op):
                return self._operation_owned(op)

            def row_for_assignment(assignment):
                issue = issue_by_id.get(str(assignment.get("issue_id")))
                if issue is None:
                    issue = issue_by_number.get(str(assignment.get("number")))
                if issue is None or str(issue.get("id")) != str(assignment.get("issue_id")):
                    raise ExecutionError("planned issue identity drift; replan required")
                return issue

            def final_assignment(op, assignment):
                return next((row for row in op.get("final_assignments", [])
                             if str(row.get("issue_id")) == str(assignment.get("issue_id"))
                             and str(row.get("number")) == str(assignment.get("number"))), None)

            def expected_final_assignment(op, assignment, expected, destination=None):
                """Return the reviewed settled assignment for a legacy row.

                Older hand-authored additive plans did not carry the planner's
                ``final_assignments`` projection.  Their settled state is still
                unambiguous: add the destination exactly once when it was not
                already present in the reviewed before snapshot.
                """
                final = final_assignment(op, assignment)
                if final is not None:
                    return resolve_issue_value(final, labels)
                if (op["kind"] == "additive_label_migration" and destination is not None
                        and not any(x["name"].casefold() == destination["name"].casefold()
                                    for x in expected["labels"])):
                    settled = copy.deepcopy(expected)
                    settled["labels"].append({"id": destination["id"], "name": destination["name"]})
                    settled["labels"].sort(key=lambda x: (0, x["id"]) if isinstance(x["id"], int) else (1, x["id"]))
                    return settled
                return None

            def assignment_matches(op, assignment, expected, *, allow_final=True):
                issue = row_for_assignment(assignment)
                if issue == expected:
                    return "before"
                if allow_final and operation_owned(op):
                    destination = None
                    if op["kind"] == "additive_label_migration":
                        destination = label_by_name.get(op["to"].casefold())
                    final = expected_final_assignment(op, assignment, expected, destination)
                    if final is not None and issue == final:
                        return "final"
                raise ExecutionError(f"{op['id']}: issue label drift; replan required")

            def resolve_label(row):
                if row is None:
                    return None
                name = row.get("name")
                if isinstance(name, str):
                    return label_by_name.get(name.casefold())
                return label_by_id.get(str(row.get("id")))

            for op in target["operations"]:
                if op["repository"] != target["repository"] or str(op["repository_id"]) != str(target["repository_id"]):
                    raise ExecutionError("operation target differs from reviewed repository identity")
                if op["kind"] == "replace_topics":
                    if current_topics == sorted(op["before"]):
                        current_topics = sorted(op["after"])
                    elif current_topics != sorted(op["after"]):
                        raise ExecutionError("topic drift; replan required")
                    continue
                if op["kind"] == "create_label":
                    expected = {"id": "new", "name": op["after"]["name"], "color": op["after"]["color"].lower(),
                                "description": op["after"].get("description") or "", "archived": False}
                    actual = label_by_name.get(op["after"]["name"].casefold())
                    if actual is not None:
                        if not operation_owned(op) or not same(actual, expected):
                            raise ExecutionError("label appeared without reviewed creation intent")
                        expected = dict(actual)
                    label_by_name[op["after"]["name"].casefold()] = expected
                    label_key = (f"new:{expected['name'].casefold()}"
                                 if expected.get("id") == "new" else str(expected["id"]))
                    label_by_id[label_key] = expected
                    labels = list(label_by_id.values())
                    continue
                if op["kind"] == "update_label":
                    expected_before = label_value(op["before"])
                    expected_after = label_value(op["after"])
                    label_id = op.get("label_id", expected_before["id"])
                    actual = label_by_id.get(str(label_id))
                    if actual is None:
                        raise ExecutionError("shared label definition drift")
                    if actual == expected_before:
                        label_by_id[str(label_id)] = expected_after
                        label_by_name[expected_after["name"].casefold()] = expected_after
                    elif actual == expected_after and operation_owned(op):
                        pass
                    else:
                        raise ExecutionError("shared label definition drift")
                    labels = list(label_by_id.values())
                    continue
                if op["kind"] == "rename_label":
                    before = label_value(op["before"])
                    after = label_value(op["after"])
                    actual = label_by_id.get(str(op["label_id"]))
                    collision = label_by_name.get(op["to"].casefold())
                    if collision is not None and str(collision.get("id")) != str(op["label_id"]):
                        raise ExecutionError("rename destination collision")
                    if actual is None:
                        raise ExecutionError("rename definition/assignment drift; replan required")
                    if actual == before:
                        if all(isinstance(x, dict) and isinstance(x.get("labels"), list) for x in op.get("assignments", [])):
                            for assignment in op.get("assignments", []):
                                expected = resolve_issue_value(assignment, labels)
                                if assignment_matches(op, assignment, expected) == "before":
                                    issue = row_for_assignment(assignment)
                                    for label in issue["labels"]:
                                        if str(label["id"]) == str(op["label_id"]):
                                            label["name"] = op["to"]
                        label_by_id[str(op["label_id"])] = after
                        label_by_name.pop(op["from"].casefold(), None)
                        label_by_name[op["to"].casefold()] = after
                    elif actual == after and operation_owned(op):
                        if all(isinstance(x, dict) and isinstance(x.get("labels"), list) for x in op.get("assignments", [])):
                            for assignment in op.get("assignments", []):
                                expected = resolve_issue_value(assignment, labels)
                                issue = row_for_assignment(assignment)
                                immediate = copy.deepcopy(expected)
                                for label in immediate["labels"]:
                                    if str(label["id"]) == str(op["label_id"]):
                                        label["name"] = op["to"]
                                final = final_assignment(op, assignment)
                                if issue != immediate and (final is None or issue != resolve_issue_value(final, labels)):
                                    raise ExecutionError(f"{op['id']}: issue label drift; replan required")
                    else:
                        raise ExecutionError("rename definition/assignment drift; replan required")
                    labels = list(label_by_id.values())
                    continue
                if op["kind"] == "additive_label_migration":
                    source = label_by_id.get(str(op["source_label_id"]))
                    if source is None:
                        raise ExecutionError("additive source identity drift; replan required")
                    source_expected = label_value(op["source_definition"])
                    source_final = op.get("final_source_definition")
                    if source != source_expected:
                        if not (operation_owned(op) and source_final is not None and source == label_value(source_final)):
                            raise ExecutionError("reviewed source label definition missing or changed")
                    destination = label_by_name.get(op["to"].casefold())
                    if op.get("create"):
                        expected_destination = {"id": "new", "name": op["to"], "color": op["create"]["color"].lower(),
                                                "description": op["create"].get("description") or "", "archived": False}
                        if destination is None:
                            destination = expected_destination
                            label_by_name[op["to"].casefold()] = destination
                            label_by_id[f"new:{destination['name'].casefold()}"] = destination
                        elif not (operation_owned(op) and same(destination, expected_destination)):
                            raise ExecutionError("destination appeared without this plan's creation intent")
                    else:
                        if destination is None:
                            raise ExecutionError("destination stable identity drift")
                        destination_expected = label_value(op["destination_definition"])
                        destination_final = op.get("final_destination_definition")
                        if destination != destination_expected:
                            if not (operation_owned(op) and destination_final is not None and destination == label_value(destination_final)):
                                raise ExecutionError("reviewed destination label definition missing or changed")
                    labels = list(label_by_id.values())
                    usages = sorted(
                        {str(x.get("issue_id")): {"number": x.get("number"), "issue_id": x.get("issue_id")}
                         for x in op.get("assignments", [])}.values(),
                        key=lambda x: x["number"],
                    )
                    source_usage = sorted(
                        {str(issue["id"]): {"number": issue_number_by_id.get(str(issue["id"])), "issue_id": issue["id"]}
                         for issue in issue_by_id.values()
                         if any(str(label["id"]) == str(op["source_label_id"]) for label in issue["labels"])}.values(),
                        key=lambda x: x["number"],
                    )
                    # The assignment list is the complete source-usage
                    # snapshot, so omitted source issues are a conflict even
                    # when every listed issue happens to be unchanged.
                    if usages != source_usage:
                        raise ExecutionError("source assignments drifted; replan required")
                    for assignment in op.get("assignments", []):
                        expected = resolve_issue_value(assignment, labels)
                        status = assignment_matches(op, assignment, expected)
                        destination_present = any(x["name"].casefold() == op["to"].casefold()
                                                  for x in expected["labels"])
                        if status == "before" and not assignment.get("destination_preexisting") and not destination_present:
                            issue = row_for_assignment(assignment)
                            destination_id = destination["id"]
                            issue["labels"].append({"id": destination_id, "name": destination["name"]})
                            issue["labels"].sort(key=lambda x: (0, x["id"]) if isinstance(x["id"], int) else (1, x["id"]))
                    continue
                raise ExecutionError("unknown operation kind")

    def final_readback(self, plan):
        """Read every reviewed final state after the ordered writes settle."""

        for target in plan["targets"]:
            self.identity(target)
            topic_ops = [op for op in target["operations"] if op["kind"] == "replace_topics"]
            if topic_ops:
                effect = self.base_effect(topic_ops[-1], "topics", before=sorted(topic_ops[-1]["before"]), after=sorted(topic_ops[-1]["after"]))
                if self.read(effect) != effect["after"]:
                    raise ExecutionError("final topic readback did not match the reviewed plan")
            labels = self.labels(target["repository"]) if any(op["kind"] != "replace_topics" for op in target["operations"]) else []
            by_id = {str(row["id"]): row for row in labels}
            by_name = {row["name"].casefold(): row for row in labels}
            for op in target["operations"]:
                kind = op["kind"]
                if kind == "replace_topics":
                    continue
                if kind == "create_label":
                    actual = by_name.get(op["after"]["name"].casefold())
                    expected = {"id": "new", "name": op["after"]["name"], "color": op["after"]["color"].lower(),
                                "description": op["after"].get("description") or "", "archived": False}
                    if actual is None or not same(actual, expected):
                        raise ExecutionError(f"{op['id']}: final label creation readback failed")
                    continue
                if kind == "update_label":
                    label_id = op.get("label_id", op["before"]["id"])
                    actual = by_id.get(str(label_id))
                    if actual is None or actual != label_value(op["after"]):
                        raise ExecutionError(f"{op['id']}: final label definition readback failed")
                    continue
                if kind == "rename_label":
                    actual = by_id.get(str(op["label_id"]))
                    if actual is None or actual != label_value(op["after"]):
                        raise ExecutionError(f"{op['id']}: final rename readback failed")
                    rows = op.get("final_assignments", [])
                elif kind == "additive_label_migration":
                    source = by_id.get(str(op["source_label_id"]))
                    expected_source = op.get("final_source_definition", op.get("source_definition"))
                    if source is None or expected_source is None or source != label_value(expected_source):
                        raise ExecutionError(f"{op['id']}: final source definition readback failed")
                    destination = by_name.get(op["to"].casefold())
                    expected_destination = op.get("final_destination_definition")
                    if expected_destination is None:
                        if op.get("create"):
                            expected_destination = {"id": "new", "name": op["to"], "color": op["create"]["color"],
                                                   "description": op["create"].get("description") or "", "archived": False}
                        else:
                            expected_destination = op.get("destination_definition")
                    if expected_destination is not None and expected_destination.get("id") != "new":
                        expected_destination = label_value(expected_destination)
                    if destination is None or expected_destination is None or not same(destination, expected_destination):
                        raise ExecutionError(f"{op['id']}: final destination definition readback failed")
                    rows = op.get("final_assignments", [])
                    if not rows:
                        rows = []
                        for original in op.get("assignments", []):
                            if (original.get("destination_preexisting")
                                    or any(x.get("name", "").casefold() == destination["name"].casefold()
                                           for x in original.get("labels", []))):
                                continue
                            row = copy.deepcopy(original)
                            row["labels"].append({"id": destination["id"], "name": destination["name"]})
                            rows.append(row)
                else:
                    raise ExecutionError("unknown operation kind")
                for row in rows:
                    actual = issue_value(self.api(target["repository"], f"/issues/{row['number']}"))
                    expected = resolve_issue_value(row, labels)
                    if actual != expected:
                        raise ExecutionError(f"{op['id']}: final assignment readback failed for issue {row['number']}")

    def preflight_additive(self, op):
        # Materialize everything before the first write, including later issue
        # conflicts, even when the destination does not yet exist.
        labels = self.labels(op["repository"])
        dst = next((x for x in labels if x["name"].casefold() == op["to"].casefold()), None)
        generator = self.additive_effects(op)
        if op.get("create"):
            next(generator)
        if dst:
            for effect in generator:
                actual = self.read(effect)
                if not self._forward_match(effect, actual):
                    raise ExecutionError("issue label drift; replan required")
        elif op.get("create"):
            for row in op["assignments"]:
                if "labels" not in row:
                    raise ExecutionError("assignment plan lacks complete before labels")
                before = resolve_issue_value(row, labels)
                current = issue_value(self.api(op["repository"], f"/issues/{row['number']}"))
                if current != before:
                    raise ExecutionError("issue label drift; replan required")
        else:
            list(generator)  # Raises for an absent destination/source identity.

    def validate_plan(self, plan):
        expected = hashlib.sha256(canonical({k: v for k, v in plan.items() if k != "digest"}).encode()).hexdigest()
        if plan.get("digest") != expected:
            raise ExecutionError("plan digest is invalid")
        seen = set()
        kinds = {"replace_topics", "rename_label", "additive_label_migration", "create_label", "update_label"}
        try:
            for target in plan["targets"]:
                repo = target["repository"]
                if (not isinstance(repo, str) or not re.fullmatch(r"AI-Ascension/[A-Za-z0-9_.-]+", repo)
                        or repo.split("/")[1] in {".", ".."}
                        or not str(target["repository_id"]).isdigit() or int(target["repository_id"]) < 1
                        or not re.fullmatch(r"[a-fA-F0-9]{40}", target["default_commit"])
                        or not isinstance(target["default_branch"], str) or not target["default_branch"]):
                    raise ExecutionError("invalid repository identity or source pin")
                for op in target["operations"]:
                    if (op["kind"] not in kinds or not isinstance(op["id"], str) or not op["id"]
                            or op["id"] in seen or op["repository"] != repo
                            or str(op["repository_id"]) != str(target["repository_id"])):
                        raise ExecutionError("invalid or duplicate operation target/kind")
                    seen.add(op["id"])
                    if op["kind"] == "replace_topics":
                        for field in ("before", "after"):
                            names = op[field]
                            if (not isinstance(names, list) or len(names) > 20 or len(set(names)) != len(names)
                                    or any(not isinstance(x, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,49}", x) for x in names)):
                                raise ExecutionError("invalid complete topic set")
                        if "ai-ascension" not in op["after"]:
                            raise ExecutionError("common brand topic is required")
                    if op["kind"] in {"rename_label", "additive_label_migration"}:
                        for name in (op["from"], op["to"]):
                            if not isinstance(name, str) or not 1 <= len(name) <= 50 or any(ord(x) < 32 or ord(x) == 127 for x in name):
                                raise ExecutionError("invalid migration label name")
                        for assignment in op["assignments"]:
                            if (type(assignment["number"]) is not int or assignment["number"] < 1
                                    or type(assignment["issue_id"]) is not int or assignment["issue_id"] < 1):
                                raise ExecutionError("invalid issue identity/number")
                        if op["kind"] == "rename_label":
                            effect = self.rename_effect(op)
                            if (effect["before"]["label"]["name"] != op["from"] or effect["after"]["label"]["name"] != op["to"]
                                    or effect["before"]["label"]["id"] != op["label_id"] or effect["after"]["label"]["id"] != op["label_id"]):
                                raise ExecutionError("rename label identity/name mismatch")
                        else:
                            label_value(op["source_definition"])
                            if op.get("create"):
                                label_value({"id": 1, **op["create"]})
                            else:
                                label_value(op["destination_definition"])
                            if op.get("final_source_definition") is not None:
                                label_value(op["final_source_definition"])
                            if op.get("final_destination_definition") is not None:
                                if op.get("final_destination_definition", {}).get("id") == "new":
                                    label_value({"id": 1, **{k: v for k, v in op["final_destination_definition"].items() if k != "id"}})
                                else:
                                    label_value(op["final_destination_definition"])
                            for assignment in op["assignments"]:
                                issue_value({"id": assignment["issue_id"], "labels": assignment["labels"]})
                            for assignment in op.get("final_assignments", []):
                                issue_value({"id": assignment["issue_id"], "labels": assignment["labels"]})
                    if op["kind"] in {"create_label", "update_label"}:
                        self.definition_effect(op)
                        if op["kind"] == "create_label":
                            label_value({**op["after"], "id": 1})
        except (KeyError, TypeError, ValueError) as exc:
            raise ExecutionError("malformed execution plan") from exc

    def validate_effect(self, effect, op):
        if effect["repository"] != op["repository"] or effect["operation_id"] != op["id"]:
            raise ExecutionError("journal effect target differs from plan")
        if op["kind"] == "replace_topics":
            expected = self.base_effect(op, "topics", before=sorted(op["before"]), after=sorted(op["after"]))
        elif op["kind"] == "rename_label":
            expected = self.rename_effect(op)
        elif op["kind"] in {"create_label", "update_label"}:
            expected = self.definition_effect(op)
        elif effect["kind"] == "create" and op.get("create"):
            expected = self.base_effect(op, "create", name=op["to"], before=None,
                after={"id": "new", "name": op["to"], "color": op["create"]["color"].lower(),
                       "description": op["create"].get("description") or "", "archived": False})
            expected["key"] += ":create"
        elif effect["kind"] == "issue" and op["kind"] == "additive_label_migration":
            row = next((x for x in op["assignments"] if x["number"] == effect["number"]), None)
            if row is None:
                raise ExecutionError("journal issue is absent from reviewed assignments")
            before = issue_value({"id": row["issue_id"], "labels": row["labels"]})
            destinations = [x for x in effect["after"]["labels"] if x["name"] == op["to"]]
            if len(destinations) != 1 or any(x["name"].casefold() == op["to"].casefold() for x in before["labels"]):
                raise ExecutionError("journal claims a pre-existing or unknown assignment")
            destination = destinations[0]
            if op.get("destination_label_id") is not None and destination["id"] != op["destination_label_id"]:
                raise ExecutionError("journal destination identity differs from plan")
            after = {"id": before["id"], "labels": sorted(
                before["labels"] + [destination],
                key=lambda x: (0, x["id"]) if isinstance(x["id"], int) else (1, x["id"]),
            )}
            src = label_value(op["source_definition"])
            if op.get("create"):
                definition = {"id": destination["id"], "name": op["to"], "color": op["create"]["color"],
                              "description": op["create"].get("description") or "", "archived": False}
                dst = label_value(definition)
            else:
                dst = label_value(op["destination_definition"])
            expected = self.base_effect(op, "issue", number=row["number"], destination=op["to"], before=before,
                                        after=after, definitions=[src, dst])
            final_assignment = next((x for x in op.get("final_assignments", [])
                                     if str(x.get("issue_id")) == str(row.get("issue_id"))
                                     and str(x.get("number")) == str(row.get("number"))), None)
            if final_assignment is not None:
                # The journal records the settled projection when subsequent
                # reviewed operations touch the same issue.  It is part of the
                # authenticated effect and must be validated before rollback.
                expected["final"] = copy.deepcopy(final_assignment)
            expected["key"] += f":issue:{row['issue_id']}"
        else:
            raise ExecutionError("journal effect kind differs from reviewed operation")
        if effect != expected:
            raise ExecutionError("journal effect preconditions differ from reviewed plan")

    def apply(self, plan, *, execute, resume=False):
        self.validate_plan(plan)
        if not execute:
            return {"plan_digest": plan["digest"], "execute": False, "applied": [], "writes": 0}
        with Journal(self.path, plan, self.state_dir) as self.log:
            if self.log.events and not resume:
                # A fully converged second application is allowed, but partial
                # journals require an explicit resume to avoid ambiguous work.
                pending = {e["key"] for e in self.log.events if e.get("phase") == "intent"}
                pending -= {e["key"] for e in self.log.events if e.get("phase") in {"verified", "reconciled"}}
                if pending:
                    raise ExecutionError("unfinished journal; inspect live state and use --resume")
            self.preflight(plan)
            result = {"plan_digest": plan["digest"], "execute": True, "applied": [], "writes": 0}
            for target in plan["targets"]:
                for op in target["operations"]:
                    if op["kind"] == "replace_topics":
                        effects = [self.base_effect(op, "topics", before=sorted(op["before"]), after=sorted(op["after"]))]
                    elif op["kind"] == "rename_label":
                        effects = [self.rename_effect(op)]
                    elif op["kind"] in {"create_label", "update_label"}:
                        effects = [self.definition_effect(op)]
                    else:
                        effects = self.additive_effects(op)
                    for effect in effects:
                        if self.effect(effect, target):
                            result["applied"].append(effect["key"])
                            result["writes"] += 1
            self.final_readback(plan)
            return result

    def rollback(self, plan, *, execute):
        self.validate_plan(plan)
        result = {"plan_digest": plan["digest"], "execute": execute, "rolled_back": [], "conflicts": [], "retained_labels": [], "writes": 0}
        if not execute:
            return result
        with Journal(self.path, plan, self.state_dir) as self.log:
            targets = {op["id"]: (target, op) for target in plan["targets"] for op in target["operations"]}
            effects = {}
            for event in self.log.events:
                if event.get("phase") == "intent":
                    effects[event["key"]] = event["effect"]
            for effect in reversed(list(effects.values())):
                try:
                    target, op = targets[effect["operation_id"]]
                    self.validate_effect(effect, op)
                    if effect["kind"] == "create":
                        result["retained_labels"].append(effect["name"])
                        continue
                    if not self.log.owned(effect["key"]):
                        if same(self.read(effect), effect["before"]):
                            continue
                        raise ExecutionError("uncertain forward effect ownership; manual review required")
                    if self.effect(effect, target, rollback=True):
                        result["rolled_back"].append(effect["key"])
                        result["writes"] += 1
                except Exception as exc:
                    conflict = {"key": effect.get("key", "unknown") if isinstance(effect, dict) else "unknown", "reason": str(exc)}
                    self.log.append({"phase": "rollback-conflict", **conflict})
                    result["conflicts"].append(conflict)
            return result
