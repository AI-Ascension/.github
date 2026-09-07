#!/usr/bin/env python3
"""Regression tests for metadata validation, planning, and snapshot collection."""

from __future__ import annotations

import importlib.util
import json
import copy
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("metadata_tool", ROOT / "tools" / "metadata.py")
assert SPEC and SPEC.loader
metadata = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(metadata)


SHA = "a" * 40
SHA2 = "b" * 40


def evidence(subject: str = "implementation", reason: str = "reviewed source") -> dict:
    return {
        "name": "ai-ascension",
        "meaning": "shared organization identity",
        "subject": subject,
        "reason": reason,
        "evidence": {"repository": "AI-Ascension/example", "commit": SHA, "path": "README.md"},
    }


def repo_snapshot(*, topics=None, labels=None, issues=None, rid=1, full="AI-Ascension/example", branch="main", commit=SHA):
    return {
        "id": rid,
        "full_name": full,
        "name": full.rsplit("/", 1)[1],
        "default_branch": branch,
        "default_commit": commit,
        "archived": False,
        "visibility": "public",
        "topics": {"names": list(topics if topics is not None else ["ai-ascension"])},
        "labels": list(labels if labels is not None else []),
        "issues": list(issues if issues is not None else []),
    }


def metadata_map(*, topics=None, kind="implementation", review_status="reviewed", blockers=None, rid=1, full="AI-Ascension/example", branch="main", commit=SHA):
    return {
        "schema_version": 1,
        "organization": "AI-Ascension",
        "brand_topic": "ai-ascension",
        "review_status": review_status,
        "blockers": list(blockers or []),
        "repositories": [{
            "id": rid,
            "full_name": full,
            "name": full.rsplit("/", 1)[1],
            "kind": kind,
            "default_branch": branch,
            "default_commit": commit,
            "topics": list(topics if topics is not None else [evidence()]),
            "topic_removals": [],
        }],
    }


class FakeRunner:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def run(self, args, *, input_text=None, timeout=60):
        self.calls.append((list(args), input_text, timeout))
        if not self.responses:
            raise AssertionError("unexpected command")
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return response


