# Source and evidence snapshot — 2026-09-04

The public browser proof is a historical deterministic gateway replay. Its pinned test result
does not describe every capability of later default branches. Conversely, unmerged proposals
must not be credited to default branches.

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

## Updating public claims

Keep historical proof pins intact and add dated evidence rather than silently relabeling them.
Do not say “nothing touches the game” when describing current source, or use the bounded probe
as proof of gameplay. Repository and organization descriptions are separate GitHub settings;
this document does not change them or authorize deployments.
