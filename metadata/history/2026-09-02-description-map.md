# ORG_PRESENCE_DESCRIPTION_MAP

Status: **approved by lead 2026-09-02T06:56Z** after two cold-reader rounds (§3). One approved map
drives organization metadata, all eight repository descriptions/homepages/topics, README public-entry
blocks, site metadata/OG tags, social/proof-card copy, and launch drafts. Baseline values come from
`ORG_PRESENCE_FACTS.md` §3–4. Application log in §5. User review is a manual step
(`MANUAL_STEPS.md`); a user decision overrides any row here.

Contract: one sentence, 80–160 characters where possible (GitHub limit 350), leads with purpose or
owned boundary, one concrete verb+noun, no hype/urgency/affiliation/metrics/testimonials/dates,
no unsupported present-tense runtime/host/compatibility/adoption claims, distinct across products.

## 1. Approved map

| Surface | Before (baseline) | Supplement candidate | **Approved** | Chars | Basis / label |
| --- | --- | --- | --- | --- | --- |
| Organization description | `null` → `""` (scope test 06:44Z) | Make an AI-to-game path inspectable—one Rust-owned contract at a time. | Independent Rust project building a path from AI agents to Slay the Spire 2 as small, tested boundaries that can refuse a request; nothing is live yet. | 146 | direction `proposed`; "independent", "Rust", "tested boundaries that can refuse a request" `confirmed` (policy + deterministic tests); "nothing is live yet" `confirmed` (all COMPATIBILITY docs) |
| Organization display name | `null` | — | AI-Ascension | 12 | wordmark |
| Organization website | `null` → `https://ai-ascension.github.io` (07:10Z) | — | https://aiascension.tech/ (user input 07:40Z; the Pages site remains the evidence map and is linked from the profile) | — | user decision |
| `.github` (profile repo) | absent | Shared proof, evidence, and contribution standards for AI-Ascension. | Contributor guide, issue forms, security policy, and shared standards for the AI-Ascension organization. | 104 | `confirmed` once repo exists |
| `AI-Ascension.github.io` (Pages) | absent | Evidence-first public map of AI-Ascension's bounded AI-to-game path. | Public site for AI-Ascension: what is tested today, what is only proposed, and a browser replay of one gateway contract test. | 123 | `confirmed` once site exists; replay backed by FACTS §6 |
| `sts2-game-core` | STS2 host-independent game core | Host-independent domain and policy boundaries for the AI-to-game path. | Host-independent Rust domain core: typed game-state values, pure validation, and policy rules with no I/O. | 105 | `confirmed` (README "Initial semantic seam"; core owns no HTTP/MCP/process/filesystem) |
| `sts2-game-mod` | STS2 game-facing host, loader, and adapter boundary | Owner-local host boundary and managed translation for AI-Ascension. | Game-process adapter: a bounded main-thread work queue, versioned ABI check, and HTTP request admission limits. | 108 | `confirmed` crates `host`, `http-adapter`; "managed loader" deliberately omitted (README: unimplemented) |
| `sts2-gateway` | STS2 instance gateway control plane | Lifecycle, leases, routing, and isolation for bounded game-host instances. | In-memory control plane for game-host instances: lifecycle, one lease per instance with epoch fencing, and fixed routes. | 114 | `confirmed` in-memory (`control.rs`, `identity.rs`, `forwarding.rs`); "isolation" removed because only record-level isolation exists |
| `sts2-mcp-server` | STS2 MCP server adapter | Thin MCP tool adapter for gateway contracts and authority boundaries. | Thin MCP tool adapter that maps approved calls to the authenticated gateway API without bypassing it. | 100 | `confirmed` by `seam.rs` (one request per call; rejects before gateway); readers flagged the claim as one to verify → evidence page maps it to tests |
| `sts2-harness` | STS2 experiment and model harness | Experiments, episodes, replay, and evidence artifacts for bounded AI-to-game work. | Experiment coordinator for AI runs: episodes, a pluggable model-provider interface, replay of recorded records, and artifact lineage. | 131 | `confirmed` ports/seams; "replay of recorded records" chosen over "deterministic replay" so no one reads it as replaying a live model |
| `sts2-protocol` | STS2 shared neutral protocol contracts | Language- and transport-neutral metadata contracts for the ascent. | Shared metadata contracts (identity, versions, error envelopes) in language-neutral schemas with golden test vectors. | 111 | `confirmed` (`schemas/common`, `conformance/golden`) |

