# Independent execution re-review

Reviewed 2026-09-07 against the latest stable files visible at review time. The reviewed
implementation hashes are:

| File | SHA-256 |
| --- | --- |
| `tools/metadata_execution.py` | `3ca56deedd9ea6a99dc8d88cb54119ecb329a29fe4d5d1c72cd1849129420a01` |
| `tools/metadata_journal.py` | `50d0d5458a7619757adb764d0003820680c427275d8510355b27820cff5408b1` |
| `tests/test_metadata_execution.py` | `ee003b8601d974b74b144aa5c3937adcf6d8729676db6a6f56233a6094cdc09b` |
| `tools/metadata.py` (verification and CLI boundary) | `67be5c0f5c54f726db1e2ae64df300de50688a745215a9c6daaefa6a74b31f38` |

The prior review is preserved in `execution-independent-review.md`. This rereview edited no
implementation or test file.

## Validation

* `python3 -m unittest -v tests/test_metadata_execution.py`: **25 passed**.
* `python3 -m unittest discover -s tests -v`: **51 passed**.
* The integration cases now pass: additive verification preserves the source and unmanaged
  labels, and rename verification detects a later definition edit.
* An authenticated plan-shaped intent without a verified event produced a manual-review
  conflict and zero rollback writes.
* Removing a pre-existing destination assignment from the reviewed issue snapshot was rejected
  during preflight with zero writes.
* A complete authenticated malformed event failed closed; an authenticated empty effect was
  returned as a rollback conflict instead of escaping with `KeyError`.
* Invalid repository and issue path inputs were rejected by `validate_plan` before any write.
* Same-journal concurrent access was rejected by the non-blocking file lock; two separate journal
  paths were able to proceed concurrently, as described below.

## Prior findings

### Valid forged intent: resolved within the local trust boundary

`metadata_journal.py` now creates a 32-byte key in the operator state directory, authenticates
the chained records with HMAC, binds the chain to the plan digest, and refuses an existing
journal when its local key is absent. `MetadataWriter.rollback` also requires a matching
`verified` event with `owned: true`; an `intent` alone is treated as uncertain ownership. The
focused forged-journal test and the signed plan-shaped intent probe both produced no unauthorized
rollback write.

The local state directory and its key remain a trusted same-user boundary by design. A process
that can read the local key can forge a valid `verified` event and authorize rollback; the
journal has no independent operator signature or authorization record. Do not adopt journals
from another machine, and do not treat local HMAC as provider or human approval evidence.

### Separate journal paths for one repository: **unresolved high-severity blocker**

The `flock` is held only on `self.path`, and the key is also derived from that path. A barrier
probe let two writers with different journal paths complete preflight against the same topic set;
both then issued `PUT /topics` successfully with different complete sets. The final state was the
last writer's set, with no conflict. A repository-scoped lock or an API compare-and-swap contract
is still required before claiming serialized writes across plans.

### Edit after the last read and before mutation: **unresolved high-severity blocker**

`effect` reads the state, records intent, and then calls `mutate`; the GitHub write has no ETag or
conditional precondition. A fake server edit inserted `human` immediately before `PUT /topics`.
The executor returned success and overwrote that edit. Postcondition verification only observes
the state after the overwrite and cannot close this window. This is a documented GitHub/API
atomicity limitation in the current design; the implementation must not claim race-free or
atomic live application until a server-side conditional write or an equivalent serialized
repository lock is in place.

The same limitation applies to label-definition PATCH and rollback topic/label writes.

### Pre-existing additive assignments: resolved

`preflight_additive` now re-reads every assignment row, including rows for which the destination
was already present in the reviewed snapshot. If that unowned row changes or loses the destination,
execution fails before the first write. The focused regression and the independent probe both
confirmed this behavior. Rollback continues to skip assignments the plan did not own.

### Additive and rename verification: resolved

`_assignment_mismatches` now expects the additive destination while preserving the source and
every unmanaged label. `_definition_matches` compares stable ID, name, color, description, and
archive state for rename verification. The two previously failing integration cases pass, as does
the complete 51-test suite.

### Torn and malformed journal data: mostly resolved, with a durability limitation

The journal authenticates every complete line and rejects a malformed or unauthenticated record.
An incomplete final line is backed up by digest, truncated from the active journal, and replaced
with an authenticated `recovered-tail` record; the focused recovery test passes. Rollback now
catches malformed effects as per-effect conflicts rather than raising while constructing the
error result.

The conflict result is returned to the caller but is not itself appended as a durable journal
event. If the process dies before the caller records the result, the malformed effect remains
only as an authenticated intent and will be reconsidered on a later inspection. Keep the
manual-review requirement, and add a durable conflict event if crash-survivable conflict history
is required.

### Rollback network uncertainty: resolved for ordinary exceptions

Mutation exceptions are logged as `rollback-uncertain` and re-raised from the effect; rollback
catches the exception, returns a conflict, and continues its per-effect loop. The timeout
regression confirms that an accepted write followed by a timeout is reported as one conflict and
is not blindly retried. A later explicit read/resume remains necessary because a timeout does not
identify whether the server accepted the mutation.

### Endpoint and issue-path validation: resolved at executor entry

