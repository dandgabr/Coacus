"""The opt-in policy that stops the agent's write tools from editing the guard."""

from __future__ import annotations

import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from engine.guardrail import evaluate as guard
from engine.guardrail import selfprotect
from scripts import coacus_install

REPO = Path(__file__).resolve().parents[1]
GUARD_CLI = REPO / "scripts/coacus_guard.py"
SHIPPED = REPO / selfprotect.SOURCE

PROTECTED = [
    "/home/u/.config/coacus/policies/browser.policy.json", "/home/u/.config/coacus/policies/x.policy.json",
    "/home/u/Code/Coacus/methodology/lifecycle/policies/default.policy.json",
    "/home/u/Code/Coacus/scripts/coacus_guard.py", "scripts/coacus_guard.py",
    "/home/u/Code/Coacus/engine/guardrail/evaluate.py", "engine/guardrail/selfprotect.py",
    "/home/u/.claude/settings.json", ".claude/settings.json", "/proj/.claude/settings.local.json",
    "/home/u/.codex/hooks.json", "/home/u/.codex/config.toml",
    "/home/u/.config/opencode/plugins/coacus-guardrails.js", "/proj/.opencode/plugins/x.js",
    "/home/u/.cursor/hooks.json", "/home/u/.gemini/config/plugins/coacus/hooks.json",
    "/stage/coacus-policies/self-protection.policy.json",
]
UNPROTECTED = [
    "README.md", "/home/u/proj/src/app.py", "/home/u/.claude/CLAUDE.md", "/home/u/.claude/settings.json.bak",
    "/home/u/.codex/AGENTS.md", "/home/u/Code/Coacus/docs/usage.md", "/home/u/Code/Coacus/tests/test_x.py",
    "/home/u/.config/other/policies/a.json", "scripts/other_tool.py",
]


def shipped() -> dict:
    return json.loads(SHIPPED.read_text(encoding="utf-8"))


def enabled() -> list[dict]:
    return selfprotect.build_policy(REPO, Path("/stage/coacus-policies"))["policies"]


class TestShippedPolicy(unittest.TestCase):
    def test_it_ships_disabled_and_only_denies_writes(self) -> None:
        data = shipped()
        self.assertIs(data["enabled"], False)
        ids = [p["id"] for p in data["policies"]]
        self.assertEqual(len(ids), len(set(ids)))
        for policy in data["policies"]:
            with self.subTest(policy=policy["id"]):
                self.assertEqual(policy["action"]["verb"], "write")
                self.assertEqual(policy["decision"], "deny")
                self.assertEqual(policy["on_ask_unavailable"], "deny")
                self.assertIn("legitimate", policy["message"])
                self.assertIn("own terminal", policy["message"])

    def test_the_disabled_file_is_never_loaded(self) -> None:
        self.assertNotIn("guard-script", [p["id"] for p in guard.load_policies(REPO)])

    def test_the_release_text_is_in_the_message_and_the_constant(self) -> None:
        self.assertIn("never the agent", selfprotect.RELEASE_HOW)
        self.assertIn('"enabled": false', selfprotect.RELEASE_HOW)


