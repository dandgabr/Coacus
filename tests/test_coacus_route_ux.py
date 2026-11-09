"""Tests for CLI UX Ergonomics in coacus_route.py (Fitts, Hick, Miller, Von Restorff, Jakob)."""

from __future__ import annotations

import io
import os
import unittest
from pathlib import Path
from unittest.mock import patch

from engine.router import Candidate
from scripts.coacus_route import DEFAULT_INTERACTIVE_TOP, format_candidates, main

ROOT = Path(__file__).resolve().parents[1]


class TestCoacusRouteUX(unittest.TestCase):
    def setUp(self) -> None:
        self.candidates = [
            Candidate(
                name="software-architect",
                category="software-engineering",
                score=10.0,
                matched=["architecture", "design"],
                description="Software Architecture Agent that applies DDD and SOLID.",
            ),
            Candidate(
                name="ui-ux-designer",
                category="software-engineering",
                score=8.5,
                matched=["ux", "design"],
                description="Senior specialist agent in Interface Design and UX.",
            ),
            Candidate(
                name="frontend-developer",
                category="software-engineering",
                score=6.0,
                matched=["frontend"],
                description="Frontend developer specialist.",
            ),
            Candidate(
                name="qa-engineer",
                category="software-engineering",
                score=5.0,
                matched=["qa"],
                description="Quality assurance engineer.",
            ),
            Candidate(
                name="backend-developer",
                category="software-engineering",
                score=4.0,
                matched=["backend"],
                description="Backend developer specialist.",
            ),
        ]

    def test_raw_format_produces_exact_tsv(self) -> None:
        """Raw format must strictly produce score\\tname\\tcategory\\tmatched (Jakob/Unix)."""
        output = format_candidates(self.candidates[:2], raw=True)
        lines = output.splitlines()
        self.assertEqual(len(lines), 2)
        self.assertEqual(
            lines[0],
            "10.0\tsoftware-architect\tsoftware-engineering\tarchitecture,design",
        )
        self.assertEqual(
            lines[1],
            "8.5\tui-ux-designer\tsoftware-engineering\tux,design",
        )

    def test_interactive_format_no_color(self) -> None:
        """When use_color=False (NO_COLOR), must format clean layout with zero ANSI escape codes."""
        output = format_candidates(self.candidates[:3], raw=False, use_color=False)
        self.assertNotIn("\033[", output)
        self.assertIn("PRIMARY RECOMMENDATION: software-architect", output)
        self.assertIn("Specialist Alternatives:", output)
        self.assertIn("ui-ux-designer", output)
        self.assertIn("frontend-developer", output)
        # Fitts's Law: quick action must be on the very last line
        lines = output.strip().splitlines()
        self.assertTrue(lines[-1].startswith("Quick action: python3 scripts/coacus_install.py"))
        self.assertIn("software-architect", lines[-1])

    def test_interactive_format_with_color(self) -> None:
        """When use_color=True, ANSI styles isolate primary candidate (Von Restorff)."""
        output = format_candidates(self.candidates[:3], raw=False, use_color=True)
        self.assertIn("\033[1m", output)  # Verify ANSI bold escape sequence is present.
        self.assertIn("★ PRIMARY RECOMMENDATION:", output)
        self.assertIn("software-architect", output)
        lines = output.strip().splitlines()
        self.assertTrue(lines[-1].startswith("Quick action:"))

    def test_progressive_disclosure_hint(self) -> None:
        """When total matches exceed displayed candidates, progressive disclosure hint is shown (Hick)."""
        output = format_candidates(
            self.candidates[:DEFAULT_INTERACTIVE_TOP],
            raw=False,
            use_color=False,
            total_matches=len(self.candidates),
        )
        self.assertIn("and 1 more candidates (use --all or --top <N> to view all)", output)

    def test_cli_main_raw_flag(self) -> None:
        """Passing --raw outputs TSV to stdout."""
        stdout = io.StringIO()
        with patch("sys.stdout", stdout):
            ret = main(["software architecture", "--raw"])
        self.assertEqual(ret, 0)
        output = stdout.getvalue()
        first_line = output.splitlines()[0]
        parts = first_line.split("\t")
        self.assertGreaterEqual(len(parts), 3)

    def test_cli_piped_defaults_to_raw(self) -> None:
        """When sys.stdout.isatty() is False, automatically defaults to TSV without flags."""
        stdout = io.StringIO()
        with patch("sys.stdout", stdout), patch("sys.stdout.isatty", return_value=False):
            ret = main(["software architecture"])
        self.assertEqual(ret, 0)
        output = stdout.getvalue()
        first_line = output.splitlines()[0]
        parts = first_line.split("\t")
        self.assertGreaterEqual(len(parts), 3)


if __name__ == "__main__":
    unittest.main()