### Homepages and topics (approved)

| Repository | Homepage | Topics |
| --- | --- | --- |
| `.github` | https://ai-ascension.github.io | `ai-ascension`, `community-health` |
| `AI-Ascension.github.io` | https://ai-ascension.github.io | `ai-ascension`, `github-pages`, `static-site` |
| `sts2-game-core` | https://ai-ascension.github.io/repositories.html#sts2-game-core | `rust`, `ai-ascension`, `domain-model`, `validation` |
| `sts2-game-mod` | https://ai-ascension.github.io/repositories.html#sts2-game-mod | `rust`, `ai-ascension`, `host-boundary`, `game-mod` |
| `sts2-gateway` | https://ai-ascension.github.io/repositories.html#sts2-gateway | `rust`, `ai-ascension`, `control-plane`, `lease-fencing` |
| `sts2-mcp-server` | https://ai-ascension.github.io/repositories.html#sts2-mcp-server | `rust`, `ai-ascension`, `mcp`, `model-context-protocol` |
| `sts2-harness` | https://ai-ascension.github.io/repositories.html#sts2-harness | `rust`, `ai-ascension`, `evaluation-harness`, `replay` |
| `sts2-protocol` | https://ai-ascension.github.io/repositories.html#sts2-protocol | `rust`, `ai-ascension`, `protocol`, `conformance` |

Topics are metadata, not claims; none asserts a runtime, host, or game compatibility.

## 2. Distinctness check

Distinct owned nouns: domain core / validation (core); game-process adapter / queue / ABI (mod);
in-memory control plane / lease / fencing (gateway); MCP adapter (mcp-server); experiment coordinator
/ episodes / lineage (harness); metadata contracts / schemas / golden vectors (protocol). The phrase
"AI-to-game path" no longer appears in any description; "bounded" appears once, as a technical
qualifier of the work queue.

## 3. Cold-reader results

Three fresh contexts per round, no repository names shown, personas: curious software person
(Sonnet), Rust developer / roguelike player (Haiku), skeptical security maintainer (Opus).

### Round 1 (06:50Z) — first draft; consensus problems

- "one owned contract at a time" — cryptic to all three readers (org line rated murkiest twice).
- "bounded AI-to-game path" repeated in four descriptions, never defined; reads as a tagline.
- Site (C) and harness (H) overlapped on "replay" and "evidence artifacts"; readers could not tell who owns replay.
- "audience paths", "evidence-first", "boundary seams", "owner-local", "admission guard", "the ascent" flagged as insider wording.
- Security reader wanted evidence for: MCP "without bypassing it", site "deterministic proof", gateway "isolation", and the meaning of "independent" for a commercial title.

### Round 2 (06:53Z) — revised draft; results

- All three identified each repository's owned boundary correctly; MCP adapter (G) and domain core (D) rated clearest; the org line remained the murkiest ("posture, not artifact") but was now understood as "an agent-facing gateway to a game that inspects and can refuse requests".
- Player persona (2b) found nothing that sounds like a cheat: "Not a cheat; anti-cheat."
- Residual asks: "proven" is a strong word (C); "per-instance isolation — by what?" (F); "deterministic replay against a nondeterministic LLM overclaims" (H); "every request … can refuse it" is a security guarantee that needs an enforcement point (A); "epoch fencing" and "provider port" are jargon.

### Final revisions applied (06:56Z)

- C: "proven" → "tested". F: "per-instance isolation" → "In-memory … one lease per instance with epoch fencing". H: "deterministic replay" → "replay of recorded records"; "provider port" → "a pluggable model-provider interface". A: "every request crosses an inspectable boundary that can refuse it" → "small, tested boundaries that can refuse a request; nothing is live yet". E: "adapter seams" → "adapter". "epoch fencing" kept in F because it names the exact mechanism the public proof shows; the site defines it next to the proof.
- Residual: the org description is inherently positioning; the site hero and status line carry the proof link that readers asked for. Recorded as accepted residual, not hidden.

## 4. Approval

