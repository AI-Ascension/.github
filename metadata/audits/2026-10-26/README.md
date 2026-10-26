# Public inventory addition — 2026-10-26

Prepared for maintainer review; no live topic, label, or repository write.
The scheduled [drift run 40356892900](https://github.com/AI-Ascension/.github/actions/runs/40356892900)
reported two unmapped repositories. Existing source pins and historical manifests
remain unchanged; advanced source pins are informational, not a refresh request.

Read-only repository and `branches/main` API observations at 16:44 UTC confirmed
that this registry and both discoveries are public:

| Repository | Stable ID | Archived | Default-branch source |
| --- | --- | --- | --- |
| AI-Ascension/STS2MCP | 1192832633 | Yes | `main` at `4431b1e5a5c2e34fcc7dbcf5617236602e334f49` |
| AI-Ascension/jev-factorio-agent | 1379060982 | No | `main` at `b1a8dd180d95968b95278e7c2d2ff5b930d6eae5` |

The pinned READMEs at line 7 describe respectively a game mod exposing an API and
a Factorio agent. This supports `kind: implementation`, not verified runtime
claims. STS2MCP is an archived fork. No source or settings in either repository
were changed.

Both rows use the established `managed: false` mechanism pending owner
applicability decisions. The schema requires a brand-topic entry even on unmanaged
rows. Neither repository currently has `ai-ascension`: STS2MCP reports
`agentic-ai`, `mcp-server`, `research-and-development`, `slay-the-spire-2`;
jev-factorio-agent reports `ai-agent`, `factorio`, `jev`, `python`, `system-one`,
`typesafe`. Their registry brand entries are therefore explicitly **proposed
additions**, not retained topics or source-derived branding claims. They do not
constitute complete topic sets for application. Owner review must establish
applicability and complete evidence-backed topics before enabling management;
archived repositories remain ineligible for writes.

Private discovery handling is unchanged: identities and fresh private evidence
stay outside this public registry. The root `observed_at` remains the historical
managed-pin review time; each new row records its own observation time.
