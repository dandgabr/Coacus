"""A mechanism failure allows the call and says so on stderr (ADR 0002, D4)."""

from __future__ import annotations

import io
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest import mock

from scripts import coacus_guard

REPO = Path(__file__).resolve().parents[1]


class TestMechanismFailureAdvisory(unittest.TestCase):
    def test_a_crash_allows_and_writes_an_advisory(self) -> None:
        err = io.StringIO()
        with mock.patch.object(coacus_guard.guard, "load_policies", side_effect=RuntimeError("simulated failure")), \
                redirect_stderr(err):
            out = coacus_guard.run("claude-code", "tool.pre", "{}", REPO)
        self.assertEqual(out, "{}")
        self.assertIn("mechanism failure (RuntimeError)", err.getvalue())

    def test_the_advisory_never_carries_the_payload(self) -> None:
        err = io.StringIO()
        with mock.patch.object(coacus_guard.guard, "load_policies", side_effect=RuntimeError("secret-value")), \
                redirect_stderr(err):
            coacus_guard.run("claude-code", "tool.pre", '{"tool":"bash","tool_input":{"command":"secret"}}', REPO)
        self.assertNotIn("secret", err.getvalue())

    def test_a_normal_decision_writes_nothing_to_stderr(self) -> None:
        err = io.StringIO()
        with redirect_stderr(err):
            coacus_guard.run("claude-code", "tool.pre", "{}", REPO)
        self.assertEqual(err.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
