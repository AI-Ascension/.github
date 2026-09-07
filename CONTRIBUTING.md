# Contributing to AI-Ascension

These rules apply across every `AI-Ascension` repository. Each product repository adds its own
`CONTRIBUTING.md`, `docs/ARCHITECTURE.md`, `docs/COMPATIBILITY.md`, and decision records; when they
say more, they win for that repository. Nothing here requires you to understand all six
product repositories. One boundary and one bounded task is enough.

## Evidence labels

Every claim in an issue, pull request, README, or site page carries exactly one label:

| Label | Meaning |
| --- | --- |
| `confirmed` | Observed by a named command or test at a named commit; anyone can reproduce it. |
| `source-derived` | Stated by a repository's own documents and not separately run. |
| `proposed` | A design or direction that has not been built. |
| `inferred` | A conclusion drawn from confirmed facts but not itself observed. |
| `unverified` | Not checked. Unknown is not "no"; write `unverified`, not a guess. |

The site's pinned proof establishes deterministic, in-memory behavior at its recorded commits,
not the complete current runtime. Later default branches include runtime executables, bounded
Windows/Linux campaign and replay records, and a read-only coordinator-synchronization check. See
[STATUS.md](STATUS.md) for the exact sources and evidence limits. Do not generalize those records
to model-played Victory, native multiplayer, other hosts, or current release artifacts; equally, do
not claim that no listener or host integration exists. Label an inspected report `source-derived`
when you have not independently reproduced its runtime result.

## Boundary rules for every repository

- Follow the target repository's language boundary and documented exceptions. The six STS2
  product repositories are Rust-first and prohibit Python; game-mod explicitly permits its
  narrow managed C# loader and supporting tooling. The static site and observability stack
  have different source/configuration boundaries. Where provided, run the repository's policy
  tool (`cargo run --locked --package repo-policy -- --strict`); these shared documents do not
  authorize new exceptions.
- No proprietary game files: no binaries, data, art, saves, or host assemblies, in source or in
  fixtures, ever.
- No copied harness source. Write original code; do not transliterate another implementation or
  cite its source structure as a requirement.
- One task per branch. Do not combine unrelated changes.
- No direct commits to `main`. Every change arrives as a pull request.
- Agents and humans may prepare and verify a change; only maintainers merge, tag, publish, or
  deploy. A passing CI run is not a merge claim.
- Keep credentials, personal paths, and private multiplayer data out of every commit, issue, and
  attachment.

## Shared issue and pull-request labels

`labels.yml` is the canonical shared definition file. The shared work-kind vocabulary is `bug`,
`enhancement`, `documentation`, `research`, `maintenance`, and `question`. The standard GitHub
labels `good first issue` and `help wanted` are available for maintainer triage; neither is assigned
by a template or by this migration.

The defect form keeps its existing `defect.yml` URL for link compatibility and now applies `bug`.
The live `defect` and `bug` labels, and the live `docs` and `documentation` labels, have distinct
IDs in nine repositories. Their migration is additive: assignments receive the destination only
when the reviewed plan is applied, both definitions remain, and unrelated labels are preserved.

The four audience labels (`audience:player`, `audience:rust`, `audience:mcp`, and
`audience:security`) replace the corresponding `wedge:*` labels through stable-ID rename rows where
the source exists. Audience labels are inactive in forms, workflows, filters, and site links until
the destination label is provisioned. Existing `wedge:*` assignments remain valid during the
transition. The migration records the three public seed repositories where those source labels are
absent; it does not invent assignments there.

`priority:p0` through `priority:p3`, `status:needs-triage`, `status:blocked`, and the `area:*`
overlays are definitions for future review. A label-sync check does not assign them or establish an
issue's evidence level. Security details continue to use the private reporting path in
[`SECURITY.md`](SECURITY.md).

## First safe tasks

Each task is bounded, needs no game, no model, and no credentials, and is filed under the
`first-task` label. The audience label shown below is the post-provisioning name; existing issues
may still carry the corresponding `wedge:*` label while the migration is in progress.

1. **Add a gateway fence-case fixture** (`audience:rust`). Extend the proof recipe with one more case
   the gateway already tests at `sts2-gateway@e7bce21`, for example `WrongCaller`, `WrongSession`,
   `WrongLease`, `Missing`, or `Expired`, using only the crate's public API and injected fakes.
   Submit it through the [proof-recipe form](.github/ISSUE_TEMPLATE/proof-recipe.yml) with the
   command, the expected output, and its SHA-256.
2. **Record a contract observation on the MCP seam** (`audience:mcp`). Read `tests/seam.rs` in
   `sts2-mcp-server` and the tool schema, then describe one observed behavior of the tool-call to
   gateway-request mapping, or an adapter example against the schema, through the
   [contract-observation form](.github/ISSUE_TEMPLATE/contract-observation.yml).
3. **Write a security or failure-handling note** (`audience:security`). Check one fail-closed case in
   `crates/gateway/tests/control_plane.rs` against the claim on the evidence page and report
   agreement or disagreement. Anything exploitable goes through [SECURITY.md](SECURITY.md) instead.
4. **Fix a clarity problem on a public page** (`audience:player`, `documentation`). If a label, term, or
   sentence on the site or a README is confusing or unsupported, file it through the
   [evidence form](.github/ISSUE_TEMPLATE/evidence.yml) or open a small pull request against the
   page.

## Running the proof recipe

The recipe lives in the site repository at `recipes/gateway-lease-fence` and depends on
`sts2-gateway` by git URL and pinned revision. Prerequisites: Rust 1.97.1 via `rustup` (selected by
the recipe's `rust-toolchain.toml`), `git`, and network access for the first build's fetch.

```
cd recipes/gateway-lease-fence
cargo run --locked --release > out.json
sha256sum out.json fixture.json                       # Linux, macOS, Git Bash
Get-FileHash out.json, fixture.json -Algorithm SHA256 # PowerShell 7
```

Both hashes must be `1115b6f6fab379ddf161614d783c65f92be11f2fbcfcc41d3b12fc648fa6695d`. Use a
plain `>` redirect; `Out-File` rewrites line endings. The program reads no environment variables,
writes nothing but stdout, and involves no model or provider. Mode: deterministic replay of
repository tests, not live game compatibility.

## How pull requests are reviewed

1. A maintainer checks the boundary rules above and the compatibility classification you gave
   (internal, additive-compatible, safety correction, deprecation, or breaking).
2. Evidence is read before code: the exact commands you ran and their results, and the label on
   each claim. Reviewers must be able to tell evidence from assumption.
3. Formatting, lint, tests, policy, and documentation checks must pass in CI; a green run does not
   substitute for review.
4. Review feedback is about the change, not the person. Resolve concerns or explain why not.
5. A maintainer merges. Contributors and agents never merge their own work.

Small documentation corrections and focused tests need no prior design discussion. Changes to
routes, tools, threading, shutdown, listener exposure, authentication, or dependencies do: open an
issue first.

## Licensing of contributions

By submitting a change you confirm you may license it under the repository's MIT license and that
you have identified any copied, generated, or adapted material and kept its notices. No contributor
license agreement or sign-off is required.

## What is never required

Stars, forks, follows, shares, or posts about the project are never a condition of contributing,
of being reviewed, or of being credited.

AI-Ascension is an independent project. It is not affiliated with or endorsed by Mega Crit or Valve and grants no rights to game files, assets, or marks. No game files are stored or distributed.
