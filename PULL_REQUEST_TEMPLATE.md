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

- [ ] Rust-only; no other product-language source was added.
- [ ] No game files, host assemblies, saves, credentials, personal paths, or private data are included.
- [ ] No copied or transliterated third-party implementation source.
- [ ] No claim states or implies live runtime, host, listener, or game compatibility.
- [ ] `cargo run --locked --package repo-policy -- --strict`, `cargo fmt --all --check`, clippy with `-D warnings`, and `cargo test --workspace --all-targets --all-features` pass locally (or the section above says which did not run).
- [ ] Remaining risks and `unverified` items are listed above.
