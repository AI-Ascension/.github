#!/usr/bin/env python3
"""Compare a read-only snapshot with canonical topics and managed definitions.

This is a *reporting* tool.  A discovered difference is the report's content,
not a reason to abort: the scheduled drift monitor must be able to enumerate
every difference in one run.  Only malformed or unverifiable inputs, where no
trustworthy report can be produced, surface as ``invalid_or_stale_input``.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from metadata import (
    MetadataError,
    applicability_exclusions,
    normalize_labels,
    normalize_metadata,
    read_document,
    validate_snapshot,
)


def _commit(snapshot_repo):
    value = snapshot_repo.get("default_commit")
    return value.get("sha") if isinstance(value, dict) else value


def _label_fields(value):
    return {
        "color": value["color"].lower(),
        "description": value.get("description") or "",
        "archived": bool(value.get("archived", False) or value.get("archived_at") is not None),
    }


def _compare(metadata, shared_labels, snapshot):
    desired = normalize_metadata(metadata)
    labels = normalize_labels(shared_labels)
    live = validate_snapshot(snapshot)
    repositories = live["repositories"]
    by_id = {str(x["id"]): x for x in repositories}
    by_name = {x["full_name"]: x for x in repositories}
    # A well-formed exclusion record is still meaningful here; an *unrecorded*
    # unlisted repository is drift to report, not an input error.
    applicability_exclusions(desired, live)
    excluded = {str(x["repository_id"]) for x in live.get("applicability_exclusions", [])}
    known = {str(x["id"]) for x in desired["repositories"]}
    mismatches = []
    for repo in repositories:
        if str(repo["id"]) not in known | excluded:
            mismatches.append({"repository": repo["full_name"], "kind": "unmapped_repository"})
    for row in desired["repositories"]:
        if row.get("managed") is False:
            continue
        current = by_id.get(str(row["id"])) or by_name.get(row["full_name"])
        if current is None:
            mismatches.append({"repository": row["full_name"], "kind": "missing_repository"})
            continue
        if row.get("default_branch") and row["default_branch"] != current.get("default_branch"):
            mismatches.append({"repository": row["full_name"], "kind": "default_branch",
                               "actual": current.get("default_branch"), "desired": row["default_branch"]})
        if row.get("default_commit") and row["default_commit"] != _commit(current):
            mismatches.append({"repository": row["full_name"], "kind": "source_pin",
                               "actual": _commit(current), "desired": row["default_commit"]})
        if row.get("visibility") and row["visibility"] != current.get("visibility"):
            mismatches.append({"repository": row["full_name"], "kind": "visibility",
                               "actual": current.get("visibility"), "desired": row["visibility"]})
        if bool(row.get("archived", False)) != bool(current.get("archived", False)):
            mismatches.append({"repository": row["full_name"], "kind": "archive_state",
                               "actual": bool(current.get("archived", False)),
                               "desired": bool(row.get("archived", False))})
        topics = current["topics"]
        actual = sorted(topics["names"] if isinstance(topics, dict) else topics)
        expected = sorted(x["name"] for x in row["topics"])
        if actual != expected:
            mismatches.append({"repository": row["full_name"], "kind": "topics", "actual": actual, "desired": expected})
        present = {x["name"].casefold(): x for x in current["labels"]}
        for definition in labels:
            if "repository_ids" in definition and str(row["id"]) not in definition["repository_ids"]:
                continue
            actual_label = present.get(definition["name"].casefold())
            if actual_label is None or _label_fields(actual_label) != _label_fields(definition):
                mismatches.append({"repository": row["full_name"], "kind": "shared_label", "label": definition["name"],
                                   "actual": _label_fields(actual_label) if actual_label else None,
                                   "desired": _label_fields(definition)})
    return {"ok": not mismatches, "review_status": desired["review_status"], "mismatches": mismatches}


def report(metadata, shared_labels, snapshot):
    try:
        return _compare(metadata, shared_labels, snapshot)
    except MetadataError as exc:
        return {"ok": False, "mismatches": [{"kind": "invalid_or_stale_input", "reason": str(exc)}]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--labels", type=Path, required=True)
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument("--output", type=Path, help="also write the report as JSON")
    args = parser.parse_args()
    try:
        result = report(read_document(args.metadata), read_document(args.labels), read_document(args.snapshot))
    except (MetadataError, OSError, json.JSONDecodeError) as exc:
        result = {"ok": False, "mismatches": [{"kind": "invalid_or_stale_input", "reason": str(exc)}]}
        print(json.dumps(result, indent=2, sort_keys=True))
        return 1
    payload = json.dumps(result, indent=2, sort_keys=True)
    print(payload)
    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
