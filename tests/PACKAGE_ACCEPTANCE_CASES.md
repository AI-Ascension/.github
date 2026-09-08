# Supplied acceptance cases

These are the 50 received case IDs, scenarios and required observations. The
final disposition follows the package fixtures and current-head source review.
Supporting commands and evidence are maintained in the
[acceptance matrix](ACCEPTANCE_MATRIX.md). `PARTIAL` and `UNVERIFIED` are not passes.

| ID | Scenario | Required observation | Final disposition |
| --- | --- | --- | --- |
| INV-01 | Accessible repository list expands or paginates | Every accessible entry is inventoried once; missing access is explicit. | PASS-inventory: paginated listing, 13 unique IDs |
| INV-02 | Default branch is not main | Actual default branch/commit is used; branch is not changed. | PASS-review |
| INV-03 | Blob/tree identity provided as a head pin | Reject as commit evidence until resolved to an actual commit. | PASS-local |
| INV-04 | Product exists only in an open PR | Distinguish branch evidence from accepted default-branch implementation. | PASS-review |
| RUS-01 | Member omits lint inheritance | Effective policy violation is detected. | PASS-local |
| RUS-02 | Member locally weakens a mandatory lint | Detect or require a valid exact approved exception. | PASS-local |
| RUS-03 | Nested/excluded standalone Rust package | Package is inventoried; no false full-workspace coverage claim. | PASS-local |
| RUS-04 | Production unwrap/expect/panic/todo/unimplemented | Compiler/Clippy enforcement fails on actual constructs. | PASS-local |
| RUS-05 | Test assertions or comments mention banned words | Approved test behavior and non-executable text do not fail spuriously. | PASS-local |
| RUS-06 | Unsafe outside approved boundary | Fail; an approved FFI boundary remains compilable with checked scope. | PASS-local |
| RUS-07 | Dangerous or mutually incompatible feature combination | No live effect; explicit supported matrix and truthful exclusion. | N/A: no declared Cargo features; no live all-features effects |
| RUS-08 | Documentation example is broken | Explicit documentation-test lane fails. | PASS-local |
| POL-01 | Legacy preferred/hard-size behavior | Reproduce current strict behavior; preserve it until reviewed migration. | PASS-local |
| POL-02 | New-profile preferred limit only exceeded | Advisory is visible; it does not become an implicit mandatory failure. | PASS-local |
| POL-03 | New-profile hard limit exceeded | Mandatory failure absent a valid rule-scoped exception. | PASS-local |
| POL-04 | Unreadable or malformed policy/config | Fail explicitly; never run with empty defaults. | PASS-local |
| POL-05 | Production source is under src/bin | It remains inspected, not ignored as generated output. | PASS-local |
| POL-06 | Broad ignored directory hides source | Scope error is detected or explicitly accounted for. | PASS-local |
| POL-07 | Symlink or path escapes the repository | Follow declared policy without escaping or silently claiming coverage. | PASS-local |
| EXC-01 | Pending example or self-authored approval string | No suppression without real applicable approval evidence. | PASS-local |
| EXC-02 | Expired/mismatched/stale path exception | Reject or require explicit renewal; do not silently broaden scope. | PASS-local |
| EXC-03 | Formatter exception attempts to suppress secret rule | Reject; independent security/provenance rules remain active. | PASS-local |
| CON-01 | Formatter changes frozen schema/vector/checksum data | Detect drift; preserve original bytes unless separately versioned. | PASS-local |
| CON-02 | Wire/ABI/environment spelling is normalized | Compatibility check rejects an unapproved external-name change. | PASS-scoped: owner wire/ABI regressions and frozen-byte checks |
| CON-03 | Unknown effect after admission/timeout | Preserve identity and uncertainty; no blind duplicate mutation. | PASS-local |
| NET-01 | Project overrides root nullable/analyzer settings | Evaluated settings reveal override; no false inherited-policy claim. | PASS-local |
| NET-02 | Callback after shutdown or ABI version/length mismatch | Source-linked negative test rejects or contains invalid access. | PASS-source: ABI version/length/layout negatives; live unload UNVERIFIED |
| NET-03 | Proprietary host dependency unavailable | Report host lane not-run/blocked, preserve source-only tests. | PASS-reporting: exact-host lane remains UNVERIFIED |
| PHP-01 | Allowed exact origin and default-port normalization | Accept only the explicitly reviewed origin policy. | PASS-local |
| PHP-02 | Suffix lookalike, opaque/malformed origin, unexpected scheme/port | Reject without network calls; deliberate absent-Origin rule is tested. | PASS-local |
| PHP-03 | Two concurrent unique subscriptions | Neither accepted update is lost. | PASS-local |
| PHP-04 | Concurrent duplicates/rate-limit increments | Serial-equivalent state under defined policy; bounded lock wait. | PASS-local |
| PHP-05 | Corrupt store, failed open/lock/write/replacement | No false persistence success or destructive empty-state overwrite. | PASS-local |
| PHP-06 | Exception includes synthetic secret/path markers | No prohibited marker reaches public response or logs. | PASS-local |
| PHP-07 | JSON array/scalar, scalar field given array, oversize input | Stable bounded errors; no coercion warning leakage. | PASS-local |
| PHP-08 | Production PHP differs from PHPUnit runtime | Separate minima are truthful and tested without unapproved upgrade. | PASS-local |
| WEB-01 | Browser keyboard/focus/reduced-motion/error cases | Local browser verifies behavior separately from synthetic DOM. | PASS-local |
| WEB-02 | HTML receives untrusted content | Content remains data; no unintended executable insertion. | PASS-local |
| OPS-01 | Dotenv contains shell metacharacters | Parsed as data; no command execution. | PASS-local |
| OPS-02 | Native subprocess fails on Bash/PowerShell | Failure propagates; owned cleanup is bounded and scoped. | PASS-fixtures: owned Bash/PowerShell failures and query preflight fakes; Windows host UNVERIFIED |
| OPS-03 | Dry run with existing data/config | No service/data/credential mutation or destructive cleanup. | N/A for operations init/query helpers: no dry-run mode; preservation tested on synthetic early-failure paths; real initialization not run |
| OPS-04 | Host-public publish versus internal container bind | Correct distinction; unapproved exposure fails. | PASS-local |
| CI-01 | Missing tool/target or zero selected tests | Not a successful required check. | PASS-local |
| CI-02 | Matrix job skipped/cancelled/failed | Aggregate cannot falsely report all mandatory checks passed. | PASS-local |
| CI-03 | PR edits policy to disable its own required check | Protected baseline/owner review detects the enforcement change. | PARTIAL: local disable negatives pass; protected external owner gate UNVERIFIED |
| CI-04 | Untrusted PR attempts privileged execution | No secret-bearing/privileged code execution. | PASS-source-review: read-only untrusted workflow; hosted execution UNVERIFIED |
| CI-05 | Public reports include rendered secret configuration | Artifact/log privacy test rejects publication. | PASS-local |
| REP-01 | Run checks and synchronization twice | Identical inputs produce stable diagnostics/configs and no second diff. | PASS-local |
| REP-02 | Warm/cold cache or supported platform changes | Tool/target provenance and actual prerequisites remain explicit. | PASS-provenance: cold/warm dependencies and target records; unavailable platforms explicit |
| END-01 | Completion report | Exact source revisions, commands, effects, failures and blockers are truthful. | PASS-review |
