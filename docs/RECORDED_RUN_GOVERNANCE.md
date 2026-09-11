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

## Admission evidence and ownership

Implementation and review may proceed against an exact pinned candidate before
admission. Candidate implementation does not require a merged contract or an
admitted digest; it must be revalidated whenever the candidate changes.

The protocol owner's `docs/recorded-run-admission.md` defines technical admission
and release gates. Governance summarizes those gates; it introduces no separate
approval process or merge-before-testing requirement. The workflow-owned
`integration/recorded-run-matrix.md` is the authoritative shared compatibility
matrix. The coordinator's deployment ledger supplies dated host evidence.

For candidate 3, the owner requires corrected harness export and source
reconciliation, validation and consumption of identical real-source bytes by
both consumers, resolution of applicable review findings, and browser/tracking
integration evidence. Protocol maintainers then record technical admission
against the exact source commit, schema/inventory pins, consumer evidence and
migration classification. Candidate status and empty admitted-consumer metadata
remain truthful until that decision. Release/version publication follows the
owner's existing release policy separately; task-specific agent permissions
are not compatibility requirements.

Passing a schema validator, a synthetic fixture, a component test, or one
consumer import alone does not satisfy this gate. An admitted artifact does not
by itself establish successful gameplay, process settlement, deployment,
release readiness, or organization-wide compatibility.

## Version and digest policy

The inspected protocol candidate is `1.0.0-candidate.3`, which supersedes
candidates 1 and 2. The protocol owner's candidate requires exact wire-version
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

Source-derived snapshot, 2026-09-11: candidate 3 exists at local, unpublished
protocol commit `6cdcf0995b25185e59c57d21b1e7a23c2d9b5f8a`. Its sources are
`schemas/recorded-run-bundle-v1-candidate3.schema.json`,
`artifacts/recorded-run-bundle-v1-candidate3/`, ADR 0035, and
`docs/recorded-run-admission.md`. The older unsuffixed artifact directory still
contains candidate 2; it must not supply candidate 3 pins. No tag or release
is asserted.

| Review pin at this snapshot | SHA-256 |
| --- | --- |
| Candidate 3 schema | `a6c32127290f4d5e670d8863f97a74a7b8e3e411e735d81394b51fe1578b4eb6` |
| Candidate 3 artifact inventory (`SHA256SUMS`) | `580c1cf3be4bb3e4eb37b9acd9166808b7386b0eb84286cc0798a0d88e35bb35` |

Studio's local unpublished commit is
`ad9f764c5caf6a7208b55d380e4f79f7ad8e6455`; observability's is
`3f611e52c96cfbef6d37b0e1a553eaa8184010b1`, including import edge fixes
`6c5ee3fd7aecda4fd641931d990daef57367a5ee` and a separate baseline rollback
correction. These revisions exist locally; publication is not claimed.

The current workflow matrix records eight valid and 25 invalid candidate 3
vectors passing all three implementations, matching summaries/payloads, and
duplicate import retaining one revision. Protocol and Studio independent
review findings are closed within their reviewed scope. Observability final
edge/baseline review and harness corrected immutable binary remain pending.
Local Chromium and synthetic tracking results do not fill the fresh Train gate.

The coordinator records real candidate 2 Train export/import (8 events and
1 accounting record), 240 source rows reconciled as 9 emitted and 231 filtered,
and nine unchanged source fingerprints. Actual candidate 2 disposable
Collector-to-MLflow evidence includes 19 persisted spans, one revision, retry
and restart checks. Laminar and fresh candidate 3 actual tracking remain
unverified.

The deployed LAN preview at `http://192.168.1.146:4173/` is the privacy-patched
candidate 2 release
`f5722374a5de4e7bd3393b42a64479b43c78cd7a0889d71f629e8d0885f3ca35`.
Coordinator evidence verifies served bytes, enabled user-service lifetime,
rollback to the prior release and restoration, and VM-origin Chromium actual
Train/privacy/duplicate/authoring checks. This is dated evidence, not a live
status probe by governance. Candidate 3 deployment and an independent physical
LAN-client check remain unverified. Historical candidate 2 results must retain
their original pins and scope.

## Migration commands and next outcomes

From the protocol worktree, with Node 24, validate an existing candidate 3 ZIP:

```sh
node tools/recorded-run/validate.mjs /path/to/candidate3.zip
```

From the workflow worktree, after building its documented runner binaries,
run the pinned ordered consumer plan into a new output directory:

```sh
cargo run --locked --manifest-path tools/recorded-run-driver/Cargo.toml -- \
  integration/recorded-run-candidate3-consume-plan.json \
  /path/to/candidate3.zip .local/candidate3-consume-new
```

Use workflow's `conformance/recorded-run.md` for build, vector and deeper
payload/persistence comparison commands. A golden ZIP demonstrates synthetic
conformance only. Runner exit 0 means the scoped comparison passed, exit 1 a
failed gate, and exit 2 missing required pins. Do not relabel candidate 2 ZIPs
or remove a candidate suffix; re-export with the corrected producer and re-pin
all affected consumers. Preserve historical tooling and a last-known-good pin.

Fresh Train candidate 3 evidence entry: **pending** corrected exporter
source/binary pin, fresh bundle byte/semantic digests, unchanged-source
reconciliation, both consumer and actual tracking results, browser/deployed
asset/rollback evidence, and final review dispositions in the workflow matrix.
Its full export plan intentionally has no exporter pin yet. Formal protocol
admission remains pending those owner-defined gates; organization-wide
recorded-run compatibility remains `unverified`.
