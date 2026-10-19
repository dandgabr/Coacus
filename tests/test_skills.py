"""Tests for the skill contract validator (skill-authoring, corpus import)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from engine.validators import skills


def write_skill(root: Path, category: str, name: str, body: str = "Do the thing.") -> Path:
    directory = root / "knowledge" / "skills" / category / name
    directory.mkdir(parents=True)
    skill = directory / "SKILL.md"
    skill.write_text(
        f"---\nname: {name}\ndescription: >-\n  Does {name} when asked.\n---\n\n"
        f"# {name}\n\n{body}\n",
        encoding="utf-8",
    )
    return skill


class TestSkillValidator(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name) / "repo"

    def test_valid_skill_passes(self) -> None:
        write_skill(self.root, "roles", "sample-skill")
        self.assertEqual(skills.validate(self.root), [])

    def test_name_directory_mismatch_fails(self) -> None:
        skill = write_skill(self.root, "roles", "sample-skill")
        skill.write_text(
            skill.read_text(encoding="utf-8").replace(
                "name: sample-skill", "name: other-skill"
            ),
            encoding="utf-8",
        )
        errors = skills.validate(self.root)
        self.assertTrue(any("directory name" in e for e in errors))

    def test_duplicate_slug_fails(self) -> None:
        write_skill(self.root, "roles", "dup-skill")
        write_skill(self.root, "other", "dup-skill")
        errors = skills.validate(self.root)
        self.assertTrue(any("duplicate skill name" in e for e in errors))

    def test_broken_local_link_fails(self) -> None:
        write_skill(self.root, "roles", "link-skill", body="See [x](references/missing.md).")
        errors = skills.validate(self.root)
        self.assertTrue(any("broken local link" in e for e in errors))

    def test_existing_local_link_passes(self) -> None:
        skill = write_skill(
            self.root, "roles", "link-skill", body="See [x](references/ok.md)."
        )
        references = skill.parent / "references"
        references.mkdir()
        (references / "ok.md").write_text("ok\n", encoding="utf-8")
        self.assertEqual(skills.validate(self.root), [])

    def test_external_link_is_ignored(self) -> None:
        write_skill(self.root, "roles", "ext-skill", body="See [x](https://example.com).")
        self.assertEqual(skills.validate(self.root), [])

    def test_skill_directly_under_skills_dir_fails(self) -> None:
        directory = self.root / "knowledge" / "skills"
        directory.mkdir(parents=True)
        (directory / "SKILL.md").write_text(
            "---\nname: flat\ndescription: x\n---\n\n# flat\nbody\n", encoding="utf-8"
        )
        errors = skills.validate(self.root)
        self.assertTrue(any("right depth" in e for e in errors))

    def test_nested_skill_fails(self) -> None:
        outer = write_skill(self.root, "roles", "outer-skill")
        nested_dir = outer.parent / "inner" / "inner-skill"
        nested_dir.mkdir(parents=True)
        (nested_dir / "SKILL.md").write_text(
            "---\nname: inner-skill\ndescription: x\n---\n\n# inner\nbody\n",
            encoding="utf-8",
        )
        errors = skills.validate(self.root)
        self.assertTrue(any("nested SKILL.md" in e for e in errors))

    def test_subcategory_depth_is_allowed(self) -> None:
        directory = self.root / "knowledge/skills/security/appsec/my-skill"
        directory.mkdir(parents=True)
        (directory / "SKILL.md").write_text(
            "---\nname: my-skill\ndescription: x\n---\n\n# my-skill\nbody\n",
            encoding="utf-8",
        )
        self.assertEqual(skills.validate(self.root), [])


class TestSkillWarnings(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name) / "repo"

    def test_non_english_is_blocked_by_repository_language_validator(self) -> None:
        from engine.validators import language

        write_skill(self.root, "roles", "pt-skill", body="Atua como especialista em segurança.")
        config = self.root / "config"
        config.mkdir(parents=True)
        (config / "language-exceptions.json").write_text('{"exceptions": []}\n', encoding="utf-8")
        errors = language.repository_errors(self.root)
        self.assertTrue(any("pt-skill" in error for error in errors))

    def test_english_skill_has_no_warnings(self) -> None:
        write_skill(self.root, "roles", "en-skill")
        self.assertEqual(skills.warnings(self.root), [])

    def test_oversized_description_is_blocked_by_quality_validator(self) -> None:
        from engine.validators import skill_quality

        skill = write_skill(self.root, "roles", "long-description")
        text = skill.read_text(encoding="utf-8").replace(
            "Does long-description when asked.", "x" * (1024 + 1)
        )
        skill.write_text(text, encoding="utf-8")
        errors = skill_quality.validate(self.root)
        self.assertEqual(len(errors), 1)
        self.assertIn("long-description/SKILL.md", errors[0])


if __name__ == "__main__":
    unittest.main()


class TestFenceLanguageGate(unittest.TestCase):
    """Language validation includes content in Markdown fences."""

    def setUp(self) -> None:
        from engine.validators import language

        self.language = language
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name) / "repo"
        config = self.root / "config"
        config.mkdir(parents=True)
        (config / "language-exceptions.json").write_text(
            '{"exceptions": []}\n', encoding="utf-8"
        )

    def test_fence_with_portuguese_fails(self) -> None:
        write_skill(
            self.root,
            "roles",
            "pt-fence",
            body="## Diagram\n\n```\n# Configuração do agente\n```\n",
        )
        errors = self.language.repository_errors(self.root)
        self.assertTrue(any("non-English" in error or "needs human review" in error for error in errors))

    def test_prose_portuguese_is_detected(self) -> None:
        write_skill(
            self.root,
            "roles",
            "pt-prose",
            body="Atua como especialista em seguranca.\n",
        )
        self.assertTrue(any("pt-prose" in error for error in self.language.repository_errors(self.root)))

    def test_english_fence_passes(self) -> None:
        skill = write_skill(
            self.root,
            "roles",
            "en-fence",
            body="## English Diagram\n\n```\n[ Data input ]\n```\n",
        )
        text = skill.read_text(encoding="utf-8")
        text = text.replace("Does en-fence when asked.", "Provides an English fence example.")
        text = text.replace("# en-fence", "# English Fence Example")
        skill.write_text(text, encoding="utf-8")
        self.assertEqual(self.language.repository_errors(self.root), [])

    def test_language_specific_sample_requires_exact_exception(self) -> None:
        write_skill(self.root, "domains", "linguistic-pt-br", body="x")
        nested = self.root / "knowledge/skills/domains/linguistics" / "linguistic-pt-br"
        nested.mkdir(parents=True)
        (nested / "SKILL.md").write_text(
            "---\nname: linguistic-pt-br\ndescription: >-\n  Teaches PT-BR.\n---\n\n"
            "# linguistic-pt-br\n\n```\n[ Configuração ]\n```\n",
            encoding="utf-8",
        )
        self.assertTrue(any("linguistic-pt-br" in error for error in self.language.repository_errors(self.root)))


class TestStraySkillGuard(unittest.TestCase):
    """I1: a SKILL.md outside the known roots is never registered or installed."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name) / "repo"

    def test_stray_skill_outside_roots_is_rejected(self) -> None:
        write_skill(self.root, "roles", "sample-skill")  # a valid one
        stray = self.root / "knowledge/rules/stray"
        stray.mkdir(parents=True)
        (stray / "SKILL.md").write_text(
            "---\nname: stray\ndescription: >-\n  Stray.\n---\n\n# stray\n",
            encoding="utf-8",
        )
        errors = skills.validate(self.root)
        self.assertTrue(any("outside a known skill root" in e for e in errors))

    def test_workflow_root_is_not_stray(self) -> None:
        workflow = self.root / "methodology/workflows/using-coacus"
        workflow.mkdir(parents=True)
        (workflow / "SKILL.md").write_text(
            "---\nname: using-coacus\ndescription: >-\n  Entry.\n---\n\n# using-coacus\n",
            encoding="utf-8",
        )
        self.assertEqual(skills.validate(self.root), [])
