#!/usr/bin/env python3
"""Compare a read-only snapshot with canonical topics and managed definitions."""
import argparse
import json
from pathlib import Path

from metadata import MetadataError, read_document, validate_metadata


def report(metadata, shared_labels, snapshot):
    checked = validate_metadata(metadata, shared_labels, snapshot)
    desired = checked["metadata"]
    live = checked["snapshot"]["repositories"]
    by_id = {str(x["id"]): x for x in live}
    mismatches = []
    known = {str(x["id"]) for x in desired["repositories"]}
    excluded = {str(x["repository_id"]) for x in checked["snapshot"].get("applicability_exclusions", [])}
    for repo in live:
        if str(repo["id"]) not in known | excluded:
            mismatches.append({"repository": repo["full_name"], "kind": "unmapped_repository"})
    for row in desired["repositories"]:
        if row.get("managed") is False:
            continue
        repo = by_id[str(row["id"])]
        topics = repo["topics"]
        actual = sorted(topics["names"] if isinstance(topics, dict) else topics)
        expected = sorted(x["name"] for x in row["topics"])
        if actual != expected:
            mismatches.append({"repository": row["full_name"], "kind": "topics", "actual": actual, "desired": expected})
        labels = {x["name"].casefold(): x for x in repo["labels"]}
        for definition in checked["labels"]:
            if "repository_ids" in definition and str(row["id"]) not in definition["repository_ids"]:
                continue
            actual_label = labels.get(definition["name"].casefold())
            fields = lambda x: {"color": x["color"].lower(), "description": x.get("description") or "", "archived": bool(x.get("archived", False) or x.get("archived_at") is not None)}
            if actual_label is None or fields(actual_label) != fields(definition):
                mismatches.append({"repository": row["full_name"], "kind": "shared_label", "label": definition["name"],
                                   "actual": fields(actual_label) if actual_label else None, "desired": fields(definition)})
    return {"ok": not mismatches, "review_status": desired["review_status"], "mismatches": mismatches}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--labels", type=Path, required=True)
    parser.add_argument("--snapshot", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = report(read_document(args.metadata), read_document(args.labels), read_document(args.snapshot))
    except MetadataError as exc:
        result = {"ok": False, "mismatches": [{"kind": "invalid_or_stale_input", "reason": str(exc)}]}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
