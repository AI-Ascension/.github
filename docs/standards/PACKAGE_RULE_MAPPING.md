# Supplied rule mapping

All 37 `ASC-*` identifiers are retained in the executable [rule catalog](../../standards/rules.yaml). The 18 earlier local IDs remain as compatible references; they do not authorize ordinary safety exceptions. Owner-specific check commands and measured outcomes are in the [adoption report](ADOPTION_REPORT.md). The case IDs below refer to the supplied 50-case matrix.

A rule marked `manual` still requires owner evidence: metadata validation does not execute its product checks or certify its semantic obligation. The shared catalog uses `automated` only for a direct scoped command; combined review/test obligations stay manual even where component tests exist.

| Supplied rule | Earlier/local enforcement | Acceptance IDs | Evidence family |
| --- | --- | --- | --- |
| `ASC-OWN-001` | X-OWN-001, X-AUTH-001 | INV-04, CON-03 | Owner architecture review and existing boundary tests |
| `ASC-CON-001` | X-ID-001, X-VER-001, X-BYTE-001 | CON-01, CON-02 | Owner contract tests and frozen-byte audit |
| `ASC-CON-002` | X-ID-001, X-VER-001, X-BYTE-001 | CON-01, CON-02 | Owner contract tests and frozen-byte audit |
| `ASC-ERR-001` | X-ERR-001 | CON-03, PHP-06 | Owner unknown-result and safe error regression tests |
| `ASC-RES-001` | X-TIME-001, X-LIFE-001 | NET-02, PHP-04, OPS-02 | Bounded resource and lifecycle tests |
| `ASC-SEC-001` | X-PRIV-001 | PHP-02, PHP-06, PHP-07, WEB-02, CI-05 | Input/redaction regressions and artifact review |
| `ASC-SEC-002` | X-PRIV-001 | PHP-02, PHP-06, PHP-07, WEB-02, CI-05 | Input/redaction regressions and artifact review |
| `ASC-EFX-001` | X-CI-001 | OPS-03, REP-01, END-01 | Isolated fixture execution and command review |
| `ASC-DEP-001` | X-VER-001 | RUS-07, PHP-08, REP-02 | Lockfile, compiler, target and dependency inventory |
| `ASC-FMT-001` | Owner formatter configuration | CON-01, REP-01 | Check-only native formatters; frozen fixtures excluded |
| `ASC-SIZE-001` | Owner SIZE001/SIZE002 and policy version 2 | POL-01, POL-02, POL-03 | Versioned owner policy positive/negative fixtures |
| `ASC-SIZE-002` | Owner SIZE001/SIZE002 and policy version 2 | POL-01, POL-02, POL-03 | Versioned owner policy positive/negative fixtures |
| `ASC-DES-001` | Owner design guidance | POL-02 | Advisory design review; no automated semantic claim |
| `ASC-PROV-001` | X-VER-001, X-BYTE-001 | INV-03, CON-01, END-01 | Typed source records and native checksum commands |
| `ASC-EXC-001` | X-EXC-001 | EXC-01, EXC-02, EXC-03 | Canonical approval/date/path and safety-suppression negatives |
| `ASC-RUS-001` | RUST-LINT-001, RUST-BOUND-001 | RUS-01 through RUS-08 | Owner repo-policy, compiler/Clippy and separate doctests |
| `ASC-RUS-002` | RUST-LINT-001, RUST-BOUND-001 | RUS-01 through RUS-08 | Owner repo-policy, compiler/Clippy and separate doctests |
| `ASC-RUS-003` | RUST-LINT-001, RUST-BOUND-001 | RUS-01 through RUS-08 | Owner repo-policy, compiler/Clippy and separate doctests |
| `ASC-RUS-004` | RUST-LINT-001, RUST-BOUND-001 | RUS-01 through RUS-08 | Owner repo-policy, compiler/Clippy and separate doctests |
| `ASC-NET-001` | MANAGED-BOUND-001 | NET-01, NET-02, NET-03 | Evaluated settings and source-linked probes; exact-host limits separate |
| `ASC-NET-002` | MANAGED-BOUND-001 | NET-01, NET-02, NET-03 | Evaluated settings and source-linked probes; exact-host limits separate |
| `ASC-PHP-001` | WEB-ORIGIN-001, WEB-CONCUR-001 | PHP-01 through PHP-08 | PHPUnit, static analysis, formatter and platform records |
| `ASC-PHP-002` | WEB-ORIGIN-001, WEB-CONCUR-001 | PHP-01 through PHP-08 | PHPUnit, static analysis, formatter and platform records |
| `ASC-PHP-003` | WEB-ORIGIN-001, WEB-CONCUR-001 | PHP-01 through PHP-08 | PHPUnit, static analysis, formatter and platform records |
| `ASC-PHP-004` | WEB-ORIGIN-001, WEB-CONCUR-001 | PHP-01 through PHP-08 | PHPUnit, static analysis, formatter and platform records |
| `ASC-WEB-001` | Owner static site tooling | WEB-01, WEB-02 | Node and Chromium suites; publication inventory |
| `ASC-WEB-002` | Owner static site tooling | WEB-01, WEB-02 | Node and Chromium suites; publication inventory |
| `ASC-OPS-001` | OPS-LISTENER-001, X-LIFE-001 | OPS-01 through OPS-04 | Shell/PowerShell fakes, bootstrap and Compose negatives |
| `ASC-OPS-002` | OPS-LISTENER-001, X-LIFE-001 | OPS-01 through OPS-04 | Shell/PowerShell fakes, bootstrap and Compose negatives |
| `ASC-OPS-003` | OPS-LISTENER-001, X-LIFE-001 | OPS-01 through OPS-04 | Shell/PowerShell fakes, bootstrap and Compose negatives |
| `ASC-CI-001` | X-CI-001 | CI-01 through CI-05 | Profile/aggregate negatives and owner workflow review |
| `ASC-CI-002` | X-CI-001 | CI-01 through CI-05 | Profile/aggregate negatives and owner workflow review |
| `ASC-CI-003` | X-CI-001 | CI-01 through CI-05 | Profile/aggregate negatives and owner workflow review |
| `ASC-TST-001` | Owner regression suites | RUS-01 through CI-05 | Executable counterexamples recorded per repository |
| `ASC-EVD-001` | DOC-EVIDENCE-001 | END-01 | Exact adoption/check ledger and independent review |
| `ASC-REP-001` | X-CI-001 | REP-01, REP-02 | Idempotent sync and recorded tool/prerequisite evidence |
| `ASC-PLN-001` | Planning profiles | INV-04, POL-06 | Bootstrap source/configuration inventory rejects product scaffolding |

## Exception interpretation

The package permits ordinary exceptions only for `ASC-FMT-001`, `ASC-SIZE-001`, `ASC-SIZE-002` and `ASC-DES-001`. The validator now rejects eligibility changes on every other rule even if a catalog claims otherwise. Source-linked regression tests also reject attempts to use privacy, error or production-panic rules in a style exception. No exception is installed.

The proposed schema is an authoring format with proposed/revoked/disabled states. The implemented schema describes an active candidate, uses `compensating_tests`, `reviewed_on`, `expires_on` and `removal_criteria`, and binds repository identity through the enclosing pinned profile. These are explicit field-format adaptations, not approval equivalence. The supplied pending example remains unapproved and cannot be installed. All production exception activation still fails closed until independent review evidence can be verified; a valid date or URL is insufficient.

The original preferred/hard budgets are retained at their owners. No new web/operations hard ceiling or blanket formatting exception was introduced. Safety or architecture changes require their separate owner authority, outside the ordinary exception mechanism.
