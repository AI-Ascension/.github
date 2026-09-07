# Public metadata preparation evidence

Start with [the audit](../../../docs/TAGGING_AUDIT.md). `fleet-plan.json` and `canary-plan.json` are digest-bound candidates, blocked pending independent review and lacking external authorization. Their Markdown counterparts list proposed changes.

`public-before.json` contains only public repository metadata and issue/label identities needed by the credential-free fleet regression. It excludes issue bodies, comments, account records, and private repositories. It is a bounded test fixture, not a complete source-evidence snapshot. The source manifests contain public source pins and digests; the canonical map carries per-topic citations. Raw inventory is intentionally untracked.

The prior execution review reports are retained as historical evidence only. Consult `orchestration.json` for the unfulfilled nesting requirement and `validation.json` for final local checks. No file in this directory proves remote application, publication, deployment, or live execution.
