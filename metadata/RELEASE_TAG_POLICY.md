# Prospective release-tag policy

Status: proposed for maintainer review; no existing tag or release is changed.

Repository topics, issue labels, and Git tags are separate namespaces. The metadata
tool must never create, move, or delete Git refs, or create or publish releases.
Its authorization must not grant those operations.

The 2026-09-07 [public inventory](audits/2026-09-07/public-inventory-summary.json)
found no Git tags or GitHub releases in the 12 public in-scope repositories. This dated observation does not establish a permanent
absence of releases. Consult each repository's `RELEASING.md`, package manifests,
and current refs before proposing its first release.

Future release proposals must state the owning repository, exact commit, artifact
version, compatibility boundary, required checks, and authorized maintainer.
Preserve existing package, binary, repository, and protocol-profile names. A tag
must identify the tested source commit; an annotated tag or release description
must not promote static or synthetic evidence to live-host compatibility.

The proposed default spelling is `vMAJOR.MINOR.PATCH`, with explicit prereleases
such as `v0.1.0-alpha.1` when the release owner chooses them. These examples are
not versions to publish. Check existing consumers before accepting this spelling;
it does not override an established owner convention. Use component prefixes only
when independently released components actually require separate version lines.
Publish only with separate,
recorded release authorization. Correct an erroneous published version with a new
version according to the owning repository's policy; do not silently move tags.

## Proposed pre-1.0 compatibility boundaries

The following is reviewable guidance, not a declaration of stable APIs or approval
to release. For a future `0.x` release, record breaking changes and migration in
the owning compatibility record, propose a minor increment for such changes, and
reserve ordinary patch increments for compatible corrections. Safety corrections
still need an explicit compatibility classification. Owners decide the first
version and accept this policy before publication. Existing `0.0.0` manifest
values do not establish a released product version.

| Repository | Boundary the release owner must classify |
| --- | --- |
| sts2-harness | Episode/experiment records, replay, scoring, and provider adapters; preserve independent protocol and model/host pins. |
| sts2-mcp-server | MCP tool schemas and gateway mapping; transport acceptance does not establish host execution. |
| sts2-gateway | Authentication, admission, routing, leases, error and timing contracts; independently pin the host adapter. |
| sts2-game-mod | HTTP, native ABI, managed loader, game-host/platform support, and package contents are independent versions. |
| sts2-game-core | Pure semantic/state contracts; a core release does not certify full-game simulation or host compatibility. |
| sts2-protocol | Wire/schema profiles, generated artifacts, and conformance fixtures; retain profile names and digest lineage. |
| ai-agent-observability | Deployment configuration and integration versions; container health is not ingestion/persistence verification. |
| .github | Metadata schema, command contracts, and migration compatibility; metadata releases do not synchronize product releases. |
| AI-Ascension.github.io | Public documentation and fixture compatibility; historical source pins remain exact. |
| aiascension.tech | Website/PHP response and deployment compatibility; this task neither deploys nor delivers email. |
| ascension-watchdog | Planning profile; a product release requires accepted implementation and its own release policy first. |
| ascension-map-visualizer | Planning profile; a specification revision is not a working renderer release. |

The six STS2 owners' existing `RELEASING.md` and compatibility documents retain
authority over their boundaries. Pinned source references are recorded in the
tagging audit. No synchronized organization version, release workflow, tag
protection, signing rule, package version, or dependency pin changes here.
