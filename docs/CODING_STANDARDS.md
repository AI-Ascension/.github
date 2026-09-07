# Coding standards

This repository uses the `org-governance` profile in [standards-profile.toml](../standards-profile.toml).
The [local lock](../standards.lock.json) pins the first-party [baseline](../standards/BASELINE.md),
bundle bytes and generated profile configuration. Local architecture, public contracts,
historical recipe pins and applicable owner decisions remain authoritative in their scopes.

Run the fast and required commands in the profile from their named target directories.
`standards-sync validate` checks metadata and pinned bytes; native checks validate source behavior.
Tools and browser reports are development inputs and are excluded from site publication.
Missing tools or targets are unverified checks. Exceptions need actual rule-scoped review evidence;
none are authorized by this adoption. Local commits do not establish hosted CI, merge, protected
checks, deployment, mail delivery, provider or game behavior.
