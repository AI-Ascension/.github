"""Regression oracles for actual requests, uncertainty, and human edits."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from metadata_execution import ExecutionError, _MetadataWriter as MetadataWriter, canonical


REPO = "AI-Ascension/example"
SHA = "a" * 40


def label(number, name):
    return {"id": number, "name": name, "color": "abcdef", "description": name, "archived": False}


class FakeAPI:
    def __init__(self):
        self.topics = ["ai-ascension"]
        self.labels = [label(1, "docs"), label(2, "documentation"), label(3, "human: label")]
        self.issues = [{"id": 101, "number": 1, "labels": copy.deepcopy([self.labels[0], self.labels[2]])}]
        self.writes = []
        self.timeout_after_write = False
        self.before_write_read = None
        self.branch = "trunk"
        self.visibility = "public"
        self.identity_reads = 0
        self.identity_hook = None

    def _run(self, endpoint, method="GET", payload=None, paginate=False):
        prefix = "repos/AI-Ascension/example"
        if not endpoint.startswith(prefix):
            raise AssertionError("unexpected target " + endpoint)
        suffix = unquote(endpoint[len(prefix):]).split("?")[0]
        if method == "GET":
            if suffix == "":
                self.identity_reads += 1
                if self.identity_hook:
                    self.identity_hook(self.identity_reads)
                if self.before_write_read:
                    hook, self.before_write_read = self.before_write_read, None
                    hook()
                return {"id": 7, "full_name": REPO, "default_branch": self.branch, "archived": False, "visibility": self.visibility}
            if suffix == "/commits/trunk":
                return {"sha": SHA}
            if suffix == "/topics":
                return {"names": copy.deepcopy(self.topics)}
            if suffix == "/labels":
                # Two pages deliberately; do not confuse a nested response with one row.
                return copy.deepcopy([self.labels[:1], self.labels[1:]])
            if suffix == "/issues":
                return copy.deepcopy([self.issues])
            if suffix.startswith("/issues/"):
                number = int(suffix.split("/")[2])
                return copy.deepcopy(next(x for x in self.issues if x["number"] == number))
            raise AssertionError("unexpected read " + suffix)
        self.writes.append((method, suffix, copy.deepcopy(payload)))
        if suffix == "/topics" and method == "PUT":
            self.topics = copy.deepcopy(payload["names"])
        elif suffix.startswith("/labels/") and method == "PATCH":
            name = suffix[len("/labels/"):]
            row = next(x for x in self.labels if x["name"] == name)
            row["name"] = payload.get("new_name", row["name"])
            row.update({k: v for k, v in payload.items() if k in {"color", "description"}})
            for issue in self.issues:
                for assigned in issue["labels"]:
                    if assigned["id"] == row["id"]:
                        assigned["name"] = row["name"]
        elif suffix == "/labels" and method == "POST":
            self.labels.append({"id": max([19] + [x["id"] for x in self.labels]) + 1, **payload, "archived": False})
        elif suffix.startswith("/issues/"):
            parts = suffix.split("/")
            issue = next(x for x in self.issues if x["number"] == int(parts[2]))
            if method == "POST":
                for name in payload["labels"]:
                    item = next(x for x in self.labels if x["name"] == name)
                    if not any(x["id"] == item["id"] for x in issue["labels"]):
                        issue["labels"].append(copy.deepcopy(item))
            elif method == "DELETE":
                issue["labels"] = [x for x in issue["labels"] if x["name"] != parts[4]]
            else:
                raise AssertionError("whole issue-label replacement is forbidden")
        else:
            raise AssertionError("unexpected write " + suffix)
        if self.timeout_after_write:
            self.timeout_after_write = False
            raise TimeoutError("connection lost after server accepted write")
        return {}


def topics_op():
    return {"id": "topics:7", "kind": "replace_topics", "repository": REPO, "repository_id": "7",
            "before": ["ai-ascension"], "after": ["ai-ascension", "rust"]}


def plan(op):
    value = {"targets": [{"repository": REPO, "repository_id": "7", "default_branch": "trunk",
                          "default_commit": SHA, "operations": [op]}]}
    value["digest"] = hashlib.sha256(canonical(value).encode()).hexdigest()
    return value


def additive(api, create=False):
    return {"id": "add:7", "kind": "additive_label_migration", "repository": REPO, "repository_id": "7",
            "from": "docs", "to": "documentation", "source_label_id": 1, "destination_label_id": None if create else 2,
            "source_definition": copy.deepcopy(next(x for x in api.labels if x["id"] == 1)),
            "destination_definition": None if create else copy.deepcopy(next(x for x in api.labels if x["id"] == 2)),
            "create": {"name": "documentation", "color": "abcdef", "description": "documentation"} if create else None,
            "assignments": [{"issue_id": x["id"], "number": x["number"], "labels": copy.deepcopy(x["labels"])} for x in api.issues]}


class ExecutionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "journal.jsonl"
        self.api = FakeAPI()
        self.writer = MetadataWriter(self.api, self.path, state_dir=Path(self.tmp.name) / "keys", minimum_write_interval=0)

    def test_dry_run_does_not_create_journal_or_write(self):
        self.writer.apply(plan(topics_op()), execute=False)
        self.writer.rollback(plan(topics_op()), execute=False)
        self.assertEqual([], self.api.writes)
        self.assertFalse(self.path.exists())

    def test_full_topic_set_and_second_application_zero_writes(self):
        p = plan(topics_op())
        self.assertEqual(1, self.writer.apply(p, execute=True)["writes"])
        self.assertEqual([("PUT", "/topics", {"names": ["ai-ascension", "rust"]})], self.api.writes)
        self.assertEqual(0, self.writer.apply(p, execute=True)["writes"])
        self.assertTrue(any(json.loads(x)["phase"] == "verified" for x in self.path.read_text().splitlines()))

    def test_stale_topics_reject_before_any_write(self):
        self.api.topics.append("human")
        with self.assertRaises(ExecutionError):
            self.writer.apply(plan(topics_op()), execute=True)
        self.assertEqual([], self.api.writes)

    def test_timeout_is_reconciled_without_repeating_write(self):
        self.api.timeout_after_write = True
        p = plan(topics_op())
        with self.assertRaises(TimeoutError):
            self.writer.apply(p, execute=True)
        with self.assertRaises(ExecutionError):
            self.writer.apply(p, execute=True)
        self.assertEqual(0, self.writer.apply(p, execute=True, resume=True)["writes"])
        self.assertEqual(1, len(self.api.writes))

    def test_rollback_topics_preserves_later_human_edit(self):
        p = plan(topics_op())
        self.writer.apply(p, execute=True)
        self.api.topics.append("human")
        result = self.writer.rollback(p, execute=True)
        self.assertEqual(1, len(result["conflicts"]))
        self.assertEqual(0, result["writes"])
        self.assertIn("human", self.api.topics)

    def test_rollback_does_not_claim_preexisting_target_state(self):
        self.api.topics.append("rust")
        p = plan(topics_op())
        self.writer.apply(p, execute=True)
        self.assertEqual(0, self.writer.rollback(p, execute=True)["writes"])
        self.assertIn("rust", self.api.topics)

    def test_rename_keeps_label_id_and_assignments(self):
        self.api.labels = [self.api.labels[0], self.api.labels[2]]
        before = copy.deepcopy(self.api.labels[0])
        after = {**before, "name": "documentation"}
        op = {"id": "rename:7", "kind": "rename_label", "repository": REPO, "repository_id": "7", "label_id": 1,
              "from": "docs", "to": "documentation", "before": before, "after": after,
              "assignments": [{"number": 1, "issue_id": 101}]}
        p = plan(op)
        self.writer.apply(p, execute=True)
        self.assertEqual(("PATCH", "/labels/docs", {"new_name": "documentation", "color": "abcdef", "description": "docs"}), self.api.writes[0])
        self.assertEqual(1, self.api.issues[0]["labels"][0]["id"])
        self.assertEqual(0, self.writer.apply(p, execute=True)["writes"])
        self.assertEqual(1, self.writer.rollback(p, execute=True)["writes"])
        self.assertEqual("docs", self.api.issues[0]["labels"][0]["name"])

    def test_additive_preserves_source_and_unmanaged_labels(self):
        p = plan(additive(self.api))
        self.writer.apply(p, execute=True)
        self.assertEqual({1, 2, 3}, {x["id"] for x in self.api.issues[0]["labels"]})
        self.assertEqual("POST", self.api.writes[0][0])
        self.assertEqual(0, self.writer.apply(p, execute=True)["writes"])
        self.writer.rollback(p, execute=True)
        self.assertEqual({1, 3}, {x["id"] for x in self.api.issues[0]["labels"]})

    def test_additive_rollback_never_erases_preexisting_destination(self):
        self.api.issues[0]["labels"].append(copy.deepcopy(self.api.labels[1]))
        p = plan(additive(self.api))
        self.assertEqual(0, self.writer.apply(p, execute=True)["writes"])
        self.assertEqual(0, self.writer.rollback(p, execute=True)["writes"])
        self.assertIn(2, [x["id"] for x in self.api.issues[0]["labels"]])

    def test_additive_rollback_flags_later_issue_edits(self):
        p = plan(additive(self.api))
        self.writer.apply(p, execute=True)
        self.api.issues[0]["labels"].append(label(4, "maintainer"))
        result = self.writer.rollback(p, execute=True)
        self.assertEqual(0, result["writes"])
        self.assertEqual(1, len(result["conflicts"]))
        self.assertEqual({1, 2, 3, 4}, {x["id"] for x in self.api.issues[0]["labels"]})

    def test_create_destination_and_resume_after_uncertain_creation(self):
        self.api.labels = [x for x in self.api.labels if x["id"] != 2]
        p = plan(additive(self.api, create=True))
        self.api.timeout_after_write = True
        with self.assertRaises(TimeoutError):
            self.writer.apply(p, execute=True)
        self.assertEqual(1, self.writer.apply(p, execute=True, resume=True)["writes"])
        self.assertEqual(2, len(self.api.writes))
        result = self.writer.rollback(p, execute=True)
        self.assertEqual(["documentation"], result["retained_labels"])
        self.assertEqual({1, 3}, {x["id"] for x in self.api.issues[0]["labels"]})
        self.assertIn("documentation", [x["name"] for x in self.api.labels])

    def test_later_issue_conflict_preflights_before_label_creation(self):
        self.api.labels = [x for x in self.api.labels if x["id"] != 2]
        p = plan(additive(self.api, create=True))
        self.api.issues[0]["labels"].append(label(4, "maintainer"))
        with self.assertRaises(ExecutionError):
            self.writer.apply(p, execute=True)
        self.assertEqual([], self.api.writes)

    def test_wrong_journal_plan_is_rejected(self):
        p = plan(topics_op())
        self.writer.apply(p, execute=True)
        p["digest"] = "e" * 64
        with self.assertRaises(ExecutionError):
            self.writer.rollback(p, execute=True)
        self.assertEqual(1, len(self.api.writes))

    def test_absent_destination_without_create_cannot_write(self):
        p = plan(additive(self.api))
        self.api.labels = [x for x in self.api.labels if x["id"] != 2]
        with self.assertRaises(ExecutionError):
            self.writer.apply(p, execute=True)
        self.assertEqual([], self.api.writes)

    def test_tampered_journal_cannot_supply_rollback_topics(self):
        p = plan(topics_op())
        self.writer.apply(p, execute=True)
        events = [json.loads(x) for x in self.path.read_text().splitlines()]
        events[0]["effect"]["before"] = ["attacker"]
        self.path.write_text("".join(json.dumps(x) + "\n" for x in events))
        with self.assertRaises(ExecutionError):
            self.writer.rollback(p, execute=True)
        self.assertEqual(1, len(self.api.writes))

    def test_shared_definition_update_preserves_assignments(self):
        before = copy.deepcopy(self.api.labels[0])
        op = {"id": "update:7:1", "kind": "update_label", "repository": REPO, "repository_id": "7",
              "before": before, "after": {**before, "description": "Reviewed definition"}}
        p = plan(op)
        self.writer.apply(p, execute=True)
        self.assertEqual("Reviewed definition", self.api.labels[0]["description"])
        self.assertEqual({1, 3}, {x["id"] for x in self.api.issues[0]["labels"]})
        self.api.labels[0]["color"] = "123456"
        self.assertEqual(1, len(self.writer.rollback(p, execute=True)["conflicts"]))

    def test_shared_label_create_is_retained_by_rollback(self):
        op = {"id": "create:7", "kind": "create_label", "repository": REPO, "repository_id": "7", "before": None,
              "after": {"id": "new", "name": "first-task", "color": "abcdef", "description": "Scoped task"}}
        p = plan(op)
        self.writer.apply(p, execute=True)
        self.assertEqual(0, self.writer.apply(p, execute=True)["writes"])
        result = self.writer.rollback(p, execute=True)
        self.assertEqual(["first-task"], result["retained_labels"])
        self.assertEqual(0, result["writes"])

    def test_drift_between_preflight_and_write_is_rejected(self):
        def edit_on_second_read(count):
            if count == 2:
                self.api.topics.append("human")
        self.api.identity_hook = edit_on_second_read
        with self.assertRaises(ExecutionError):
            self.writer.apply(plan(topics_op()), execute=True)
        self.assertEqual([], self.api.writes)

    def test_all_operations_preflight_before_first_write(self):
        before = copy.deepcopy(self.api.labels[0])
        p = plan(topics_op())
        p["targets"][0]["operations"].append({"id": "update:7", "kind": "update_label", "repository": REPO,
            "repository_id": "7", "before": before, "after": {**before, "description": "new"}})
        p["digest"] = hashlib.sha256(canonical({k: v for k, v in p.items() if k != "digest"}).encode()).hexdigest()
        self.api.labels[0]["description"] = "human"
        with self.assertRaises(ExecutionError):
            self.writer.apply(p, execute=True)
        self.assertEqual([], self.api.writes)

    def test_archived_at_api_field_blocks_assignments(self):
        p = plan(additive(self.api))
        self.api.labels[1]["archived_at"] = "2026-09-07T10:00:00Z"
        with self.assertRaises(ExecutionError):
            self.writer.apply(p, execute=True)
        self.assertEqual([], self.api.writes)

    def test_uncertain_forward_effect_is_not_owned_for_rollback(self):
        self.api.timeout_after_write = True
        p = plan(topics_op())
        with self.assertRaises(TimeoutError):
            self.writer.apply(p, execute=True)
        self.writer.apply(p, execute=True, resume=True)
        result = self.writer.rollback(p, execute=True)
        self.assertEqual(1, len(result["conflicts"]))
        self.assertEqual(0, result["writes"])

    def test_torn_last_journal_record_recovers_from_authenticated_prefix(self):
        p = plan(topics_op())
        self.writer.apply(p, execute=True)
        with self.path.open("a") as stream:
            stream.write('{"partial":')
        self.assertEqual(0, self.writer.apply(p, execute=True, resume=True)["writes"])
        self.assertTrue(any(json.loads(x)["phase"] == "recovered-tail" for x in self.path.read_text().splitlines()))

    def test_preexisting_destination_cannot_disappear_silently(self):
        self.api.issues[0]["labels"].append(copy.deepcopy(self.api.labels[1]))
        p = plan(additive(self.api))
        self.api.issues[0]["labels"] = [x for x in self.api.issues[0]["labels"] if x["id"] != 2]
        with self.assertRaises(ExecutionError):
            self.writer.apply(p, execute=True)
        self.assertEqual([], self.api.writes)

    def test_rollback_timeout_is_reported_as_uncertainty_conflict(self):
        p = plan(topics_op())
        self.writer.apply(p, execute=True)
        self.api.timeout_after_write = True
        result = self.writer.rollback(p, execute=True)
        self.assertEqual(1, len(result["conflicts"]))
        self.assertEqual(2, len(self.api.writes))
        self.assertTrue(any(json.loads(x)["phase"] == "rollback-conflict" for x in self.path.read_text().splitlines()))

    def test_distinct_journals_lock_the_same_repository_before_preflight(self):
        from metadata_journal import Journal
        p = plan(topics_op())
        keys = Path(self.tmp.name) / "keys"
        with Journal(self.path, p, keys):
            other = MetadataWriter(self.api, Path(self.tmp.name) / "other.jsonl", state_dir=keys)
            with self.assertRaises(ExecutionError):
                other.apply(p, execute=True)
        self.assertEqual([], self.api.writes)
        self.assertEqual(0, self.api.identity_reads)
        self.assertEqual(1, self.writer.apply(p, execute=True)["writes"])

    def test_visibility_drift_is_rejected_before_writes(self):
        p = plan(topics_op())
        p["targets"][0]["visibility"] = "private"
        p["digest"] = hashlib.sha256(canonical({k: v for k, v in p.items() if k != "digest"}).encode()).hexdigest()
        with self.assertRaises(ExecutionError):
            self.writer.apply(p, execute=True)
        self.assertEqual([], self.api.writes)

    def test_forged_journal_cannot_claim_human_assignment(self):
        p = plan(additive(self.api))
        self.api.issues[0]["labels"].append(copy.deepcopy(self.api.labels[1]))
        self.path.write_text(json.dumps({"plan_digest": p["digest"], "phase": "intent", "key": "add:7:issue:101"}) + "\n")
        with self.assertRaises(ExecutionError):
            self.writer.rollback(p, execute=True)
        self.assertEqual([], self.api.writes)


if __name__ == "__main__":
    unittest.main()
