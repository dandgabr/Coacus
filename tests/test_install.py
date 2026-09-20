"""Tests for the Coacus installer (scripts/coacus_install.py)."""

from __future__ import annotations

import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from scripts import coacus_install

ENTRY = """---
name: using-coacus
description: >-
  Establishes how to work in a Coacus repository. Use when starting any task.
---

# Using Coacus

ENTRY-BODY-MARKER
"""


def make_repo(tmp: Path) -> Path:
    root = tmp / "repo"
    skill = root / "methodology/workflows/using-coacus"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(ENTRY, encoding="utf-8")
    plugin = root / "harnesses/opencode/bootstrap"
    plugin.mkdir(parents=True)
    (plugin / "coacus.js").write_text(
        "const COACUS_ROOT = '__COACUS_ROOT__';\n", encoding="utf-8"
    )
    return root


def add_skill(root: Path, relative: str) -> Path:
    """Create a minimal skill under ``relative`` (e.g. knowledge/skills/security/x)."""
    skill = root / relative
    skill.mkdir(parents=True, exist_ok=True)
    name = skill.name
    (skill / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: test skill\n---\n\n# {name}\n",
        encoding="utf-8",
    )
    return skill


class TestInstaller(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name)
        self.root = make_repo(self.tmp)
        self.config = self.tmp / "config"

    def test_dry_run_writes_nothing(self) -> None:
        result = coacus_install.install("opencode", self.root, self.config, dry_run=True)
        self.assertTrue(result["dry_run"])
        self.assertFalse(self.config.exists())

    def test_opencode_installs_plugin_with_root_substituted(self) -> None:
        coacus_install.install("opencode", self.root, self.config, dry_run=False)
        plugin = self.config / "plugins/coacus.js"
        self.assertTrue(plugin.is_file())
        self.assertIn(self.root.as_posix(), plugin.read_text(encoding="utf-8"))
        self.assertNotIn("__COACUS_ROOT__", plugin.read_text(encoding="utf-8"))

    def test_opencode_installs_skills(self) -> None:
        coacus_install.install("opencode", self.root, self.config, dry_run=False)
        self.assertTrue(
            (self.config / "skills/using-coacus/SKILL.md").is_file()
        )

    def test_manifest_enables_idempotent_uninstall(self) -> None:
        coacus_install.install("opencode", self.root, self.config, dry_run=False)
        manifest = self.config / coacus_install.MANIFEST_NAME
        self.assertTrue(manifest.is_file())
        result = coacus_install.uninstall("opencode", self.config)
        self.assertTrue(result["removed"])
        self.assertFalse((self.config / "plugins/coacus.js").exists())

    def test_antigravity_stages_plugin_without_registry_edit(self) -> None:
        # Antigravity activates by directory placement; no registry edit.
        for name, content in (
            ("plugin.json", '{"name": "coacus-antigravity", "description": "x"}'),
            ("coacus-rule.md", "---\nactivation: always_on\n---\n# bootstrap"),
        ):
            target = self.root / "harnesses/antigravity/bootstrap" / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        coacus_install.install("antigravity", self.root, self.config, dry_run=False)
        plugin = self.config / "config/plugins/coacus"
        self.assertTrue((plugin / "plugin.json").is_file())
        self.assertTrue((plugin / "coacus-rule.md").is_file())
        self.assertFalse((self.config / "config/plugins.json").exists())

    def test_codex_installs_skills_and_hook(self) -> None:
        for name in ("hooks.json", "session-start.sh"):
            target = self.root / "harnesses/codex/bootstrap" / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(
                '{"hooks":{"SessionStart":[{"hooks":[{"command":'
                '"bash \\"__COACUS_ROOT__/x.sh\\""}]}]}}\n'
                if name == "hooks.json"
                else "#!/usr/bin/env bash\necho ok\n",
                encoding="utf-8",
            )
        coacus_install.install("codex", self.root, self.config, dry_run=False)
        # Codex scans $HOME/.agents/skills (config_dir.parent), not ~/.codex/skills.
        self.assertTrue((self.config.parent / ".agents/skills/using-coacus/SKILL.md").is_file())
        self.assertTrue((self.config / "hooks.json").is_file())
        hooks = (self.config / "hooks.json").read_text(encoding="utf-8")
        self.assertNotIn("__COACUS_ROOT__", hooks)
        self.assertIn(self.root.as_posix(), hooks)

    def test_claude_code_stages_hook_plugin_and_skills(self) -> None:
        for name in ("hooks.json", "session-start.sh"):
            target = self.root / "harnesses/claude-code/bootstrap" / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(
                '{"hooks":{"SessionStart":[{"hooks":[{"command":'
                '"\\"${CLAUDE_PLUGIN_ROOT:-.}/bootstrap/session-start.sh\\""}]}]}}\n'
                if name == "hooks.json"
                else "#!/usr/bin/env bash\necho ok\n",
                encoding="utf-8",
            )
        coacus_install.install("claude-code", self.root, self.config, dry_run=False)
        self.assertTrue((self.config / "skills/using-coacus/SKILL.md").is_file())
        plugin = self.config / "plugins/coacus"
        self.assertTrue((plugin / ".claude-plugin/plugin.json").is_file())
        # the script must land where hooks.json resolves it
        self.assertTrue((plugin / "bootstrap/session-start.sh").is_file())
        command = json.loads((plugin / "hooks/hooks.json").read_text())["hooks"][
            "SessionStart"
        ][0]["hooks"][0]["command"]
        resolved = (
            command.replace("${CLAUDE_PLUGIN_ROOT:-.}", plugin.as_posix())
            .strip('"')
        )
        self.assertTrue(Path(resolved).is_file(), resolved)

    def test_skills_install_includes_references(self) -> None:
        reference = self.root / "methodology/workflows/using-coacus/references"
        reference.mkdir(parents=True)
        (reference / "opencode-tools.md").write_text("# map\n", encoding="utf-8")
        coacus_install.install("opencode", self.root, self.config, dry_run=False)
        self.assertTrue(
            (self.config / "skills/using-coacus/references/opencode-tools.md").is_file()
        )

    def test_uninstall_dry_run_removes_nothing(self) -> None:
        coacus_install.install("opencode", self.root, self.config, dry_run=False)
        plugin = self.config / "plugins/coacus.js"
        manifest = self.config / coacus_install.MANIFEST_NAME
        result = coacus_install.uninstall("opencode", self.config, dry_run=True)
        self.assertTrue(result["dry_run"])
        self.assertTrue(plugin.is_file())
        self.assertTrue(manifest.is_file())

    def test_uninstall_rejects_paths_outside_config_dir(self) -> None:
        victim = self.tmp / "victim.txt"
        victim.write_text("do not delete\n", encoding="utf-8")
        self.config.mkdir(parents=True, exist_ok=True)
        (self.config / coacus_install.MANIFEST_NAME).write_text(
            json.dumps({"harness": "opencode", "files": [victim.as_posix()]}),
            encoding="utf-8",
        )
        result = coacus_install.uninstall("opencode", self.config)
        self.assertEqual(result["removed"], [])
        self.assertIn(victim.as_posix(), result["skipped"])
        self.assertTrue(victim.is_file())

    def test_opencode_installs_governor_gate_when_present(self) -> None:
        gate = self.root / "harnesses/opencode/bootstrap/governor-gate.js"
        gate.write_text("const COACUS_ROOT = '__COACUS_ROOT__';\n", encoding="utf-8")
        coacus_install.install("opencode", self.root, self.config, dry_run=False)
        installed = self.config / "plugins/coacus-governor.js"
        self.assertTrue(installed.is_file())
        self.assertNotIn("__COACUS_ROOT__", installed.read_text(encoding="utf-8"))

    def test_malformed_harness_manifest_is_a_clean_error(self) -> None:
        from engine.generators import bootstrap

        broken = self.root / "harnesses/broken/harness.json"
        broken.parent.mkdir(parents=True)
        broken.write_text("{ not json", encoding="utf-8")
        with self.assertRaises(ValueError) as ctx:
            bootstrap.expected_outputs(self.root)
        self.assertIn("invalid harness manifest", str(ctx.exception))


