# Implementation ledger

This ledger records source changes and observed local evidence from 2026-09-07.
The maintained rules and repository map are under `standards/`; this is evidence,
not a second normative policy source. Adoption, hosted CI, owner review, protected
checks and runtime acceptance remain separate states.

## Decisions and evidence

| Boundary | Before | Implemented behavior and evidence |
| --- | --- | --- |
| Shared distribution | No effective local pinned adoption across the inventory | A locked Rust tool verifies the complete committed bundle, repository/profile/owner identity, profile configuration digest and safe local targets. Twelve adopters validate. Second sync preserves bytes and timestamps. |
| Validator correctness | The draft's profile and path checks missed weakening and copy hazards | Seventeen tests cover identity, mandatory command removal/replacement/demotion, missing targets, exact generated output, symlinks, CRLF/digest changes, safe sync, real Git source pins, unapproved/expired exceptions and all twelve generated profiles. Three valid and nine invalid conformance fixtures pass. |
| Bootstrap scope | Planning repositories could be misclassified as excluded or initialized products | Both adopt documentation/configuration checks without a product workspace. The checker parses real Markdown/JSON/TOML/YAML, checks local file links and rejects nested/case-variant manifests, forbidden/unlisted source and ignored-source escapes. Independent review reproduced eight rejected escape mutations. |
| Build output | A copied tool could leave untracked compiler output | Every adopter has the exact standards-tool target ignore. Independent default-target checks preserved Git status while creating 553 ignored compiler-output files per reviewed target. No broad standards ignore is used. |
| Rust severity | Legacy strict mode promoted every warning, including preferred size | Version 1 retains legacy behavior. Version 2 keeps preferred `SIZE001` advisory; mandatory failures and hard limits still block. Existing compiler/edition/MSRV and native command shapes are preserved. |
| Rust entry points | Future omitted/weak member inheritance and nested/ignored entries were insufficiently checked | Owner-local checkers validate effective inheritance/overrides and exact nested-tooling admission. Actual Cargo fixtures reproduce a source-level `allow` bypass of workspace `deny`; separate production Clippy uses `-F` for unwrap/expect/panic/todo/unimplemented. Six invalid constructs/overrides fail while valid comments and scoped tests pass. Mandatory rule IDs cannot be moved into the version-2 advisory list. Final target counts and executable documentation results are recorded in the adoption report. |
| Harness fixture | A shell `read` fixture intermittently exceeded the 250 ms close budget, and its 60,000-byte payload was smaller than the observed pipe capacity | The fixture sends 128 KiB before draining stdin with foreground `cat`; a serialized parent writer demonstrably stalls. Cleanup runs before the negative assertion. The production process source and timeout are unchanged. Original runtime-source fixture failed 14/80 repetitions; final focused pair and all 16 process cases pass. |
| Managed configuration | 120 whitespace diagnostics across 132 baseline C# files; settings were not all verified effectively | Thirteen actual projects are evaluated in Debug and Release. The exact project inventory and twelve settings/format/inventory negative cases pass. Check-only formatting uses an isolated copy; 133 admitted C# files pass. |
| Native/managed boundary | Source-linked layout and error-buffer assertions had gaps | Existing real probes remain. Added buffer/layout assertions and two actual-source ABI mutations exercise fixed-width layout and C calling convention. A synthetic listener-start secret marker reproduced raw exception logging before the fixed event mapping. |
| Operations | Compose checks could miss entrypoint, lifecycle and mount/port option changes | ShellCheck, bootstrap, dotenv non-execution, configuration invariants, one positive/43 invalid models and one positive/18 invalid rendered source cases pass. Rendering isolates ambient interpolation. Compose/jq/ShellCheck downloads are pinned and content-hash checked. |
| PHP origin | Raw suffix origin membership | Exact parsed scheme/host/effective-port membership and deliberate missing-Origin behavior; lookalikes, malformed/opaque origins, invalid ports and valid cases are covered. This is not authentication. |
| PHP persistence | Read/modify/write outside the final write lock | Complete operation serialization, bounded locks/reads, explicit errors and same-directory replacement. Barrier-based process tests cover duplicates, increments, corrupt data, failed writes and interruption. Atomic replacement is not cross-host durability proof. |
| PHP input and logging | Unbounded/invalid shapes and raw exception text | Bounded bodies/fields, scalar/shape checks and fixed error mapping with synthetic markers. PHP 8.3.6 validation passes 49 tests/121 assertions, PHPStan 2.2.13 and CS Fixer 3.95.24. Production constraint remains >=8.1; test tools require >=8.2. |
| Browser source | Native sites lacked scoped development gates and real-browser evidence | Both retain static HTML/CSS/JavaScript. PHP site passes two Node and three Chromium cases; Pages passes ten Node and three Chromium cases. Keyboard/focus, errors and reduced motion are exercised separately from synthetic DOM tests. |
| Publication | Tooling/reports could be copied into publication output | Explicit runtime inventories reject linked/missing inputs and omit standards, dependencies, tests and reports. Repeated publication inventories/digests are stable. Existing font licenses and historical proof bytes remain intact; fonts/assets are not in the shared bundle. |
| Recipe gate | The generated pipeline conflicted with command validation | A bounded checked-in Node wrapper checks Cargo exit/signal/error and exact output bytes. Positive/negative runner tests and both actual historical Rust recipe comparisons pass. |
| CI wiring | Some native policy checks lacked merge-queue events; some profile checks were absent | Existing check names are retained; source wiring adds the missing events and checks. Committed-diff guards check event base SHAs with an initial-commit fallback. Five older Rust steps were also repaired after review showed clean-checkout diffs miss committed whitespace defects; all five extracted guards accepted a clean commit and rejected bad committed content with both base-SHA and fallback paths. Existing source boundary tripwires remain. |
| Aggregate result | Separate managed settings checks needed inclusion in final result | The game-mod aggregate waits on Rust, managed-source and managed-standards and accepts only three successes. All 125 combinations of success/failure/cancelled/skipped/empty were checked; only all-success passed. |
| Frozen data | Baseline contracts and recipes must not be reformatted or repinned | Comparison against original commits covers 441 existing schema/artifact/conformance/fixture/recipe/evidence/checksum files: none changed or disappeared. This is a defined byte inventory, not a claim about every repository byte. |

