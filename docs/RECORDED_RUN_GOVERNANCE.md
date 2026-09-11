# Recorded-run compatibility governance

Status: proposed governance guidance. No portable recorded-run schema, profile,
bundle, conformance vector, digest, release, consumer implementation, or
organization-wide compatibility claim is admitted by this document.

## Ownership

| Concern | Owner | Governance boundary |
| --- | --- | --- |
| Portable envelope, profile names, schema, canonical bytes, conformance vectors, and contract admission | `sts2-protocol` | The only repository that may publish an admitted shared recorded-run contract. |
| Run meaning, legacy-format detection, export, source-to-contract mapping, omissions, and reconciliation | `sts2-harness` | Source recordings and private storage remain harness-owned. SQLite is optional read-only evidence. |
| Browser file import and read-only recorded inspection | `ascension-workflow-studio` | Imported data is distinct from live workflow state and cannot provide execution controls. |
| Independent tracking import and duplicate/update behavior | `ai-agent-observability` | Imported history is not live telemetry or proof of backend persistence. |
| Cross-repository scenario, compatibility matrix, and acceptance ledger | `ascension-workflow`, unless an accepted owner decision assigns it elsewhere | It compares contract-defined fields; it does not become a second scheduler or contract owner. |
| Game, gateway, MCP, and watchdog records | Their existing repository owners | Their authority and identity namespaces remain intact; historical import conveys no game, lease, retry, or recovery authority. |

`org-governance` consumes dated technical evidence and records organization-level
limits. It must link an exact contract artifact or commit only after one exists.

## Admission gate

Implementation and review may proceed against an exact pinned candidate before
admission. Candidate implementation does not require a merged contract or an
admitted digest; it must be revalidated whenever the candidate changes.

A proposed recorded-run contract may be called admitted only when all of these
evidence items name the same exact contract bytes and digest:

1. `sts2-protocol` has merged its versioned schema, profile rules, package and
   extraction rules, compatibility behavior, valid and invalid vectors, and a
   reproducible conformance command.
2. `sts2-harness` has a bounded deterministic exporter for a detected source
   format, an allowlisted mapping, and a reconciliation of emitted, filtered,
   unsupported, malformed-tail, and rejected records.
3. Workflow Studio and `ai-agent-observability` have independently validated
   and processed the identical artifact, with their capability and duplicate
   behavior recorded.
4. Evidence covers integrity, unsafe and colliding archive entries, resource
   bounds, unsupported required versions, unknown optional profiles, malformed
   or truncated records, omission/redaction, distinct identity namespaces, and
   lossless nanosecond handling.
5. A maintainer has accepted the technical admission in the owning protocol
   repository. Governance documentation may then cite that decision and its
   scoped consumer evidence.

Passing a schema validator, a synthetic fixture, a component test, or one
consumer import alone does not satisfy this gate. An admitted artifact does not
by itself establish successful gameplay, process settlement, deployment,
release readiness, or organization-wide compatibility.

## Version and digest policy

The inspected protocol candidate is `1.0.0-candidate.2`, which supersedes
`1.0.0-candidate.1`. The protocol owner's candidate requires exact wire-version
matching; a shared major number alone does not imply compatibility between
candidates or with a future release. A wire or semantic change requires a new
candidate revision, fresh pins, and producer/consumer revalidation. Published
artifact bytes must not be silently rewritten.

Keep schema, producer, adapter, protocol, runtime, game-mod, provider and workflow
versions independent. A candidate version does not synchronize those components
or create an organization release. Record the exact schema SHA-256 and artifact
`SHA256SUMS` inventory digest as review pins. These differ from an exported ZIP's
byte digest and the contract-defined semantic digest of a recording revision.
None of these digests is an admission decision.

The candidate separates logical recording identity from semantic revision.
Re-import of the same identity and semantic digest is idempotent. A changed
semantic digest identifies another revision; it does not authorize automatic
merge or overwrite. Consumer evidence must show revision handling and conflicts
without collapsing source identity namespaces or manufacturing workflow IDs.

## Compatibility claims and contributor guidance

Each report must state its available exact bundle digest, producer and adapter version,
source-format detector, contract/profile version, consumer revision, commands,
results, omissions, and remaining `unverified` items. It must distinguish
`confirmed`, `source-derived`, `inferred`, `proposed`, `unverified`, and
`unsupported` dispositions alongside the shared evidence labels. Missing pins
and unrun checks remain explicitly pending; contributors must not invent them.

Consumers reject unsupported required major versions and unsafe or integrity
failing packages before presenting records. Unknown optional profiles may be
retained with a diagnostic only when the admitted contract permits that
behavior. Import is inspection-only: it never grants replay, pause, resume,
step, restart, retry, recovery, lease, or game-mutation authority.

Portable exports contain only profile-admitted allowlisted fields. They exclude
credentials, private prompts, raw provider output, raw MCP messages, private
host or filesystem paths, proprietary assets, and unreviewed text. Integrity
digests prove byte integrity within their declared scope; they do not prove
authenticity or successful gameplay.

## Current boundary

Source-derived snapshot, 2026-09-11: concrete candidate schema, artifact copy,
semantic/package rules, fixtures, checksum inventory, validator and proposed
ADR 0034 now exist in the protocol integration worktree. They are unadmitted
candidate files; no candidate commit or release is cited here because the
inspected files are uncommitted. The local review locations are
`worktrees/recorded-run-sts2-protocol/artifacts/recorded-run-bundle-v1/` and
`recorded-run-integration/sts2-protocol.md` in the coordination workspace.

| Review pin at this snapshot | SHA-256 |
| --- | --- |
| Candidate 2 schema | `d5098e5f969d99707d3ad1d97acdbc803285b93f1eb1dcfe5dc3f63c534192af` |
| Candidate 2 artifact inventory (`SHA256SUMS`) | `a43f4ee6a93973aa0cf60dd8e4de70520b9c3214d1ed772fdb66610054773d64` |

The coordinator records protocol, harness, Studio, observability and workflow
implementation in progress. Candidate 1 references in earlier handoffs are
historical and require migration/revalidation against the agreed successor.
This governance snapshot does not establish agreement on those pins.

Pending evidence gates remain: producer/two-consumer agreement and independent
review; required repository and conformance checks; deterministic real-source
export with source preservation and count/omission reconciliation; identical
artifact import in Studio and observability with identity, evidence, accounting
and retry comparisons; browser import and authoring/contrast checks; verified
LAN deployment with tested asset digests, explicit lifetime and rollback; and
the workflow-owned scoped matrix and maintainer admission decision. The
coordinator's receipt of all ten discovery handoffs is discovery coverage only.
The organization disposition remains `unverified` for portable recorded-run
compatibility.
