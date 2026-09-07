# Standards conformance fixtures

These small fixtures exercise the shape and trust boundaries of the local validator. They are
metadata fixtures only; they contain no credentials, proprietary files, provider calls, game
files, host assemblies, or private traces.

| Fixture | Expected result | Boundary |
| --- | --- | --- |
| `valid-profile.toml` | accepted by the profile parser | exact source commit, local distribution, three check lanes |
| `valid-lock.json` | accepted as a shape fixture | local source, sorted safe paths, explicit unpublished state |
| `invalid-profile-floating.toml` | rejected | `main` cannot stand in for a commit |
| `invalid-profile-missing-source.toml` | rejected | a profile must bind source metadata |
| `invalid-lock-traversal.json` | rejected | parent-path escape in a lock entry |
| `invalid-lock-published.json` | rejected | prepared local source cannot claim remote publication |
| `invalid-exception-pending.yaml` | rejected | pending/self-written text is not approval |
| `invalid-exception-broad-path.yaml` | rejected | exceptions name exact repository-relative files |

The executable checker runs these as negative fixtures without network access:

```text
cargo run --locked --manifest-path standards/tools/standards-sync/Cargo.toml -- fixture-check --root standards/conformance
```

Each negative case must fail for the named reason. A command that returns zero for an invalid
fixture is itself a conformance failure.

