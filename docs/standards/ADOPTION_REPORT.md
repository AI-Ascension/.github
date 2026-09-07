# Coding standards adoption report

This is the local implementation handoff for the 2026-09-07 AI-Ascension coding
standards task. It covers all 13 accessible repositories from the paginated
inventory. The source is prepared in isolated branches named
`codex/standards-baseline-20260907`; no branch was pushed or merged.

The canonical bundle is pinned to commit
`0f743fd4cce4428f813a6d6f50c51d4fb901561b` of `AI-Ascension/.github`, with digest
`sha256:326b45c4ee3421788da0ec5c258b0c1fc9f562034a2fcac260c50223b5b9f13d`.
Every local lock preserves `published: false`, hashes all 36 bundle files and
hashes the generated root profile configuration. This is local byte provenance,
not a remote signature or protected owner approval.

## Repository revisions and results

| Repository | Validated implementation commit | Local result |
| --- | --- | --- |
| `aiascension.tech` | `fdb23feb7cdcd55b6508fecbe575e03dd8bfbab9` | 49 PHP tests/121 assertions; 2 Node tests; 3 Chromium cases |
| `sts2-game-core` | `bb72a7e09639588714d323174df310a18768e30a` | 57 tests + 2 doctests; native gates pass |
| `sts2-game-mod` | `b52674be3c24e4af502d29635b1f55fba765503c` | 93 tests + 5 doctests; native gates pass; 13 managed projects/26 settings pairs and source probes pass |
| `sts2-gateway` | `8d19ffd6a61b38b47293c45cd0fa97d6bcc06f08` | 138 tests + 2 doctests; native gates pass |
| `sts2-mcp-server` | `bc4c1fba00b3706ed6fbfbcf80f7a5dcfa7f1bd2` | 128 tests + 2 doctests; native gates pass; 1 default-ignored peer case separately passes |
| `sts2-harness` | `a87c9e26eae96d9de334bff2ab4318c64f86aa2a` | 197 tests + 2 doctests; native gates pass |
| `sts2-protocol` | `1114288b7fccbe1bc0076757723d6f20d0fdf644` | 69 tests + 2 doctests; native gates pass |
| `.github` | `0f30e04e4eabcd50b035e76eba424d49979c1da0` | 15 tool tests; 3 positive/9 negative fixtures; 15 link cases; 12 adopter validations |
| `AI-Ascension.github.io` | `0004bc545497abd7531a2b071d9f0d78928e6b35` | 10 Node tests; 3 Chromium cases; both historical recipes match |
| `ai-agent-observability` | `1f35d7b7c5784392e27c7ba936089e8748f20dea` | Shell/bootstrap/config gates pass; 43 model and 18 rendered negative cases; buildx unverified |
| `ascension-watchdog` | `47eda974594ff330ab82d5c51feba209cdb824c2` | 7 Markdown, 2 JSON and 1 YAML inputs checked; product absent as intended |
| `ascension-map-visualizer` | `c34978f4ff707f17bc82d38fdcd853ad583134d9` | 3 Markdown, 1 TOML and 1 YAML inputs checked; product absent as intended |
| `ascension-brand-overhaul` | `851ea5e0744fca10e86fea4dbc36118c4bb68a75` | Explicitly excluded; historical checksum failure leaves 40/41 baseline tests passing |

The canonical row identifies the implementation/lock commit before this report.
The final documentation commit and every final branch tip are recorded in the
local delivery handoff. All other rows identify the final implementation tips.
Rust counts include owner policy tests; the separate documentation lane executes
15 cases across 15 runnable libraries. The native `cdylib` and binary-only tools
are identified as unsupported doctest targets, without claiming empty passes.
The latest small policy/CI edits also received focused policy and workflow checks.
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
  separate workspace documentation tests, and 21 artifact checksum commands from
  their actual target directories (270 successful file checks). The production
  check uses `--lib --bins` and `-F` for the five prohibited Clippy constructs;
  all-target checks retain scoped test allowances. Exact final case counts appear above.
- Managed: `check-managed.sh settings`/`format`, `test-managed-settings.sh`,
  `test-managed-abi.sh`, PowerShell parser/self-test/process fakes and the existing
  real source-linked probe projects. Thirteen existing synthetic shell command
  groups retained in native CI also passed.
- PHP: Composer validate/verify, CS Fixer, PHPStan and PHPUnit with isolated
  process/storage/mail fakes; PHP 8.3.6, 49 tests and 121 assertions.
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

The operator subsequently supplied the proposed BASELINE.md and AUDIT_FINDINGS.md;
[the companion comparison](COMPANION_COMPARISON.md) records their reconciliation.
The original manifests, exception schema, sources.json and acceptance matrix remain
unavailable. [The implemented matrix](../../tests/ACCEPTANCE_MATRIX.md) therefore
derives from the explicit prompt and received prose, not those unseen package files. The requested
three descendant layers were unavailable in the child tool environment; actual
execution metadata showed eleven native Luna/max descendants across waves, all at
depth one. A stopped alternate-client attempt was not counted as valid ancestry.

Exact-host assemblies, actual Windows process integration, native live unload/
thread behavior, cPanel runtime/extensions and SMTP/MTA delivery remain unverified.
The default MCP suite deliberately ignores one peer integration requiring an
explicit reviewed gateway binary. That lane was separately executed and passed
1/1 using current local gateway/MCP executables, synthetic credentials and
ephemeral loopback listeners; it asserts no downstream game connection.
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
