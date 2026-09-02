# Governance

How decisions are made across the `AI-Ascension` repositories, who may do what, and how a claim
earns a stronger evidence label.

## Authority order

When sources disagree, the earlier item wins:

1. An explicit decision by the project owner or a maintainer, recorded in an issue, pull request,
   or decision record.
2. Project policy: the shared rules in this repository ([CONTRIBUTING.md](CONTRIBUTING.md),
   [SECURITY.md](SECURITY.md), [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)) and each repository's
   `policy.toml` as enforced by its `repo-policy` tool.
3. Each repository's own `README.md`, `docs/ARCHITECTURE.md`, `docs/COMPATIBILITY.md`, and
   `docs/decisions/*.md`.
4. Design guidance: site copy, identity guidelines, planning notes, and this file's non-normative
   explanations.

A public page never outranks the repository it describes. If the site and a README disagree, the
README is the source and the site is corrected.

## Roles

| Role | May | May not |
| --- | --- | --- |
| Maintainer | Merge, tag, publish, deploy, change repository settings, apply labels, resolve disputes, edit `CODEOWNERS`. | Merge their own change without a second look when another maintainer is available. |
| Contributor | Open issues and pull requests, review, propose designs, submit fixtures and observations. | Merge, push to `main`, publish, or speak for the project. |
| Agent (automated or model-driven) | Prepare branches, run checks, draft text, verify claims, report results with labels. | Merge, publish, deploy, post to communities, contact people, or change permissions or policy. |

Anyone in any role may say `unverified`. No one may remove that label without evidence.

## Promoting a claim

A claim moves up the ladder only with a named artifact:

| From | To | Requires |
| --- | --- | --- |
| `unverified` | `source-derived` | A quotation from the repository's own documents at a named commit. |
| `source-derived` or `inferred` | `confirmed` | A command or test, the commit it ran at, and its observed result, reproducible by a reviewer. |
| `proposed` | anything stronger | The thing being built, then the row above. |

Runtime, host, and game claims stay `unverified` until a maintainer records a run against a real
host and a reviewer reproduces it. No planning target, screenshot, or model output promotes a claim
by itself. A claim can also move down: a failing reproduction returns it to `unverified` and the
public surface that carried it is corrected in the same change.

## Descriptions and public text

One approved description map drives the organization description, every repository description,
homepage, and topic set, the README entry blocks, and the site's metadata. The site's
[evidence page](https://ai-ascension.github.io/evidence.html) shows the current approved text next
to the artifact that supports it. To change a description, change the map first, then apply it
everywhere in one pass and record before and after values; a description that drifts from the map
is a defect. A user decision overrides any row in the map.

## Changing this file

By pull request, merged by a maintainer, like everything else.
