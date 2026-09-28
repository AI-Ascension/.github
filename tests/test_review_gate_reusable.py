"""The cross-repository gate contract, asserted rather than assumed.

The reusable form of the review gate is what `.github#49` will install in every
sibling repository, and it is what a required status check ruleset will name.
Two things about it are load-bearing and neither is checkable by running it:

1. The reference workflow must accept `workflow_call`, or a sibling's `uses:`
   is rejected at parse time and its check never exists -- which reads as a
   green required check that is not enforcing anything.
2. The job key must remain `review-of-record`, because the ruleset names the
   CHECK CONTEXT, not the file. A rename here silently invalidates every
   ruleset that was written against the old name, and nothing fails.
"""

import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / ".github" / "workflows" / "review-gate.yml"
CONSUMER = ROOT / ".github" / "workflows" / "review-gate-reusable.yml"

# The check context every installed ruleset names. Kept as a constant so a
# future change to either side fails one assertion instead of quietly
# un-invalidating the organisation's rulesets.
CHECK_CONTEXT = "review-of-record"


def triggers(workflow):
    """The `on:` block, whether or not PyYAML decoded it as the boolean True.

    YAML 1.1 reads a bare `on` key as the boolean `True`, and PyYAML follows
    1.1, so `workflow["on"]` is a `KeyError` and `workflow[True]` is the real
    mapping. Both spellings are accepted here so this test does not itself
    become a source of the confusion it is guarding against.
    """
    for key in ("on", True):
        if key in workflow:
            return workflow[key]
    raise AssertionError("workflow declares no trigger block")


class ReusableReferenceTest(unittest.TestCase):
    def test_reference_accepts_workflow_call(self):
        # Without this the sibling's `uses:` never resolves, and the required
        # check it was supposed to register does not exist.
        self.assertIn(
            "workflow_call", triggers(yaml.safe_load(REFERENCE.read_text()))
        )

    def test_consumer_calls_the_reference(self):
        job = yaml.safe_load(CONSUMER.read_text())["jobs"][CHECK_CONTEXT]
        self.assertIn("uses", job)
        # Pinned to a ref, never to a branch: a branch reference would let a
        # change to the reference alter a caller's required check with no
        # review in the calling repository at all.
        ref = job["uses"].split("@", 1)[1]
        self.assertNotIn("/", ref, f"consumer calls a branch or tag, not a commit: {ref}")
        self.assertGreaterEqual(
            len(ref), 40, f"consumer ref is not a full commit SHA: {ref}"
        )

    def test_consumer_job_key_is_the_check_context(self):
        # The ruleset names the context. This is the assertion that stops a
        # rename from silently detaching every installed ruleset.
        self.assertIn(CHECK_CONTEXT, yaml.safe_load(CONSUMER.read_text())["jobs"])

    def test_both_sides_read_only(self):
        # The gate runs a token and a shell block. Write scope would widen the
        # blast radius of a compromised reference for no benefit: the gate only
        # ever reads a pull request.
        for path in (REFERENCE, CONSUMER):
            permissions = yaml.safe_load(path.read_text())["permissions"]
            self.assertEqual(permissions.get("contents"), "read", path.name)
            self.assertNotIn("write", str(permissions), path.name)

    def test_gate_never_checks_out_the_pull_request_head(self):
        # Checking out the head would mean executing code the pull request
        # controls, in a job that holds a token -- so a PR editing the gate
        # could pass itself with zero reviews. This is asserted, not trusted,
        # because it is the single property the whole gate exists to provide.
        text = REFERENCE.read_text()
        self.assertIn("ref: ${{ github.event.repository.default_branch }}", text)
        self.assertIn("persist-credentials: false", text)

    def test_dispatch_input_is_not_a_string(self):
        # A `string` input would let a `workflow_dispatch` caller interpolate
        # `$(...)` into a `run:` block. `number` is coerced by GitHub before
        # interpolation, so the value cannot arrive as text.
        for path in (REFERENCE, CONSUMER):
            dispatch = triggers(yaml.safe_load(path.read_text())).get("workflow_dispatch")
            self.assertIsNotNone(dispatch, path.name)
            self.assertEqual(dispatch["inputs"]["number"]["type"], "number", path.name)


if __name__ == "__main__":
    unittest.main()
