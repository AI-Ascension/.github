<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/AI-Ascension/.github/main/profile/assets/banner-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/AI-Ascension/.github/main/profile/assets/banner-light.svg">
  <img src="https://raw.githubusercontent.com/AI-Ascension/.github/main/profile/assets/banner-light.svg" alt="AI-Ascension — Inspect how AI requests to a game get fenced, one Rust contract at a time. Runtime: unverified. Deterministic tests: confirmed." width="100%">
</picture>

## Inspect how AI requests to a game get fenced, one Rust contract at a time.

Start with deterministic, in-memory contract tests you can replay here and re-run with cargo. Later default branches include runtime executables, bounded Windows/Linux Slay the Spire 2 campaign and replay records, and a read-only coordinator-synchronization check. **Model-played Victory, native multiplayer, reliable autonomous coverage, and broader compatibility remain unverified.** See the [dated source/evidence snapshots](https://github.com/AI-Ascension/.github/blob/main/STATUS.md) for exact pins and limits; this profile has not independently reproduced those runtime records.

## Historical candidate boundary — 2026-09-07

These open candidates provide source and component checks for the Runtime-v4 path. Their checks do not establish a host run, provider settlement, or release.

| Candidate | Public state | Scope at this date |
| --- | --- | --- |
| [`sts2-gateway` draft PR #22](https://github.com/AI-Ascension/sts2-gateway/pull/22) | `9cbd2c4` · mergeable · Rust quality and policy checks passed | Bounded route and consumer source path; live host settlement remains unverified. |
| [`sts2-mcp-server` draft PR #27](https://github.com/AI-Ascension/sts2-mcp-server/pull/27) | `9228574` · mergeable · foundation quality and policy checks passed | Runtime-v4 expert mapping source; merge to the default branch and native settlement remain pending. |
| [`sts2-harness` draft PR #36](https://github.com/AI-Ascension/sts2-harness/pull/36) | `5f17cd6` · based on `cb17b6c` · mergeable · Rust quality and policy checks passed | Catalog-recovery source integration; 223 workspace tests plus separate independent oracles reviewed; provider, native, host-restart, and gameplay settlement remain unverified. |

Native final artifact and installation, model-played Victory, native co-op actions and recovery, Workshop lifecycle, live observability ingestion/correlation, deployment, and release acceptance remain unverified. Refer to the [dated status record](https://github.com/AI-Ascension/.github/blob/main/STATUS.md) for the wider repository matrix and evidence limits.

## Earlier current default-main source boundary — 2026-09-10, 00:50 UTC

The current default branches carry the bounded Runtime-v4 expert source/component paths and the
merged REST selector recovery. These exact heads do not establish native host legality, settled
effects, provider execution, deployment, or release.

| Repository | Current default-main head | Source/component scope at this date |
| --- | --- | --- |
| [`sts2-protocol`](https://github.com/AI-Ascension/sts2-protocol/commit/f2dac90529f584a6511c1760adce9da28f7f910a) | `f2dac905` | Runtime-v4 expert schemas, artifacts, manifests, checksum inventories, validators, and conformance cases; schema digests `0ee034d5da83f34e9fa0ba23038738d56ef8cfccb1c6e752af3ab63d212c8e42` and `393318bda8c3522c0ecbacc78b95471a9f4dc3f825169d2048f4c74a7b7f2929`. |
| [`sts2-game-mod`](https://github.com/AI-Ascension/sts2-game-mod/commit/d8b46bccbee9eff108efdab9c8fc9b27dbf2c034) | `d8b46bcc` | Runtime-v4 expert state/action bridge and bounded synthetic route/admission checks; native expert gameplay and settlement remain unverified. |
| [`sts2-gateway`](https://github.com/AI-Ascension/sts2-gateway/commit/434d8c77fb01895e90c741609e3d2a0ad0e9e8b8) | `434d8c77` | Runtime-v4 expert routes, bounded map route, and copied artifacts; host settlement and deployment remain unverified. |
| [`sts2-mcp-server`](https://github.com/AI-Ascension/sts2-mcp-server/commit/3b6d71fe9642d27717ca6cfa07b5342b914c044c) | `3b6d71fe` | Runtime-v4 expert mapping and merged REST selector recovery; native MCP-to-game settlement remains unverified. |
| [`sts2-harness`](https://github.com/AI-Ascension/sts2-harness/commit/b8c50c87db0275f0e08d69892f1ebce275f4acb6) | `b8c50c8` | Expert composition, recovery, and bounded synthetic checks; provider, native, host-restart, and gameplay settlement remain unverified. |

The current source records are component evidence. The separate `coop-synchronization-v1` profile is
a read-only gateway/MCP coordinator-report contract; it carries no action, vote, shared-effect, or
host-game authority. Native co-op gameplay and disconnect/rejoin recovery remain unverified.
Model-played Victory, broad character/seed/branch coverage, observability correlation, Workshop
lifecycle, deployment, and public release also remain unverified.

## Earlier live default-main source boundary — 2026-09-10, 02:22 UTC

A fresh GitHub REST refresh re-checked all nine default branches and their open pull requests.
The exact current heads are below; they establish source/component identity only. The [status
record](https://github.com/AI-Ascension/.github/blob/main/STATUS.md) retains the 36 open PRs with
their heads, draft/ready state, mergeability, and check conclusions.

| Repository | Current `main` head | Bounded scope at this refresh |
| --- | --- | --- |
| [`sts2-game-core`](https://github.com/AI-Ascension/sts2-game-core/commit/87e0f3d9355c0827e989d9fbc31804440852519b) | `87e0f3d9355c` | Host-independent semantics and tests. |
| [`sts2-game-mod`](https://github.com/AI-Ascension/sts2-game-mod/commit/c21ddf38bd2b540be871f88303078625966270ce) | `c21ddf38bd2b` | Runtime-v4 expert bridge and bounded synthetic checks; native expert gameplay remains unverified. |
| [`sts2-gateway`](https://github.com/AI-Ascension/sts2-gateway/commit/776327aca63c8ff6c6920865cd5c72de83b10c7b) | `776327aca63c` | Runtime-v4 routes and map consumer path; host settlement remains unverified. |
| [`sts2-mcp-server`](https://github.com/AI-Ascension/sts2-mcp-server/commit/4787efa1251bcc0eddccc5fea63a8939a8eb06d0) | `4787efa1251` | Runtime-v4 mapping and REST selector recovery; native MCP-to-game settlement remains unverified. |
| [`sts2-harness`](https://github.com/AI-Ascension/sts2-harness/commit/f8b5858d09978edf17c24b81a5ced07847e2bd5d) | `f8b5858d0997` | Documentation merge on top of the merged PR41 functional source; provider and gameplay settlement remain unverified. |
| [`sts2-protocol`](https://github.com/AI-Ascension/sts2-protocol/commit/7fa0d8e82fbc245db74187106918d9f1af58c447) | `7fa0d8e82fbc` | Runtime-v4 schemas, artifacts, validators, and conformance cases. |
| [`ai-agent-observability`](https://github.com/AI-Ascension/ai-agent-observability/commit/28a48590afb75b07590e1b78ea47dae08f5c3ade) | `28a48590afb7` | Source topology and deployment tooling; current-main gameplay ingestion and persistence remain unverified. |
| [`.github`](https://github.com/AI-Ascension/.github/commit/217c9c10d82fc22e553c9af222a3a3bbb08259fa) | `217c9c10d82f` | Governance and acceptance status records. |
| [`AI-Ascension.github.io`](https://github.com/AI-Ascension/AI-Ascension.github.io/commit/832068b69a44cca2bbfa7ea35e90190eddc3b35a) | `832068b69a44c` | Static evidence and repository pages; deployment remains unverified. |

The independent review of [harness PR41](https://github.com/AI-Ascension/sts2-harness/pull/41)
confirmed its exact merged source head `03fdc626`, formatting, repository policy, Clippy, and a
serial workspace result of 285 passed and 5 ignored. Its bounded map, replay, REST recovery, and
receipt-query source does not establish native gameplay or provider settlement. Native host
legality, model-played Victory, multiplayer actions and recovery, observability persistence,
Workshop lifecycle, deployment, and release remain unverified.

**[Run the 45-second proof](https://ai-ascension.github.io/proof.html)** — browser only; no account, no install, no game files, no model.

## Pick your path

**Curious player or observer.** The browser proof touches no game: it replays a historical test in which a stale lease is denied before any transport call. It is not a live-play demonstration. [Run the proof](https://ai-ascension.github.io/proof.html), then compare its [historical evidence](https://ai-ascension.github.io/evidence.html) with the [dated runtime evidence](https://github.com/AI-Ascension/.github/blob/main/STATUS.md). If a label confuses you, [report it](https://github.com/AI-Ascension/.github/issues/new?template=evidence.yml).

**Rust or systems contributor.** You do not need all nine repositories. Start with one boundary, the gateway lease fence, and one bounded task. [Run the cargo recipe](https://ai-ascension.github.io/recipes.html): it prints the same trace as the browser replay, with the exact test names and source lines. Then take a `first-task` issue and [submit a fence-case fixture](https://github.com/AI-Ascension/.github/issues/new?template=proof-recipe.yml).

**AI, MCP, or automation builder.** In the pinned in-memory tests, one MCP tool call maps to one gateway request path, and malformed frames are rejected before the gateway is reached. Later source includes executable transport and a read-only coordinator-synchronization profile; the recorded coordinator exchange has no native game connections and is not evidence of multiplayer gameplay. Read the [architecture](https://ai-ascension.github.io/architecture.html) alongside the [current-source boundary](https://github.com/AI-Ascension/.github/blob/main/STATUS.md), run the recipe without credentials, then [file a contract observation](https://github.com/AI-Ascension/.github/issues/new?template=contract-observation.yml).

**Maintainer or security operator.** Authority stays with the game host. The historical pinned gateway tests exercise rejection of stale epochs, wrong instances, and oversized bodies before transport, plus injected process, readiness, and transport failures. Those fake-boundary results do not establish the live executable's lifecycle or restart safety. Read the [evidence page](https://ai-ascension.github.io/evidence.html) and [SECURITY.md](https://github.com/AI-Ascension/.github/blob/main/SECURITY.md), verify the claim-to-test mapping yourself, then send a security note privately or a failure-handling observation.

## The ascent

Read from the bottom up. A request from a model descends through each tier toward the game host, and each tier can refuse it. This table preserves the **historical proof snapshot**, including its descriptions and evidence pins; it is not a current default-branch compatibility matrix. Later runtime and coordinator evidence is [tracked separately](https://github.com/AI-Ascension/.github/blob/main/STATUS.md).

| Tier | Repository | Owns | Status |
| --- | --- | --- | --- |
| model / provider | not a repository | Whatever model or provider a harness run is configured to call. | No provider is called by any test. Live use: `proposed`. |
| harness | [`sts2-harness`](https://github.com/AI-Ascension/sts2-harness) (flagship) | Experiment coordinator for AI runs: episodes, a pluggable model-provider interface, replay of recorded records, and artifact lineage. | `confirmed` deterministic in-memory tests at [`b485150`](https://github.com/AI-Ascension/sts2-harness/commit/b485150f4728b7fa1c2b10a9d14e7b6ea2124d0e). Runtime: `unverified`. |
| MCP adapter | [`sts2-mcp-server`](https://github.com/AI-Ascension/sts2-mcp-server) | Thin MCP tool adapter that maps approved calls to the authenticated gateway API without bypassing it. | `confirmed` deterministic in-memory tests at [`5faed97`](https://github.com/AI-Ascension/sts2-mcp-server/commit/5faed9761866f89b922f01d3d389f3db55b9cf5e). Live transport: `unverified`. |
| gateway | [`sts2-gateway`](https://github.com/AI-Ascension/sts2-gateway) (proof lives here) | In-memory control plane for game-host instances: lifecycle, one lease per instance with epoch fencing, and fixed routes. | `confirmed` deterministic in-memory tests at [`e7bce21`](https://github.com/AI-Ascension/sts2-gateway/commit/e7bce21d0cbd48a02c25d6463a3376ea1c94e253). Listener, supervisor: `unverified`. |
| game adapter | [`sts2-game-mod`](https://github.com/AI-Ascension/sts2-game-mod) | Game-process adapter: a bounded main-thread work queue, versioned ABI check, and HTTP request admission limits. | `confirmed` deterministic in-memory tests at [`aa465f3`](https://github.com/AI-Ascension/sts2-game-mod/commit/aa465f38cda19e246b022374be05acadb4c66d21). Any game process: `unverified`. |
| game host | not a repository | The game itself. No game files are stored or distributed here. | Not contacted by this historical proof. Later host-probe evidence is scoped separately. |

### Beside the ascent

| Repository | Owns | Status |
| --- | --- | --- |
| [`sts2-game-core`](https://github.com/AI-Ascension/sts2-game-core) | Host-independent Rust domain core: typed game-state values, pure validation, and policy rules with no I/O. | `confirmed` deterministic in-memory tests at [`6c46a55`](https://github.com/AI-Ascension/sts2-game-core/commit/6c46a5536e0e9f825af428db8b4811dcb2a4f26d). |
| [`sts2-protocol`](https://github.com/AI-Ascension/sts2-protocol) | Shared metadata contracts (identity, versions, error envelopes) in language-neutral schemas with golden test vectors. | `confirmed` conformance tests at [`f3ef7ca`](https://github.com/AI-Ascension/sts2-protocol/commit/f3ef7ca3037133cfc0cc571a12af2be1cba3df8f). |

The six STS2 product repositories are Rust-first, with a documented managed-loader exception in game-mod. The organization also owns the static site, governance files, and [observability stack](https://github.com/AI-Ascension/ai-agent-observability). Project code is MIT-licensed; third-party notices and each repository's source policy still apply. No game files are distributed here. Full map: [repositories](https://ai-ascension.github.io/repositories.html).

## Status and evidence

Every public claim carries one of five labels:

- <img src="https://raw.githubusercontent.com/AI-Ascension/.github/main/profile/assets/stamps/confirmed.svg" width="14" height="14" alt=""> `confirmed` — observed by a named command or test at a named commit, reproducible by anyone.
- <img src="https://raw.githubusercontent.com/AI-Ascension/.github/main/profile/assets/stamps/source-derived.svg" width="14" height="14" alt=""> `source-derived` — stated by a repository's own documents (README, ARCHITECTURE, COMPATIBILITY) and not separately run.
- <img src="https://raw.githubusercontent.com/AI-Ascension/.github/main/profile/assets/stamps/proposed.svg" width="14" height="14" alt=""> `proposed` — a design or direction that has not been built.
- <img src="https://raw.githubusercontent.com/AI-Ascension/.github/main/profile/assets/stamps/inferred.svg" width="14" height="14" alt=""> `inferred` — a conclusion drawn from confirmed facts but not itself observed.
- <img src="https://raw.githubusercontent.com/AI-Ascension/.github/main/profile/assets/stamps/unverified.svg" width="14" height="14" alt=""> `unverified` — not checked; treated as unknown, never as "no".

Historical proof stamp: `confirmed` for the deterministic in-memory tests at the pinned commits above; no runtime result follows from that proof. The public proof replays `stale_epoch_and_wrong_instance_are_denied_before_transport` and `fixed_transport_is_bounded_and_fail_closed` from `crates/gateway/tests/control_plane.rs` at `sts2-gateway@e7bce21`; the claim-to-test mapping is on the [evidence page](https://ai-ascension.github.io/evidence.html). The [dated status record](https://github.com/AI-Ascension/.github/blob/main/STATUS.md) now also points to bounded Windows/Linux campaign/replay and read-only coordinator evidence; those records do not establish model-played Victory, native multiplayer, or release readiness. Star and fork counts are counts, not evidence. The planned four-model live race is described at [aiascension.tech](https://aiascension.tech/); the event announcement is not evidence of a completed autonomous run.

## Contribute

Start with [CONTRIBUTING.md](https://github.com/AI-Ascension/.github/blob/main/CONTRIBUTING.md) (boundary rules, first safe tasks, how to run the recipe) and the site's [contributing page](https://ai-ascension.github.io/contributing.html). Report defects, contract observations, doubtful labels, and proof recipes through the [issue forms](https://github.com/AI-Ascension/.github/issues/new/choose). Security concerns go through [SECURITY.md](https://github.com/AI-Ascension/.github/blob/main/SECURITY.md), never a public issue. Decisions and roles are in [GOVERNANCE.md](https://github.com/AI-Ascension/.github/blob/main/GOVERNANCE.md). Stars and shares are never required.

AI-Ascension is an independent project. It is not affiliated with or endorsed by Mega Crit or Valve and grants no rights to game files, assets, or marks. No game files are stored or distributed.


## Latest default-main source boundary — 2026-09-10, 02:36 UTC

After the 02:22 UTC documentation refresh, a read-only requery recorded the latest default-main
heads below. It found 31 open PRs; the [status record](https://github.com/AI-Ascension/.github/blob/main/STATUS.md)
retains their exact heads, draft/ready states, mergeability, and check conclusions. These source
records remain separate from native host, provider, gameplay, observability, deployment, Workshop,
and release acceptance.

| Repository | Current `main` head | Source/component scope |
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

The requery confirms the documentation merges at `.github` `8336899bb0a154055691225f7e59d92e8acf2190`
and site `2ae456c6395c1e62395f79db7f42dc3712a6ab3c`. Native host loading, provider settlement,
terminal gameplay, native co-op actions and recovery, observability persistence, Workshop lifecycle,
deployment, and release remain unverified.

## Latest default-main source boundary — 2026-09-10, 03:11 UTC

A read-only GitHub API requery ran from `2026-09-10T03:11:42Z` through `2026-09-10T03:11:44Z` after site PR18 merged. It recorded the nine current default-main heads and 31 open PRs; the [status record](https://github.com/AI-Ascension/.github/blob/main/STATUS.md) contains the exact PR heads, draft/ready states, merge states, and check conclusions. These source records remain separate from native host, provider, gameplay, observability, deployment, Workshop, and release acceptance.

| Repository | Current `main` head | Source/component scope |
| --- | --- | --- |
| [`sts2-game-core`](https://github.com/AI-Ascension/sts2-game-core/commit/87e0f3d9355c0827e989d9fbc31804440852519b) | `87e0f3d9355c` | Host-independent semantics and tests. |
| [`sts2-game-mod`](https://github.com/AI-Ascension/sts2-game-mod/commit/caae865986d2274736d92b4f9be2bbda24bab83d) | `caae865986d2` | Merged seeded-run adapter and Runtime-v4 source/component paths; native expert gameplay, installation, and settlement remain unverified. |
| [`sts2-gateway`](https://github.com/AI-Ascension/sts2-gateway/commit/2b44bf347f790509c9f13378c89719d09366d45b) | `2b44bf347f79` | Merged seeded-run boundary and Runtime-v4 routes; host settlement and deployment remain unverified. |
| [`sts2-mcp-server`](https://github.com/AI-Ascension/sts2-mcp-server/commit/b5a9262f1c76da76ea6f84fca0f1ee821ff67001) | `b5a9262f1c76` | Merged seeded-run profile and Runtime-v4 mapping; native MCP-to-game settlement remains unverified. |
| [`sts2-harness`](https://github.com/AI-Ascension/sts2-harness/commit/3926e5a30ab569612e67d2dfdc6542f1391e95d7) | `3926e5a30ab5` | Merged seeded-run transport and PR41 source; provider, native, host-restart, and gameplay settlement remain unverified. |
| [`sts2-protocol`](https://github.com/AI-Ascension/sts2-protocol/commit/d3ab5fca7d9d74bb31eeb3e5b343d8024ee44404) | `d3ab5fca7d9d` | Merged seeded-run selection context and Runtime-v4 schemas, artifacts, validators, and conformance cases. |
| [`ai-agent-observability`](https://github.com/AI-Ascension/ai-agent-observability/commit/28a48590afb75b07590e1b78ea47dae08f5c3ade) | `28a48590afb7` | Source topology and deployment tooling; current-main gameplay ingestion, persistence, and two-backend correlation remain unverified. |
| [`.github`](https://github.com/AI-Ascension/.github/commit/f948584281f29b4adb1dc0178036d85237b37e20) | `f948584281f2` | Governance and acceptance status records at this capture; no metadata, deployment, or release change is implied. |
| [`AI-Ascension.github.io`](https://github.com/AI-Ascension/AI-Ascension.github.io/commit/d5a11452334aab87dfb63986b8c5fe01c9d619b0) | `d5a11452334a` | Merged PR18 static evidence and repository pages; Pages deployment and runtime evidence remain unverified. |

The release boundary remains unverified: current source and checks do not establish a final installable artifact, host loading, Workshop lifecycle, or public release. The observability boundary remains unverified: current-main source and tooling do not establish gameplay ingestion, persistence, or correlation in both backends. Site PR18 is merged at [`d5a1145`](https://github.com/AI-Ascension/AI-Ascension.github.io/commit/d5a11452334aab87dfb63986b8c5fe01c9d619b0).

## Latest default-main source boundary — 2026-09-10, 07:49 UTC

A read-only GitHub API requery recorded nine default-main heads and 27 open pull requests. The [status record](https://github.com/AI-Ascension/.github/blob/main/STATUS.md) retains the exact pull-request heads, draft/ready states, merge states, and hosted check results. These source records remain separate from native host, provider, gameplay, observability, deployment, Workshop, and release acceptance.

| Repository | Current `main` head | Source/component scope |
| --- | --- | --- |
| [`sts2-game-core`](https://github.com/AI-Ascension/sts2-game-core/commit/07b51c88ebe949aec263c130ccc63200e38dfaa7) | `07b51c88ebe9` | Host-independent semantics and tests. |
| [`sts2-game-mod`](https://github.com/AI-Ascension/sts2-game-mod/commit/903b645bf4dc5b299fbf16e4cef498b9bcd0ea18) | `903b645bf4dc` | Seeded-run adapter source and managed source boundary; native expert gameplay, installation, and settlement remain unverified. |
| [`sts2-gateway`](https://github.com/AI-Ascension/sts2-gateway/commit/6b6c7f2fac67de22fdf78c9fd818c6781f689ba0) | `6b6c7f2fac67` | Seeded-run gateway source and bounded routes; host settlement and deployment remain unverified. |
| [`sts2-mcp-server`](https://github.com/AI-Ascension/sts2-mcp-server/commit/73e777b96700917cca5ff8f6ce0f5a72009384bc) | `73e777b96700` | Seeded-run transport and gateway mapping source; native MCP-to-game settlement remains unverified. |
| [`sts2-harness`](https://github.com/AI-Ascension/sts2-harness/commit/68e4f935f251c5e20d07b929c6b1c096d0b7b183) | `68e4f935f251` | Seeded-run transport and coordinator source; provider execution, native host restart, and gameplay settlement remain unverified. |
| [`sts2-protocol`](https://github.com/AI-Ascension/sts2-protocol/commit/e5e545c2ff7166e073f6d44256016f85d7ea7e83) | `e5e545c2ff71` | Seeded-run protocol contract source, schemas, artifacts, validators, and conformance cases. |
| [`ai-agent-observability`](https://github.com/AI-Ascension/ai-agent-observability/commit/28a48590afb75b07590e1b78ea47dae08f5c3ade) | `28a48590afb7` | Source topology and deployment tooling; current-main gameplay ingestion, persistence, and two-backend correlation remain unverified. |
| [`.github`](https://github.com/AI-Ascension/.github/commit/92ab3ed900272703dbbe892bd333ead2a6cf1a86) | `92ab3ed90027` | Governance and acceptance status records; no metadata, deployment, or release change is implied. |
| [`AI-Ascension.github.io`](https://github.com/AI-Ascension/AI-Ascension.github.io/commit/d5a11452334aab87dfb63986b8c5fe01c9d619b0) | `d5a11452334a` | Static evidence and repository pages; Pages deployment is separately reported below and runtime evidence remains unverified. |


The current release and observability boundaries remain unverified. Site PR18 is merged at [`d5a1145`](https://github.com/AI-Ascension/AI-Ascension.github.io/commit/d5a11452334aab87dfb63986b8c5fe01c9d619b0); validation and GitHub Pages deployment succeeded, and the Pages API reports `built`. The `.github` presentation PR10 remains a separate draft and is not part of this current snapshot.
