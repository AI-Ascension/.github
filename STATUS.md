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
The initial stack heads remain recorded in the table below. Two later source-only follow-ups corrected
function-budget findings in the game-mod and harness; the current default-branch pointers after those
follow-ups are recorded in the next table.

| Component | Default-branch source after the merge | Runtime-v3 position merged |
| --- | --- | --- |
| Protocol | [`4bfc120`](https://github.com/AI-Ascension/sts2-protocol/tree/4bfc120d4221182ca3e80bed0174fb787b6b4690) | 1/6 — `sts2-protocol#8` |
| Game-core | [`87e0f3d`](https://github.com/AI-Ascension/sts2-game-core/tree/87e0f3d9355c0827e989d9fbc31804440852519b) | 2/6 — `sts2-game-core#6` |
| Game-mod | [`7aa51ee`](https://github.com/AI-Ascension/sts2-game-mod/tree/7aa51ee003f5b69ff36e7ba9951f3d58fb8bb162) | 3/6 — `sts2-game-mod#15` |
| Gateway | [`52bd147`](https://github.com/AI-Ascension/sts2-gateway/tree/52bd147667667d62d8d10c7de861d996f365600b) | 4/6 — `sts2-gateway#7` |
| MCP adapter | [`b3684bf`](https://github.com/AI-Ascension/sts2-mcp-server/tree/b3684bf005f09622c39b154b4c081e867105edcf) | 5/6 — `sts2-mcp-server#8` |
| Harness | [`ffa2564`](https://github.com/AI-Ascension/sts2-harness/tree/ffa2564836c7364ab1692cc81307e1bdecff428a) | 6/6 — `sts2-harness#10` |

### Current default heads after source-only budget follow-ups

These are the current `source-derived` default-branch pointers. The follow-up changes preserve the
Runtime-v3 wire fields, validation behavior, artifact bytes, and evidence boundary; they only split
functions by responsibility and document those boundaries.

| Component | Current default-branch source | Initial lane and follow-up |
| --- | --- | --- |
| Protocol | [`4bfc120`](https://github.com/AI-Ascension/sts2-protocol/tree/4bfc120d4221182ca3e80bed0174fb787b6b4690) | 1/6 — `sts2-protocol#8`; no budget follow-up |
| Game-core | [`87e0f3d`](https://github.com/AI-Ascension/sts2-game-core/tree/87e0f3d9355c0827e989d9fbc31804440852519b) | 2/6 — `sts2-game-core#6`; no budget follow-up |
| Game-mod | [`f9b81f4`](https://github.com/AI-Ascension/sts2-game-mod/tree/f9b81f4759d23419278af93d7656aacba9bc2adc) | 3/6 — `#15`; source-only function-budget correction [`#27`](https://github.com/AI-Ascension/sts2-game-mod/pull/27) at [`bc46e44`](https://github.com/AI-Ascension/sts2-game-mod/tree/bc46e44337b459c5a0aeada5abab72cd78244a41); current corrections [`#28`](https://github.com/AI-Ascension/sts2-game-mod/pull/28) and [`#29`](https://github.com/AI-Ascension/sts2-game-mod/pull/29) |
| Gateway | [`52bd147`](https://github.com/AI-Ascension/sts2-gateway/tree/52bd147667667d62d8d10c7de861d996f365600b) | 4/6 — `sts2-gateway#7`; no budget follow-up |
| MCP adapter | [`b3684bf`](https://github.com/AI-Ascension/sts2-mcp-server/tree/b3684bf005f09622c39b154b4c081e867105edcf) | 5/6 — `sts2-mcp-server#8`; no budget follow-up |
| Harness | [`3b9a70f`](https://github.com/AI-Ascension/sts2-harness/tree/3b9a70fdf07467498cdce1556177258ed7dc4a45) | 6/6 — `#10`, then source-only function-budget correction [`#19`](https://github.com/AI-Ascension/sts2-harness/pull/19) |

The game-mod follow-up reports 17 changed or new members with a maximum of 57 nonblank lines;
the harness follow-up reports 529 changed or new functions with a maximum of 58 nonblank lines.
Both report zero changed functions over 60 or 80 lines, and their repository policy, formatting,
Clippy, tests, artifact checks, and applicable source-only checks passed. These are source and
static-test results; they do not establish host loading or gameplay.

### Game-mod corrections — 2026-09-05

The current game-mod default branch is [`f9b81f4`](https://github.com/AI-Ascension/sts2-game-mod/tree/f9b81f4759d23419278af93d7656aacba9bc2adc),
which includes two additional source-only corrections after the function-budget follow-up:

- [`sts2-game-mod#28`](https://github.com/AI-Ascension/sts2-game-mod/pull/28), merged at
  [`8dca989`](https://github.com/AI-Ascension/sts2-game-mod/commit/8dca98904464b5b47dec5de88518e6c237fafad7),
  adds the missing Runtime-v2 `SHA256SUMS` CI check and its testing documentation. Frozen
  Runtime-v2 bytes are unchanged; this is checksum-integrity coverage.
- [`sts2-game-mod#29`](https://github.com/AI-Ascension/sts2-game-mod/pull/29), merged at the
  current head, adds local safety explanations for five native unsafe blocks and corrects the
  provenance wording for the historical overlay evidence, with the repeat-seed limitation recorded
  in the changelog. The patch changes comments and documentation only; executable behavior, ABI,
  HTTP contracts, managed sources, frozen artifact bytes, and packaging remain unchanged.

These corrections add source, CI, and documentation evidence only. They do not establish a live host,
gameplay, provider, profile, or save run.

What this does and does not establish:

- It is `confirmed` that each repository's declared gates passed for the initial stack heads and
  the two source-only follow-up heads shown above: formatting,
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
