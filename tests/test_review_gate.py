import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import review_gate
from review_gate import ReviewGateError, ReviewGateRunner, check, evaluate, main

HEAD = "a" * 40
OTHER = "b" * 40


def review(commit_id=HEAD, state="COMMENTED", submitted="2026-09-26T01:00:00Z", rid=1):
    return {
        "id": rid,
        "state": state,
        "commit_id": commit_id,
        "submitted_at": submitted,
        "user": {"login": "CompleteDotTech"},
    }


class EvaluateTests(unittest.TestCase):
    def test_no_reviews_at_all_fails(self):
        result = evaluate([], HEAD)
        self.assertFalse(result["ok"])
        self.assertIn("no reviews at all", result["reason"])

    def test_review_pinned_to_head_passes(self):
        result = evaluate([review()], HEAD)
        self.assertTrue(result["ok"])
        self.assertEqual(result["review_of_record_id"], 1)

    def test_review_pinned_to_other_sha_fails(self):
        result = evaluate([review(commit_id=OTHER)], HEAD)
        self.assertFalse(result["ok"])
        self.assertIn("no review pinned to head", result["reason"])
        self.assertIn(OTHER, result["reason"])

    def test_mixed_reviews_passes_only_via_pinned_one(self):
        result = evaluate([review(commit_id=OTHER, rid=1), review(rid=2)], HEAD)
        self.assertTrue(result["ok"])
        self.assertEqual(result["review_of_record_id"], 2)

    def test_earliest_pinned_review_is_the_record(self):
        reviews = [
            review(rid=9, submitted="2026-09-26T05:00:00Z"),
            review(rid=3, submitted="2026-09-26T01:00:00Z"),
        ]
        result = evaluate(reviews, HEAD)
        self.assertTrue(result["ok"])
        self.assertEqual(result["review_of_record_id"], 3)

    def test_all_states_count_when_pinned(self):
        # The shared merging account gets 422 on APPROVE, so reviews of record
        # are COMMENTED. Any state must count as long as it is pinned.
        for state in ("COMMENTED", "APPROVED", "CHANGES_REQUESTED", "DISMISSED"):
            with self.subTest(state=state):
                self.assertTrue(evaluate([review(state=state)], HEAD)["ok"])

    def test_short_sha_is_not_a_pin(self):
        # A truncated commit_id must not satisfy the pin.
        result = evaluate([review(commit_id=HEAD[:7])], HEAD)
        self.assertFalse(result["ok"])


class FailClosedTests(unittest.TestCase):
    def test_missing_head_sha_raises(self):
        for bad in (None, "", "not-a-sha", HEAD[:7], 12345, {}):
            with self.subTest(head=bad):
                with self.assertRaises(ReviewGateError):
                    evaluate([review()], bad)

    def test_reviews_not_an_array_raises(self):
        for bad in (None, {"message": "Not Found"}, "garbage", 5):
            with self.subTest(reviews=bad):
                with self.assertRaises(ReviewGateError):
                    evaluate(bad, HEAD)

    def test_malformed_review_entry_raises(self):
        with self.assertRaises(ReviewGateError):
            evaluate(["not-an-object"], HEAD)

    def test_empty_payload_is_not_a_pass(self):
        # The recurring failure shape: an instrument that selects zero items
        # and exits 0. Here a truncated/empty review set must never pass.
        result = evaluate([], HEAD)
        self.assertFalse(result["ok"])


