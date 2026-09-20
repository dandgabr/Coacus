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
    for harness in ("claude-code", "codex", "cursor"):
        base = root / f"harnesses/{harness}/bootstrap"
        base.mkdir(parents=True)
        (base / "session-start.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (base / "hooks.json").write_text(
            '{"command": "__COACUS_ROOT__/x"}\n', encoding="utf-8"
        )
    anti = root / "harnesses/antigravity/bootstrap"
    anti.mkdir(parents=True)
    (anti / "plugin.json").write_text("{}\n", encoding="utf-8")
    (anti / "coacus-rule.md").write_text("# rule\n", encoding="utf-8")
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


def add_agent(root: Path, relative: str) -> Path:
    """Create a minimal agent under ``relative`` (e.g. knowledge/agents/x/name)."""
    agent = root / relative
    agent.mkdir(parents=True, exist_ok=True)
    name = agent.name
    (agent / coacus_install.AGENT_SOURCE_NAME).write_text(
        f"---\nname: {name}\ndescription: test agent\n---\n\n# {name}\n",
        encoding="utf-8",
    )
    return agent


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
        result = coacus_install.uninstall("opencode", self.root, self.config)
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
        result = coacus_install.uninstall("opencode", self.root, self.config, dry_run=True)
        self.assertTrue(result["dry_run"])
        self.assertTrue(plugin.is_file())
        self.assertTrue(manifest.is_file())

    def test_uninstall_rejects_paths_outside_the_plan(self) -> None:
        victim = self.tmp / "victim.txt"
        victim.write_text("do not delete\n", encoding="utf-8")
        self.config.mkdir(parents=True, exist_ok=True)
        (self.config / coacus_install.MANIFEST_NAME).write_text(
            json.dumps({"harness": "opencode", "files": [victim.as_posix()]}),
            encoding="utf-8",
        )
        result = coacus_install.uninstall("opencode", self.root, self.config)
        self.assertEqual(result["removed"], [])
        self.assertIn(victim.as_posix(), result["skipped"])
        self.assertTrue(victim.is_file())

    def test_uninstall_removes_skills_stored_outside_config_dir(self) -> None:
        # Codex and Cursor write skills to <home>/.agents/skills, outside their
        # config dir. They must still be removed on uninstall.
        home = self.tmp / "home"
        config = home / ".codex"
        coacus_install.install("codex", self.root, config, dry_run=False)
        skills = home / ".agents" / "skills"
        self.assertTrue(any(skills.glob("*/SKILL.md")))
        result = coacus_install.uninstall("codex", self.root, config)
        self.assertEqual(result["skipped"], [])
        self.assertTrue(result["removed"])
        self.assertFalse(any(skills.glob("*/SKILL.md")))

    def test_uninstall_removes_orphan_when_source_was_deleted(self) -> None:
        import shutil

        coacus_install.install("opencode", self.root, self.config, dry_run=False)
        shutil.rmtree(self.root / "methodology/workflows/using-coacus")
        result = coacus_install.uninstall("opencode", self.root, self.config)
        self.assertEqual(result["skipped"], [])
        self.assertFalse(
            (self.config / "skills/using-coacus/SKILL.md").exists()
        )

    def test_uninstall_preserves_files_another_harness_claims(self) -> None:
        # Codex and Cursor share <home>/.agents/skills; uninstalling one must
        # not delete files the other still needs.
        root = make_repo(self.tmp / "shared")
        home = self.tmp / "home2"
        for harness in ("codex", "cursor"):
            base = root / f"harnesses/{harness}/bootstrap"
            base.mkdir(parents=True, exist_ok=True)
            (base / "session-start.sh").write_text("#!/bin/sh\n", encoding="utf-8")
            (base / "hooks.json").write_text(
                '{"command": "__COACUS_ROOT__/x"}', encoding="utf-8"
            )
        coacus_install.install("codex", root, home / ".codex", dry_run=False)
        coacus_install.install("cursor", root, home / ".cursor", dry_run=False)
        coacus_install.uninstall("codex", root, home / ".codex")
        self.assertTrue(
            (home / ".agents/skills/using-coacus/SKILL.md").is_file()
        )
        self.assertTrue(coacus_install.verify("cursor", root, home / ".cursor")["ok"])

    def test_agent_name_traversal_is_refused(self) -> None:
        evil = self.root / "knowledge/agents/roles/evil"
        evil.mkdir(parents=True)
        (evil / "agent.source.md").write_text(
            "---\nname: ../../../../escaped\ndescription: x\n---\n\nbody\n",
            encoding="utf-8",
        )
        with self.assertRaises(ValueError) as ctx:
            coacus_install.install("opencode", self.root, self.config, dry_run=False)
        self.assertIn("kebab-case", str(ctx.exception))

    def test_symlinks_in_a_skill_are_not_followed(self) -> None:
        skill = self.root / "knowledge/skills/roles/leaky"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text(
            "---\nname: leaky\ndescription: x\n---\n\nbody\n", encoding="utf-8"
        )
        secret = self.tmp / "secret.txt"
        secret.write_text("top secret", encoding="utf-8")
        (skill / "link.txt").symlink_to(secret)
        coacus_install.install("opencode", self.root, self.config, dry_run=False)
        self.assertFalse((self.config / "skills/leaky/link.txt").exists())

    def test_binary_skill_companion_installs_and_verifies(self) -> None:
        skill = self.root / "knowledge/skills/roles/with-image"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text(
            "---\nname: with-image\ndescription: x\n---\n\nbody\n", encoding="utf-8"
        )
        (skill / "logo.png").write_bytes(b"\x89PNG\x00\xff")
        coacus_install.install("opencode", self.root, self.config, dry_run=False)
        self.assertEqual(
            (self.config / "skills/with-image/logo.png").read_bytes(),
            b"\x89PNG\x00\xff",
        )
        self.assertTrue(coacus_install.verify("opencode", self.root, self.config)["ok"])

    def test_malformed_install_manifest_is_a_clean_error(self) -> None:
        self.config.mkdir(parents=True, exist_ok=True)
        (self.config / coacus_install.MANIFEST_NAME).write_text(
            "{ not json", encoding="utf-8"
        )
        self.assertIn(
            "unreadable install manifest",
            str(coacus_install.verify("opencode", self.root, self.config)["error"]),
        )
        self.assertIn(
            "unreadable install manifest",
            str(coacus_install.uninstall("opencode", self.root, self.config)["error"]),
        )

    def test_hooks_json_survives_a_quote_in_the_repo_path(self) -> None:
        # A naive str.replace would corrupt the JSON when the root has a quote.
        root = make_repo(self.tmp / 'we"ird')
        config = self.tmp / "qcfg"
        coacus_install.install("codex", root, config, dry_run=False)
        json.loads((config / "hooks.json").read_text(encoding="utf-8"))

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
        result = coacus_install.uninstall("opencode", self.root, self.config)
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


