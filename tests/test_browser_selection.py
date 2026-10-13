"""Tests for install-time browser detection, selection and the generated policy."""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from engine.guardrail import browsers, evaluate
from scripts import coacus_guard, coacus_install

REPO = Path(__file__).resolve().parents[1]
CATALOG = browsers.load_catalog(REPO)


def which_for(*names: str):
    """A fake ``shutil.which`` resolving only ``names``."""
    return lambda name: f"/fake/bin/{name}" if name in names else None


def detect(*names: str, paths: tuple[str, ...] = (), flatpak: set[str] | None = None) -> list[dict]:
    return browsers.detect(
        CATALOG, which=which_for(*names), exists=lambda p: p in paths, flatpak=flatpak or set()
    )


class TestDetect(unittest.TestCase):
    def test_binary_on_path(self) -> None:
        found = detect("chromium-browser", "firefox")
        self.assertEqual([b["id"] for b in found], ["chromium", "firefox"])

    def test_known_absolute_path_and_flatpak(self) -> None:
        found = detect(paths=("/opt/google/chrome/chrome",), flatpak={"com.brave.Browser"})
        self.assertEqual([b["id"] for b in found], ["google-chrome", "brave"])
        self.assertEqual(found[1]["binary"], "flatpak:com.brave.Browser")

    def test_nothing_installed(self) -> None:
        self.assertEqual(detect(), [])


class TestChoose(unittest.TestCase):
    def test_auto_prefers_catalogue_order_without_fallback(self) -> None:
        found = detect("brave", "google-chrome", "chromium")
        picked = browsers.choose(CATALOG, found)
        self.assertEqual((picked["primary"], picked["fallback"]), ("chromium", None))

    def test_auto_skips_missing_preferences(self) -> None:
        found = detect("brave", "firefox")
        self.assertEqual(browsers.choose(CATALOG, found)["primary"], "brave")

    def test_explicit_primary_and_fallback(self) -> None:
        found = detect("chromium", "firefox")
        picked = browsers.choose(CATALOG, found, primary="firefox", fallback="chromium")
        self.assertEqual((picked["primary"], picked["fallback"]), ("firefox", "chromium"))

    def test_rejects_uninstalled_or_equal_choices(self) -> None:
        found = detect("chromium")
        for kwargs in ({"primary": "brave"}, {"primary": "chromium", "fallback": "firefox"},
                       {"primary": "chromium", "fallback": "chromium"}):
            with self.assertRaises(ValueError):
                browsers.choose(CATALOG, found, **kwargs)
        with self.assertRaises(ValueError):
            browsers.choose(CATALOG, [])


class TestPrompt(unittest.TestCase):
    def run_prompt(self, answers: list[str], *names: str) -> dict | None:
        feed = iter(answers)
        return browsers.prompt_selection(
            CATALOG, detect(*names), ask=lambda _: next(feed), say=lambda _: None
        )

    def test_defaults_accept_preferred_primary_and_no_fallback(self) -> None:
        picked = self.run_prompt(["", ""], "chromium", "brave")
        self.assertEqual((picked["primary"], picked["fallback"]), ("chromium", None))

    def test_number_and_id_answers(self) -> None:
        picked = self.run_prompt(["2", "chromium"], "chromium", "brave")
        self.assertEqual((picked["primary"], picked["fallback"]), ("brave", "chromium"))

    def test_skip_returns_none(self) -> None:
        self.assertIsNone(self.run_prompt(["skip"], "chromium"))

    def test_fallback_equal_to_primary_is_re_asked(self) -> None:
        picked = self.run_prompt(["chromium", "chromium", "brave"], "chromium", "brave")
        self.assertEqual(picked["fallback"], "brave")


class TestPolicy(unittest.TestCase):
    def setUp(self) -> None:
        found = detect("chromium", "google-chrome", "brave")
        self.selection = browsers.choose(CATALOG, found, primary="chromium")
        self.doc = browsers.build_policy(CATALOG, self.selection)
        self.policies = self.doc["policies"]

    def decide(self, verb: str, resource: str) -> str:
        return evaluate.evaluate(self.policies, verb, resource)["decision"]

    def test_denies_every_non_selected_browser(self) -> None:
        for command in (
            "google-chrome-stable --headless",
            "nohup /opt/google/chrome/google-chrome &",
            'bash -c "brave-browser https://example.com"',
            "env FOO=1 brave",
            "sudo -u nobody firefox",
            "flatpak run com.google.Chrome",
            "echo $(microsoft-edge)",
        ):
            self.assertEqual(self.decide("exec", command), "deny", command)

    def test_selected_browser_and_mentions_are_allowed(self) -> None:
        for command in (
            "chromium-browser --version",
            "chromium --remote-debugging-port=9222",
            "grep google-chrome notes.txt",
            'git commit -m "stop using brave"',
            "ls /opt/google/chrome",
            "curl -s http://127.0.0.1:9222/json/version",
        ):
            self.assertEqual(self.decide("exec", command), "allow", command)

    def test_fallback_is_allowed_too(self) -> None:
        doc = browsers.build_policy(
            CATALOG, browsers.choose(CATALOG, detect("chromium", "firefox"), primary="chromium", fallback="firefox")
        )
        result = evaluate.evaluate(doc["policies"], "exec", "firefox https://example.com")
        self.assertEqual(result["decision"], "allow")

    def test_profiles_are_denied_for_read_and_write(self) -> None:
        self.assertEqual(self.decide("read", "/home/user/.config/google-chrome/Default/Cookies"), "deny")
        self.assertEqual(self.decide("write", "/home/user/.config/BraveSoftware"), "deny")
        self.assertEqual(self.decide("read", "/home/user/.config/chromium/Default/Preferences"), "allow")

    def test_document_is_enabled_and_marked_generated(self) -> None:
        self.assertIs(self.doc["enabled"], True)
        self.assertEqual(self.doc["generated"]["by"], browsers.GENERATED_BY)
        self.assertEqual(self.doc["generated"]["primary"], "chromium")


