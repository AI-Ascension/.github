# Reviewed reusable-gate source

`7e5e885835ddb09cd7927412f61c63f4c42bb57a.yml` is the exact, unmodified
`.github/workflows/review-gate.yml` blob from `AI-Ascension/.github` commit
`7e5e885835ddb09cd7927412f61c63f4c42bb57a` (trusted-source input correction, #56).
Git blob: `262df6486dfe25f62c4599e0f1da768dd396bc02`.

The consumer previously pinned `dc0777e892af4b725d2a234a8174c1e763201f35`,
whose workflow does not declare `workflow_call`. Checking only the current
local canonical workflow missed this historical-source mismatch.

For a pin upgrade, independently review the candidate workflow, evaluator and
tests, then export the workflow with `git show <reviewed-sha>:.github/workflows/review-gate.yml`.
Record its `git rev-parse <reviewed-sha>:.github/workflows/review-gate.yml` blob
ID in the test and update both consumer references together. The regression
loads the exported historical source without network access or Git history;
it does not infer callability from the current branch or blindly fetch code.

Scope: this repair restores the pull-request and review-event calls. The
pinned callee does not accept a `number` workflow-call input, so the wrapper's
existing manual dispatch does not forward its number and remains fail-closed.
Manual-dispatch support requires a separate canonical contract change before
a consumer pin update; this fixture is not evidence that dispatch is repaired.

## Canonical dispatch contract (not the historical pin)

`source-derived`: GitHub's [reusable-workflow context reference](https://docs.github.com/en/actions/reference/workflows-and-actions/reusing-workflow-configurations#github-context)
associates `github` with the caller, whereas its [inputs reference](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts#inputs-context)
defines reusable `inputs` from `workflow_call` and the caller's `with` block.
The [dispatch event reference](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#workflow_dispatch)
also exposes manual inputs in `github.event.inputs`. Both automatic events
supply top-level `pull_request` in their [webhook payload](https://docs.github.com/en/webhooks/webhook-events-and-payloads#pull_request_review).

The current canonical workflow therefore selects `github.event.inputs.number`
only when the inherited event name is `workflow_dispatch`; `pull_request` and
`pull_request_review` exclusively select `github.event.pull_request.number`.
It accepts a positive decimal integer without leading zeroes, rejects missing
or malformed values and unsupported events, and passes context values as env
data rather than interpolating them into shell source. No callable `number`
or repository-identity override is added; `gate-repository` and `gate-sha`
remain implementation-location inputs, not the PR identity.

`confirmed` by `python -m unittest tests/test_review_gate_events.py -v`: local
modeled-context tests execute the canonical shell for direct/reusable dispatch,
automatic events, conflicting inputs, malformed numbers, injection-like text,
and evaluator failure. These are not hosted Actions tests or proof of a live
manual dispatch. Live dispatch remains `unverified`.

This canonical change alone does not repair the wrapper's historical pin.
After the canonical change lands and its resulting immutable commit is
reviewed, update the consumer's `uses` SHA and `gate-sha` together, exporting
that commit's exact workflow fixture and updating its blob assertion. No
consumer pin is advanced in the canonical repair.
