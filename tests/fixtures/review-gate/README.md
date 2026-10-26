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
