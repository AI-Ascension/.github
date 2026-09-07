# Organization metadata

`repositories.yml` is the proposed canonical public repository-topic registry.
`/labels.yml` is the single shared label-definition authority, and
`label-migrations.yml` defines the proposed transitions. Owners in `/CODEOWNERS`
review these files through the existing governance process. Source review does
not authorize API changes or approve public positioning on the owner's behalf.

The supplied tagging specification now provides the previously missing topic
sets and label mappings. Its unchanged design input is in `inputs/`; desired
state is maintained only in the canonical files above. Historical description
map evidence remains unchanged in `history/` and is not a current topic authority.
Descriptions and homepages are outside this tagging task.

Use [tagging operations](../docs/TAGGING.md) for commands, permissions,
management/exclusion decisions, journals, and rollback;
[tagging migration](../docs/TAGGING_MIGRATION.md) for consumer rollout ordering;
and [tagging audit](../docs/TAGGING_AUDIT.md) for source pins, per-repository
before/after results, validation, and actual application status.

Volatile API snapshots and private issue/repository data remain local by default.
The public registry includes only the 12 supplied public repositories. An
additional private discovery is held out pending an owner applicability decision;
its identity is not published. Pinned public-source manifests remain reproducible
review evidence, not proof of live application or improved gameplay.

`review_status` records preparation/source review. Only an independently recorded
operator/maintainer authorization bound to the exact plan digest permits a remote
write. Unreviewed removals or unresolved evidence block application. Planning
subjects remain explicit through `project-planning`, and source/configuration
support is distinct from locally reproduced runtime evidence.

No tag refs, releases, protection, permissions, names, or application behavior are
changed. [Release-tag guidance](RELEASE_TAG_POLICY.md) is prospective only.
