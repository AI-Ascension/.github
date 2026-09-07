# Tagging preparation audit

The supplied tagging specification is reconciled into a candidate for 12 public repositories. Nothing has been published or applied. Independent review of the final source map and execution changes remains outstanding; external authorization is separately absent. The planner therefore marks both prepared plans inapplicable.

The [topic reconciliation](../metadata/audits/2026-09-07/topic-reconciliation.md) records all complete before/after topic sets. The canonical map contains 89 evidence-backed topic entries pinned to default-branch commits. Every existing topic is retained. Planning repositories remain identified as planning. No repository description or role statement is rewritten.

The [fleet plan](../metadata/audits/2026-09-07/fleet-plan.md) contains 12 complete topic replacements, 36 stable-ID label renames, 18 additive migrations that retain existing sources, and 74 scoped label creations. The additive rows currently require no assignment writes. Two closed public issues carry renamed audience labels. No issue receives a new good-first-issue, first-task, triage, priority, or status assignment. Source-absent migrations are explicitly assessed in the migration manifest and generate no operations.

The [candidate canary](../metadata/audits/2026-09-07/canary-plan.md) targets only the organization's public `.github` repository. It is a suggested review scope, not a maintainer selection or approval. Machine-readable plans beside both Markdown files bind complete operations, input digests, source pins, and inverse descriptions. Any review-status change, refreshed input, or source commit change requires regeneration and approval of the resulting digest.

The [consumer audit](../metadata/audits/2026-09-07/consumer-activation.json) verifies that `bug` already exists in every target. Three targets have preexisting missing specialist-form defaults; every missing default is included in the candidate label creations. Provision and read back those definitions before claiming complete inherited-form readiness. The companion Pages change is prepared locally at `f74e2c15968c476f9bcf6669817830d58e789cce`; it changes two visible `defect` references to `bug`, preserves form URLs, and passed all five Pages tests. It has not been pushed.

## Validation and limits

The Python suite passes 80 tests, including the actual prepared fleet plan exercised against a stateful fake API. That fixture produces 122 writes on first application, verifies final state, makes zero writes on repeat apply and resume, and rolls back 48 owned changes without conflicts. Rollback retains 74 newly created definitions by policy. These counts are synthetic evidence, not GitHub results. A separate six-migration single-issue regression exercises combined additive destinations, definition changes, stable-ID renames, final verification, repeat/resume, replanning, and rollback. Existing tests cover later human edits, stale preconditions, partial failure, uncertain writes, journal forgery, and locks.

All six JSON schemas pass schema validation. The canonical map, label palette, and prepared fleet plan validate against their schemas. Canonical validation against the refreshed read-only inventory passes. The existing link-check regression passes all 15 cases. Hosted CI and native Windows execution have not run. The scripts use Python's standard library with PyYAML for non-JSON YAML; command handling has local transport tests and a successful read-only GitHub response-header parsing check.

The requested three descendant levels could not be executed: depth-1 agents lacked callable child-spawn tools. Three resumed lead spawns accepted the requested Luna/max parameters, but provider-side model attestation was unavailable. The execution lead later hit a provider usage limit; the root completed remaining code and local tests. See the [orchestration record](../metadata/audits/2026-09-07/orchestration.json). Earlier independent-review reports are historical and do not certify these final changes.

## Remaining gates

1. Obtain independent source and execution review, including the final projection logic; resolve findings and update review state.
2. Regenerate plans from fresh read-only inventory and review exact scope and digests. Publish the prepared repository changes only with maintainer authorization.
3. Obtain explicit operator authorization for the selected repository IDs, operations, and plan digest; run and verify the authorized canary before any wider authorized rollout.
4. Capture actual journals and readback evidence locally. Private inventory, credentials, and authorization records must remain outside tracked publication artifacts.

Operator instructions are in [TAGGING.md](TAGGING.md); release policy is prospective and creates no Git tags or releases.
