"""Planner/executor/verifier integration using synthetic, credential-free state."""
import contextlib
import copy
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from test_metadata import metadata, metadata_map, repo_snapshot
from test_metadata_execution import FakeAPI, REPO, SHA
from metadata import APIError, GitHubClient, _top_level_string
from metadata_execution import _MetadataWriter as MetadataWriter
import metadata_drift
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

    def test_drift_reports_unlisted_repository_as_a_finding_not_an_input_error(self):
        """A discovered repository is drift to report, not a reason to abort.

        The scheduled monitor must enumerate every difference in one run, so an
        unrecorded repository cannot collapse the whole report into a single
        ``invalid_or_stale_input`` error. Planning keeps its stricter gate, which
        is asserted separately by the policy tests.
        """
        extra = repo_snapshot(rid=8, full="AI-Ascension/unlisted-fixture")
        extra["visibility"] = "public"
        result = report(self.desired, [], {"repositories": [self.snapshot(), extra]})
        self.assertFalse(result["ok"])
        self.assertEqual(
            [{"kind": "unmapped_repository", "repository": "AI-Ascension/unlisted-fixture"}],
            result["mismatches"],
        )

    def test_drift_reports_stale_source_pin_and_default_branch(self):
        """The step advertises source-pin reporting; it must actually appear."""
        snapshot = self.snapshot()
        newer = "c" * 40
        snapshot["default_commit"] = newer
        result = report(self.desired, [], snapshot)
        self.assertEqual(["source_pin"], [x["kind"] for x in result["mismatches"]])
        self.assertEqual({"actual": newer, "desired": SHA, "repository": REPO, "kind": "source_pin"},
                         result["mismatches"][0])
        snapshot = self.snapshot()
        snapshot["default_branch"] = "bootstrap"
        result = report(self.desired, [], snapshot)
        self.assertEqual(["default_branch"], [x["kind"] for x in result["mismatches"]])

    def test_drift_reports_a_pin_the_live_branch_no_longer_contains(self):
        """Advancing past a baseline is movement; losing the baseline is drift.

        Live-head equality cannot tell those apart: both look like "pin != head".
        A registry whose pin is still reachable from the live head is informational,
        while a pin the live branch has moved off -- behind, or onto another line --
        must still be reported, or the monitor would go green on a diverged source.
        """
        snapshot = self.snapshot()
        newer = "c" * 40
        snapshot["default_commit"] = newer

        contained = report(self.desired, [], snapshot, {REPO: "ahead"})
        self.assertTrue(contained["ok"], contained)
        self.assertEqual([], contained["mismatches"])
        self.assertEqual(
            [{"baseline": SHA, "kind": "source_pin_advanced", "observed": newer, "repository": REPO}],
            contained["advanced"],
        )

        for relation in ("behind", "diverged", "identical", None):
            with self.subTest(relation=relation):
                drifted = report(self.desired, [], snapshot, {} if relation is None else {REPO: relation})
                self.assertFalse(drifted["ok"], drifted)
                self.assertEqual(["source_pin"], [x["kind"] for x in drifted["mismatches"]])
                self.assertEqual([], drifted["advanced"])

    def test_drift_measures_ancestry_only_for_pins_that_no_longer_match(self):
        """A settled registry must not spend compare calls on every repository."""
        requested = []

        class CompareAPI:
            def compare_status(self, full_name, base, head):
                requested.append((full_name, base, head))
                return "ahead"

        client = CompareAPI()
        snapshot = self.snapshot()
        self.assertEqual({}, metadata_drift._pin_ancestry(self.desired, snapshot, client))
        self.assertEqual([], requested)

        snapshot["default_commit"] = "c" * 40
        relations = metadata_drift._pin_ancestry(self.desired, snapshot, client)
        self.assertEqual({REPO: "ahead"}, relations)
        self.assertEqual([(REPO, SHA, "c" * 40)], requested)

    def test_drift_ancestry_lookup_fails_closed_when_a_pin_cannot_be_measured(self):
        """An unmeasurable pin must stay a mismatch, never be assumed contained."""
        class Unreachable:
            def compare_status(self, full_name, base, head):
                raise APIError("GitHub returned non-JSON response for compare", "api")

        snapshot = self.snapshot()
        snapshot["default_commit"] = "c" * 40
        self.assertEqual({}, metadata_drift._pin_ancestry(self.desired, snapshot, Unreachable()))
        result = report(self.desired, [], snapshot, {})
        self.assertFalse(result["ok"])
        self.assertEqual(["source_pin"], [x["kind"] for x in result["mismatches"]])

    def test_compare_reads_only_the_relation_so_a_malformed_body_cannot_break_it(self):
        """A commit message can make the whole compare body invalid JSON.

        The full response embeds user-controlled commit text, and this
        organization has a commit whose body contains a literal ``\\u00"`` that
        makes the document unparseable.  A strict parse fails, and ``jq``
        cannot rescue it because it parses the same bytes.  The monitor must
        therefore read only the leading relation field, or one repository's
        commit text would turn an unrelated source into a reported mismatch.
        """
        malformed = (
            '{"url":"https://api.github.com/x","html_url":"https://github.com/x",'
            '"status":"ahead","ahead_by":3,"commits":[{"commit":{"message":'
            '"fix \\u00" in the body"'
            '}}]}'
        )

        class Runner:
            def __init__(self):
                self.calls = []

            def run(self, args, *, input_text=None, timeout=60):
                self.calls.append(list(args))
                return malformed

        runner = Runner()
        client = GitHubClient(runner=runner)
        self.assertEqual("ahead", client.compare_status(REPO, "a" * 40, "b" * 40))
        self.assertEqual(
            [["gh", "api", f"repos/AI-Ascension/example/compare/{'a' * 40}...{'b' * 40}?per_page=1"]],
            runner.calls,
        )

    def test_compare_ignores_a_status_key_that_comes_from_commit_text(self):
        """The relation is read from the top of the body only.

        A commit message can contain a `"status":"behind"` string.  The read
        stops at the first nested object, so a status key that only appears
        inside the commit payload is not mistaken for GitHub's own answer,
        which would invert the finding.
        """
        class Runner:
            def __init__(self, body):
                self.body = body

            def run(self, args, *, input_text=None, timeout=60):
                return self.body

        spoofed = '{"url":"u","status":"ahead","commits":[{"commit":{"message":"\\"status\\":\\"behind\\""}}]}'
        self.assertEqual("ahead", GitHubClient(runner=Runner(spoofed)).compare_status(REPO, "a" * 40, "b" * 40))
        nested_only = '{"url":"u","commits":[{"commit":{"message":"\\"status\\":\\"behind\\""}}],"total_commits":1}'
        self.assertIsNone(GitHubClient(runner=Runner(nested_only)).compare_status(REPO, "a" * 40, "b" * 40))
        self.assertIsNone(GitHubClient(runner=Runner("not json at all")).compare_status(REPO, "a" * 40, "b" * 40))

    def test_top_level_read_finds_the_relation_behind_a_nested_payload(self):
        """The relation follows the commit list, so a prefix match cannot work.

        The compare body puts the scalar relation after the embedded commits.
        A scan that stops at the first nested object would report nothing, so
        the reader must track depth across the whole document and still refuse
        a value that only appears inside a string or a nested object.
        """
        real = ('{"url":"u","html_url":"h","commits":[{"sha":"a","commit":{"message":"x"}}],'
                '"status":"behind","behind_by":2,"total_commits":1}')
        self.assertEqual("behind", _top_level_string(real, "status"))
        self.assertIsNone(_top_level_string('{"a":{"status":"diverged"}}', "status"))
        self.assertIsNone(_top_level_string('{"a":"\\"status\\":\\"diverged\\""}', "status"))
        self.assertIsNone(_top_level_string('{"a":1}', "status"))
        self.assertEqual("ahead", _top_level_string('{"a":1,"status":"ahead"}', "status"))

    def test_compare_refuses_untrusted_input_and_unmeasured_relations(self):
        """Only a real relation counts; anything else stays unmeasured."""
        class Runner:
            def run(self, args, *, input_text=None, timeout=60):
                return '{"url":"u","status":"nonsense"}'

        client = GitHubClient(runner=Runner())
        self.assertIsNone(client.compare_status(REPO, "not-a-sha", "b" * 40))
        self.assertIsNone(client.compare_status("../../etc", "a" * 40, "b" * 40))
        self.assertIsNone(client.compare_status("owner/name/extra", "a" * 40, "b" * 40))
        self.assertIsNone(client.compare_status(REPO, "a" * 40, "b" * 40))

    def test_drift_records_a_valid_exclusion_and_rejects_a_malformed_one(self):
        extra = repo_snapshot(rid=8, full="AI-Ascension/excluded-fixture")
        extra["visibility"] = "private"
        snapshot = {"repositories": [self.snapshot(), extra]}
        snapshot["applicability_exclusions"] = [
            {"repository_id": "8", "decision": "excluded-pending-owner", "reason": "Owner applicability decision pending."}
        ]
        self.assertTrue(report(self.desired, [], snapshot)["ok"])
        snapshot["applicability_exclusions"][0]["reason"] = "   "
        result = report(self.desired, [], snapshot)
        self.assertEqual(["invalid_or_stale_input"], [x["kind"] for x in result["mismatches"]])

    def test_drift_cli_can_write_its_report_and_signals_drift_with_a_nonzero_exit(self):
        """A report is still produced, and drift keeps the monitor's teeth."""
        import contextlib
        snapshot = self.snapshot()
        snapshot["default_commit"] = "c" * 40
        paths = {name: self.root / name for name in ("metadata.json", "labels.json", "snapshot.json", "report.json")}
        paths["metadata.json"].write_text(json.dumps(self.desired))
        paths["labels.json"].write_text("[]")
        paths["snapshot.json"].write_text(json.dumps(snapshot))
        argv = ["--metadata", str(paths["metadata.json"]), "--labels", str(paths["labels.json"]),
                "--snapshot", str(paths["snapshot.json"]), "--output", str(paths["report.json"])]
        with patch.object(sys, "argv", ["metadata_drift.py", *argv]), contextlib.redirect_stdout(io.StringIO()):
            code = metadata_drift.main()
        self.assertEqual(1, code)
        written = json.loads(paths["report.json"].read_text())
        self.assertEqual(["source_pin"], [x["kind"] for x in written["mismatches"]])

    def test_drift_cli_writes_report_for_unreadable_input(self):
        """A missing input is itself a reportable result, not a silent abort."""
        import contextlib
        report = self.root / "report.json"
        argv = ["--metadata", str(self.root / "absent.json"), "--labels", str(self.root / "absent-labels.json"),
                "--snapshot", str(self.root / "absent-snapshot.json"), "--output", str(report)]
        with patch.object(sys, "argv", ["metadata_drift.py", *argv]), contextlib.redirect_stdout(io.StringIO()):
            code = metadata_drift.main()
        self.assertEqual(1, code)
        written = json.loads(report.read_text())
        self.assertEqual(["invalid_or_stale_input"], [x["kind"] for x in written["mismatches"]])

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
