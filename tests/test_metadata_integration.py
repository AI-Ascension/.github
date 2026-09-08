"""Planner/executor/verifier integration using synthetic, credential-free state."""
import contextlib
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from test_metadata import metadata, metadata_map, repo_snapshot
from test_metadata_execution import FakeAPI, REPO, SHA
from metadata_execution import _MetadataWriter as MetadataWriter
from metadata_drift import report


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.api = FakeAPI()
        self.desired = metadata_map(rid=7, branch="trunk")

    def snapshot(self):
        value = repo_snapshot(rid=7, branch="trunk", labels=copy.deepcopy(self.api.labels),
                              topics=self.api.topics, issues=copy.deepcopy(self.api.issues))
        value.update(archived=False, visibility="public")
        return value

    def test_planned_additive_effect_verifies_and_reapplies_without_writes(self):
        migrations = [{"repository": REPO, "from": "docs", "to": "documentation", "strategy": "additive"}]
        p = metadata.make_plan(self.desired, self.snapshot(), labels=[], migrations=migrations)
        writer = MetadataWriter(self.api, self.root / "journal", state_dir=self.root / "keys", minimum_write_interval=0)
        self.assertEqual(1, writer.apply(p, execute=True)["writes"])
        checked = metadata.verify_plan(p, self.snapshot())
        self.assertTrue(checked["ok"], checked)
        self.assertEqual(0, writer.apply(p, execute=True)["writes"])
        self.api.issues = []
        self.assertFalse(metadata.verify_plan(p, self.snapshot())["ok"])

    def test_planned_rename_with_definition_change_verifies(self):
        self.api.labels = [x for x in self.api.labels if x["id"] != 2]
        migrations = [{"repository": REPO, "from": "docs", "to": "documentation", "strategy": "rename"}]
        definitions = [{"name": "documentation", "color": "123456", "description": "Reviewed new definition"}]
        p = metadata.make_plan(self.desired, self.snapshot(), labels=definitions, migrations=migrations)
        writer = MetadataWriter(self.api, self.root / "journal", state_dir=self.root / "keys", minimum_write_interval=0)
        self.assertEqual(1, writer.apply(p, execute=True)["writes"])
        self.assertTrue(metadata.verify_plan(p, self.snapshot())["ok"])
        self.api.labels[0]["description"] = "later edit"
        self.assertFalse(metadata.verify_plan(p, self.snapshot())["ok"])

    def _exercise_six_migrations(self, *, create_destinations=False):
        from test_metadata_execution import label
        pairs = [("defect", "bug"), ("docs", "documentation")] + [
            ("wedge:" + name, "audience:" + name)
            for name in ("player", "rust", "mcp", "security")]
        sources = [label(i + 10, source) for i, (source, _) in enumerate(pairs)]
        destinations = [] if create_destinations else [label(i + 30, pairs[i][1]) for i in range(2)]
        human = label(99, "human: label")
        self.api.labels = copy.deepcopy(sources + destinations + [human])
        self.api.issues = [{"id": 101, "number": 1, "labels": copy.deepcopy(sources + [human])}]
        before = self.snapshot()
        migrations = [{"repository": REPO, "from": source, "to": dest,
                       "strategy": "additive" if i < 2 else "rename",
                       "stable_label_id": i + 10}
                      for i, (source, dest) in enumerate(pairs)]
        definitions = [{"name": dest, "color": "123456", "description": "Reviewed definition"}
                       for _, dest in pairs]
        p = metadata.make_plan(self.desired, before, labels=definitions, migrations=migrations)
        writer = MetadataWriter(self.api, self.root / "journal", state_dir=self.root / "keys", minimum_write_interval=0)
        self.assertGreater(writer.apply(p, execute=True)["writes"], 0)
        checked = metadata.verify_plan(p, self.snapshot())
        self.assertTrue(checked["ok"], checked)
        self.assertEqual(0, writer.apply(p, execute=True, resume=True)["writes"])
        self.assertEqual(0, writer.apply(p, execute=True)["writes"])
        replanned = metadata.make_plan(self.desired, self.snapshot(), labels=definitions, migrations=migrations)
        self.assertEqual([], [op for target in replanned["targets"] for op in target["operations"] if op["kind"] != "additive_label_migration"])
        rolled = writer.rollback(p, execute=True)
        self.assertEqual([], rolled["conflicts"], rolled)
        original_ids = {row["id"] for row in before["labels"]}
        self.assertEqual(before["labels"], [row for row in self.snapshot()["labels"] if row["id"] in original_ids])
        self.assertEqual(2 if create_destinations else 0, len(rolled["retained_labels"]))
        self.assertEqual(before["issues"], self.snapshot()["issues"])

    def test_six_migrations_on_one_issue_apply_verify_resume_and_rollback(self):
        self._exercise_six_migrations()

    def test_created_destinations_in_combined_migration_roll_back_assignments(self):
        self._exercise_six_migrations(create_destinations=True)

    def test_cli_invalid_authorization_never_constructs_a_client(self):
        p = metadata.make_plan(self.desired, self.snapshot(), labels=[], migrations=[])
        pp, ap = self.root / "plan.json", self.root / "synthetic-invalid-authorization.json"
        pp.write_text(json.dumps(p))
        ap.write_text(json.dumps({"plan_digest": "wrong"}))
        with patch.object(metadata, "GitHubClient") as client, contextlib.redirect_stderr(io.StringIO()):
            code = metadata.main(["apply", "--plan", str(pp), "--authorization", str(ap), "--operator", "test-only", "--execute"])
        self.assertEqual(2, code)
        client.assert_not_called()

    def test_read_only_drift_detects_topics_and_preserves_unmanaged_labels(self):
        self.assertTrue(report(self.desired, [], self.snapshot())["ok"])
        self.api.topics.append("human-topic")
        result = report(self.desired, [], self.snapshot())
        self.assertEqual(["topics"], [x["kind"] for x in result["mismatches"]])
        self.assertEqual([], self.api.writes)

    def test_cli_rejects_wrong_authenticated_operator_before_executor(self):
        snapshot = self.snapshot()
        snapshot["tree"] = {"truncated": False, "tree": [{"path": "README.md", "type": "blob"}]}
        p = metadata.make_plan(self.desired, snapshot, labels=[], migrations=[])
        self.assertTrue(p["review"]["applicable"])
        pp, ap = self.root / "plan.json", self.root / "synthetic-authorization.json"
        pp.write_text(json.dumps(p))
        ap.write_text(json.dumps({
            "plan_digest": p["digest"], "operator": "test-only",
            "authorization_id": "synthetic-test-only",
            "approval_record": {"record_id": "synthetic", "reviewer": "fixture", "decision": "approved"},
            "repositories": [7], "operations": ["topics", "labels"],
        }))
        with patch.object(metadata, "GitHubClient") as client, \
                patch.object(metadata, "ExecutionMetadataWriter") as writer, \
                contextlib.redirect_stderr(io.StringIO()):
            client.return_value._run.return_value = {"login": "different-account"}
            code = metadata.main(["apply", "--plan", str(pp), "--authorization", str(ap),
                                  "--operator", "test-only", "--execute"])
        self.assertEqual(2, code)
        client.return_value._run.assert_called_once_with("user")
        writer.assert_not_called()

    def test_cli_returns_nonzero_for_rollback_conflicts(self):
        snapshot = self.snapshot()
        snapshot["tree"] = {"truncated": False, "tree": [{"path": "README.md", "type": "blob"}]}
        p = metadata.make_plan(self.desired, snapshot, labels=[], migrations=[])
        pp, ap = self.root / "plan.json", self.root / "synthetic-authorization.json"
        pp.write_text(json.dumps(p))
        ap.write_text(json.dumps({
            "plan_digest": p["digest"], "operator": "test-only",
            "authorization_id": "synthetic-test-only",
            "approval_record": {"record_id": "synthetic", "reviewer": "fixture", "decision": "approved"},
            "repositories": [7], "operations": ["rollback"],
        }))
        with patch.object(metadata, "GitHubClient") as client, \
                patch.object(metadata, "ExecutionMetadataWriter") as writer, \
                contextlib.redirect_stdout(io.StringIO()):
            client.return_value._run.return_value = {"login": "test-only"}
            writer.return_value.rollback.return_value = {"writes": 0, "conflicts": [{"reason": "later human edit"}]}
            code = metadata.main(["rollback", "--plan", str(pp), "--authorization", str(ap),
                                  "--operator", "test-only", "--execute"])
        self.assertEqual(1, code)
        client.return_value._run.assert_called_once_with("user")
        writer.return_value.rollback.assert_called_once()


if __name__ == "__main__":
    unittest.main()