## Additional existing synthetic checks

All thirteen game-mod shell command groups retained in its CI were run locally
with isolated fake data/executables. Session launch/restore/bridge, provider build,
package installation, authorization, addon selection, development-cycle guards,
self-test, Workshop package staging, runtime lifecycle and GPU provisioning/boot
fixtures all exited zero. The summed observed command wall time was 22.482 seconds.
These remain mandatory wherever the existing native CI runs them, even though the
local profile lists these additional command groups in its extended set. They
establish no actual provider, Workshop upload, host, VM, service or gameplay result.

## Independent review

Independent review found and caused repairs to missing managed inventory checks,
Compose lifecycle/options, PHP shape/port/bounds/error handling, publication
inventory, canonical command generation, bootstrap source escapes, output hygiene,
and CI reachability. Canonical closure reran the pinned tool, all fifteen tests,
Clippy, formatting, conformance, fresh sync and the reproduced negative cases.
The Pages wrapper was independently reviewed. Final CI closure reviewed all 22 scoped workflow YAML files, 33 pinned external
action references and the aggregate failure behavior; the bounded committed-diff
follow-up found no removed native checks. Final Rust results and exact local
revisions appear in the adoption report.

The root retained its model. Execution metadata confirms fourteen actual descendants
across waves requested and ran `gpt-5.6-luna` with `max`; all observed descendants
were at depth one. Child runtimes did not expose native collaboration tools, so
the required coordinator/leaf ancestry is unverified. One earlier worker attempted
an alternate client; it was stopped and its output is not ancestry evidence.
The ceiling of twelve open descendants was not exceeded. Raw runtime identifiers
and logs remain private; no hidden reasoning transcript is part of this ledger.

## Remaining debt and explicit limits

- No exceptions were approved or installed. Example approval strings, fixture-local
  records and unqueried review URLs cannot suppress production rules.
- Preferred Rust size diagnostics remain visible. They are advisory guidance, not
  ignored privacy/correctness failures or a broad suppression baseline.
- The brand package is explicitly excluded: its existing `.gitignore` historical
  checksum mismatch causes its validator and one of 41 package tests to fail.
  Its owner must reconcile the source/archive before adoption; no historical
  checksum was rewritten.
- The full package was received and checksum-verified. All 37 rule IDs are retained,
  the ordinary-exception mismatch was reproduced and fixed, and supplied source
  object types were checked. See the package comparison and rule mapping.
- Exact-host `sts2.dll`/Godot assemblies, actual Windows bridge execution, native
  unload/thread behavior, cPanel PHP/extensions and mail delivery remain unverified.
  Source-linked probes and Linux checks do not prove those boundaries.
- Docker/buildx checks were unavailable locally. Compose parser success is not a
  container build, healthy running service, ingestion, persistence or restart test.
- No branch was pushed, PR/issue opened, merge performed, protected-check setting
  changed, artifact published, service installed, site deployed, mail sent, game
  launched, paid provider called or production data mutated by this task.
