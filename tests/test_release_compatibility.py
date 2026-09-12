"""Independent synthetic fixtures for fail-closed release evidence consistency."""

import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location("release", Path(__file__).resolve().parents[1] / "tools/release_compatibility.py")
release = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(release)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="release-evidence-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.sources = {"AI-Ascension/producer": "a" * 40, "AI-Ascension/consumer": "b" * 40}
        self.contract = {"id": "portable-v2", "producer": "AI-Ascension/producer",
                         "consumers": ["AI-Ascension/consumer"], "version": "candidate2", "sha256": "c" * 64}
        log = b"synthetic fixture only; not actual native qualification\n"
        (self.root / "native.log").write_bytes(log)
        self.receipt = {"id": "native", "kind": "native-session0", "subjects": self.sources,
                        "contracts": ["portable-v2"], "result": "passed", "completed_at": "2000-01-01T00:00:00Z",
                        "runner": "synthetic-test-fixture", "log_path": "native.log", "log_sha256": digest(log)}
        receipt_digest = self.write("native.json", self.receipt)
        self.policy = {"schema_version": 1, "release_id": "synthetic-rc", "sources": self.sources,
                       "contracts": [self.contract], "checks": [{"id": "native", "kind": "native-session0",
                       "subjects": self.sources, "contracts": ["portable-v2"], "receipt_sha256": receipt_digest}]}
        self.manifest = {"schema_version": 1, "release_id": "synthetic-rc", "sources": copy.deepcopy(self.sources),
                         "contracts": [copy.deepcopy(self.contract)],
                         "evidence": [{"id": "native", "path": "native.json", "sha256": receipt_digest}]}

    def write(self, name, value):
        raw = json.dumps(value).encode()
        (self.root / name).write_bytes(raw)
        return digest(raw)

    def verify(self, approved=None):
        policy_digest = self.write("policy.json", self.policy)
        self.write("manifest.json", self.manifest)
        return release.verify(self.root / "manifest.json", self.root / "policy.json", approved or policy_digest, self.root)

    def reseal_receipt(self):
        value = self.write("native.json", self.receipt)
        self.policy["checks"][0]["receipt_sha256"] = value
        self.manifest["evidence"][0]["sha256"] = value

    def test_consistent_synthetic_fixture(self):
        result = self.verify()
        self.assertEqual(result["status"], "reviewed_evidence_consistent_not_published")

    def test_cli_success_and_fail_closed_exit(self):
        policy_digest = self.write("policy.json", self.policy)
        self.write("manifest.json", self.manifest)
        command = [sys.executable, str(Path(release.__file__)), "--manifest", str(self.root / "manifest.json"),
                   "--policy", str(self.root / "policy.json"), "--policy-sha256", policy_digest,
                   "--evidence-root", str(self.root)]
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["release_id"], "synthetic-rc")
        (self.root / "native.log").unlink()
        rejected = subprocess.run(command, capture_output=True, text=True, check=False)
        self.assertEqual(rejected.returncode, 1)
        self.assertIn("release evidence rejected", rejected.stderr)
        self.assertEqual(rejected.stdout, "")

    def test_manifest_matches_published_schema_field_inventory(self):
        schema_dir = Path(release.__file__).resolve().parents[1] / "metadata/schema"
        for name, fixture in (("release-compatibility", self.manifest), ("release-policy", self.policy), ("release-receipt", self.receipt)):
            schema = json.loads((schema_dir / f"{name}.schema.json").read_text())
            self.assertEqual(set(schema["required"]), set(fixture))
            self.assertEqual(set(schema["properties"]), set(fixture))
            self.assertIs(schema["additionalProperties"], False)

    def test_policy_cannot_be_resealed_without_independent_approval(self):
        approved = self.write("policy.json", self.policy)
        self.policy["checks"] = []
        with self.assertRaisesRegex(release.InvalidRelease, "approved digest"):
            self.verify(approved)

    def test_omitted_and_duplicate_evidence(self):
        for rows in ([], self.manifest["evidence"] * 2):
            with self.subTest(rows=rows):
                self.manifest["evidence"] = rows
                with self.assertRaises(release.InvalidRelease):
                    self.verify()

    def test_changed_sources_and_contract_versions(self):
        self.manifest["sources"]["AI-Ascension/consumer"] = "d" * 40
        with self.assertRaisesRegex(release.InvalidRelease, "source set"):
            self.verify()
        self.manifest["sources"] = self.sources
        self.manifest["contracts"][0]["version"] = "candidate3"
        with self.assertRaisesRegex(release.InvalidRelease, "contract set"):
            self.verify()

    def test_native_cannot_be_replaced_by_synthetic_or_unavailable(self):
        for field, value, message in (("kind", "synthetic", "scope mismatch"), ("result", "unverified", "did not pass"), ("result", "skipped", "did not pass")):
            with self.subTest(field=field, value=value):
                original = self.receipt[field]
                self.receipt[field] = value
                self.reseal_receipt()
                with self.assertRaisesRegex(release.InvalidRelease, message):
                    self.verify()
                self.receipt[field] = original

    def test_receipt_and_log_tamper(self):
        self.receipt["runner"] = "different"
        self.write("native.json", self.receipt)
        with self.assertRaisesRegex(release.InvalidRelease, "reviewed content"):
            self.verify()
        self.reseal_receipt()
        (self.root / "native.log").write_text("changed")
        with self.assertRaisesRegex(release.InvalidRelease, "log content"):
            self.verify()

    def test_empty_log_and_unreferenced_bundle_content_rejected(self):
        (self.root / "native.log").write_bytes(b"")
        self.receipt["log_sha256"] = digest(b"")
        self.reseal_receipt()
        with self.assertRaisesRegex(release.InvalidRelease, "log must be nonempty"):
            self.verify()
        log = b"synthetic fixture only; not actual native qualification\n"
        (self.root / "native.log").write_bytes(log)
        self.receipt["log_sha256"] = digest(log)
        self.reseal_receipt()
        (self.root / "unreviewed-payload.txt").write_text("not evidence")
        with self.assertRaisesRegex(release.InvalidRelease, "unreferenced evidence"):
            self.verify()

    def test_unreferenced_symlink_rejected(self):
        (self.root / "hidden-link").symlink_to(self.root / "native.log")
        with self.assertRaisesRegex(release.InvalidRelease, "symlink in evidence"):
            self.verify()

    def test_paths_and_symlinks(self):
        for name in ("../native.json", "/native.json", "C:\\native.json", "folder/../native.json"):
            with self.subTest(name=name):
                self.manifest["evidence"][0]["path"] = name
                with self.assertRaisesRegex(release.InvalidRelease, "unsafe"):
                    self.verify()
        (self.root / "link.json").symlink_to(self.root / "native.json")
        self.manifest["evidence"][0]["path"] = "link.json"
        with self.assertRaisesRegex(release.InvalidRelease, "symlink"):
            self.verify()

    def test_future_completion_rejected(self):
        self.receipt["completed_at"] = "9999-01-01T00:00:00Z"
        self.reseal_receipt()
        with self.assertRaisesRegex(release.InvalidRelease, "future"):
            self.verify()

    def test_duplicate_json_keys_rejected(self):
        (self.root / "duplicate.json").write_text('{"id":"one","id":"two"}')
        with self.assertRaisesRegex(release.InvalidRelease, "duplicate JSON"):
            release.read_json(self.root / "duplicate.json")

    def test_single_repo_build_cannot_claim_cross_repo_qualification(self):
        self.policy["checks"][0]["subjects"] = {"AI-Ascension/producer": "a" * 40}
        self.receipt["subjects"] = self.policy["checks"][0]["subjects"]
        self.reseal_receipt()
        with self.assertRaisesRegex(release.InvalidRelease, "source lacks qualification"):
            self.verify()