class TestVerify(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name)
        self.root = make_repo(self.tmp)
        self.config = self.tmp / "config"
        add_skill(self.root, "knowledge/skills/security/grc/security-grc-compliance")
        add_skill(self.root, "knowledge/skills/languages/lang-python")
        add_skill(self.root, "knowledge/skills/languages/lang-rust")

    def test_verify_reports_not_installed(self) -> None:
        report = coacus_install.verify("opencode", self.root, self.config)
        self.assertFalse(report["installed"])
        self.assertFalse(report["ok"])
        self.assertIn("error", report)

    def test_verify_ok_after_install(self) -> None:
        coacus_install.install("opencode", self.root, self.config, dry_run=False)
        report = coacus_install.verify("opencode", self.root, self.config)
        self.assertTrue(report["installed"])
        self.assertTrue(report["ok"])
        self.assertEqual(report["counts"]["skills"], 4)
        self.assertEqual(report["missing"], [])
        self.assertEqual(report["drifted"], [])
        self.assertEqual(report["planned_files"], report["recorded_files"])

    def test_verify_counts_are_canonical_not_inferred(self) -> None:
        coacus_install.install("opencode", self.root, self.config, dry_run=False)
        report = coacus_install.verify("opencode", self.root, self.config)
        # 4 skills (using-coacus + 3) and no agents in this minimal repo.
        self.assertEqual(report["counts"]["skills"], 4)
        self.assertEqual(report["counts"]["agents"], 0)
        self.assertEqual(
            report["counts"]["skills"]
            + report["counts"]["agents"]
            + report["counts"]["hook_files"]
            + report["counts"]["other_files"],
            report["planned_files"],
        )

    def test_verify_detects_drift(self) -> None:
        coacus_install.install("opencode", self.root, self.config, dry_run=False)
        target = self.config / "skills/lang-python/SKILL.md"
        target.write_text("tampered\n", encoding="utf-8")
        report = coacus_install.verify("opencode", self.root, self.config)
        self.assertFalse(report["ok"])
        self.assertEqual(report["drifted"], [target.as_posix()])

    def test_verify_detects_missing_file(self) -> None:
        coacus_install.install("opencode", self.root, self.config, dry_run=False)
        target = self.config / "skills/lang-rust/SKILL.md"
        target.unlink()
        report = coacus_install.verify("opencode", self.root, self.config)
        self.assertFalse(report["ok"])
        self.assertEqual(report["missing"], [target.as_posix()])

    def test_verify_honors_manifest_filters(self) -> None:
        coacus_install.install(
            "opencode",
            self.root,
            self.config,
            dry_run=False,
            only=["languages"],
        )
        report = coacus_install.verify("opencode", self.root, self.config)
        self.assertTrue(report["ok"])
        self.assertEqual(report["only"], ["languages"])
        # only the two language skills, not the security one.
        self.assertEqual(report["counts"]["skills"], 2)

    def test_verify_is_read_only(self) -> None:
        coacus_install.install("opencode", self.root, self.config, dry_run=False)
        before = sorted(
            p.as_posix()
            for p in self.config.rglob("*")
            if p.is_file()
        )
        coacus_install.verify("opencode", self.root, self.config)
        after = sorted(
            p.as_posix() for p in self.config.rglob("*") if p.is_file()
        )
        self.assertEqual(before, after)

    def test_main_verify_exit_zero_when_ok(self) -> None:
        coacus_install.install("opencode", self.root, self.config, dry_run=False)
        buffer = StringIO()
        with redirect_stdout(buffer):
            code = coacus_install.main(
                ["opencode", "--verify", "--config-dir", self.config.as_posix()],
                root=self.root,
            )
        self.assertEqual(code, 0)
        self.assertIn('"ok": true', buffer.getvalue())

    def test_unknown_only_token_is_rejected(self) -> None:
        import contextlib

        with self.assertRaises(SystemExit), contextlib.redirect_stderr(StringIO()):
            coacus_install.main(
                ["opencode", "--only", "doesnotexist", "--dry-run"], root=self.root
            )

    def test_main_verify_exit_one_on_drift(self) -> None:
        coacus_install.install("opencode", self.root, self.config, dry_run=False)
        (self.config / "skills/lang-python/SKILL.md").write_text(
            "tampered\n", encoding="utf-8"
        )
        buffer = StringIO()
        with redirect_stdout(buffer):
            code = coacus_install.main(
                ["opencode", "--verify", "--config-dir", self.config.as_posix()],
                root=self.root,
            )
        self.assertEqual(code, 1)
        self.assertIn('"ok": false', buffer.getvalue())

    def test_component_counts_classifies_paths(self) -> None:
        files = [
            (Path("/c/skills/lang-python/SKILL.md"), ""),
            (Path("/c/agent/backend-developer.md"), ""),
            (Path("/c/agents/toml-agent.toml"), ""),
            (Path("/c/plugins/coacus/agents/antigravity-agent/agent.md"), ""),
            (Path("/c/plugins/coacus/governor-hook.sh"), ""),
            (Path("/c/plugins/coacus/hooks.json"), ""),
        ]
        counts = coacus_install._component_counts(files)
        self.assertEqual(counts["skills"], 1)
        self.assertEqual(counts["agents"], 3)
        self.assertEqual(counts["hook_files"], 2)
        self.assertEqual(counts["other_files"], 0)

    def test_component_counts_distinguish_flat_agents(self) -> None:
        files = [
            (Path("/c/agents/backend-developer.md"), ""),
            (Path("/c/agents/qa-testing-specialist.md"), ""),
            (Path("/c/agent/task.md"), ""),
        ]
        counts = coacus_install._component_counts(files)
        self.assertEqual(counts["agents"], 3)