class RunnerTests(unittest.TestCase):
    """These drive the real subprocess seam so failure is demonstrated, not asserted."""

    def _fake_gh(self, directory, body, returncode=0, stderr=""):
        script = Path(directory) / "gh"
        script.write_text(
            "#!/bin/sh\n"
            f"cat <<'BODY'\n{body}\nBODY\n"
            f"cat >&2 <<'ERR'\n{stderr}\nERR\n"
            f"exit {returncode}\n"
        )
        script.chmod(0o755)
        return str(script)

    def test_nonzero_exit_raises(self):
        with tempfile.TemporaryDirectory() as name:
            path = self._fake_gh(name, "", returncode=1, stderr="gh: Not Found (HTTP 404)")
            with self.assertRaises(ReviewGateError) as caught:
                ReviewGateRunner(gh_path=path).head_sha("AI-Ascension/.github", 49)
            self.assertIn("404", str(caught.exception))

    def test_empty_body_raises(self):
        with tempfile.TemporaryDirectory() as name:
            path = self._fake_gh(name, "")
            with self.assertRaises(ReviewGateError) as caught:
                ReviewGateRunner(gh_path=path).head_sha("AI-Ascension/.github", 49)
            self.assertIn("empty body", str(caught.exception))

    def test_non_json_body_raises(self):
        with tempfile.TemporaryDirectory() as name:
            path = self._fake_gh(name, "<html>gateway error</html>")
            with self.assertRaises(ReviewGateError) as caught:
                ReviewGateRunner(gh_path=path).head_sha("AI-Ascension/.github", 49)
            self.assertIn("non-JSON", str(caught.exception))

    def test_error_object_body_is_rejected_not_accepted(self):
        # A 200 with an error-shaped body must not be mistaken for a payload.
        with tempfile.TemporaryDirectory() as name:
            path = self._fake_gh(name, json.dumps({"message": "Not Found"}))
            with self.assertRaises(ReviewGateError):
                ReviewGateRunner(gh_path=path).reviews("AI-Ascension/.github", 49)

    def test_head_payload_that_is_not_object_raises(self):
        with tempfile.TemporaryDirectory() as name:
            path = self._fake_gh(name, json.dumps([1, 2, 3]))
            with self.assertRaises(ReviewGateError):
                ReviewGateRunner(gh_path=path).head_sha("AI-Ascension/.github", 49)

    def test_missing_executable_raises(self):
        with self.assertRaises(ReviewGateError):
            ReviewGateRunner(gh_path="/nonexistent/gh-binary").head_sha("AI-Ascension/.github", 49)

    def test_real_subprocess_roundtrip_extracts_head_and_reviews(self):
        # End-to-end through the actual subprocess seam.
        with tempfile.TemporaryDirectory() as name:
            path = self._fake_gh(
                name,
                json.dumps({"head": {"sha": HEAD}}),
            )
            runner = ReviewGateRunner(gh_path=path)
            self.assertEqual(runner.head_sha("AI-Ascension/.github", 1), HEAD)

    def test_head_sha_extracted_from_payload(self):
        class Stub(ReviewGateRunner):
            def _run(self, endpoint):
                return {"head": {"sha": HEAD}}

        self.assertEqual(Stub().head_sha("AI-Ascension/.github", 1), HEAD)

    def test_head_sha_missing_in_payload_raises(self):
        class Stub(ReviewGateRunner):
            def _run(self, endpoint):
                return {"head": {}}

        with self.assertRaises(ReviewGateError):
            Stub().head_sha("AI-Ascension/.github", 1)

    def test_reviews_nested_pages_flattened(self):
        class Stub(ReviewGateRunner):
            def _run(self, endpoint):
                return [[review(rid=1)], [review(rid=2)]]

        self.assertEqual(len(Stub().reviews("AI-Ascension/.github", 1)), 2)

    def test_reviews_not_list_raises(self):
        class Stub(ReviewGateRunner):
            def _run(self, endpoint):
                return {"message": "Not Found"}

        with self.assertRaises(ReviewGateError):
            Stub().reviews("AI-Ascension/.github", 1)


class CheckTests(unittest.TestCase):
    def test_check_propagates_undetermined_state(self):
        class Broken:
            def head_sha(self, repository, number):
                raise ReviewGateError("boom")

            def reviews(self, repository, number):
                return []

        with self.assertRaises(ReviewGateError):
            check("AI-Ascension/.github", 1, runner=Broken())

    def test_check_uses_all_reviews_not_just_latest(self):
        # Regression for the unpinned/earliest-review audit note: reading only
        # the latest review must not be how the gate decides.
        #
        # The pinned review is deliberately FIRST and the later review is the
        # unpinned one. A `reviews[-1:]` implementation -- look only at the
        # latest -- sees the unpinned review, decides "no review of record,"
        # and fails. Only an implementation that reads the whole list finds
        # the pin at index 0. With the pinned review last, this test could not
        # tell those two implementations apart and would pass either way.
        class LatestOnly:
            def head_sha(self, repository, number):
                return HEAD

            def reviews(self, repository, number):
                return [review(rid=1, submitted="2026-09-26T01:00:00Z"),
                        review(commit_id=OTHER, rid=5, submitted="2026-09-26T09:00:00Z")]

        result = check("AI-Ascension/.github", 1, runner=LatestOnly())
        self.assertTrue(result["ok"])
        self.assertEqual(result["review_of_record_id"], 1)


class MainTests(unittest.TestCase):
    def test_main_returns_one_on_undetermined_state(self):
        # A failing check must exit nonzero so the check-run is red.
        import io
        import contextlib

        class Broken:
            def head_sha(self, repository, number):
                raise ReviewGateError("api down")

            def reviews(self, repository, number):
                return []

        original = review_gate.check
        review_gate.check = lambda repo, num: check(repo, num, runner=Broken())
        try:
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                code = main(["--repository", "AI-Ascension/.github", "--number", "1"])
            self.assertEqual(code, 1)
            self.assertIn("undetermined", buffer.getvalue())
        finally:
            review_gate.check = original


if __name__ == "__main__":
    unittest.main()