class TestPolicyFiles(unittest.TestCase):
    def test_write_read_remove_roundtrip(self) -> None:
        selection = {"primary": "chromium", "fallback": None, "detected": ["chromium"]}
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            path = browsers.write_policy(directory, browsers.build_policy(CATALOG, selection))
            self.assertTrue(path.is_file())
            self.assertEqual(browsers.read_selection(directory)["primary"], "chromium")
            self.assertTrue(browsers.remove_policy(directory))
            self.assertFalse(path.exists())

    def test_remove_never_deletes_a_hand_written_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / browsers.POLICY_FILE
            path.write_text(json.dumps({"enabled": True, "policies": []}), encoding="utf-8")
            self.assertFalse(browsers.remove_policy(Path(tmp)))
            self.assertTrue(path.exists())

    def test_user_policies_load_only_when_requested(self) -> None:
        selection = {"primary": "chromium", "fallback": None, "detected": ["chromium"]}
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            browsers.write_policy(directory, browsers.build_policy(CATALOG, selection))
            self.assertEqual(evaluate.load_policies(REPO), [])
            loaded = evaluate.load_policies(REPO, include_user=True, user_dir=directory)
            self.assertGreater(len(loaded), 5)

    def test_user_policy_dir_resolution(self) -> None:
        home = Path("/h")
        self.assertEqual(evaluate.user_policy_dir({"COACUS_POLICY_DIR": "/x"}, home), Path("/x"))
        self.assertEqual(
            evaluate.user_policy_dir({"XDG_CONFIG_HOME": "/xdg"}, home), Path("/xdg/coacus/policies")
        )
        self.assertEqual(evaluate.user_policy_dir({}, home), Path("/h/.config/coacus/policies"))


class TestGuardUsesUserPolicy(unittest.TestCase):
    def test_guard_denies_via_generated_policy(self) -> None:
        selection = {"primary": "chromium", "fallback": None, "detected": ["chromium"]}
        with tempfile.TemporaryDirectory() as tmp:
            browsers.write_policy(Path(tmp), browsers.build_policy(CATALOG, selection))
            payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": "brave-browser"}})
            with patch.dict(os.environ, {"COACUS_POLICY_DIR": tmp}):
                out = json.loads(coacus_guard.run("claude-code", "tool.pre", payload, REPO))
            self.assertEqual(out["hookSpecificOutput"]["permissionDecision"], "deny")
            allowed = json.dumps({"tool_name": "Bash", "tool_input": {"command": "chromium --version"}})
            with patch.dict(os.environ, {"COACUS_POLICY_DIR": tmp}):
                self.assertEqual(coacus_guard.run("claude-code", "tool.pre", allowed, REPO), "{}")


class TestGuardArgvCommand(unittest.TestCase):
    def test_argv_list_is_rendered_as_one_shell_string(self) -> None:
        verb, resource = coacus_guard._action(
            {"tool_name": "Bash", "tool_input": {"command": ["bash", "-lc", "brave-browser --x"]}}
        )
        self.assertEqual(verb, "exec")
        self.assertEqual(resource, "bash -lc 'brave-browser --x'")
        self.assertIn("brave-browser", evaluate.command_candidates(resource))

    def test_string_command_is_unchanged(self) -> None:
        verb, resource = coacus_guard._action(
            {"tool_name": "Bash", "tool_input": {"command": "ls -la"}}
        )
        self.assertEqual((verb, resource), ("exec", "ls -la"))


class TestInstallerStep(unittest.TestCase):
    def run_main(self, argv: list[str]) -> tuple[int, list[dict]]:
        out = StringIO()
        with redirect_stdout(out):
            code = coacus_install.main(argv, REPO)
        return code, json.loads(out.getvalue())

    def test_explicit_selection_writes_policy_in_custom_dir(self) -> None:
        found = detect("chromium", "brave")
        with tempfile.TemporaryDirectory() as tmp, \
                patch("engine.guardrail.browsers.detect", return_value=found):
            code, results = self.run_main([
                "claude-code", "--config-dir", tmp, "--force", "--no-lock-skills",
                "--skills", "using-coacus", "--only", "workflows",
                "--browser-primary", "chromium", "--dry-run",
            ])
            self.assertEqual(code, 0)
            state = results[0]["browser_policy"]
            self.assertEqual(state["status"], "dry-run")
            self.assertEqual(state["selection"]["primary"], "chromium")
            self.assertFalse((Path(tmp) / "coacus-policies" / browsers.POLICY_FILE).exists())

    def test_bad_selection_stops_before_installing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, \
                patch("engine.guardrail.browsers.detect", return_value=detect("chromium")):
            code, results = self.run_main([
                "claude-code", "--config-dir", tmp, "--force", "--browser-primary", "brave",
            ])
            self.assertEqual(code, 2)
            self.assertIn("not installed", results[0]["error"])
            self.assertFalse(list(Path(tmp).iterdir()))

    def test_off_by_default_without_a_tty(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            code, results = self.run_main([
                "claude-code", "--config-dir", tmp, "--force", "--dry-run",
                "--skills", "using-coacus", "--only", "workflows",
            ])
            self.assertEqual(code, 0)
            self.assertEqual(results[0]["browser_policy"]["status"], "off")


if __name__ == "__main__":
    unittest.main()
