"""Tests for the agent specialty validator (agent-roles)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from engine.validators import specialty

from tests.support import make_repo

BOUNDARIES = (
    "\n## Responsibility boundaries\n\n"
    "| Concern | Owner |\n|---|---|\n| Something else | `{owner}` |\n\n"
    "You own the sample duty.\n"
)


class TestSpecialtyValidator(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = make_repo(Path(self._tmp.name))
        self.source = self.root / "knowledge/agents/roles/sample-agent/agent.source.md"

    def _append(self, text: str) -> None:
        """Replace the fixture's boundaries section with ``text`` (possibly empty)."""
        original = self.source.read_text(encoding="utf-8")
        head = original.split("\n## Responsibility boundaries", 1)[0]
        self.source.write_text(head + text, encoding="utf-8")

    def test_missing_boundaries_fails(self) -> None:
        self._append("\n")
        errors = specialty.validate(self.root)
        self.assertTrue(any("Responsibility boundaries" in e for e in errors))

    def test_boundaries_naming_an_existing_agent_pass(self) -> None:
        self._append(BOUNDARIES.format(owner="sample-agent"))
        self.assertEqual(specialty.validate(self.root), [])

    def test_unknown_owner_fails(self) -> None:
        self._append(BOUNDARIES.format(owner="retired-agent"))
        errors = specialty.validate(self.root)
        self.assertTrue(any("retired-agent" in e for e in errors))

    def test_free_text_owner_is_not_checked(self) -> None:
        self._append(BOUNDARIES.format(owner="the default coding agent"))
        self.assertEqual(specialty.validate(self.root), [])

    def test_a_heading_with_an_emoji_prefix_counts(self) -> None:
        self._append(
            BOUNDARIES.format(owner="sample-agent").replace(
                "## Responsibility", "## 🧭 Responsibility"
            )
        )
        self.assertEqual(specialty.validate(self.root), [])

    def test_wholly_contained_skill_sets_fail(self) -> None:
        skills = self.root / "knowledge/skills/roles"
        names = [f"skill-{i}" for i in range(6)]
        for name in names:
            (skills / name).mkdir(parents=True)
            (skills / name / "SKILL.md").write_text(
                f"---\nname: {name}\ndescription: Does {name} work. Use when needed.\n---\n\nBody.\n",
                encoding="utf-8",
            )
        listing = "".join(f"  - knowledge/skills/roles/{n}/SKILL.md\n" for n in names)
        for agent, count in (("big-agent", 6), ("small-agent", 5)):
            folder = self.root / "knowledge/agents/roles" / agent
            folder.mkdir(parents=True)
            (folder / "agent.source.md").write_text(
                f"---\nname: {agent}\ncategory: roles\ndescription: >-\n  Agent {agent}.\n"
                f"skills:\n{''.join(listing.splitlines(True)[:count])}---\n\n"
                f"Body.\n{BOUNDARIES.format(owner='sample-agent')}",
                encoding="utf-8",
            )
        errors = specialty.validate(self.root)
        self.assertTrue(any("overlap 5/5" in e for e in errors), errors)

    def test_baseline_skills_do_not_count_as_overlap(self) -> None:
        skills = self.root / "knowledge/skills/roles"
        names = ["version-freshness", "clean-code-reusability", "security-privacy"]
        for name in names:
            (skills / name).mkdir(parents=True, exist_ok=True)
            (skills / name / "SKILL.md").write_text(
                f"---\nname: {name}\ndescription: Does {name} work. Use when needed.\n---\n\nBody.\n",
                encoding="utf-8",
            )
        listing = "".join(f"  - knowledge/skills/roles/{n}/SKILL.md\n" for n in names)
        for agent in ("one-agent", "two-agent"):
            folder = self.root / "knowledge/agents/roles" / agent
            folder.mkdir(parents=True)
            (folder / "agent.source.md").write_text(
                f"---\nname: {agent}\ncategory: roles\ndescription: >-\n  Agent {agent}.\n"
                f"skills:\n{listing}---\n\nBody.\n{BOUNDARIES.format(owner='sample-agent')}",
                encoding="utf-8",
            )
        self.assertFalse(any("overlap" in e for e in specialty.validate(self.root)))


if __name__ == "__main__":
    unittest.main()
