"""Tests for canonical agent validation (D1) and hygiene (D2/D12)."""

from __future__ import annotations

import unittest

from engine.validators import agents as agent_validator
from engine.validators import hygiene

from tests.support import make_repo


class TestAgentValidator(unittest.TestCase):
    def setUp(self) -> None:
        import tempfile

        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = make_repo(self._tmp_path())

    def _tmp_path(self):
        from pathlib import Path

        return Path(self._tmp.name)

    def _source(self):
        return (
            self.root
            / "knowledge/agents/roles/sample-agent/agent.source.md"
        )

    def test_valid_repo_passes(self) -> None:
        self.assertEqual(agent_validator.validate(self.root), [])

    def test_directory_name_mismatch_fails(self) -> None:
        source = self._source()
        text = source.read_text(encoding="utf-8").replace(
            "name: sample-agent", "name: other-name"
        )
        source.write_text(text, encoding="utf-8")
        errors = agent_validator.validate(self.root)
        self.assertTrue(any("directory name" in e for e in errors))

    def test_missing_skill_path_fails(self) -> None:
        source = self._source()
        text = source.read_text(encoding="utf-8").replace(
            "  - knowledge/skills/roles/sample-skill/SKILL.md",
            "  - knowledge/skills/roles/ghost/SKILL.md",
        )
        source.write_text(text, encoding="utf-8")
        errors = agent_validator.validate(self.root)
        self.assertTrue(any("does not exist" in e for e in errors))

    def test_non_kebab_name_fails(self) -> None:
        source = self._source()
        text = source.read_text(encoding="utf-8").replace(
            "name: sample-agent", "name: Sample Agent"
        )
        source.write_text(text, encoding="utf-8")
        errors = agent_validator.validate(self.root)
        self.assertTrue(any("kebab-case" in e for e in errors))

    def test_model_in_source_fails(self) -> None:
        source = self._source()
        text = source.read_text(encoding="utf-8").replace(
            "description: >-\n", "model: inherit\ndescription: >-\n"
        )
        source.write_text(text, encoding="utf-8")
        errors = agent_validator.validate(self.root)
        self.assertTrue(any("'model' must be omitted" in e for e in errors))


