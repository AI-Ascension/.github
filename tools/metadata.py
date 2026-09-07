#!/usr/bin/env python3
"""Deterministic, fail-closed metadata maintenance tooling.

The command line interface intentionally has no implicit network writes.  A
snapshot may be read from a fixture or collected with ``gh api``.  Plans are
content addressed, and ``apply``/``rollback`` require an explicit execute
switch plus an authorization document bound to the plan digest.

This module has no repository-specific topic or migration values.  Those
values belong in the reviewed metadata map and migration input supplied by an
operator.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import subprocess
import sys
import time
import urllib.parse
from collections import defaultdict
from pathlib import Path
from typing import Any, Mapping, Sequence

try:
    from metadata_execution import ExecutionError, _MetadataWriter as ExecutionMetadataWriter
except ImportError:  # pragma: no cover - direct import remains available in tools/
    ExecutionError = RuntimeError
    ExecutionMetadataWriter = None

try:
    import yaml
except ImportError:  # pragma: no cover - exercised by the CLI in minimal hosts
    yaml = None


SCHEMA_VERSION = 1
TOPIC_MAX_COUNT = 20
TOPIC_MAX_LENGTH = 50
TOPIC_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$")
SHA_RE = re.compile(r"^[0-9a-fA-F]{40}$")
LABEL_MAX_LENGTH = 50
HEX_COLOR_RE = re.compile(r"^[0-9a-fA-F]{6}$")
SAFE_REPO_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")

# These labels carry project policy rather than generic taxonomy.  A rename
# would silently change the meaning of existing contribution, proof, or
# security records, so migrations must be reviewed as a separate operation.
PROTECTED_RENAME_SOURCES = frozenset({
    "first-task",
    "proof-recipe",
    "contract-observation",
    "evidence",
    "unverified-claim",
    "security",
})

# The generic source-membership migration does not establish suitability for
# GitHub's contributor triage labels or for evidence-state labels.  In
# particular, no migration row may mass-assign one of these destinations.
UNSAFE_MIGRATION_DESTINATIONS = frozenset({
    "first-task",
    "proof-recipe",
    "contract-observation",
    "evidence",
    "unverified-claim",
    "security",
    "good first issue",
    "good-first-issue",
    "help wanted",
    "help-wanted",
})


def _label_archived(label: Mapping[str, Any], field: str = "label") -> bool:
    """Return one archive state for old and current GitHub label responses.

    GitHub has returned both an ``archived`` boolean and an ``archived_at``
    timestamp in different representations.  A timestamp is authoritative
    when present; treating it as an unarchived label would permit writes to a
    retired label.
    """

    archived = label.get("archived")
    if archived is not None and not isinstance(archived, bool):
        raise MetadataError(f"{field}.archived must be boolean when present")
    archived_at = label.get("archived_at")
    if archived_at is not None and (not isinstance(archived_at, str) or not archived_at.strip()):
        raise MetadataError(f"{field}.archived_at must be a non-empty timestamp when present")
    return bool(archived) or archived_at is not None


class MetadataError(Exception):
    """A user-correctable validation or safety error."""


class APIError(MetadataError):
    """A GitHub API failure with a stable category."""

    def __init__(self, message: str, category: str = "api", *, uncertain: bool = False, retry_after: float | None = None):
        super().__init__(message)
        self.category = category
        self.uncertain = uncertain
        self.retry_after = retry_after


def canonical_json(value: Any) -> str:
    """Serialize JSON for stable digests and machine-readable artifacts."""

    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_document(path: Path) -> Any:
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise MetadataError(f"cannot read {path}: {exc}") from exc
    try:
        if path.suffix.lower() in {".yaml", ".yml"}:
            if yaml is None:
                raise MetadataError("PyYAML is required to read YAML input")
            value = yaml.safe_load(raw)
        else:
            value = json.loads(raw)
    except (ValueError, yaml.YAMLError if yaml is not None else ValueError) as exc:
        raise MetadataError(f"invalid document {path}: {exc}") from exc
    if value is None:
        raise MetadataError(f"document {path} is empty")
    return value


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # A final newline makes artifacts pleasant to review while the digest is
    # calculated over the parsed value, not presentation whitespace.
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def fail(message: str) -> int:
    print(f"metadata: error: {message}", file=sys.stderr)
    return 2


def _as_list(value: Any, field: str) -> list[Any]:
    if not isinstance(value, list):
        raise MetadataError(f"{field} must be a list")
    return value


def _as_mapping(value: Any, field: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise MetadataError(f"{field} must be an object")
    return value


def _sha(value: Any, field: str, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str) or (not allow_empty and not value):
        raise MetadataError(f"{field} must be a SHA-1 string")
    if allow_empty and value == "":
        return value
    if not SHA_RE.fullmatch(value):
        raise MetadataError(f"{field} must contain exactly 40 hexadecimal characters")
    return value.lower()


def _repo_identity(repo: Mapping[str, Any], where: str = "repository") -> tuple[str, str, str]:
    rid = repo.get("id", repo.get("repository_id"))
    if isinstance(rid, bool) or not isinstance(rid, (str, int)) or str(rid) == "":
        raise MetadataError(f"{where}.id must be a non-empty numeric/string repository ID")
    full = repo.get("full_name")
    if not isinstance(full, str) or not SAFE_REPO_RE.fullmatch(full):
        raise MetadataError(f"{where}.full_name must be owner/name")
    name = repo.get("name")
    if not isinstance(name, str) or not name:
        raise MetadataError(f"{where}.name must be non-empty and match the source repository field")
    if name != full.rsplit("/", 1)[1]:
        raise MetadataError(f"{where}.name does not match full_name")
    return str(rid), full, name


def _topic_name(topic: Any, field: str) -> str:
    if isinstance(topic, str):
        name = topic
    elif isinstance(topic, Mapping):
        name = topic.get("name")
    else:
        name = None
    if not isinstance(name, str) or not name:
        raise MetadataError(f"{field} must contain a topic name")
    if len(name) > TOPIC_MAX_LENGTH or not TOPIC_RE.fullmatch(name):
        raise MetadataError(f"{field} topic {name!r} is not valid GitHub topic syntax/length")
    return name


def normalize_topic_entries(entries: Any, field: str) -> list[dict[str, Any]]:
    result = []
    for index, raw in enumerate(_as_list(entries, field)):
        item_field = f"{field}[{index}]"
        name = _topic_name(raw, item_field)
        if isinstance(raw, str):
            result.append({"name": name})
            continue
        item = dict(_as_mapping(raw, item_field))
        item["name"] = name
        result.append(item)
    return result


def topic_names(entries: Any, field: str = "topics") -> list[str]:
    if isinstance(entries, Mapping):
        entries = entries.get("names")
        if entries is None:
            raise MetadataError(f"{field} object must contain names")
    normalized = normalize_topic_entries(entries, field)
    names = [item["name"] for item in normalized]
    if len(names) > TOPIC_MAX_COUNT:
        raise MetadataError(f"{field} contains {len(names)} topics; GitHub permits at most {TOPIC_MAX_COUNT}")
    if len(set(names)) != len(names):
        raise MetadataError(f"{field} contains duplicate topic names")
    return names


def _evidence(item: Mapping[str, Any], field: str) -> None:
    evidence = item.get("evidence")
    if not isinstance(evidence, Mapping):
        raise MetadataError(f"{field}.evidence is required for every reviewed topic")
    source = evidence.get("repository", evidence.get("repo"))
    commit = evidence.get("commit", evidence.get("sha"))
    path = evidence.get("path")
    subject = item.get("subject", evidence.get("subject"))
    if not isinstance(source, str) or not SAFE_REPO_RE.fullmatch(source):
        raise MetadataError(f"{field}.evidence.repository must be owner/name")
    _sha(commit, f"{field}.evidence.commit")
    if not isinstance(path, str) or not path or path.startswith("/") or ".." in Path(path).parts:
        raise MetadataError(f"{field}.evidence.path must be a relative source path")
    if subject not in {"implementation", "planned"}:
        raise MetadataError(f"{field}.subject must be implementation or planned")
    meaning = item.get("meaning", evidence.get("meaning"))
    if not isinstance(meaning, str) or not meaning.strip():
        raise MetadataError(f"{field}.meaning is required")
    reason = item.get("reason")
    if not isinstance(reason, str) or not reason.strip():
        raise MetadataError(f"{field}.reason is required")


def _map_rows(metadata: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    rows = metadata.get("repositories")
    if rows is None:
        rows = metadata.get("repository")
    if rows is None:
        raise MetadataError("metadata map must contain repositories")
    rows = _as_list(rows, "repositories")
    for i, row in enumerate(rows):
        _as_mapping(row, f"repositories[{i}]")
    return rows


def normalize_metadata(metadata: Any) -> dict[str, Any]:
    root = dict(_as_mapping(metadata, "metadata"))
    version = root.get("schema_version", SCHEMA_VERSION)
    if version != SCHEMA_VERSION:
        raise MetadataError(f"unsupported metadata schema_version {version!r}")
    organization = root.get("organization")
    if not isinstance(organization, str) or not organization:
        raise MetadataError("metadata.organization is required")
    brand = root.get("brand_topic", "ai-ascension")
    _topic_name(brand, "metadata.brand_topic")
    review_status = root.get("review_status")
    if review_status not in {"reviewed", "incomplete-missing-companions", "blocked"}:
        raise MetadataError("metadata.review_status must be reviewed, incomplete-missing-companions, or blocked")
    blockers = root.get("blockers", [])
    if not isinstance(blockers, list) or any(not isinstance(x, str) or not x.strip() for x in blockers):
        raise MetadataError("metadata.blockers must be a list of non-empty strings")
    rows = []
    seen_ids: set[str] = set()
    seen_names: set[str] = set()
    for index, raw in enumerate(_map_rows(root)):
        row = dict(_as_mapping(raw, f"repositories[{index}]"))
        rid, full, name = _repo_identity(row, f"repositories[{index}]")
        if rid in seen_ids or full in seen_names:
            raise MetadataError(f"duplicate repository identity at repositories[{index}]")
        seen_ids.add(rid)
        seen_names.add(full)
        if type(row.get("managed", True)) is not bool:
            raise MetadataError(f"repositories[{index}].managed must be boolean")
        if row.get("managed") is False and not str(row.get("applicability_reason", "")).strip():
            raise MetadataError(f"repositories[{index}] unmanaged repository needs an applicability reason")
        kind = row.get("kind")
        if kind not in {"implementation", "planning", "coordination", "site", "other"}:
            raise MetadataError(f"repositories[{index}].kind must identify implementation/planning/site/etc")
        topics_raw = row.get("topics", [])
        topics = normalize_topic_entries(topics_raw, f"repositories[{index}].topics")
        names = [x["name"] for x in topics]
        if len(names) > TOPIC_MAX_COUNT or len(set(names)) != len(names):
            raise MetadataError(f"repositories[{index}].topics must have <=20 unique topics")
        for ti, item in enumerate(topics):
            _evidence(item, f"repositories[{index}].topics[{ti}]")
        removals = row.get("topic_removals", row.get("remove_topics", []))
        removal_entries = normalize_topic_entries(removals, f"repositories[{index}].topic_removals") if removals else []
        for ri, item in enumerate(removal_entries):
            _evidence(item, f"repositories[{index}].topic_removals[{ri}]")
        removal_names = [item["name"] for item in removal_entries]
        if set(names) & set(removal_names):
            raise MetadataError(f"repositories[{index}] cannot retain and remove the same topic")
        if "brand_topic_exempt" in row or "brand_topic_exempt_reason" in row:
            raise MetadataError(f"repositories[{index}] brand-topic exemptions are unsupported")
        if brand not in names:
            raise MetadataError(f"repositories[{index}] must include common brand topic {brand!r}")
        if kind == "planning":
            planning_entries = [item for item in topics if item["name"] in {"planning", "project-planning"}]
            if not planning_entries:
                raise MetadataError(
                    f"repositories[{index}] planning repository needs visible 'project-planning' topic"
                )
            if any(item.get("subject") != "planned" for item in planning_entries):
                raise MetadataError(
                    f"repositories[{index}] planning topic must have subject planned"
                )
            if not any(item.get("subject") == "planned" for item in topics):
                raise MetadataError(f"repositories[{index}] planning repository needs at least one planned topic entry")
            if any(item.get("subject") != "planned" for item in topics):
                raise MetadataError(f"repositories[{index}] planning repository cannot claim implementation topics")
        default_branch = row.get("default_branch")
        if default_branch is not None and (not isinstance(default_branch, str) or not default_branch):
            raise MetadataError(f"repositories[{index}].default_branch must be non-empty when present")
        default_commit = row.get("default_commit")
        if default_commit is not None:
            _sha(default_commit, f"repositories[{index}].default_commit")
        visibility = row.get("visibility")
        if visibility is not None and (not isinstance(visibility, str) or not visibility.strip()):
            raise MetadataError(f"repositories[{index}].visibility must be a non-empty string when present")
        archived = row.get("archived")
        if archived is not None and not isinstance(archived, bool):
            raise MetadataError(f"repositories[{index}].archived must be boolean when present")
        normalized = row
        normalized.update({"id": rid, "repository_id": rid, "full_name": full, "name": name, "topics": topics, "topic_removals": removal_entries})
        rows.append(normalized)
    if not rows:
        raise MetadataError("canonical metadata must identify at least one repository")
    root["schema_version"] = version
    root["organization"] = organization
    root["brand_topic"] = brand
    root["review_status"] = review_status
    root["blockers"] = blockers
    root["repositories"] = rows
    return root


def normalize_labels(labels: Any) -> list[dict[str, Any]]:
    if isinstance(labels, Mapping):
        labels = labels.get("labels", labels.get("definitions"))
    rows = _as_list(labels, "labels")
    result = []
    # GitHub label lookup is case-insensitive; preserve display casing but
    # reject colliding identities in shared authority data.
    seen: set[str] = set()
    for index, raw in enumerate(rows):
        item = dict(_as_mapping(raw, f"labels[{index}]"))
        if set(item) - {"name", "color", "description", "archived", "archived_at", "repository_ids", "applicability_reason"}:
            raise MetadataError(f"labels[{index}] has an unsupported definition or applicability field")
        name = item.get("name")
        color = item.get("color")
        description = item.get("description", "")
        if not isinstance(name, str) or not name or name != name.strip() or len(name) > LABEL_MAX_LENGTH or any(ord(x) < 32 or ord(x) == 127 for x in name):
            raise MetadataError(f"labels[{index}].name must be 1..50 characters")
        identity = name.casefold()
        if identity in seen:
            raise MetadataError(f"labels contains duplicate name {name!r}")
        seen.add(identity)
        if not isinstance(color, str) or not HEX_COLOR_RE.fullmatch(color):
            raise MetadataError(f"labels[{index}].color must be six hexadecimal characters")
        if not isinstance(description, str) or len(description) > 100:
            raise MetadataError(f"labels[{index}].description must be at most 100 characters")
        if "repository_ids" in item:
            scope = _as_list(item["repository_ids"], f"labels[{index}].repository_ids")
            if any(isinstance(x, bool) or not str(x).isdigit() or int(str(x)) < 1 for x in scope):
                raise MetadataError(f"labels[{index}].repository_ids must be positive repository IDs")
            normalized_scope = sorted(str(x) for x in scope)
            if len(set(normalized_scope)) != len(normalized_scope):
                raise MetadataError(f"labels[{index}].repository_ids contains duplicates")
            item["repository_ids"] = normalized_scope
        item.update({
            "name": name,
            "color": color.upper(),
            "description": description,
            "archived": _label_archived(item, f"labels[{index}]"),
        })
        result.append(item)
    return result


def _current_topics(snapshot_repo: Mapping[str, Any]) -> list[str]:
    topics = snapshot_repo.get("topics", [])
    if isinstance(topics, Mapping):
        topics = topics.get("names", [])
    names = topic_names(topics, "snapshot.topics")
    return sorted(set(names))


def _snapshot_repos(snapshot: Any) -> list[dict[str, Any]]:
    if isinstance(snapshot, list):
        rows = snapshot
    elif isinstance(snapshot, Mapping):
        rows = snapshot.get("repositories")
        if rows is None:
            # A single audit file is accepted for convenient verification.
            rows = [snapshot]
    else:
        raise MetadataError("snapshot must be an object with repositories or a list")
    result = []
    seen_ids: set[str] = set()
    seen_names: set[str] = set()
    for i, raw in enumerate(rows):
        row = dict(_as_mapping(raw, f"snapshot.repositories[{i}]"))
        if "repository" in row:
            repository = dict(_as_mapping(row["repository"], f"snapshot.repositories[{i}].repository"))
            for key in ("topics", "labels", "issues", "default_commit", "branches", "tags", "releases", "tree"):
                if key in row and key not in repository:
                    repository[key] = row[key]
            row = repository | {k: v for k, v in row.items() if k != "repository"}
        rid, full, name = _repo_identity(row, f"snapshot.repositories[{i}]")
        if rid in seen_ids or full in seen_names:
            raise MetadataError(f"snapshot contains duplicate repository {full}")
        seen_ids.add(rid)
        seen_names.add(full)
        archived = row.get("archived")
        if not isinstance(archived, bool):
            raise MetadataError(f"snapshot {full}.archived must be boolean")
        visibility = row.get("visibility")
        if visibility not in {"public", "private", "internal"}:
            raise MetadataError(f"snapshot {full}.visibility must be explicitly queried")
        row["archived"] = archived
        row["visibility"] = visibility
        branch = row.get("default_branch")
        if not isinstance(branch, str) or not branch:
            raise MetadataError(f"snapshot {full} has no actual default_branch")
        commit = row.get("default_commit")
        if isinstance(commit, Mapping):
            commit = commit.get("sha")
        _sha(commit, f"snapshot {full}.default_commit")
        for required in ("topics", "labels", "issues"):
            if required not in row or row[required] is None:
                raise MetadataError(f"snapshot {full} is missing queried field {required}; unknown is not empty")
        topic_names(row["topics"], f"snapshot {full}.topics")
        labels = row["labels"]
        if isinstance(labels, Mapping):
            labels = labels.get("labels", [])
        _as_list(labels, f"snapshot {full}.labels")
        _as_list(row["issues"], f"snapshot {full}.issues")
        result.append(row)
    return sorted(result, key=lambda r: (str(r["id"]), r["full_name"]))


def normalize_snapshot(snapshot: Any) -> dict[str, Any]:
    if isinstance(snapshot, Mapping) and snapshot.get("schema_version") == SCHEMA_VERSION and "repositories" in snapshot:
        root = dict(snapshot)
    else:
        root = {"schema_version": SCHEMA_VERSION, "repositories": _snapshot_repos(snapshot)}
    root["schema_version"] = SCHEMA_VERSION
    root["repositories"] = _snapshot_repos(root)
    # Observational timestamps are useful audit data but must not make plan
    # digests drift when the same input is regenerated.
    root.setdefault("source", "fixture")
    return root


def _label_usage(repo: Mapping[str, Any]) -> dict[str, list[dict[str, Any]]]:
    usage: dict[str, list[dict[str, Any]]] = defaultdict(list)
    explicit = repo.get("label_usage")
    if isinstance(explicit, Mapping):
        for name, rows in explicit.items():
            if isinstance(rows, list):
                usage[str(name)] = [dict(x) for x in rows if isinstance(x, Mapping)]
    issues = repo.get("issues", [])
    if isinstance(issues, list):
        for issue in issues:
            if not isinstance(issue, Mapping):
                continue
            number = issue.get("number")
            for label in issue.get("labels", []) or []:
                if isinstance(label, Mapping):
                    name = label.get("name")
                else:
                    name = label
                if isinstance(name, str):
                    usage[name].append({"number": number, "issue_id": issue.get("id")})
    for name in list(usage):
        unique = {(x.get("number"), x.get("issue_id")): x for x in usage[name]}
        usage[name] = [unique[key] for key in sorted(unique, key=lambda x: (str(x[0]), str(x[1])))]
    return dict(sorted(usage.items()))


def normalize_migrations(migrations: Any) -> list[dict[str, Any]]:
    if isinstance(migrations, Mapping):
        rows = migrations.get("migrations")
        if rows is None:
            # Allow repository keyed mapping only when every value is a list.
            rows = []
            for repository, values in migrations.items():
                if repository in {"schema_version", "organization", "generated_at"}:
                    continue
                if not isinstance(values, list):
                    raise MetadataError("migration mapping values must be lists")
                for value in values:
                    item = dict(_as_mapping(value, f"migrations.{repository}"))
                    item.setdefault("repository", repository)
                    rows.append(item)
    else:
        rows = migrations
    rows = _as_list(rows, "migrations")
    result = []
    seen: set[tuple[str, str, str]] = set()
    for index, raw in enumerate(rows):
        item = dict(_as_mapping(raw, f"migrations[{index}]"))
        repository = item.get("repository", item.get("full_name"))
        if not isinstance(repository, str) or not SAFE_REPO_RE.fullmatch(repository):
            raise MetadataError(f"migrations[{index}].repository must be owner/name")
        source = item.get("from", item.get("source"))
        destination = item.get("to", item.get("destination"))
        if not isinstance(source, str) or not source or len(source) > LABEL_MAX_LENGTH:
            raise MetadataError(f"migrations[{index}].from must be a label name")
        if not isinstance(destination, str) or not destination or len(destination) > LABEL_MAX_LENGTH:
            raise MetadataError(f"migrations[{index}].to must be a label name")
        if any(name != name.strip() or any(ord(x) < 32 or ord(x) == 127 for x in name) for name in (source, destination)):
            raise MetadataError(f"migrations[{index}] contains whitespace or control characters at a label boundary")
        if source.casefold() == destination.casefold():
            raise MetadataError(f"migrations[{index}] source and destination are identical")
        strategy = item.get("strategy", "rename")
        if strategy not in {"rename", "additive"}:
            raise MetadataError(f"migrations[{index}].strategy must be rename or additive")
        source_key = source.casefold()
        destination_key = destination.casefold()
        if strategy == "rename" and source_key in PROTECTED_RENAME_SOURCES:
            raise MetadataError(
                f"migrations[{index}] cannot rename protected label {source!r}; preserve its project meaning and review a separate migration"
            )
        normalized_destination = destination_key.replace("_", "-")
        if (
            destination_key in UNSAFE_MIGRATION_DESTINATIONS
            or normalized_destination in UNSAFE_MIGRATION_DESTINATIONS
            or destination_key.startswith("priority")
            or destination_key.startswith("evidence status")
            or destination_key.startswith("evidence-")
        ):
            raise MetadataError(
                f"migrations[{index}] cannot automatically assign destination label {destination!r}; suitability requires an explicit reviewed assignment"
            )
        key = (repository, source.casefold(), destination.casefold())
        if key in seen:
            raise MetadataError(f"duplicate migration {repository}: {source} -> {destination}")
        seen.add(key)
        item.update({"repository": repository, "from": source, "to": destination, "strategy": strategy})
        result.append(item)
    return sorted(result, key=lambda x: (x["repository"], x["from"], x["to"]))


def _topics_digest(names: Sequence[str]) -> str:
    return digest(sorted(names))


def _labels_digest(labels: Sequence[Mapping[str, Any]]) -> str:
    reduced = []
    for row in labels:
        reduced.append({
            "id": row.get("id"),
            "name": row.get("name"),
            "color": row.get("color"),
            "description": row.get("description", ""),
            "archived": _label_archived(row),
        })
    return digest(sorted(reduced, key=lambda x: (str(x.get("id")), str(x.get("name")))))


def validate_snapshot(snapshot: Any) -> dict[str, Any]:
    normalized = normalize_snapshot(snapshot)
    warnings: list[str] = []
    for row in normalized["repositories"]:
        full = row["full_name"]
        default = row.get("default_commit")
        commit = default.get("sha") if isinstance(default, Mapping) else default
        # Some audit collectors retain the commit endpoint's tree wrapper at
        # ``tree.sha``.  A tree SHA is rejected only when the source explicitly
        # identifies it as a tree object; equality with an unlabeled sidecar
        # field alone is not enough to relabel a valid commit.
        tree = row.get("tree")
        if isinstance(tree, Mapping) and tree.get("object_type") == "tree" and tree.get("sha") == commit:
            raise MetadataError(f"snapshot {full} uses a tree SHA as default_commit")
        labels = row.get("labels", [])
        labels_wrapped = isinstance(labels, Mapping)
        if labels_wrapped:
            labels = labels.get("labels", [])
        labels = _as_list(labels, f"snapshot {full}.labels")
        seen_ids: set[str] = set()
        seen_names: set[str] = set()
        normalized_labels: list[dict[str, Any]] = []
        for label_index, label in enumerate(labels):
            if not isinstance(label, Mapping):
                raise MetadataError(f"snapshot {full} has malformed label row")
            label = dict(label)
            name = label.get("name")
            if not isinstance(name, str) or not name:
                raise MetadataError(f"snapshot {full} has label without name")
            if label.get("id") is None:
                raise MetadataError(f"snapshot {full} label {name!r} has no stable ID")
            identity = name.casefold()
            if identity in seen_names:
                raise MetadataError(f"snapshot {full} repeats label {name!r}")
            seen_names.add(identity)
            sid = str(label["id"])
            if sid in seen_ids:
                raise MetadataError(f"snapshot {full} repeats label ID {sid!r}")
            seen_ids.add(sid)
            label["archived"] = _label_archived(label, f"snapshot {full}.labels[{label_index}]")
            normalized_labels.append(label)
        row["labels"] = {"labels": normalized_labels} if labels_wrapped else normalized_labels
        if row.get("issues") is None:
            warnings.append(f"{full}: issue/PR label usage was not queried")
    normalized["validation"] = {"ok": True, "warnings": sorted(warnings)}
    return normalized


def _evidence_commit(item: Mapping[str, Any]) -> str:
    evidence = _as_mapping(item.get("evidence"), "topic.evidence")
    return str(evidence.get("commit", evidence.get("sha", ""))).lower()


def _evidence_path(item: Mapping[str, Any]) -> str:
    evidence = _as_mapping(item.get("evidence"), "topic.evidence")
    return str(evidence.get("path", ""))


def _tree_paths(source: Mapping[str, Any]) -> set[str] | None:
    """Return complete tree paths, or ``None`` when the audit is incomplete."""

    tree = source.get("tree")
    if not isinstance(tree, Mapping) or tree.get("truncated") is True:
        return None
    entries = tree.get("tree")
    if not isinstance(entries, list):
        return None
    paths: set[str] = set()
    for entry in entries:
        if not isinstance(entry, Mapping) or not isinstance(entry.get("path"), str):
            return None
        paths.add(entry["path"])
    return paths


def _validate_evidence_against_snapshot(meta: Mapping[str, Any], snap: Mapping[str, Any]) -> dict[str, Any]:
    """Check source pins when the complete source audit is available.

    A source row that is absent or has no complete tree cannot prove its
    evidence path in an offline snapshot.  It becomes a review blocker rather
    than being treated as verified.  A source commit mismatch or a missing
    path in a complete tree is an integrity error and aborts planning.
    """

    by_name = {row["full_name"]: row for row in snap["repositories"]}
    unavailable: list[str] = []
    checked = 0
    for repository in meta["repositories"]:
        if repository.get("managed") is False:
            continue
        entries = list(repository.get("topics", [])) + list(repository.get("topic_removals", []))
        for topic in entries:
            evidence = _as_mapping(topic.get("evidence"), f"{repository['full_name']}.topic.evidence")
            source_name = evidence.get("repository", evidence.get("repo"))
            source = by_name.get(source_name) if isinstance(source_name, str) else None
            path = _evidence_path(topic)
            commit = _evidence_commit(topic)
            if source is None:
                unavailable.append(f"{repository['full_name']}:{topic['name']}: source audit {source_name!r} is unavailable")
                continue
            actual_commit = _commit_sha(source)
            if commit != actual_commit:
                raise MetadataError(
                    f"{repository['full_name']} topic {topic['name']!r} evidence commit {commit!r} "
                    f"does not match audited source commit {actual_commit!r} for {source_name}"
                )
            tree = source.get("tree")
            if isinstance(tree, Mapping):
                tree_sha = tree.get("sha")
                # A tree object is never a commit pin.  Some collectors expose
                # an explicit object type; reject that ambiguity even when
                # the hexadecimal values happen to match.
                if tree.get("object_type") == "tree" and tree_sha == commit:
                    raise MetadataError(
                        f"{repository['full_name']} topic {topic['name']!r} evidence uses a tree SHA as commit"
                    )
            paths = _tree_paths(source)
            if paths is None:
                unavailable.append(f"{repository['full_name']}:{topic['name']}: source tree for {source_name} is unavailable or truncated")
                continue
            if path not in paths:
                raise MetadataError(
                    f"{repository['full_name']} topic {topic['name']!r} evidence path {path!r} "
                    f"is absent from audited commit {commit}"
                )
            checked += 1
    return {"ok": not unavailable, "checked": checked, "unavailable": sorted(unavailable)}


def _normalize_repository_selection(
    repository_ids: Sequence[Any] | Any | None,
    meta: Mapping[str, Any],
    snap: Mapping[str, Any],
) -> tuple[list[str], bool]:
    """Validate a repeatable canary selection against the complete inputs."""

    all_ids = sorted({str(row["id"]) for row in meta["repositories"] if row.get("managed") is not False})
    snapshot_ids = {str(row["id"]) for row in snap["repositories"]}
    if repository_ids is None:
        return all_ids, False
    if isinstance(repository_ids, (str, int)) and not isinstance(repository_ids, bool):
        values: list[Any] = [repository_ids]
    else:
        if isinstance(repository_ids, (bytes, bytearray)) or not isinstance(repository_ids, Sequence):
            raise MetadataError("repository selection must contain one or more repository IDs")
        values = list(repository_ids)
    if not values:
        raise MetadataError("repository selection must contain at least one repository ID")
    selected: list[str] = []
    seen: set[str] = set()
    for value in values:
        if isinstance(value, bool) or not isinstance(value, (str, int)) or str(value).strip() == "":
            raise MetadataError("--repository-id values must be non-empty numeric/string IDs")
        identifier = str(value)
        if identifier in seen:
            raise MetadataError(f"duplicate --repository-id {identifier!r}")
        seen.add(identifier)
        if identifier not in all_ids:
            raise MetadataError(f"unknown --repository-id {identifier!r}; it is absent from the canonical map")
        if identifier not in snapshot_ids:
            raise MetadataError(f"--repository-id {identifier!r} is absent from the complete snapshot")
        selected.append(identifier)
    return sorted(selected), True


def _label_applicability(metadata, labels):
    known = {str(row["id"]) for row in metadata["repositories"]}
    for label in labels or []:
        if set(label.get("repository_ids", [])) - known:
            raise MetadataError("label applicability names an unknown repository ID")


def _inventory_applicability(metadata: Mapping[str, Any], snapshot: Mapping[str, Any]) -> None:
    """Unlisted discoveries require a recorded exclusion, never silent omission.

    Exclusions stay in the local snapshot so private identities need not enter
    the public registry. They cannot authorize a write to an excluded target.
    """
    known = {str(row["id"]) for row in metadata["repositories"]}
    observed = {str(row["id"]) for row in snapshot["repositories"]}
    excluded = set()
    for row in _as_list(snapshot.get("applicability_exclusions", []), "snapshot.applicability_exclusions"):
        item = _as_mapping(row, "applicability exclusion")
        identifier = str(item.get("repository_id", ""))
        if (identifier not in observed or identifier in known or identifier in excluded
                or item.get("decision") != "excluded-pending-owner"
                or not isinstance(item.get("reason"), str) or not item["reason"].strip()):
            raise MetadataError("invalid, overlapping, or unexplained repository exclusion")
        excluded.add(identifier)
    if observed - known - excluded:
        raise MetadataError("unlisted repositories require an explicit applicability decision in the local snapshot")


def validate_metadata(metadata: Any, labels: Any | None = None, snapshot: Any | None = None) -> dict[str, Any]:
    normalized = normalize_metadata(metadata)
    labels_result = normalize_labels(labels) if labels is not None else None
    _label_applicability(normalized, labels_result)
    snapshot_result = validate_snapshot(snapshot) if snapshot is not None else None
    if snapshot_result is not None:
        _inventory_applicability(normalized, snapshot_result)
        by_id = {str(x["id"]): x for x in snapshot_result["repositories"]}
        by_name = {x["full_name"]: x for x in snapshot_result["repositories"]}
        for row in normalized["repositories"]:
            if row.get("managed") is False:
                continue
            current = by_id.get(str(row["id"]))
            if current is None:
                current = by_name.get(row["full_name"])
            if current is None:
                raise MetadataError(f"metadata repository {row['full_name']} is absent from snapshot")
            if str(current["id"]) != str(row["id"]):
                raise MetadataError(f"repository identity mismatch for {row['full_name']}")
            if current.get("archived", False):
                raise MetadataError(f"repository {row['full_name']} is archived; metadata writes are forbidden")
            if row.get("default_branch") and row["default_branch"] != current.get("default_branch"):
                raise MetadataError(f"default branch drift for {row['full_name']}")
            if row.get("default_commit"):
                actual = current.get("default_commit")
                actual = actual.get("sha") if isinstance(actual, Mapping) else actual
                if row["default_commit"] != actual:
                    raise MetadataError(f"default commit drift for {row['full_name']}")
            if row.get("visibility") and row["visibility"] != current.get("visibility"):
                raise MetadataError(f"visibility drift for {row['full_name']}")
            if row.get("archived") is not None and row["archived"] != current.get("archived", False):
                raise MetadataError(f"archive state drift for {row['full_name']}")
    evidence_result = _validate_evidence_against_snapshot(normalized, snapshot_result) if snapshot_result is not None else None
    return {"metadata": normalized, "labels": labels_result, "snapshot": snapshot_result, "evidence": evidence_result, "ok": True}


def _desired_topics(row: Mapping[str, Any], current: Sequence[str]) -> tuple[list[str], list[str]]:
    current_set = set(current)
    additions = [x["name"] for x in row.get("topics", [])]
    removals = [x.get("name") if isinstance(x, Mapping) else x for x in row.get("topic_removals", [])]
    replace = bool(row.get("replace_topics", False))
    if replace:
        desired = set(additions)
        # A complete replacement must explicitly account for every current
        # topic that disappears.  This prevents accidental truncation.
        missing_reviews = sorted(current_set - desired - set(removals))
        if missing_reviews:
            raise MetadataError(
                f"{row['full_name']} complete topic replacement omits current topics without explicit removal: {', '.join(missing_reviews)}"
            )
    else:
        desired = current_set | set(additions)
    desired -= set(removals)
    if len(desired) > TOPIC_MAX_COUNT:
        raise MetadataError(f"{row['full_name']} desired topic set has {len(desired)} entries; refusing truncation")
    return sorted(desired), sorted(current_set - desired)


def _labels_by_name(repo: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    rows = repo.get("labels", [])
    if isinstance(rows, Mapping):
        rows = rows.get("labels", [])
    result: dict[str, dict[str, Any]] = {}
    for x in rows:
        if not isinstance(x, Mapping) or x.get("name") is None:
            continue
        value = dict(x)
        value["archived"] = _label_archived(value, f"{repo.get('full_name')}.labels")
        result[str(value["name"]).casefold()] = value
    return result


def _issue_assignment_rows(repo: Mapping[str, Any], source: str, destination: str | None = None) -> list[dict[str, Any]]:
    """Capture complete issue label identities for a conservative migration."""
    rows = repo.get("issues")
    if not isinstance(rows, list):
        raise MetadataError(f"{repo.get('full_name')}: complete issue/PR usage is required for label migration")
    result: list[dict[str, Any]] = []
    for issue in rows:
        if not isinstance(issue, Mapping) or issue.get("number") is None:
            continue
        if not isinstance(issue.get("id"), int):
            raise MetadataError(f"{repo.get('full_name')} issue {issue.get('number')} has no stable issue ID")
        labels: list[dict[str, Any]] = []
        has_source = False
        has_destination = False
        for label in issue.get("labels", []) or []:
            if isinstance(label, Mapping):
                name = label.get("name")
                label_id = label.get("id")
                if not isinstance(label_id, int) or not isinstance(name, str) or not name:
                    raise MetadataError(f"{repo.get('full_name')} issue {issue['number']} has unknown label identity")
                labels.append({"id": label_id, "name": name})
            else:
                raise MetadataError(f"{repo.get('full_name')} issue {issue['number']} has malformed label identity")
            if isinstance(name, str) and name.casefold() == source.casefold():
                has_source = True
            if destination and isinstance(name, str) and name.casefold() == destination.casefold():
                has_destination = True
        if has_source:
            result.append({
                "issue_id": issue["id"],
                "number": issue["number"],
                # The execution engine consumes this complete pre-write list;
                # retaining every identity prevents replacing an issue's
                # unrelated labels during a migration.
                "labels": labels,
                "destination_preexisting": has_destination,
            })
    return sorted(result, key=lambda x: (str(x.get("number")), str(x.get("issue_id"))))


def make_plan(
    metadata: Any,
    snapshot: Any,
    labels: Any | None = None,
    migrations: Any | None = None,
    *,
    operator: str | None = None,
    authorization_id: str | None = None,
    repository_ids: Sequence[Any] | Any | None = None,
    repository_id: Any | None = None,
) -> dict[str, Any]:
    meta = normalize_metadata(metadata)
    snap = validate_snapshot(snapshot)
    _inventory_applicability(meta, snap)
    if repository_ids is not None and repository_id is not None:
        raise MetadataError("use only one of repository_ids and repository_id")
    if repository_id is not None:
        repository_ids = [repository_id]
    selected_ids, selection_explicit = _normalize_repository_selection(repository_ids, meta, snap)
    evidence_result = _validate_evidence_against_snapshot(meta, snap)
    shared_labels = normalize_labels(labels) if labels is not None else []
    _label_applicability(meta, shared_labels)
    migration_rows = normalize_migrations(migrations) if migrations is not None else []
    current_by_id = {str(x["id"]): x for x in snap["repositories"]}
    current_by_name = {x["full_name"]: x for x in snap["repositories"]}
    targets: list[dict[str, Any]] = []
    for row in meta["repositories"]:
        if row.get("managed") is False:
            continue
        current = current_by_id.get(str(row["id"])) or current_by_name.get(row["full_name"])
        if current is None:
            raise MetadataError(f"metadata target {row['full_name']} is absent from snapshot")
        if str(current["id"]) != str(row["id"]):
            raise MetadataError(f"metadata target ID mismatch for {row['full_name']}")
        if current["full_name"] != row["full_name"]:
            raise MetadataError(f"metadata owner/name drift for repository ID {row['id']}")
        if current.get("archived", False):
            raise MetadataError(f"{row['full_name']} is archived; metadata writes are forbidden")
        if row.get("archived") is not None and row["archived"] is not False:
            raise MetadataError(f"{row['full_name']} is marked archived; metadata writes are forbidden")
        if row.get("archived") is not None and row["archived"] != current.get("archived", False):
            raise MetadataError(f"metadata archive state drift for {row['full_name']}")
        if row.get("visibility") and row["visibility"] != current.get("visibility"):
            raise MetadataError(f"metadata visibility drift for {row['full_name']}")
        if row.get("default_branch") and row["default_branch"] != current.get("default_branch"):
            raise MetadataError(f"metadata default branch drift for {row['full_name']}")
        if row.get("default_commit") and row["default_commit"] != _commit_sha(current):
            raise MetadataError(f"metadata default commit drift for {row['full_name']}")
        current_topics = _current_topics(current)
        desired_topics, removed = _desired_topics(row, current_topics)
        operations: list[dict[str, Any]] = []
        if desired_topics != current_topics:
            operations.append({
                "id": f"topics:{current['id']}",
                "kind": "replace_topics",
                "repository_id": str(current["id"]),
                "repository": current["full_name"],
                "before": current_topics,
                "after": desired_topics,
                "precondition": {"default_branch": current["default_branch"], "default_commit": _commit_sha(current), "visibility": current.get("visibility", "unknown"), "archived": False, "topics_digest": _topics_digest(current_topics)},
                "reviewed_removals": removed,
            })
        repo_labels = _labels_by_name(current)
        # Plan one deterministic state machine per repository.  Definitions
        # which are needed by a migration are reconciled before the migration;
        # every later operation then sees the exact virtual definition and
        # assignment state produced by the preceding operation.
        virtual_labels = copy.deepcopy(repo_labels)
        repository_keys = {str(current["id"]), current["full_name"]}
        repo_shared_labels = [
            definition for definition in shared_labels
            if definition.get("repository_ids") is None
            or any(str(identifier) in repository_keys for identifier in definition["repository_ids"])
        ]
        virtual_issues: list[dict[str, Any]] = [
            copy.deepcopy(issue) for issue in current.get("issues", [])
            if isinstance(issue, Mapping)
        ]
        repo_migrations = [m for m in migration_rows if m["repository"] == current["full_name"]]
        touched_migration_names: set[str] = set()
        migration_destination_keys = {m["to"].casefold() for m in repo_migrations}
        rename_source_keys = {m["from"].casefold() for m in repo_migrations if m["strategy"] == "rename"}

        def virtual_labels_digest() -> str:
            return _labels_digest(list(virtual_labels.values()))

        def virtual_assignment_rows(source_name: str, destination_name: str | None = None) -> list[dict[str, Any]]:
            rows: list[dict[str, Any]] = []
            for issue in virtual_issues:
                if not isinstance(issue.get("id"), int) or issue.get("number") is None:
                    continue
                labels_for_issue: list[dict[str, Any]] = []
                has_source = False
                has_destination = False
                for label in issue.get("labels", []) or []:
                    if not isinstance(label, Mapping):
                        raise MetadataError(f"{current['full_name']} issue {issue['number']} has malformed label identity")
                    label_id = label.get("id")
                    if not (isinstance(label_id, int) or label_id == "new") or not isinstance(label.get("name"), str) or not label["name"]:
                        raise MetadataError(f"{current['full_name']} issue {issue['number']} has unknown label identity")
                    labels_for_issue.append({"id": label_id, "name": label["name"]})
                    has_source |= label["name"].casefold() == source_name.casefold()
                    has_destination |= bool(destination_name) and label["name"].casefold() == destination_name.casefold()
                if has_source:
                    rows.append({
                        "issue_id": issue["id"],
                        "number": issue["number"],
                        "labels": labels_for_issue,
                        "destination_preexisting": has_destination,
                    })
            return sorted(rows, key=lambda x: (str(x["number"]), str(x["issue_id"])))

        def set_operation_sequence(operation: dict[str, Any]) -> None:
            # The sequence is part of the reviewed plan and is intentionally
            # assigned before the plan digest is calculated.
            operation["sequence"] = len(operations)

        for migration in repo_migrations:
            source = migration["from"]
            destination = migration["to"]
            overlap = {source.casefold(), destination.casefold()} & touched_migration_names
            if overlap:
                raise MetadataError(f"{current['full_name']}: overlapping label migrations require separate reviewed waves: {', '.join(sorted(overlap))}")
            touched_migration_names.update({source.casefold(), destination.casefold()})
            initial_source = repo_labels.get(source.casefold())
            if initial_source is None:
                # A completed in-place rename is represented by the same
                # stable label ID under its reviewed destination name.  Treat
                # that exact state as converged so a fresh plan remains safe
                # and deterministic; an absent source without this identity
                # proof still fails closed.
                stable_id = migration.get("stable_label_id")
                if stable_id is None:
                    stable_id = migration.get("source_label_id")
                settled_destination = repo_labels.get(destination.casefold())
                if (migration["strategy"] == "rename" and type(stable_id) is int and stable_id > 0
                        and settled_destination is not None and settled_destination.get("id") == stable_id):
                    continue
                raise MetadataError(f"{current['full_name']}: source label {source!r} is absent")
            src = virtual_labels.get(source.casefold())
            dst = virtual_labels.get(destination.casefold())
            if src is None:
                raise MetadataError(f"{current['full_name']}: source label {source!r} is absent")
            if src.get("id") is None or src.get("id") == "new":
                raise MetadataError(f"{current['full_name']}: source label {source!r} has no stable ID")
            if _label_archived(src, f"{current['full_name']}.labels.{source}"):
                raise MetadataError(f"{current['full_name']}: archived source label {source!r} cannot be migrated")
            if dst is not None and _label_archived(dst, f"{current['full_name']}.labels.{destination}"):
                raise MetadataError(f"{current['full_name']}: archived destination label {destination!r} cannot receive assignments")
            label_digest_before = virtual_labels_digest()
            if migration["strategy"] == "rename":
                if dst is not None:
                    raise MetadataError(f"{current['full_name']}: rename destination {destination!r} already exists; use additive strategy")
                shared_destination = next((x for x in repo_shared_labels if str(x.get("name", "")).casefold() == destination.casefold()), None)
                after_color = shared_destination["color"] if shared_destination else src.get("color")
                after_description = shared_destination.get("description", "") if shared_destination else src.get("description", "")
                source_name = str(src.get("name", source))
                assignment_rows = virtual_assignment_rows(source_name)
                operation = {
                    "id": f"label-rename:{current['id']}:{src.get('id', source)}",
                    "kind": "rename_label",
                    "repository_id": str(current["id"]),
                    "repository": current["full_name"],
                    "label_id": src.get("id"),
                    "from": source_name,
                    "to": destination,
                    "assignments": assignment_rows,
                    "before": {"id": src.get("id"), "name": source_name, "color": src.get("color"), "description": src.get("description", ""), "archived": _label_archived(src)},
                    "after": {"id": src.get("id"), "name": destination, "color": after_color, "description": after_description, "archived": _label_archived(src)},
                    "precondition": {"label_id": src.get("id"), "label_digest": label_digest_before, "visibility": current.get("visibility", "unknown"), "archived": False},
                }
                set_operation_sequence(operation)
                operations.append(operation)
                virtual_labels.pop(source.casefold(), None)
                virtual_labels[destination.casefold()] = {
                    **copy.deepcopy(src),
                    "name": destination,
                    "color": after_color,
                    "description": after_description,
                }
                for issue in virtual_issues:
                    for assigned in issue.get("labels", []) or []:
                        if isinstance(assigned, Mapping) and str(assigned.get("id")) == str(src.get("id")):
                            assigned["name"] = destination
            else:
                source_name = str(src.get("name", source))
                destination_name = str(dst.get("name", destination)) if dst else destination
                assignment_rows = virtual_assignment_rows(source_name, destination_name)
                if dst is None:
                    definition = next((x for x in repo_shared_labels if str(x.get("name", "")).casefold() == destination.casefold()), None)
                    if definition is None:
                        raise MetadataError(f"{current['full_name']}: additive destination {destination!r} is absent from labels.yml")
                    if _label_archived(definition, f"labels.yml.{destination}"):
                        raise MetadataError(f"{current['full_name']}: labels.yml destination {destination!r} is archived")
                    create = {"name": destination, "color": definition["color"], "description": definition.get("description", "")}
                else:
                    create = None
                operation = {
                    "id": f"label-additive:{current['id']}:{source}->{destination}",
                    "kind": "additive_label_migration",
                    "repository_id": str(current["id"]),
                    "repository": current["full_name"],
                    "from": source_name,
                    "to": destination_name,
                    "source_label_id": src.get("id"),
                    "destination_label_id": dst.get("id") if dst else None,
                    "source_definition": {"id": src.get("id"), "name": source_name, "color": str(src.get("color", "")).upper(), "description": src.get("description", ""), "archived": _label_archived(src)},
                    "destination_definition": ({"id": dst.get("id"), "name": destination_name, "color": str(dst.get("color", "")).upper(), "description": dst.get("description", ""), "archived": _label_archived(dst)} if dst else None),
                    "create": create,
                    "assignments": assignment_rows,
                    "precondition": {"labels_digest": label_digest_before, "source_label_id": src.get("id"), "destination_label_id": dst.get("id") if dst else None, "visibility": current.get("visibility", "unknown"), "archived": False},
                }
                set_operation_sequence(operation)
                operations.append(operation)
                if dst is None and create is not None:
                    virtual_labels[destination.casefold()] = {"id": "new", **copy.deepcopy(create), "archived": False}
                    dst = virtual_labels[destination.casefold()]
                for assignment in assignment_rows:
                    if assignment["destination_preexisting"]:
                        continue
                    issue = next((x for x in virtual_issues if x.get("id") == assignment["issue_id"]), None)
                    if issue is not None:
                        issue.setdefault("labels", []).append({"id": dst["id"], "name": dst["name"]})

        # Reconcile the shared definitions after migrations.  This ordering is
        # deliberate: migration effects guard the definitions observed in the
        # source snapshot, then a later definition operation records the
        # canonical update as its own reversible journal effect.
        retired_label_names = {
            migration["from"].casefold()
            for migration in repo_migrations
            if migration["strategy"] == "rename"
        }
        for definition in repo_shared_labels:
            name = str(definition["name"])
            key = name.casefold()
            if key in retired_label_names:
                continue
            existing = virtual_labels.get(key)
            if existing is None:
                # A migration-created destination is already represented by
                # its additive operation and must not be created twice.
                if key in migration_destination_keys:
                    continue
                after = {"id": "new", "name": name, "color": definition["color"], "description": definition.get("description", ""), "archived": False}
                operation = {
                    "id": f"label-create:{current['id']}:{name}",
                    "kind": "create_label",
                    "repository_id": str(current["id"]),
                    "repository": current["full_name"],
                    "before": None,
                    "after": after,
                    "precondition": {"labels_digest": virtual_labels_digest(), "visibility": current.get("visibility", "unknown"), "archived": False},
                }
                set_operation_sequence(operation)
                operations.append(operation)
                virtual_labels[key] = copy.deepcopy(after)
            elif existing.get("id") != "new":
                before = {"id": existing.get("id"), "name": existing.get("name", name), "color": str(existing.get("color", "")).upper(), "description": existing.get("description", ""), "archived": _label_archived(existing)}
                after = {"id": before["id"], "name": before["name"], "color": definition["color"], "description": definition.get("description", ""), "archived": before["archived"]}
                if before["color"].upper() != after["color"].upper() or before["description"] != after["description"]:
                    if before["archived"]:
                        raise MetadataError(f"{current['full_name']}: archived shared label {name!r} cannot be updated")
                    operation = {
                        "id": f"label-update:{current['id']}:{before['id']}",
                        "kind": "update_label",
                        "repository_id": str(current["id"]),
                        "repository": current["full_name"],
                        "label_id": before["id"],
                        "before": before,
                        "after": after,
                        "precondition": {"labels_digest": virtual_labels_digest(), "visibility": current.get("visibility", "unknown"), "archived": False},
                    }
                    set_operation_sequence(operation)
                    operations.append(operation)
                    virtual_labels[key] = copy.deepcopy(after)

        # Bind each migration to the definition state reached by the complete
        # operation sequence.  The executor uses these fields to recognize a
        # settled migration after a later canonical definition update.
        for operation in operations:
            if operation["kind"] != "additive_label_migration":
                continue
            source_final = virtual_labels.get(operation["from"].casefold())
            destination_final = virtual_labels.get(operation["to"].casefold())
            if source_final is not None:
                operation["final_source_definition"] = {
                    "id": source_final.get("id"), "name": source_final.get("name", operation["from"]),
                    "color": str(source_final.get("color", "")).upper(), "description": source_final.get("description", ""),
                    "archived": _label_archived(source_final),
                }
            if destination_final is not None:
                operation["final_destination_definition"] = {
                    "id": destination_final.get("id"), "name": destination_final.get("name", operation["to"]),
                    "color": str(destination_final.get("color", "")).upper(), "description": destination_final.get("description", ""),
                    "archived": _label_archived(destination_final),
                }

        # Preserve the immediate snapshots above for execution/rollback, and
        # attach one final projection to every migration.  The executor uses
        # this projection to recognize a later migration's settled state on a
        # second apply without mistaking it for unrelated human drift.
        final_issues = {str(x.get("id")): x for x in virtual_issues if x.get("id") is not None}
        for operation in operations:
            if operation["kind"] not in {"rename_label", "additive_label_migration"}:
                continue
            final_rows: list[dict[str, Any]] = []
            for assignment in operation.get("assignments", []):
                issue = final_issues.get(str(assignment.get("issue_id")))
                if issue is None:
                    continue
                final_rows.append({
                    "issue_id": assignment["issue_id"],
                    "number": assignment["number"],
                    "labels": [
                        {"id": label.get("id"), "name": label.get("name")}
                        for label in issue.get("labels", [])
                        if isinstance(label, Mapping)
                    ],
                    "destination_preexisting": assignment.get("destination_preexisting", False),
                })
            operation["final_assignments"] = final_rows
        targets.append({
            "repository_id": str(current["id"]),
            "repository": current["full_name"],
            "default_branch": current["default_branch"],
            "default_commit": _commit_sha(current),
            "visibility": current.get("visibility", "unknown"),
            "archived": False,
            "operations": operations,
        })
    all_targets = targets
    selected_set = set(selected_ids)
    targets = [target for target in all_targets if target["repository_id"] in selected_set]
    _describe_operations(targets, meta, shared_labels, migration_rows)
    review_blockers = list(meta["blockers"])
    if not evidence_result["ok"]:
        review_blockers.extend(evidence_result["unavailable"])
    review_blockers = sorted(set(review_blockers))
    plan: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "organization": meta["organization"],
        "brand_topic": meta["brand_topic"],
        "inputs": {"metadata_digest": digest(meta), "snapshot_digest": digest(snap), "labels_digest": digest(shared_labels), "migrations_digest": digest(migration_rows), "selection_digest": digest(selected_ids)},
        "manifest_revision": "sha256:" + digest(meta),
        "selection": {"repository_ids": selected_ids, "explicit": selection_explicit},
        "review": {"status": meta["review_status"], "blockers": review_blockers, "evidence": evidence_result, "applicable": meta["review_status"] == "reviewed" and not review_blockers},
        "authorization": {"operator": operator, "authorization_id": authorization_id, "repositories": selected_ids, "operations": ["topics", "labels"]},
        "targets": sorted(targets, key=lambda x: (x["repository_id"], x["repository"])),
    }
    plan["digest"] = digest(plan)
    return plan


def _commit_sha(repo: Mapping[str, Any]) -> str:
    value = repo.get("default_commit")
    if isinstance(value, Mapping):
        value = value.get("sha")
    return _sha(value, f"{repo.get('full_name')}.default_commit")


def _describe_operations(targets, metadata, labels, migrations):
    """Bind review context and conservative inverses into the plan digest."""
    by_id = {str(row["id"]): row for row in metadata["repositories"]}
    for target in targets:
        for op in target["operations"]:
            if op["kind"] == "replace_topics":
                row = by_id[target["repository_id"]]
                op["reason"] = "Reconcile the complete source-backed topic set while preserving valid observed topics."
                op["evidence"] = copy.deepcopy(row["topics"] + row.get("topic_removals", []))
                op["required_permission"] = "administration:write"
                op["blast_radius"] = {"repository_topics": True, "public_discovery_metadata": True}
                op["inverse"] = {"kind": "restore_topics", "expected": op["after"], "restore": op["before"], "requires_owned_journal": True}
            else:
                migration = next((m for m in migrations if m["repository"] == op["repository"] and m["from"] == op.get("from") and m["to"] == op.get("to")), None)
                op["reason"] = migration.get("reason", "Reviewed semantic label migration.") if migration else "Reconcile the canonical shared label definition; preserve all unmanaged definitions and assignments."
                op["evidence"] = {"labels_sha256": digest(labels), "migrations_sha256": digest(migrations), "observed_label_id": op.get("label_id", op.get("source_label_id"))}
                op["required_permission"] = "issues:write"
                count = len(op.get("assignments", []))
                op["blast_radius"] = {"label_definition": op["kind"] != "additive_label_migration" or bool(op.get("create")), "reviewed_issue_pr_assignments": count, "assignment_scope": "reviewed open and closed issues/PRs"}
                if op["kind"] == "additive_label_migration":
                    op["inverse"] = {"kind": "remove_owned_destination_assignments", "preserve_preexisting": True, "retain_source": True, "retain_created_definitions": True}
                elif op["kind"] == "create_label":
                    op["inverse"] = {"kind": "manual_review", "reason": "Created label definitions are retained by default."}
                else:
                    op["inverse"] = {"kind": "restore_label_definition", "expected": op["after"], "restore": op["before"], "requires_owned_journal": True}


def plan_diff(plan: Mapping[str, Any]) -> str:
    lines: list[str] = []
    for target in plan.get("targets", []):
        operations = target.get("operations", [])
        if not operations:
            continue
        lines.append(f"\n### {target['repository']} ({target['repository_id']})\n")
        for op in operations:
            if op["kind"] == "replace_topics":
                lines.append(f"- Topics: {', '.join(op['before']) or '(none)'} → {', '.join(op['after']) or '(none)'}")
            elif op["kind"] == "rename_label":
                lines.append(f"- Rename: {op['from']!r} → {op['to']!r} (stable ID {op.get('label_id')}; {len(op.get('assignments', []))} issue/PR assignments)")
            elif op["kind"] == "additive_label_migration":
                create = " create destination" if op.get("create") else " destination exists"
                lines.append(f"- Additive migration: {op['from']!r} → {op['to']!r} ({len(op.get('assignments', []))} assignments;{create}; retain source)")
            elif op["kind"] == "create_label":
                lines.append(f"- Create label: {op['after']['name']!r} ({op['after']['color']})")
            elif op["kind"] == "update_label":
                lines.append(f"- Update definition: {op['before']['name']!r}: {op['before']['color']}/{op['before'].get('description', '')!r} → {op['after']['color']}/{op['after'].get('description', '')!r}")
    return "\n".join(lines) if lines else "No metadata writes planned."


def snapshot_from_fixture(path: Path) -> dict[str, Any]:
    if path.is_dir():
        files = sorted(path.glob("*.json"))
        if not files:
            raise MetadataError(f"fixture directory {path} contains no JSON audit files")
        rows = []
        for item in files:
            value = read_document(item)
            if not isinstance(value, Mapping) or "repository" not in value:
                # Inventory sidecars (repository seeds, source evidence,
                # orchestration notes, and consumer references) are not
                # repository snapshots.  Rich audit files carry a repository
                # object and are loaded below.
                continue
            rows.append(value)
        return normalize_snapshot(rows)
    return normalize_snapshot(read_document(path))


class CommandRunner:
    """Small seam around subprocess for deterministic tests and safe logging."""

    def run(self, args: Sequence[str], *, input_text: str | None = None, timeout: int = 60) -> str:
        try:
            process = subprocess.run(args, input=input_text, text=True, capture_output=True, timeout=timeout, check=False)
        except subprocess.TimeoutExpired as exc:
            raise APIError(f"command timed out after {timeout}s", "timeout", uncertain=True) from exc
        except OSError as exc:
            raise APIError(f"unable to run permitted tooling: {exc}", "tooling") from exc
        if process.returncode:
            message = (process.stderr or process.stdout or "command failed").strip()
            lowered = (message + "\n" + (process.stdout or "")).lower()
            statuses = re.findall(r"http(?:/[0-9.]+)?\s+(\d{3})", lowered)
            status = int(statuses[-1]) if statuses else None
            if "rate limit" in lowered or status == 429:
                category = "rate_limit"
            elif status in {401, 403} or any(x in lowered for x in ("authentication", "bad credentials", "unauthorized", "forbidden")):
                category = "authentication"
            elif any(x in lowered for x in ("timed out", "timeout", "connection reset", "temporary failure", "network")):
                category = "timeout"
            else:
                category = {404: "not_found", 409: "conflict", 422: "validation"}.get(status, "api")
            headers = re.split(r"\r?\n\r?\n", process.stdout or "", maxsplit=1)[0] if (process.stdout or "").startswith("HTTP/") else ""
            delays = re.findall(r"(?im)^retry-after:\s*([0-9]+)\s*$", headers)
            resets = re.findall(r"(?im)^x-ratelimit-reset:\s*([0-9]+)\s*$", headers)
            exhausted = re.search(r"(?im)^x-ratelimit-remaining:\s*0\s*$", headers)
            retry_after = float(delays[-1]) if delays else None
            if exhausted and resets:
                retry_after = max(retry_after or 0, float(resets[-1]) - time.time() + 1)
            # Responses may contain arbitrary user data or secrets. Retain only
            # status/category/delay in printable diagnostics and journal errors.
            summary = f"permitted tooling failed ({category}); HTTP {status or 'unknown'}"
            if retry_after is not None:
                summary += f"; retry no sooner than {max(0, retry_after):.0f}s"
            raise APIError(summary, category, uncertain=category == "timeout", retry_after=retry_after)
        output = process.stdout
        if "--include" in args and output.startswith("HTTP/"):
            parts = re.split(r"\r?\n\r?\n", output, maxsplit=1)
            if len(parts) != 2:
                raise APIError("missing HTTP response body boundary", "api")
            output = parts[1]
        return output


class GitHubClient:
    """GitHub API adapter using the authenticated ``gh`` executable only."""

    def __init__(self, runner: CommandRunner | Any | None = None, *, retries: int = 2, timeout: int = 60):
        self.runner = runner or CommandRunner()
        self.retries = max(0, retries)
        self.timeout = timeout

    def _run(self, endpoint: str, *, method: str = "GET", payload: Any | None = None, paginate: bool = False) -> Any:
        args = ["gh", "api"]
        if paginate:
            args.extend(["--paginate", "--slurp"])
        else:
            args.append("--include")
        if method != "GET":
            args.extend(["--method", method])
        if payload is not None:
            args.extend(["--input", "-"])
        args.append(endpoint)
        input_text = canonical_json(payload) if payload is not None else None
        last: Exception | None = None
        for attempt in range(self.retries + 1):
            try:
                raw = self.runner.run(args, input_text=input_text, timeout=self.timeout)
                try:
                    return json.loads(raw) if raw.strip() else None
                except json.JSONDecodeError as exc:
                    raise APIError(f"GitHub returned non-JSON response for {endpoint}", "api") from exc
            except APIError as exc:
                last = exc
                if exc.category == "rate_limit":
                    # Retry only a safe read with a server-specified delay and
                    # a bounded budget. A long/unknown delay stops the run.
                    delay = exc.retry_after
                    if method == "GET" and delay is not None and 0 < delay <= 60 and attempt < self.retries:
                        time.sleep(min(60, max(delay, 2**attempt)))
                        continue
                    raise
                if exc.category not in {"rate_limit", "timeout"} or attempt >= self.retries:
                    raise
                # Keep retry bounded and deterministic.  A journal records the
                # eventual outcome; no automatic write is retried after an
                # uncertain timeout without the caller inspecting state.
                # A write is never retried by this adapter.  The caller must
                # inspect state and use the journal/resume path, even when a
                # rate-limit response appears before a request was accepted.
                if method != "GET":
                    raise
                if exc.uncertain:
                    raise
                time.sleep(min(2**attempt, 4))
        assert last is not None
        raise last

    @staticmethod
    def _flatten_paginated(value: Any) -> list[Any]:
        if isinstance(value, list):
            flattened: list[Any] = []
            for item in value:
                flattened.extend(GitHubClient._flatten_paginated(item))
            return flattened
        return [value]

    def list_org_repositories(self, organization: str) -> list[dict[str, Any]]:
        pages = self._run(f"orgs/{urllib.parse.quote(organization, safe='')}/repos?per_page=100&type=all", paginate=True)
        rows = [x for x in self._flatten_paginated(pages) if isinstance(x, Mapping)]
        return sorted((dict(x) for x in rows), key=lambda x: (str(x.get("id")), str(x.get("full_name"))))

    def snapshot(self, organization: str) -> dict[str, Any]:
        repositories = []
        for seed in self.list_org_repositories(organization):
            full = seed.get("full_name")
            if not isinstance(full, str):
                raise MetadataError("GitHub repository response lacks full_name")
            quoted = "/".join(urllib.parse.quote(part, safe="") for part in full.split("/"))
            repository = self._run(f"repos/{quoted}")
            default_branch = repository.get("default_branch")
            if not isinstance(default_branch, str) or not default_branch:
                raise MetadataError(f"{full} has no actual default branch")
            commit = self._run(f"repos/{quoted}/commits/{urllib.parse.quote(default_branch, safe='')}")
            topics = self._run(f"repos/{quoted}/topics")
            labels = self._run(f"repos/{quoted}/labels?per_page=100", paginate=True)
            issue_pages = self._run(f"repos/{quoted}/issues?state=all&per_page=100", paginate=True)
            branches = self._run(f"repos/{quoted}/branches?per_page=100", paginate=True)
            tags = self._run(f"repos/{quoted}/tags?per_page=100", paginate=True)
            releases = self._run(f"repos/{quoted}/releases?per_page=100", paginate=True)
            tree = self._run(f"repos/{quoted}/git/trees/{commit.get('sha')}?recursive=1")
            issues = self._flatten_paginated(issue_pages)
            label_rows = self._flatten_paginated(labels)
            row = {
                "repository": dict(repository),
                "default_commit": dict(commit),
                "topics": dict(topics),
                "labels": [dict(x) for x in label_rows if isinstance(x, Mapping)],
                "label_usage": {},
                "issues": [dict(x) for x in issues if isinstance(x, Mapping)],
                "branches": self._flatten_paginated(branches),
                "tags": self._flatten_paginated(tags),
                "releases": self._flatten_paginated(releases),
                "tree": tree,
            }
            usage = _label_usage(row)
            row["label_usage"] = usage
            repositories.append(row)
        return {"schema_version": SCHEMA_VERSION, "organization": organization, "repositories": _snapshot_repos(repositories), "source": "github-gh-api"}


def _authorization(value: Any, plan: Mapping[str, Any], operator: str | None, *, operation: str = "apply") -> None:
    if operation not in {"apply", "rollback"}:
        raise MetadataError(f"unsupported authorization operation {operation!r}")
    auth = _as_mapping(value, "authorization")
    plan_digest = plan.get("digest")
    if not isinstance(plan_digest, str) or not re.fullmatch(r"[0-9a-f]{64}", plan_digest):
        raise MetadataError("plan has no valid digest")
    if auth.get("plan_digest") != plan_digest:
        raise MetadataError("authorization is bound to a different plan digest")
    if not isinstance(operator, str) or not operator:
        raise MetadataError("--operator is required for writes")
    if auth.get("operator") != operator:
        raise MetadataError("authorization operator does not match --operator")
    if not isinstance(auth.get("authorization_id"), str) or not auth["authorization_id"].strip():
        raise MetadataError("authorization.authorization_id is required")
    record = auth.get("approval_record")
    if not isinstance(record, Mapping):
        raise MetadataError("authorization.approval_record is required; administrator access is not approval")
    if not isinstance(record.get("record_id"), str) or not record["record_id"].strip():
        raise MetadataError("authorization.approval_record.record_id is required")
    if not isinstance(record.get("reviewer"), str) or not record["reviewer"].strip():
        raise MetadataError("authorization.approval_record.reviewer is required")
    if record.get("decision") != "approved":
        raise MetadataError("authorization.approval_record.decision must be approved")
    approved_repos = {str(x) for x in _as_list(auth.get("repositories"), "authorization.repositories")}
    selection = plan.get("selection")
    if isinstance(selection, Mapping) and isinstance(selection.get("repository_ids"), list):
        plan_repos = {str(x) for x in selection["repository_ids"]}
    else:
        plan_repos = {str(x["repository_id"]) for x in plan.get("targets", []) if x.get("operations")}
    if not plan_repos <= approved_repos:
        raise MetadataError("authorization does not cover every planned repository ID")
    allowed_ops = set(_as_list(auth.get("operations"), "authorization.operations"))
    if operation == "rollback":
        if "rollback" not in allowed_ops:
            raise MetadataError("rollback requires a distinct rollback authorization operation")
        return
    needed = set()
    for target in plan.get("targets", []):
        for op in target.get("operations", []):
            needed.add("topics" if op["kind"] == "replace_topics" else "labels")
    if not needed <= allowed_ops:
        raise MetadataError("authorization does not cover every operation type")


def _actual_operator(client: GitHubClient, expected: str) -> None:
    """Bind the caller to the authenticated GitHub identity before writes."""
    identity = client._run("user")
    if not isinstance(identity, Mapping) or identity.get("login") != expected:
        raise MetadataError("--operator does not match the authenticated GitHub operator")


def _check_target_identity(actual: Mapping[str, Any], target: Mapping[str, Any]) -> None:
    if str(actual.get("id")) != str(target["repository_id"]) or actual.get("full_name") != target["repository"]:
        raise MetadataError(f"repository identity changed for {target['repository']}")
    if actual.get("default_branch") != target["default_branch"] or _commit_sha(actual) != target["default_commit"]:
        raise MetadataError(f"default branch/commit drift for {target['repository']}; replan required")
    if target.get("archived", False) is not False:
        raise MetadataError(f"plan marks {target['repository']} archived; metadata writes are forbidden")
    if actual.get("archived", False):
        raise MetadataError(f"repository {target['repository']} is archived; metadata writes are forbidden")
    expected_visibility = target.get("visibility")
    if expected_visibility is not None and actual.get("visibility", "unknown") != expected_visibility:
        raise MetadataError(f"repository visibility drift for {target['repository']}; replan required")


def _issue_label_identities(issue: Mapping[str, Any], field: str) -> list[dict[str, Any]] | None:
    labels = issue.get("labels")
    if not isinstance(labels, list):
        return None
    result: list[dict[str, Any]] = []
    for index, label in enumerate(labels):
        if not isinstance(label, Mapping) or label.get("id") is None or not isinstance(label.get("name"), str):
            return None
        result.append({"id": str(label["id"]), "name": label["name"]})
    return sorted(result, key=lambda x: (x["id"], x["name"]))


def _issue_maps(repo: Mapping[str, Any]) -> tuple[dict[str, Mapping[str, Any]], dict[str, Mapping[str, Any]]]:
    by_id: dict[str, Mapping[str, Any]] = {}
    by_number: dict[str, Mapping[str, Any]] = {}
    rows = repo.get("issues")
    if not isinstance(rows, list):
        return by_id, by_number
    for issue in rows:
        if not isinstance(issue, Mapping):
            continue
        if issue.get("id") is not None:
            by_id[str(issue["id"])] = issue
        if issue.get("number") is not None:
            by_number[str(issue["number"])] = issue
    return by_id, by_number


def _find_planned_issue(
    assignment: Mapping[str, Any],
    by_id: Mapping[str, Mapping[str, Any]],
    by_number: Mapping[str, Mapping[str, Any]],
) -> Mapping[str, Any] | None:
    issue_id = assignment.get("issue_id")
    number = assignment.get("number")
    issue = by_id.get(str(issue_id)) if issue_id is not None else None
    if issue is None and number is not None:
        issue = by_number.get(str(number))
    if issue is None:
        return None
    if issue_id is not None and str(issue.get("id")) != str(issue_id):
        return None
    if number is not None and str(issue.get("number")) != str(number):
        return None
    return issue


def _definition_matches(actual: Mapping[str, Any] | None, expected: Mapping[str, Any], *, id_required: bool = True) -> bool:
    if actual is None:
        return False
    if id_required and str(actual.get("id")) != str(expected.get("id")):
        return False
    return (
        actual.get("name") == expected.get("name")
        and str(actual.get("color", "")).upper() == str(expected.get("color", "")).upper()
        and actual.get("description", "") == expected.get("description", "")
        and _label_archived(actual) == bool(expected.get("archived", False))
    )


def _assignment_mismatches(
    op: Mapping[str, Any],
    current: Mapping[str, Any],
    labels: Mapping[str, Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Verify every planned issue assignment by stable issue/label IDs."""

    mismatches: list[dict[str, Any]] = []
    by_id, by_number = _issue_maps(current)
    assignments = op.get("final_assignments", op.get("assignments"))
    projected = "final_assignments" in op
    if not isinstance(assignments, list):
        return [{"operation_id": op["id"], "reason": "assignment_snapshot_missing"}]
    destination: Mapping[str, Any] | None = None
    if op["kind"] == "additive_label_migration":
        if op.get("create"):
            destination = labels.get(str(op["to"]).casefold())
            if destination is None or _label_archived(destination):
                mismatches.append({"operation_id": op["id"], "reason": "created_destination_not_verified"})
            elif not _definition_matches(
                destination,
                {"id": destination.get("id"), "name": op["to"], "color": op["create"]["color"], "description": op["create"].get("description", ""), "archived": False},
                id_required=False,
            ):
                mismatches.append({"operation_id": op["id"], "reason": "created_destination_definition_drift"})
        else:
            destination = next((row for row in labels.values() if str(row.get("id")) == str(op.get("destination_label_id"))), None)
            if not _definition_matches(destination, op.get("final_destination_definition", op.get("destination_definition", {}))) or _label_archived(destination or {}):
                mismatches.append({"operation_id": op["id"], "reason": "destination_definition_not_verified"})
    for assignment in assignments:
        if not isinstance(assignment, Mapping) or not isinstance(assignment.get("labels"), list):
            mismatches.append({"operation_id": op["id"], "reason": "assignment_snapshot_missing", "issue": assignment.get("number") if isinstance(assignment, Mapping) else None})
            continue
        issue = _find_planned_issue(assignment, by_id, by_number)
        if issue is None:
            mismatches.append({"operation_id": op["id"], "reason": "planned_issue_missing", "issue": assignment.get("number")})
            continue
        expected = []
        for label in assignment["labels"]:
            if not isinstance(label, Mapping) or label.get("id") is None or not isinstance(label.get("name"), str):
                expected = []
                break
            resolved = labels.get(label["name"].casefold()) if label["id"] == "new" else label
            if resolved is None:
                mismatches.append({"operation_id": op["id"], "reason": "created_assignment_label_missing"})
                continue
            expected.append({"id": str(resolved["id"]), "name": label["name"]})
        if not expected and assignment["labels"]:
            mismatches.append({"operation_id": op["id"], "reason": "assignment_snapshot_malformed", "issue": assignment.get("number")})
            continue
        if not projected and op["kind"] == "rename_label":
            changed = False
            for label in expected:
                if label["id"] == str(op.get("label_id")):
                    label["name"] = op["to"]
                    changed = True
            if not changed:
                mismatches.append({"operation_id": op["id"], "reason": "planned_source_assignment_missing", "issue": assignment.get("number")})
        elif not projected and op["kind"] == "additive_label_migration" and not assignment.get("destination_preexisting"):
            if destination is None:
                continue
            expected.append({"id": str(destination["id"]), "name": destination["name"]})
        actual = _issue_label_identities(issue, f"{op['id']}:{assignment.get('number')}")
        if actual is None or actual != sorted(expected, key=lambda x: (x["id"], x["name"])):
            mismatches.append({
                "operation_id": op["id"],
                "issue": assignment.get("number"),
                "reason": "issue_assignments_not_verified",
                "actual": actual,
                "expected": sorted(expected, key=lambda x: (x["id"], x["name"])),
            })
    return mismatches


