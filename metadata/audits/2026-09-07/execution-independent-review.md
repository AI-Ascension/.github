# Independent review of metadata execution

Observed 2026-09-07 against the latest files available at review time. The reviewed executor
was `tools/metadata_execution.py`, SHA-256
`694cf83b7f7fe92ff11614a1ccb06c3323b318c9fd402e96c223947d0fac5055`.
The reviewed focused test file was `tests/test_metadata_execution.py`, SHA-256
`bfdc8ef386a65fb08acf97ef3086c39cb7a4424b435d3f5433843e5f343ee827`.
The reviewer edited neither implementation nor test files.

## Validation run

`python3 -m unittest -v tests/test_metadata_execution.py` passed all 20 focused tests.
The tests cover dry-run behavior, full topic replacement, preflight drift, pagination,
uncertain apply, ordinary additive assignment, label-definition guards, journal digest and
effect tampering, and preservation of unmanaged labels.

`python3 -m unittest discover -s tests -v` ran 41 tests and had two failures in
`tests/test_metadata_integration.py`:

* `test_planned_additive_effect_verifies_and_reapplies_without_writes` reports
  `source_assignment_remains` after the executor intentionally preserves the source label.
* `test_planned_rename_with_definition_change_verifies` accepts a later human description edit
  because rename verification checks the label ID but not the resulting color/description.

The focused suite does not exercise the adversarial cases below.

## Findings

### Blocker: a valid forged intent can authorize rollback

`Journal` opens an ordinary appendable path, takes a process-local `flock`, and checks only the
top-level plan digest (`tools/metadata_execution.py:47-80`). It records no owner, operator,
authorization ID, authenticated signature, event chain, or protected file mode. Rollback treats
every event whose phase is `intent` as an owned effect (`tools/metadata_execution.py:412-434`).
`validate_effect` now rejects an altered effect, but it proves only that the event has the exact
shape of a plan effect; it does not prove that this writer created the event or that the write
was accepted by the server.

An adversarial probe generated an exact, plan-shaped issue intent without running apply, then
simulated a human adding the destination label. `rollback(..., execute=True)` returned one write
and issued:

```text
forged_valid_intent 1 [('DELETE', '/issues/1/labels/documentation', None)] [1, 3]
```

The final label IDs lost the independently added destination. The existing tampering test only
changes a value in a real journal and therefore does not cover a valid forged event. A rollback
record needs an owner/authentication boundary and a state machine that distinguishes a verified
write from an unverified intent. An uncertain or absent apply must remain a manual-review
conflict when the live state happens to equal the desired state.

The journal lock also applies only to the selected path. Two valid plans with different journal
paths can still write the same repository concurrently. A repository-scoped lock or server-side
conditional mutation is needed for the conflicting target.

### High: a concurrent topic edit after the last read is overwritten

`effect` reads the current state, appends intent, and then calls `mutate` without an ETag or
conditional precondition (`tools/metadata_execution.py:181-214`). Topic mutation is a complete
set `PUT` (`:154-157`). A probe injected a `human` topic after the effect's topic read and before
the `PUT`; the executor reported success and replaced the human edit:

```text
topic_race {'plan_digest': '...', 'execute': True, 'applied': ['topics:7'], 'writes': 1}
writes [('PUT', '/topics', {'names': ['ai-ascension', 'rust']})]
final_topics ['ai-ascension', 'rust']
```

The focused race test (`tests/test_metadata_execution.py:277-284`) injects drift during the
second identity read, before the effect's final topic read. It does not cover the actual
read-to-write window. The same TOCTOU applies to label-definition PATCH and rollback topic PUT.
The writer needs an API-supported conditional write or a server-side compare-and-swap contract;
a postcondition read alone can report success after it has already discarded the concurrent edit.

### High: pre-existing additive assignments can disappear without a conflict

For an assignment whose destination was present in the reviewed `before` labels, the generator
skips the effect as unowned (`tools/metadata_execution.py:267-272`). `preflight_additive` does
not read those skipped issue rows (`:313-334`). If a maintainer removes that pre-existing
destination before apply, execution returns zero writes and zero conflicts while the reviewed
destination is absent:

```text
preexisting_assignment_drift {'plan_digest': '...', 'execute': True,
 'applied': [], 'writes': 0} [] [1, 3]
```

This preserves ownership during the normal case, but it silently treats a changed unowned row as
converged. Re-read every pre-existing assignment and return a manual-review conflict when it no
longer matches the reviewed state. Rollback must continue to skip rows the plan did not own.

### High: the verifier contradicts additive source preservation and misses rename definition drift