class MetadataValidationTests(unittest.TestCase):
    def test_topic_dict_and_snapshot_are_normalized(self):
        snapshot = metadata.validate_snapshot(repo_snapshot(topics=["ai-ascension"]))
        self.assertEqual(snapshot["repositories"][0]["topics"], {"names": ["ai-ascension"]})

    def test_topic_grammar_count_and_uniqueness_fail_closed(self):
        bad = metadata_map(topics=[evidence(), {**evidence(), "name": "Bad_Topic"}])
        with self.assertRaises(metadata.MetadataError):
            metadata.normalize_metadata(bad)
        too_many = [dict(evidence(), name=f"topic-{i}") for i in range(21)]
        too_many[0] = evidence()
        with self.assertRaises(metadata.MetadataError):
            metadata.normalize_metadata(metadata_map(topics=too_many))
        duplicate = [evidence(), dict(evidence(), name="ai-ascension")]
        with self.assertRaises(metadata.MetadataError):
            metadata.normalize_metadata(metadata_map(topics=duplicate))

    def test_missing_reason_and_removal_evidence_fail(self):
        with self.assertRaisesRegex(metadata.MetadataError, "reason"):
            metadata.normalize_metadata(metadata_map(topics=[dict(evidence(), reason="")]))
        removal = dict(evidence(), name="legacy-topic")
        value = metadata_map()
        value["repositories"][0]["topic_removals"] = [{"name": "legacy-topic", "meaning": "old", "subject": "implementation", "reason": "remove"}]
        with self.assertRaisesRegex(metadata.MetadataError, "evidence"):
            metadata.normalize_metadata(value)

    def test_planning_rows_need_planned_subject(self):
        with self.assertRaisesRegex(metadata.MetadataError, "planning repository"):
            metadata.normalize_metadata(metadata_map(kind="planning"))
        mixed = metadata_map(kind="planning", topics=[dict(evidence("planned"), name="planning"), evidence()])
        with self.assertRaisesRegex(metadata.MetadataError, "cannot claim implementation"):
            metadata.normalize_metadata(mixed)

    def test_snapshot_unknown_fields_are_not_empty(self):
        value = repo_snapshot()
        del value["labels"]
        with self.assertRaisesRegex(metadata.MetadataError, "unknown is not empty"):
            metadata.validate_snapshot(value)

    def test_snapshot_requires_stable_label_ids_and_casefold_identity(self):
        with self.assertRaisesRegex(metadata.MetadataError, "stable ID"):
            metadata.validate_snapshot(repo_snapshot(labels=[{"name": "docs", "color": "ffffff", "description": ""}]))
        with self.assertRaises(metadata.MetadataError):
            metadata.normalize_labels([
                {"name": "Defect", "color": "ffffff", "description": ""},
                {"name": "defect", "color": "000000", "description": ""},
            ])

    def test_identity_and_default_branch_are_checked_against_snapshot(self):
        value = metadata_map(branch="main")
        with self.assertRaisesRegex(metadata.MetadataError, "default branch drift"):
            metadata.validate_metadata(value, snapshot=repo_snapshot(branch="bootstrap"))

    def test_visibility_is_checked_and_archived_repository_is_write_blocked(self):
        value = metadata_map()
        value["repositories"][0]["visibility"] = "public"
        current = repo_snapshot()
        current["visibility"] = "private"
        with self.assertRaisesRegex(metadata.MetadataError, "visibility drift"):
            metadata.make_plan(value, current, labels=[], migrations=[])
        current["visibility"] = "public"
        current["archived"] = True
        with self.assertRaisesRegex(metadata.MetadataError, "archived"):
            metadata.make_plan(value, current, labels=[], migrations=[])

    def test_archive_timestamp_is_authoritative_for_labels(self):
        value = [{"id": 10, "name": "docs", "color": "ffffff", "description": "", "archived_at": "2026-01-01T00:00:00Z"}]
        normalized = metadata.normalize_labels([{k: v for k, v in value[0].items() if k != "id"}])
        self.assertTrue(normalized[0]["archived"])
        with self.assertRaisesRegex(metadata.MetadataError, "archived"):
            metadata.make_plan(metadata_map(), repo_snapshot(labels=value), labels=[], migrations=[{"repository": "AI-Ascension/example", "from": "docs", "to": "other", "strategy": "additive"}])