class TestCoverage(unittest.TestCase):
    def test_every_protected_path_is_denied_and_the_rest_allowed(self) -> None:
        policies = enabled()
        for path in PROTECTED:
            with self.subTest(path=path):
                self.assertEqual(guard.evaluate(policies, "write", path)["decision"], "deny")
        for path in UNPROTECTED:
            with self.subTest(path=path):
                self.assertEqual(guard.evaluate(policies, "write", path)["decision"], "allow")

    def test_reading_a_protected_file_is_not_blocked(self) -> None:
        self.assertEqual(guard.evaluate(enabled(), "read", "/home/u/.claude/settings.json")["decision"], "allow")

    def test_the_policy_directory_in_use_is_covered_even_when_custom(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            custom = Path(tmp) / "my-rules"
            document = selfprotect.build_policy(REPO, custom)
            self.assertEqual(guard.evaluate(document["policies"], "write", str(custom / "a.policy.json"))["decision"],
                             "deny")
            again = selfprotect.build_policy(REPO, custom)
            self.assertEqual(len(again["policies"]), len(document["policies"]))

    def test_build_marks_the_copy_as_generated_and_enabled(self) -> None:
        document = selfprotect.build_policy(REPO, Path("/x/policies"))
        self.assertIs(document["enabled"], True)
        self.assertEqual(document["generated"]["by"], selfprotect.GENERATED_BY)
        self.assertIs(shipped()["enabled"], False)


class TestEndToEnd(unittest.TestCase):
    def test_the_guard_denies_a_write_tool_with_the_release_message(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp) / "policies"
            selfprotect.write_policy(directory, selfprotect.build_policy(REPO, directory))
            env = {k: v for k, v in os.environ.items() if k not in ("CI", "COACUS_GUARD_ASK", "COACUS_GUARD_NO_ASK")}
            env["COACUS_POLICY_DIR"] = str(directory)

            def run(tool: str, path: str) -> dict:
                proc = subprocess.run(
                    [sys.executable, str(GUARD_CLI), "--harness", "claude-code", "--event", "tool.pre", "--root", str(REPO)],
                    input=json.dumps({"tool": tool, "tool_input": {"file_path": path}}),
                    capture_output=True, text=True, env=env, timeout=60)
                return json.loads(proc.stdout.strip())

            denied = run("Write", "/home/u/.claude/settings.json")
            self.assertEqual(denied["hookSpecificOutput"]["permissionDecision"], "deny")
            self.assertIn("own terminal", denied["hookSpecificOutput"]["permissionDecisionReason"])
            self.assertEqual(run("Edit", str(directory / "x.policy.json"))["hookSpecificOutput"]["permissionDecision"], "deny")
            self.assertEqual(run("Write", "/home/u/proj/app.py"), {})
            self.assertEqual(run("Read", "/home/u/.claude/settings.json"), {})


class TestStatusAndRemoval(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.dir = Path(self._tmp.name)

    def test_status(self) -> None:
        self.assertEqual(selfprotect.status(self.dir), "absent")
        document = selfprotect.build_policy(REPO, self.dir)
        selfprotect.write_policy(self.dir, document)
        self.assertEqual(selfprotect.status(self.dir), "active")
        document["enabled"] = False
        selfprotect.write_policy(self.dir, document)
        self.assertEqual(selfprotect.status(self.dir), "disabled")
        (self.dir / selfprotect.POLICY_FILE).write_text("{bad", encoding="utf-8")
        self.assertEqual(selfprotect.status(self.dir), "absent")

    def test_remove_deletes_only_a_generated_file(self) -> None:
        selfprotect.write_policy(self.dir, selfprotect.build_policy(REPO, self.dir))
        self.assertTrue(selfprotect.remove_policy(self.dir))
        self.assertFalse((self.dir / selfprotect.POLICY_FILE).exists())
        (self.dir / selfprotect.POLICY_FILE).write_text(json.dumps({"enabled": True, "policies": []}), encoding="utf-8")
        self.assertFalse(selfprotect.remove_policy(self.dir))
        self.assertTrue((self.dir / selfprotect.POLICY_FILE).exists())
        self.assertFalse(selfprotect.remove_policy(self.dir / "missing"))


class TestInstallerStep(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.dir = Path(self._tmp.name) / "policies"

    def step(self, mode: str, answer: str = "", dry_run: bool = False) -> dict:
        said: list[str] = []
        result = coacus_install.self_protection_step(
            REPO, mode, self.dir, dry_run=dry_run, ask=lambda _p: answer, say=said.append)
        result["said"] = said
        return result

    def test_off_does_nothing(self) -> None:
        self.assertEqual(self.step("off")["status"], "off")
        self.assertFalse(self.dir.exists())

    def test_on_writes_an_active_policy(self) -> None:
        result = self.step("on")
        self.assertEqual(result["status"], "written")
        self.assertEqual(selfprotect.status(self.dir), "active")

    def test_dry_run_writes_nothing(self) -> None:
        self.assertEqual(self.step("on", dry_run=True)["status"], "dry-run")
        self.assertFalse(self.dir.exists())

    def test_prompt_explains_the_release_and_needs_a_yes(self) -> None:
        for answer in ("", "n", "maybe", "\n"):
            with self.subTest(answer=answer):
                result = self.step("prompt", answer)
                self.assertEqual(result["status"], "skipped")
                self.assertFalse(self.dir.exists())
        result = self.step("prompt", " YES ")
        self.assertEqual(result["status"], "written")
        self.assertIn("never the agent", result["said"][0])

    def test_eof_and_interrupt_count_as_no(self) -> None:
        for exc in (EOFError, KeyboardInterrupt):
            with self.subTest(exc=exc.__name__):
                def ask(_p, exc=exc):
                    raise exc
                result = coacus_install.self_protection_step(REPO, "prompt", self.dir, ask=ask, say=lambda _m: None)
                self.assertEqual(result["status"], "skipped")


class TestInstallerFlow(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        base = Path(self._tmp.name)
        self.config = base / "cfg"
        self.config.mkdir()
        self.env = {k: v for k, v in os.environ.items() if k not in ("CI", "COACUS_GUARD_ASK")}
        self.env["COACUS_POLICY_DIR"] = str(base / "policies")
        self.policy_dir = self.config / "coacus-policies"

    def run_main(self, *extra: str) -> tuple[int, list]:
        argv = ["codex", "--config-dir", str(self.config), "--skills", "using-coacus", "--agents", "general",
                "--browser-policy", "off", "--skills-mode", "copy", "--force", *extra]
        out = io.StringIO()
        with mock.patch.dict(os.environ, self.env, clear=True), \
                mock.patch.object(coacus_install, "_home", return_value=Path(self._tmp.name) / "home"), \
                contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            code = coacus_install.main(argv, REPO)
        return code, json.loads(out.getvalue())

    def test_the_default_without_a_terminal_installs_nothing(self) -> None:
        code, report = self.run_main()
        self.assertEqual(code, 0)
        self.assertEqual(report[0]["self_protection"]["status"], "off")
        self.assertFalse((self.policy_dir / selfprotect.POLICY_FILE).exists())

    def test_on_installs_the_policy_and_verify_reports_it(self) -> None:
        code, report = self.run_main("--self-protection", "on")
        self.assertEqual(code, 0)
        self.assertEqual(report[0]["self_protection"]["status"], "written")
        self.assertEqual(selfprotect.status(self.policy_dir), "active")
        _, verified = self.run_main("--verify")
        self.assertEqual(verified[0]["self_protection"]["status"], "active")

    def test_dry_run_reports_without_writing(self) -> None:
        _, report = self.run_main("--self-protection", "on", "--dry-run")
        self.assertEqual(report[0]["self_protection"]["status"], "dry-run")
        self.assertFalse(self.policy_dir.exists())

    def test_uninstall_all_removes_only_the_generated_copy(self) -> None:
        self.run_main("--self-protection", "on")
        argv = ["all", "--config-dir", str(self.config), "--uninstall", "--force"]
        out = io.StringIO()
        with mock.patch.dict(os.environ, self.env, clear=True), \
                mock.patch.object(coacus_install, "_home", return_value=Path(self._tmp.name) / "home"), \
                contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            coacus_install.main(argv, REPO)
        self.assertEqual(json.loads(out.getvalue())[0]["self_protection"]["status"], "removed")
        self.assertFalse((self.policy_dir / selfprotect.POLICY_FILE).exists())


if __name__ == "__main__":
    unittest.main()
