"""Contract checks for the security assessment planner skill."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from engine.frontmatter import parse

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "knowledge/skills/security/appsec/security-assessment-planning/SKILL.md"
ACTIVATION_SET = ROOT / "evals/fixtures/activation/security-assessment-planning.json"


class TestSecurityAssessmentPlanning(unittest.TestCase):
    def test_activation_fixture_covers_positive_and_near_miss_in_both_languages(self) -> None:
        data = json.loads(ACTIVATION_SET.read_text(encoding="utf-8"))
        cases = data["cases"]
        self.assertEqual(
            {(case["intent"], case["language"]) for case in cases},
            {
                ("positive", "en"),
                ("positive", "pt-BR"),
                ("near-miss", "en"),
                ("near-miss", "pt-BR"),
            },
        )
        self.assertTrue(all(case["prompt"].strip() for case in cases))

    def test_planner_routes_surfaces_and_preserves_scope_boundary(self) -> None:
        doc = parse(SKILL.read_text(encoding="utf-8"))
        body = doc.body.lower()
        for requirement in (
            "authorization",
            "source code",
            "live web",
            "api",
            "ci",
            "needs validation",
            "review-findings-pipeline",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, body)

    def test_every_link_resolves(self) -> None:
        doc = parse(SKILL.read_text(encoding="utf-8"))
        import re

        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", doc.body):
            if target.startswith(("https://", "http://", "#")):
                continue
            self.assertTrue((SKILL.parent / target.split("#", 1)[0]).exists(), target)


if __name__ == "__main__":
    unittest.main()
