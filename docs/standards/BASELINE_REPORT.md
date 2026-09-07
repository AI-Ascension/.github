# Standards baseline report

Status: source-derived and locally validated, 2026-09-07. This report records the maintained
baseline and its evidence boundary; it is not a claim that every adopter has merged or enabled it.

## Authority and inventory

`standards/repositories.yaml` records 13 reviewed `AI-Ascension` repositories with repository IDs,
node IDs, default branches, exact baseline commits, owners, language scopes, and adoption state.
The naming authority remains the aggregate `planning/naming_conventions/NAMING_CONVENTIONS.md` and
`naming-registry.yaml`; this bundle records the stable rule IDs without copying that registry.

The canonical source bundle is `AI-Ascension/.github`. A local lock names the source commit and the
SHA-256 bundle digest and the exact generated profile configuration SHA-256. `published: false` remains required until a separate remote publication is
verified. The local sync command verifies the commit's complete `standards/` tree before copying it.

## Rule severity and verification

The maintained ledger keeps the mandatory blocking rules and their exception eligibility. It adds a
verification mode so a metadata command cannot impersonate an owner review:

| Rule family | IDs | Severity | Verification |
| --- | --- | --- | --- |
| Identity, authority, errors, lifecycle, bounds, privacy, ownership | `X-ID-001`, `X-AUTH-001`, `X-ERR-001`, `X-LIFE-001`, `X-TIME-001`, `X-PRIV-001`, `X-OWN-001` | mandatory/blocking | manual, unverified until owner evidence |
| Version and local profile/lock provenance | `X-VER-001`, `X-CI-001` | mandatory/blocking | automated metadata and byte validation |
| Frozen bytes and exception approval | `X-BYTE-001`, `X-EXC-001` | mandatory/blocking | manual owner/contract review; metadata shape is automated |
| Rust lint inheritance and production failure boundaries | `RUST-LINT-001`, `RUST-BOUND-001` | mandatory/blocking | policy tool is automated; production boundary review is manual |
| Managed/native evidence boundary | `MANAGED-BOUND-001` | mandatory/blocking | manual and source-linked; exact-host evidence is separate |
| PHP origin and persistence regressions | `WEB-ORIGIN-001`, `WEB-CONCUR-001` | mandatory/blocking | Composer test command where the target tests cover the assertion |
| Private Compose listeners | `OPS-LISTENER-001` | mandatory/blocking | `bash tests/compose-invariants.sh` |
| Evidence labels | `DOC-EVIDENCE-001` | mandatory/blocking | manual documentation review |

The rules with `verification: manual` use `command: null`. They remain mandatory obligations, but
`standards-sync validate` does not report them as passed. Production exception validation also
rejects fixture-only `local-review:` records and unqueried GitHub URLs; the fixture command has an
explicit fixed date and review mode so its test cannot become an accidental approval path.

## Repository profile map

The profile generator has an explicit plan for each non-excluded repository. It uses observed
workflow commands and real targets; it does not invent `scripts/`, `managed/`, `tests/link-check.sh`,
or generic Docker commands. Rust profile commands retain the existing all-features test/Clippy gates after the six-repository
feature inventory found no declared features. Documentation tests execute separately.