class MetadataPlanTests(unittest.TestCase):
    def test_plan_is_stable_and_preserves_unlisted_topics(self):
        current = repo_snapshot(topics=["ai-ascension", "legacy-topic"])
        desired = metadata_map(topics=[evidence()])
        first = metadata.make_plan(desired, current, labels=[], migrations=[])
        second = metadata.make_plan(desired, current, labels=[], migrations=[])
        self.assertEqual(first["digest"], second["digest"])
        self.assertFalse(first["targets"][0]["operations"])

    def test_full_replacement_requires_explicit_removal_and_writes_complete_set(self):
        desired = metadata_map(topics=[evidence()])
        desired["repositories"][0]["replace_topics"] = True
        with self.assertRaisesRegex(metadata.MetadataError, "omits current topics"):
            metadata.make_plan(desired, repo_snapshot(topics=["ai-ascension", "legacy-topic"]), labels=[], migrations=[])
        removal = dict(evidence(), name="legacy-topic", reason="reviewed removal")
        desired["repositories"][0]["topic_removals"] = [removal]
        plan = metadata.make_plan(desired, repo_snapshot(topics=["ai-ascension", "legacy-topic"]), labels=[], migrations=[])
        operation = plan["targets"][0]["operations"][0]
        self.assertEqual(operation["kind"], "replace_topics")
        self.assertEqual(operation["after"], ["ai-ascension"])

    def test_blocked_map_produces_non_applicable_plan(self):
        desired = metadata_map(review_status="incomplete-missing-companions", blockers=["proposal missing"])
        plan = metadata.make_plan(desired, repo_snapshot(), labels=[], migrations=[])
        self.assertFalse(plan["review"]["applicable"])
        self.assertIn("proposal missing", plan["review"]["blockers"])
        self.assertTrue(any("source tree" in blocker for blocker in plan["review"]["blockers"]))

    def test_rename_collision_and_additive_assignment_contract(self):
        labels = [
            {"id": 10, "name": "defect", "color": "ffffff", "description": "old"},
            {"id": 11, "name": "bug", "color": "ff0000", "description": "new"},
        ]
        issue = {"id": 501, "number": 7, "labels": [labels[0], {"id": 12, "name": "docs", "color": "00ff00"}]}
        current = repo_snapshot(labels=labels, issues=[issue])
        desired = metadata_map()
        with self.assertRaisesRegex(metadata.MetadataError, "destination.*already exists"):
            metadata.make_plan(desired, current, labels=[], migrations=[{"repository": "AI-Ascension/example", "from": "defect", "to": "bug", "strategy": "rename"}])
        plan = metadata.make_plan(desired, current, labels=[], migrations=[{"repository": "AI-Ascension/example", "from": "defect", "to": "bug", "strategy": "additive"}])
        op = plan["targets"][0]["operations"][0]
        self.assertEqual(op["kind"], "additive_label_migration")
        self.assertEqual(op["assignments"][0]["labels"][0], {"id": 10, "name": "defect"})
        self.assertFalse(op["assignments"][0]["destination_preexisting"])

    def test_shared_definitions_are_added_without_deleting_unmanaged_labels(self):
        current = repo_snapshot(labels=[{"id": 10, "name": "unmanaged", "color": "ffffff", "description": "keep"}])
        desired = metadata_map()
        shared = [{"name": "docs", "color": "111111", "description": "shared docs"}]
        plan = metadata.make_plan(desired, current, labels=shared, migrations=[])
        self.assertEqual([x["kind"] for x in plan["targets"][0]["operations"]], ["create_label"])
        self.assertEqual(plan["targets"][0]["operations"][0]["after"]["id"], "new")

    def test_rename_coalesces_canonical_destination_definition(self):
        source = {"id": 10, "name": "defect", "color": "ffffff", "description": "old"}
        current = repo_snapshot(labels=[source])
        desired = metadata_map()
        shared = [{"name": "bug", "color": "ff0000", "description": "canonical bug"}]
        plan = metadata.make_plan(desired, current, labels=shared, migrations=[{"repository": "AI-Ascension/example", "from": "defect", "to": "bug", "strategy": "rename"}])
        ops = plan["targets"][0]["operations"]
        self.assertEqual([x["kind"] for x in ops], ["rename_label"])
        self.assertEqual(ops[0]["after"]["color"], "FF0000")
        self.assertEqual(ops[0]["after"]["description"], "canonical bug")

    def test_overlapping_migrations_require_separate_reviewed_waves(self):
        labels = [
            {"id": 10, "name": "one", "color": "ffffff", "description": ""},
            {"id": 11, "name": "two", "color": "ffffff", "description": ""},
        ]
        desired = metadata_map()
        migrations = [
            {"repository": "AI-Ascension/example", "from": "one", "to": "three", "strategy": "rename"},
            {"repository": "AI-Ascension/example", "from": "three", "to": "four", "strategy": "rename"},
        ]
        with self.assertRaisesRegex(metadata.MetadataError, "overlapping"):
            metadata.make_plan(desired, repo_snapshot(labels=labels), labels=[], migrations=migrations)

    def test_repository_selection_is_sorted_and_bound_to_plan_digest(self):
        desired = metadata_map()
        second = copy.deepcopy(desired["repositories"][0])
        second.update({"id": 2, "repository_id": 2, "full_name": "AI-Ascension/second", "name": "second"})
        desired["repositories"].append(second)
        current = [repo_snapshot(rid=1), repo_snapshot(rid=2, full="AI-Ascension/second")]
        canary = metadata.make_plan(desired, current, labels=[], migrations=[], repository_ids=[2])
        fleet = metadata.make_plan(desired, current, labels=[], migrations=[])
        self.assertEqual(["2"], canary["selection"]["repository_ids"])
        self.assertTrue(canary["selection"]["explicit"])
        self.assertEqual(["2"], [target["repository_id"] for target in canary["targets"]])
        self.assertNotEqual(canary["digest"], fleet["digest"])
        with self.assertRaisesRegex(metadata.MetadataError, "duplicate"):
            metadata.make_plan(desired, current, labels=[], migrations=[], repository_ids=[2, "2"])
        with self.assertRaisesRegex(metadata.MetadataError, "unknown"):
            metadata.make_plan(desired, current, labels=[], migrations=[], repository_ids=[99])

    def test_protected_and_triage_label_migrations_fail_closed(self):
        desired = metadata_map()
        current = repo_snapshot(labels=[{"id": 1, "name": "first-task", "color": "ffffff", "description": ""}])
        for migration in (
            {"repository": "AI-Ascension/example", "from": "first-task", "to": "starter", "strategy": "rename"},
            {"repository": "AI-Ascension/example", "from": "first-task", "to": "help wanted", "strategy": "additive"},
            {"repository": "AI-Ascension/example", "from": "first-task", "to": "priority-high", "strategy": "additive"},
            {"repository": "AI-Ascension/example", "from": "first-task", "to": "evidence", "strategy": "additive"},
        ):
            with self.assertRaisesRegex(metadata.MetadataError, "protected|automatically assign"):
                metadata.make_plan(desired, current, labels=[], migrations=[migration])


