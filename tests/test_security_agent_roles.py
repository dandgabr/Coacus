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
        self.assertIn("## Responsibility boundaries", text)
        self.assertIn("`security-specialist`", text)
        self.assertIn("`project-reviewer`", text)

    def test_reviewer_covers_all_aspects_and_can_dispatch(self) -> None:
        text = _source("project-reviewer")
        self.assertIn("across every", " ".join(text.split()))
        self.assertIn("### Dispatching other agents", text)
        self.assertIn("<finding>", text)
        self.assertIn("read-only", text)
        self.assertIn("governor", text.lower())

    def test_every_dispatching_agent_has_the_authorization_gate(self) -> None:
        for name in ("security-specialist", "security-architect", "project-reviewer"):
            text = " ".join(_source(name).split())
            with self.subTest(agent=name):
                self.assertIn("authorizes coordination", text)
                self.assertIn("never ", text)
                self.assertIn("`NEED_INFO`", text)

    def test_dispatchers_refuse_agents_defined_inside_the_target(self) -> None:
        for name in ("security-specialist", "project-reviewer"):
            text = " ".join(_source(name).split())
            with self.subTest(agent=name):
                self.assertIn("lives inside the target under review", text)
                self.assertIn("maximum depth is 1", text)

    def test_reviewer_dispatches_read_only_or_says_it_is_unenforced(self) -> None:
        text = " ".join(_source("project-reviewer").split())
        self.assertIn("read-only tool allowlist", text)
        self.assertIn("unenforced read-only", text)

    def test_a_security_only_review_has_an_owner(self) -> None:
        reviewer = " ".join(_source("project-reviewer").split())
        self.assertIn("review limited to one aspect such as security", reviewer)
        specialist = " ".join(_source("security-specialist").split())
        self.assertIn("limited to one such as security", specialist)

    def test_specialist_names_an_owner_for_running_appsec_tools(self) -> None:
        self.assertIn("`devops-engineer`", _source("security-specialist"))

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
        self.assertEqual(self._top("code review of this change"), "project-reviewer")

    def test_review_and_question_requests_reach_the_right_role(self) -> None:
        cases = (("review this pull request", "project-reviewer"),
                 ("security-only review of this change", "project-reviewer"),
                 ("explain owasp asvs level 2", "security-specialist"),
                 ("threat model our payment service", "security-architect"))
        for prompt, expected in cases:
            with self.subTest(prompt=prompt):
                names = [c.name for c in router.rank(ROOT, prompt, limit=4)]
                self.assertIn(expected, names, prompt)

    def test_tool_and_review_requests_reach_an_agent_that_can_hand_them_on(self) -> None:
        # The specialist is the front door: it may rank first for these, and its
        # body names the owner. The test pins that the owner is also among the top 6.
        for prompt, owner in (("security review of this api", "project-reviewer"),
                              ("run a dast scan with zap", "devops-engineer"),
                              ("threat model review", "security-architect")):
            with self.subTest(prompt=prompt):
                top = [c.name for c in router.rank(ROOT, prompt, limit=6)]
                self.assertIn(owner, top, prompt)


if __name__ == "__main__":
    unittest.main()
