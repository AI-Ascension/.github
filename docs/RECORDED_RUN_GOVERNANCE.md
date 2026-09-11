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
`f6861dffb0f45cdc01f122c027f219437f4773fd`, including import edge fixes
and descriptor-based extended-metadata rollback corrections. Harness's final
local commit is `a065fe5187afefa9deccba2355ed5c1f00ba20ac`, correcting seed
identity validation against the source contract. These revisions exist locally;
publication is not claimed.

The current workflow matrix records eight valid and 25 invalid candidate 3
vectors passing all three implementations, matching summaries/payloads, and
duplicate import retaining one revision. Protocol and Studio independent
review findings are closed within their reviewed scope. Coordinator evidence
also records independent observability consumer and metadata-rollback closure.
Harness reports 656 tests passed, zero failed and five ignored at its final
revision, plus formatting, Clippy, strict policy and build checks. These are
owner/coordinator results, not product tests rerun by governance.

The independent harness reviewer closed the original findings and named
follow-ups after rerunning all five review-2 cases and validating the actual
Train review-2 artifact. The closure verifies source-schema seed identity
handling, three affected rows for raw-seed omissions, and invalid versus
unsupported accounting dispositions. It reports no new defect within that
bounded scope; it is not an exhaustive source-format or filesystem audit.
Evidence: `recorded-run-integration/reviews/harness-independent.md`.

### Actual Train candidate 3, review 2

The corrected exporter produced the same 11,506-byte ZIP twice from the existing
Train recording. Its byte SHA-256 is
`fe10fe2d9674493469f17a51f59d2b01f07b4cbd1c5179e061148e97bf476317`;
semantic digest is
`e5bd1aaac5209573192861c81f3bbac6b6356c24f48c129b52e93e508454b686`.
The executed transport binary SHA-256 is
`48a4ff28886dfbeaba9de0bcb03f1325434952023e9a775eec9b9b6dbbc14fb3`.
All nine recorded source fingerprints (sizes, hashes and modification times)
are unchanged. Reconciliation remains 240 source rows: 9 emitted and 231
filtered, yielding 8 events and 1 accounting record.

The protocol, Studio and observability CLIs accepted those exact bytes.
Cross-consumer evidence compares events, accounting, omissions, identities,
provenance and evidence exactly; retry retains one revision. Seed start is
record-scoped settled/observed. Process exit remains failed, gameplay remains
`episode_failed`, and two action outcomes remain unknown. Seed settlement does
not establish settled gameplay actions, game defeat or successful gameplay.
The exported completeness remains partial with source_snapshot unverified;
unchanged fingerprints do not rewrite that conservative producer assertion.

Actual disposable Collector 0.160.0 → MLflow 3.16.0 proof records 19 persisted
spans and one revision, exact accounting/identity/evidence/stream values, stable
duplicate and restart behavior, and unchanged input artifact. Laminar remains
unverified; Docker image builds were not run.

The coordinator records active LAN preview `http://192.168.1.146:4173/` at
candidate 3 Studio package
`52891bfb9614672cba058e1527b5c653b55e0c321f7a5aef6f8461569c77a821`.
Review-2 VM-origin Chromium evidence verifies actual import, numeric observations
and reported usage, six privacy rejection cases preserving prior state,
duplicate no-op, six readable designer nodes, no page errors or unexpected
requests, and all four served file hashes. Activation/reconnect records establish
enabled service lifetime; the earlier candidate 2 rollback exercise remains
historical procedure evidence, not a newly exercised candidate 3 rollback.
An independent physical LAN-client check remains unverified. Governance inspected
the reports locally and did not probe the host or repeat browser/backend runs.

Evidence locations in the coordination workspace are
`recorded-run-integration/train-candidate3-review2-export-result.json`,
`train-candidate3-review2-seed-evidence.json`,
`train-candidate3-review2-cross-consumer.json`,
`train-candidate3-review2-backend.json`, and
`train-lan-candidate3-review2.json` in that same directory. The workflow matrix
remains authoritative for the shared acceptance ledger. At this inspection its
review-1 rows still awaited these review-2 results; this dated evidence update
does not silently relabel those historical rows or constitute admission.

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

Fresh Train candidate 3 review-2 round-trip evidence is now recorded above.
Workflow owns propagation of its exact producer/bundle pins and evidence into
the shared plans and matrix; old review-1 plans must not be treated as review-2
reproductions. Formal protocol admission remains pending the owner's recorded
decision and final evidence consolidation. No merge, tag, release publication
or organization-wide compatibility is claimed. Docker image builds, Laminar
and an independent physical LAN-client check retain their stated limitations.
