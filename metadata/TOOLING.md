# Metadata tooling contract

The maintained operator guide is [docs/TAGGING.md](../docs/TAGGING.md). The
executable entrypoint is `tools/metadata`, backed by `tools/metadata.py`. Supported
subcommands are `validate`, `snapshot`, `plan`, `apply`, `verify`, and `rollback`.
The internal `_MetadataWriter` is private to the guarded CLI and synthetic tests.

Schemas in `schema/` describe the canonical repository map, shared definitions,
migration input, local snapshot, plan, and authorization. Custom validation also
checks cross-file identity, applicability, source pins, label collisions, topic
preservation, and forbidden automatic assignment destinations. Repeating an
identical set of normalized inputs produces the same plan digest.

`labels.yml` may scope a definition with `repository_ids`; an empty list is an
inactive proposal. Unknown or misspelled applicability fields fail rather than
becoming a global label definition. Snapshot collection paginates repositories,
labels, issues/PRs, branches, tags, and releases. It resolves actual default-branch
commits and source trees. Absent visibility/archive/usage fields are errors, not
empty or safe defaults. Private exclusions stay in the local snapshot and cannot
authorize target selection.

`plan` consumes the complete map and snapshot even when repeated
`--repository-id` selects a canary. Operations include content-bound reasons,
evidence, permission requirements, blast radius, before/after state, and inverse
semantics. Source paths are checked against pinned, complete source trees; a
missing/truncated tree blocks applicability.

Execution and rollback use stable repository/label/issue identities, complete
preflight, immediate state re-reads, postcondition verification, durable signed
journals, and explicit uncertain-outcome resume. See
[EXECUTION_BOUNDARIES.md](EXECUTION_BOUNDARIES.md) for concurrency, local trust,
Linux/WSL support, and limitations. Created label definitions are retained by
default; conflicts return a nonzero exit status. The fake-transport regressions
are under `tests/test_metadata*.py`; consumer transitions have separate tests.

No live apply, rollback, publication, or hosted workflow result is implied by a
local test pass. The dated audit records the exact checks actually executed.

## Source pins and ancestry

`tools/metadata_drift.py` reports a recorded `default_commit` that no longer
matches the live default-branch head. In an active organization the head moves
continuously, so that condition alone cannot tell ordinary movement apart from
a registry that has lost the source it was reviewed against. By default the
monitor therefore asks GitHub how the two revisions relate and separates the
two cases:

- `source_pin_advanced` is informational. The live branch still contains the
  recorded baseline, so the source moved forward without diverging from what
  was reviewed. The registry is left unchanged: advancing a baseline to a new
  head remains a separate, reviewed owner decision.
- `source_pin` remains a red mismatch when the live branch is behind the pin,
  has diverged from it, or the relation cannot be measured.

The monitor fails closed. An unmeasurable pin is never assumed contained, and
`--no-ancestry` restores strict live-head equality for callers that need it.
Ancestry is read one field at a time because the compare endpoint embeds
user-controlled commit text, which can make the whole response invalid JSON.
