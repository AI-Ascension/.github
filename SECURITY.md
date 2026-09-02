# Security Policy

This policy applies to every `AI-Ascension` repository unless a repository's own `SECURITY.md`
says otherwise.

## Supported state

No repository has a released artifact. Security fixes apply to the current `main` line of the
affected repository.

## Reporting privately

1. Open the affected repository on GitHub, choose the **Security** tab, and use **Report a
   vulnerability** (GitHub private vulnerability reporting). Only maintainers see the report.
2. If private reporting is not available on that repository, open a minimal public issue that says
   only that you need a private channel for a security matter. Do not describe the problem there.
   A maintainer will open a private advisory and invite you to it.

There is no security email address. Any address claiming to be one is not ours.

In the private report, include the repository and commit, platform, impact, the conditions that
reproduce it, and the smallest safe demonstration. Never include exploit code that works against a
live target, save files, credentials or tokens, personal file paths, multiplayer identifiers, or
another person's data. Maintainers acknowledge receipt privately, coordinate a fix and a disclosure
window, and credit the reporter when asked and appropriate.

## Project risk boundary

Any listener into a game process is game-control authority: it can expose profile or run state and
request mutations, so unexpected binding, proxy inheritance, authentication bypass, cross-origin
access, path disclosure, unsafe FFI, host-thread violations, queue loss, and mutation replay are all
security-relevant here. Today nothing is live: no repository exposes a listener, runs a process
supervisor, connects to a game, or authenticates at an external boundary (`unverified` for all
runtime behavior; `confirmed` only for deterministic in-memory tests at the pinned commits). A
report about a gap between a documented contract and a test is still welcome; file it as a security
note through the private channel above, or as a contract observation if it is not exploitable.

Do not test anything from this project against another person, a public lobby, a valued profile, or
a non-disposable save.

## Conduct reports

Conduct concerns use the same private channel; see [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