- Workflow source is reviewable, but source alone cannot prevent an authorized
  editor from replacing a gate. Owner review and external branch-protection
  activation remain necessary and were not authorized or claimed.

## Complete-package and refreshed-head closure

The received package passed all 20 checksum entries and its three schemas and
instances validated. All 37 proposed rule IDs and 50 acceptance scenarios are
retained in the maintained mapping/checklist. Its 23 blob references matched the
initial source baseline; four entries labelled as trees were actual commits and
are recorded with their resolved trees. These package provenance references are
not claims about every subsequently refreshed source file.

The package exposed an ordinary-exception eligibility mismatch: legacy safety
rules were eligible even though the supplied interpretation permits only four
style/design IDs. A negative fixture reproduced acceptance before the repair.
Catalog and validator now reject forged eligibility for mandatory safety rules;
pending, expired and self-authored approvals still cannot authorize suppression.
The canonical suite now passes 17 tests plus three positive/nine negative fixtures,
including real Git tree/blob IDs rejected as commit pins.

Additional executable cases cover member lint weakening, unsafe outside the native
boundary, a broken documentation example, malformed/unreadable policy, PHP lock
open failure, and empty PHPUnit selections. PHP 8.1 production-only checks are
separate from PHP 8.3 development tests; addon coverage is explicitly syntax-only.
Chromium malicious-content fixtures and rendered-secret publication negatives
were added to both sites. Independent review found no blocking issues in these
fixes or the narrow protocol fixture-only `expect_used` allowances.

A fresh paginated inventory returned 13 unique repository IDs. Seven accepted
default heads had advanced. Local standards commits were carried chronologically
onto new branches rooted at those heads, preserving the earlier branches. The
harness CI conflict was resolved by retaining both upstream split-sandbox guards
and the standards whitespace, production and documentation checks. No task
commits were pushed and no remote merge was performed.

All six refreshed Rust workspaces passed full local checks: 770 tests and 15
documentation cases. Two default-ignored executable cases separately passed:
MCP/gateway peer composition and the new Runtime-v4 harness composition with
synthetic downstream/provider fixtures. Neither establishes live game behavior.
The current protected-byte comparison found no drift in 414 scoped files; 32
artifact checksum commands verified 343 files. The final read-only comparison
of all 13 remote default heads matched the refreshed inventory.

Raw command logs and baseline/carry/rollback records remain in the private local
delivery directory. Exact final branch tips and tested reverse-commit sequences
are in its handoff; the published-source states remain explicitly unperformed.

## Reverification and relative-deadline correction

A repeat of the local checks exposed two shell timing failures. The environment's
Bash `SECONDS` moved forward and backward with wall time; a deterministic
forward-step fixture reproduced premature guardian timeout in the original bridge.
Game-mod commit `23006423ad24992277361b77b9cb5c64f844625b` uses validated Linux/WSL
`/proc/uptime` for the relative handoff deadline. Epoch authorization expiry and
lease limits retain their existing semantics. Clock failure rejects before child
creation. The original bounded reads, receipt checks and owned cleanup remain.

All 29 managed/shell/PowerShell command groups subsequently passed. Twenty paired
bridge/install repetitions passed all 40 commands, including deterministic forward
and backward clock-step cases, malformed/stalled receipts and unavailable-clock
rejection. Game-mod also passed the seven Rust check groups, 98 tests, five separate
documentation cases and an explicit all-target build. ShellCheck had the same 16
companion-source diagnostics as baseline, with no new diagnostics. Independent
review found no blocking issue. This closes the observed local timing regression;
it does not establish Windows, suspend/resume or exact-host runtime behavior.

The final read-only snapshot showed another gateway/MCP/harness head advance.
Each incoming tree delta only changed `RELEASING.md`; nine local standards
commits per repository carried without conflict. Independent review found no
policy, CI, Rust or test interaction. The canonical inventory was updated and
all twelve active copies validate at source `eed9921b5c5d5c41380655bded84f9e2d0aab599`.
Repeated sync preserved bytes and mtimes; prior delivery branches were preserved.
The final protected-path audit compared 481 files against the recorded baselines
with no drift, and all 32 artifact commands verified 343 checksums. Its explicit
selection covers artifact, schema, conformance, fixture, evidence and checksum
paths; this is a scoped comparison, not every repository byte.

The three final carries each passed all seven Rust command groups: gateway 147
tests/two documentation cases, MCP 143/two, and harness 241/two. Combined with
current core/mod/protocol results, the final total remains 770 regular tests and
15 documentation cases. The closing read-only remote check matched all thirteen
recorded default-head baselines. Exact final task commits and rollback sequences
remain in the local handoff, separate from hosted execution and activation.
