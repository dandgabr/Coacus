"""The security-specialist, security-architect and project-reviewer roles stay exclusive."""

from __future__ import annotations

import unittest
from pathlib import Path

from engine import router

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "knowledge" / "agents"


def _source(name: str) -> str:
    return next(AGENTS.rglob(f"{name}/agent.source.md")).read_text(encoding="utf-8")


class TestRoleBoundaries(unittest.TestCase):
    def test_specialist_answers_and_routes_but_does_not_review_or_opine(self) -> None:
        text = _source("security-specialist")
        self.assertIn("Answers information-security questions", text)
        self.assertIn("`security-architect`", text)
        self.assertIn("`project-reviewer`", text)
        self.assertIn("coacus_route.py", text)
        self.assertNotIn("<finding>", text)  # the review schema moved to the reviewer

    def test_architect_owns_the_project_security_architecture_only(self) -> None:
        text = _source("security-architect")
        self.assertIn("security architect of the project", text)
        self.assertIn("### Role boundary", text)
        self.assertIn("`security-specialist`", text)
        self.assertIn("`project-reviewer`", text)

    def test_reviewer_covers_all_aspects_and_can_dispatch(self) -> None:
        text = _source("project-reviewer")
        self.assertIn("every\n  aspect", text)
        self.assertIn("### Dispatching other agents", text)
        self.assertIn("<finding>", text)
        self.assertIn("read-only", text)
        self.assertIn("governor", text)

    def test_every_dispatching_agent_treats_returned_text_as_data(self) -> None:
        for name in ("security-specialist", "project-reviewer"):
            with self.subTest(agent=name):
                self.assertIn("untrusted-content-security", _source(name))


class TestRouting(unittest.TestCase):
    def _top(self, prompt: str) -> str:
        return router.rank(ROOT, prompt)[0].name

    def test_each_role_is_the_top_route_for_its_own_request(self) -> None:
        self.assertEqual(self._top("security question about sql injection"), "security-specialist")
        self.assertEqual(self._top("security architecture threat modeling"), "security-architect")
        self.assertEqual(self._top("full review of this project"), "project-reviewer")


if __name__ == "__main__":
    unittest.main()
