#!/usr/bin/env python3
"""Fail-closed gate: require a review of record pinned to the pull-request head.

The policy in ``CONTRIBUTING.md`` says a green run does not substitute for review,
but no workflow in this organization enforced it.  This module is that check.

Design constraints, all fail-closed:

* A review counts only when ``review.commit_id`` equals the pull request's *head*
  SHA -- not merely that "some review exists".  This is the unpinned-review
  failure class: a review of an older commit does not review the code that
  landed.
* Reviews of *any* state count.  This organization's shared merging account
  receives HTTP 422 on ``APPROVE`` submissions, so every review of record is a
  ``COMMENT`` review.  Requiring ``APPROVED`` would block every merge.  Only the
  pin is load-bearing.
* Every review on the pull request is considered, not just the most recent one.
  A later re-review or audit note is common and must not mask an earlier
  pinned review, and the earliest pinned review is the one that gated the merge.
* Anything the tool cannot determine is a *failure*, never a pass: an API
  error, a malformed response, a missing/unparseable head SHA, an empty
  selection, or a garbage body.  An instrument that selects zero items and
  exits 0 is indistinguishable from a real pass, so the exit status and the
  decision are derived from the same reviewed data.

The decision function :func:`evaluate` is pure and network-free so the policy
is testable in isolation.  The network read is confined to
:class:`ReviewGateRunner` (a thin ``gh api`` seam matching the repository's
existing transport style) and to :func:`main`.
"""

import argparse
import json
import re
import subprocess
from typing import Any, Sequence


class ReviewGateError(Exception):
    """Review state could not be determined; the gate must fail, not pass."""


# A git object name: 7-40 lowercase hex characters.  GitHub returns the full
# 40-character SHA for head commits; short forms are rejected so a truncated
# or padded field cannot silently compare unequal to the head and mask a real
# pin, and cannot be mistaken for a real SHA.
_FULL_SHA = re.compile(r"^[0-9a-f]{40}$")


def _require_full_sha(value: Any, field: str) -> str:
    if not isinstance(value, str) or not _FULL_SHA.match(value):
        raise ReviewGateError(f"{field} is missing or not a full 40-character commit SHA")
    return value


def _review_commit(review: Any) -> str | None:
    """Return a review's commit_id when it is a well-formed full SHA, else None.

    A malformed review entry is *not* a hard error here: a single odd review
    should not crash the gate, but it also must never satisfy the pin.  It
    simply cannot count as a review of record.  Structural errors in the
    collection as a whole are caught by :func:`_validate_reviews`.
    """
    if not isinstance(review, dict):
        return None
    value = review.get("commit_id")
    if isinstance(value, str) and _FULL_SHA.match(value):
        return value
    return None


def _validate_reviews(reviews: Any) -> list[dict[str, Any]]:
    """Fail closed unless ``reviews`` is a well-formed array of review objects."""
    if not isinstance(reviews, list):
        raise ReviewGateError("reviews response is not an array")
    for index, review in enumerate(reviews):
        if not isinstance(review, dict):
            raise ReviewGateError(f"reviews[{index}] is not an object")
    return reviews


def evaluate(reviews: Any, head_sha: Any) -> dict[str, Any]:
    """Decide whether ``reviews`` contains a review of record for ``head_sha``.

    Returns a mapping with ``ok`` (bool) and ``reason`` (str).  ``ok`` is True
    only when at least one review is pinned to the exact head SHA.  Any input
    the function cannot interpret raises :class:`ReviewGateError`; callers must
    treat that as a failure.
    """
    head = _require_full_sha(head_sha, "head SHA")
    entries = _validate_reviews(reviews)

    pinned: list[dict[str, Any]] = []
    for review in entries:
        if _review_commit(review) == head:
            pinned.append(review)

    if pinned:
        # Report the earliest pinned review as the review of record, matching
        # how the audit reads the thread, but the decision depends only on the
        # existence of a pin, not on this choice.
        record = min(
            pinned,
            key=lambda r: (str(r.get("submitted_at") or ""), str(r.get("id") or "")),
        )
        return {
            "ok": True,
            "reason": (
                f"{len(pinned)} review(s) pinned to head {head}; "
                f"review of record id={record.get('id')} state={record.get('state')}"
            ),
            "head_sha": head,
            "review_of_record_id": record.get("id"),
        }

    # No review is pinned to the head.  Distinguish "no reviews at all" from
    # "reviews exist but none pinned" -- both fail, but the reason differs.
    if not entries:
        reason = f"no review of record: head {head} has no reviews at all"
    else:
        observed = sorted({_review_commit(r) or "(missing commit_id)" for r in entries})
        reason = (
            f"no review pinned to head {head}: {len(entries)} review(s) present, "
            f"pinned to {', '.join(observed)}"
        )
    return {"ok": False, "reason": reason, "head_sha": head, "review_of_record_id": None}


