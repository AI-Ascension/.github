#!/usr/bin/env python3
"""Verify a release evidence bundle against an independently pinned review policy.

No network, publication, mutation, signature assertion, or implicit qualification.
The policy digest must come from a trusted review channel, not the candidate bundle.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


class InvalidRelease(ValueError):
    """Missing, mismatched, malformed or insufficient qualification evidence."""


MAX_EVIDENCE_FILES = 4096
MAX_EVIDENCE_BYTES = 256 * 1024 * 1024


def require(condition, message):
    if not condition:
        raise InvalidRelease(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def bounded_bytes(path, limit):
    with path.open("rb") as stream:
        raw = stream.read(limit + 1)
    require(len(raw) <= limit, "input exceeds size bound")
    return raw


def read_json(path):
    raw = bounded_bytes(path, 8 * 1024 * 1024)
    return json.loads(raw, object_pairs_hook=unique_object), hashlib.sha256(raw).hexdigest()


def fields(value, expected, label):
    require(isinstance(value, dict) and set(value) == set(expected), f"invalid {label} fields")


def text(value):
    return isinstance(value, str) and 0 < len(value) <= 200 and not any(ord(c) < 32 for c in value)


def hex_value(value, length):
    return isinstance(value, str) and re.fullmatch(f"[a-f0-9]{{{length}}}", value) is not None


def sources(value):
    require(isinstance(value, dict) and bool(value), "sources must be nonempty")
    for repository, commit in value.items():
        require(re.fullmatch(r"AI-Ascension/[A-Za-z0-9_.-]+", repository) is not None, "invalid source repository")
        require(hex_value(commit, 40), "source must be an exact commit")


def by_id(rows, label):
    require(isinstance(rows, list) and bool(rows), f"{label} must be nonempty")
    result = {}
    for row in rows:
        require(isinstance(row, dict) and text(row.get("id")), f"invalid {label} ID")
        require(row["id"] not in result, f"duplicate {label} ID")
        result[row["id"]] = row
    return result


def contract_rows(rows, source_map):
    contracts = by_id(rows, "contracts")
    for row in contracts.values():
        fields(row, ["id", "producer", "consumers", "version", "sha256"], "contract")
        require(row["producer"] in source_map, "unknown contract producer")
        consumers = row["consumers"]
        require(isinstance(consumers, list) and consumers and all(isinstance(c, str) for c in consumers), "invalid consumers")
        require(len(set(consumers)) == len(consumers) and all(c in source_map for c in consumers), "unknown or duplicate consumer")
        require(text(row["version"]) and hex_value(row["sha256"], 64), "contract version/digest missing")
    return contracts


def safe_receipt(root, name):
    require(isinstance(name, str) and len(name) <= 500, "invalid receipt path")
    require(not any(c in name for c in "\\:\x00") and not name.startswith("/"), "unsafe receipt path")
    parts = name.split("/")
    require(all(part and part not in (".", "..") for part in parts), "unsafe receipt path")
    current = root
    for part in parts:
        current = current / part
        require(not current.is_symlink(), "symlink receipt path")
    require(current.is_file(), "receipt missing or not a file")
    return current


def relative_if_within(root, candidate):
    try:
        return candidate.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return None


def verify_evidence_inventory(root, allowed):
    """Reject hidden payloads and symlinks before trusting a bounded evidence bundle."""
    files = 0
    total = 0
    for candidate in root.rglob("*"):
        relative = candidate.relative_to(root).as_posix()
        stat = candidate.lstat()
        require(not candidate.is_symlink(), "symlink in evidence bundle")
        if candidate.is_dir():
            continue
        require(candidate.is_file(), "unsupported evidence bundle entry")
        require(relative in allowed, "unreferenced evidence file")
        files += 1
        total += stat.st_size
        require(files <= MAX_EVIDENCE_FILES and total <= MAX_EVIDENCE_BYTES, "evidence bundle exceeds bounds")


def verify(manifest_path, policy_path, approved_policy_sha256, evidence_root):
    require(hex_value(approved_policy_sha256, 64), "independently approved policy digest required")
    policy, policy_digest = read_json(policy_path)
    require(policy_digest == approved_policy_sha256, "policy differs from independently approved digest")
    manifest, _ = read_json(manifest_path)
    fields(policy, ["schema_version", "release_id", "sources", "contracts", "checks"], "policy")
    fields(manifest, ["schema_version", "release_id", "sources", "contracts", "evidence"], "manifest")
    for document in (manifest, policy):
        require(type(document["schema_version"]) is int and document["schema_version"] == 1, "unsupported schema")
        require(text(document["release_id"]), "release ID required")
        sources(document["sources"])
        contract_rows(document["contracts"], document["sources"])
    require(manifest["release_id"] == policy["release_id"], "release ID mismatch")
    require(manifest["sources"] == policy["sources"], "release source set differs from reviewed source set")
    require(by_id(manifest["contracts"], "contracts") == by_id(policy["contracts"], "contracts"), "contract set/version/digest mismatch")
    checks = by_id(policy["checks"], "checks")
    evidence = by_id(manifest["evidence"], "evidence")
    require(set(checks) == set(evidence), "required evidence missing or unexpected")
    receipt_paths = set()
    allowed_paths = set()
    for candidate in (manifest_path, policy_path):
        relative = relative_if_within(evidence_root, candidate)
        if relative:
            allowed_paths.add(relative)
    completed = []
    for check_id, check in checks.items():
        fields(check, ["id", "kind", "subjects", "contracts", "receipt_sha256"], "required check")
        require(check["kind"] in ("build", "synthetic", "native-session0", "operations", "exact-host"), "unknown qualification kind")
        sources(check["subjects"])
        require(all(policy["sources"].get(repo) == sha for repo, sha in check["subjects"].items()), "check source mismatch")
        require(isinstance(check["contracts"], list) and check["contracts"] and all(isinstance(c, str) for c in check["contracts"]), "check contracts required")
        require(len(set(check["contracts"])) == len(check["contracts"]) and set(check["contracts"]) <= set(by_id(policy["contracts"], "contracts")), "unknown or duplicate check contract")
        require(hex_value(check["receipt_sha256"], 64), "reviewed receipt digest required")
        row = evidence[check_id]
        fields(row, ["id", "path", "sha256"], "evidence")
        require(isinstance(row["path"], str) and row["path"] not in receipt_paths, "duplicate receipt path")
        receipt_paths.add(row["path"])
        allowed_paths.add(row["path"])
        receipt, digest = read_json(safe_receipt(evidence_root, row["path"]))
        require(digest == row["sha256"] == check["receipt_sha256"], "receipt differs from reviewed content")
        fields(receipt, ["id", "kind", "subjects", "contracts", "result", "completed_at", "runner", "log_path", "log_sha256"], "receipt")
        require(all(receipt[key] == check[key] for key in ("id", "kind", "subjects", "contracts")), "receipt scope mismatch")
        require(receipt["result"] == "passed", "required qualification did not pass")
        require(text(receipt["runner"]) and hex_value(receipt["log_sha256"], 64), "runner/log evidence missing")
        log = safe_receipt(evidence_root, receipt["log_path"])
        log_bytes = bounded_bytes(log, 64 * 1024 * 1024)
        require(bool(log_bytes), "log must be nonempty")
        require(hashlib.sha256(log_bytes).hexdigest() == receipt["log_sha256"], "log content digest mismatch")
        allowed_paths.add(receipt["log_path"])
        require(isinstance(receipt["completed_at"], str), "completion timestamp required")
        try:
            timestamp = datetime.fromisoformat(receipt["completed_at"].replace("Z", "+00:00"))
        except ValueError as error:
            raise InvalidRelease("invalid completion timestamp") from error
        require(timestamp.tzinfo is not None, "completion timestamp must include timezone")
        require(timestamp <= datetime.now(timezone.utc), "completion timestamp is in the future")
        completed.append({"id": check_id, "kind": check["kind"]})
    covered = {contract for check in checks.values() for contract in check["contracts"]}
    require(covered == set(by_id(policy["contracts"], "contracts")), "contract lacks qualification coverage")
    require({repo for check in checks.values() for repo in check["subjects"]} == set(policy["sources"]), "source lacks qualification coverage")
    for contract in policy["contracts"]:
        for consumer in contract["consumers"]:
            require(any(contract["id"] in check["contracts"] and
                        {contract["producer"], consumer} <= set(check["subjects"])
                        for check in checks.values()), "producer/consumer edge lacks joint qualification scope")
    verify_evidence_inventory(evidence_root, allowed_paths)
    return {"release_id": manifest["release_id"], "status": "reviewed_evidence_consistent_not_published",
            "policy_sha256": policy_digest, "checks": completed}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--policy", type=Path, required=True)
    parser.add_argument("--policy-sha256", required=True)
    parser.add_argument("--evidence-root", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = verify(args.manifest, args.policy, args.policy_sha256, args.evidence_root.resolve())
        print(json.dumps(result, indent=2))
        return 0
    except (InvalidRelease, OSError, ValueError, TypeError, KeyError) as error:
        print(f"release evidence rejected: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
