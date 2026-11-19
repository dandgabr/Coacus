"""Installer: retire what left the corpus, and partial or total removal."""

from __future__ import annotations

import json
import os
import shutil
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from scripts import coacus_install

from tests.test_install import add_agent, add_skill, make_repo


class InstallerCase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name)
        env = patch.dict(
            os.environ,
            {"APPDATA": str(self.tmp / "appdata"), "LOCALAPPDATA": str(self.tmp / "localappdata")},
        )
        env.start()
        self.addCleanup(env.stop)
        self.root = make_repo(self.tmp)
        self.config = self.tmp / "config"
        self.alpha = add_agent(self.root, "knowledge/agents/roles/alpha-agent")
        self.beta = add_agent(self.root, "knowledge/agents/roles/beta-agent")
        add_skill(self.root, "knowledge/skills/languages/lang-python")
        add_skill(self.root, "knowledge/skills/languages/lang-rust")

    def install(self, **kwargs) -> dict:
        return coacus_install.install(
            "opencode", self.root, self.config, dry_run=False, lock_skills=False, **kwargs
        )

    def agent_file(self, name: str) -> Path:
        return self.config / "agent" / f"{name}.md"

    def manifest(self) -> dict:
        return json.loads((self.config / coacus_install.MANIFEST_NAME).read_text(encoding="utf-8"))


class TestRetireRemovedFromCorpus(InstallerCase):
    def test_full_install_retires_an_agent_that_left_the_corpus(self) -> None:
        self.install()
        self.assertTrue(self.agent_file("beta-agent").is_file())
        shutil.rmtree(self.beta)
        self.install()
        self.assertFalse(self.agent_file("beta-agent").exists())
        self.assertTrue(self.agent_file("alpha-agent").is_file())
        self.assertNotIn(self.agent_file("beta-agent").as_posix(), self.manifest()["files"])
        self.assertTrue(coacus_install.verify("opencode", self.root, self.config)["ok"])

    def test_full_install_retires_a_skill_that_left_the_corpus(self) -> None:
        self.install()
        gone = self.config / "skills/lang-rust/SKILL.md"
        self.assertTrue(gone.is_file())
        shutil.rmtree(self.root / "knowledge/skills/languages/lang-rust")
        self.install()
        self.assertFalse(gone.exists())
        self.assertFalse((self.config / "skills/lang-rust").exists())

    def test_an_edited_installed_agent_is_kept_and_reported(self) -> None:
        self.install()
        edited = self.agent_file("beta-agent")
        edited.write_text("my own notes", encoding="utf-8")
        shutil.rmtree(self.beta)
        result = self.install()
        self.assertEqual(edited.read_text(encoding="utf-8"), "my own notes")
        self.assertIn(edited.as_posix(), result["retained"])

    def test_a_filtered_install_does_not_retire_the_files_it_left_out(self) -> None:
        self.install()
        self.install(agents=["alpha-*"])
        self.assertTrue(self.agent_file("beta-agent").is_file())

    def test_a_file_outside_the_artifact_trees_is_not_retired_by_absence(self) -> None:
        self.install()
        self.assertFalse(coacus_install._is_artifact_path(
            self.config / "hooks.json", [self.config]))
        self.assertTrue(coacus_install._is_artifact_path(
            self.config / "agents/x.md", [self.config]))
        self.assertTrue(coacus_install._is_artifact_path(
            self.config / "config/plugins/coacus/catalog/corpus/a.md", [self.config]))


class TestRemoval(InstallerCase):
    def remove(self, **kwargs) -> dict:
        return coacus_install.uninstall("opencode", self.root, self.config, **kwargs)

    def test_partial_removal_by_agent_keeps_everything_else(self) -> None:
        self.install()
        result = self.remove(agents=["beta-*"])
        self.assertTrue(result["partial"])
        self.assertFalse(self.agent_file("beta-agent").exists())
        self.assertTrue(self.agent_file("alpha-agent").is_file())
        self.assertTrue((self.config / "skills/lang-python/SKILL.md").is_file())
        self.assertTrue(coacus_install.verify("opencode", self.root, self.config)["ok"])
        self.assertIn(self.agent_file("beta-agent").as_posix(), self.manifest()["removed"])

    def test_partial_removal_by_skill(self) -> None:
        self.install()
        self.remove(skills=["lang-rust"])
        self.assertFalse((self.config / "skills/lang-rust").exists())
        self.assertTrue((self.config / "skills/lang-python/SKILL.md").is_file())
        self.assertTrue(self.agent_file("alpha-agent").is_file())

    def test_partial_removal_of_a_name_that_left_the_corpus(self) -> None:
        self.install()
        shutil.rmtree(self.beta)
        self.remove(agents=["beta-agent"])
        self.assertFalse(self.agent_file("beta-agent").exists())

    def test_partial_removal_dry_run_changes_nothing(self) -> None:
        self.install()
        before = self.manifest()
        result = self.remove(agents=["beta-*"], dry_run=True)
        self.assertEqual(result["removed"], [self.agent_file("beta-agent").as_posix()])
        self.assertTrue(self.agent_file("beta-agent").is_file())
        self.assertEqual(self.manifest(), before)

    def test_partial_removal_with_no_match_says_so(self) -> None:
        self.install()
        result = self.remove(agents=["nothing-*"])
        self.assertEqual(result["removed"], [])
        self.assertIn("nothing recorded", result["note"])

    def test_partial_removal_keeps_a_locally_edited_file(self) -> None:
        self.install()
        edited = self.agent_file("beta-agent")
        edited.write_text("my own notes", encoding="utf-8")
        result = self.remove(agents=["beta-*"])
        self.assertEqual(edited.read_text(encoding="utf-8"), "my own notes")
        self.assertIn(edited.as_posix(), result["skipped"])
        self.assertIn(edited.as_posix(), self.manifest()["files"])

    def test_a_reinstall_restores_what_a_partial_removal_took(self) -> None:
        self.install()
        self.remove(agents=["beta-*"])
        self.install()
        self.assertTrue(self.agent_file("beta-agent").is_file())
        self.assertNotIn("removed", self.manifest())
        self.assertTrue(coacus_install.verify("opencode", self.root, self.config)["ok"])

    def test_total_removal_deletes_the_manifest(self) -> None:
        self.install()
        result = self.remove()
        self.assertFalse(result["partial"])
        self.assertFalse((self.config / coacus_install.MANIFEST_NAME).exists())
        self.assertFalse(self.agent_file("alpha-agent").exists())

    def test_remove_flag_is_an_alias_of_uninstall_and_takes_filters(self) -> None:
        self.install()
        with redirect_stdout(StringIO()):
            code = coacus_install.main(
                ["opencode", "--remove", "--agents", "beta-*", "--config-dir", str(self.config)],
                root=self.root,
            )
        self.assertEqual(code, 0)
        self.assertFalse(self.agent_file("beta-agent").exists())
        self.assertTrue(self.agent_file("alpha-agent").is_file())


if __name__ == "__main__":
    unittest.main()
