#!/usr/bin/env python3
"""Read-only checks for the label catalog, migration matrix, and active forms."""

from __future__ import annotations

import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_SEED = {
    "AI-Ascension/.github": 1354466045,
    "AI-Ascension/AI-Ascension.github.io": 1354473981,
    "AI-Ascension/aiascension.tech": 1209899690,
    "AI-Ascension/sts2-harness": 1354378100,
    "AI-Ascension/sts2-mcp-server": 1354378057,
    "AI-Ascension/sts2-gateway": 1354378018,
    "AI-Ascension/sts2-game-mod": 1354377975,
    "AI-Ascension/sts2-game-core": 1354377929,
    "AI-Ascension/sts2-protocol": 1354378136,
    "AI-Ascension/ascension-watchdog": 1359537708,
    "AI-Ascension/ascension-map-visualizer": 1359701124,
    "AI-Ascension/ai-agent-observability": 1357224960,
}
SOURCE_DESTINATIONS = {
    "defect": "bug",
    "docs": "documentation",
    "wedge:player": "audience:player",
    "wedge:rust": "audience:rust",
    "wedge:mcp": "audience:mcp",
    "wedge:security": "audience:security",
}
SOURCE_PRESENT_REPOSITORIES = {
    name
    for name in PUBLIC_SEED
    if name not in {
        "AI-Ascension/aiascension.tech",
        "AI-Ascension/ascension-watchdog",
        "AI-Ascension/ascension-map-visualizer",
    }
}
OPTIONAL_TRIAGE_PREFIXES = ("priority:", "status:", "area:")


def read_yaml(path: Path):
    with path.open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)


class LabelCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.labels = read_yaml(ROOT / "labels.yml")
        cls.by_name = {row["name"]: row for row in cls.labels}
        cls.migrations = read_yaml(ROOT / "metadata" / "label-migrations.yml")

    def test_catalog_names_and_colors_are_unique_and_valid(self):
        self.assertEqual(len(self.labels), len(self.by_name))
        for row in self.labels:
            self.assertRegex(row["name"], r"^.{1,50}$")
            self.assertRegex(row["color"], r"^[0-9A-Fa-f]{6}$")
            self.assertTrue(row.get("description"))
            if "repository_ids" in row:
                self.assertIsInstance(row["repository_ids"], list)
                for repository_id in row["repository_ids"]:
                    self.assertRegex(str(repository_id), r"^[0-9]+$")

    def test_existing_palette_and_specialist_meanings_are_preserved(self):
        expected = {
            "first-task": ("2F7F66", "A bounded first contribution that needs no game, model, or credentials."),
            "proof-recipe": ("9C5B12", "A fixture, runnable check, adapter example, or showcase of a real run."),
            "contract-observation": ("4E6A8F", "An observed behavior of a public contract that the documents should state."),
            "evidence": ("9A7B1C", "A public claim, label, or description that looks wrong, unsupported, or unclear."),
            "unverified-claim": ("A8402F", "A statement on a public surface whose label may be stronger than its evidence."),
            "security": ("A8402F", "Security-relevant; details belong in the private channel per SECURITY.md."),
            "defect": ("9C5B12", "Behavior or a test that does not match the repository's own documents."),
            "docs": ("5E564A", "Documentation or public-page clarity."),
            "wedge:player": ("6F5A94", "Curious player or observer path."),
            "wedge:rust": ("6F5A94", "Rust or systems contributor path."),
            "wedge:mcp": ("6F5A94", "AI, MCP, or automation builder path."),
            "wedge:security": ("6F5A94", "Maintainer or security operator path."),
        }
        for name, (color, description) in expected.items():
            self.assertEqual((self.by_name[name]["color"], self.by_name[name]["description"]), (color, description))
        for name in ("wedge:player", "wedge:rust", "wedge:mcp", "wedge:security"):
            self.assertEqual(self.by_name[name]["repository_ids"], [])

    def test_work_kind_and_standard_triage_definitions_exist(self):
        for name in ("bug", "enhancement", "documentation", "research", "maintenance", "question", "good first issue", "help wanted"):
            self.assertIn(name, self.by_name)
        self.assertEqual(self.by_name["bug"]["color"], "d73a4a")
        self.assertEqual(self.by_name["documentation"]["color"], "0075ca")
        all_seed_ids = {str(repository_id) for repository_id in PUBLIC_SEED.values()}
        for name in ("research", "maintenance"):
            self.assertEqual(set(self.by_name[name]["repository_ids"]), all_seed_ids)

    def test_optional_overlays_have_explicit_applicability(self):
        for row in self.labels:
            name = row["name"]
            if name.startswith("area:"):
                self.assertIn("repository_ids", row)
                self.assertTrue(row["repository_ids"], name)
            if name.startswith(("priority:", "status:")):
                self.assertEqual(row.get("repository_ids"), [], name)
                self.assertTrue(row.get("applicability_reason"), name)


class LabelConsumerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.labels = read_yaml(ROOT / "labels.yml")
        cls.label_names = {row["name"] for row in cls.labels}
        cls.manifest = read_yaml(ROOT / "metadata" / "label-migrations.yml")

    def test_active_issue_forms_use_existing_safe_labels(self):
        for path in sorted((ROOT / ".github" / "ISSUE_TEMPLATE").glob("*.yml")):
            form = read_yaml(path)
            for label in form.get("labels", []) or []:
                self.assertIn(label, self.label_names, path.name)
                self.assertFalse(label == "good first issue" or label == "help wanted", path.name)
                self.assertFalse(label.startswith(OPTIONAL_TRIAGE_PREFIXES), path.name)
        defect = read_yaml(ROOT / ".github" / "ISSUE_TEMPLATE" / "defect.yml")
        self.assertEqual(defect["labels"], ["bug"])
        self.assertEqual(defect["title"], "[bug] ")

    def test_scope_covers_exactly_the_public_seed(self):
        scope = self.manifest["scope"]
        self.assertEqual(self.manifest["review_status"], "proposed")
        repositories = {row["repository"]: row for row in scope["repositories"]}
        self.assertEqual(set(repositories), set(PUBLIC_SEED))
        self.assertEqual(scope["seed_count"], 12)
        self.assertEqual(scope["excluded"]["visibility"], "private")
        self.assertEqual(scope["excluded"]["status"], "pending-explicit-applicability")
        for repository, repository_id in PUBLIC_SEED.items():
            self.assertEqual(repositories[repository]["repository_id"], repository_id)
            self.assertEqual(repositories[repository]["visibility"], "public")
            self.assertFalse(repositories[repository]["archived"])

    def test_migration_rows_match_live_presence_and_strategy(self):
        rows = self.manifest["migrations"]
        self.assertEqual(len(rows), 54)
        keys = {(row["repository"], row["from"], row["to"]) for row in rows}
        expected = {(repository, source, destination)
                   for repository in SOURCE_PRESENT_REPOSITORIES
                   for source, destination in SOURCE_DESTINATIONS.items()}
        self.assertEqual(keys, expected)
        for row in rows:
            self.assertEqual(row["repository_id"], PUBLIC_SEED[row["repository"]])
            self.assertTrue(row["source_present"])
            self.assertIsInstance(row["source_label_id"], int)
            self.assertGreater(row["source_label_id"], 0)
            if row["from"] in ("defect", "docs"):
                self.assertEqual(row["strategy"], "additive")
                self.assertTrue(row["destination_preexisting"])
                self.assertIsInstance(row["destination_label_id"], int)
                self.assertIsNone(row["stable_label_id"])
            else:
                self.assertEqual(row["strategy"], "rename")
                self.assertFalse(row["destination_preexisting"])
                self.assertIsNone(row["destination_label_id"])
                self.assertEqual(row["stable_label_id"], row["source_label_id"])

    def test_source_absence_is_recorded_without_noop_migration_rows(self):
        absent = {
            row["repository"]: set(row["source_labels_absent"])
            for row in self.manifest["scope"]["repositories"]
            if row["source_labels_absent"]
        }
        self.assertEqual(set(absent), {
            "AI-Ascension/aiascension.tech",
            "AI-Ascension/ascension-watchdog",
            "AI-Ascension/ascension-map-visualizer",
        })
        self.assertTrue(all(values == set(SOURCE_DESTINATIONS) for values in absent.values()))
        self.assertFalse(any(row["repository"] in absent for row in self.manifest["migrations"]))

    def test_assignment_counts_and_triage_decision_are_truthful(self):
        self.assertEqual(self.manifest["counts"]["migration_rows"], 54)
        self.assertEqual(self.manifest["counts"]["additive_collision_rows"], 18)
        self.assertEqual(self.manifest["counts"]["stable_id_rename_rows"], 36)
        self.assertEqual(self.manifest["counts"]["observed_source_assignments_to_migrate"], 2)
        self.assertEqual(self.manifest["counts"]["observed_open_source_assignments"], 0)
        self.assertEqual(self.manifest["counts"]["observed_closed_source_assignments"], 2)
        review = self.manifest["issue_first_task_review"]
        self.assertEqual(review["decision"], "no-good-first-issue-assignment")
        self.assertIn("read-only", review["mode"])
        self.assertIn("closed", review["reason"])
        self.assertFalse(any(row["to"] in {"good first issue", "help wanted"} for row in self.manifest["migrations"]))
        self.assertFalse(any(row["to"].startswith(OPTIONAL_TRIAGE_PREFIXES) for row in self.manifest["migrations"]))

    def test_audience_consumers_are_explicitly_inactive_until_provisioned(self):
        activation = self.manifest["consumer_activation"]
        self.assertEqual(activation["proposed_audience_consumers"]["status"], "inactive-until-provisioned")
        self.assertEqual(activation["current_forms"][0]["label"], "bug")
        self.assertIn("defect.yml", activation["current_forms"][0]["note"])


if __name__ == "__main__":
    unittest.main()
