"""Inventory-only additions remain known but never become write targets."""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import metadata
from metadata_drift import report
from test_metadata import metadata_map, repo_snapshot


class InventoryAdditionTests(unittest.TestCase):
    def test_public_discoveries_are_known_without_authorizing_writes(self):
        registry = json.loads((ROOT / 'metadata/repositories.yml').read_text())
        expected = {'AI-Ascension/STS2MCP': (1192832633, True),
                    'AI-Ascension/jev-factorio-agent': (1379060982, False)}
        desired = metadata_map()
        observed = [repo_snapshot()]
        for name, (rid, archived) in expected.items():
            row = next(r for r in registry['repositories'] if r['full_name'] == name)
            self.assertEqual(rid, row['id'])
            self.assertEqual('public', row['visibility'])
            self.assertEqual(archived, row['archived'])
            self.assertIs(row['managed'], False)
            self.assertTrue(row['applicability_reason'])
            self.assertEqual('add', row['topics'][0]['change'])
            self.assertEqual('proposed', row['topics'][0]['evidence']['classification'])
            desired['repositories'].append(copy.deepcopy(row))
            live = repo_snapshot(rid=rid, full=name, commit=row['default_commit'],
                                 topics=['unmanaged-existing-topic'])
            live['archived'] = archived
            observed.append(live)
        snapshot = {'repositories': observed}
        before = report(metadata_map(), [], snapshot)
        self.assertEqual(set(expected), {r['repository'] for r in before['mismatches']})
        self.assertTrue(all(r['kind'] == 'unmapped_repository' for r in before['mismatches']))
        self.assertTrue(report(desired, [], snapshot)['ok'])
        plan = metadata.make_plan(desired, snapshot, labels=[], migrations=[])
        self.assertFalse(set(expected) & {t['repository'] for t in plan['targets']})
        # A subsequent unknown repository still fails: no broad exclusion added.
        observed.append(repo_snapshot(rid=99, full='AI-Ascension/unknown-fixture'))
        result = report(desired, [], snapshot)
        self.assertEqual([{'kind': 'unmapped_repository',
                           'repository': 'AI-Ascension/unknown-fixture'}], result['mismatches'])
