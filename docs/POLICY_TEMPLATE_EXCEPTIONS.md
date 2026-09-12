# Policy-template exceptions

`workflow-templates/` are opt-in starter files, not active organization workflows.
Their differing validation behavior is therefore not an unauthorized drift from a
repository's local policy. A consumer becomes governed only after it copies a
template, selects its own checks, and records a standards-adoption row or an
owner-approved exception.

The scheduled standards report deliberately excludes `st2-project-planning` and
all private or evidence-only material. It reads only the three named public
consumer locks in `metadata/standards-adoption.json`; a missing lock, changed
digest, changed source state, or an attempt to add a planning/private row fails.

The current source bundle is the recorded local distribution at
`eed9921b5c5d5c41380655bded84f9e2d0aab599`. It is not published. The local
reusable-CI pilot may be run within this repository, but an owner must authorize
publication and hosted evidence before any other repository receives a remote
SHA-pinned call.
