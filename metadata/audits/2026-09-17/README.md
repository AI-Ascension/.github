# Refreshed metadata review — 2026-09-17

Prepared for owner review. No live topic, label, or assignment write has been performed. Publication of
this preparation change does not authorize application. The 2026-09-07 and 2026-09-08 reviews remain
unchanged as historical evidence and must not be executed.

This refresh resolves the scheduled `Metadata drift (read only)` report, which was red on `main`
`bbd2e7366f0b6fa2158eced219bcb9eab5db9162` (run
[35233563386](https://github.com/AI-Ascension/.github/actions/runs/35233563386), job `105243604557`,
2026-09-17T14:26Z). That red state is tracked by [`.github#38`](https://github.com/AI-Ascension/.github/issues/38).

The recorded pins were re-verified against the live default branches immediately before publication on
2026-09-18; six managed heads had advanced again since the first pass (see
[Source pins refreshed](#source-pins-refreshed)).

## The source pin is a moving target

`source_pin` is a strict-equality check between the recorded commit and the live default-branch head. This
organization is under continuous concurrent development, so heads advance every few hours: during this
single refresh pass `sts2-harness`, `sts2-gateway`, `sts2-game-mod`, `ai-agent-observability`,
`ascension-watchdog` and `AI-Ascension.github.io` all moved, and the recorded pins were refreshed a second
time for that reason. The weekly schedule (`23 9 * * 1`) therefore reports drift on essentially every run,
by construction, even when nothing is wrong with the registry.

Refreshing pins restores a truthful green **at the reviewed commit**, which is what this change does. It
does **not** make the monitor durable: any later merge into one of these ten repositories re-reds it. A
durable fix is an owner decision, because the two candidate semantics disagree:

- keep strict equality and treat the registry pin as a snapshot that a human re-reviews periodically
  (the current design; drift is then expected and informational between reviews), or
- treat the pin as a reviewed baseline and report drift only when the head is not a descendant of it
  (fast-forward advance expected; force-push, rewrite, or branch reset is the real signal).

The second option requires a change to `tools/metadata_drift.py`, which this lane is explicitly not
authorized to make to turn the check green. The decision and its rationale are recorded here for the owner
rather than being pre-empted.

## What actually drifted

The live organization was re-read read-only on 2026-09-17. Topics and shared labels were **already
reconciled** with the canonical map: all eleven selected repositories carry the complete desired topic
sets, and all 54 new or renamed destinations (`audience:*`, `research`, `maintenance`, `area:*`, `bug`,
`documentation`) exist live. The 15 reported mismatches were registry staleness, not remote state:

- **11 stale `source_pin` entries.** The recorded default-branch commits were the 2026-09-08 heads.
  Ten managed repositories advanced since; each new pin was re-read from the live default branch.
- **4 `unmapped_repository` entries.** `ascension-brand-overhaul`, `ascension-workflow`,
  `ascension-context-console` and `ascension-workflow-studio` were created after the 2026-09-08 refresh
  and had no recorded applicability.

No live write was performed by this refresh, and none is claimed.

## The self-reference defect (root cause of a permanently red job)

`metadata/repositories.yml` is stored **inside** `AI-Ascension/.github`. The `.github` row previously
asserted `"default_commit": "bbd2e736…"`. A file at commit C cannot contain C as its own value, because C
is the hash of the tree holding that value. Measured directly:

```
simulated landing commit (would be main head after merge): 064511164e27d88097efce244d373799b266944a
.github pin inside that commit                           : bbd2e7366f0b6fa2158eced219bcb9eab5db9162
=> pin == head ? False
```

On a CI-shaped snapshot (public-only, no local exclusions) the consequence is exact:

```
registry with the .github self-pin, post-merge head -> ok False, 1 mismatch: source_pin AI-Ascension/.github
registry without the self-pin,      post-merge head -> ok True,  mismatches []
```

So no merge could ever leave that row green; the monitor was guaranteed red forever. The row now carries
`self_reference_note` instead of `default_commit`. This is **not** a weakened check: the drift monitor
still evaluates this repository's topics, labels, default branch, visibility and archive state.

```
registry without the self-pin, .github topics changed -> ok False, 1 mismatch: topics AI-Ascension/.github
```

The write path is unaffected. Plan preconditions bind the commit read from the snapshot, not the registry
row, so apply-time drift detection for `.github` is unchanged: the 2026-09-17 plan records
`default_commit: bbd2e736…` on that target and in its `replace_topics` precondition.

Two related states stay distinct and honest:

- `metadata.py validate --snapshot` and `metadata.py plan --snapshot` cross-check each topic's
  `evidence.commit` against the audited source commit. Because the `.github` evidence pins are themselves
  refreshed to the observed head, a later merge still invalidates a *live-snapshot* plan for `.github`.
  That is correct: a plan is bound to the exact bytes it was reviewed against. The scheduled drift
  **report** does not perform that cross-check and is green.
- Nothing here authorizes execution. `authorization_state` remains `not-recorded`.

## Source pins refreshed

All eleven were re-verified against the live default branch on 2026-09-17.

| Public target | Stable ID | Branch | Previous pin | Refreshed pin |
| --- | ---: | --- | --- | --- |
| AI-Ascension/.github | 1354466045 | `main` | `049f5018…` | `bbd2e736…` (self-reference; see above) |
| AI-Ascension/AI-Ascension.github.io | 1354473981 | `main` | `1065799d…` | `42ad0609e648aaf5d0ee59039c458cd724fd2731` |
| AI-Ascension/ai-agent-observability | 1357224960 | `main` | `28a48590…` | `3d147ae1fd3e55f96748b7c1a0e6b729ff95e60c` |
| AI-Ascension/ascension-map-visualizer | 1359701124 | `bootstrap` | `9aded886…` | `3370db162be8a0618da1c846327be3facf86dd2b` |
| AI-Ascension/ascension-watchdog | 1359537708 | `bootstrap` | `bc8ebf20…` | `9fc213dde7d46b152c64b4c7751d6eff4e034091` |
| AI-Ascension/sts2-game-core | 1354377929 | `main` | `87e0f3d9…` | `4b51ec24297a39c8626a666001b5eb2fcbdccaec` |
| AI-Ascension/sts2-game-mod | 1354377975 | `main` | `e162e249…` | `9ebc779bf6ac0997f57dff63f01fab8b17b7a274` |
| AI-Ascension/sts2-gateway | 1354378018 | `main` | `53745dd2…` | `2f7490d72e262378d5a55c920b6ca6355e21ef68` |
| AI-Ascension/sts2-harness | 1354378100 | `main` | `e5bb677b…` | `67de2007b35bea4bb4e9f2bb65b1eaeadc90a2b5` |
| AI-Ascension/sts2-mcp-server | 1354378057 | `main` | `655e0c72…` | `65cb405616ecddfb7bf7b76edf341be30a442ca2` |
| AI-Ascension/sts2-protocol | 1354378136 | `main` | `6d7fb859…` | `bfe28e455de48d6d9db466bbcf6062ab5d85e9af` |

Every `evidence.commit` on those rows was re-pointed to the same verified commit, and the evidence path
was confirmed present in the audited tree. `metadata.py plan` reports `review.evidence = {"checked": 83,
"ok": true, "unavailable": []}`.

Re-pointing evidence was not a blanket rewrite. For each advanced repository the whole `previous...new`
commit range was inspected, and the change set was checked against every cited evidence path. No cited
evidence file was modified in any of those ranges (`ai-agent-observability` 3 files changed,
`AI-Ascension.github.io` 2, `ascension-watchdog` 6, `sts2-game-mod` 57, `sts2-gateway` 7, `sts2-harness`
39; none of them a cited evidence path), so each topic's cited source is byte-identical at the new pin and
the re-point is honest rather than assumed.

## Applicability decision for the four new repositories

`ascension-brand-overhaul` (1359787764), `ascension-workflow` (1363224464),
`ascension-context-console` (1363303312) and `ascension-workflow-studio` (1364045713) are now recorded in
the canonical map with `managed: false`, so they are visible and identified but **cannot be selected for
any live write**. Each carries `applicability_reason` and `management_reason` stating that an owner
applicability decision is required.

This is a recording decision, not an applicability decision: it stops the monitor from reporting an
unexplained unmapped repository while leaving the real question — which standards apply to each — to the
owner. Each row's single `ai-ascension` topic is `source-derived` evidence that was re-read from that
repository's `README.md` at the pinned commit (line 7 for `ascension-brand-overhaul`, line 1 for the
others). No live topic write is proposed for these rows.

Two **private** repositories discovered by the same refresh, `st2-project-planning` (1360058142) and
`obs-vm-setup` (1367380548), are deliberately **not** in this publication. They are recorded as
`excluded-pending-owner` in the ignored `metadata/snapshots/applicability-exclusions.json` and supplied to
`metadata.py snapshot --exclusions`. Private identities and raw snapshots stay outside Git.

## Complete proposal

See [complete topic sets and operation diff](fleet-plan.md) and [machine-readable fleet plan](fleet-plan.json).

- Plan digest: `a09fb7136abd14f100f460dfdf2ba0f6f3e923cf3dc54882a3c204a2ad45eb0b`.
- Manifest revision: `sha256:e045e941ffbd246bb15ad9ab4a3a47627d5fbea0392909f3d5baafd36c91453f`.
- Migrations digest: `447f26e16729019c1552e4d2a403d6c605c4edddb9b4e9306c0b5f55b42c86cd`.
- Snapshot digest: `95e984c604e28832680c9b5e988c055f0e78f848bef1b55d84a98b536c865a4b`.

The proposal is the reviewed 2026-09-08 operation sequence regenerated against the refreshed registry:
11 complete topic replacements, 44 stable-ID `wedge:*` → `audience:*` renames, 22 additive `defect` →
`bug` / `docs` → `documentation` migrations, and 54 scoped label creations, across the same 11 selected
repositories (10, 11, 14 and 16 operations per target; 109 definition/rename/topic writes in total).
No operation was added, removed or reordered. All additive rows still carry zero observed assignments.

`metadata/label-migrations.yml` is unchanged and still records `observed_at: 2026-09-08`. It is the reviewed
transition input, not a live-state assertion, and its 66 rows describe labels that the live organization
has already reconciled. Refreshing its observation date would rewrite a reviewed input without adding
information; the fresh live observation is recorded here instead. Its `review_status` remains `proposed`.

## Validation

Executed in the `fix/metadata-drift-refresh-20260917` worktree at the prepared head:

```
python3 tools/metadata.py validate --metadata metadata/repositories.yml --labels labels.yml \
  --snapshot /tmp/live-metadata-0918.json
  -> {"labels_present": true, "ok": true, "repository_count": 16, "snapshot_present": true}   exit 0

python3 tools/metadata_drift.py --metadata metadata/repositories.yml --labels labels.yml \
  --snapshot /tmp/live-metadata-0918.json
  -> {"mismatches": [], "ok": true, "review_status": "reviewed"}                              exit 0

# CI shape: public-only snapshot, no local exclusions
python3 tools/metadata_drift.py --metadata metadata/repositories.yml --labels labels.yml \
  --snapshot /tmp/ci-shaped-0918.json
  -> {"mismatches": [], "ok": true, "review_status": "reviewed"}                              exit 0

python3 tools/standards_adoption.py --ledger metadata/standards-adoption.json \
  --workspace-root .../consumers
  -> {"checked_consumers": 2, "findings": [], "ok": true}                                     exit 0

STANDARDS_CONSUMER_ROOT=.../consumers python3 -m unittest discover -s tests -p 'test_*.py' -v
  -> Ran 111 tests ... OK

bash tests/link-check-template.sh
  -> PASS file-anchor / external-and-mail / external-failure                                    exit 0
```

The four `test_standards_adoption` errors that appear without `STANDARDS_CONSUMER_ROOT` are environmental
(the consumer checkouts are absent locally) and are identical before and after this change; the hosted
`Metadata validation` job supplies that root. The full suite is otherwise byte-identical to the baseline.

## Remaining gates

All eleven selected repositories remain blocked at owner authorization for the 2026-09-08 proposal.
Applied: none. Failed live operations: none attempted. This refresh changes recorded metadata only; it
performs no topic, label, or assignment write and authorizes none. Independent live post-apply readback,
same-plan second-apply write count, journals, and rollout completion remain unperformed. No clean live
desired state is claimed beyond the drift report's own scope: topics, labels, default branch, visibility
and archive state for the eleven selected repositories, plus identity coverage for every discovered
repository.
