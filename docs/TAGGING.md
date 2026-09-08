# Organization tagging operations

Status: the implementation tooling is merged. The [2026-09-08 rollout review](../metadata/audits/2026-09-08/README.md) records refreshed inputs and exact proposed plans. Local preparation, source review, owner authorization, publication, API application, and independent live verification remain separate states. No live metadata write is authorized by this document.

## Maintained inputs

- `metadata/repositories.yml`: public repository IDs, exact default-branch pins,
  management applicability, complete topic sets, meanings, and source evidence.
- `labels.yml`: the only shared label-definition authority. Optional
  `repository_ids` scopes a definition; an empty list leaves it as an inactive
  vocabulary proposal. Definitions never automatically assign issues.
- `metadata/label-migrations.yml`: source/destination meanings, collision
  strategies, observed IDs, assignment scope, and rollout ordering.
- `metadata/inputs/2026-09-07-tagging-specification.md`: the supplied design input,
  preserved as evidence. It is not another editable desired-state map.

Every managed repository needs the `ai-ascension` topic. Planning repositories
remain visibly marked `project-planning`; roadmap subjects do not establish a
working implementation. Existing valid topics remain unless a removal has an
explicit reviewed reason and evidence. A combined set over 20 fails instead of
being truncated. No organization, repository, package, binary, or profile name is
changed by this tooling.

`managed: false` prevents selection. Any discovered repository absent from the
public registry needs a local applicability exclusion with its stable ID,
`decision: excluded-pending-owner`, and a reason. Exclusions cannot overlap
managed entries or authorize writes. Keep private identities and raw snapshots
outside Git; use the ignored `metadata/snapshots/` directory or private storage.
The public audit discloses counts and scope without private names or issue bodies.

## Read-only preparation

Requirements: Python 3.12, PyYAML 6.0.3, and an existing authenticated GitHub CLI
for live reads. Linux/WSL is the tested execution environment. No product runtime,
game host, provider, deployment, or installed service is required.

Run these commands from the coordination repository. Supply the local exclusion
file only when the refreshed inventory contains reviewed out-of-scope entries;
its schema is a JSON array of the exclusion records described above.

```sh
./tools/metadata snapshot --org AI-Ascension \
  --exclusions metadata/snapshots/applicability-exclusions.json \
  --output metadata/snapshots/before.json
./tools/metadata validate --metadata metadata/repositories.yml \
  --labels labels.yml --snapshot metadata/snapshots/before.json
./tools/metadata plan --metadata metadata/repositories.yml --labels labels.yml \
  --migrations metadata/label-migrations.yml --snapshot metadata/snapshots/before.json \
  --output metadata/plans/fleet.json --diff-output metadata/plans/fleet.md
python3 -m unittest discover -s tests -p 'test_*.py' -v
bash tests/link-check-template.sh
```

An empty applicability list is appropriate only when every discovered repository
is represented in the canonical map. Do not delete an unlisted repository from a
snapshot to make validation pass. `snapshot --input` normalizes an existing local
snapshot without network access.

Each plan binds all input digests, its selected repository IDs, source commit
preconditions, reasons/evidence, permission requirements, before/after states,
assignment blast radius, and conservative inverses. Its manifest revision is a
content-addressed SHA-256, so presentation-only timestamp changes cannot silently
change the approved operation list. Compare exact plan digests before execution.

A maintainer chooses the canary. Repeat `--repository-id` when planning an
approved subset. The selection changes the digest; a fleet approval does not
implicitly select a canary, and a canary approval does not authorize the fleet.
The candidate canary must not trigger releases, deployment, or unrelated jobs.

To regenerate the supplied `.github` candidate for review, use:

```sh
./tools/metadata plan --metadata metadata/repositories.yml --labels labels.yml \
  --migrations metadata/label-migrations.yml --snapshot metadata/snapshots/before.json \
  --repository-id 1354466045 --output metadata/plans/canary.json \
  --diff-output metadata/plans/canary.md
```