| Repository | Profile | Adoption | Check source |
| --- | --- | --- | --- |
| `sts2-game-core` | `rust-pure` | prepared | `.github/workflows/ci.yml` Rust format, policy, Clippy, tests, and docs |
| `sts2-protocol` | `rust-pure` | prepared | `.github/workflows/ci.yml` artifact checksum and Rust gates |
| `sts2-gateway` | `rust-service` | prepared | `.github/workflows/ci.yml` protocol artifact and Rust gates |
| `sts2-mcp-server` | `rust-service` | prepared | `.github/workflows/ci.yml` artifact test/checksum and Rust gates |
| `sts2-harness` | `rust-service` | prepared | `.github/workflows/ci.yml` patch manifest, artifact, and Rust gates |
| `sts2-game-mod` | `rust-managed` | prepared | `.github/workflows/ci.yml` managed probes and source-only gates |
| `AI-Ascension.github.io` | `web-static` | prepared | `.github/workflows/validate.yml` Node, browser, and pinned recipes |
| `aiascension.tech` | `web-php` | prepared | `composer.json` scripts `lint`, `analyse`, `test`, and `verify` |
| `ai-agent-observability` | `operations` | prepared | `.github/workflows/ci.yml` shell, bootstrap, Compose, and Dockerfile checks |
| `ascension-watchdog` | `planning-bootstrap` | prepared | validated bootstrap docs/config only; no accepted product manifest |
| `ascension-map-visualizer` | `planning-bootstrap` | prepared | validated bootstrap prompt/config only; no accepted implementation |
| `ascension-brand-overhaul` | `brand-package` | excluded | historical `CHECKSUMS.sha256` needs source-aware review before bundle adoption |
| `AI-Ascension/.github` | `org-governance` | ready | canonical validator, fixtures, and link-check fixture |

`excluded` is an explicit state with a reason in `repositories.yaml`; it does not imply a failed
product check or authorize creating a product workspace. `prepared` means a profile plan exists;
it does not mean the adopter has received a local copy, run its checks, or enabled branch protection.

## Local evidence

The canonical tool was checked with Rust 1.97.1 using its locked dependency graph. The observed
local results are:

```text
cargo +1.97.1 test --locked --manifest-path standards/tools/standards-sync/Cargo.toml
15 passed
cargo +1.97.1 clippy --locked --manifest-path standards/tools/standards-sync/Cargo.toml --all-targets -- -D warnings
passed
cargo +1.97.1 run --locked --manifest-path standards/tools/standards-sync/Cargo.toml -- fixture-check --root standards/conformance
3 valid fixtures accepted; 9 negative fixtures rejected
```

These results establish the local validator and fixture behavior. They do not establish adopter CI,
remote publication, merge, protected-check activation, host/runtime behavior, deployment, release,
mail, game, or provider evidence.

## Baseline observations retained for comparison

All six original Rust workspaces passed locked metadata discovery with Rust/Cargo
1.97.1 (edition 2024, declared MSRV 1.97.1). There were 18 workspace packages in
total and no declared feature entries. Exact original revisions are retained in
the repository map. The original compiler, edition and runtime dependency pins
remain unchanged; TOML dependencies added to two owner policy tools are tooling.

Replays of the exact original core and game-mod revisions in disposable source
copies recorded the existing format/Clippy/all-target test commands. Core passed
all five metadata/policy/format/Clippy/test commands with 42 tests. Game-mod passed
metadata, format, Clippy and 77 tests; its strict policy returned exit 1 because a
255-nonblank-line managed source file exceeded the preferred limit of 250. This
is the reproduced preferred-size/strict-mode mismatch, not a hard-size breach.
These are exact-source baseline replays, not a claim that every full suite in the
organization was executed before the first implementation edit.

Managed baseline evaluation covered 13 projects in Debug and Release. All 26
project/configuration pairs had the required settings and twelve host-free Release
projects built. Eight existing source-linked probe programs passed; the Windows
bridge identified its unrun Windows process portion explicitly. Check-only C#
formatting returned exit 2 with 120 diagnostics across 132 source files. The host
probe requires separately supplied assemblies and was not built.

The brand package's existing integrity check failed for its historical
`.gitignore` digest, leaving 40 of 41 package tests passing. This result is retained
as an exclusion reason; task work did not update that historical checksum.

The source-derived PHP origin, operation-serialization and logging findings were
reproduced with isolated synthetic fixtures before their respective behavior
corrections. Browser/publication and structured Compose checks were then exercised
with real local tools and negative mutations. The final evidence, precise tool
versions, remaining limits and revisions are in [the adoption report](ADOPTION_REPORT.md)
and [the implementation ledger](IMPLEMENTATION_LEDGER.md).
