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
