"""Tests for the Coacus installer (scripts/coacus_install.py)."""

from __future__ import annotations

import json
import tempfile
import unittest
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


if __name__ == "__main__":
    unittest.main()