class SnapshotAndAuthorizationTests(unittest.TestCase):
    def test_paginated_org_listing_is_flattened_and_sorted(self):
        rows = [
            {"id": 2, "full_name": "AI-Ascension/b", "name": "b"},
            {"id": 1, "full_name": "AI-Ascension/a", "name": "a"},
        ]
        runner = FakeRunner([json.dumps([rows[:1], rows[1:]])])
        client = metadata.GitHubClient(runner=runner, retries=0)
        self.assertEqual([x["id"] for x in client.list_org_repositories("AI-Ascension")], [1, 2])
        self.assertIn("--paginate", runner.calls[0][0])
        self.assertIn("--slurp", runner.calls[0][0])

    def test_write_failures_are_not_retried_by_client(self):
        runner = FakeRunner([metadata.APIError("rate limited", "rate_limit")])
        client = metadata.GitHubClient(runner=runner, retries=3)
        with self.assertRaises(metadata.APIError):
            client._run("repos/AI-Ascension/example/topics", method="PUT", payload={"names": ["ai-ascension"]})
        self.assertEqual(len(runner.calls), 1)

    def test_rate_limited_reads_stop_without_guessed_retry_delay(self):
        runner = FakeRunner([metadata.APIError("rate limited", "rate_limit")])
        client = metadata.GitHubClient(runner=runner, retries=3)
        with self.assertRaises(metadata.APIError):
            client._run("repos/AI-Ascension/example/topics")
        self.assertEqual(1, len(runner.calls))

    def test_authorization_binds_to_64_char_plan_digest_operator_and_targets(self):
        plan = {"digest": "c" * 64, "targets": [{"repository_id": "1", "operations": [{"kind": "replace_topics"}]}]}
        auth = {"plan_digest": "c" * 64, "operator": "maintainer", "authorization_id": "review-1", "repositories": ["1"], "operations": ["topics"], "approval_record": {"record_id": "PR-1", "reviewer": "owner", "decision": "approved"}}
        metadata._authorization(auth, plan, "maintainer")
        with self.assertRaises(metadata.MetadataError):
            metadata._authorization({**auth, "plan_digest": "d" * 64}, plan, "maintainer")
        with self.assertRaises(metadata.MetadataError):
            metadata._authorization(auth, plan, "other")

    def test_rollback_requires_distinct_authorization_operation(self):
        plan = {"digest": "c" * 64, "targets": [{"repository_id": "1", "operations": [{"kind": "replace_topics"}]}]}
        auth = {"plan_digest": "c" * 64, "operator": "maintainer", "authorization_id": "review-1", "repositories": ["1"], "operations": ["topics"], "approval_record": {"record_id": "PR-1", "reviewer": "owner", "decision": "approved"}}
        with self.assertRaisesRegex(metadata.MetadataError, "distinct rollback"):
            metadata._authorization(auth, plan, "maintainer", operation="rollback")
        metadata._authorization({**auth, "operations": ["rollback"]}, plan, "maintainer", operation="rollback")


if __name__ == "__main__":
    unittest.main()
