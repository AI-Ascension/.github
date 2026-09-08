# Coding standards adoption report

Status: local implementation and validation; external activation remains separate.

This is the local implementation handoff for the 2026-09-07 AI-Ascension coding
standards task. It covers all 13 accessible repositories from the paginated
inventory. The source is prepared in isolated branches named
`codex/standards-baseline-20260907` and `codex/standards-current-20260907`; no branch was pushed or merged. Seven accepted upstream heads advanced during the task and the local implementation was carried onto those refreshed commits. The original baseline branches remain available; the operations delivery uses the isolated `ai-agent-observability-current` checkout.

The canonical bundle is pinned to commit
`4d774b58c4e18f7090df5a3799703f52940c998d` of `AI-Ascension/.github`, with digest
`sha256:0a444bf2404d384aabcef34fee47b7ab73b2735c3210b6852ea4a23f1f60f4f0`.
Every local lock preserves `published: false`, hashes all 36 bundle files and
hashes the generated root profile configuration. This is local byte provenance,
not a remote signature or protected owner approval.

## Repository revisions and results

| Repository | Validated implementation commit | Local result |
| --- | --- | --- |
| `aiascension.tech` | `4b309e8319a6061aa00b32266cd2c297409d6e04` | 51 PHP tests/128 assertions; 2 Node tests; 5 Chromium cases; PHP 8.1 production lane 11 checks |
| `sts2-game-core` | `902cdbbf64940d41028ee6cdc2a52945f022afb9` | 61 tests + 2 doctests; native gates pass |
| `sts2-game-mod` | `4af930158e3d211dc480a10a3e248f56138c0ff2` | 98 tests + 5 doctests; native gates pass; 13 managed projects/26 settings pairs and source probes pass |
| `sts2-gateway` | `d0611ae235b45e06c24dadc96ed6a2d78fbba236` | 147 tests + 2 doctests; native gates pass |
| `sts2-mcp-server` | `e8a34bd9e3d35662046099e2f3d2208ae359e35a` | 143 tests + 2 doctests; native gates pass; 1 default-ignored peer case separately passes |
| `sts2-harness` | `8bca6e37abaa31043e4a7255bf8e6803780703d2` | 241 tests + 2 doctests; native gates pass; 1 default-ignored synthetic Runtime-v4 composition case separately passes |
| `sts2-protocol` | `86a48daaf42c2fa86a7ed73103cf640fef3cb64e` | 80 tests + 2 doctests; native gates pass |
| `.github` | `c62d898756c9be713ee2424d29b1218f24c139eb` | 17 tool tests; 3 positive/9 negative fixtures; 15 link cases; 12 adopter validations |
| `AI-Ascension.github.io` | `c56bb421455fd5f1bceed42572d775e77dd170d0` | 10 Node tests; 4 Chromium cases; both historical recipes match |
| `ai-agent-observability` | `b444bf6d146943dfb8f87f68aa66e3eec28edff2` | Shell/bootstrap/config/query fake gates pass; 43 model, 18 rendered negatives and 24 required-setting cases; buildx unverified |
| `ascension-watchdog` | `d73f2b2c4a75806e9a089f3a2f0a5b17f3bb12b3` | 7 Markdown, 2 JSON and 1 YAML inputs checked; product absent as intended |
| `ascension-map-visualizer` | `21f04cef819514bed20d986e21f43b3d669b3665` | 3 Markdown, 1 TOML and 1 YAML inputs checked; product absent as intended |
| `ascension-brand-overhaul` | `851ea5e0744fca10e86fea4dbc36118c4bb68a75` | Explicitly excluded; historical checksum failure leaves 40/41 baseline tests passing |

The canonical row identifies the implementation/lock commit before this report.
The final documentation commit and every final branch tip are recorded in the
local delivery handoff. All other rows identify the final implementation tips.
Rust counts include owner policy tests; the separate documentation lane executes
15 cases across 15 runnable libraries. The native `cdylib` and binary-only tools
are identified as unsupported doctest targets, without claiming empty passes.
The refreshed Rust source received all seven full command groups again. The initial protocol all-target Clippy failure was reproduced and fixed with test-only `expect_used` allowances in two new Runtime-v4 fixture files; the full protocol suite then passed. The 770 regular tests exclude two default-ignored executable integration cases, both separately executed successfully.
The maintained repository IDs, actual default branches and exact baseline
commits are in [the reviewed inventory](../../standards/repositories.yaml).

## Commands actually exercised

Each adopter's `standards-profile.toml` is the exact command/target matrix. Commands run from
the repository-relative directory in each check's `target` field.
Normal validation is local to that repository and does not require a sibling
checkout or floating policy branch. Provision the pinned toolchain and locked
dependencies first; local Rust verification used `--offline` after provisioning.

- Shared: `cargo +1.97.1 fmt --manifest-path standards/tools/standards-sync/Cargo.toml --check`,
  locked tests, Clippy with `--all-targets -- -D warnings`, `fixture-check`,
  `validate --root .`, and two sync runs with byte/mtime comparison.
- Rust: locked Cargo metadata, `cargo fmt --all --check`, owner-local
  `repo-policy --strict`, workspace/all-target/all-feature Clippy and tests,
  separate workspace documentation tests, and 32 artifact checksum commands from
  their actual target directories (343 successful file checks). The production
  check uses `--lib --bins` and `-F` for the five prohibited Clippy constructs;
  all-target checks retain scoped test allowances. Exact final case counts appear above.
- Managed: `check-managed.sh settings`/`format`, `test-managed-settings.sh`,
  `test-managed-abi.sh`, PowerShell parser/self-test/process fakes and the existing
  real source-linked probe projects. Thirteen existing synthetic shell command
  groups retained in native CI also passed.