`validate_plan` now binds repository strings to the `AI-Ascension/<name>` shape, rejects traversal
and malformed source pins, validates positive integer issue identities, and validates operation
schemas before `apply` or `rollback` opens the journal or invokes the client. Independent
traversal and `1/labels` issue-number probes were rejected with no writes. The lower-level
`api`/`mutate` methods remain generic seams; callers must enter through the validated plan API.

### Authorization boundary: unresolved for direct low-level callers

The CLI requires a reviewed applicable plan, an authorization record, the requested operation,
operator binding, and (for apply) the authenticated GitHub user before constructing the writer.
The CLI regression confirms an invalid authorization does not construct a client. The imported
`MetadataWriter` still accepts a self-consistent plan with `execute=True` without operator,
approval, or authorization checks, exactly as its module doc states. Keep the class private to the
guarded CLI or move a mandatory authorization boundary into the execution API before treating the
module as safe for general callers.

## Additional boundary observation

The current `MetadataWriter.identity` checks repository ID, full name, default branch, commit, and
archive state, but does not compare a captured target visibility when the plan contains one. The
planner and CLI validate visibility in their own paths; direct execution therefore needs an
explicit visibility check if visibility is part of the write precondition.

## Release/application conclusion

The repaired journal, ownership checks, pre-existing assignment preflight, verifier, malformed
record handling, timeout conflict handling, and plan input validation are supported by tests and
probes. Live application remains blocked by the unresolved repository-scoped concurrency and
read-to-write race windows, the low-level authorization bypass, and the local-key trust/durability
limitations described above. No live GitHub write was made by this re-review.

## Final delta re-review — 2026-09-07

This bounded delta independently checked the three repairs applied after the preceding review.
The latest files evaluated have these SHA-256 values:

| File | SHA-256 |
| --- | --- |
| `tools/metadata_execution.py` | `0af078a2c37c8a33974b2dccb6a47f5c4177183b34e7e7864e6e9f2cd8501a09` |
| `tools/metadata_journal.py` | `6a445f4a7d012913359a0f251efdf5e62315335dca8126ce7a8d583210191048` |
| `tests/test_metadata_execution.py` | `e492c92f6bb81c1b1deb140e7364dec72e729a8eaa5240589159594a9094a99b` |
| `tools/metadata.py` | `67be5c0f5c54f726db1e2ae64df300de50688a745215a9c6daaefa6a74b31f38` |

`python3 -m unittest -v tests/test_metadata_execution.py` passed **27 tests**, and
`python3 -m unittest discover -s tests -v` passed **54 tests**.

### Repository-scoped journal locking: resolved

`Journal` now creates and non-blockingly locks a state-directory file derived from each stable
repository ID before it reads the journal or permits preflight. IDs are acquired in sorted order;
partial acquisition errors release already-held handles, and context exit releases all handles.
The new distinct-journal regression confirms that a second journal for the same repository is
rejected before an identity read. An independent concurrent probe produced one lock conflict and
one successful writer, with one metadata write. A separate probe forced an identity failure and
then successfully reused the same state and journal path, confirming release after an apply
error. The previous cross-journal overwrite finding is resolved for this local process boundary.

### Visibility precondition: resolved

`MetadataWriter.identity` now compares a captured target visibility with the live repository
identity after checking ID, full name, branch, archive state, and commit. The new regression and
an independent private-versus-public probe both rejected before any metadata write.

### Durable rollback conflicts: resolved

When rollback catches an effect exception, it now appends a signed `rollback-conflict` event to the
journal before returning the conflict result. The timeout regression checks the event, and an
independent accepted-write-then-timeout probe observed the returned conflict, zero rollback writes,
and a durable authenticated `rollback-conflict` as the final record.

The GitHub read-to-write mutation window remains the documented API limitation from the preceding
review. No code or evidence here claims atomic or race-free GitHub writes; a server-side
conditional mutation or equivalent external serialization would still be required for that
stronger claim. The privileged low-level executor boundary and local-key trust model remain as
previously recorded. No live GitHub write was made by this delta review.

## Final candidate delta — 2026-09-07

This final bounded check covers exactly the three handoff changes made after the preceding delta.
The final candidate hashes evaluated are:

| File | SHA-256 |
| --- | --- |
| `tools/metadata_execution.py` | `c3943a00dc7174a0ee4124dd1ecc9ac3cc43d74241ec80206eb3b453faa54f9c` |
| `tools/metadata_journal.py` | `6a445f4a7d012913359a0f251efdf5e62315335dca8126ce7a8d583210191048` |
| `tests/test_metadata_execution.py` | `30fdf04bcdd8c58bee390a9f1b6b2debc20abe38a369ab95ffaa16de225e3607` |
| `tools/metadata.py` | `b6c4526d202b448c528ab5064f3b174b2c7ddb82c50593508cb9e671f03b38de` |
| `tests/test_metadata_integration.py` | `cc14dc0e3a40c0017f74ee8e82340c632436269272ba5de6c5e64cf7f401c637` |

`python3 -m unittest discover -s tests -q` passed **56 tests**. Independent checks confirmed:

* a GET `rate_limit` raises immediately with one runner call, without a guessed retry delay;
* the CLI returns exit status 1 when rollback returns conflicts; and
* `metadata_execution` exports `_MetadataWriter` without a public `MetadataWriter`, while the
  guarded CLI imports the private class under its internal alias.

These three final candidate changes are verified. The previously documented GitHub read-to-write
race remains an API limitation, with no atomicity or race-free write claim added. No live GitHub
write was made by this check.
