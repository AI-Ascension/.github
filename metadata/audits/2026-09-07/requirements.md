# Requirement-by-requirement completion audit

This audit maps the supplied specification to inspectable evidence. It records preparation; it does not convert synthetic tests into live verification or confer authorization.

| Specification | Evidence and current disposition |
| --- | --- |
| 1. Authority and operating mode | CLI authorization tests bind operator, target IDs, operations, and digest. Remote write authorization is absent. Only isolated local repository changes and read-only API queries occurred. Publication and apply remain blocked. |
| 2. Three-level Luna/max orchestration | Actual accepted spawns and ancestry limitations are in `orchestration.json`. Root model retained; only depth 1 verified. Required nested execution remains unavailable. This is reported as a verification failure under the specification's explicit fallback. |
| 3. Fresh inventory and default source | Refreshed full API inventory is local/private. `public-inventory-summary.json`, `public-before.json`, source manifests, and `open-pr-collisions.json` expose bounded public evidence. In-scope registry covers all 12 public seed IDs. Nonpublic applicability is recorded locally. Language breakdown and protection rules remain unknown. |
| 4. Topic taxonomy | Canonical map has 89 justified topic entries across all 12 public targets. `topic-reconciliation.md` lists complete before/after sets and decisions. Existing topics are retained. Planning rows remain planning; source evidence is pinned. Independent final source assessment remains pending. |
| 5. Source of truth and governance | Canonical repository and label manifests, management scopes, schemas, governance proposals, and historical source pins exist. Raw private snapshots/authorization/journals are untracked. |
| 6. Labels and consumers | Migration manifest has 54 explicit rows with IDs, source-absent assessments, collision strategies and assignment counts. Scoped palette preserves specialist meanings. Consumer evidence and Pages companion commit are in `TAGGING_MIGRATION.md`; transition regression uses observed definitions and planned provisions. No new triage assignments are made. |
| 7. Prospective releases | `metadata/RELEASE_TAG_POLICY.md` provides per-repository pre-1.0 boundaries. Public inventory records tag/release observations and source package declarations. No refs, versions, release workflows or dependency pins changed. |
| 8. Deterministic tooling | All six CLI commands implemented. Fleet and canary plans bind source and input digests, operation state, evidence, blast radius, and inverses. Stateful regressions cover full fleet and combined migrations. Executable Git mode corrected for fresh checkouts. Malformed paginated API rows are rejected instead of silently omitted. API races and ownership limits are documented. |
| 9. Credentials and CI | Two read-only workflows use pinned actions, no administrative secret inputs, no execute mode, and no untrusted-write trigger. Regression inspects these properties. Actual hosted CI is not run. |
| 10. Required validation | 84 Python tests, 15 existing link cases, six schemas, and five companion Pages tests passed locally. Detailed coverage mapping below; native Windows and hosted CI remain unrun. Independent final review remains pending. |
| 11. Deliverables and rollout | All preparation artifacts and companion diff exist locally. Candidate canary is explicitly unselected/unapproved. Independent review, maintainer selection, authorization, publication, live apply/readback, repeat apply, and final live drift report remain gated. |
| 12. Final report | `docs/TAGGING_AUDIT.md` links public scope, topic decisions, migrations, consumer changes, evidence, limits and next stages. Exact local revisions are in Git history and validation receipts. No PR exists, and live application/verification/rollback have not occurred. |

## Required validation coverage

| Item | Inspectable coverage |
| --- | --- |
| 1. Topic syntax and limits | `test_topic_grammar_count_and_uniqueness_fail_closed` |
| 2. Inventory, identity and applicability | `test_identity_and_default_branch_are_checked_against_snapshot`, archive/visibility tests, all `test_metadata_policy.py` management-scope tests |
| 3. Evidence and planning classification | Missing reason/removal evidence, planning-subject and project-planning tests; canonical validation against source tree pins |
| 4. Complete retained topics/removal approval | Stable/preserved topic test and full replacement/removal test |
| 5. No writes during preparation/failed gates | Fake transport read paths; dry-run, invalid authorization before client construction, full preflight, stale-state and wrong-operator tests |
| 6. Digests and forged claims | Stable plan, target selection digest, authorization scope, journal forgery and different-plan rejection tests |
| 7. Complete replacement | Full intended array assertion and full-fleet topic rollback comparison |
| 8. Rename/collision/additive/pagination | Migration planning and execution tests; nested fake pages; public open/closed issue/PR count and assignment observations |
| 9. Label spelling and malformed API values | Colons/spaces in fake labels; unknown stable identity, casefold collisions and malformed inputs tests |
| 10. HTTP, rate limits and uncertainty | Six transport tests plus timeout-before/after effect, uncertain creation and resume tests |
| 11. Idempotence | Exact fleet repeat/resume returns zero writes; combined six-migration repeat/resume regression |
| 12. Partial rollback/concurrency/unrelated use | Later-human-edit, uncertain ownership, retained definitions, preexisting destination, and repository locking tests; complete fleet rollback |
| 13. Consumer transition | `test_shared_form_defaults_exist_at_changed_transition_and_after_provision`; bug exists before; all form defaults resolve after the candidate provisions. Actual full activation remains unperformed. |
| 14. Unrelated resources unchanged | Fake transport rejects non-topic/label mutation paths. Changed-file scope contains no runtime, tag, release, repository-rename or protection changes. No live mutation was called. |
| 15. Workflow trust and redaction | `test_metadata_workflows_have_read_only_credentials_and_no_secret_inputs`; safe HTTP diagnostic tests; CLI checks authenticated operator before execution |

A passing test name alone is not independent review. Reviewers must inspect the test assertions and code paths, especially final projections and journal-owned rollback. Staged live checks stay unproven until actual authorized execution and independent readback occur.
