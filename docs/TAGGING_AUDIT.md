# Tagging preparation audit

## Current preparation — 2026-09-08

The implementation PRs are merged. The [refreshed rollout review](../metadata/audits/2026-09-08/README.md) supersedes the dated preparation status below. Fresh source/metadata inspection selects 11 public targets, holds one historical target out after visibility drift, and records one additional private exclusion outside Git. No live metadata application is authorized or performed. The owner must select the canary and approve its exact fresh digest; publication and merge are separate from application.

## Historical preparation — 2026-09-07

The supplied tagging specification is reconciled into a candidate for 12 public repositories. Nothing has been published or applied. Independent technical review passed for the source map and corrected execution logic; external authorization is absent. Both regenerated plans pass the technical review gate, and the CLI still requires actual owner/operator authorization before any write.

The [topic reconciliation](../metadata/audits/2026-09-07/topic-reconciliation.md) records all complete before/after topic sets. The canonical map contains 89 evidence-backed topic entries pinned to default-branch commits. Every existing topic is retained. Planning repositories remain identified as planning. No repository description or role statement is rewritten.

The [fleet plan](../metadata/audits/2026-09-07/fleet-plan.md) contains 12 complete topic replacements, 36 stable-ID label renames, 18 additive migrations that retain existing sources, and 74 scoped label creations. The additive rows currently require no assignment writes. Two closed public issues carry renamed audience labels. No issue receives a new good-first-issue, first-task, triage, priority, or status assignment. Source-absent migrations are explicitly assessed in the migration manifest and generate no operations.

The [candidate canary](../metadata/audits/2026-09-07/canary-plan.md) targets only the organization's public `.github` repository. It is a suggested review scope, not a maintainer selection or approval. Machine-readable plans beside both Markdown files bind complete operations, input digests, source pins, and inverse descriptions. Any review-status change, refreshed input, or source commit change requires regeneration and approval of the resulting digest.

The [consumer audit](../metadata/audits/2026-09-07/consumer-activation.json) verifies that `bug` already exists in every target. Three targets have preexisting missing specialist-form defaults; every missing default is included in the candidate label creations. Provision and read back those definitions before claiming complete inherited-form readiness. The companion Pages change is prepared locally at `f74e2c15968c476f9bcf6669817830d58e789cce`; it changes two visible `defect` references to `bug`, preserves form URLs, and passed all five Pages tests. It has not been pushed.

The [public inventory summary](../metadata/audits/2026-09-07/public-inventory-summary.json) records identities, actual source pins, descriptions/homepages, source package declarations, tag/release observations, issue/PR counts, and observed permissions. Language breakdown and protection rules were not queried; absence is not inferred. The [open PR audit](../metadata/audits/2026-09-07/open-pr-collisions.json) inspected metadata and changed-file pages for all 27 public PRs open in the refreshed inventory. Five touch potential governance/workflow consumers, but none directly overlaps the prepared coordinator or Pages changes. Unmerged implementation is excluded from the topic evidence. Recheck PR state before publication.

No operation in this task changes repository names, Git tags, releases, runtime behavior, or protections. This describes this task's changes; it does not claim those fields could not change through another actor.

## Validation and limits

The Python suite passes 84 tests, including the actual prepared fleet plan exercised against a stateful fake API. That fixture produces 122 writes on first application, verifies final state, reports no simulated drift, makes zero writes on repeat apply and resume, and rolls back 48 owned changes without conflicts. Rollback retains 74 newly created definitions by policy. These counts are synthetic evidence, not GitHub results. A separate six-migration single-issue regression exercises combined additive destinations, definition changes, stable-ID renames, final verification, repeat/resume, replanning, and rollback, including two destinations created within the same plan. The independent review exposed a symbolic-ID rollback mismatch in that case; the added regression failed before the correction and passes after it. Three cited public files missing from the review cache were fetched at their pinned commits and blob-verified; all 89 citations now resolve to cached source. Existing tests cover later human edits, stale preconditions, partial failure, uncertain writes, journal forgery, and locks.

All six JSON schemas pass schema validation. The canonical map, label palette, and prepared fleet plan validate against their schemas. Canonical validation against the refreshed read-only inventory passes. The existing link-check regression passes all 15 cases. Hosted CI and native Windows execution have not run. The scripts use Python's standard library with PyYAML for non-JSON YAML; command handling has local transport tests and a successful read-only GitHub response-header parsing check.

The requested three descendant levels could not be executed: depth-1 agents lacked callable child-spawn tools. Three resumed lead spawns accepted the requested Luna/max parameters, but provider-side model attestation was unavailable. The execution lead later hit a provider usage limit; the root completed remaining code and local tests. See the [orchestration record](../metadata/audits/2026-09-07/orchestration.json). Earlier independent-review reports are historical. A subsequent attempt stopped before a verdict; the successful retry is recorded in the [final independent review](../metadata/audits/2026-09-07/final-independent-review.md).

## Remaining gates

1. Obtain owner authorization to publish the prepared coordinator and Pages branches as draft PRs; no publication is implied by technical review.
2. Have the maintainer select the canary and approve its exact repository ID, operations, assignment scope and plan digest. Refresh/replan if preconditions have changed.
3. Run and independently verify the authorized canary before any separately authorized wider rollout.
4. Capture actual journals and readback evidence locally. Private inventory, credentials, and authorization records must remain outside tracked publication artifacts.

Operator instructions are in [TAGGING.md](TAGGING.md); release policy is prospective and creates no Git tags or releases.
