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

    def test_non_english_marker_warns(self) -> None:
        write_skill(self.root, "roles", "pt-skill", body="Atua como especialista em segurança.")
        warnings = skills.warnings(self.root)
        self.assertTrue(any("non-English" in w for w in warnings))

    def test_english_skill_has_no_warnings(self) -> None:
        write_skill(self.root, "roles", "en-skill")
        self.assertEqual(skills.warnings(self.root), [])


if __name__ == "__main__":
    unittest.main()


class TestFenceLanguageGate(unittest.TestCase):
    """Code fences carry diagrams and comments; PT there is a blocking error.

    The prose sweep intentionally drops fences, so a separate gate (F6b) keeps
    contamination in ASCII diagrams, code comments and string literals out.
    """

    def setUp(self) -> None:
        from engine.validators import language

        self.language = language
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name) / "repo"

    def test_fence_with_portuguese_fails(self) -> None:
        write_skill(
            self.root,
            "roles",
            "pt-fence",
            body="## Diagram\n\n```\n# Configuração do agente\n```\n",
        )
        errors = self.language.fence_errors(self.root)
        self.assertEqual(len(errors), 1)
        self.assertIn("code fence", errors[0])

    def test_prose_only_portuguese_is_not_a_fence_error(self) -> None:
        write_skill(
            self.root,
            "roles",
            "pt-prose",
            body="Atua como especialista em seguranca.\n",
        )
        self.assertEqual(self.language.fence_errors(self.root), [])

    def test_english_fence_passes(self) -> None:
        write_skill(
            self.root,
            "roles",
            "en-fence",
            body="## Diagram\n\n```\n[ Data input ]\n```\n",
        )
        self.assertEqual(self.language.fence_errors(self.root), [])

    def test_fence_exempt_file_is_skipped(self) -> None:
        write_skill(self.root, "domains", "linguistic-pt-br", body="x")
        nested = self.root / "knowledge/skills/domains/linguistics" / "linguistic-pt-br"
        nested.mkdir(parents=True)
        (nested / "SKILL.md").write_text(
            "---\nname: linguistic-pt-br\ndescription: >-\n  Teaches PT-BR.\n---\n\n"
            "# linguistic-pt-br\n\n```\n[ Configuração ]\n```\n",
            encoding="utf-8",
        )
        self.assertEqual(self.language.fence_errors(self.root), [])


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
