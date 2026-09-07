# standards-sync

standards-sync is the small, pinned-dependency validator and local distributor for the
AI-Ascension standards bundle. It is a Rust binary so Rust-only repositories can use the same
checker without Python, a sibling checkout, a network fetch, or a provider call. Its manifest is
an isolated Cargo workspace with Rust 1.97.1, serde 1.0.229, serde_json 1.0.151, serde_yaml
0.9.34, sha2 0.10.9, and toml 1.1.4 pinned in Cargo.lock.

## Validate a local adoption

From a repository containing standards/, standards-profile.toml, and standards.lock.json:

    cargo +1.97.1 run --locked --manifest-path standards/tools/standards-sync/Cargo.toml -- validate --root .

Validation checks exact source/profile metadata, safe and sorted lock paths, every local file's
SHA-256, the bundle digest, required rules and profile IDs, all 13 reviewed repository records,
self-identifying schemas, and valid/negative fixture inventory. A mismatch exits nonzero. The
checker never updates a lock or changes a source file.

## Distribute locally

An operator with a local canonical .github checkout may copy its standards/ bytes to an adopter
and create the two root metadata files in one deterministic operation:

    cargo +1.97.1 run --locked --manifest-path standards/tools/standards-sync/Cargo.toml -- \
      sync --source-root /path/to/.github --target-root /path/to/adopter \
      --repository AI-Ascension/sts2-gateway --profile-id rust-service \
      --owner GW --source-commit <40-lowercase-hex-commit>

The command verifies that the supplied commit is a local Git commit whose complete standards/
tree is byte-identical to the source checkout, then computes the bundle digest over sorted
standards/<path>, NUL, file bytes, NUL records; emits published:false; and refuses to overwrite a
differing managed file. A caller must stage the resulting paths explicitly and obtain owner review
before a local adopter claims ready.

The command has no GitHub, registry, deployment, game, host, mail, or provider access. Remote
publication is a separate operation and is never inferred from published:false or a passing local
check.
