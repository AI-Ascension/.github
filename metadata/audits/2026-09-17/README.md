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

After that merge landed (`4a1e6126`), the monitor was re-dispatched and reported **one** remaining
mismatch: `ascension-watchdog` advanced `9fc213dd…` → `de8e4216…` at 2026-09-18T00:13:46Z, thirteen
minutes after the refresh read it. The advance is a clean fast-forward (`ahead_by: 1`, `behind_by: 0`)
touching only `docs/evidence/single-deployment-soak-prerequisite-20260917.md`; the cited `README.md` blob
is byte-identical (`7a798913…`) at both commits, so the evidence pin was re-pointed honestly. That single
pin is refreshed here.

The same production run is the strongest available proof that the two substantive fixes work: across
16 repositories it reported **zero** `AI-Ascension/.github` mismatches (the self-pin defect is gone) and
**zero** `unmapped_repository` mismatches (the four new repositories are now recorded). The only signal
left was the genuine live advance above.

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

### A second manifestation of the same defect class

`metadata.py validate --snapshot` and `metadata.py plan --snapshot` additionally require every topic's
`evidence.commit` to equal the snapshot's current head. For `AI-Ascension/.github` that requirement has
the same self-referential shape as the removed `default_commit`: the registry is stored inside the
repository whose head it must name, so the evidence pins can only match at the commit that wrote them and
must mismatch at every later head. Observed directly after the merge:

```
metadata: error: AI-Ascension/.github topic 'ai-ascension' evidence commit
  'bbd2e7366f0b…' does not match audited source commit '4a1e6126…' for AI-Ascension/.github
```

This is the documented plan-binding behavior, not a new defect: a plan is bound to the exact bytes it was
reviewed against, so a later merge correctly invalidates a *live-snapshot* plan. It does not affect the
scheduled monitor — `tools/metadata_drift.py` never calls `_validate_evidence_against_snapshot`, and the
hosted `Metadata validation` job runs `validate` **without** a snapshot, exactly as the lane requires. The
evidence *content* is stable; only the commit pointer moves. The three cited files (`README.md`,
`CONTRIBUTING.md`, `GOVERNANCE.md`) have identical blobs (`6fff11a9…`, `c0068e71…`, `f1ea9c1f…`) at both
the pre- and post-merge heads. A cleaner model — cite the commit where evidence was observed rather than
requiring equality with the live head — is part of the same owner decision recorded above.

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
| AI-Ascension/ascension-watchdog | 1359537708 | `bootstrap` | `bc8ebf20…` | `de8e42164c87f19d4c997dc6ff5d357af3ffab14` |
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

- Plan digest: `fcc8b17650db65e8f4395f1c91771add5061ec9d3765f78c29395b599fec52d1`.
- Manifest revision: `sha256:f4634209781a3c6a875020b74f39b7994d73b94c094e58ad714cc990e72c76c0`.
- Migrations digest: `447f26e16729019c1552e4d2a403d6c605c4edddb9b4e9306c0b5f55b42c86cd`.
- Snapshot digest: `d5d2264030c6d878fb04a430c43617268755ef7d81018d8278e141979c8a7fa7`.

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

## Second managed-pin refresh — 2026-09-20

The six managed pins recorded above were re-observed against the live default branches at
`2026-09-20T21:21:07Z` and had all advanced:

| repository | recorded | observed |
| --- | --- | --- |
| `ascension-map-visualizer` | `3370db16…` | `c8e7c88c…` |
| `ascension-watchdog` | `de8e4216…` | `0e4bf177…` |
| `sts2-game-mod` | `9ebc779b…` | `d82cdc52…` |
| `sts2-gateway` | `2f7490d7…` | `2d7f758b…` |
| `sts2-harness` | `67de2007…` | `ba2fccdb…` |
| `sts2-mcp-server` | `65cb4056…` | `c468e761…` |

Each advance was checked to be a clean fast-forward (`behind_by: 0`) before any pin was re-pointed, and
every cited evidence path was compared at both commits by blob SHA rather than assumed. 42 of the 44
re-pointed evidence commits are byte-identical evidence: the cited `README.md`, `Cargo.toml`, Map prompt
and `AGENTS.md` blobs are unchanged at both commits. The one exception is `sts2-game-mod`'s `csharp` and
`dotnet` evidence,
`experiments/managed-rust-interop/gameplay-tests/RuntimeV3ValidationProbe.csproj`, which changed
`152e9262…` → `cd5152e8…` by one added
`<Compile Include="../game-loader/LaunchContractRefusal.cs" …>` item. Its cited lines 1 and 4 are above
that insertion, so the file still substantiates both topics.

`sts2-harness` advanced twice during this pass (`67de2007…` → `acd06d7e…` at 19:53Z → `ba2fccdb…` at
21:14Z); the table records the head observed at the freeze timestamp. This is the moving target described
above, not a new defect: the repository is under active concurrent development and a further merge re-reds
the scheduled report. The durable fix remains the owner decision recorded above, and this refresh does not
pre-empt it.

Local checks at the prepared head, run as CI runs them:

```
python3 tools/metadata_drift.py --metadata metadata/repositories.yml --labels labels.yml \
  --snapshot <public-only snapshot, no local exclusions>
  -> {"mismatches": [], "ok": true, "review_status": "reviewed"}                              exit 0

python3 tools/standards_adoption.py --ledger metadata/standards-adoption.json \
  --workspace-root .../consumers
  -> {"checked_consumers": 2, "findings": [], "ok": true}                                     exit 0

python3 tools/metadata.py validate --metadata metadata/repositories.yml --labels labels.yml
  -> {"labels_present": true, "ok": true, "repository_count": 16, "snapshot_present": false}   exit 0

bash tests/link-check-template.sh
  -> 15 PASS, 0 FAIL                                                                          exit 0

python3 -m unittest discover -s tests
  -> Ran 112 tests ... OK
```

The fleet plan was regenerated from the refreshed inputs rather than hand-edited. The regeneration is
deterministic — `make_plan` reproduces the pre-change plan from the pre-change inputs — and changes only
the target source pins and the four digest fields recorded above. The reviewed operation sequence
(11 topic replacements, 44 stable-ID renames, 22 migrations, 54 label creations, 109 writes) is unchanged.

Deliberately not refreshed: the two stale `managed: false` pins, `aiascension.tech` (`4e2d99c9…` →
`34aedf3c…`) and `ascension-workflow-studio` (`996a38ea…` → `28513217…`). The monitor skips unmanaged rows,
and each row's `management_reason` holds its identity and evidence unchanged pending the owner
applicability decision.

## Remaining gates

All eleven selected repositories remain blocked at owner authorization for the 2026-09-08 proposal.
Applied: none. Failed live operations: none attempted. This refresh changes recorded metadata only; it
performs no topic, label, or assignment write and authorizes none. Independent live post-apply readback,
same-plan second-apply write count, journals, and rollout completion remain unperformed. No clean live
desired state is claimed beyond the drift report's own scope: topics, labels, default branch, visibility
and archive state for the eleven selected repositories, plus identity coverage for every discovered
repository.
