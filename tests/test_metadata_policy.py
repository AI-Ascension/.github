"""Management boundaries and reviewable plans, using synthetic repository data."""
import copy
import unittest

from test_metadata import metadata, metadata_map, repo_snapshot, evidence


class ManagementTests(unittest.TestCase):
    def test_unqueried_archive_and_visibility_are_not_assumed_safe(self):
        for field in ("archived", "visibility"):
            value = repo_snapshot()
            del value[field]
            with self.assertRaises(metadata.MetadataError):
                metadata.validate_snapshot(value)

    def test_unlisted_discovery_requires_explicit_local_exclusion(self):
        desired = metadata_map()
        extra = repo_snapshot(rid=2, full="AI-Ascension/private-fixture")
        extra["visibility"] = "private"
        snapshot = {"schema_version": 1, "repositories": [repo_snapshot(), extra]}
        with self.assertRaisesRegex(metadata.MetadataError, "applicability"):
            metadata.make_plan(desired, snapshot, labels=[], migrations=[])
        snapshot["applicability_exclusions"] = [{"repository_id": "2", "decision": "excluded-pending-owner", "reason": "Synthetic private repository excluded pending owner scope."}]
        plan = metadata.make_plan(desired, snapshot, labels=[], migrations=[])
        self.assertEqual(["1"], plan["selection"]["repository_ids"])
        self.assertNotIn("private-fixture", metadata.canonical_json(plan))
        with self.assertRaises(metadata.MetadataError):
            metadata.make_plan(desired, snapshot, labels=[], migrations=[], repository_ids=[2])

    def test_managed_false_cannot_be_selected(self):
        desired = metadata_map()
        excluded = copy.deepcopy(desired["repositories"][0])
        excluded.update(id=2, name="excluded", full_name="AI-Ascension/excluded", managed=False,
                        applicability_reason="No source management requested.")
        desired["repositories"].append(excluded)
        plan = metadata.make_plan(desired, repo_snapshot(), labels=[], migrations=[])
        self.assertEqual(["1"], plan["selection"]["repository_ids"])
        with self.assertRaises(metadata.MetadataError):
            metadata.make_plan(desired, repo_snapshot(), labels=[], migrations=[], repository_ids=[2])

    def test_project_planning_marker_cannot_claim_implementation(self):
        topics = [evidence(subject="planned"), {**evidence(subject="planned"), "name": "project-planning"}]
        metadata.normalize_metadata(metadata_map(kind="planning", topics=topics))
        topics[1]["subject"] = "implementation"
        with self.assertRaises(metadata.MetadataError):
            metadata.normalize_metadata(metadata_map(kind="planning", topics=topics))

    def test_operations_bind_review_evidence_blast_radius_and_inverse(self):
        desired = metadata_map(topics=[evidence(), {**evidence(), "name": "rust"}])
        plan = metadata.make_plan(desired, repo_snapshot(), labels=[], migrations=[])
        op = plan["targets"][0]["operations"][0]
        self.assertEqual("administration:write", op["required_permission"])
        self.assertEqual(["ai-ascension"], op["inverse"]["restore"])
        self.assertEqual(2, len(op["evidence"]))
        self.assertTrue(op["blast_radius"]["repository_topics"])
        changed = copy.deepcopy(plan)
        changed["targets"][0]["operations"][0]["reason"] = "unreviewed change"
        self.assertNotEqual(plan["digest"], metadata.digest({k: v for k, v in changed.items() if k != "digest"}))

    def test_misspelled_or_unknown_label_scope_cannot_become_global(self):
        definition = {"name": "area:metadata", "color": "abcdef", "description": "Scoped work"}
        with self.assertRaises(metadata.MetadataError):
            metadata.normalize_labels([{**definition, "repositor_ids": [1]}])
        with self.assertRaises(metadata.MetadataError):
            metadata.make_plan(metadata_map(), repo_snapshot(), labels=[{**definition, "repository_ids": [999]}], migrations=[])


if __name__ == "__main__":
    unittest.main()
