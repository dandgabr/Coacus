"""Every hook that runs a Coacus script runs it with python -I."""

from __future__ import annotations

import base64
import json
import re
import shlex
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import coacus_install

REPO = Path(__file__).resolve().parents[1]


def hook_templates() -> list[Path]:
    paths = sorted(REPO.glob("harnesses/*/bootstrap/*hooks*.json"))
    return [p for p in paths if "__COACUS_PYTHON__" in p.read_text(encoding="utf-8")]


class TestInstalledCommands(unittest.TestCase):
    def test_there_are_templates_to_check(self) -> None:
        self.assertGreaterEqual(len(hook_templates()), 6)

    def test_every_rendered_python_command_is_isolated(self) -> None:
        for path in hook_templates():
            rendered = coacus_install._hook_substitute(
                path.read_text(encoding="utf-8"), REPO, REPO / "plugin", sys.executable)
            commands = []

            def walk(value, key=""):
                if isinstance(value, dict):
                    for k, v in value.items():
                        walk(v, k)
                elif isinstance(value, list):
                    for item in value:
                        walk(item)
                elif isinstance(value, str) and key == "command":
                    commands.append(value)

            walk(json.loads(rendered))
            self.assertTrue(commands, path.name)
            for command in commands:
                with self.subTest(template=str(path.relative_to(REPO)), command=command[:60]):
                    self.assertEqual(shlex.split(command)[1], "-I")

    def test_the_opencode_plugins_pass_the_flag(self) -> None:
        for name in ("coacus-guardrails.js", "governor-gate.js"):
            text = (REPO / "harnesses/opencode/bootstrap" / name).read_text(encoding="utf-8")
            with self.subTest(plugin=name):
                self.assertRegex(text, r"\[\s*'-I', (GUARD|GOVERNOR)")

    def test_a_command_that_already_has_a_flag_is_left_alone(self) -> None:
        rendered = coacus_install._hook_substitute(
            json.dumps({"command": '__COACUS_PYTHON__ -S "__COACUS_ROOT__/scripts/x.py"'}), REPO, None, sys.executable)
        self.assertNotIn("-I", shlex.split(json.loads(rendered)["command"]))


class TestRunsIsolated(unittest.TestCase):
    def test_the_session_start_hook_ignores_a_module_planted_in_the_working_directory(self) -> None:
        template = (REPO / "harnesses/claude-code/bootstrap/hooks.json").read_text(encoding="utf-8")
        rendered = json.loads(coacus_install._hook_substitute(template, REPO, REPO / "harnesses/claude-code", sys.executable))
        command = rendered["hooks"]["SessionStart"][0]["hooks"][0]["command"]
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "json.py").write_text("raise SystemExit('PLANTED')\n", encoding="utf-8")
            result = subprocess.run(shlex.split(command), capture_output=True, text=True, cwd=tmp, timeout=60)
        self.assertNotIn("PLANTED", result.stdout + result.stderr)
        self.assertEqual(result.returncode, 0)
        json.loads(result.stdout)

    def test_the_guard_ignores_a_planted_module_too(self) -> None:
        template = (REPO / "harnesses/claude-code/bootstrap/guardrail-hooks.json").read_text(encoding="utf-8")
        rendered = json.loads(coacus_install._hook_substitute(template, REPO, None, sys.executable))
        command = rendered["hooks"]["PreToolUse"][0]["hooks"][0]["command"]
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "json.py").write_text("raise SystemExit('PLANTED')\n", encoding="utf-8")
            result = subprocess.run(shlex.split(command), input="{}", capture_output=True, text=True, cwd=tmp, timeout=60)
        self.assertNotIn("PLANTED", result.stdout + result.stderr)
        json.loads(result.stdout)


class TestOwnershipAndWindows(unittest.TestCase):
    MARKER = f"{REPO.as_posix()}/scripts/coacus_guard.py"

    def test_an_isolated_entry_and_an_old_plain_one_are_both_ours(self) -> None:
        isolated = coacus_install._command([sys.executable, "-I", self.MARKER, "--event", "tool.pre"])
        plain = shlex.join([sys.executable, self.MARKER, "--event", "tool.pre"])
        for command in (isolated, plain):
            with self.subTest(command=command[:40]):
                self.assertTrue(coacus_install._entry_owned({"hooks": [{"type": "command", "command": command}]}, {self.MARKER}))

    def test_a_reinstall_replaces_an_old_plain_entry_with_the_isolated_one(self) -> None:
        old = shlex.join([sys.executable, self.MARKER, "--event", "tool.pre"])
        new = coacus_install._command([sys.executable, "-I", self.MARKER, "--event", "tool.pre"])
        existing = {"hooks": {"PreToolUse": [{"hooks": [{"type": "command", "command": old}]}]}}
        fragment = {"hooks": {"PreToolUse": [{"hooks": [{"type": "command", "command": new}]}]}}
        merged = coacus_install._merge_hooks(existing, fragment, {self.MARKER})
        self.assertEqual([e["hooks"][0]["command"] for e in merged["hooks"]["PreToolUse"]], [new])

    def test_the_windows_form_isolates_and_keeps_the_script_first(self) -> None:
        with mock.patch.object(coacus_install.os, "name", "nt"):
            command = coacus_install._command(["C:/Python/python.exe", "-I", "C:/repo/scripts/coacus_guard.py", "--event", "tool.pre"])
        self.assertTrue(command.startswith('"C:/Python/python.exe" -I -c '))
        encoded = re.search(r"b64decode\('([^']+)'\)", command).group(1)
        self.assertEqual(json.loads(base64.b64decode(encoded))[0], "C:/repo/scripts/coacus_guard.py")
        self.assertTrue(coacus_install._entry_owned({"hooks": [{"type": "command", "command": command}]},
                                                    {"C:/repo/scripts/coacus_guard.py"}))

    def test_the_windows_form_without_the_marker_keeps_its_old_shape(self) -> None:
        with mock.patch.object(coacus_install.os, "name", "nt"):
            command = coacus_install._command(["C:/Python/python.exe", "C:/repo/scripts/x.py"])
        self.assertTrue(command.startswith('"C:/Python/python.exe" -c '))


if __name__ == "__main__":
    unittest.main()