- PHP: Composer validate/verify, CS Fixer, PHPStan and PHPUnit with isolated
  process/storage/mail fakes; PHP 8.3.6, 51 tests and 128 assertions. A separate PHP 8.1.2 production-only installation (Composer 2.8.12, no development packages) passed 11 main-API checks and 78 PHP syntax checks, plus syntax checks on the two addon entrypoints; addon runtime dependencies remain unverified.
- Sites: locked npm tooling, `npm run verify`, Chromium and publication negatives.
  Both Pages recipe wrappers also ran actual locked historical Rust recipes and
  compared exact fixture bytes.
- Operations: shell syntax, ShellCheck 0.10.0, bootstrap, validation regressions,
  structured Compose 2.39.4/jq 1.8.1, model and rendered-source negatives,
  invariants and required settings. No container daemon was needed or started.
- Bootstrap: `check-bootstrap --root .` verifies local adoption and real
  Markdown/JSON/TOML/YAML inventories without initializing a product workspace.

The observed tool versions were Rust/Cargo 1.97.1, .NET SDK 9.0.317,
PowerShell 7.4.13, Node 24.15.0/npm 11.12.1, ESLint 9.35.0,
Prettier 3.9.6, Playwright 1.63.0, PHP 8.3.6/Composer 2.10.3,
PHPUnit 11.5.55, PHPStan 2.2.13, PHP CS Fixer 3.95.24,
ShellCheck 0.10.0, Compose 2.39.4 and jq 1.8.1. Frontend and PHP
analysis dependencies remain development-only. PowerShell evidence covers
syntax and owned process fakes, not a PSScriptAnalyzer or Windows host run.

A completed process is not automatically a passing acceptance case. The tests
reject missing targets, changed bytes, unsafe paths, weak effective settings,
failed recipe processes and bad aggregate results. Genuine unsupported host or
crate targets stay separately identified.

## Severity and remaining debt

| Policy mode | Preferred size | Mandatory finding | Hard size limit |
| --- | --- | --- | --- |
| Version 1, ordinary | warning | diagnostic/error according to existing rule | error |
| Version 1, strict | blocking warning | blocking | blocking |
| Version 2, strict | visible advisory | blocking | blocking |

Only preferred `SIZE001` guidance changed strict-mode classification. The
migration preserves legacy parsing/behavior and keeps mandatory lint, privacy,
configuration and correctness obligations. No production exception was approved
or installed. Manual ownership, architecture, lifecycle and privacy requirements
remain mandatory even where source review is the appropriate verification.

The brand repository remains explicitly excluded because its historical
`.gitignore` checksum already fails. Its package baseline is 40/41 tests; no
historical checksum was rewritten. This is an unresolved source/archive integrity
issue, not a green adoption or an authorized suppression.

## Evidence boundaries and unavailable acceptance

| State | Evidence |
| --- | --- |
| Prepared source | Local explicit commits; separate behavior, formatting, tooling, CI and adoption changes |
| Local checks | Results and adversarial fixtures described here and in the implementation ledger |
| Remote publication | Not performed; no pushed branches or PR links |
| Hosted CI/merge queue | Not executed; workflow source reviewed only |
| Policy merge/adoption | No default branch changed by this task; local adoption is not merged policy |
| Protected-check activation | Not inspected/changed as an activation action; external owner configuration remains separate |
| Runtime/deployment/release | No host/game/provider/mail/service/deployment/release result claimed |

The operator supplied the complete original package. [The package comparison](COMPANION_COMPARISON.md)
records checksum/schema validation, all 37 rule IDs, the exception repair and corrected
source object types. [The acceptance matrix](../../tests/ACCEPTANCE_MATRIX.md) maps the
supplied cases to local evidence and explicit external limits. The requested
three descendant layers were unavailable in the child tool environment; actual
execution metadata showed fourteen native Luna/max descendants across waves, all at
depth one. A stopped alternate-client attempt was not counted as valid ancestry.

Exact-host assemblies, actual Windows process integration, native live unload/
thread behavior, cPanel runtime/extensions and SMTP/MTA delivery remain unverified.
The default MCP suite deliberately ignores one peer integration requiring an
explicit reviewed gateway binary. That lane was separately executed and passed
1/1 using current local gateway/MCP executables, synthetic credentials and
ephemeral loopback listeners; it asserts no downstream game connection. The new harness Runtime-v4 composition case also passed 1/1 with the reviewed current gateway, MCP and harness binaries, an environment-cleared synthetic provider bridge and synthetic downstream; this is executable composition, not live gameplay.
Docker/buildx checks were unavailable locally. The native game-mod `cdylib` is not
an executable Cargo doctest target; its source-linked ABI tests are separate.

No push, PR/issue, merge, protection setting, publication, service installation,
site deployment, live mail, game launch, runtime provider call or production-data
mutation was performed. Original shared working trees were not used for edits.

## Rollback

Use the final per-repository rollback record with a clean, isolated review branch.
Revert the listed commits in newest-first order. Removing an adoption requires
its native validator/CI integration to be reverted or deliberately migrated too;
removing the copied files alone would correctly make required validation fail.
Restore the profile and lock together. To roll back
all task source changes, revert the recorded task commits in newest-first order
through normal owner review; PHP security fixes and native behavior corrections
must not be silently removed as a formatting rollback. Do not reset, clean,
force-push or rewrite unrelated history. There is no deployment, volume, saved
game or service rollback associated with these local commits.

See [the implementation ledger](IMPLEMENTATION_LEDGER.md) for before/after
findings, review repairs, case details and remaining limits.
