# Refreshed metadata rollout review — 2026-09-08

Prepared for owner review. No live topic, label, or assignment write has been performed. Publication of this preparation PR does not authorize application. Historical plans remain unchanged as evidence and must not be executed.

## Source and inventory

Both implementation PRs are merged: `.github` #11 at `049f5018ba09328bf2c7deb12ca3130d881e4022` and Pages #13 at `1065799de6eea8427ac5ae96e3b9238932ea761f`. These were also their default-branch heads at refresh. Current public source pins are listed below. Ten public pins advanced; one stayed unchanged. The source comparison and blob-verified topic receipts support retaining all selected desired topic meanings. No existing topic is removed. Watchdog and map visualizer retain `project-planning` and planned subjects.

The existing snapshot command inventoried all 13 accessible repositories and paginated all open/closed issues and pull requests. All 12 historical registry IDs were reconciled. Eleven remain public and managed. One historical target changed visibility and is explicitly `managed: false`, with old identity and evidence preserved unchanged; fresh private content is excluded. One additional private discovery retains a local stable-ID exclusion pending owner applicability. Private snapshots and exclusion records stay outside Git. No repository was silently dropped.

| Public target | Stable ID | Default branch | Source commit |
| --- | ---: | --- | --- |
| AI-Ascension/.github | 1354466045 | `main` | `049f5018ba09328bf2c7deb12ca3130d881e4022` |
| AI-Ascension/ai-agent-observability | 1357224960 | `main` | `28a48590afb75b07590e1b78ea47dae08f5c3ade` |
| AI-Ascension/AI-Ascension.github.io | 1354473981 | `main` | `1065799de6eea8427ac5ae96e3b9238932ea761f` |
| AI-Ascension/ascension-map-visualizer | 1359701124 | `bootstrap` | `9aded88629436497d22b9e6bb7590d0ec8ae5815` |
| AI-Ascension/ascension-watchdog | 1359537708 | `bootstrap` | `bc8ebf2054d2e3d2d74c1c7e5f775ae01952215d` |
| AI-Ascension/sts2-game-core | 1354377929 | `main` | `87e0f3d9355c0827e989d9fbc31804440852519b` |
| AI-Ascension/sts2-game-mod | 1354377975 | `main` | `e162e2490c189672bf168967f06fbf89b88d4010` |
| AI-Ascension/sts2-gateway | 1354378018 | `main` | `53745dd2a335cdca0d0f8ce9772faef0c2e725c2` |
| AI-Ascension/sts2-harness | 1354378100 | `main` | `e5bb677b05b36dd88cc76a5d5b5633be36085838` |
| AI-Ascension/sts2-mcp-server | 1354378057 | `main` | `655e0c728206c5b6e271d8bf7ed2e4681fa16dd3` |
| AI-Ascension/sts2-protocol | 1354378136 | `main` | `6d7fb8591d3d4a4be5a7e4cfb055e81c86a2fc6d` |

## Complete proposal

See [complete topic sets and operation diff](fleet-plan.md), [machine-readable fleet plan](fleet-plan.json), [all label definitions and applicability](label-definitions.md), and [source receipts](topic-source-receipts.json). The canonical migration input records each source/destination label ID, collision decision and open/closed assignment count. Unmanaged labels and repository extensions are preserved.

