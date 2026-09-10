# Source and evidence snapshot — 2026-09-04

The public browser proof is a historical deterministic gateway replay. Its pinned test result
does not describe every capability of later default branches. Conversely, unmerged proposals
must not be credited to default branches.

A later dated snapshot for 2026-09-05 is appended below. The 2026-09-04 pins and their
labels in this section are historical and are retained unchanged.

## Current default-source boundary

These are `source-derived` pointers, not new runtime executions:

| Component | Default-branch source inspected | What the source adds beyond the original in-memory proof |
| --- | --- | --- |
| Game-mod | [`f5cc07b`](https://github.com/AI-Ascension/sts2-game-mod/tree/f5cc07b6d0f0ef89bd06ea9378e39aa93e82a405) | Managed C# loader, Rust/native listener, host-thread probe, settings and packaging. |
| Gateway | [`c611be6`](https://github.com/AI-Ascension/sts2-gateway/tree/c611be623488a5d57a07e61cd5bb928339d1beff) | Runtime executable with authenticated bounded routes for an attached mod listener. |
| MCP adapter | [`750214c`](https://github.com/AI-Ascension/sts2-mcp-server/tree/750214cf6a403622a09655f7656fadfc520bcad6) | Executable newline-delimited JSON-RPC transport and gateway mapping. |
| Harness | [`7452f6b`](https://github.com/AI-Ascension/sts2-harness/tree/7452f6bc8f48073acd2f2903c6327b25dd2f7314) | Runtime coordinator for the bounded host-probe path, distinct from autonomous provider gameplay. |

The organization also includes [protocol contracts](https://github.com/AI-Ascension/sts2-protocol),
[pure game-core semantics](https://github.com/AI-Ascension/sts2-game-core), this governance
repository, the [static public site](https://github.com/AI-Ascension/AI-Ascension.github.io), and
the [observability stack](https://github.com/AI-Ascension/ai-agent-observability). These are nine
repositories, not nine Rust-only applications. Follow each repository's own source policy.

## Dated host evidence, not general readiness

The [game-mod report](https://github.com/AI-Ascension/sts2-game-mod/blob/f5cc07b6d0f0ef89bd06ea9378e39aa93e82a405/docs/evidence/runtime-v1-host-live-20260902.md)
and [harness integration report](https://github.com/AI-Ascension/sts2-harness/blob/7452f6bc8f48073acd2f2903c6327b25dd2f7314/docs/evidence/runtime-v1-host-integration-20260902.md)
record a September 2 runtime-v1 trace through harness → MCP → gateway → mod → host on
STS2 v0.107.1 (release `59260271`), Windows x86-64. The recorded action displayed a bounded
status overlay and rejected a stale generation. It was not `play_card`, `end_turn`, or an
autonomous game run, and no model provider was exercised.

The reports label that operator-observed result `confirmed`; this snapshot has inspected the
reports, not independently rerun the host. Their source identities include uncommitted worktree
changes, and the operator capture/full logs are not retained. Package hashes are recorded, but
they do not establish an exactly reproducible source tree or validation of today's differently
named package. Treat this snapshot's account of that run as `source-derived`.

Gameplay settlement, reliable autonomous runs, restart recovery, multi-instance behavior,
provider execution, and compatibility beyond the recorded host/package require separate evidence.
The existence of runtime source is not proof of deployment. Open Runtime-v3/gameplay proposals
must be assessed at their own exact heads and as an integrated combination before stronger claims.

## Later snapshot — 2026-09-05: Runtime-v3 gameplay lane merged

These are `source-derived` pointers, not new runtime executions. They do not supersede or relabel
the 2026-09-04 pins above; those remain the historical record for that date.

On 2026-09-05 the owner selected the Exo semantic-catalog lane (`RUNTIME_V3_LANE=exo`) for the two
incompatible Runtime-v3 gameplay proposals whose conflict is recorded in ADR 0007. The six-position
stack merged in fixed order and each repository's default-branch CI passed at the resulting head.

| Component | Default-branch source after the merge | Runtime-v3 position merged |
| --- | --- | --- |
| Protocol | [`4bfc120`](https://github.com/AI-Ascension/sts2-protocol/tree/4bfc120d4221182ca3e80bed0174fb787b6b4690) | 1/6 — `sts2-protocol#8` |
| Game-core | [`87e0f3d`](https://github.com/AI-Ascension/sts2-game-core/tree/87e0f3d9355c0827e989d9fbc31804440852519b) | 2/6 — `sts2-game-core#6` |
| Game-mod | [`7aa51ee`](https://github.com/AI-Ascension/sts2-game-mod/tree/7aa51ee003f5b69ff36e7ba9951f3d58fb8bb162) | 3/6 — `sts2-game-mod#15` |
| Gateway | [`52bd147`](https://github.com/AI-Ascension/sts2-gateway/tree/52bd147667667d62d8d10c7de861d996f365600b) | 4/6 — `sts2-gateway#7` |
| MCP adapter | [`b3684bf`](https://github.com/AI-Ascension/sts2-mcp-server/tree/b3684bf005f09622c39b154b4c081e867105edcf) | 5/6 — `sts2-mcp-server#8` |
| Harness | [`ffa2564`](https://github.com/AI-Ascension/sts2-harness/tree/ffa2564836c7364ab1692cc81307e1bdecff428a) | 6/6 — `sts2-harness#10` |

What this does and does not establish:

- It is `confirmed` that each repository's declared gates passed at the head above: formatting,
  Clippy at `-D warnings`, the workspace test suites, the frozen artifact checksum inventories,
  and each repository's `repo-policy --strict` budget check. That is a statement about commands
  at commits, and nothing more.
- It is **not** evidence of gameplay, autonomous runs, settlement, restart recovery, multi-instance
  behavior, provider execution, or host compatibility. No game was launched, no mod was loaded into
  a host, no profile or save was touched, and no model provider was called during this pass.
- The managed bridge has no concrete `IRuntimeV3HostSource`. That remains an explicit `unverified`
  integration limitation and is not evidence of a completed live run.
- The bounded `play_card` lane was closed as superseded, not merged. Its six branches are preserved
  and unmodified, and the independent Runtime-v2 work those branches also carried was split out and
  merged separately beforehand so that no independent contribution was lost.
- The September 2 runtime-v1 host probe described above is unchanged by this merge and keeps its
  original date, scope, and labels. Nothing in this snapshot promotes a `proposed` or `unverified`
  claim to `confirmed`.

Two co-op proposals remain open and unmerged, `sts2-protocol#11` and `sts2-mcp-server#16`; their
admission is blocked pending contract admission and they are credited to no default branch.

## Updating public claims

Keep historical proof pins intact and add dated evidence rather than silently relabeling them.
Do not say “nothing touches the game” when describing current source, or use the bounded probe
as proof of gameplay. Repository and organization descriptions are separate GitHub settings;
this document does not change them or authorize deployments.

## Final source supplement — 2026-09-05, 14:00 UTC

The snapshots above are retained as historical records at their original source pins. This
`source-derived` supplement replaces the later claims in governance PRs #4 and #5 that all
follow-ups only split functions without changing behavior. In particular, harness PR #19 includes
an allocation behavior correction. Earlier source and host evidence keeps its original scope.

### Intermediate follow-up stage — historical source pointers

| Component | Intermediate source | Scope |
| --- | --- | --- |
| Game-mod | [`bc46e44`](https://github.com/AI-Ascension/sts2-game-mod/tree/bc46e44337b459c5a0aeada5abab72cd78244a41) | [`#27`](https://github.com/AI-Ascension/sts2-game-mod/pull/27): function-budget correction, before #28 and #29. |
| Harness | [`3b9a70f`](https://github.com/AI-Ascension/sts2-harness/tree/3b9a70fdf07467498cdce1556177258ed7dc4a45) | [`#19`](https://github.com/AI-Ascension/sts2-harness/pull/19): function-budget refactoring and allocation correction; also the final source below. |

`source-derived`: the game-mod follow-up reports 17 changed or new members, maximum 57 nonblank
lines. The harness count of 529 changed or new functions, maximum 58 nonblank lines and zero over
60 or 80, belongs to the initial audit at `0149db1ebef3eec89a8183b5ae14b180587e305b`, against
`e9235847bb9b438ce91111ebf60f8f6298cb7976`. It is not a final-head audit. Initial harness CI failed
file-size and argument-count gates; the final PR head `51f7a8a8773442b2dcea8458331aac7dc6d9d256`
resolved those failures and passed CI, followed by separate successful merge-head checks below.

### Final default-source pointers and exact-head CI

`source-derived`: these are the six Rust product default-branch source pointers inspected for
this supplement. `confirmed`: the linked GitHub Actions runs completed successfully at each
listed full commit. CI results establish source/static-test evidence at those commits only.

| Component | Final default-branch source | Successful main CI / policy runs |
| --- | --- | --- |
| Protocol | [`3470bd6`](https://github.com/AI-Ascension/sts2-protocol/tree/3470bd6291d87d4d3259ebe075ce3417d26812cf) | [CI](https://github.com/AI-Ascension/sts2-protocol/actions/runs/33970128073) / [policy](https://github.com/AI-Ascension/sts2-protocol/actions/runs/33970128065) |
| Game-core | [`87e0f3d`](https://github.com/AI-Ascension/sts2-game-core/tree/87e0f3d9355c0827e989d9fbc31804440852519b) | [CI](https://github.com/AI-Ascension/sts2-game-core/actions/runs/33942193166) / [policy](https://github.com/AI-Ascension/sts2-game-core/actions/runs/33942193023) |
| Game-mod | [`f9b81f4`](https://github.com/AI-Ascension/sts2-game-mod/tree/f9b81f4759d23419278af93d7656aacba9bc2adc) | [CI](https://github.com/AI-Ascension/sts2-game-mod/actions/runs/33970297978) / [policy](https://github.com/AI-Ascension/sts2-game-mod/actions/runs/33970297977) |
| Gateway | [`52bd147`](https://github.com/AI-Ascension/sts2-gateway/tree/52bd147667667d62d8d10c7de861d996f365600b) | [CI](https://github.com/AI-Ascension/sts2-gateway/actions/runs/33942336516) / [policy](https://github.com/AI-Ascension/sts2-gateway/actions/runs/33942336523) |
| MCP adapter | [`b3684bf`](https://github.com/AI-Ascension/sts2-mcp-server/tree/b3684bf005f09622c39b154b4c081e867105edcf) | [CI](https://github.com/AI-Ascension/sts2-mcp-server/actions/runs/33942406614) / [policy](https://github.com/AI-Ascension/sts2-mcp-server/actions/runs/33942406619) |
| Harness | [`3b9a70f`](https://github.com/AI-Ascension/sts2-harness/tree/3b9a70fdf07467498cdce1556177258ed7dc4a45) | [CI](https://github.com/AI-Ascension/sts2-harness/actions/runs/33969740064) / [policy](https://github.com/AI-Ascension/sts2-harness/actions/runs/33969740048) |

`source-derived` changes since the initial Exo stack:

- Protocol [`#12`](https://github.com/AI-Ascension/sts2-protocol/pull/12) removes the two Runtime-v3
  file-size exemptions by moving action, transition, and recovery types to `action.rs`, and
  artifact metadata and request context to `metadata.rs`. Public reexports retain their paths;
  message validation and constructor bodies are unchanged. Schemas, golden fixtures, artifact
  bytes, digests, dependencies, toolchain, and lint configuration are preserved. Its metadata,
  formatting, Clippy, tests, strict policy, and every artifact checksum inventory passed at the
  final head; consumer integration and live gameplay remain `unverified`.
- Game-mod [`#28`](https://github.com/AI-Ascension/sts2-game-mod/pull/28), merged at
  [`8dca989`](https://github.com/AI-Ascension/sts2-game-mod/commit/8dca98904464b5b47dec5de88518e6c237fafad7),
  adds the missing Runtime-v2 checksum CI gate for all 23 inventory entries; frozen bytes are
  unchanged. [`#29`](https://github.com/AI-Ascension/sts2-game-mod/pull/29) adds local safety
  explanations for five native unsafe blocks, removes a personal screenshot path from the
  historical overlay report without inventing provenance, and documents the merged opt-in
  repeat-seed practice change. #29 changes comments and documentation only, preserving executable
  behavior, ABI, HTTP contracts, managed sources, frozen artifacts, and packaging.
- Harness [`#19`](https://github.com/AI-Ascension/sts2-harness/pull/19) also sends the independently
  configured `x-mcp-session-id` allocation header and attempts cleanup after failed allocation
  validation using an attributable returned lease fence. Substitution requires matching
  instance/caller/session identity and a safe lease/epoch. A lease is marked released only after
  a response confirms `released`; rejected or failed cleanup does not establish release.
  Synthetic listener tests cover the header, returned-fence cleanup, and rejected confirmation.
  Frozen protocol artifact bytes are preserved. This is a functional correction as well as
  refactoring, and does not establish successful live allocation or cleanup.

`unverified`: gameplay, autonomous runs, settlement, restart recovery, multi-instance behavior,
provider execution, host loading, current-package compatibility, and release readiness are not
established by these source/CI checks. The managed bridge still lacks a concrete
`IRuntimeV3HostSource`. No host or provider run is added by this supplement; the September 2
runtime-v1 probe remains a dated, bounded, source-derived report with its original limitations.

## Reviewed bounded evidence snapshot — 2026-09-06

This supplement records the default-branch source heads and dated owner evidence reviewed on
2026-09-06 for the project-wide acceptance audit. The commit links and evidence links below are
pinned to that reviewed snapshot; the historical pins and labels above remain historical. This
update does not turn a source, build, or component result into a release, deployment, or general
compatibility claim.

| Repository | Reviewed default-branch head | Evidence at the reviewed head |
| --- | --- | --- |
| `sts2-game-core` | [`87e0f3d`](https://github.com/AI-Ascension/sts2-game-core/commit/87e0f3d9355c0827e989d9fbc31804440852519b) | host-independent source and tests |
| `sts2-game-mod` | [`3ee5be4`](https://github.com/AI-Ascension/sts2-game-mod/commit/3ee5be4be104248d64b938fc5763c8b96fbec9be) | [native terminal observation](https://github.com/AI-Ascension/sts2-game-mod/blob/3ee5be4be104248d64b938fc5763c8b96fbec9be/docs/evidence/native-victory-observation-20260906.md), [GPU lifecycle](https://github.com/AI-Ascension/sts2-game-mod/blob/3ee5be4be104248d64b938fc5763c8b96fbec9be/docs/evidence/train-gpu-lifecycle-20260906.md) |
| `sts2-gateway` | [`218ec8e`](https://github.com/AI-Ascension/sts2-gateway/commit/218ec8e6604f166ecf07d36cbc6e81cb6591efa0) | [gateway README](https://github.com/AI-Ascension/sts2-gateway/blob/218ec8e6604f166ecf07d36cbc6e81cb6591efa0/README.md) and co-op producer |
| `sts2-harness` | [`14ed0c3`](https://github.com/AI-Ascension/sts2-harness/commit/14ed0c338f23274ad065fd9ee5fdfdaae316cb38) | [Windows campaign/replay](https://github.com/AI-Ascension/sts2-harness/blob/14ed0c338f23274ad065fd9ee5fdfdaae316cb38/docs/evidence/seeded-astra-campaign-20260906.md), [Linux campaign/replay](https://github.com/AI-Ascension/sts2-harness/blob/14ed0c338f23274ad065fd9ee5fdfdaae316cb38/docs/evidence/linux-seeded-campaign-20260906.md) |
| `sts2-mcp-server` | [`7fbe380`](https://github.com/AI-Ascension/sts2-mcp-server/commit/7fbe380cfbee1b46736ae57019eb56b3e4179dc0) | [read-only co-op executable evidence](https://github.com/AI-Ascension/sts2-mcp-server/blob/7fbe380cfbee1b46736ae57019eb56b3e4179dc0/docs/evidence/coop-synchronization-20260906.md) |
| `sts2-protocol` | [`fe2a872`](https://github.com/AI-Ascension/sts2-protocol/commit/fe2a872b01c5425d03e2faf3a938d39b1de33b78) | [co-op admission decision](https://github.com/AI-Ascension/sts2-protocol/blob/fe2a872b01c5425d03e2faf3a938d39b1de33b78/docs/decisions/0013-coop-synchronization-admission.md) |
| `.github` | [`22a5077`](https://github.com/AI-Ascension/.github/commit/22a5077e5f6a43259a9924dcd6c516dd13e2d1df) | this status record and shared policy |
| `AI-Ascension.github.io` | [`1991771`](https://github.com/AI-Ascension/AI-Ascension.github.io/commit/19917719dbe1b8ee9cd61fac89f556f93cb3a9e3) | public evidence ledger and repository map |
| `ai-agent-observability` | [`b258803`](https://github.com/AI-Ascension/ai-agent-observability/commit/b25880376d3a3334c77f58637267db93581c4c77) | source topology only; live gameplay telemetry remains unverified |

### What the dated runtime records establish

- **Native Windows and Linux campaigns:** the v0.107.1 owner records show visible Astra-controlled
  setup-to-Defeat campaigns through harness → MCP → gateway → mod. The Windows campaign settled
  333 actions and its fresh process replay completed all 333. The Linux campaign settled 431
  actions after one controller restart following a catalog-read failure, and its fresh process
  replay completed all 431 with an independent audit. These records are bounded to the named seed,
  host build, actions, and replay procedure.
- **Terminal Victory observation:** forced Windows and Linux fixtures observe a living-player native
  Victory surface, disabled input, and an empty legal catalog. The fixtures bypass ordinary play;
  they do not establish a model-played campaign Victory.
- **Co-op synchronization:** the consumed `coop-synchronization-v1` profile is a read-only
  coordinator report produced by gateway and read by MCP. Its executable check covered convergence,
  disagreement, disconnect/recovery, stale leases, and rejected reports with zero downstream game
  connections. It provides no native peer identity, action, vote, shared-effect, or multiplayer
  game authority.

### Remaining acceptance boundaries

Model-played Victory, all characters/seeds/branches, broader restart and host-version coverage,
native multiplayer, clean-install/update/rollback and Workshop publication lifecycle, and current
main evidence of real gameplay telemetry reaching both observability backends remain `unverified`.
The project has no public release or deployment claim from these records. Keep each evidence link
scoped to its named guest, host version, fixture, process, and operation set.

## Current acceptance boundary — 2026-09-07

This supplement records the prepared source candidates and the evidence scope at this date. The
release surface is part of `sts2-game-mod`; the organization contained nine repositories when this
boundary was first recorded and thirteen by 2026-09-08 (see the supplement below). A source,
build, or component check does not establish a host run, provider settlement, deployment, or release.

| Repository | Prepared candidate | Scope established at this boundary |
| --- | --- | --- |
| [`sts2-protocol`](https://github.com/AI-Ascension/sts2-protocol) | Runtime-v4 gameplay `520721f5f0f6b7a6078bf0b2d9f8d3c5545a9c97`; co-op `fe2a872b01c5425d03e2faf3a938d39b1de33b78` | Protocol artifacts and synchronization contracts are prepared; native action, vote, effect, and peer gameplay remain unverified. |
| [`sts2-game-core`](https://github.com/AI-Ascension/sts2-game-core) | `87e0f3d9355c0827e989d9fbc31804440852519b` | Host-independent game semantics and tests; no native host or provider result. |
| [`sts2-game-mod`](https://github.com/AI-Ascension/sts2-game-mod) | Integrated `b53789d6ae5c3c391b2d32ab0656737b5a868b68` | Managed/native builds, the 220-type default audit, and the local bundle identity checks pass; no host load or gameplay run. |
| [`sts2-gateway`](https://github.com/AI-Ascension/sts2-gateway) | Consumer `17b93bf35e5256f6adf690aa148fa57d4f56c523` | Bounded route and consumer checks; live host settlement and deployment remain unverified. |
| [`sts2-mcp-server`](https://github.com/AI-Ascension/sts2-mcp-server) | Consumer `c71e453265c73f134a421796ff8f9cfc624e774d` | Binding and expert-mapping checks; live MCP-to-game settlement remains unverified. |
| [`sts2-harness`](https://github.com/AI-Ascension/sts2-harness) | Consumer `181754e5f1ad049c989c1ea72bba9b28affa6bb9` | Formatting, policy, Clippy, 213 workspace tests, and locked release builds pass; provider and gameplay settlement remain unverified. |
| [`.github`](https://github.com/AI-Ascension/.github) | Status preparation from main `0cbdf744d515b16c042eb6e16b1537d8ccf11771` | Dated acceptance summary; no product release or runtime completion claim. |
| [`AI-Ascension.github.io`](https://github.com/AI-Ascension/AI-Ascension.github.io) | Site preparation `4f94cb1d85c4b84c59138ff36e9e697b55491850`; [PR #11](https://github.com/AI-Ascension/AI-Ascension.github.io/pull/11) merged at [`e81dd4e`](https://github.com/AI-Ascension/AI-Ascension.github.io/commit/e81dd4e9ff2f8e5f8ffafc8b1a489d1e1cc7ef9f) | Static documentation tests, merge, and Pages deployment pass; this establishes the reviewed site documentation only, not gameplay or release readiness. |
| [`ai-agent-observability`](https://github.com/AI-Ascension/ai-agent-observability) | Integration `6ce281090f9e5862b1209f4062941c68b4047f7e` | Deployment and privacy source preparation; current-main gameplay ingestion and backend persistence remain unverified. |

The b53789d native outputs are reproducible at the recorded source boundary: Windows is 1,470,920
bytes with SHA-256 `8989565f71399d68ad752a0a3125bdd3bdeec399406813e08d8dc0bdb509dc0b`, and Linux is
656,472 bytes with SHA-256 `9c04f03333c443717c200a6fa38bd2943bb5c0fa7f143519489bc0e62c9441fa`.
Twelve package-path regression tests and the managed type audit pass with no forbidden or missing types. These results cover source,
build, and bundle identity only; they do not establish installation, loading, or compatibility.

A local Windows PowerShell 5.1 parser run for the transport candidates is clean, but Train-guest Windows NetSecurity
rule creation and readback remain unverified. Native launch is paused while the reserved host lacks a
safe storage margin. Model-controlled native gameplay, final platform campaigns and fresh replays,
co-op action and disconnect/rejoin recovery, provider settlement, and live observability correlation
remain open.

A Steam destination item was created as item `3797477798` with legal agreement still required. It
was create-only: no content or preview was uploaded, and visibility, subscription, discovery,
loading, update, rollback, deployment, and public release were not established. Agreement acceptance
and a separate item-state check are required before Workshop lifecycle verification.

These candidates and checks are prepared evidence, not merge approval. Remote heads, pull-request
state, and required checks must be re-queried before any PR, merge, deployment, or publication.

## Repository inventory supplement — 2026-09-08

The organization holds thirteen repositories, not nine. Four are outside the STS2 review pass and
its evidence tables above; this supplement records only what a read-only inventory observed on
2026-09-08 (`source-derived`, nothing executed):

| Repository | Default branch observed | Foundation and CI | Relation to the STS2 repositories |
| --- | --- | --- | --- |
| `ascension-map-visualizer` | `bootstrap` (no `main`) | `AGENTS.md` and `LICENSE` only; no workflow. Draft PR #2 carries the foundation set. | Draft depends on a `sts2-protocol` PR-head revision and unmerged harness schemas; must re-pin to merged commits before merge. |
| `ascension-watchdog` | `bootstrap` (no `main`) | `AGENTS.md`, `LICENSE`, `README.md`, `SECURITY.md`; no workflow. | Draft PR #2 pins protocol `8874b095` (an ancestor of protocol `main`); its CI is red at the current head. |
| `aiascension.tech` | `codex/wire-mailing-list-email` (no `main`) | `README.md` only; no `LICENSE`, no workflow has ever run. | No STS2 relation. Its README describes a live four-model race without an evidence label; treat that page as `proposed` until a dated run record exists. |
| `ascension-brand-overhaul` (private) | `main` | `AGENTS.md`, `README.md`, policy scripts; no `LICENSE`, no CI at `main`. | Brand sources for the presentation drafts open across the other repositories. |

None of the four has a protected default branch. The twelve shared labels from `labels.yml` were
applied to all four on 2026-09-08. Nothing in this supplement changes a claim above; the STS2
evidence tables remain scoped to the nine repositories they name.

## Earlier current default-main source supplement — 2026-09-10, 00:50 UTC

This dated supplement reconciles the live default-main refresh recorded at
`CURRENT-REMOTE-REFRESH-20260910.json` with the public source boundaries. It records source and
component identity only. The current heads do not establish native host legality, settled effects,
provider execution, deployment, release, or general compatibility.

| Repository | Default branch | Reviewed current head | Bounded source/component record |
| --- | --- | --- | --- |
| `sts2-protocol` | `main` | [`f2dac905`](https://github.com/AI-Ascension/sts2-protocol/commit/f2dac90529f584a6511c1760adce9da28f7f910a) | Runtime-v4 expert schemas, copied artifacts, manifests, checksum inventories, typed validators, and conformance cases. |
| `sts2-game-core` | `main` | [`87e0f3d9`](https://github.com/AI-Ascension/sts2-game-core/commit/87e0f3d9355c0827e989d9fbc31804440852519b) | Host-independent semantics and tests; no native host or provider result. |
| `sts2-game-mod` | `main` | [`d8b46bcc`](https://github.com/AI-Ascension/sts2-game-mod/commit/d8b46bccbee9eff108efdab9c8fc9b27dbf2c034) | Runtime-v4 expert state/action bridge and bounded synthetic route/admission checks; live expert gameplay and settlement remain unverified. |
| `sts2-gateway` | `main` | [`434d8c77`](https://github.com/AI-Ascension/sts2-gateway/commit/434d8c77fb01895e90c741609e3d2a0ad0e9e8b8) | Runtime-v4 expert routes, bounded map route, and copied artifacts; host settlement and deployment remain unverified. |
| `sts2-mcp-server` | `main` | [`3b6d71fe`](https://github.com/AI-Ascension/sts2-mcp-server/commit/3b6d71fe9642d27717ca6cfa07b5342b914c044c) | Runtime-v4 expert mapping and merged REST selector recovery; native MCP-to-game settlement remains unverified. |
| `sts2-harness` | `main` | [`b8c50c8`](https://github.com/AI-Ascension/sts2-harness/commit/b8c50c87db0275f0e08d69892f1ebce275f4acb6) | Expert composition, recovery, and bounded synthetic checks; provider and gameplay settlement remain unverified. |
| `ai-agent-observability` | `main` | [`28a48590`](https://github.com/AI-Ascension/ai-agent-observability/commit/28a48590afb75b07590e1b78ea47dae08f5c3ade) | Source topology only; current-main gameplay ingestion, persistence, and two-backend correlation remain unverified. |
| `.github` | `main` | [`dbdc1f19`](https://github.com/AI-Ascension/.github/commit/dbdc1f19b623a5bfe67ab86a8e986b07201c85ca) | Status, profile, and shared policy records; this supplement does not authorize metadata, deployment, or release changes. |
| `AI-Ascension.github.io` | `main` | [`1065799d`](https://github.com/AI-Ascension/AI-Ascension.github.io/commit/1065799de6eea8427ac5ae96e3b9238932ea761f) | Static evidence and repository pages; site source does not establish deployment or runtime evidence. |

The live refresh recorded gateway PR #28 merged at `434d8c77`, MCP PR #32 merged at `3b6d71fe`,
and harness PR #41 merged at `ee28096d`. Protocol PR #24 and game-mod PR #66 remained open/draft;
public-site PR #12 and organization PR #10 remained draft. This state is an inventory at the
recorded refresh time. The separately documented acceptance gates remain partial, with native
campaign, Linux preflight, co-op actuation, observability, Workshop lifecycle, deployment, and
release boundaries unresolved.

This documentation correction pass opened draft PRs from the reviewed current heads: protocol #29
at `0451578c`, MCP #35 at `bc922d11`, harness #48 at `abac06e2`, game-mod #67 at `dd5fb4ef`,
gateway #32 at `322bfb34`, public site #15 at `1e5dd2c7`, and organization #15 at `278b4dfd`.
They contain documentation-only updates and remain separate from product runtime, host, provider,
deployment, release, and gameplay acceptance. Their checks and merge state must be re-queried before
any merge or publication claim.

The admitted `coop-synchronization-v1` profile is a read-only gateway/MCP coordinator-report
contract. It carries no action, vote, shared-effect, or host-game authority. The preserved
`coop-gameplay-v1` action/vote/effect proposal remains unadmitted, and the current source records
do not establish native peer admission or disconnect/rejoin recovery.

## Earlier live default-main and pull-request refresh — 2026-09-10, 02:22 UTC

This supplement supersedes the earlier 00:50 UTC inventory for current GitHub references. It is a
read-only source and pull-request snapshot captured from the GitHub API. The exact refs and
individual check-run records are retained in the acceptance handoff. Source heads and green checks
remain source/component evidence; they do not establish native host legality, settled gameplay,
provider execution, deployment, release, Workshop lifecycle, or observability persistence.

| Repository | Current `main` head | Source/component boundary at this snapshot |
| --- | --- | --- |
| `sts2-game-core` | [`87e0f3d9355c`](https://github.com/AI-Ascension/sts2-game-core/commit/87e0f3d9355c0827e989d9fbc31804440852519b) | Host-independent semantics and tests. |
| `sts2-game-mod` | [`c21ddf38bd2b`](https://github.com/AI-Ascension/sts2-game-mod/commit/c21ddf38bd2b540be871f88303078625966270ce) | Runtime-v4 expert bridge, bounded synthetic checks, and documentation boundary; native expert gameplay and settlement remain unverified. |
| `sts2-gateway` | [`776327aca63c`](https://github.com/AI-Ascension/sts2-gateway/commit/776327aca63c8ff6c6920865cd5c72de83b10c7b) | Runtime-v4 routes, map consumer path, and source checks; host settlement and deployment remain unverified. |
| `sts2-mcp-server` | [`4787efa1251b`](https://github.com/AI-Ascension/sts2-mcp-server/commit/4787efa1251bcc0eddccc5fea63a8939a8eb06d0) | Runtime-v4 mapping and REST selector recovery; native MCP-to-game settlement remains unverified. |
| `sts2-harness` | [`f8b5858d0997`](https://github.com/AI-Ascension/sts2-harness/commit/f8b5858d09978edf17c24b81a5ced07847e2bd5d) | Current head includes the documentation merge; the functional PR41 source is merged at [`ee28096dc722`](https://github.com/AI-Ascension/sts2-harness/commit/ee28096dc722b1e9ef466fc966a79a3422f56ecc). Provider, native, host-restart, and gameplay settlement remain unverified. |
| `sts2-protocol` | [`7fa0d8e82fbc`](https://github.com/AI-Ascension/sts2-protocol/commit/7fa0d8e82fbc245db74187106918d9f1af58c447) | Runtime-v4 schemas, artifacts, validators, and conformance cases. |
| `ai-agent-observability` | [`28a48590afb7`](https://github.com/AI-Ascension/ai-agent-observability/commit/28a48590afb75b07590e1b78ea47dae08f5c3ade) | Source topology and deployment tooling; current-main gameplay ingestion, persistence, and two-backend correlation remain unverified. |
| `.github` | [`217c9c10d82f`](https://github.com/AI-Ascension/.github/commit/217c9c10d82fc22e553c9af222a3a3bbb08259fa) | Governance and acceptance status records. PR15 merged at this head; no metadata, deployment, or release change is implied. |
| `AI-Ascension.github.io` | [`832068b69a44c`](https://github.com/AI-Ascension/AI-Ascension.github.io/commit/832068b69a44cca2bbfa7ea35e90190eddc3b35a) | Static evidence and repository pages; site source does not establish deployment or runtime evidence. |

The 36 open pull requests at the capture time were:

| Repository | Open PRs — head, state, and checks at capture |
| --- | --- |
| `sts2-game-core` | [#10](https://github.com/AI-Ascension/sts2-game-core/pull/10) `bf077908` ready, checks green; [#9](https://github.com/AI-Ascension/sts2-game-core/pull/9) `9a27a80c` draft, checks green. |
| `sts2-game-mod` | [#66](https://github.com/AI-Ascension/sts2-game-mod/pull/66) `5096370b` ready, checks green; [#65](https://github.com/AI-Ascension/sts2-game-mod/pull/65) `57cee12e` ready, Rust foundation failed; [#64](https://github.com/AI-Ascension/sts2-game-mod/pull/64) `79fd4c98` ready, checks green; [#63](https://github.com/AI-Ascension/sts2-game-mod/pull/63) `ad927851` draft, checks green; [#59](https://github.com/AI-Ascension/sts2-game-mod/pull/59) `1ec9431d` draft, checks green; [#58](https://github.com/AI-Ascension/sts2-game-mod/pull/58) `f060c564` draft, checks green; [#57](https://github.com/AI-Ascension/sts2-game-mod/pull/57) `b5fb4ada` draft, dirty merge state; [#55](https://github.com/AI-Ascension/sts2-game-mod/pull/55) `7cc0af3c` draft, checks green; [#54](https://github.com/AI-Ascension/sts2-game-mod/pull/54) `089a60dc` draft, dirty merge state. |
| `sts2-gateway` | [#31](https://github.com/AI-Ascension/sts2-gateway/pull/31) `4411dbfa` ready, checks green; [#30](https://github.com/AI-Ascension/sts2-gateway/pull/30) `193c01a1` ready, checks green; [#29](https://github.com/AI-Ascension/sts2-gateway/pull/29) `9ec73d67` ready, checks green; [#21](https://github.com/AI-Ascension/sts2-gateway/pull/21) `22d780c1` draft, checks green. |
| `sts2-mcp-server` | [#34](https://github.com/AI-Ascension/sts2-mcp-server/pull/34) `3df1549f` ready, checks green; [#33](https://github.com/AI-Ascension/sts2-mcp-server/pull/33) `f4fc4abc` ready, checks green; [#26](https://github.com/AI-Ascension/sts2-mcp-server/pull/26) `6ad97aae` draft, checks green. |
| `sts2-harness` | [#45](https://github.com/AI-Ascension/sts2-harness/pull/45) `416826b9` ready, checks green; [#44](https://github.com/AI-Ascension/sts2-harness/pull/44) `78511d27` ready, Rust quality failed; [#42](https://github.com/AI-Ascension/sts2-harness/pull/42) `a8631198` ready, Rust quality failed; [#40](https://github.com/AI-Ascension/sts2-harness/pull/40) `baabf976` draft, dirty merge state; [#35](https://github.com/AI-Ascension/sts2-harness/pull/35) `423d9052` draft, dirty merge state; [#34](https://github.com/AI-Ascension/sts2-harness/pull/34) `d2105005` draft, checks green. |
| `sts2-protocol` | [#28](https://github.com/AI-Ascension/sts2-protocol/pull/28) `78510509` ready, checks green; [#27](https://github.com/AI-Ascension/sts2-protocol/pull/27) `fa36a49d` ready, checks green; [#26](https://github.com/AI-Ascension/sts2-protocol/pull/26) `c64180b8` ready, checks green; [#25](https://github.com/AI-Ascension/sts2-protocol/pull/25) `b9c25eff` ready, checks green; [#24](https://github.com/AI-Ascension/sts2-protocol/pull/24) `e9199f07` draft, dirty merge state; [#20](https://github.com/AI-Ascension/sts2-protocol/pull/20) `0c39c5a5` draft, checks green. |
| `ai-agent-observability` | [#16](https://github.com/AI-Ascension/ai-agent-observability/pull/16) `a1267155` draft, deployment check green; [#13](https://github.com/AI-Ascension/ai-agent-observability/pull/13) `f872902e` draft, deployment check green; [#12](https://github.com/AI-Ascension/ai-agent-observability/pull/12) `67f455c0` draft, deployment check green; [#10](https://github.com/AI-Ascension/ai-agent-observability/pull/10) `b3a9fa64` draft, dirty merge state. |
| `.github` | [#10](https://github.com/AI-Ascension/.github/pull/10) `d8452379` draft, no checks configured. |
| `AI-Ascension.github.io` | [#12](https://github.com/AI-Ascension/AI-Ascension.github.io/pull/12) `e5153d66` draft, static-and-proof check green, dirty merge state. |

Harness PR41 was independently reviewed at its exact head [`03fdc626`](https://github.com/AI-Ascension/sts2-harness/commit/03fdc6268c1a00e0699e2326b78e340f87228098): its three-dot diff from `e72de4d` contains 179 files, formatting, strict policy, Clippy, and a serial full-workspace result of 285 passed and 5 ignored. A default-parallel rerun exposed one process-start race and is retained in the independent review; the serial rerun passed. PR41's bounded map, replay, REST recovery, and receipt-query source does not establish native gameplay or provider settlement.

The capture records `.github` PR15 already merged at `217c9c10` and site PR15 already merged at
`832068b6`; neither requires another merge action. Historical snapshots and candidate branches
remain preserved with their original dates and labels.


## Post-merge current default-main requery — 2026-09-10, 02:36 UTC

A second read-only GitHub refresh after the documentation merges captured the current default
branches and open pull requests at `2026-09-10T02:36:42.838999Z`. The machine-readable capture
is retained in the acceptance handoff as
`CURRENT-REMOTE-REFRESH-20260910-r3.json` (SHA-256
`34092d43cce3f10ba731096d728aa8caf89615a213a71f7ba7088727bfd9ea43`). It supersedes the
02:22 UTC table above for current repository identity. The 31 open PR records below are an
inventory at this timestamp; source heads and green checks remain source/component evidence and
do not establish native host legality, settled gameplay, provider execution, deployment, release,
Workshop lifecycle, or observability persistence.

| Repository | Current `main` head | Source/component boundary |
| --- | --- | --- |
| `sts2-game-core` | [`87e0f3d9355c`](https://github.com/AI-Ascension/sts2-game-core/commit/87e0f3d9355c0827e989d9fbc31804440852519b) | Host-independent semantics and tests. |
| `sts2-game-mod` | [`caae865986d2`](https://github.com/AI-Ascension/sts2-game-mod/commit/caae865986d2274736d92b4f9be2bbda24bab83d) | Merged seeded-run adapter and Runtime-v4 source/component paths; native expert gameplay and settlement remain unverified. |
| `sts2-gateway` | [`2b44bf347f79`](https://github.com/AI-Ascension/sts2-gateway/commit/2b44bf347f790509c9f13378c89719d09366d45b) | Merged seeded-run boundary and Runtime-v4 routes; host settlement and deployment remain unverified. |
| `sts2-mcp-server` | [`b5a9262f1c76`](https://github.com/AI-Ascension/sts2-mcp-server/commit/b5a9262f1c76da76ea6f84fca0f1ee821ff67001) | Merged seeded-run profile and Runtime-v4 mapping; native MCP-to-game settlement remains unverified. |
| `sts2-harness` | [`3926e5a30ab5`](https://github.com/AI-Ascension/sts2-harness/commit/3926e5a30ab569612e67d2dfdc6542f1391e95d7) | Merged seeded-run transport and PR41 source; provider, native, host-restart, and gameplay settlement remain unverified. |
| `sts2-protocol` | [`d3ab5fca7d9d`](https://github.com/AI-Ascension/sts2-protocol/commit/d3ab5fca7d9d74bb31eeb3e5b343d8024ee44404) | Merged seeded-run selection context and Runtime-v4 schemas, artifacts, validators, and conformance cases. |
| `ai-agent-observability` | [`28a48590afb7`](https://github.com/AI-Ascension/ai-agent-observability/commit/28a48590afb75b07590e1b78ea47dae08f5c3ade) | Source topology and deployment tooling; current-main gameplay ingestion, persistence, and two-backend correlation remain unverified. |
| `.github` | [`8336899bb0a1`](https://github.com/AI-Ascension/.github/commit/8336899bb0a154055691225f7e59d92e8acf2190) | Governance and acceptance status records. |
| `AI-Ascension.github.io` | [`2ae456c6395c`](https://github.com/AI-Ascension/AI-Ascension.github.io/commit/2ae456c6395c1e62395f79db7f42dc3712a6ab3c) | Static evidence and repository pages; deployment remains unverified. |

| Repository | Open PRs — head, state, merge state, and checks |
| --- | --- |
| `sts2-game-core` | [#10](https://github.com/AI-Ascension/sts2-game-core/pull/10) `bf077908` ready, clean, Rust quality gates=SUCCESS; policy=SUCCESS; [#9](https://github.com/AI-Ascension/sts2-game-core/pull/9) `9a27a80c` draft, clean, Rust quality gates=SUCCESS; policy=SUCCESS |
| `sts2-game-mod` | [#65](https://github.com/AI-Ascension/sts2-game-mod/pull/65) `57cee12e` ready, unstable, Rust foundation gates=FAILURE; policy=SUCCESS; Managed source-only boundary=SUCCESS; [#64](https://github.com/AI-Ascension/sts2-game-mod/pull/64) `79fd4c98` ready, clean, Rust foundation gates=SUCCESS; policy=SUCCESS; Managed source-only boundary=SUCCESS; [#63](https://github.com/AI-Ascension/sts2-game-mod/pull/63) `ad927851` draft, clean, Rust foundation gates=SUCCESS; policy=SUCCESS; Managed source-only boundary=SUCCESS; [#59](https://github.com/AI-Ascension/sts2-game-mod/pull/59) `1ec9431d` draft, clean, Rust foundation gates=SUCCESS; policy=SUCCESS; Managed source-only boundary=SUCCESS; [#58](https://github.com/AI-Ascension/sts2-game-mod/pull/58) `f060c564` draft, clean, Rust foundation gates=SUCCESS; policy=SUCCESS; Managed source-only boundary=SUCCESS; [#57](https://github.com/AI-Ascension/sts2-game-mod/pull/57) `b5fb4ada` draft, dirty, Rust foundation gates=SUCCESS; policy=SUCCESS; Managed source-only boundary=SUCCESS; [#55](https://github.com/AI-Ascension/sts2-game-mod/pull/55) `7cc0af3c` draft, clean, Rust foundation gates=SUCCESS; policy=SUCCESS; Managed source-only boundary=SUCCESS; [#54](https://github.com/AI-Ascension/sts2-game-mod/pull/54) `089a60dc` draft, dirty, Rust foundation gates=SUCCESS; policy=SUCCESS; Managed source-only boundary=SUCCESS |
| `sts2-gateway` | [#30](https://github.com/AI-Ascension/sts2-gateway/pull/30) `6bab0129` ready, clean, Rust quality gates=SUCCESS; Repository policy=SUCCESS; [#29](https://github.com/AI-Ascension/sts2-gateway/pull/29) `4ae1cb54` ready, clean, Rust quality gates=SUCCESS; Repository policy=SUCCESS; [#21](https://github.com/AI-Ascension/sts2-gateway/pull/21) `22d780c1` draft, clean, Rust quality gates=SUCCESS; Repository policy=SUCCESS |
| `sts2-mcp-server` | [#33](https://github.com/AI-Ascension/sts2-mcp-server/pull/33) `f4fc4abc` ready, clean, Foundation quality gates=SUCCESS; policy=SUCCESS; [#26](https://github.com/AI-Ascension/sts2-mcp-server/pull/26) `6ad97aee` draft, clean, Foundation quality gates=SUCCESS; policy=SUCCESS |
| `sts2-harness` | [#44](https://github.com/AI-Ascension/sts2-harness/pull/44) `78511d27` ready, unstable, Rust quality gates=FAILURE; policy=SUCCESS; [#42](https://github.com/AI-Ascension/sts2-harness/pull/42) `a8631198` ready, unstable, Rust quality gates=FAILURE; policy=SUCCESS; [#40](https://github.com/AI-Ascension/sts2-harness/pull/40) `baabf976` draft, dirty, Rust quality gates=SUCCESS; policy=SUCCESS; [#35](https://github.com/AI-Ascension/sts2-harness/pull/35) `423d9052` draft, dirty, Rust quality gates=SUCCESS; policy=SUCCESS; [#34](https://github.com/AI-Ascension/sts2-harness/pull/34) `d2105005` draft, clean, Rust quality gates=SUCCESS; policy=SUCCESS |
| `sts2-protocol` | [#28](https://github.com/AI-Ascension/sts2-protocol/pull/28) `78510509` ready, clean, Rust quality gates=SUCCESS; policy=SUCCESS; [#27](https://github.com/AI-Ascension/sts2-protocol/pull/27) `fa36a49d` ready, clean, Rust quality gates=SUCCESS; policy=SUCCESS; [#26](https://github.com/AI-Ascension/sts2-protocol/pull/26) `c64180b8` ready, clean, Rust quality gates=SUCCESS; policy=SUCCESS; [#24](https://github.com/AI-Ascension/sts2-protocol/pull/24) `e9199f07` draft, dirty, Rust quality gates=SUCCESS; policy=SUCCESS; [#20](https://github.com/AI-Ascension/sts2-protocol/pull/20) `0c39c5a5` draft, clean, Rust quality gates=SUCCESS; policy=SUCCESS |
| `ai-agent-observability` | [#16](https://github.com/AI-Ascension/ai-agent-observability/pull/16) `a1267155` draft, clean, Validate deployment contract=SUCCESS; [#13](https://github.com/AI-Ascension/ai-agent-observability/pull/13) `f872902e` draft, clean, Validate deployment contract=SUCCESS; [#12](https://github.com/AI-Ascension/ai-agent-observability/pull/12) `67f455c0` draft, clean, Validate deployment contract=SUCCESS; [#10](https://github.com/AI-Ascension/ai-agent-observability/pull/10) `b3a9fa64` draft, dirty, Validate deployment contract=SUCCESS |
| `.github` | [#10](https://github.com/AI-Ascension/.github/pull/10) `d8452379` draft, clean, no checks |
| `AI-Ascension.github.io` | [#12](https://github.com/AI-Ascension/AI-Ascension.github.io/pull/12) `e5153d66` draft, dirty, static-and-proof=SUCCESS |

The documentation merges are `.github#16` at `8336899bb0a154055691225f7e59d92e8acf2190` and
site `#16` at `2ae456c6395c1e62395f79db7f42dc3712a6ab3c`, with hosted site check
`static-and-proof` successful. The independent harness PR41 review remains scoped to its merged
source head `03fdc626`, formatting, policy, Clippy, and 285 passed/5 ignored serial tests.

Remaining open check failures are game-mod PR65 and harness PR44/PR42. Dirty merge states are
game-mod PR57/PR54, harness PR40/PR35, protocol PR24, observability PR10, and site PR12.
Native host loading, model-provider settlement, terminal gameplay, native co-op actions/recovery,
observability persistence/correlation, Workshop lifecycle, deployment, and release remain
unverified or blocked by the separate acceptance gates.

## Latest post-merge default-main and pull-request refresh — 2026-09-10, 03:11 UTC

A read-only GitHub API requery ran from `2026-09-10T03:11:42Z` through `2026-09-10T03:11:44Z` after site PR18 merged. It checked all nine task repositories and found 31 open pull requests. This supplement supersedes the 02:36 UTC table above for current repository identity; source heads and check records remain source/component evidence and do not establish native host legality, settled gameplay, provider execution, deployment, release, Workshop lifecycle, or observability persistence.

| Repository | Current `main` head | Source/component and acceptance boundary |
| --- | --- | --- |
| `sts2-game-core` | [`87e0f3d9355c`](https://github.com/AI-Ascension/sts2-game-core/commit/87e0f3d9355c0827e989d9fbc31804440852519b) | Host-independent semantics and tests. |
| `sts2-game-mod` | [`caae865986d2`](https://github.com/AI-Ascension/sts2-game-mod/commit/caae865986d2274736d92b4f9be2bbda24bab83d) | Merged seeded-run adapter and Runtime-v4 source/component paths; native expert gameplay, installation, and settlement remain unverified. |
| `sts2-gateway` | [`2b44bf347f79`](https://github.com/AI-Ascension/sts2-gateway/commit/2b44bf347f790509c9f13378c89719d09366d45b) | Merged seeded-run boundary and Runtime-v4 routes; host settlement and deployment remain unverified. |
| `sts2-mcp-server` | [`b5a9262f1c76`](https://github.com/AI-Ascension/sts2-mcp-server/commit/b5a9262f1c76da76ea6f84fca0f1ee821ff67001) | Merged seeded-run profile and Runtime-v4 mapping; native MCP-to-game settlement remains unverified. |
| `sts2-harness` | [`3926e5a30ab5`](https://github.com/AI-Ascension/sts2-harness/commit/3926e5a30ab569612e67d2dfdc6542f1391e95d7) | Merged seeded-run transport and PR41 source; provider, native, host-restart, and gameplay settlement remain unverified. |
| `sts2-protocol` | [`d3ab5fca7d9d`](https://github.com/AI-Ascension/sts2-protocol/commit/d3ab5fca7d9d74bb31eeb3e5b343d8024ee44404) | Merged seeded-run selection context and Runtime-v4 schemas, artifacts, validators, and conformance cases. |
| `ai-agent-observability` | [`28a48590afb7`](https://github.com/AI-Ascension/ai-agent-observability/commit/28a48590afb75b07590e1b78ea47dae08f5c3ade) | Source topology and deployment tooling; current-main gameplay ingestion, persistence, and two-backend correlation remain unverified. |
| `.github` | [`f948584281f2`](https://github.com/AI-Ascension/.github/commit/f948584281f29b4adb1dc0178036d85237b37e20) | Governance and acceptance status records at this capture; no metadata, deployment, or release change is implied. |
| `AI-Ascension.github.io` | [`d5a11452334a`](https://github.com/AI-Ascension/AI-Ascension.github.io/commit/d5a11452334aab87dfb63986b8c5fe01c9d619b0) | Merged PR18 static evidence and repository pages; Pages deployment and runtime evidence remain unverified. |

The release boundary remains unverified: the current merged game-mod source and its checks do not establish a final installable artifact, host loading, clean-install or update compatibility, Workshop publication or lifecycle, or a public release. The observability boundary remains unverified: the current-main observability source and deployment tooling do not establish gameplay ingestion, persistence, or correlation in both backends.

The 31 open pull requests at capture were:

| Repository | Open PRs — exact head, state, merge state, and checks at capture |
| --- | --- |
| `sts2-game-core` | [#10](https://github.com/AI-Ascension/sts2-game-core/pull/10) `bf07790881279eb0b0f5a87c87d44313d136d370` ready, clean; Rust quality gates=SUCCESS; policy=SUCCESS. [#9](https://github.com/AI-Ascension/sts2-game-core/pull/9) `9a27a80c32dcadd8030cf42c861e9e5da4daed1c` draft, clean; Rust quality gates=SUCCESS; policy=SUCCESS. |
| `sts2-game-mod` | [#65](https://github.com/AI-Ascension/sts2-game-mod/pull/65) `57cee12eab5f6af6ebb4325979e7d2df64c501a0` ready, unstable; Rust foundation gates=FAILURE; policy=SUCCESS; Managed source-only boundary=SUCCESS. [#64](https://github.com/AI-Ascension/sts2-game-mod/pull/64) `79fd4c989fb725298d1a816a1ddbcae946c6e10b` ready, clean; Rust foundation gates=SUCCESS; policy=SUCCESS; Managed source-only boundary=SUCCESS. [#63](https://github.com/AI-Ascension/sts2-game-mod/pull/63) `ad9278512563d4a319177d4c10654ceec696c78c` draft, clean; Rust foundation gates=SUCCESS; policy=SUCCESS; Managed source-only boundary=SUCCESS. [#59](https://github.com/AI-Ascension/sts2-game-mod/pull/59) `1ec9431de14070f8f94fc281d44b3ae5d41573a0` draft, clean; Rust foundation gates=SUCCESS; policy=SUCCESS; Managed source-only boundary=SUCCESS. [#58](https://github.com/AI-Ascension/sts2-game-mod/pull/58) `f060c564163f36c4a20ab1d5d265bb462d6ab32f` draft, clean; Rust foundation gates=SUCCESS; policy=SUCCESS; Managed source-only boundary=SUCCESS. [#57](https://github.com/AI-Ascension/sts2-game-mod/pull/57) `b5fb4adad3b423c1bad18af9a14404fd8342ac50` draft, dirty; Rust foundation gates=SUCCESS; policy=SUCCESS; Managed source-only boundary=SUCCESS. [#55](https://github.com/AI-Ascension/sts2-game-mod/pull/55) `7cc0af3c64da639b191060251e667782d535bb0c` draft, clean; Rust foundation gates=SUCCESS; policy=SUCCESS; Managed source-only boundary=SUCCESS. [#54](https://github.com/AI-Ascension/sts2-game-mod/pull/54) `089a60dc9f6377cc38b23cfab3b12ad0a00aeef7` draft, dirty; Rust foundation gates=SUCCESS; policy=SUCCESS; Managed source-only boundary=SUCCESS. |
| `sts2-gateway` | [#30](https://github.com/AI-Ascension/sts2-gateway/pull/30) `6bab0129ac106444e3235f03cf3ef1ac4cdc9857` ready, clean; Rust quality gates=SUCCESS; Repository policy=SUCCESS. [#29](https://github.com/AI-Ascension/sts2-gateway/pull/29) `4ae1cb54c854f987134672a96f43b8ffd7439b1f` ready, clean; Rust quality gates=SUCCESS; Repository policy=SUCCESS. [#21](https://github.com/AI-Ascension/sts2-gateway/pull/21) `22d780c12c60d8a2e5e1310f57deeea172decbd6` draft, clean; Rust quality gates=SUCCESS; Repository policy=SUCCESS. |
| `sts2-mcp-server` | [#33](https://github.com/AI-Ascension/sts2-mcp-server/pull/33) `f4fc4abc680e0048c40edbd1a0ba6bf182dc5c9e` ready, clean; Foundation quality gates=SUCCESS; policy=SUCCESS. [#26](https://github.com/AI-Ascension/sts2-mcp-server/pull/26) `6ad97aeead88cdb2097675ddff076bc4bb97529d` draft, clean; Foundation quality gates=SUCCESS; policy=SUCCESS. |
| `sts2-harness` | [#44](https://github.com/AI-Ascension/sts2-harness/pull/44) `78511d27aabedd1937e62d9255a24cdaa6b61475` ready, unstable; Rust quality gates=FAILURE; policy=SUCCESS. [#42](https://github.com/AI-Ascension/sts2-harness/pull/42) `a863119854480442070aa2f8e546effcf133efe5` ready, unstable; Rust quality gates=FAILURE; policy=SUCCESS. [#40](https://github.com/AI-Ascension/sts2-harness/pull/40) `baabf9767264de11e09cd65cc7262ba36664ec2d` draft, dirty; Rust quality gates=SUCCESS; policy=SUCCESS. [#35](https://github.com/AI-Ascension/sts2-harness/pull/35) `423d9052c8780173e640fa5991e88e8bae282f47` draft, dirty; Rust quality gates=SUCCESS; policy=SUCCESS. [#34](https://github.com/AI-Ascension/sts2-harness/pull/34) `d2105005ebdb6a5f7dd5e266e80b139e294cf89e` draft, clean; Rust quality gates=SUCCESS; policy=SUCCESS. |
| `sts2-protocol` | [#28](https://github.com/AI-Ascension/sts2-protocol/pull/28) `78510509f6060c5b0fcc79d78cb37847013bffb2` ready, clean; Rust quality gates=SUCCESS; policy=SUCCESS. [#27](https://github.com/AI-Ascension/sts2-protocol/pull/27) `fa36a49da2882bef1828b05eab84713290e0eea8` ready, clean; Rust quality gates=SUCCESS; policy=SUCCESS. [#26](https://github.com/AI-Ascension/sts2-protocol/pull/26) `c64180b840c3355cedb1ed3eba2c2f94031f962a` ready, clean; Rust quality gates=SUCCESS; policy=SUCCESS. [#24](https://github.com/AI-Ascension/sts2-protocol/pull/24) `e9199f0706b1629b19efc6d7874d01662b1802b2` draft, dirty; Rust quality gates=SUCCESS; policy=SUCCESS. [#20](https://github.com/AI-Ascension/sts2-protocol/pull/20) `0c39c5a53b005d94df59f14f0962255d0962203a` draft, clean; Rust quality gates=SUCCESS; policy=SUCCESS. |
| `ai-agent-observability` | [#16](https://github.com/AI-Ascension/ai-agent-observability/pull/16) `a126715501d65a2d25f9d6ecf9c6bd142cc5f590` draft, clean; Validate deployment contract=SUCCESS. [#13](https://github.com/AI-Ascension/ai-agent-observability/pull/13) `f872902ed987f5946bf843824063d10884a1bd29` draft, clean; Validate deployment contract=SUCCESS. [#12](https://github.com/AI-Ascension/ai-agent-observability/pull/12) `67f455c0d4aa142139b3942ed0ad56138eecbf8b` draft, clean; Validate deployment contract=SUCCESS. [#10](https://github.com/AI-Ascension/ai-agent-observability/pull/10) `b3a9fa64f51aa249f387190ce76df8c80a02af4b` draft, dirty; Validate deployment contract=SUCCESS. |
| `.github` | [#10](https://github.com/AI-Ascension/.github/pull/10) `d84523795a64556b82d29f6da1dab62eb9b8b4c8` draft, clean; no checks configured. |
| `AI-Ascension.github.io` | [#12](https://github.com/AI-Ascension/AI-Ascension.github.io/pull/12) `e5153d6628843bbc734686ae926e143a1cf90526` draft, dirty; static-and-proof=SUCCESS. |

The site PR18 merge is recorded at [`d5a1145`](https://github.com/AI-Ascension/AI-Ascension.github.io/commit/d5a11452334aab87dfb63986b8c5fe01c9d619b0). This snapshot keeps all earlier tables and their dates unchanged.

## Latest default-main and pull-request refresh — 2026-09-10, 07:49 UTC

A read-only GitHub CLI API requery ran from `2026-09-10T07:49:24.167067Z` through `2026-09-10T07:49:35.506153Z`. It recorded nine default-main refs and 27 open pull requests. The machine-readable capture is retained in the acceptance handoff as `CURRENT-REMOTE-REFRESH-20260910-r5.json` (SHA-256 `0608c58a55667cf428fcaf1c7684ed083550355a1ac9300ff6e3fee530f08be9`) and supersedes the 03:11 UTC table above for current repository identity. These are source/component and pull-request records; they do not establish native host legality, settled gameplay, provider execution, observability persistence, deployment, release, or Workshop lifecycle.

| Repository | Current `main` head | Source/component and acceptance boundary |
| --- | --- | --- |
| `sts2-game-core` | [`07b51c88ebe9`](https://github.com/AI-Ascension/sts2-game-core/commit/07b51c88ebe949aec263c130ccc63200e38dfaa7) | Host-independent semantics and tests. |
| `sts2-game-mod` | [`903b645bf4dc`](https://github.com/AI-Ascension/sts2-game-mod/commit/903b645bf4dc5b299fbf16e4cef498b9bcd0ea18) | Seeded-run adapter source and managed source boundary; native expert gameplay, installation, and settlement remain unverified. |
| `sts2-gateway` | [`6b6c7f2fac67`](https://github.com/AI-Ascension/sts2-gateway/commit/6b6c7f2fac67de22fdf78c9fd818c6781f689ba0) | Seeded-run gateway source and bounded routes; host settlement and deployment remain unverified. |
| `sts2-mcp-server` | [`73e777b96700`](https://github.com/AI-Ascension/sts2-mcp-server/commit/73e777b96700917cca5ff8f6ce0f5a72009384bc) | Seeded-run transport and gateway mapping source; native MCP-to-game settlement remains unverified. |
| `sts2-harness` | [`68e4f935f251`](https://github.com/AI-Ascension/sts2-harness/commit/68e4f935f251c5e20d07b929c6b1c096d0b7b183) | Seeded-run transport and coordinator source; provider execution, native host restart, and gameplay settlement remain unverified. |
| `sts2-protocol` | [`e5e545c2ff71`](https://github.com/AI-Ascension/sts2-protocol/commit/e5e545c2ff7166e073f6d44256016f85d7ea7e83) | Seeded-run protocol contract source, schemas, artifacts, validators, and conformance cases. |
| `ai-agent-observability` | [`28a48590afb7`](https://github.com/AI-Ascension/ai-agent-observability/commit/28a48590afb75b07590e1b78ea47dae08f5c3ade) | Source topology and deployment tooling; current-main gameplay ingestion, persistence, and two-backend correlation remain unverified. |
| `.github` | [`92ab3ed90027`](https://github.com/AI-Ascension/.github/commit/92ab3ed900272703dbbe892bd333ead2a6cf1a86) | Governance and acceptance status records; no metadata, deployment, or release change is implied. |
| `AI-Ascension.github.io` | [`d5a11452334a`](https://github.com/AI-Ascension/AI-Ascension.github.io/commit/d5a11452334aab87dfb63986b8c5fe01c9d619b0) | Static evidence and repository pages; Pages deployment is separately reported below and runtime evidence remains unverified. |


The release boundary remains unverified: current source and checks do not establish a final installable artifact, host loading, clean-install or update compatibility, Workshop publication or lifecycle, or a public release. The observability boundary remains unverified: current-main source and tooling do not establish gameplay ingestion, persistence, or correlation in both backends.

The 27 open pull requests at capture were:

| Repository | Open PRs — exact head, state, merge state, and checks at capture |
| --- | --- |
| `sts2-game-core` | [#9](https://github.com/AI-Ascension/sts2-game-core/pull/9) `9a27a80c32dcadd8030cf42c861e9e5da4daed1c` draft, clean; Rust quality gates=SUCCESS; policy=SUCCESS. |
| `sts2-game-mod` | [#65](https://github.com/AI-Ascension/sts2-game-mod/pull/65) `57cee12eab5f6af6ebb4325979e7d2df64c501a0` ready, unstable; Rust foundation gates=FAILURE; policy=SUCCESS; Managed source-only boundary=SUCCESS. [#63](https://github.com/AI-Ascension/sts2-game-mod/pull/63) `ad9278512563d4a319177d4c10654ceec696c78c` draft, clean; Rust foundation gates=SUCCESS; policy=SUCCESS; Managed source-only boundary=SUCCESS. [#59](https://github.com/AI-Ascension/sts2-game-mod/pull/59) `1ec9431de14070f8f94fc281d44b3ae5d41573a0` draft, clean; Rust foundation gates=SUCCESS; policy=SUCCESS; Managed source-only boundary=SUCCESS. [#58](https://github.com/AI-Ascension/sts2-game-mod/pull/58) `f060c564163f36c4a20ab1d5d265bb462d6ab32f` draft, clean; Rust foundation gates=SUCCESS; policy=SUCCESS; Managed source-only boundary=SUCCESS. [#57](https://github.com/AI-Ascension/sts2-game-mod/pull/57) `b5fb4adad3b423c1bad18af9a14404fd8342ac50` draft, dirty; Rust foundation gates=SUCCESS; policy=SUCCESS; Managed source-only boundary=SUCCESS. [#55](https://github.com/AI-Ascension/sts2-game-mod/pull/55) `7cc0af3c64da639b191060251e667782d535bb0c` draft, clean; Rust foundation gates=SUCCESS; policy=SUCCESS; Managed source-only boundary=SUCCESS. [#54](https://github.com/AI-Ascension/sts2-game-mod/pull/54) `089a60dc9f6377cc38b23cfab3b12ad0a00aeef7` draft, dirty; Rust foundation gates=SUCCESS; policy=SUCCESS; Managed source-only boundary=SUCCESS. |
| `sts2-gateway` | [#35](https://github.com/AI-Ascension/sts2-gateway/pull/35) `3faaab4f7479efdd0925eb4ace927c24e6ae33c2` draft, dirty; no hosted checks. [#34](https://github.com/AI-Ascension/sts2-gateway/pull/34) `9713bb9e33c3c294cb8813b7bda7d7c6afc9bdac` draft, dirty; no hosted checks. [#21](https://github.com/AI-Ascension/sts2-gateway/pull/21) `22d780c12c60d8a2e5e1310f57deeea172decbd6` draft, clean; Rust quality gates=SUCCESS; Repository policy=SUCCESS. |
| `sts2-mcp-server` | [#26](https://github.com/AI-Ascension/sts2-mcp-server/pull/26) `6ad97aeead88cdb2097675ddff076bc4bb97529d` draft, clean; Foundation quality gates=SUCCESS; policy=SUCCESS. |
| `sts2-harness` | [#51](https://github.com/AI-Ascension/sts2-harness/pull/51) `08a104eda337fb4b922ac0e5d114f98dc8d96c3c` draft, dirty; no hosted checks. [#50](https://github.com/AI-Ascension/sts2-harness/pull/50) `f4f8032eadd2ea826bf3f6049e0c50d32d907f39` draft, clean; Rust quality gates=SUCCESS; policy=SUCCESS. [#44](https://github.com/AI-Ascension/sts2-harness/pull/44) `78511d27aabedd1937e62d9255a24cdaa6b61475` ready, unstable; Rust quality gates=FAILURE; policy=SUCCESS. [#42](https://github.com/AI-Ascension/sts2-harness/pull/42) `a863119854480442070aa2f8e546effcf133efe5` ready, unstable; Rust quality gates=FAILURE; policy=SUCCESS. [#40](https://github.com/AI-Ascension/sts2-harness/pull/40) `baabf9767264de11e09cd65cc7262ba36664ec2d` draft, dirty; Rust quality gates=SUCCESS; policy=SUCCESS. [#35](https://github.com/AI-Ascension/sts2-harness/pull/35) `423d9052c8780173e640fa5991e88e8bae282f47` draft, dirty; Rust quality gates=SUCCESS; policy=SUCCESS. [#34](https://github.com/AI-Ascension/sts2-harness/pull/34) `d2105005ebdb6a5f7dd5e266e80b139e294cf89e` draft, clean; Rust quality gates=SUCCESS; policy=SUCCESS. |
| `sts2-protocol` | [#24](https://github.com/AI-Ascension/sts2-protocol/pull/24) `e9199f0706b1629b19efc6d7874d01662b1802b2` draft, dirty; Rust quality gates=SUCCESS; policy=SUCCESS. [#20](https://github.com/AI-Ascension/sts2-protocol/pull/20) `0c39c5a53b005d94df59f14f0962255d0962203a` draft, clean; Rust quality gates=SUCCESS; policy=SUCCESS. |
| `ai-agent-observability` | [#16](https://github.com/AI-Ascension/ai-agent-observability/pull/16) `a126715501d65a2d25f9d6ecf9c6bd142cc5f590` draft, clean; Validate deployment contract=SUCCESS. [#13](https://github.com/AI-Ascension/ai-agent-observability/pull/13) `f872902ed987f5946bf843824063d10884a1bd29` draft, clean; Validate deployment contract=SUCCESS. [#12](https://github.com/AI-Ascension/ai-agent-observability/pull/12) `67f455c0d4aa142139b3942ed0ad56138eecbf8b` draft, clean; Validate deployment contract=SUCCESS. [#10](https://github.com/AI-Ascension/ai-agent-observability/pull/10) `b3a9fa64f51aa249f387190ce76df8c80a02af4b` draft, dirty; Validate deployment contract=SUCCESS. |
| `.github` | [#10](https://github.com/AI-Ascension/.github/pull/10) `d84523795a64556b82d29f6da1dab62eb9b8b4c8` draft, clean; no hosted checks. |
| `AI-Ascension.github.io` | [#12](https://github.com/AI-Ascension/AI-Ascension.github.io/pull/12) `e5153d6628843bbc734686ae926e143a1cf90526` draft, dirty; static-and-proof=SUCCESS. |


The site PR18 merge remains recorded at [`d5a1145`](https://github.com/AI-Ascension/AI-Ascension.github.io/commit/d5a11452334aab87dfb63986b8c5fe01c9d619b0). Its successful validation run is `34431902416`; its successful GitHub Pages deployment run is `34431902452`; the Pages API reported `built` for `https://ai-ascension.github.io/`. The `.github` PR10 presentation branch remains a separate draft at `d84523795a64556b82d29f6da1dab62eb9b8b4c8` with no hosted checks and is not credited to this refresh.

## Latest default-main and pull-request refresh — 2026-09-10, 08:09 UTC

A read-only GitHub CLI API requery ran from `2026-09-10T08:09:11.513037Z` through `2026-09-10T08:09:12.800229Z`, after `sts2-harness` PR50 merged. It recorded nine default-main refs and 27 open pull requests. The machine-readable capture is retained in the acceptance handoff as `CURRENT-REMOTE-REFRESH-20260910-r6.json` (SHA-256 `daa7e023d6995a59dbc8ee4972aadb1add5af161b26c387ef3ca73c22c2a67c3`) and supersedes the 07:49 UTC table above for current repository identity. These are source/component and pull-request records; they do not establish native host legality, settled gameplay, provider execution, observability persistence, deployment, release, or Workshop lifecycle.

| Repository | Current `main` head | Source/component and acceptance boundary |
| --- | --- | --- |
| `sts2-game-core` | [`07b51c88ebe9`](https://github.com/AI-Ascension/sts2-game-core/commit/07b51c88ebe949aec263c130ccc63200e38dfaa7) | Host-independent semantics and tests. |
| `sts2-game-mod` | [`903b645bf4dc`](https://github.com/AI-Ascension/sts2-game-mod/commit/903b645bf4dc5b299fbf16e4cef498b9bcd0ea18) | Seeded-run adapter source and managed source boundary; native expert gameplay, installation, and settlement remain unverified. |
| `sts2-gateway` | [`6b6c7f2fac67`](https://github.com/AI-Ascension/sts2-gateway/commit/6b6c7f2fac67de22fdf78c9fd818c6781f689ba0) | Seeded-run gateway source and bounded routes; host settlement and deployment remain unverified. |
| `sts2-mcp-server` | [`73e777b96700`](https://github.com/AI-Ascension/sts2-mcp-server/commit/73e777b96700917cca5ff8f6ce0f5a72009384bc) | Seeded-run transport and gateway mapping source; native MCP-to-game settlement remains unverified. |
| `sts2-harness` | [`33437ddb18f6`](https://github.com/AI-Ascension/sts2-harness/commit/33437ddb18f69f68d88521d947efa3568a32a3bf) | Merged durable recovery and raw action identity plus seeded-run transport/coordinator source; provider execution, native host restart, and gameplay settlement remain unverified. |
| `sts2-protocol` | [`e5e545c2ff71`](https://github.com/AI-Ascension/sts2-protocol/commit/e5e545c2ff7166e073f6d44256016f85d7ea7e83) | Seeded-run protocol contract source, schemas, artifacts, validators, and conformance cases. |
| `ai-agent-observability` | [`28a48590afb7`](https://github.com/AI-Ascension/ai-agent-observability/commit/28a48590afb75b07590e1b78ea47dae08f5c3ade) | Source topology and deployment tooling; current-main gameplay ingestion, persistence, and two-backend correlation remain unverified. |
| `.github` | [`e11bc10775eb`](https://github.com/AI-Ascension/.github/commit/e11bc10775eb1cd68909fd6aa6230c6b13966ea3) | Governance and acceptance status records; no metadata, deployment, or release change is implied. |
| `AI-Ascension.github.io` | [`d5a11452334a`](https://github.com/AI-Ascension/AI-Ascension.github.io/commit/d5a11452334aab87dfb63986b8c5fe01c9d619b0) | Static evidence and repository pages; Pages deployment is separately reported below and runtime/release evidence remains unverified. |

The native candidate boundary remains incomplete. Operator evidence records that the previously reviewed stale Windows candidate was removed only after fresh identity-bound guards and that the retained profile/save was hash-verified; this is storage cleanup evidence and does not establish a current native install, host load, provider settlement, or model-played gameplay.

The release boundary remains unverified: current source and checks do not establish a final installable artifact, native host loading, clean-install/update/rollback compatibility, Workshop agreement acceptance, item content or preview visibility, subscription/discovery/loading/update/rollback, or a public release. The earlier Workshop item was create-only, with agreement acceptance and a separate item-state check still required. The observability boundary remains unverified: current-main source and tooling do not establish gameplay ingestion, persistence, or correlation in both backends.

The 27 open pull requests at capture were:

| Repository | Open PRs — exact head, state, merge state, and checks at capture |
| --- | --- |
| `sts2-game-core` | [#9](https://github.com/AI-Ascension/sts2-game-core/pull/9) `9a27a80c32dcadd8030cf42c861e9e5da4daed1c` draft, clean; Rust quality gates=SUCCESS; policy=SUCCESS. |
| `sts2-game-mod` | [#69](https://github.com/AI-Ascension/sts2-game-mod/pull/69) `829a7c30c9b4572ad4bfd80b2beba38049eb288d` draft, dirty; no hosted checks. [#65](https://github.com/AI-Ascension/sts2-game-mod/pull/65) `57cee12eab5f6af6ebb4325979e7d2df64c501a0` ready, unstable; Rust foundation gates=FAILURE; policy=SUCCESS; Managed source-only boundary=SUCCESS. [#63](https://github.com/AI-Ascension/sts2-game-mod/pull/63) `ad9278512563d4a319177d4c10654ceec696c78c` draft, clean; Rust foundation gates=SUCCESS; policy=SUCCESS; Managed source-only boundary=SUCCESS. [#59](https://github.com/AI-Ascension/sts2-game-mod/pull/59) `1ec9431de14070f8f94fc281d44b3ae5d41573a0` draft, clean; Rust foundation gates=SUCCESS; policy=SUCCESS; Managed source-only boundary=SUCCESS. [#58](https://github.com/AI-Ascension/sts2-game-mod/pull/58) `f060c564163f36c4a20ab1d5d265bb462d6ab32f` draft, clean; Rust foundation gates=SUCCESS; policy=SUCCESS; Managed source-only boundary=SUCCESS. [#57](https://github.com/AI-Ascension/sts2-game-mod/pull/57) `b5fb4adad3b423c1bad18af9a14404fd8342ac50` draft, dirty; Rust foundation gates=SUCCESS; policy=SUCCESS; Managed source-only boundary=SUCCESS. [#55](https://github.com/AI-Ascension/sts2-game-mod/pull/55) `7cc0af3c64da639b191060251e667782d535bb0c` draft, clean; Rust foundation gates=SUCCESS; policy=SUCCESS; Managed source-only boundary=SUCCESS. [#54](https://github.com/AI-Ascension/sts2-game-mod/pull/54) `089a60dc9f6377cc38b23cfab3b12ad0a00aeef7` draft, dirty; Rust foundation gates=SUCCESS; policy=SUCCESS; Managed source-only boundary=SUCCESS. |
| `sts2-gateway` | [#35](https://github.com/AI-Ascension/sts2-gateway/pull/35) `3faaab4f7479efdd0925eb4ace927c24e6ae33c2` draft, dirty; no hosted checks. [#34](https://github.com/AI-Ascension/sts2-gateway/pull/34) `9713bb9e33c3c294cb8813b7bda7d7c6afc9bdac` draft, dirty; no hosted checks. [#21](https://github.com/AI-Ascension/sts2-gateway/pull/21) `22d780c12c60d8a2e5e1310f57deeea172decbd6` draft, clean; Rust quality gates=SUCCESS; Repository policy=SUCCESS. |
| `sts2-mcp-server` | [#26](https://github.com/AI-Ascension/sts2-mcp-server/pull/26) `6ad97aeead88cdb2097675ddff076bc4bb97529d` draft, clean; Foundation quality gates=SUCCESS; policy=SUCCESS. |
| `sts2-harness` | [#51](https://github.com/AI-Ascension/sts2-harness/pull/51) `38bff93ee63a2e397de7a45cddf716d046684e14` draft, dirty; no hosted checks. [#44](https://github.com/AI-Ascension/sts2-harness/pull/44) `bba4940d9ed2fbfb9213ffc59b707cc34cdbc6d7` ready, unstable; Rust quality gates=IN_PROGRESS; policy=SUCCESS. [#42](https://github.com/AI-Ascension/sts2-harness/pull/42) `91ce16848bc1f094c1bbf243c1131cb932e4c2b5` ready, unstable; Rust quality gates=IN_PROGRESS; policy=SUCCESS. [#40](https://github.com/AI-Ascension/sts2-harness/pull/40) `baabf9767264de11e09cd65cc7262ba36664ec2d` draft, dirty; Rust quality gates=SUCCESS; policy=SUCCESS. [#35](https://github.com/AI-Ascension/sts2-harness/pull/35) `423d9052c8780173e640fa5991e88e8bae282f47` draft, dirty; Rust quality gates=SUCCESS; policy=SUCCESS. [#34](https://github.com/AI-Ascension/sts2-harness/pull/34) `d2105005ebdb6a5f7dd5e266e80b139e294cf89e` draft, clean; Rust quality gates=SUCCESS; policy=SUCCESS. |
| `sts2-protocol` | [#24](https://github.com/AI-Ascension/sts2-protocol/pull/24) `e9199f0706b1629b19efc6d7874d01662b1802b2` draft, dirty; Rust quality gates=SUCCESS; policy=SUCCESS. [#20](https://github.com/AI-Ascension/sts2-protocol/pull/20) `0c39c5a53b005d94df59f14f0962255d0962203a` draft, clean; Rust quality gates=SUCCESS; policy=SUCCESS. |
| `ai-agent-observability` | [#16](https://github.com/AI-Ascension/ai-agent-observability/pull/16) `a126715501d65a2d25f9d6ecf9c6bd142cc5f590` draft, clean; Validate deployment contract=SUCCESS. [#13](https://github.com/AI-Ascension/ai-agent-observability/pull/13) `f872902ed987f5946bf843824063d10884a1bd29` draft, clean; Validate deployment contract=SUCCESS. [#12](https://github.com/AI-Ascension/ai-agent-observability/pull/12) `67f455c0d4aa142139b3942ed0ad56138eecbf8b` draft, clean; Validate deployment contract=SUCCESS. [#10](https://github.com/AI-Ascension/ai-agent-observability/pull/10) `b3a9fa64f51aa249f387190ce76df8c80a02af4b` draft, dirty; Validate deployment contract=SUCCESS. |
| `.github` | [#10](https://github.com/AI-Ascension/.github/pull/10) `d84523795a64556b82d29f6da1dab62eb9b8b4c8` draft, unknown; no hosted checks. |
| `AI-Ascension.github.io` | [#12](https://github.com/AI-Ascension/AI-Ascension.github.io/pull/12) `e5153d6628843bbc734686ae926e143a1cf90526` draft, dirty; static-and-proof=SUCCESS. |

The site PR18 merge remains recorded at [`d5a1145`](https://github.com/AI-Ascension/AI-Ascension.github.io/commit/d5a11452334aab87dfb63986b8c5fe01c9d619b0). Its successful validation run is `34431902416`; its successful GitHub Pages deployment run is `34431902452`; the Pages API reported `built` for `https://ai-ascension.github.io/`. These are static-site deployment observations and do not establish product release or runtime acceptance. The `.github` presentation PR10 remains a separate draft at `d84523795a64556b82d29f6da1dab62eb9b8b4c8`, with no hosted checks, and is not credited to this refresh.

## Latest default-main and pull-request refresh — 2026-09-10, 08:32 UTC

A read-only GitHub CLI API requery ran from `2026-09-10T08:32:26.062924Z` through `2026-09-10T08:32:38.968244Z`, after `sts2-game-mod` PR69 merged. It recorded nine default-main refs and 29 open pull requests. The machine-readable capture is retained in the acceptance handoff as `CURRENT-REMOTE-REFRESH-20260910-r7.json` (SHA-256 `ed2c01dbd939d0f51d8939b30864a05f83edbf30b5fd7e4a40cf5e0b7acb3bda`) and supersedes the 08:09 UTC table above for current repository identity. These are source/component and pull-request records; they do not establish native host legality, settled gameplay, provider execution, observability persistence, deployment, release, or Workshop lifecycle.

| Repository | Current `main` head | Source/component and acceptance boundary |
| --- | --- | --- |
| `sts2-game-core` | [`07b51c88ebe9`](https://github.com/AI-Ascension/sts2-game-core/commit/07b51c88ebe949aec263c130ccc63200e38dfaa7) | Host-independent semantics and tests. |
| `sts2-game-mod` | [`b9754b803cbf`](https://github.com/AI-Ascension/sts2-game-mod/commit/b9754b803cbff79836143d5c115146f65b55184c) | Merged PR69 native co-op host contract and source probes; exact-host loader build, live runtime, and model-controlled action settlement remain unverified. |
| `sts2-gateway` | [`6b6c7f2fac67`](https://github.com/AI-Ascension/sts2-gateway/commit/6b6c7f2fac67de22fdf78c9fd818c6781f689ba0) | Seeded-run gateway source and bounded routes; host settlement and deployment remain unverified. |
| `sts2-mcp-server` | [`73e777b96700`](https://github.com/AI-Ascension/sts2-mcp-server/commit/73e777b96700917cca5ff8f6ce0f5a72009384bc) | Seeded-run transport and gateway mapping source; native MCP-to-game settlement remains unverified. |
| `sts2-harness` | [`33437ddb18f6`](https://github.com/AI-Ascension/sts2-harness/commit/33437ddb18f69f68d88521d947efa3568a32a3bf) | Merged durable recovery and raw action identity plus seeded-run transport/coordinator source; provider execution, native host restart, and gameplay settlement remain unverified. |
| `sts2-protocol` | [`e5e545c2ff71`](https://github.com/AI-Ascension/sts2-protocol/commit/e5e545c2ff7166e073f6d44256016f85d7ea7e83) | Seeded-run protocol contract source, schemas, artifacts, validators, and conformance cases. |
| `ai-agent-observability` | [`28a48590afb7`](https://github.com/AI-Ascension/ai-agent-observability/commit/28a48590afb75b07590e1b78ea47dae08f5c3ade) | Source topology and deployment tooling; current-main gameplay ingestion, persistence, and two-backend correlation remain unverified. |
| `.github` | [`c0049783d665`](https://github.com/AI-Ascension/.github/commit/c0049783d665a6ffcde1d47d3777d059e935a9be) | Governance and acceptance status records; no metadata, deployment, or release change is implied. |
| `AI-Ascension.github.io` | [`d0d8087e80c9`](https://github.com/AI-Ascension/AI-Ascension.github.io/commit/d0d8087e80c974a8901d0e85bc192652faeb6d42) | Merged static evidence and repository pages; Pages deployment is separately reported and runtime/release evidence remain unverified. |

Game-mod PR [#69](https://github.com/AI-Ascension/sts2-game-mod/pull/69) merged at `2026-09-10T08:31:03Z` as [`b9754b803cbf`](https://github.com/AI-Ascension/sts2-game-mod/commit/b9754b803cbff79836143d5c115146f65b55184c) from head `ab702dbbc79bc5854bd0840b44a729834ae50e68`. Its Rust foundation, policy, and managed source-only checks succeeded. The PR describes native host contracts and source probes; its exact-host loader build and live runtime remain separate gates, and it claims no live two-peer host/client run, model-controlled action settlement, vote convergence, native checksum settlement, or disconnect/rejoin trace.

The native candidate cleanup remains storage evidence only. Native installation/loading, provider settlement, model-played terminal gameplay, and multiplayer actions or recovery remain unverified. The release boundary remains unverified: current source and checks do not establish a final installable artifact, clean-install/update/rollback compatibility, Workshop agreement/item/content/update/rollback lifecycle, or a public release. The observability boundary remains unverified: current-main source and tooling do not establish gameplay ingestion, persistence, or correlation in both backends. Site PR19 is merged at [`d0d8087e80c9`](https://github.com/AI-Ascension/AI-Ascension.github.io/commit/d0d8087e80c974a8901d0e85bc192652faeb6d42); validation and Pages deployment succeeded, and the Pages API reports `built`.

The 29 open pull requests at capture were:

| Repository | Open PRs — exact head, state, merge state, and checks at capture |
| --- | --- |
| `sts2-game-core` | [#9](https://github.com/AI-Ascension/sts2-game-core/pull/9) `9a27a80c32dcadd8030cf42c861e9e5da4daed1c` draft, clean, mergeable; Rust quality gates=SUCCESS; policy=SUCCESS. |
| `sts2-game-mod` | [#65](https://github.com/AI-Ascension/sts2-game-mod/pull/65) `57cee12eab5f6af6ebb4325979e7d2df64c501a0` ready, unknown, unknown; Rust foundation gates=FAILURE; policy=SUCCESS; Managed source-only boundary=SUCCESS. [#63](https://github.com/AI-Ascension/sts2-game-mod/pull/63) `ad9278512563d4a319177d4c10654ceec696c78c` draft, clean, mergeable; Rust foundation gates=SUCCESS; policy=SUCCESS; Managed source-only boundary=SUCCESS. [#59](https://github.com/AI-Ascension/sts2-game-mod/pull/59) `1ec9431de14070f8f94fc281d44b3ae5d41573a0` draft, clean, mergeable; Rust foundation gates=SUCCESS; policy=SUCCESS; Managed source-only boundary=SUCCESS. [#58](https://github.com/AI-Ascension/sts2-game-mod/pull/58) `f060c564163f36c4a20ab1d5d265bb462d6ab32f` draft, clean, mergeable; Rust foundation gates=SUCCESS; policy=SUCCESS; Managed source-only boundary=SUCCESS. [#57](https://github.com/AI-Ascension/sts2-game-mod/pull/57) `b5fb4adad3b423c1bad18af9a14404fd8342ac50` draft, unknown, unknown; Rust foundation gates=SUCCESS; policy=SUCCESS; Managed source-only boundary=SUCCESS. [#55](https://github.com/AI-Ascension/sts2-game-mod/pull/55) `7cc0af3c64da639b191060251e667782d535bb0c` draft, unknown, unknown; Rust foundation gates=SUCCESS; policy=SUCCESS; Managed source-only boundary=SUCCESS. [#54](https://github.com/AI-Ascension/sts2-game-mod/pull/54) `089a60dc9f6377cc38b23cfab3b12ad0a00aeef7` draft, unknown, unknown; Rust foundation gates=SUCCESS; policy=SUCCESS; Managed source-only boundary=SUCCESS. |
| `sts2-gateway` | [#36](https://github.com/AI-Ascension/sts2-gateway/pull/36) `e5543403e7ac0fa13929c296adfab877bea4212a` draft, clean, mergeable; Rust quality gates=SUCCESS; Repository policy=SUCCESS. [#35](https://github.com/AI-Ascension/sts2-gateway/pull/35) `8ce3f78bf8b0f0970b5c6a47f7d46e5010c05711` draft, clean, mergeable; Rust quality gates=SUCCESS; Repository policy=SUCCESS. [#34](https://github.com/AI-Ascension/sts2-gateway/pull/34) `9713bb9e33c3c294cb8813b7bda7d7c6afc9bdac` draft, dirty, conflicting; no hosted checks. [#21](https://github.com/AI-Ascension/sts2-gateway/pull/21) `22d780c12c60d8a2e5e1310f57deeea172decbd6` draft, clean, mergeable; Rust quality gates=SUCCESS; Repository policy=SUCCESS. |
| `sts2-mcp-server` | [#26](https://github.com/AI-Ascension/sts2-mcp-server/pull/26) `6ad97aeead88cdb2097675ddff076bc4bb97529d` draft, clean, mergeable; Foundation quality gates=SUCCESS; policy=SUCCESS. |
| `sts2-harness` | [#52](https://github.com/AI-Ascension/sts2-harness/pull/52) `623848ed6dc8b2bbfa07cd287df7aa4feba18c87` draft, dirty, conflicting; no hosted checks. [#51](https://github.com/AI-Ascension/sts2-harness/pull/51) `b905429a2d0c0890b0bf7fcc4568467126df519d` draft, dirty, conflicting; no hosted checks. [#44](https://github.com/AI-Ascension/sts2-harness/pull/44) `bba4940d9ed2fbfb9213ffc59b707cc34cdbc6d7` ready, unstable, mergeable; Rust quality gates=FAILURE; policy=SUCCESS. [#42](https://github.com/AI-Ascension/sts2-harness/pull/42) `91ce16848bc1f094c1bbf243c1131cb932e4c2b5` ready, unstable, mergeable; Rust quality gates=FAILURE; policy=SUCCESS. [#40](https://github.com/AI-Ascension/sts2-harness/pull/40) `baabf9767264de11e09cd65cc7262ba36664ec2d` draft, dirty, conflicting; Rust quality gates=SUCCESS; policy=SUCCESS. [#35](https://github.com/AI-Ascension/sts2-harness/pull/35) `423d9052c8780173e640fa5991e88e8bae282f47` draft, dirty, conflicting; Rust quality gates=SUCCESS; policy=SUCCESS. [#34](https://github.com/AI-Ascension/sts2-harness/pull/34) `d2105005ebdb6a5f7dd5e266e80b139e294cf89e` draft, clean, mergeable; Rust quality gates=SUCCESS; policy=SUCCESS. |
| `sts2-protocol` | [#31](https://github.com/AI-Ascension/sts2-protocol/pull/31) `5e43193cb5da17a5b772caa0f0fff49180cf716d` draft, clean, mergeable; Rust quality gates=SUCCESS; policy=SUCCESS. [#24](https://github.com/AI-Ascension/sts2-protocol/pull/24) `e9199f0706b1629b19efc6d7874d01662b1802b2` draft, dirty, conflicting; Rust quality gates=SUCCESS; policy=SUCCESS. [#20](https://github.com/AI-Ascension/sts2-protocol/pull/20) `0c39c5a53b005d94df59f14f0962255d0962203a` draft, clean, mergeable; Rust quality gates=SUCCESS; policy=SUCCESS. |
| `ai-agent-observability` | [#16](https://github.com/AI-Ascension/ai-agent-observability/pull/16) `a126715501d65a2d25f9d6ecf9c6bd142cc5f590` draft, clean, mergeable; Validate deployment contract=SUCCESS. [#13](https://github.com/AI-Ascension/ai-agent-observability/pull/13) `f872902ed987f5946bf843824063d10884a1bd29` draft, clean, mergeable; Validate deployment contract=SUCCESS. [#12](https://github.com/AI-Ascension/ai-agent-observability/pull/12) `67f455c0d4aa142139b3942ed0ad56138eecbf8b` draft, clean, mergeable; Validate deployment contract=SUCCESS. [#10](https://github.com/AI-Ascension/ai-agent-observability/pull/10) `b3a9fa64f51aa249f387190ce76df8c80a02af4b` draft, dirty, conflicting; Validate deployment contract=SUCCESS. |
| `.github` | [#10](https://github.com/AI-Ascension/.github/pull/10) `d84523795a64556b82d29f6da1dab62eb9b8b4c8` draft, unknown, unknown; no hosted checks. |
| `AI-Ascension.github.io` | [#12](https://github.com/AI-Ascension/AI-Ascension.github.io/pull/12) `e5153d6628843bbc734686ae926e143a1cf90526` draft, unknown, unknown; static-and-proof=SUCCESS. |
## Latest acceptance snapshot — 2026-09-10, 15:34–15:38 UTC

This `confirmed` snapshot is a read-only refresh of the nine default branches and the public
Pages result. It records exact source identities and named check runs at capture time. The
source and check records are separate from host legality, model/provider execution, settled
gameplay, observability persistence, Workshop publication, and release acceptance.

| Repository | Current `main` head (`confirmed`) | Checks observed (`confirmed`) | Source boundary (`source-derived`) |
| --- | --- | --- | --- |
| `sts2-game-core` | [`f9db577`](https://github.com/AI-Ascension/sts2-game-core/commit/f9db577530a4d159b066d3facbd780d61c044eb0) | [CI 34494626667](https://github.com/AI-Ascension/sts2-game-core/actions/runs/34494626667), [policy 34494626737](https://github.com/AI-Ascension/sts2-game-core/actions/runs/34494626737) | Host-independent semantics and tests; no host or game claim. |
| `sts2-game-mod` | [`e532f4d`](https://github.com/AI-Ascension/sts2-game-mod/commit/e532f4d9186e367bd3dc045d2377a2bd3ac9e4e5) | [CI 34491827942](https://github.com/AI-Ascension/sts2-game-mod/actions/runs/34491827942), [policy 34491828082](https://github.com/AI-Ascension/sts2-game-mod/actions/runs/34491828082) | Managed/native adapter source and probes; exact-host loading and settled gameplay remain `unverified`. |
| `sts2-gateway` | [`2cf9127`](https://github.com/AI-Ascension/sts2-gateway/commit/2cf9127bfe5b7f1f271dd1b2889d92a09f042f83) | [CI 34494472113](https://github.com/AI-Ascension/sts2-gateway/actions/runs/34494472113), [policy 34494472141](https://github.com/AI-Ascension/sts2-gateway/actions/runs/34494472141) | Bounded gateway/control-plane source; host settlement and deployment remain `unverified`. |
| `sts2-mcp-server` | [`8b6b738`](https://github.com/AI-Ascension/sts2-mcp-server/commit/8b6b73862494488fdd16fa5423fdf90a953260f4) | [CI 34494670041](https://github.com/AI-Ascension/sts2-mcp-server/actions/runs/34494670041), [policy 34494670273](https://github.com/AI-Ascension/sts2-mcp-server/actions/runs/34494670273) | Transport and gateway mapping source; native game settlement remains `unverified`. |
| `sts2-harness` | [`e5029f1`](https://github.com/AI-Ascension/sts2-harness/commit/e5029f1023f8a4df676e537298b1efc19ef00e6c) | [CI 34492899631](https://github.com/AI-Ascension/sts2-harness/actions/runs/34492899631), [policy 34492899599](https://github.com/AI-Ascension/sts2-harness/actions/runs/34492899599) | Coordinator, record/replay, and transport source; provider execution, worker acceptance, native restart, and gameplay settlement remain `unverified`. |
| `sts2-protocol` | [`997de2a`](https://github.com/AI-Ascension/sts2-protocol/commit/997de2aec7590dc0f362dce71814431add624e98) | [CI 34492025822](https://github.com/AI-Ascension/sts2-protocol/actions/runs/34492025822), [policy 34492025836](https://github.com/AI-Ascension/sts2-protocol/actions/runs/34492025836) | Schemas, artifacts, validators, and conformance source; native co-op consumer admission remains `unverified`. |
| `ai-agent-observability` | [`d7e79e1`](https://github.com/AI-Ascension/ai-agent-observability/commit/d7e79e1a9663601013e513048caea7063b0de9ae) | [CI 34493891085](https://github.com/AI-Ascension/ai-agent-observability/actions/runs/34493891085) | Telemetry topology and deployment tooling; live ingestion, query, persistence, and two-backend correlation remain `unverified`. |
| `.github` | [`fec27b9`](https://github.com/AI-Ascension/.github/commit/fec27b97b5920466aaebe2b97c8a54ab71468cda) | No hosted check recorded for this governance repository in this refresh. | Governance and acceptance records only; no metadata, deployment, or release change is implied. |
| `AI-Ascension.github.io` | [`3935679`](https://github.com/AI-Ascension/AI-Ascension.github.io/commit/3935679ceb378da60237e764ec615a8eb2b05527) | [site validation 34495457608](https://github.com/AI-Ascension/AI-Ascension.github.io/actions/runs/34495457608), [Pages deploy 34495457785](https://github.com/AI-Ascension/AI-Ascension.github.io/actions/runs/34495457785) | Static evidence pages; Pages publication is confirmed separately and does not establish product runtime or release. |

### Acceptance boundaries

- `unverified` **Model-played terminal evidence:** no model-controlled Victory or replay of a
  model-controlled Victory is recorded. The named Windows and Linux replays are bounded Defeat
  campaigns; forced Victory fixtures bypass ordinary play and do not establish a model-played
  Victory.
- `unverified` **Native co-op settlement and recovery:** no live two-peer model-controlled action,
  vote convergence, shared effect, checksum settlement, or disconnect/rejoin recovery trace is
  recorded. Game-mod PR #69 added contracts and probes at source level; the current gateway, MCP,
  and harness records do not establish an admitted native co-op consumer path. The read-only
  coordinator synchronization profile has no native peer or game authority.
- `confirmed` **Observability query boundary:** MLflow returned HTTP 200 for a failed run containing
  124 spans but no terminal outcome. Laminar health returned HTTP 200, while its query returned
  HTTP 401 with zero rows/pages. No controlled-restart persistence result is recorded. `unverified`
  acceptance therefore still needs rootful Podman/host access and a separate valid Laminar
  operator credential/path, followed by real terminal campaign queries before and after restart.
  Observability issue #8 is closed; that closure does not prove operator query access.
- `confirmed` **Release inventory:** the read-only release inventory found zero tags and zero GitHub
  releases across all nine repositories at this capture. No public release is established.
- `unverified` **Workshop lifecycle:** the game-mod package validators and staging sources do not
  establish an uploaded Workshop item. Steam legal agreement acceptance, entitlement, item and
  content visibility, subscription/discovery/loading, update, and rollback remain unverified.

### Harness worker source boundary

`confirmed` source inspection at `sts2-harness@e5029f1` found no `mod worker_command` or
`mod worker_runtime` declaration in [`crates/harness/src/lib.rs`](https://github.com/AI-Ascension/sts2-harness/blob/e5029f1023f8a4df676e537298b1efc19ef00e6c/crates/harness/src/lib.rs#L3-L31).
The tree contains `worker_command.rs`, `worker_runtime.rs`, and worker tests, but those files are
not compiled through the crate root. `worker_command.rs` references missing operation/support
modules, and `worker_runtime.rs` references missing handoff/store and completion/execution/control
test modules. Worker acceptance is therefore `unverified` until the complete module graph is
wired and tested or the superseded files are removed or archived.

### Pages publication

`confirmed`: the site `main` head is
[`3935679`](https://github.com/AI-Ascension/AI-Ascension.github.io/commit/3935679ceb378da60237e764ec615a8eb2b05527).
Site validation run [34495457608](https://github.com/AI-Ascension/AI-Ascension.github.io/actions/runs/34495457608)
and Pages deployment run [34495457785](https://github.com/AI-Ascension/AI-Ascension.github.io/actions/runs/34495457785)
succeeded; the Pages API reported `built` for `https://ai-ascension.github.io/`, and a live request
returned HTTP 200. The deployed evidence page still displayed the older 08:32 source snapshot at
capture, so this is static-site publication evidence only.

## Latest acceptance successor — 2026-09-10, 15:54+ UTC

This `confirmed` read-only refresh supersedes the 15:34–15:38 UTC table for current default-branch
identity while preserving that earlier snapshot above as history. It rechecked all nine default
branches, their latest completed hosted checks, release/tag counts, and the current Pages
publication result. Source and check records remain separate from native host legality,
model/provider execution, settled gameplay, observability persistence, Workshop publication, and
release acceptance.

| Repository | Current `main` head (`confirmed`) | Checks observed (`confirmed`) | Source boundary (`source-derived`) |
| --- | --- | --- | --- |
| `sts2-game-core` | [`f9db577`](https://github.com/AI-Ascension/sts2-game-core/commit/f9db577530a4d159b066d3facbd780d61c044eb0) | [CI 34494626667](https://github.com/AI-Ascension/sts2-game-core/actions/runs/34494626667), [policy 34494626737](https://github.com/AI-Ascension/sts2-game-core/actions/runs/34494626737) passed | Host-independent semantics and tests; no host or game claim. |
| `sts2-game-mod` | [`a70a5e5`](https://github.com/AI-Ascension/sts2-game-mod/commit/a70a5e5bb2fa89fade7e16dbb4a58ed80e31355b) | [CI 34498220756](https://github.com/AI-Ascension/sts2-game-mod/actions/runs/34498220756), [policy 34498220893](https://github.com/AI-Ascension/sts2-game-mod/actions/runs/34498220893) passed | PR #71 release source-policy and copied REST artifact parity merge; host loading and settled gameplay remain `unverified`. |
| `sts2-gateway` | [`2cf9127`](https://github.com/AI-Ascension/sts2-gateway/commit/2cf9127bfe5b7f1f271dd1b2889d92a09f042f83) | [CI 34494472113](https://github.com/AI-Ascension/sts2-gateway/actions/runs/34494472113), [policy 34494472141](https://github.com/AI-Ascension/sts2-gateway/actions/runs/34494472141) passed | Bounded gateway/control-plane source; host settlement and deployment remain `unverified`. |
| `sts2-mcp-server` | [`8b6b738`](https://github.com/AI-Ascension/sts2-mcp-server/commit/8b6b73862494488fdd16fa5423fdf90a953260f4) | [CI 34494670041](https://github.com/AI-Ascension/sts2-mcp-server/actions/runs/34494670041), [policy 34494670273](https://github.com/AI-Ascension/sts2-mcp-server/actions/runs/34494670273) passed | Transport and gateway mapping source; native game settlement remains `unverified`. |
| `sts2-harness` | [`4342789`](https://github.com/AI-Ascension/sts2-harness/commit/4342789de4bf5a5f23aee85be273db9a263c9c31) | [CI 34498649592](https://github.com/AI-Ascension/sts2-harness/actions/runs/34498649592), [policy 34498649531](https://github.com/AI-Ascension/sts2-harness/actions/runs/34498649531) passed | PR #58 worker handoff/runtime/store graph, schema, fixtures, and restart/recovery tests are wired at source/component level; native worker execution and gameplay settlement remain `unverified`. |
| `sts2-protocol` | [`997de2a`](https://github.com/AI-Ascension/sts2-protocol/commit/997de2aec7590dc0f362dce71814431add624e98) | [CI 34492025822](https://github.com/AI-Ascension/sts2-protocol/actions/runs/34492025822), [policy 34492025836](https://github.com/AI-Ascension/sts2-protocol/actions/runs/34492025836) passed | Schemas, artifacts, validators, and conformance source; native co-op consumer admission remains `unverified`. |
| `ai-agent-observability` | [`d7e79e1`](https://github.com/AI-Ascension/ai-agent-observability/commit/d7e79e1a9663601013e513048caea7063b0de9ae) | [CI 34493891085](https://github.com/AI-Ascension/ai-agent-observability/actions/runs/34493891085) passed | Telemetry topology and deployment tooling; live ingestion, query, persistence, and two-backend correlation remain `unverified`. |
| `.github` | [`309df81`](https://github.com/AI-Ascension/.github/commit/309df810983d18d8221712b92012e7a8fd0dd8cc) | No hosted check recorded for this governance repository in this refresh. | Governance and acceptance records only; no metadata, deployment, or release change is implied. |
| `AI-Ascension.github.io` | [`a451a70`](https://github.com/AI-Ascension/AI-Ascension.github.io/commit/a451a700d52befa73499c09bb4bc6ae4878d2cde) | [site validation 34498420048](https://github.com/AI-Ascension/AI-Ascension.github.io/actions/runs/34498420048), [Pages deploy 34498419971](https://github.com/AI-Ascension/AI-Ascension.github.io/actions/runs/34498419971) passed | Static evidence pages; Pages publication is confirmed separately and does not establish product runtime or release. |

### Merged source/component updates

- `confirmed` **Game-mod PR #71:** [PR #71](https://github.com/AI-Ascension/sts2-game-mod/pull/71) merged
  at [`a70a5e5`](https://github.com/AI-Ascension/sts2-game-mod/commit/a70a5e5bb2fa89fade7e16dbb4a58ed80e31355b)
  from head `2e70efee` on base `e532f4d`. It closes the current-main source-distribution policy
  gap and restores parity between the copied `runtime-v4-expert-rest-action` README/SHA256SUMS
  and canonical `sts2-protocol@997de2a`. This is source/release-policy evidence; it does not
  establish a final release, host compatibility, Steam publication, or Workshop upload.
- `confirmed` **Harness PR #58:** [PR #58](https://github.com/AI-Ascension/sts2-harness/pull/58) merged
  at [`4342789`](https://github.com/AI-Ascension/sts2-harness/commit/4342789de4bf5a5f23aee85be273db9a263c9c31)
  from head `ed033f26` on base `e5029f1`. The crate root now wires
  [`worker_handoff`](https://github.com/AI-Ascension/sts2-harness/blob/4342789de4bf5a5f23aee85be273db9a263c9c31/crates/harness/src/lib.rs#L32-L34),
  `worker_runtime`, and `worker_runtime_store`; the merge also adds the watchdog-worker-v1
  schema, manifest, valid/invalid fixtures, authenticated command mapping, and restart/recovery
  regressions. This is source/component and CI evidence; it does not establish native worker
  execution, provider execution, host restart, or gameplay settlement.

### Acceptance boundaries

- `unverified` **Model-played terminal evidence:** no model-controlled Victory or replay of a
  model-controlled Victory is recorded. The named Windows and Linux replays are bounded Defeat
  campaigns; forced Victory fixtures bypass ordinary play and do not establish a model-played
  Victory.
- `unverified` **Native co-op settlement and recovery:** no live two-peer model-controlled action,
  vote convergence, shared effect, checksum settlement, or disconnect/rejoin recovery trace is
  recorded. Current source and synchronization records do not establish an admitted native co-op
  consumer path.
- `confirmed` **Observability query boundary:** MLflow returned HTTP 200 for a failed run containing
  124 spans but no terminal outcome. Laminar health returned HTTP 200, while its query returned
  HTTP 401 with zero rows/pages. No controlled-restart persistence result is recorded. `unverified`
  acceptance still needs rootful Podman/host access and a valid Laminar operator credential/path,
  followed by real terminal campaign queries before and after restart.
- `confirmed` **Release inventory:** the read-only refresh found zero tags and zero GitHub releases
  across all nine repositories at capture. No public release is established.
- `unverified` **Workshop lifecycle:** package validators and staging sources do not establish an
  uploaded Workshop item. Steam legal agreement acceptance, entitlement, item and content
  visibility, subscription/discovery/loading, update, and rollback remain unverified.

### Pages publication

`confirmed`: site `main` is [`a451a70`](https://github.com/AI-Ascension/AI-Ascension.github.io/commit/a451a700d52befa73499c09bb4bc6ae4878d2cde).
Site validation run [34498420048](https://github.com/AI-Ascension/AI-Ascension.github.io/actions/runs/34498420048)
and Pages deployment run [34498419971](https://github.com/AI-Ascension/AI-Ascension.github.io/actions/runs/34498419971)
succeeded. The Pages deployment record `6375647948` reached `success` for
`https://ai-ascension.github.io/`; this is static publication evidence only. The successor
documentation in this draft branch is not deployed until its PR is merged.

## Latest acceptance successor — 2026-09-10, 16:13 UTC (post-16:03 merge)

This `confirmed` read-only refresh follows the merge of harness PR #51 at
`2026-09-10T16:03:56Z`. It supersedes the 15:54+ table above only for current
default-branch identity and preserves that table as history. The refresh rechecked
all nine default branches and their latest completed hosted checks. Source and check
records remain separate from native host legality, model/provider execution, settled
gameplay, observability persistence, Workshop publication, and release acceptance.

| Repository | Current `main` head (`confirmed`) | Checks observed (`confirmed`) | Source boundary (`source-derived`) |
| --- | --- | --- | --- |
| `sts2-game-core` | [`f9db577`](https://github.com/AI-Ascension/sts2-game-core/commit/f9db577530a4d159b066d3facbd780d61c044eb0) | [CI 34494626667](https://github.com/AI-Ascension/sts2-game-core/actions/runs/34494626667), [policy 34494626737](https://github.com/AI-Ascension/sts2-game-core/actions/runs/34494626737) passed | Host-independent semantics and tests; no host or game claim. |
| `sts2-game-mod` | [`a70a5e5`](https://github.com/AI-Ascension/sts2-game-mod/commit/a70a5e5bb2fa89fade7e16dbb4a58ed80e31355b) | [CI 34498220756](https://github.com/AI-Ascension/sts2-game-mod/actions/runs/34498220756), [policy 34498220893](https://github.com/AI-Ascension/sts2-game-mod/actions/runs/34498220893) passed | PR #71 source-policy and copied REST artifact parity merge; host loading and settled gameplay remain `unverified`. |
| `sts2-gateway` | [`2cf9127`](https://github.com/AI-Ascension/sts2-gateway/commit/2cf9127bfe5b7f1f271dd1b2889d92a09f042f83) | [CI 34494472113](https://github.com/AI-Ascension/sts2-gateway/actions/runs/34494472113), [policy 34494472141](https://github.com/AI-Ascension/sts2-gateway/actions/runs/34494472141) passed | Bounded gateway/control-plane source; host settlement and deployment remain `unverified`. |
| `sts2-mcp-server` | [`8b6b738`](https://github.com/AI-Ascension/sts2-mcp-server/commit/8b6b73862494488fdd16fa5423fdf90a953260f4) | [CI 34494670041](https://github.com/AI-Ascension/sts2-mcp-server/actions/runs/34494670041), [policy 34494670273](https://github.com/AI-Ascension/sts2-mcp-server/actions/runs/34494670273) passed | Transport and gateway mapping source; native game settlement remains `unverified`. |
| `sts2-harness` | [`780f2d5`](https://github.com/AI-Ascension/sts2-harness/commit/780f2d521508a2aadc76c4d779544d967955f102) | PR #51 [CI 34499698232](https://github.com/AI-Ascension/sts2-harness/actions/runs/34499698232) and [policy 34499698312](https://github.com/AI-Ascension/sts2-harness/actions/runs/34499698312), then main [CI 34499708670](https://github.com/AI-Ascension/sts2-harness/actions/runs/34499708670) and [policy 34499708793](https://github.com/AI-Ascension/sts2-harness/actions/runs/34499708793), passed | PR #51 context-capture source/component wiring; native provider receipt, worker execution, host behavior, and gameplay settlement remain `unverified`. |
| `sts2-protocol` | [`997de2a`](https://github.com/AI-Ascension/sts2-protocol/commit/997de2aec7590dc0f362dce71814431add624e98) | [CI 34492025822](https://github.com/AI-Ascension/sts2-protocol/actions/runs/34492025822), [policy 34492025836](https://github.com/AI-Ascension/sts2-protocol/actions/runs/34492025836) passed | Schemas, artifacts, validators, and conformance source; native co-op consumer admission remains `unverified`. |
| `ai-agent-observability` | [`d7e79e1`](https://github.com/AI-Ascension/ai-agent-observability/commit/d7e79e1a9663601013e513048caea7063b0de9ae) | [CI 34493891085](https://github.com/AI-Ascension/ai-agent-observability/actions/runs/34493891085) passed | Telemetry topology and deployment tooling; live ingestion, query, persistence, and two-backend correlation remain `unverified`. |
| `.github` | [`c2b1771`](https://github.com/AI-Ascension/.github/commit/c2b17712e3d88b0e291893d067c809ff5c7fc426) | No hosted check recorded for this governance repository in this refresh. | Governance and acceptance records only; no metadata, deployment, or release change is implied. |
| `AI-Ascension.github.io` | [`457f002`](https://github.com/AI-Ascension/AI-Ascension.github.io/commit/457f0027981a16ffe223767fb78acaf4be591790) | [site validation 34499991425](https://github.com/AI-Ascension/AI-Ascension.github.io/actions/runs/34499991425), [Pages deploy 34499991509](https://github.com/AI-Ascension/AI-Ascension.github.io/actions/runs/34499991509) passed | Static evidence pages; Pages publication is confirmed separately and does not establish product runtime or release. |

### Harness PR #51 source/component boundary

`confirmed` **Harness PR #51:** [PR #51](https://github.com/AI-Ascension/sts2-harness/pull/51)
merged at [`780f2d5`](https://github.com/AI-Ascension/sts2-harness/commit/780f2d521508a2aadc76c4d779544d967955f102)
from head `280fd39` on base [`4342789`](https://github.com/AI-Ascension/sts2-harness/commit/4342789de4bf5a5f23aee85be273db9a263c9c31).
It adds bounded `CapturePort` modes and identities, ordered component manifests,
lifecycle capture, queue/private-vault gates, and parity/failure-fidelity tests; the
capture path is wired through direct `ExoSession::decide`, the generic `ProviderPort`
route, Astra's final CLI handoff, and Ollama's final serialized HTTP write. A successful
outbound body write is recorded as completion; response, malformed, timeout, and
partial-write failures remain indeterminate and are not receipts. The PR checks and
post-merge main checks passed. The PR body also records its final validation at
[`f95e8bc`](https://github.com/AI-Ascension/sts2-harness/commit/f95e8bcf1d248837dc983537a45335a036f3560e),
production capture source [`316c8bd`](https://github.com/AI-Ascension/sts2-harness/commit/316c8bd1814d9f9762a08c534898ec827365c91a),
and fidelity artifact SHA-256 `2b6b8dd5509801fe0e9d104cb97f669d59c6f0ac302ac5b19da116334fcbbcd6`.
Those are source/component and synthetic differential evidence. No real provider, game, or external service was called; the fake downstream
comparisons do not establish a provider receipt, game action, browser run, native
platform behavior, or an integrated producer/store demonstration. The native preflight
reached root → lead only; coordinator/specialist ancestry remains `unverified` because
the child had no collaboration tools.

### Acceptance boundaries

- `unverified` **Model-played terminal evidence:** no model-controlled Victory or replay of a
  model-controlled Victory is recorded. The named Windows and Linux replays are bounded Defeat
  campaigns; forced Victory fixtures bypass ordinary play and do not establish a model-played
  Victory.
- `unverified` **Native co-op settlement and recovery:** no live two-peer model-controlled action,
  vote convergence, shared effect, checksum settlement, or disconnect/rejoin recovery trace is
  recorded. Current source and synchronization records do not establish an admitted native co-op
  consumer path.
- `confirmed` **Observability query boundary:** MLflow returned HTTP 200 for a failed run containing
  124 spans but no terminal outcome. Laminar health returned HTTP 200, while its query returned
  HTTP 401 with zero rows/pages. No controlled-restart persistence result is recorded. `unverified`
  acceptance still needs rootful Podman/host access and a valid Laminar operator credential/path,
  followed by real terminal campaign queries before and after restart.
- `confirmed` **Release inventory:** the read-only refresh found zero tags and zero GitHub releases
  across all nine repositories at capture. No public release is established.
- `unverified` **Workshop lifecycle:** package validators and staging sources do not establish an
  uploaded Workshop item. Steam legal agreement acceptance, entitlement, item and content
  visibility, subscription/discovery/loading, update, and rollback remain unverified.

### Pages publication

At this capture, site `main` was [`457f002`](https://github.com/AI-Ascension/AI-Ascension.github.io/commit/457f0027981a16ffe223767fb78acaf4be591790).
Site validation run [34499991425](https://github.com/AI-Ascension/AI-Ascension.github.io/actions/runs/34499991425)
and Pages deployment run [34499991509](https://github.com/AI-Ascension/AI-Ascension.github.io/actions/runs/34499991509)
succeeded. Deployment `6375923984` reached `success`; a live request to
`https://ai-ascension.github.io/evidence.html` returned HTTP 200 with SHA-256
`e67ec29a894e37194e6d93fe298107013ecdac797f261975f325566452dfbf3a` and the 15:54,
`a70a5e5`, and `4342789` markers. This is static publication evidence only; the r10
successor documentation is not deployed until its site PR merges.
