"""--verify reports an installed Coacus hook whose script is no longer on disk."""

from __future__ import annotations

import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import coacus_install

REPO = Path(__file__).resolve().parents[1]


class TestMissingHookScripts(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.base = Path(self._tmp.name)
        self.root = self.base / "checkout"
        self.guard = self.root / "scripts" / "coacus_guard.py"
        self.settings = self.base / "settings.json"

    def write(self, *commands: str, key: str = "hooks") -> None:
        entries = [{"hooks": [{"type": "command", "command": c}]} for c in commands]
        self.settings.write_text(json.dumps({key: {"PreToolUse": entries}}), encoding="utf-8")

    def missing(self) -> list[str]:
        return coacus_install._missing_hook_scripts(self.root, "claude-code", [self.settings])

    def command(self, *extra: str) -> str:
        return coacus_install._command([sys.executable, "-I", self.guard.as_posix(), *extra])

    def test_a_removed_checkout_is_reported(self) -> None:
        self.write(self.command("--event", "tool.pre"))
        self.assertEqual(self.missing(), [self.guard.as_posix()])

    def test_a_present_script_is_not_reported(self) -> None:
        self.guard.parent.mkdir(parents=True)
        self.guard.write_text("", encoding="utf-8")
        self.write(self.command("--event", "tool.pre"))
        self.assertEqual(self.missing(), [])

    def test_the_forms_an_install_can_write_are_all_read(self) -> None:
        plain = f"{sys.executable} {self.guard.as_posix()} --event tool.pre"
        optional = coacus_install._command([sys.executable, "@optional", self.guard.as_posix(), "--event", "prompt.submit"])
        with mock.patch.object(coacus_install.os, "name", "nt"):
            windows = coacus_install._command([sys.executable, self.guard.as_posix(), "--event", "tool.pre"])
            windows_optional = coacus_install._command([sys.executable, "@optional", self.guard.as_posix()])
        for form in (plain, self.command(), optional, windows, windows_optional):
            with self.subTest(form=form[:50]):
                self.write(form)
                self.assertEqual(self.missing(), [self.guard.as_posix()])

    def test_a_foreign_hook_with_a_missing_script_is_not_ours_to_report(self) -> None:
        self.write(f"{sys.executable} /opt/other/tool.py", "echo hello")
        self.assertEqual(self.missing(), [])

    def test_nested_entries_and_a_plugin_hooks_file_are_found(self) -> None:
        self.settings.write_text(json.dumps({"a": [{"b": {"hooks": [{"command": self.command()}]}}]}), encoding="utf-8")
        self.assertEqual(self.missing(), [self.guard.as_posix()])

    def test_unreadable_and_non_json_targets_are_skipped(self) -> None:
        bad = self.base / "bad.json"
        bad.write_text("{not json", encoding="utf-8")
        text = self.base / "notes.txt"
        text.write_text(self.command(), encoding="utf-8")
        gone = self.base / "gone.json"
        self.assertEqual(coacus_install._missing_hook_scripts(self.root, "claude-code", [bad, text, gone]), [])

    def test_malformed_commands_never_raise(self) -> None:
        for value in (None, 5, "", "'unbalanced", "python -c", ["x"]):
            self.settings.write_text(json.dumps({"hooks": [{"command": value}]}), encoding="utf-8")
            with self.subTest(value=value):
                self.assertEqual(self.missing(), [])


class TestVerifyReport(unittest.TestCase):
    def test_verify_fails_and_names_the_script(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config, home = Path(tmp) / "cfg", Path(tmp) / "home"
            home.mkdir()
            env = {k: v for k, v in os.environ.items() if k not in ("CI", "COACUS_GUARD_ASK")}
            env["COACUS_POLICY_DIR"] = str(Path(tmp) / "policies")
            argv = ["claude-code", "--config-dir", str(config), "--skills", "using-coacus", "--agents", "general",
                    "--browser-policy", "off", "--self-protection", "off", "--skills-mode", "copy", "--force", "--yes"]
            with mock.patch.dict(os.environ, env, clear=True), mock.patch.object(coacus_install, "_home", return_value=home), \
                    contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(coacus_install.main(argv, REPO), 0)
                with contextlib.redirect_stdout(io.StringIO()) as out:
                    clean = coacus_install.main(["claude-code", "--config-dir", str(config), "--verify"], REPO)
                self.assertEqual(clean, 0)
                self.assertEqual(json.loads(out.getvalue())[0]["hook_scripts_missing"], [])
                with mock.patch.object(coacus_install, "_missing_hook_scripts", return_value=["/gone/coacus_guard.py"]), \
                        contextlib.redirect_stdout(io.StringIO()) as out:
                    broken = coacus_install.main(["claude-code", "--config-dir", str(config), "--verify"], REPO)
        report = json.loads(out.getvalue())[0]
        self.assertEqual(broken, 1)
        self.assertFalse(report["ok"])
        self.assertEqual(report["hook_scripts_missing"], ["/gone/coacus_guard.py"])


if __name__ == "__main__":
    unittest.main()
