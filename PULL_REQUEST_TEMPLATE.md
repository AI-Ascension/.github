## Outcome

What this change makes true, and why it is needed. One task per branch.

## Boundary and compatibility

- Repository boundary or contract affected:
- Compatibility classification (internal, additive-compatible, safety correction, deprecation, breaking):
- Public documents updated (README, ARCHITECTURE, COMPATIBILITY, decisions, CHANGELOG):

## Evidence

- Exact commands run and their results:
- Checks not run, and why:

## Claims

List each claim this change makes on a public surface, with its label
(`confirmed`, `source-derived`, `proposed`, `inferred`, `unverified`):

-

## Checklist

- [ ] Source languages and tooling follow the target repository's policy and documented exceptions.
- [ ] No game files, host assemblies, saves, credentials, personal paths, or private data are included.
- [ ] No copied or transliterated third-party implementation source.
- [ ] Runtime, host, listener, and game claims identify their exact evidence, version, and limits; historical or synthetic evidence is not presented as current live validation.
- [ ] The target repository's documented checks pass locally (or the section above says which did not run). For Rust workspaces these include strict repository policy, formatting, clippy with `-D warnings`, and workspace tests where provided.
- [ ] Remaining risks and `unverified` items are listed above.
