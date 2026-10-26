# Reviewed reusable-gate source

## Current caller pin

`9a92f68d06a6c7c2dbc9ab6723198bde457a1902.yml` is the exact, unmodified
`.github/workflows/review-gate.yml` blob from `AI-Ascension/.github` commit
`9a92f68d06a6c7c2dbc9ab6723198bde457a1902` (canonical event-selection repair, #65).
Git blob: `e01bf4204e772e4dc0cf46c861c9241caaf0cabb`.
SHA-256: `5c00e20afb27104735b11a7870145602bd565bcbaf4a6c29a30d99704ac6b2f3`.

The `.github` wrapper now pins both `uses` and `gate-sha` to this reviewed
merged commit. No other repository's caller or policy is changed.
`confirmed` by `python -m unittest discover -s tests -p 'test_review_gate*.py' -v`:
the fixture's Git blob is checked, the caller references agree, and the same
modeled-context executable event cases run against both canonical source and
the pinned fixture. Automatic events cannot be overridden by manual or
callable inputs. Hosted manual dispatch remains `unverified`; these tests do
not dispatch a workflow or change GitHub settings.

## Historical callable-source repair (#64)

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

Historical scope: that repair restored the pull-request and review-event calls. The
then-pinned callee did not accept a `number` workflow-call input, so the wrapper's
existing manual dispatch did not forward its number and remained fail-closed.
That historical fixture is retained unchanged as evidence of the earlier
callability repair, not as evidence that dispatch was repaired.

## Canonical dispatch contract (#65, now adopted by the current pin)

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

The canonical repair (#65) deliberately left the historical consumer pin
unchanged. This separate adoption advances only `.github`'s caller to its
reviewed immutable merge commit and retains both source fixtures.