class TestHygiene(unittest.TestCase):
    def setUp(self) -> None:
        import tempfile

        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = make_repo(self._tmp_path())

    def _tmp_path(self):
        from pathlib import Path

        return Path(self._tmp.name)

    def _skill(self):
        return self.root / "knowledge/skills/roles/sample-skill/SKILL.md"

    def test_clean_repo_passes(self) -> None:
        self.assertEqual(hygiene.validate(self.root), [])

    def test_absolute_path_is_rejected(self) -> None:
        skill = self._skill()
        skill.write_text(
            skill.read_text(encoding="utf-8") + "\nSee /home/dev/notes.md\n",
            encoding="utf-8",
        )
        errors = hygiene.validate(self.root)
        self.assertTrue(any("absolute path" in e for e in errors))

    def test_secret_literal_is_rejected(self) -> None:
        skill = self._skill()
        skill.write_text(
            skill.read_text(encoding="utf-8") + '\napi_key = "supersecret123"\n',
            encoding="utf-8",
        )
        errors = hygiene.validate(self.root)
        self.assertTrue(any("credential" in e for e in errors))

    def test_env_interpolation_is_accepted(self) -> None:
        skill = self._skill()
        skill.write_text(
            skill.read_text(encoding="utf-8") + "\napi_key = {env:API_KEY}\n",
            encoding="utf-8",
        )
        self.assertEqual(hygiene.validate(self.root), [])

    def test_tool_name_in_skill_body_is_rejected(self) -> None:
        skill = self._skill()
        skill.write_text(
            skill.read_text(encoding="utf-8") + "\nNow call the WebFetch tool.\n",
            encoding="utf-8",
        )
        errors = hygiene.validate(self.root)
        self.assertTrue(any("tool name" in e for e in errors))

    def test_windows_absolute_path_is_rejected(self) -> None:
        skill = self._skill()
        skill.write_text(
            skill.read_text(encoding="utf-8") + "\nOpen C:\\Users\\dev\\file.md\n",
            encoding="utf-8",
        )
        errors = hygiene.validate(self.root)
        self.assertTrue(any("absolute path" in e for e in errors))

    def test_forward_slash_windows_path_is_rejected(self) -> None:
        skill = self._skill()
        skill.write_text(
            skill.read_text(encoding="utf-8") + "\nOpen C:/Users/dev/file.md\n",
            encoding="utf-8",
        )
        errors = hygiene.validate(self.root)
        self.assertTrue(any("absolute path" in e for e in errors))

    def test_tilde_home_path_is_rejected(self) -> None:
        skill = self._skill()
        skill.write_text(
            skill.read_text(encoding="utf-8") + "\nStored at file:///home/dev/notes.md\n",
            encoding="utf-8",
        )
        errors = hygiene.validate(self.root)
        self.assertTrue(any("absolute path" in e for e in errors))

    def test_system_paths_are_allowed(self) -> None:
        # D12 targets machine-specific paths; documented OS paths must pass.
        skill = self._skill()
        skill.write_text(
            skill.read_text(encoding="utf-8")
            + "\nConfig lives at /etc/systemd/system/foo.service\n",
            encoding="utf-8",
        )
        self.assertEqual(hygiene.validate(self.root), [])

    def test_api_endpoints_are_allowed(self) -> None:
        skill = self._skill()
        skill.write_text(
            skill.read_text(encoding="utf-8") + "\nGET /v1/orders and /health/live\n",
            encoding="utf-8",
        )
        self.assertEqual(hygiene.validate(self.root), [])

    def test_code_fences_are_not_scanned(self) -> None:
        skill = self._skill()
        skill.write_text(
            skill.read_text(encoding="utf-8")
            + "\n```ini\nwsrep_provider = /usr/lib/galera/libgalera_smm.so\n```\n",
            encoding="utf-8",
        )
        self.assertEqual(hygiene.validate(self.root), [])

    def test_dollar_var_interpolation_is_accepted(self) -> None:
        skill = self._skill()
        skill.write_text(
            skill.read_text(encoding="utf-8") + "\ntoken = ${API_TOKEN}\n",
            encoding="utf-8",
        )
        self.assertEqual(hygiene.validate(self.root), [])


class TestAgentValidatorAdditional(unittest.TestCase):
    def setUp(self) -> None:
        import tempfile

        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = make_repo(self._tmp_path())

    def _tmp_path(self):
        from pathlib import Path

        return Path(self._tmp.name)

    def _source(self):
        return self.root / "knowledge/agents/roles/sample-agent/agent.source.md"

    def test_category_mismatch_fails(self) -> None:
        source = self._source()
        source.write_text(
            source.read_text(encoding="utf-8").replace(
                "category: roles", "category: engineering"
            ),
            encoding="utf-8",
        )
        errors = agent_validator.validate(self.root)
        self.assertTrue(any("directory category" in e for e in errors))

    def test_empty_body_fails(self) -> None:
        source = self._source()
        source.write_text(
            "---\nname: sample-agent\ncategory: roles\n"
            "description: >-\n  Sample.\nskills: []\n---\n",
            encoding="utf-8",
        )
        errors = agent_validator.validate(self.root)
        self.assertTrue(any("instruction body is empty" in e for e in errors))

    def test_duplicate_name_fails(self) -> None:
        import shutil

        first = self.root / "knowledge/agents/roles/sample-agent"
        second = self.root / "knowledge/agents/roles/other-agent"
        shutil.copytree(first, second)
        errors = agent_validator.validate(self.root)
        self.assertTrue(any("duplicate agent name" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
