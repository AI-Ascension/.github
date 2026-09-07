# Standards verification recipe

This recipe separates metadata, owner checks, and external evidence. It is intended for a local
checkout and has no provider, game, mail, deployment, or remote-settings side effect.
Provision the pinned compiler and locked dependencies first; Cargo may download missing dependencies.
With that cache present, append `--offline` before `--` to Cargo build/run/test invocations
when a no-network check is required. The validator binary itself performs no network access.

## Canonical source

From the `.github` checkout:

```bash
git diff --check
cargo +1.97.1 fmt --manifest-path standards/tools/standards-sync/Cargo.toml -- --check
cargo +1.97.1 test --locked --manifest-path standards/tools/standards-sync/Cargo.toml
cargo +1.97.1 clippy --locked --manifest-path standards/tools/standards-sync/Cargo.toml --all-targets -- -D warnings
cargo +1.97.1 run --locked --manifest-path standards/tools/standards-sync/Cargo.toml -- fixture-check --root standards/conformance
cargo +1.97.1 run --locked --manifest-path standards/tools/standards-sync/Cargo.toml -- validate --root .
```

The final `validate` command is run after the canonical profile and lock have been generated from
the exact source commit. Before that lock step, use the tests and fixture-check command; an old lock
must fail rather than being silently refreshed.

## Adopter

```bash
cargo +1.97.1 run --locked --manifest-path standards/tools/standards-sync/Cargo.toml -- validate --root .
```

Then run the generated profile commands from `standards-profile.toml`. The command/target map is
declarative and safety-checked; the validator does not execute it. A command that cannot run because
of a missing SDK, browser, container engine, host assembly, fixture, or permission is `unverified`.

## Trust boundaries

`standards-sync validate` confirms source identity, lock inventory, file bytes, schemas, rule shape,
profile shape, repository metadata, and fixture inventory. It cannot confirm semantic identity,
ownership, lifecycle, privacy, host compatibility, deployment, provider behavior, or independent
review approval. Rules with `verification: manual` require the owner evidence appropriate to the
target. A passing fixture is evidence about the validator's negative case, not about an adopter's
product.

No remote publication, pull request, merge, protected-check change, service installation, release,
mail delivery, game launch, or provider call is part of this recipe.
