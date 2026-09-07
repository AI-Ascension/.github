# Standards migration

Adoption is a local, reviewable copy of the canonical `standards/` tree plus two root metadata
files. It does not replace a repository's policy tool, architecture documents, formatter settings,
artifact manifests, or owner decisions.

## Prepare a local adopter

From a clean canonical `.github` worktree at the intended source commit, run the checked-in tool
with the reviewed repository, profile, and owner:

```bash
cargo +1.97.1 run --locked \
  --manifest-path standards/tools/standards-sync/Cargo.toml -- \
  sync --source-root /path/to/.github --target-root /path/to/adopter \
  --repository AI-Ascension/sts2-gateway --profile-id rust-service \
  --owner GW --source-commit <40-lowercase-hex-commit>
```

The command verifies that the supplied commit's complete `standards/` tree matches the source
checkout, copies only absent or byte-identical files, and emits `published: false`. It rejects
traversal, symlinks, differing managed files, unknown repository/profile/owner combinations, and
explicitly excluded repositories. Stage only the generated paths after inspecting them.
Add the exact `standards/tools/standards-sync/target/` line to the adopter root `.gitignore`
so default Cargo checks do not leave untracked compiler output; never ignore the entire bundle.

## Review and enablement sequence

1. Record the adopter's exact baseline head and local worktree state.
2. Run `standards-sync validate --root .` from the adopter after the copy.
3. Run every fast and required command in the generated profile from its recorded target. Capture
   tool versions, exit codes, case counts, and prerequisites; report unavailable tools as
   `unverified`.
4. Have the repository owner review the profile, lock, protected paths, and any manual rules.
5. Add or update the repository's normal CI workflow in a separate owner-reviewed change. Preserve
   existing required check names until a coordinated transition is complete.
6. Treat merge, branch protection, remote publication, deployment, and runtime evidence as separate
   states. A local validator result cannot enable a protected check or promote a runtime claim.

Planning repositories adopt documentation/configuration checks and the isolated standards tool.
They do not gain a root product workspace or runtime acceptance lanes. The brand package stays
excluded while its historical checksum boundary and the
recursive validator are reviewed; do not copy the Rust checker into it as a generic solution.

## Rollback

Remove only the adopter files introduced by the same local change, or revert that adopter commit
through its ordinary review process. Restore the previous profile and lock together so no checkout
claims a source digest it does not contain. The canonical source bundle remains unchanged by an
adopter rollback. Never reset or clean unrelated worktrees and never rewrite a published history.
