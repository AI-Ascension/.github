"""HTTP failure semantics and secret-free diagnostics, without network access."""
import subprocess
import unittest
from unittest.mock import patch

from test_metadata import metadata, FakeRunner


class TransportTests(unittest.TestCase):
    def test_http_failures_are_classified_without_exposing_response_text(self):
        categories = {401: "authentication", 403: "authentication", 404: "not_found", 409: "conflict", 422: "validation", 429: "rate_limit"}
        for status, category in categories.items():
            response = subprocess.CompletedProcess([], 1, stdout=f"HTTP/2.0 {status}\n\n{{}}", stderr="synthetic-secret-marker")
            with self.subTest(status=status), patch.object(metadata.subprocess, "run", return_value=response):
                with self.assertRaises(metadata.APIError) as failure:
                    metadata.CommandRunner().run(["gh", "api", "--include", "user"])
                self.assertEqual(category, failure.exception.category)
                self.assertNotIn("synthetic-secret-marker", str(failure.exception))

    def test_success_headers_are_removed_before_json_parsing(self):
        response = subprocess.CompletedProcess([], 0, stdout='HTTP/2.0 200 OK\r\nX-RateLimit-Remaining: 50\r\n\r\n{"names":[]}', stderr="")
        with patch.object(metadata.subprocess, "run", return_value=response):
            self.assertEqual({"names": []}, metadata.GitHubClient()._run("repos/AI-Ascension/example/topics"))

    def test_safe_read_obeys_known_retry_after_with_bounded_attempts(self):
        runner = FakeRunner([metadata.APIError("limited", "rate_limit", retry_after=7), '{"names":[]}'])
        with patch.object(metadata.time, "sleep") as sleep:
            self.assertEqual({"names": []}, metadata.GitHubClient(runner=runner, retries=1)._run("repos/AI-Ascension/example/topics"))
        sleep.assert_called_once_with(7)
        self.assertEqual(2, len(runner.calls))

    def test_long_limit_and_write_limit_stop_without_retry(self):
        for method, delay in [("GET", 120), ("PUT", 5), ("GET", None)]:
            runner = FakeRunner([metadata.APIError("limited", "rate_limit", retry_after=delay)])
            with self.subTest(method=method, delay=delay), patch.object(metadata.time, "sleep") as sleep:
                with self.assertRaises(metadata.APIError):
                    metadata.GitHubClient(runner=runner)._run("repos/AI-Ascension/example/topics", method=method)
                sleep.assert_not_called()
                self.assertEqual(1, len(runner.calls))

    def test_rate_limit_reset_cannot_be_shortened_by_retry_after(self):
        response = subprocess.CompletedProcess([], 1, stdout="HTTP/2.0 429\nRetry-After: 2\nX-RateLimit-Remaining: 0\nX-RateLimit-Reset: 110\n\n{}", stderr="rate limit exceeded")
        with patch.object(metadata.subprocess, "run", return_value=response), patch.object(metadata.time, "time", return_value=100):
            with self.assertRaises(metadata.APIError) as failure:
                metadata.CommandRunner().run(["gh", "api", "--include", "user"])
        self.assertGreaterEqual(failure.exception.retry_after, 10)

    def test_limited_reads_exhaust_the_attempt_budget(self):
        runner = FakeRunner([metadata.APIError("limited", "rate_limit", retry_after=1) for _ in range(3)])
        with patch.object(metadata.time, "sleep") as sleep:
            with self.assertRaises(metadata.APIError):
                metadata.GitHubClient(runner=runner, retries=2)._run("user")
        self.assertEqual([1, 2], [x.args[0] for x in sleep.call_args_list])
        self.assertEqual(3, len(runner.calls))


if __name__ == "__main__":
    unittest.main()