Lead approval: **approved 2026-09-02T06:56Z** by the lead orchestrator (this session) after the
revisions above. No user input was available; user review is a manual step in `MANUAL_STEPS.md`.

## 5. Application log (command, account, response, prior → new, timestamp)

(pending — populated during D5/D6 application)

### 5.1 Organization and product repositories — applied 2026-09-02T07:10:15Z–07:10:38Z (account `CompleteDotTech`, org admin)

Full command transcript with prior/after JSON: `planning/org_presence/metadata-application.log`.

| Destination | Command | Prior value | New value | Response |
| --- | --- | --- | --- | --- |
| org `name` | `gh api -X PATCH orgs/AI-Ascension -f name=…` | `null` | `AI-Ascension` | 200, `updated_at 2026-09-02T07:10:15Z` |
| org `description` | same call | `null` (then `""` after the 06:44Z scope test) | approved org sentence (146 chars) | 200 |
| org `blog` (website) | same call | `null` | `https://ai-ascension.github.io` | 200 |
| `sts2-game-core` description / topics | `gh repo edit AI-Ascension/sts2-game-core --description … --add-topic …` | `STS2 host-independent game core` / `[]` | approved / `ai-ascension, domain-model, rust, validation` | re-query matched |
| `sts2-game-mod` | same pattern | `STS2 game-facing host, loader, and adapter boundary` / `[]` | approved / `ai-ascension, game-mod, host-boundary, rust` | matched |
| `sts2-gateway` | same | `STS2 instance gateway control plane` / `[]` | approved / `ai-ascension, control-plane, lease-fencing, rust` | matched |
| `sts2-mcp-server` | same | `STS2 MCP server adapter` / `[]` | approved / `ai-ascension, mcp, model-context-protocol, rust` | matched |
| `sts2-harness` | same | `STS2 experiment and model harness` / `[]` | approved / `ai-ascension, evaluation-harness, replay, rust` | matched |
| `sts2-protocol` | same | `STS2 shared neutral protocol contracts` / `[]` | approved / `ai-ascension, conformance, protocol, rust` | matched |

Homepages for the six product repositories are deliberately deferred until the Pages site is
deployed (so no public link dangles); see §5.2. Rollback: re-run `gh repo edit` with the prior
description and `--remove-topic` for each topic; org fields via the same PATCH with prior values
(`null` cannot be restored literally; `""` is the closest).

### 5.2 New repositories, homepages, site metadata — applied 07:29Z–07:39Z

| Destination | Prior | New | Command / evidence |
| --- | --- | --- | --- |
| `AI-Ascension/.github` description/homepage/topics | absent | approved `.github` sentence; `https://ai-ascension.github.io`; `ai-ascension, community-health` | `gh repo create … --description … --homepage …` + `gh repo edit --add-topic` (07:29Z) |
| `AI-Ascension/AI-Ascension.github.io` description/homepage/topics | absent | approved Pages sentence; site URL; `ai-ascension, github-pages, static-site` | same pattern (07:37Z) |
| six product `homepage` | `null` | `https://ai-ascension.github.io/repositories.html#<repo>` | `gh repo edit --homepage` (07:39Z), re-queried |
| site `<meta name="description">` / `og:description` / `twitter:description` on `index.html` | n/a | approved Pages sentence (verified on the live page 07:38Z) | `curl https://ai-ascension.github.io/` |
| README public-entry blocks (six PRs) | `# <repo>` first line | approved description verbatim in the header blockquote | PR #1 in each repo; captains' byte-compare |
| social/proof cards | n/a | approved descriptions as outlined vector overlays | `assets/identity/social/*.png`, `ART_TRANSFORMS.md` |
| launch drafts | n/a | descriptions verbatim (launch editor verified 3/3 by `grep -F`) | `ORG_PRESENCE_LAUNCH_PACK.md` §4 |

### 5.3 Organization website — user input 07:40Z, applied 07:43:04Z

| Destination | Prior | New | Command |
| --- | --- | --- | --- |
| org `blog` | `https://ai-ascension.github.io` (set 07:10Z; original baseline `null`) | `https://aiascension.tech/` | `gh api -X PATCH orgs/AI-Ascension -f blog=…` → 200 |

The Pages site stays the evidence map; the profile README, every site footer, the index "proposed"
list, and evidence ledger row 19 cross-link the event site with label `proposed`.
