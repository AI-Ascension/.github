# Tagging migration plan

## Current preparation — 2026-09-08

The implementation PRs are merged. The [refreshed rollout review](../metadata/audits/2026-09-08/README.md) supersedes the dated preparation status below. Fresh source/metadata inspection selects 11 public targets, holds one historical target out after visibility drift, and records one additional private exclusion outside Git. No live metadata application is authorized or performed. The owner must select the canary and approve its exact fresh digest; publication and merge are separate from application.

## Historical preparation — 2026-09-07

This document records the prepared label transition for the public seed inventory. It is a
reviewable proposal. The 2026-09-07 refresh performed read-only API calls; no label, issue, pull
request, topic, repository, or settings write was performed.

The canonical definitions are in [`labels.yml`](../labels.yml). The machine-readable migration
input is [`metadata/label-migrations.yml`](../metadata/label-migrations.yml). The latter records
the completed snapshot's stable repository and label IDs, before-state branch and commit, source
presence, collision strategy, observed assignment counts, and the explicit public-only scope.

## Scope and current state

The reviewed seed contains these 12 public repositories. IDs, default branches, and commits are
the values read in the completed refresh and are preconditions for a later plan:

| Repository | ID | Default branch | Default commit | Source labels |
| --- | ---: | --- | --- | --- |
| `.github` | 1354466045 | `main` | `d8fb867dede3ec1cde424d7f6f6f56e49dc21227` | all six |
| `AI-Ascension.github.io` | 1354473981 | `main` | `e81dd4e9ff2f8e5f8ffafc8b1a489d1e1cc7ef9f` | all six |
| `aiascension.tech` | 1209899690 | `codex/wire-mailing-list-email` | `4e2d99c95d89ce3d18981d331faad10c9f1f7376` | absent |
| `sts2-harness` | 1354378100 | `main` | `cb17b6c15262ce9356f1e85fd475af997aedc445` | all six |
| `sts2-mcp-server` | 1354378057 | `main` | `eb89ab251665f263c2fe3e6b735eeae3d3e40c83` | all six |
| `sts2-gateway` | 1354378018 | `main` | `33ea48f3b549f08e19db80d8c68c1438fa12a60a` | all six |
| `sts2-game-mod` | 1354377975 | `main` | `8b71150895ea95c0625afc1389bb08e4034d9350` | all six |
| `sts2-game-core` | 1354377929 | `main` | `87e0f3d9355c0827e989d9fbc31804440852519b` | all six |
| `sts2-protocol` | 1354378136 | `main` | `8874b0951289fd943c7e14dea36557fa24c401d1` | all six |
| `ascension-watchdog` | 1359537708 | `bootstrap` | `dc2d20badb9e86c12067316b92d6c8289b2e6995` | absent |
| `ascension-map-visualizer` | 1359701124 | `bootstrap` | `18915e5571829e582f460bf14b674cc2db39d9c5` | absent |
| `ai-agent-observability` | 1357224960 | `main` | `b25880376d3a3334c77f58637267db93581c4c77` | all six |

The six source names are `defect`, `docs`, `wedge:player`, `wedge:rust`, `wedge:mcp`, and
`wedge:security`. Nine repositories have all six shared source definitions. The three
default-only repositories have none of them; their absence is recorded as a no-op assessment, not
as permission to invent assignments. `bug` and `documentation` already exist alongside their
source names in the nine repositories. All four `audience:*` destination names are absent from
the refreshed live catalogs.

One newly discovered private repository is excluded from this proposal. Its name and contents are
not included here. Applicability remains pending an explicit owner decision.

## Operations and blast radius

The input contains 54 applicable rows:

| Source to destination | Rows | Strategy | Live condition | Assignment behavior |
| --- | ---: | --- | --- | --- |
| `defect` → `bug` | 9 | additive | Both names exist | Copy source assignments only when the reviewed plan runs; retain source, destination, and every unrelated label. |
| `docs` → `documentation` | 9 | additive | Both names exist | Copy source assignments only when the reviewed plan runs; retain source, destination, and every unrelated label. |
| `wedge:player` → `audience:player` | 9 | stable-ID rename | Destination absent | Rename the source definition in place and retain its stable ID and assignments. |
| `wedge:rust` → `audience:rust` | 9 | stable-ID rename | Destination absent | Rename the source definition in place and retain its stable ID and assignments. |
| `wedge:mcp` → `audience:mcp` | 9 | stable-ID rename | Destination absent | Rename the source definition in place and retain its stable ID and assignments. |
| `wedge:security` → `audience:security` | 9 | stable-ID rename | Destination absent | Rename the source definition in place and retain its stable ID and assignments. |