The executor deliberately adds a destination with `POST` while retaining the source and all
other labels (`tools/metadata_execution.py:171-177`; the focused preservation test is at
`tests/test_metadata_execution.py:185-192`). `tools/metadata.py:1039-1045` instead reports
`source_assignment_remains` as a verification mismatch for every such assignment. The current
integration test failure reproduces this contradiction. Verification must assert the intended
additive invariant, including destination presence and source preservation.

For a rename, `tools/metadata.py:1023-1026` checks only that the destination name resolves to
the reviewed label ID. It omits the reviewed `after` color and description. The integration test
changes the description after apply and verification still returns `ok: true`. Rename
verification must compare the complete reviewed label definition, while retaining its stable ID
and assignments.

### Medium: interrupted or malformed journal data cannot be resumed safely

Journal records are written as a plain JSON line followed by flush/fsync
(`tools/metadata_execution.py:69-74`). A process interruption during the append can leave a
partial final line. Opening the journal then rejects the whole file, including `--resume`, with
`journal unavailable or invalid`; a probe produced:

```text
truncated_journal ExecutionError journal unavailable or invalid: Expecting ',' delimiter: ...
```

There is no record framing, tail recovery/quarantine, or explicit operator repair path. A
malformed effect also escapes rollback handling: an `intent` event with an empty effect raised
`KeyError 'key'` while the error handler itself tried to report the conflict. Rollback should
validate event schema before indexing fields and return a durable manual-review outcome. The
append format needs a recoverable integrity marker or an atomic record strategy.

### Medium: rollback network uncertainty escapes instead of becoming a conflict

`effect` logs `rollback-uncertain` and re-raises all exceptions from a mutation
(`tools/metadata_execution.py:202-209`). `rollback` catches only `ExecutionError` and `KeyError`
(`:412-434`). A timeout after the server accepted a rollback PUT therefore escapes the method:

```text
rollback_timeout TimeoutError connection lost after server accepted write
```

The live fake state was already restored, but the caller receives no conflict or reconciliable
result, and later rollback effects are not processed. Real `gh` failures use the surrounding
`APIError` type, which is caught by the outer CLI, but the executor still loses the per-effect
conflict result and resume guidance. Return an explicit uncertain conflict, preserve the journal
state, and require readback before any retry.

### Medium: endpoint and path inputs are not constrained by the executor

`api` quotes repository components but accepts arbitrary repository strings and appends raw
suffixes (`tools/metadata_execution.py:88-90`). Issue numbers are interpolated without numeric
validation or URL quoting (`:142-143`, `:171-177`). A direct probe produced these endpoints:

```text
repos/AI-Ascension/example/../../orgs/attacker/issues/1/labels
repos/AI-Ascension/example/issues/1/labels
```

The first demonstrates that `..` remains a path component; the second came from an issue number
of `1/labels`. The normal planner validates owner/name syntax and obtains issue numbers from a
snapshot, but `MetadataWriter.validate_plan` currently verifies only the self-consistent digest
(`:336-339`). An externally supplied, self-digested plan can therefore reach the executor
without structural endpoint validation. Enforce exactly one owner/name pair, integer issue
numbers, permitted operation schemas, and an explicit endpoint map before invoking the generic
client seam.

### Medium: authorization and review status live outside the executor contract

The command wrapper now checks the review flag, approval record, operator identity, and
authorization before constructing the executor (`tools/metadata.py:956-988`, `:1156-1167`).
The imported `MetadataWriter` itself accepts a plan and `execute=True` without those checks; its
module doc explicitly says it has no authorization (`tools/metadata_execution.py:1`). Keep this
class private to the guarded CLI or move a mandatory authorization/plan-review boundary into the
execution API. Tests should exercise the actual CLI path as well as the low-level fake client so
future callers cannot accidentally bypass the guard.

## Positive controls observed

The latest executor has useful controls: it validates the plan digest, rejects altered journal
effects on rollback, takes an exclusive lock for a shared journal path, re-reads identity and
metadata before each effect, performs whole-plan preflight before the first write, records an
intent before mutation, verifies postconditions, handles uncertain apply through explicit
resume, and uses additive issue-label POSTs that preserve source and unmanaged labels in the
ordinary case. These controls are valuable but do not close the ownership, TOCTOU, pre-existing
assignment, journal-recovery, or verifier gaps above.

## Required follow-up coverage

Before live application, add regression cases for a valid forged intent, two journal paths
targeting one repository, a mutation race after the final read, disappearance of a pre-existing
destination assignment, truncated and malformed journal records, rollback timeout/uncertain
results, invalid repository and issue path inputs, additive verification, and complete rename
definition verification. Re-run the focused suite and the complete suite after those repairs.