def verify_plan(plan: Mapping[str, Any], snapshot: Any) -> dict[str, Any]:
    snap = validate_snapshot(snapshot)
    mismatches: list[dict[str, Any]] = []
    by_id = {str(x["id"]): x for x in snap["repositories"]}
    for target in plan.get("targets", []):
        current = by_id.get(str(target["repository_id"]))
        if current is None:
            mismatches.append({"repository": target["repository"], "reason": "repository_missing"})
            continue
        try:
            _check_target_identity(current, target)
        except MetadataError as exc:
            mismatches.append({"repository": target["repository"], "reason": str(exc)})
            continue
        labels = _labels_by_name(current)
        for op in target.get("operations", []):
            if op["kind"] == "replace_topics" and _current_topics(current) != sorted(op["after"]):
                mismatches.append({"operation_id": op["id"], "reason": "topics_do_not_match", "actual": _current_topics(current), "expected": sorted(op["after"])})
            elif op["kind"] == "rename_label":
                row = labels.get(str(op["to"]).casefold())
                if row is None or not _definition_matches(row, op.get("after", {})):
                    mismatches.append({"operation_id": op["id"], "reason": "renamed_label_not_verified"})
                mismatches.extend(_assignment_mismatches(op, current, labels))
            elif op["kind"] == "create_label":
                row = labels.get(op["after"]["name"].casefold())
                if row is None or str(row.get("name")).casefold() != op["after"]["name"].casefold() or _label_archived(row):
                    mismatches.append({"operation_id": op["id"], "reason": "created_label_not_verified"})
                elif str(row.get("color", "")).upper() != str(op["after"].get("color", "")).upper() or row.get("description", "") != op["after"].get("description", ""):
                    mismatches.append({"operation_id": op["id"], "reason": "created_label_definition_drift"})
            elif op["kind"] == "update_label":
                row = labels.get(op["after"]["name"].casefold())
                if row is None or str(row.get("id")) != str(op.get("label_id")):
                    mismatches.append({"operation_id": op["id"], "reason": "updated_label_not_verified"})
                elif str(row.get("color", "")).upper() != str(op["after"].get("color", "")).upper() or row.get("description", "") != op["after"].get("description", ""):
                    mismatches.append({"operation_id": op["id"], "reason": "updated_label_definition_drift"})
            elif op["kind"] == "additive_label_migration":
                source = next((row for row in labels.values() if str(row.get("id")) == str(op.get("source_label_id"))), None)
                if not _definition_matches(source, op.get("final_source_definition", op.get("source_definition", {}))) or _label_archived(source or {}):
                    mismatches.append({"operation_id": op["id"], "reason": "source_definition_not_verified"})
                destination = labels.get(str(op["to"]).casefold())
                if destination is None:
                    mismatches.append({"operation_id": op["id"], "reason": "additive_labels_not_verified"})
                mismatches.extend(_assignment_mismatches(op, current, labels))
    return {"schema_version": SCHEMA_VERSION, "plan_digest": plan.get("digest"), "ok": not mismatches, "mismatches": mismatches}


