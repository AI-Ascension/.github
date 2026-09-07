# Execution and audit boundaries

The supported entrypoint is `tools/metadata.py`. Only that entrypoint loads
operator authorization and checks the authenticated GitHub account. Internal
execution classes accept an injected client for testing; they do not acquire
credentials or provide a second executable command. Importing an internal class
with a separately privileged client is outside this CLI authorization boundary.
Never execute untrusted pull-request code with administrative credentials.

## Concurrency

The executor performs a complete preflight and re-reads the affected state before
each write. It refuses detected drift and checks the resulting live state. Its
journal lock prevents two local executions from using the same journal at once.
Stable repository IDs also acquire locks in the operator state directory before
preflight, preventing overlapping plans in separate journals under that same
local state directory. Other machines, accounts, and independent API clients do
not participate in these local locks.
It spaces mutation attempts by at least one second, before the final state read.

GitHub documents that conditional requests for unsafe methods are unsupported
unless a particular endpoint says otherwise. The topics and label endpoints do
not document compare-and-swap writes. Therefore another maintainer's edit between
the final read and the write cannot be atomically prevented by this API. A topic
`PUT` replaces the complete set. Coordinate a canary/rollout window with other
metadata writers; stop and replan when an observed change conflicts. No local
lock, digest, or green test establishes an organization-wide atomic transaction.
See [GitHub REST API best practices](https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api)
and [repository topic replacement](https://docs.github.com/en/rest/repos/repos#replace-all-repository-topics).

## Journal integrity and interruption

Execution journals are authenticated with an HMAC chain. The key remains in the
operator's local state directory (`XDG_STATE_HOME`, or the standard user-local
state directory) under `ai-ascension-metadata`. It is created with owner-only
permissions. Keys never belong in the repository, a PR, or published receipts.
The trusted local state directory and executing account remain the trust boundary;
this is not a signature from GitHub and does not prove human approval.

A journal supplied by another machine or a PR has no trusted local key and is
refused. Moving a journal changes its path binding; do not substitute a fresh key
or hand-edit a record to make it acceptable. Preserve the original operator state
with the journal and use manual review if that state is unavailable.

A torn final record is preserved locally by content digest, and recovery resumes
from the authenticated prefix. A malformed complete record, invalid signature,
different plan digest, or broken chain requires manual review. Durable intent is
written before each effect and a verified receipt after a successful response and
live postcondition. A timeout is never blindly retried.

When an uncertain effect is already present on readback, resume records it as
reconciled without another write. That observation alone cannot establish who
made the change. Automatic rollback therefore owns only effects with a successful
response and verified postcondition recorded by this run. Uncertain ownership
requires manual review. Rollback preserves pre-existing destination assignments,
reports later state conflicts, and retains created label definitions by default.
Rollback conflicts are appended durably to the authenticated journal as well as
returned to the caller.

Journal locking currently uses `fcntl`; execution is supported on Linux/WSL.
Native Windows execution has not been implemented or verified. No live metadata
application has yet been authorized or performed for this task.