The public fleet has 11 complete topic replacements, 44 stable-ID `wedge:*` → `audience:*` renames, 22 additive `defect` → `bug` / `docs` → `documentation` migrations, and 54 scoped label creations. All additive rows currently have zero assignments and cause zero assignment writes. Stable renames preserve the two affected closed Pages issue assignments (#1 rust, #2 MCP). No open assignment is affected. No good-first-issue, help-wanted, priority, status, or area assignment is proposed.

Two public planning repositories now have the six legacy source definitions, added by another actor since the historical snapshot. Their 12 new migration rows use the freshly observed stable IDs. Audience destinations remain absent, so in-place rename avoids creating a competing identity. Existing bug/documentation collisions remain additive; their source definitions are retained. The palette and descriptions remain unchanged; only transition applicability expands to these two selected public targets.

The independently fetched [published contribution page](https://ai-ascension.github.io/contributing.html) is byte-identical to merged Pages source. Its eleven form links resolve to the four shared form filenames. All shared-form destination labels now exist in all eleven selected public catalogs. Audience labels remain inactive until provisioned. See [consumer evidence](consumer-activation.json).

## Proposed canary and exact authorization scope

The coordination repository has only read-only metadata validation/drift workflows; neither uses an issue/label or repository-topic event to start a release or deployment. The owner must explicitly select `AI-Ascension/.github` (stable ID `1354466045`). This is a proposal, not a selection or approval. See [complete canary diff](canary-plan.md) and [canary plan JSON](canary-plan.json).

- Canary digest: `d490e7a12083ee433ae353a5f9e0cfe637ec601144cdd39fdf8d2903ba46f7e8`.
- Manifest revision: `sha256:4f5342c6bc5654d2cb29eb6f09eca6b8658a5c18256ba6f279827802e6946e17`.
- Fleet digest (not authorized by canary approval): `fc1af35c37bdd49089d865485730b144b466e8ab471d00792c55e7e88a6a1896`.
- Proposed authenticated operator: `CompleteDotTech`; fresh GitHub readback reports repository admin, maintain, push, triage and pull capabilities on `.github`. The plan requires Administration write for topics and Issues write for labels. No credentials were printed or privileges expanded; actual write capability remains subject to CLI preflight.
- Canary operations: replace topics with `ai-ascension`, `community-health`, `contributing`, `github-organization`, `governance`; rename four audience labels in place; create `research`, `maintenance`, `area:metadata`, `area:ci`; retain both additive source/destination pairs with zero assignment additions.
- Expected canary writes: nine (one topics request, four renames, four definitions). Affected issue/PR assignments: zero. Authorization operations: `topics`, `labels`; no rollback permission is assumed.
- Approval reference: absent. No authorization record or execution journal has been manufactured. Existing publication instructions do not authorize this digest.

A later merge of this preparation PR changes the `.github` default commit and therefore invalidates this execution plan. Re-read source and live state, regenerate, independently check changed evidence, and obtain approval for the resulting fresh digest. Never substitute a PR head for the actual default-branch pin or bypass preflight.

## Validation and remaining execution gates

Independent source/consumer and plan review reports are adjacent to this file. Python, link and schema results are recorded in validation.json. Synthetic fixture execution is regression evidence only; no fake API result is live GitHub proof.

All eleven selected repositories are blocked at owner authorization; the two private repositories are held out from application. Applied: none. Failed live operations: none attempted. Independent live post-apply readback, same-plan second-apply write count, journals, and rollout completion remain unperformed. The [fresh read-only drift report](final-readonly-drift.json) records 11 topic differences and 98 managed-label differences (44 missing rename destinations and 54 missing new definitions). Comparing the two full snapshots found zero changes to selected source commits, topics, label definitions or labelled issue/PR populations during preparation; see [the comparison](preparation-drift-check.json). No clean live desired state is claimed.

After actual canary approval: use the existing CLI, approved digest/operator and durable journal; require full preflight, immediate readback, repository locks and bounded rate-limit handling. Independently verify full topic sets, stable IDs, definitions and every affected assignment, then apply the same plan/journal again and require zero writes. For uncertain writes reconcile through journal/resume without blind retries. Any observed drift stops execution and requires replan. Wider execution needs separately recorded authorization and bounded waves; no fleet authority follows from canary approval.

## Rollback limits

No label deletion is proposed. Rollback requires separate explicit permission, retains newly created definitions, removes only owned additive assignments, and restores a rename only if the same stable ID and recorded postcondition still match. Pre-existing assignments and later human edits survive; conflicts and uncertain ownership require manual review. Cross-request atomicity is not available. No repository names, descriptions, protections, credentials, tags, releases, dependency pins, deployments or runtime behavior are changed.