The 18 source-absent pair assessments cover the three default-only repositories. They do not
create a migration operation. The two additive pairs have 18 collision rows; the four audience
pairs have 36 stable-ID rename rows. The refreshed issue and pull-request inventory contained two
source assignments: the closed Pages issues #1 (`wedge:rust`) and #2 (`wedge:mcp`). No open source
assignment was observed. No `defect` or `docs` assignment was observed. A later plan must reread
all relevant issues and pull requests immediately before each write, because these counts are
observations rather than durable promises about future edits.

The existing project labels `first-task`, `proof-recipe`, `contract-observation`, `evidence`,
`unverified-claim`, and `security` retain their meanings. The legacy source definitions remain in
the canonical catalog for the transition and rollback record; a stable-ID rename wave does not
recreate a retired source on a repository where it was renamed. No label is deleted by this plan.

The catalog also defines the shared work-kind labels `bug`, `enhancement`, `documentation`,
`research`, `maintenance`, and `question`; the standard `good first issue` and `help wanted`
labels; and optional priority, status, and area overlays. Definitions alone do not assign those
labels. Priority and status overlays have no repository applicability in this proposal because no
maintainer triage decision or project-field reconciliation was recorded. Area overlays carry
explicit stable repository ID lists for their documented cross-cutting use; no area is applied to
every repository by default.

## First-task review

The only observed `first-task` assignments were Pages issues #1 and #2. Both are closed. Their
bodies provide bounded goals, acceptance criteria, pinned source revisions, commands,
prerequisites, and explicit no-game/no-model/no-credential constraints. Because they are closed,
the read-only decision is to leave `good first issue` unassigned. No `help wanted`, priority,
status, or area label is assigned by this proposal. A maintainer may make a separate decision for
a future open issue after reviewing its scope and support requirements.

## Consumer audit and transition

The pinned public source audit found these actual renamed-label consumers:

| Consumer | Observed reference | Prepared action | Activation state |
| --- | --- | --- | --- |
| `.github/ISSUE_TEMPLATE/defect.yml` | Form default `defect`, plus the `Defect` title/name | Default changed to `bug`; retain the filename for existing template URLs. | Safe after the coordination repository change because `bug` is present in every public seed repository. |
| `.github/CONTRIBUTING.md` | First-task text used `wedge:*` and `docs` | Refer to post-provisioning `audience:*` and `documentation`, while explaining the transition. | Documentation only; audience names remain inactive until provisioned. |
| `AI-Ascension.github.io/contributing.html` | The site displays “defect” and links to `template=defect.yml` | Prepared companion commit `f74e2c15968c476f9bcf6669817830d58e789cce` says “bug” while preserving the stable `defect.yml` URL. | Isolated Pages worktree prepared; `node --test tests/*.test.cjs` passed 5 tests. No push or PR. |

No exact old-label assignment was found in the pinned public workflow, Dependabot, labeler, or
pull-request-template sources. Mentions of `docs` as a source path and ordinary prose are not
label consumers. The prepared site companion is a user-facing terminology consumer. Its publication
and acceptance remain separate gates before the live surfaces are synchronized.

The changed `bug` default is present in all 12 public repositories. The three
default-only repositories already lack four other inherited form labels
(`first-task`, `proof-recipe`, `contract-observation`, `evidence`). The provisioning
plan repairs these pre-existing gaps; verify all referenced labels before claiming
complete inherited-form readiness. See the dated `consumer-activation.json` audit.

The transition order is:

1. Merge the canonical definitions, migration input, documentation, and the `bug` form update
   through the normal review path.
2. Have a maintainer review the complete plan, stable IDs, collision decisions, issue assignment
   counts, and the companion site diff. The plan must bind the exact refreshed snapshot and an
   explicit authorization record to its digest.
3. Select one low-risk canary by stable repository ID. Reread identity, default branch and commit,
   topics, all labels, and assignment pages. Apply only after the plan and authorization pass
   preflight, then read back each postcondition.
4. Apply the approved additive and stable-ID operations to the remaining public repositories in
   controlled waves. Preserve unmanaged labels and all manual edits. On drift, stop that operation
   and replan.
5. Activate any audience-specific site, filter, workflow, or template consumer only after its
   destination label is present and verified in its destination repository. The current shared
   forms have no audience default.
6. Run a second application against the verified state and require zero writes. Record partial
   failures, capability errors, and readback receipts per repository; organization-wide atomicity
   is not claimed.

No apply, canary, readback, second-run, or rollback has occurred. Administrative capability is not
authorization. The remaining gate is an explicit owner authorization for the reviewed plan and its
selected public repository IDs.

## Rollback boundaries

Rollback compares the current state with the plan's postconditions before changing anything. An
additive rollback removes only destination assignments introduced by this migration, preserves
pre-existing destination assignments and unrelated labels, and retains both definitions. A rename
rollback restores the old name only when the same stable label ID still has the recorded
postcondition and no later maintainer edit conflicts. Later edits, new uses, or uncertain writes
become manual-review conflicts. No destination label is deleted automatically.