class ReviewGateRunner:
    """Thin ``gh api`` seam for reading pull-request state.

    Mirrors the repository's existing transport idiom (see
    ``tools/metadata.CommandRunner``): shell out to the authenticated ``gh``
    executable, surface failures as :class:`ReviewGateError`, and never swallow
    an error into an empty-but-successful read.
    """

    def __init__(self, gh_path: str = "gh", timeout: int = 60):
        self.gh_path = gh_path
        self.timeout = timeout

    def _run(self, endpoint: str) -> Any:
        try:
            process = subprocess.run(
                [self.gh_path, "api", endpoint],
                text=True,
                capture_output=True,
                timeout=self.timeout,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise ReviewGateError(f"gh api timed out after {self.timeout}s for {endpoint}") from exc
        except OSError as exc:
            raise ReviewGateError(f"unable to run {self.gh_path}: {exc}") from exc
        if process.returncode:
            message = (process.stderr or process.stdout or "command failed").strip()
            raise ReviewGateError(f"gh api failed for {endpoint}: {message}")
        raw = process.stdout or ""
        if not raw.strip():
            raise ReviewGateError(f"gh api returned an empty body for {endpoint}")
        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ReviewGateError(f"gh api returned a non-JSON body for {endpoint}") from exc

    def head_sha(self, repository: str, number: int) -> str:
        payload = self._run(f"repos/{repository}/pulls/{number}")
        if not isinstance(payload, dict):
            raise ReviewGateError(f"pull request response for {repository}#{number} is not an object")
        head = payload.get("head")
        sha = head.get("sha") if isinstance(head, dict) else None
        return _require_full_sha(sha, f"head SHA for {repository}#{number}")

    def reviews(self, repository: str, number: int) -> list[dict[str, Any]]:
        payload = self._run(f"repos/{repository}/pulls/{number}/reviews?per_page=100")
        # ``gh api`` may return a list directly, or (with --slurp) a list of
        # pages.  Normalize the nested page form before validation.
        if isinstance(payload, list) and payload and all(isinstance(p, list) for p in payload):
            flattened: list[Any] = []
            for page in payload:
                flattened.extend(page)
            payload = flattened
        return _validate_reviews(payload)


def check(
    repository: str,
    number: int,
    runner: ReviewGateRunner | None = None,
) -> dict[str, Any]:
    """Fetch the pull request's head and reviews, then evaluate them.

    Any undetermined state raises :class:`ReviewGateError` instead of returning
    a verdict, so a caller cannot mistake a failed read for a passing gate.
    """
    reader = runner or ReviewGateRunner()
    head = reader.head_sha(repository, number)
    reviews = reader.reviews(repository, number)
    return evaluate(reviews, head)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", required=True, help="owner/name")
    parser.add_argument("--number", type=int, required=True, help="pull request number")
    args = parser.parse_args(argv)

    try:
        result = check(args.repository, args.number)
    except ReviewGateError as exc:
        # Fail closed and loud: an undetermined review state is a failure, and
        # the reason is printed so the check-run is actionable.
        result = {"ok": False, "reason": f"review state undetermined: {exc}"}

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