class TestPartialInstall(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name)
        self.root = make_repo(self.tmp)
        self.config = self.tmp / "config"
        add_skill(self.root, "knowledge/skills/security/grc/security-grc-compliance")
        add_skill(self.root, "knowledge/skills/security/appsec/sast-code-review")
        add_skill(self.root, "knowledge/skills/domains/academic/academic-algebra")
        add_skill(self.root, "knowledge/skills/languages/lang-python")
        add_skill(self.root, "knowledge/skills/languages/lang-rust")

    def installed_skills(self) -> set[str]:
        skills_dir = self.config / "skills"
        if not skills_dir.is_dir():
            return set()
        return {p.name for p in skills_dir.iterdir() if (p / "SKILL.md").is_file()}

    def test_discover_skills_unfiltered_returns_everything(self) -> None:
        names = {s.name for s in coacus_install.discover_skills(self.root)}
        self.assertEqual(
            names,
            {
                "using-coacus",
                "security-grc-compliance",
                "sast-code-review",
                "academic-algebra",
                "lang-python",
                "lang-rust",
            },
        )

    def test_only_selects_by_top_level_category(self) -> None:
        names = {
            s.name
            for s in coacus_install.discover_skills(self.root, only=["security"])
        }
        self.assertEqual(names, {"security-grc-compliance", "sast-code-review"})

    def test_only_selects_by_nested_segment(self) -> None:
        names = {
            s.name
            for s in coacus_install.discover_skills(self.root, only=["academic"])
        }
        self.assertEqual(names, {"academic-algebra"})

    def test_only_workflows_selects_the_workflow_collection(self) -> None:
        names = {
            s.name
            for s in coacus_install.discover_skills(self.root, only=["workflows"])
        }
        self.assertEqual(names, {"using-coacus"})

    def test_skills_filter_accepts_globs(self) -> None:
        names = {
            s.name
            for s in coacus_install.discover_skills(self.root, skills=["lang-*"])
        }
        self.assertEqual(names, {"lang-python", "lang-rust"})

    def test_only_and_skills_are_and_ed(self) -> None:
        names = {
            s.name
            for s in coacus_install.discover_skills(
                self.root, only=["languages"], skills=["lang-python"]
            )
        }
        self.assertEqual(names, {"lang-python"})

    def test_partial_install_writes_only_selected_skills(self) -> None:
        coacus_install.install(
            "opencode", self.root, self.config, dry_run=False, only=["security"]
        )
        self.assertEqual(
            self.installed_skills(), {"security-grc-compliance", "sast-code-review"}
        )

    def test_install_carries_third_party_notices(self) -> None:
        (self.root / coacus_install.NOTICE_NAME).write_text(
            "# Third-Party Notices\n\nMIT ...\n", encoding="utf-8"
        )
        coacus_install.install(
            "opencode", self.root, self.config, dry_run=False, skills=["lang-*"]
        )
        notice = self.config / "skills" / coacus_install.NOTICE_NAME
        self.assertTrue(notice.is_file())
        self.assertIn("MIT", notice.read_text(encoding="utf-8"))

    def test_install_without_notice_file_still_works(self) -> None:
        self.assertFalse((self.root / coacus_install.NOTICE_NAME).exists())
        coacus_install.install(
            "opencode", self.root, self.config, dry_run=False, only=["security"]
        )
        self.assertFalse(
            (self.config / "skills" / coacus_install.NOTICE_NAME).exists()
        )

    def test_partial_install_still_stages_the_plugin(self) -> None:
        coacus_install.install(
            "opencode", self.root, self.config, dry_run=False, skills=["lang-python"]
        )
        self.assertTrue((self.config / "plugins/coacus.js").is_file())

    def test_manifest_records_filters(self) -> None:
        coacus_install.install(
            "opencode",
            self.root,
            self.config,
            dry_run=False,
            only=["languages"],
            skills=["lang-*"],
        )
        manifest = json.loads(
            (self.config / coacus_install.MANIFEST_NAME).read_text(encoding="utf-8")
        )
        self.assertEqual(manifest["only"], ["languages"])
        self.assertEqual(manifest["skills"], ["lang-*"])

    def test_partial_uninstall_removes_exactly_what_was_installed(self) -> None:
        coacus_install.install(
            "opencode", self.root, self.config, dry_run=False, only=["languages"]
        )
        result = coacus_install.uninstall("opencode", self.config)
        self.assertTrue(result["removed"])
        self.assertEqual(self.installed_skills(), set())

    def test_list_reports_categories_and_names(self) -> None:
        inventory = coacus_install.list_skills(self.root)
        self.assertIn("security", inventory["categories"])
        self.assertIn("lang-python", inventory["skills"])
        self.assertEqual(inventory["count"], len(inventory["skills"]))

    def test_split_filter_ignores_blanks(self) -> None:
        self.assertEqual(
            coacus_install._split_filter(" security , , engineering "),
            ["security", "engineering"],
        )
        self.assertEqual(coacus_install._split_filter(None), [])
        self.assertEqual(coacus_install._split_filter(""), [])

    def test_main_list_exits_zero_without_a_harness(self) -> None:
        buffer = StringIO()
        with redirect_stdout(buffer):
            self.assertEqual(coacus_install.main(["--list"]), 0)
        self.assertIn("categories", buffer.getvalue())

    def test_main_requires_a_harness_without_list(self) -> None:
        with self.assertRaises(SystemExit):
            coacus_install.main([])

    def test_main_dry_run_honors_only(self) -> None:
        buffer = StringIO()
        with redirect_stdout(buffer):
            code = coacus_install.main(
                [
                    "opencode",
                    "--config-dir",
                    self.config.as_posix(),
                    "--dry-run",
                    "--only",
                    "security",
                ]
            )
        self.assertEqual(code, 0)
        self.assertFalse(self.config.exists())
        self.assertIn("security-grc-compliance", buffer.getvalue())


if __name__ == "__main__":
    unittest.main()
