# Public topic reconciliation audit — 2026-09-07

Status: **independently source-reviewed; external authorization not recorded**. This is a
source-controlled preparation record. It records a candidate topic map and does not report
remote settings writes. The canonical map records authorization_state as not-recorded; that
approval state is separate from source review.

## Scope and method

The reconciliation covers the 12 repositories in the supplied public tagging seed. Each row in
the canonical map is managed with the applicability reason:

> Public repository in supplied tagging seed; preparation only, external writes require scoped authorization.

The before state is the refreshed read-only topic set. The after state is the candidate complete
seed set after source review. Topic order is presentation only; the planner compares sets.
Repositories outside this public seed are not represented in this public audit.

Every topic entry in 'metadata/repositories.yml' includes a meaning, implementation/planning
subject, add/retain decision, reason, and pinned evidence with repository, commit, path, line, and
classification. The cited files are default-branch source evidence. They establish source or
planning claims only; they do not establish deployment, live gameplay, provider execution, or
publication.

## Before and candidate after

| Repository | Before (refreshed live topics) | Candidate after |
| --- | --- | --- |
| AI-Ascension/.github | ai-ascension, community-health | ai-ascension, community-health, contributing, governance, github-organization |
| AI-Ascension/ai-agent-observability | (none) | ai-ascension, ai-agents, observability, llm-observability, opentelemetry, experiment-tracking, mlflow, laminar, self-hosted, docker-compose, podman |
| AI-Ascension/AI-Ascension.github.io | ai-ascension, github-pages, static-site | ai-ascension, slay-the-spire-2, documentation, github-pages, static-site, javascript, reproducible-research |
| AI-Ascension/aiascension.tech | (none) | ai-ascension, slay-the-spire-2, website, php, javascript, mailing-list |
| AI-Ascension/ascension-map-visualizer | (none) | ai-ascension, slay-the-spire-2, map-visualization, specification, project-planning |
| AI-Ascension/ascension-watchdog | (none) | ai-ascension, watchdog, process-supervision, crash-recovery, project-planning |
| AI-Ascension/sts2-game-core | domain-model, rust, validation, ai-ascension | ai-ascension, slay-the-spire-2, rust, game-state, game-logic, domain-model, validation |
| AI-Ascension/sts2-game-mod | ai-ascension, game-mod, rust, host-boundary | ai-ascension, slay-the-spire-2, modding, game-mod, rust, csharp, dotnet, ffi, host-boundary |
| AI-Ascension/sts2-gateway | ai-ascension, control-plane, rust, lease-fencing | ai-ascension, slay-the-spire-2, rust, api-gateway, control-plane, authentication, request-routing, lease-fencing |
| AI-Ascension/sts2-harness | ai-ascension, evaluation-harness, replay, rust | ai-ascension, ai-agents, agent-harness, evaluation-harness, slay-the-spire-2, rust, replay, reproducible-research, experiment-tracking |
| AI-Ascension/sts2-mcp-server | ai-ascension, mcp, model-context-protocol, rust | ai-ascension, slay-the-spire-2, ai-agents, mcp, mcp-server, model-context-protocol, rust, tool-calling |
| AI-Ascension/sts2-protocol | ai-ascension, conformance, protocol, rust | ai-ascension, slay-the-spire-2, json-schema, protocol, specification, conformance-testing, schema-validation, rust, conformance |

## Topic decisions

| Repository | Added | Retained | Removed |
| --- | --- | --- | --- |
| AI-Ascension/.github | contributing, governance, github-organization | ai-ascension, community-health | (none) |
| AI-Ascension/ai-agent-observability | ai-ascension, ai-agents, observability, llm-observability, opentelemetry, experiment-tracking, mlflow, laminar, self-hosted, docker-compose, podman | (none) | (none) |
| AI-Ascension/AI-Ascension.github.io | slay-the-spire-2, documentation, javascript, reproducible-research | ai-ascension, github-pages, static-site | (none) |
| AI-Ascension/aiascension.tech | ai-ascension, slay-the-spire-2, website, php, javascript, mailing-list | (none) | (none) |
| AI-Ascension/ascension-map-visualizer | ai-ascension, slay-the-spire-2, map-visualization, specification, project-planning | (none) | (none) |
| AI-Ascension/ascension-watchdog | ai-ascension, watchdog, process-supervision, crash-recovery, project-planning | (none) | (none) |
| AI-Ascension/sts2-game-core | slay-the-spire-2, game-state, game-logic | ai-ascension, rust, domain-model, validation | (none) |
| AI-Ascension/sts2-game-mod | slay-the-spire-2, modding, csharp, dotnet, ffi | ai-ascension, game-mod, rust, host-boundary | (none) |
| AI-Ascension/sts2-gateway | slay-the-spire-2, api-gateway, authentication, request-routing | ai-ascension, rust, control-plane, lease-fencing | (none) |
| AI-Ascension/sts2-harness | ai-agents, agent-harness, slay-the-spire-2, reproducible-research, experiment-tracking | ai-ascension, evaluation-harness, rust, replay | (none) |
| AI-Ascension/sts2-mcp-server | slay-the-spire-2, ai-agents, mcp-server, tool-calling | ai-ascension, mcp, model-context-protocol, rust | (none) |
| AI-Ascension/sts2-protocol | slay-the-spire-2, json-schema, specification, conformance-testing, schema-validation | ai-ascension, protocol, rust, conformance | (none) |

