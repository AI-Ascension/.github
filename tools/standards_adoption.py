#!/usr/bin/env python3
"""Validate public standards-adoption locks without fetching a moving source branch."""
import argparse
import hashlib
import json
import re
from pathlib import Path

SHA = set("0123456789abcdef")
REPOSITORY = re.compile(r"AI-Ascension/[A-Za-z0-9][A-Za-z0-9_.-]{0,99}$")

def fail(message):
    raise ValueError(message)

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def validate(ledger_path, workspace_root):
    ledger = load(ledger_path)
    source = ledger.get("canonical_source", {})
    if ledger.get("schema_version") != 1 or source.get("repository") != "AI-Ascension/.github":
        fail("invalid canonical source")
    revision = source.get("revision", "")
    if len(revision) != 40 or not set(revision) <= SHA or source.get("distribution") != "local" or source.get("published") is not False:
        fail("canonical source must remain the recorded unpublished local bundle")
    consumers = ledger.get("consumers")
    if not isinstance(consumers, list) or not consumers:
        fail("scheduled public consumer set must be nonempty")
    findings = []
    seen = set()
    workspace_root = workspace_root.resolve()
    for row in consumers:
        repository, lock_path = row.get("repository"), row.get("lock_path")
        if not isinstance(repository, str) or not REPOSITORY.fullmatch(repository) or repository.endswith("project-planning"):
            fail("only explicitly listed public product consumers may be scheduled")
        if repository in seen:
            fail("duplicate scheduled public consumer")
        seen.add(repository)
        if not isinstance(lock_path, str) or lock_path.startswith("/") or ".." in Path(lock_path).parts:
            fail("unsafe consumer lock path")
        local = workspace_root / repository.rsplit("/", 1)[1] / lock_path
        try:
            local.relative_to(workspace_root)
        except ValueError:
            fail("consumer lock escapes workspace")
        current = workspace_root / repository.rsplit("/", 1)[1]
        for part in Path(lock_path).parts:
            current /= part
            if current.is_symlink():
                fail("symlinked consumer lock is not allowed")
        if not local.is_file():
            findings.append({"repository": repository, "kind": "missing_lock"})
            continue
        raw = local.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        if digest != row.get("lock_sha256"):
            findings.append({"repository": repository, "kind": "stale_or_unauthorized_lock", "expected": row.get("lock_sha256"), "actual": digest})
            continue
        lock = json.loads(raw)
        lock_source = lock.get("source", {})
        if lock_source.get("repository") != source["repository"] or lock_source.get("commit") != revision or lock_source.get("distribution") != "local" or lock_source.get("published") is not False:
            findings.append({"repository": repository, "kind": "unauthorized_source_state"})
        elif lock_source.get("bundle_digest") != row.get("content_digest"):
            findings.append({"repository": repository, "kind": "content_digest_drift"})
    return {"ok": not findings, "findings": findings, "checked_consumers": len(consumers)}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--workspace-root", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = validate(args.ledger, args.workspace_root)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        result = {"ok": False, "findings": [{"kind": "invalid_input", "reason": str(error)}]}
    print(json.dumps(result, sort_keys=True))
    return 0 if result["ok"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