This read-only command proposes a scope. The maintainer must select that scope
and approve the resulting digest before execution.

## Approval and application

Publication permission, topic Administration write capability, and Issues write
capability for labels are separate. A normal repository `GITHUB_TOKEN` does not
administer the organization. Use only an already approved credential scoped to
the approved repositories; never install an App or expand privileges here.

The operator/maintainer approval must identify the exact plan digest, manifest
revision, repository IDs, topic/label operations, assignment blast radius, and
approver. Record that actual instruction using `authorization.schema.json` only
after approval exists. Agent-authored examples and administrator access are not
approval. The CLI checks the record's binding and the authenticated GitHub login;
it cannot independently establish the human origin of an arbitrary local file.
That origin is a maintainer-controlled operational boundary. Keep approval
records outside untrusted PR inputs and do not run untrusted code with the write
credential.

After the exact scope is approved and the approved operator/authorization paths
are set in the shell, these are the execution commands:

```sh
./tools/metadata apply --plan metadata/plans/canary.json \
  --authorization "$TAGGING_AUTHORIZATION" --operator "$TAGGING_OPERATOR" \
  --journal metadata/journals/canary.jsonl --execute
./tools/metadata snapshot --org AI-Ascension \
  --exclusions metadata/snapshots/applicability-exclusions.json \
  --output metadata/snapshots/after-canary.json
./tools/metadata verify --plan metadata/plans/canary.json \
  --snapshot metadata/snapshots/after-canary.json
```

`apply` and `rollback` without `--execute` return a zero-write dry run. They still
require a structurally valid, plan-bound authorization record. Planning and
validation need no approval record. No blanket authorization record is supplied
with this candidate.

A separate reviewer checks live topics, stable label IDs/definitions, and every
approved open/closed issue/PR assignment. Run a second application of the same
verified plan and journal; it must return zero writes. Only then proceed to the
separately approved fleet plan, respecting the consumer transition ordering in
[TAGGING_MIGRATION.md](TAGGING_MIGRATION.md). Finish with readback and a read-only
drift report. Template activation must wait for its referenced labels.

## Failure handling and rollback

The executor performs full preflight and checks state before each effect. It
replaces the complete reviewed topic set and uses additive assignment APIs to
preserve unrelated labels. It records intent durably, verifies the response by
readback, and owns only confirmed effects in an authenticated local journal.
Detected drift stops the run and requires replanning. After interruption or an
uncertain network result, inspect the journal and live state before using
`apply --resume`; never blindly retry a write.

Safe single-request reads may retry a rate limit only after a server-provided
delay, within the bounded retry budget. Unknown delays, delays over 60 seconds,
paginated rate-limit failures, authentication failures, and write failures stop
and report. No rapid guessed rate-limit retry is used. Printable API diagnostics
contain classifications rather than raw response text.

Rollback needs an additional explicit `rollback` operation in the authorization
for the same plan. It restores only owned effects whose state still matches;
later human edits and uncertain ownership produce durable conflicts and a
nonzero exit status. It preserves pre-existing destination assignments and
retains created definitions by default. Keep the operator's trusted local state
with the journal; moving a journal or losing its HMAC key requires manual review.

```sh
./tools/metadata rollback --plan metadata/plans/canary.json \
  --authorization "$TAGGING_ROLLBACK_AUTHORIZATION" --operator "$TAGGING_OPERATOR" \
  --journal metadata/journals/canary.jsonl --execute
```

Repository locks coordinate only processes sharing the same operator state
folder. GitHub does not document conditional topic/label mutations, so another
client can race the final read and write. Coordinate the rollout window; do not
claim atomicity. Details are in
[execution boundaries](../metadata/EXECUTION_BOUNDARIES.md) and the
[prospective release-tag policy](../metadata/RELEASE_TAG_POLICY.md).