'retain' preserves every valid topic observed in the refreshed public state. 'add' records a
seed topic justified by the pinned default-branch source. No topic was removed, and no current
topic was silently discarded. The existing component-specific topics
'domain-model', 'validation', 'host-boundary', 'lease-fencing', and 'conformance'
remain explicitly retained even though they are not spelled out in the supplied seed set.

No supplied seed topic was rejected after source review. Unsupported capability tags were not
inferred from roadmaps, generated prompts, or neighboring repositories. The planned watchdog
and map visualizer rows intentionally omit 'rust' and other implementation tags because their
observed 'bootstrap' default branches contain planning/governance material rather than accepted
application source.

## Planning rows

'ascension-watchdog' and 'ascension-map-visualizer' use 'project-planning'. Every topic in
those rows has subject 'planned', and their meanings disclose that default-branch planning
material does not establish shipped implementation. The watchdog source describes supervision and
crash recovery as work in progress with no live recovery claim. The map prompt describes the
proposed map contracts and implementation assignment; it is not a delivered visualizer.

## Pinned source observations

| Repository | Default branch | Default commit |
| --- | --- | --- |
| AI-Ascension/.github | 'main' | 'd8fb867dede3ec1cde424d7f6f6f56e49dc21227' |
| AI-Ascension/ai-agent-observability | 'main' | 'b25880376d3a3334c77f58637267db93581c4c77' |
| AI-Ascension/AI-Ascension.github.io | 'main' | 'e81dd4e9ff2f8e5f8ffafc8b1a489d1e1cc7ef9f' |
| AI-Ascension/aiascension.tech | 'codex/wire-mailing-list-email' | '4e2d99c95d89ce3d18981d331faad10c9f1f7376' |
| AI-Ascension/ascension-map-visualizer | 'bootstrap' | '18915e5571829e582f460bf14b674cc2db39d9c5' |
| AI-Ascension/ascension-watchdog | 'bootstrap' | 'dc2d20badb9e86c12067316b92d6c8289b2e6995' |
| AI-Ascension/sts2-game-core | 'main' | '87e0f3d9355c0827e989d9fbc31804440852519b' |
| AI-Ascension/sts2-game-mod | 'main' | '8b71150895ea95c0625afc1389bb08e4034d9350' |
| AI-Ascension/sts2-gateway | 'main' | '33ea48f3b549f08e19db80d8c68c1438fa12a60a' |
| AI-Ascension/sts2-harness | 'main' | 'cb17b6c15262ce9356f1e85fd475af997aedc445' |
| AI-Ascension/sts2-mcp-server | 'main' | 'eb89ab251665f263c2fe3e6b735eeae3d3e40c83' |
| AI-Ascension/sts2-protocol | 'main' | '8874b0951289fd943c7e14dea36557fa24c401d1' |

Representative source locations reviewed (all pinned to the corresponding commit) include:

- **AI-Ascension/.github** — README.md:1,5; CONTRIBUTING.md:1; GOVERNANCE.md:1
- **AI-Ascension/ai-agent-observability** — README.md:3,5-13
- **AI-Ascension/AI-Ascension.github.io** — README.md:1,3,15,22,32-37,43-45; .github/workflows/pages.yml:1
- **AI-Ascension/aiascension.tech** — README.md:3,7,26-29,41
- **AI-Ascension/ascension-map-visualizer** — prompts/ASCENSION_MAP_VISUALIZER_ORCHESTRATION_PROMPT.md:5-7,162; AGENTS.md:3
- **AI-Ascension/ascension-watchdog** — README.md:3,5-12
- **AI-Ascension/sts2-game-core** — README.md:8,22-40; Cargo.toml:1; crates/core/src/state.rs:43; crates/core/src/validation.rs:1
- **AI-Ascension/sts2-game-mod** — README.md:8,17-45; Cargo.toml:1-9; experiments/managed-rust-interop/README.md:23-26; .../RuntimeV3ValidationProbe.csproj:1-4; crates/host/src/abi.rs:1
- **AI-Ascension/sts2-gateway** — README.md:8,27-30,102-106; Cargo.toml:1; crates/gateway/src/identity.rs:55
- **AI-Ascension/sts2-harness** — README.md:8,20,26-35,39-42,58-62; Cargo.toml:1
- **AI-Ascension/sts2-mcp-server** — README.md:8,10-13,27-30; Cargo.toml:1
- **AI-Ascension/sts2-protocol** — README.md:8,25-35,56-67; Cargo.toml:1; schemas/poc-v1.schema.json:2; conformance/cases/neutral-contract-seam.v1.json:16

## Rollout state and limits

No remote topic, label, issue/PR, repository setting, tag, release, protection rule, deployment,
or runtime behavior was changed by this reconciliation. Label migrations and consumer updates
were independently checked in the final technical review. See `final-independent-review.md`
for the verdict and resolved findings. Topic writes require an
owner-authorized, digest-bound plan and scoped administration permission; that authorization is
not recorded in this candidate.

A subsequent plan must re-read the complete topic arrays, compare them with these recorded
preconditions, and replace the entire topic array for each approved repository. A timeout or
unknown write outcome must be reconciled by operation identity before any retry. This audit
does not authorize such a plan or application.
