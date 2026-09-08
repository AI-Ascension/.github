# Implemented acceptance matrix

This matrix derives from the explicit implementation prompt and the complete
subsequently supplied package, including its original 50 acceptance cases.
Package checksums and source types were independently verified. Executable
assertions remain distinct from source review and unavailable external acceptance.

| Case | Executable evidence | Result and boundary |
| --- | --- | --- |
| Every accessible repository has an accurate profile or exclusion | `standards-sync validate`, `every_adopting_repository_has_a_valid_generated_profile`, repository-map validation | 13 stable repository IDs/default branches/baseline heads inventoried; 12 local adoptions validate, brand explicitly excluded with a reproduced baseline failure. |
| All known workspace/package/project entry points accounted for | Owner-local `repo-policy` metadata/inheritance/nested-workspace tests; managed exact project inventory | Six Rust workspaces checked; managed inventory requires exactly 13 current projects, evaluated in Debug and Release. Product initialization is rejected in bootstrap profiles. |
| Missing/weak effective configuration fails | Rust inheritance/override fixtures; `test-managed-settings.sh` | Missing inheritance, weakened levels/settings, missing/partial/empty project inventory and formatting defects are negative cases. |
| Forbidden production constructs block while legitimate test code remains valid | Compiler/Clippy gates and owner-local scoped fixtures | Six executable negative fixture variants prove production unwrap/expect/panic/todo/unimplemented and a local allow override fail under the production Clippy `-F` gate; pure Rust unsafe remains forbidden; test allowances stay scoped. |
| Severity migration preserves mandatory failures | Owner-local version-1/version-2 strict-mode tests | Legacy strict warnings still block. Version 2 reports preferred `SIZE001` as advisory; mandatory findings and hard limits still block. |
| Invalid/expired/unapproved exceptions do not suppress rules | Canonical exception/date/review-mode conformance tests | Fixture-local approval and unqueried review URLs cannot authorize production exceptions. No actual exception was installed. |
| Paths, symlinks, ignores, nested workspaces and src/bin are deliberate | Canonical sync/path tests, Rust policy fixtures, eight independently reproduced bootstrap escapes | Missing/differing/symlinked managed destinations and undeclared source/manifests fail. Only the exact standards compiler-output directory is ignored. |
| Frozen contract/artifact bytes remain unchanged | Native checksum gates and original-commit byte audit | 414 files under the current schema/artifact/conformance/fixture/evidence scopes compared; zero changed or missing. Separately, all 343 checksums in 32 artifact inventories passed. Historical website recipes were also compared separately. |
| PHP origin/privacy/input correctness | Composer PHPUnit regressions, PHPStan and CS Fixer | 51 tests/128 assertions pass; synthetic origin, shape, bounds, error mapping and log-marker cases use no real subscriber data or mail. |
| PHP operation serialization and failures | Process/barrier, duplicate, increment, corrupt-data, write/lock/interruption fixtures | Pass locally under PHP 8.3.6; no database migration or cross-host durability claim. |
| Browser behavior is distinct from synthetic DOM tests | Node and Chromium suites in both sites | PHP site: 2 Node/5 browser cases; Pages: 10 Node/4 browser cases. Keyboard/focus/error/reduced-motion behavior checked in Chromium. |
| Development files cannot become site artifacts | Explicit publication inventories and negative publication fixtures | Linked/missing runtime inputs fail; tooling, dependencies, tests, standards and reports are omitted; repeated output hashes match. |
| Historical recipes compare actual output bytes | Pages bounded recipe wrapper and runner negatives | Both real pinned recipes return success and exact fixture bytes; failed/timed-out/signalled/mismatched output is rejected. |
| Managed source evidence does not imply host compatibility | Existing source-linked probes, ABI mutation tests and PowerShell fakes | Source/settings/format/layout/buffer/process-fake checks pass. Exact host assemblies, Windows process execution and native unload/thread acceptance remain unverified. |
| Empty/missing/skipped checks cannot substitute for intended evidence | Missing target/project tests, all-profile generation, CI reachability review, aggregate truth table | Canonical/managed missing-target cases reject. Game-mod aggregate accepts only all-success across 125 status combinations. Runnable doctest counts and genuine unsupported targets are recorded separately. |
| Repeat check/sync is deterministic and preserves source/Git state | Real disposable Git sync test; all-adopter second sync; default Cargo-target review | Copied bytes and mtimes are stable; independent default-target runs preserved Git status. Dependency provisioning/build output is separate from source mutation. |
| Shell/config checks use bounded isolated fixtures | ShellCheck, bootstrap/dotenv tests, Compose structured/source negatives and 13 existing game-mod shell groups | All executed local fixture groups pass. Docker/buildx unavailable; no services, containers, VMs or real hosts were changed. |
| CI remains compatible and least-privileged | Workflow source/identity/event/permission/action/timeout review and negative committed-patch fixtures | Existing check names preserved, immutable actions and read-only validation permissions retained. Hosted execution, protection configuration and merge queue execution remain unverified. |
| Requested orchestration ancestry is real | Actual execution metadata and native agent inventory | Fourteen native descendants across waves used requested Luna/max, all at depth one. Depth-two/three tools were unavailable; no claim of the required three descendant layers. |
| Unauthorized external effects do not occur | Scoped local execution/commit ledger and remote head comparison | No push, PR, merge, protection change, deployment, release, service installation, live mail/game/provider call or production-data mutation was performed. |

Use [the implementation ledger](../docs/standards/IMPLEMENTATION_LEDGER.md) for
before/after details and [the adoption report](../docs/standards/ADOPTION_REPORT.md)
for exact local revisions, commands, counts, remaining debt and rollback.

The [received 50-case checklist](PACKAGE_ACCEPTANCE_CASES.md) preserves the exact
case IDs, scenarios and observations used for the package follow-up.