class TestAgentFiltering(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name)
        self.root = make_repo(self.tmp)
        self.config = self.tmp / "config"
        add_agent(self.root, "knowledge/agents/cybersecurity/pentester-agent")
        add_agent(self.root, "knowledge/agents/cybersecurity/security-architect")
        add_agent(self.root, "knowledge/agents/core-orchestration/general")
        add_agent(self.root, "knowledge/agents/software-engineering/backend-developer")

    def installed_agents(self, config: Path | None = None) -> set[str]:
        agents_dir = (config or self.config) / "agent"
        if not agents_dir.is_dir():
            return set()
        return {p.stem for p in agents_dir.glob("*.md")}

    def test_discover_agents_unfiltered_returns_everything(self) -> None:
        names = {a.parent.name for a in coacus_install.discover_agents(self.root)}
        self.assertEqual(
            names,
            {"pentester-agent", "security-architect", "general", "backend-developer"},
        )

    def test_only_selects_agents_by_category(self) -> None:
        names = {
            a.parent.name
            for a in coacus_install.discover_agents(self.root, only=["cybersecurity"])
        }
        self.assertEqual(names, {"pentester-agent", "security-architect"})

    def test_agents_filter_accepts_globs(self) -> None:
        names = {
            a.parent.name
            for a in coacus_install.discover_agents(self.root, agents=["*-architect"])
        }
        self.assertEqual(names, {"security-architect"})

    def test_only_token_matches_whole_segment_not_substring(self) -> None:
        names = {
            a.parent.name
            for a in coacus_install.discover_agents(self.root, only=["security"])
        }
        self.assertEqual(names, set())

    def test_skills_filter_never_narrows_agents(self) -> None:
        coacus_install.install(
            "opencode", self.root, self.config, dry_run=False, skills=["lang-*"]
        )
        self.assertEqual(len(self.installed_agents()), 4)

    def test_partial_install_filters_agents_by_category(self) -> None:
        coacus_install.install(
            "opencode", self.root, self.config, dry_run=False, only=["cybersecurity"]
        )
        self.assertEqual(
            self.installed_agents(), {"pentester-agent", "security-architect"}
        )

    def test_agents_glob_keeps_skills_intact(self) -> None:
        coacus_install.install(
            "opencode", self.root, self.config, dry_run=False, agents=["*-architect"]
        )
        self.assertEqual(self.installed_agents(), {"security-architect"})
        self.assertTrue((self.config / "skills/using-coacus/SKILL.md").is_file())

    def test_manifest_records_agents_filter(self) -> None:
        coacus_install.install(
            "opencode", self.root, self.config, dry_run=False, agents=["pentester-*"]
        )
        manifest = json.loads(
            (self.config / coacus_install.MANIFEST_NAME).read_text(encoding="utf-8")
        )
        self.assertEqual(manifest["agents"], ["pentester-*"])

    def test_all_harnesses_install_agents(self) -> None:
        for harness in ("opencode", "claude-code", "antigravity", "codex", "cursor"):
            config = self.tmp / f"cfg-{harness}"
            coacus_install.install(harness, self.root, config, dry_run=False)
            found = [
                p
                for p in config.rglob("*")
                if p.is_file()
                and (
                    p.stem == "pentester-agent"
                    or (p.name == "agent.md" and p.parent.name == "pentester-agent")
                )
            ]
            self.assertTrue(found, f"{harness} installed no agent files")


if __name__ == "__main__":
    unittest.main()
