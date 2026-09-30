"""Consistency tests: the workflow docs must describe the roster and ship steps."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONVENTIONS = (
    ROOT / "methodology/workflows/using-coacus/references/coacus-process-conventions.md"
)
WRITING_PLANS = ROOT / "methodology/workflows/superpowers-writing-plans/SKILL.md"
SUBAGENT = (
    ROOT / "methodology/workflows/superpowers-subagent-driven-development/SKILL.md"
)
FINISHING = (
    ROOT / "methodology/workflows/superpowers-finishing-a-development-branch/SKILL.md"
)
ROUTING_STD = ROOT / "docs/standards/routing.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class TestRosterStep(unittest.TestCase):
    def test_conventions_document_the_roster_step(self) -> None:
        text = read(CONVENTIONS)
        self.assertIn("numbered", text.lower())
        self.assertIn("coacus_route.py", text)

    def test_writing_plans_runs_the_roster(self) -> None:
        self.assertIn("roster", read(WRITING_PLANS).lower())

    def test_subagent_development_consumes_the_roster(self) -> None:
        self.assertIn("roster", read(SUBAGENT).lower())


class TestShipSteps(unittest.TestCase):
    def test_conventions_document_push_and_reinstall(self) -> None:
        text = read(CONVENTIONS)
        self.assertIn("gh pr create", text)
        self.assertIn("coacus_install.py", text)
        self.assertIn("--verify", text)

    def test_finishing_references_the_ship_steps(self) -> None:
        self.assertIn("coacus_install.py", read(FINISHING))


class TestRoutingStandard(unittest.TestCase):
    def test_routing_allows_the_planning_roster(self) -> None:
        self.assertIn("roster", read(ROUTING_STD).lower())

    def test_routing_keeps_the_orchestrator_as_a_caller(self) -> None:
        self.assertIn("by the orchestrator", read(ROUTING_STD).lower())


class TestShipClaimsAreTrue(unittest.TestCase):
    def test_conventions_does_not_overclaim_a_verify_skip(self) -> None:
        self.assertNotIn("undetected harness is skipped", read(CONVENTIONS).lower())

    def test_conventions_does_not_overclaim_suggestions(self) -> None:
        # `--agents` only prints suggestions when a close match exists.
        self.assertNotIn("exits non-zero with suggestions", read(CONVENTIONS).lower())

    def test_pr_command_carries_an_explicit_body(self) -> None:
        # --fill pulls the body from commits and cannot carry the diffs the doc requires.
        self.assertNotIn("gh pr create --fill", read(CONVENTIONS))

    def test_generated_diff_paths_are_nested(self) -> None:
        # There is no root `dist/`; the generated trees live under knowledge/**/dist/.
        self.assertIn("knowledge/**/dist/", read(CONVENTIONS))


class TestHandoffNamesTheRoster(unittest.TestCase):
    def test_writing_plans_handoff_names_the_roster(self) -> None:
        # The handoff message itself must name the roster, not merely reference it.
        self.assertIn("Agent roster:", read(WRITING_PLANS))


if __name__ == "__main__":
    unittest.main()
