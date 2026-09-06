<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/AI-Ascension/.github/main/profile/assets/banner-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/AI-Ascension/.github/main/profile/assets/banner-light.svg">
  <img src="https://raw.githubusercontent.com/AI-Ascension/.github/main/profile/assets/banner-light.svg" alt="AI-Ascension — Inspect how AI requests to a game get fenced, one Rust contract at a time. Runtime: unverified. Deterministic tests: confirmed." width="100%">
</picture>

## Inspect how AI requests to a game get fenced, one Rust contract at a time.

Start with deterministic, in-memory contract tests you can replay here and re-run with cargo. Later default branches include runtime executables, bounded Windows/Linux Slay the Spire 2 campaign and replay records, and a read-only coordinator-synchronization check. **Model-played Victory, native multiplayer, reliable autonomous coverage, and broader compatibility remain unverified.** See the [dated source/evidence snapshots](https://github.com/AI-Ascension/.github/blob/main/STATUS.md) for exact pins and limits; this profile has not independently reproduced those runtime records.

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
