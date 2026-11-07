"""Execute the canonical shell with modeled GitHub contexts, not hosted Actions.

Expressions are deliberately restricted to plain context-property lookup. This
checks our wiring and script, not GitHub's implementation of event inheritance.
"""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / '.github/workflows/review-gate.yml'


class ReviewGateEventsTest(unittest.TestCase):
    workflow_path = WORKFLOW

    def setUp(self):
        self.workflow = yaml.safe_load(self.workflow_path.read_text())
        self.step = self.workflow['jobs']['review-of-record']['steps'][-1]

    def run_event(self, name, event, inputs=None, exit_code=0):
        context = {'github': {'event_name': name, 'event': event,
                             'repository': 'AI-Ascension/example', 'token': ''},
                   'inputs': inputs or {}}
        # Resolve the exact workflow env bindings. An accidental inputs.number
        # regression fails reusable-dispatch and conflicting-input tests.
        env = dict(os.environ)
        for key, expression in self.step['env'].items():
            self.assertTrue(expression.startswith('${{ ') and expression.endswith(' }}'))
            value = context
            for part in expression[4:-3].split('.'):
                value = value.get(part, '') if isinstance(value, dict) else ''
            env[key] = str(value)
        self.assertNotIn('${{', self.step['run'])
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            # A stub evaluator records argv; no token, network, or real PR read.
            (root / 'tools').mkdir()
            (root / 'tools/review_gate.py').write_text(
                'import json, sys\n'
                'from pathlib import Path\n'
                "Path('argv.json').write_text(json.dumps(sys.argv[1:]))\n"
                f'raise SystemExit({exit_code})\n'
            )
            result = subprocess.run(['bash', '-e', '-o', 'pipefail', '-c', self.step['run']],
                                    cwd=root, env=env, capture_output=True, text=True,
                                    timeout=10)
            argv = json.loads((root / 'argv.json').read_text()) if (root / 'argv.json').exists() else None
            self.assertFalse((root / 'injected').exists())
            return result, argv

    def assert_number(self, name, event, inputs, number):
        result, argv = self.run_event(name, event, inputs)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(argv, ['--repository', 'AI-Ascension/example', '--number', number])

    def test_direct_dispatch(self):
        self.assert_number('workflow_dispatch', {'inputs': {'number': '42'}}, {'number': 42}, '42')

    def test_reusable_dispatch_without_callable_number(self):
        self.assert_number('workflow_dispatch', {'inputs': {'number': '42'}},
                           {'gate-repository': 'AI-Ascension/.github', 'gate-sha': 'a' * 40}, '42')

    def test_dispatch_uses_original_event_not_callable_input_or_pr(self):
        self.assert_number('workflow_dispatch', {'inputs': {'number': '42'},
                           'pull_request': {'number': 99}}, {'number': 99}, '42')

    def test_automatic_events_ignore_dispatch_and_callable_numbers(self):
        for name in ('pull_request', 'pull_request_review'):
            with self.subTest(name=name):
                self.assert_number(name, {'pull_request': {'number': 42},
                                   'inputs': {'number': '99'},
                                   'review': {'pull_request': {'number': 99}}},
                                   {'number': 99}, '42')

    def test_automatic_events_do_not_fall_back_to_manual_number(self):
        for name in ('pull_request', 'pull_request_review'):
            result, argv = self.run_event(name, {'inputs': {'number': '99'},
                                          'review': {'pull_request': {'number': 99}}}, {'number': 99})
            self.assertNotEqual(result.returncode, 0)
            self.assertIsNone(argv)

    def test_invalid_or_missing_numbers_fail_before_evaluator(self):
        for name in ('workflow_dispatch', 'pull_request', 'pull_request_review'):
            for number in ('', '0', '01', '-1', '1.5', '1e2', ' 42', '42\n', '１２',
                           '$(touch injected)', '`touch injected`', '42; touch injected'):
                with self.subTest(name=name, number=number):
                    event = {'inputs': {'number': number}, 'pull_request': {'number': number}}
                    result, argv = self.run_event(name, event, {'number': 99})
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIsNone(argv)
            result, argv = self.run_event(name, {}, {'number': 99})
            self.assertNotEqual(result.returncode, 0)
            self.assertIsNone(argv)

    def test_unsupported_events_fail_closed(self):
        for name in ('push', 'workflow_call', ''):
            result, argv = self.run_event(name, {'inputs': {'number': '42'},
                                          'pull_request': {'number': 42}})
            self.assertNotEqual(result.returncode, 0)
            self.assertIsNone(argv)

    def test_evaluator_failure_is_not_swallowed(self):
        result, argv = self.run_event('workflow_dispatch', {'inputs': {'number': '42'}}, exit_code=1)
        self.assertEqual(result.returncode, 1)
        self.assertIsNotNone(argv)

    def test_no_callable_identity_override_or_security_context_change(self):
        triggers = self.workflow.get('on', self.workflow.get(True))
        self.assertEqual(set(triggers['workflow_call']['inputs']), {'gate-repository', 'gate-sha'})
        self.assertEqual(self.workflow['permissions'], {'contents': 'read', 'pull-requests': 'read'})
        self.assertEqual(set(self.workflow['jobs']), {'review-of-record'})
        checkout = next(step for step in self.workflow['jobs']['review-of-record']['steps']
                        if step.get('uses', '').startswith('actions/checkout@'))
        self.assertEqual(checkout['with'], {'repository': '${{ env.GATE_REPOSITORY }}',
                                          'ref': '${{ env.GATE_REF }}', 'persist-credentials': False})


class PinnedReviewGateEventsTest(ReviewGateEventsTest):
    """Run the same safety cases against the actual immutable caller target."""
    def setUp(self):
        caller = yaml.safe_load((ROOT / '.github/workflows/review-gate-reusable.yml').read_text())
        pin = caller['jobs']['review-of-record']['uses'].split('@', 1)[1]
        self.workflow_path = ROOT / 'tests/fixtures/review-gate' / f'{pin}.yml'
        super().setUp()


if __name__ == '__main__':
    unittest.main()
