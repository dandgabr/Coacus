"""Tests for the skill-quality lint (skill-authoring)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from engine.validators import skill_quality


def write_skill(root: Path, name: str, body: str = "Do the thing.", description: str | None = None) -> Path:
    directory = root / "knowledge" / "skills" / "roles" / name
    directory.mkdir(parents=True)
    description = description or f"Does {name} when asked."
    skill = directory / "SKILL.md"
    skill.write_text(
        f"---\nname: {name}\ndescription: >-\n  {description}\n---\n\n"
        f"# {name}\n\n{body}\n",
        encoding="utf-8",
    )
    return skill


class TestSkillQualityErrors(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name) / "repo"

    def test_clean_skill_has_no_errors(self) -> None:
        write_skill(self.root, "sample-skill")
        self.assertEqual(skill_quality.validate(self.root), [])

    def test_name_over_sixty_four_chars_fails(self) -> None:
        write_skill(self.root, "s" + "x" * 64)
        errors = skill_quality.validate(self.root)
        self.assertTrue(any("max 64" in e for e in errors))

    def test_unbalanced_fence_fails(self) -> None:
        write_skill(self.root, "fence-skill", body="```\ncode\n")
        errors = skill_quality.validate(self.root)
        self.assertTrue(any("unbalanced code fence" in e for e in errors))

    def test_balanced_fences_pass(self) -> None:
        write_skill(self.root, "fence-skill", body="```\ncode\n```\n")
        self.assertEqual(skill_quality.validate(self.root), [])


class TestSkillQualityWarnings(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name) / "repo"

    def test_oversized_body_warns(self) -> None:
        write_skill(self.root, "big-skill", body="word " * 4000)
        warnings = skill_quality.warnings(self.root)
        self.assertTrue(any("move depth into references" in w for w in warnings))

    def test_instruction_opener_description_warns(self) -> None:
        write_skill(
            self.root,
            "reader-skill",
            description="Use this skill when reviewing things.",
        )
        warnings = skill_quality.warnings(self.root)
        self.assertTrue(any("instruction-to-reader" in w for w in warnings))

    def test_clean_skill_has_no_warnings(self) -> None:
        write_skill(self.root, "sample-skill")
        self.assertEqual(skill_quality.warnings(self.root), [])


if __name__ == "__main__":
    unittest.main()
