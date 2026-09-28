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


def executable_lines(path):
    """The file with its comments stripped.

    These workflows carry a lot of prose explaining *why* a spelling is
    wrong, and that prose necessarily contains the wrong spelling. A
    substring assertion over the raw file would therefore fail against the
    documentation of the very defect it is checking for, so the checks that
    assert an expression is ABSENT run over this instead.
    """
    return "\n".join(
        line for line in path.read_text().split("\n") if not line.lstrip().startswith("#")
    )


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
        #
        # The checkout reads `GATE_REPOSITORY`/`GATE_REF` from the environment
        # rather than from `github.event.repository`, because for a
        # `workflow_call` those are the reference repository and the pinned
        # commit -- the caller's context would name the caller's `main`, which
        # has no gate in it at all.
        text = REFERENCE.read_text()
        self.assertIn("repository: ${{ env.GATE_REPOSITORY }}", text)
        self.assertIn("ref: ${{ env.GATE_REF }}", text)
        self.assertNotIn("ref: ${{ github.event.repository.default_branch }}", text)
        self.assertIn("persist-credentials: false", text)

    def test_unresolved_gate_source_fails_closed(self):
        # A caller that supplies no `gate-sha` gets this repository's own
        # default branch, which is correct for a direct trigger and WRONG for a
        # reusable call -- so a supplied-but-malformed value must be a hard
        # error rather than falling through to that default.
        text = REFERENCE.read_text()
        self.assertIn("resolved=reusable-call", text)
        self.assertIn("resolved=direct-trigger", text)
        self.assertIn("exit 1", text)

    def test_gate_source_comes_from_caller_supplied_inputs(self):
        # A called workflow INHERITS the caller's event. Measured on
        # ascension-context-console#43: inside the gate, `github.event_name`
        # was `pull_request` and `github.workflow_sha` was the CALLER's merge
        # commit. So neither can identify the caller's pinned reference, and a
        # caller must state it. This asserts the inputs exist and that the
        # resolution step reads them.
        call = triggers(yaml.safe_load(REFERENCE.read_text()))["workflow_call"]
        self.assertIn("gate-repository", call["inputs"])
        self.assertIn("gate-sha", call["inputs"])
        text = executable_lines(REFERENCE)
        self.assertIn("${{ inputs.gate-sha }}", text)
        self.assertIn("${{ inputs.gate-repository }}", text)
        # And the event-derived spellings must be gone, so the wrong signal
        # cannot creep back in. Asserting their absence is what makes this
        # test a regression guard rather than a description. The check is on
        # executable lines only: the file documents why these spellings are
        # wrong, and a naive substring check would flag its own explanation.
        self.assertNotIn("github.event_name == 'workflow_call'", text)
        self.assertNotIn("${{ github.workflow_sha }}", text)

    def test_gate_sha_is_validated_before_use(self):
        # `gate-sha` is a `string` input, so unlike `workflow_dispatch`'s
        # `number` it is NOT coerced by GitHub. It is interpolated into a
        # shell block, so an unvalidated value would be an injection surface.
        # The step must reject anything that is not a 40-character hex SHA
        # before it reaches the checkout.
        text = executable_lines(REFERENCE)
        self.assertIn("gate-sha must be a 40-character commit SHA", text)
        self.assertIn('*[!0-9a-f]*', text)
        self.assertIn('-ne 40', text)

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
