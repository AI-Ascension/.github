# Policy-template exceptions

`workflow-templates/` are opt-in starter files, not active organization workflows.
Their differing validation behavior is therefore not an unauthorized drift from a
repository's local policy. A consumer becomes governed only after it copies a
template, selects its own checks, and records a standards-adoption row or an
owner-approved exception.

The scheduled standards report deliberately excludes `st2-project-planning` and
all private or evidence-only material. It reads only the named public consumer
locks in `metadata/standards-adoption.json`; a missing lock, changed digest,
changed source state, or an attempt to add a planning/private row fails. The
scheduled workflow checks out exactly that listed set, because a consumer lock
is only read from the workspace and an unlisted repository is never validated.
`aiascension.tech` is not listed: it became private, so the workflow's
repository-scoped token cannot read it.

The current source bundle is the recorded local distribution at
`eed9921b5c5d5c41380655bded84f9e2d0aab599`. It is not published. The local
reusable-CI pilot may be run within this repository, but an owner must authorize
publication and hosted evidence before any other repository receives a remote
SHA-pinned call.