def _load_optional(path_text: str | None) -> Any | None:
    if not path_text:
        return None
    path = Path(path_text)
    return snapshot_from_fixture(path) if path.is_dir() else read_document(path)


def _common_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="metadata", description=__doc__)
    parser.add_argument("--version", action="version", version=f"metadata {SCHEMA_VERSION}")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("validate", help="validate metadata, labels, snapshot, or plan inputs")
    p.add_argument("--metadata")
    p.add_argument("--labels")
    p.add_argument("--snapshot")
    p.add_argument("--plan")
    p.add_argument("--output", type=Path)

    p = sub.add_parser("snapshot", help="collect paginated GitHub metadata or normalize audit fixtures")
    p.add_argument("--org", default="AI-Ascension")
    p.add_argument("--input", type=Path, help="audit JSON file or directory; skips network")
    p.add_argument("--exclusions", type=Path, help="local JSON list of recorded unlisted-repository applicability exclusions")
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--retries", type=int, default=2)

    p = sub.add_parser("plan", help="create a stable, machine-readable reviewed plan")
    p.add_argument("--metadata", required=True)
    p.add_argument("--snapshot", required=True)
    p.add_argument("--labels", required=True)
    p.add_argument("--migrations", required=True)
    p.add_argument(
        "--repository-id",
        dest="repository_ids",
        action="append",
        help="limit the reviewed plan to this repository ID; repeat for a canary set",
    )
    p.add_argument("--operator")
    p.add_argument("--authorization-id")
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--diff-output", type=Path)

    for command in ("apply", "verify", "rollback"):
        p = sub.add_parser(command, help=f"{command} a reviewed plan")
        p.add_argument("--plan", type=Path, required=True)
        p.add_argument("--snapshot", type=Path)
        p.add_argument("--authorization", type=Path)
        p.add_argument("--operator")
        p.add_argument("--journal", type=Path)
        p.add_argument("--resume", action="store_true")
        p.add_argument("--execute", action="store_true", help="required for network writes; default is read-only")
        p.add_argument("--output", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _common_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "validate":
            if args.plan:
                plan = read_document(Path(args.plan))
                if not isinstance(plan, Mapping) or plan.get("digest") != digest({k: v for k, v in plan.items() if k != "digest"}):
                    raise MetadataError("plan digest is missing or invalid")
                result: Any = {"ok": True, "plan_digest": plan["digest"]}
            else:
                if not args.metadata:
                    raise MetadataError("validate requires --metadata unless validating --plan")
                result = validate_metadata(_load_optional(args.metadata), _load_optional(args.labels), _load_optional(args.snapshot))
                result = {"ok": True, "repository_count": len(result["metadata"]["repositories"]), "snapshot_present": result["snapshot"] is not None, "labels_present": result["labels"] is not None}
            if args.output:
                write_json(args.output, result)
            else:
                print(json.dumps(result, sort_keys=True))
            return 0

        if args.command == "snapshot":
            if args.input:
                snapshot = validate_snapshot(snapshot_from_fixture(args.input))
            else:
                snapshot = validate_snapshot(GitHubClient(retries=args.retries).snapshot(args.org))
            if args.exclusions:
                snapshot["applicability_exclusions"] = _as_list(read_document(args.exclusions), "applicability exclusions")
                observed = {str(x["id"]) for x in snapshot["repositories"]}
                excluded = set()
                for item in snapshot["applicability_exclusions"]:
                    if (not isinstance(item, Mapping) or str(item.get("repository_id")) not in observed
                            or str(item.get("repository_id")) in excluded or item.get("decision") != "excluded-pending-owner"
                            or not isinstance(item.get("reason"), str) or not item["reason"].strip()):
                        raise MetadataError("invalid applicability exclusion; refresh the local decision")
                    excluded.add(str(item["repository_id"]))
            write_json(args.output, snapshot)
            print(json.dumps({"ok": True, "repository_count": len(snapshot["repositories"]), "output": str(args.output)}, sort_keys=True))
            return 0

        plan = read_document(args.plan) if hasattr(args, "plan") else None
        if args.command == "plan":
            snapshot_input = snapshot_from_fixture(Path(args.snapshot)) if Path(args.snapshot).is_dir() else read_document(Path(args.snapshot))
            plan = make_plan(
                read_document(Path(args.metadata)),
                snapshot_input,
                read_document(Path(args.labels)),
                read_document(Path(args.migrations)),
                operator=args.operator,
                authorization_id=args.authorization_id,
                repository_ids=args.repository_ids,
            )
            write_json(args.output, plan)
            diff = plan_diff(plan)
            if args.diff_output:
                args.diff_output.parent.mkdir(parents=True, exist_ok=True)
                args.diff_output.write_text(diff + "\n", encoding="utf-8")
            print(diff, file=sys.stderr)
            print(json.dumps({"ok": True, "plan_digest": plan["digest"], "output": str(args.output)}, sort_keys=True))
            return 0

        if not isinstance(plan, Mapping):
            raise MetadataError("plan must be an object")
        expected = digest({k: v for k, v in plan.items() if k != "digest"})
        if plan.get("digest") != expected:
            raise MetadataError("plan digest is invalid")
        if args.command == "verify":
            if args.snapshot:
                result = verify_plan(plan, read_document(args.snapshot))
            else:
                result = {"ok": False, "plan_digest": plan["digest"], "mismatches": [{"reason": "--snapshot is required for offline verify"}]}
            if args.output:
                write_json(args.output, result)
            else:
                print(json.dumps(result, sort_keys=True))
            return 0 if result["ok"] else 1

        if not args.authorization:
            raise MetadataError(f"{args.command} requires --authorization even when --execute is absent")
        _authorization(read_document(args.authorization), plan, args.operator, operation=args.command)
        journal = args.journal or Path("metadata/journals") / f"{plan['digest']}.jsonl"
        if not isinstance(plan.get("review"), Mapping) or not plan["review"].get("applicable", False):
            raise MetadataError("plan is review-incomplete or has unresolved blockers; application is disabled")
        if ExecutionMetadataWriter is None:
            raise MetadataError("metadata execution engine is unavailable")
        client = GitHubClient()
        if args.execute:
            _actual_operator(client, args.operator)
        writer = ExecutionMetadataWriter(client, journal)
        if args.command == "apply":
            result = writer.apply(plan, execute=args.execute, resume=args.resume)
        else:
            result = writer.rollback(plan, execute=args.execute)
        if args.output:
            write_json(args.output, result)
        else:
            print(json.dumps(result, sort_keys=True))
        return 1 if result.get("conflicts") else 0
    except (MetadataError, APIError, ExecutionError) as exc:
        return fail(str(exc))
    except KeyboardInterrupt:
        return fail("interrupted; inspect journal and live state before resume")


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
