import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from standards_adoption import validate

class StandardsAdoptionTests(unittest.TestCase):
    def prepare(self):
        source = json.loads((ROOT / "metadata/standards-adoption.json").read_text())
        directory = tempfile.TemporaryDirectory()
        workspace = Path(directory.name)
        for row in source["consumers"]:
            target = workspace / row["repository"].rsplit("/", 1)[1]
            target.mkdir()
            original = Path(__import__("os").environ.get("STANDARDS_CONSUMER_ROOT", ROOT.parent)) / target.name / row["lock_path"]
            raw = original.read_bytes()
            (target / row["lock_path"]).write_bytes(raw)
            row["lock_sha256"] = hashlib.sha256(raw).hexdigest()
        ledger = workspace / "ledger.json"
        ledger.write_text(json.dumps(source))
        return directory, workspace, ledger

    def test_current_public_locks_pass(self):
        directory, workspace, ledger = self.prepare()
        with directory:
            self.assertTrue(validate(ledger, workspace)["ok"])

    def test_changed_lock_fails_closed(self):
        directory, workspace, ledger = self.prepare()
        with directory:
            consumer = json.loads(ledger.read_text())["consumers"][0]
            target = workspace / consumer["repository"].rsplit("/", 1)[1] / consumer["lock_path"]
            target.write_text(target.read_text() + "\n")
            result = validate(ledger, workspace)
            self.assertFalse(result["ok"])
            self.assertEqual("stale_or_unauthorized_lock", result["findings"][0]["kind"])

    def test_private_or_planning_consumer_is_rejected(self):
        directory, workspace, ledger = self.prepare()
        with directory:
            value = json.loads(ledger.read_text())
            value["consumers"].append({"repository": "AI-Ascension/st2-project-planning", "lock_path": "private.json"})
            ledger.write_text(json.dumps(value))
            with self.assertRaisesRegex(ValueError, "public product consumers"):
                validate(ledger, workspace)

    def test_empty_duplicate_escaping_and_symlinked_consumers_fail_closed(self):
        directory, workspace, ledger = self.prepare()
        with directory:
            value = json.loads(ledger.read_text())
            value["consumers"] = []
            ledger.write_text(json.dumps(value))
            with self.assertRaisesRegex(ValueError, "nonempty"):
                validate(ledger, workspace)
            value = json.loads((ROOT / "metadata/standards-adoption.json").read_text())
            value["consumers"].append(dict(value["consumers"][0]))
            ledger.write_text(json.dumps(value))
            with self.assertRaisesRegex(ValueError, "duplicate"):
                validate(ledger, workspace)
            value = json.loads((ROOT / "metadata/standards-adoption.json").read_text())
            value["consumers"][0]["repository"] = "AI-Ascension/../../etc"
            ledger.write_text(json.dumps(value))
            with self.assertRaisesRegex(ValueError, "public product"):
                validate(ledger, workspace)
            directory2, workspace2, ledger2 = self.prepare()
            with directory2:
                target = workspace2 / value.get("consumers", [{}])[0].get("repository", "x").rsplit("/", 1)[-1]
                # Use the known valid fixture path so the symlink check is reached.
                target = workspace2 / "ascension-map-visualizer" / "standards.lock.json"
                target.unlink()
                target.symlink_to("/dev/null")
                with self.assertRaisesRegex(ValueError, "symlinked"):
                    validate(ledger2, workspace2)
