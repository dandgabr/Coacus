"""A policy can block a prompt on Claude Code, and the hook exists only while one is enabled."""

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

from engine.guardrail import evaluate as engine
from scripts import coacus_guard, coacus_install

REPO = Path(__file__).resolve().parents[1]
NEEDLE = "BEGIN PRIVATE KEY"


def prompt_policy(decision="deny", fallback="deny", resource=NEEDLE, event="prompt.submit", verb="prompt") -> dict:
    return {"id": "no-keys", "event": event, "action": {"verb": verb, "resource": resource},
            "decision": decision, "on_ask_unavailable": fallback, "message": "do not paste keys"}


def document(*policies: dict, enabled: bool = True) -> dict:
    return {"schema": 1, "enabled": enabled, "policies": list(policies)}


class GuardCase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.base = Path(self._tmp.name)
        self.policies = self.base / "policies"
        self.policies.mkdir()
        env = {k: v for k, v in os.environ.items() if k not in ("CI", "COACUS_GUARD_ASK", "COACUS_GUARD_NO_ASK")}
        env["COACUS_POLICY_DIR"] = str(self.policies)
        patcher = mock.patch.dict(os.environ, env, clear=True)
        patcher.start()
        self.addCleanup(patcher.stop)

    def put(self, doc: dict, name: str = "p.policy.json") -> None:
        (self.policies / name).write_text(json.dumps(doc), encoding="utf-8")


class TestPromptDecision(GuardCase):
    def _run(self, payload, harness="claude-code", event="prompt.submit") -> dict:
        text = payload if isinstance(payload, str) else json.dumps(payload)
        return json.loads(coacus_guard.run(harness, event, text, REPO))

    def test_a_matching_prompt_is_blocked_with_the_reason(self) -> None:
        self.put(document(prompt_policy()))
        out = self._run({"prompt": f"here is my key\n-----{NEEDLE}-----"})
        self.assertEqual(out, {"decision": "block", "reason": "do not paste keys"})

    def test_a_clean_prompt_gets_no_opinion(self) -> None:
        self.put(document(prompt_policy()))
        self.assertEqual(self._run({"prompt": "please refactor the parser"}), {})

    def test_the_case_of_a_word_never_decides_a_prompt_rule(self) -> None:
        self.put(document(prompt_policy()))
        for text in (NEEDLE.lower(), NEEDLE.title(), f"x {NEEDLE.upper()} y"):
            with self.subTest(text=text):
                self.assertEqual(self._run({"prompt": text})["decision"], "block")

    def test_a_block_without_a_message_still_carries_a_reason(self) -> None:
        policy = prompt_policy()
        del policy["message"]
        self.put(document(policy))
        self.assertTrue(self._run({"prompt": NEEDLE})["reason"])

    def test_a_prompt_is_never_asked_about(self) -> None:
        with mock.patch.dict(os.environ, {"COACUS_GUARD_ASK": "1"}):
            for fallback, expected in (("deny", "block"), ("allow", None), ("bogus", "block")):
                with self.subTest(fallback=fallback):
                    self.put(document(prompt_policy(decision="ask", fallback=fallback)))
                    out = self._run({"prompt": NEEDLE})
                    self.assertEqual(out.get("decision"), expected)

    def test_a_note_policy_never_blocks(self) -> None:
        self.put(document(prompt_policy(decision="note")))
        self.assertEqual(self._run({"prompt": NEEDLE}), {})

    def test_only_claude_code_renders_a_block(self) -> None:
        self.put(document(prompt_policy()))
        for harness in ("codex", "cursor", "opencode", "antigravity", "command-code"):
            with self.subTest(harness=harness):
                self.assertIn(self._run({"prompt": NEEDLE}, harness), ({}, {"decision": "allow"}))

    def test_odd_payloads_say_nothing_and_never_raise(self) -> None:
        self.put(document(prompt_policy()))
        for payload in ("", "{}", "[]", "null", "not json", {"prompt": None}, {"prompt": 5}, {"prompt": ""}, {"prompt": ["x"]},
                        {"text": NEEDLE}):
            with self.subTest(payload=payload):
                self.assertEqual(self._run(payload), {})

    def test_a_prompt_over_the_size_cap_matches_every_prompt_rule(self) -> None:
        # Documented: an oversize value fails closed, as for every verb.
        self.put(document(prompt_policy()))
        huge = "a" * (engine._MAX_COMMAND_CHARS + 1)
        self.assertEqual(self._run({"prompt": huge})["decision"], "block")

    def test_a_disabled_document_blocks_nothing(self) -> None:
        self.put(document(prompt_policy(), enabled=False))
        self.assertEqual(self._run({"prompt": NEEDLE}), {})


class TestEventAndVerbStayApart(GuardCase):
    def test_a_prompt_rule_bound_to_tool_pre_never_fires_on_a_tool_call(self) -> None:
        self.put(document(prompt_policy(event="tool.pre")))
        for payload in ({"tool_name": "Bash", "tool_input": {"command": NEEDLE}},
                        {"tool_name": "Read", "tool_input": {"file_path": NEEDLE}}):
            with self.subTest(payload=payload):
                self.assertEqual(json.loads(coacus_guard.run("claude-code", "tool.pre", json.dumps(payload), REPO)), {})

    def test_a_tool_rule_bound_to_prompt_submit_never_fires_on_a_prompt(self) -> None:
        self.put(document(prompt_policy(verb="exec", resource="*private*")))
        self.assertEqual(json.loads(coacus_guard.run("claude-code", "prompt.submit", json.dumps({"prompt": "private"}), REPO)), {})

    def test_a_rule_with_no_event_is_a_tool_pre_rule_and_stays_silent_on_prompts(self) -> None:
        policy = prompt_policy()
        del policy["event"]
        self.put(document(policy))
        self.assertEqual(json.loads(coacus_guard.run("claude-code", "prompt.submit", json.dumps({"prompt": NEEDLE}), REPO)), {})

    def test_the_script_blocks_end_to_end(self) -> None:
        self.put(document(prompt_policy()))
        proc = subprocess.run(
            [sys.executable, str(REPO / "scripts/coacus_guard.py"), "--harness", "claude-code", "--event", "prompt.submit",
             "--root", str(REPO)], input=json.dumps({"prompt": NEEDLE}), capture_output=True, text=True,
            env=dict(os.environ), timeout=60)
        self.assertEqual(json.loads(proc.stdout.strip())["decision"], "block")
        self.assertEqual(proc.returncode, 0)


class TestHarnessData(unittest.TestCase):
    def test_a_native_hook_is_named_only_where_the_event_can_block_and_is_documented(self) -> None:
        named = {}
        for path in sorted((REPO / "harnesses").glob("*/harness.json")):
            events = json.loads(path.read_text(encoding="utf-8")).get("lifecycle", {}).get("events", {})
            for event, cap in events.items():
                if isinstance(cap, dict) and "native" in cap:
                    named[(path.parent.name, event)] = cap
        self.assertEqual(set(named), {("claude-code", "prompt.submit")})
        for cap in named.values():
            self.assertIs(cap["can_block"], True)
            self.assertEqual(cap["evidence"], "documented")
            self.assertTrue(cap["source"].startswith("https://"))


class TestInstall(GuardCase):
    def _fragment(self) -> dict:
        _, fragment = coacus_install._guardrail_artifacts(REPO, "claude-code", self.base / "cfg")
        return fragment

    def test_no_enabled_prompt_policy_means_no_hook_process(self) -> None:
        hooks = self._fragment()["hooks"]
        self.assertEqual(hooks["UserPromptSubmit"], [])
        self.assertIn("--event tool.pre", hooks["PreToolUse"][0]["hooks"][0]["command"])

    def test_an_enabled_prompt_policy_adds_the_hook_with_the_swapped_event(self) -> None:
        self.put(document(prompt_policy()))
        entry = self._fragment()["hooks"]["UserPromptSubmit"]
        self.assertEqual(len(entry), 1)
        command = entry[0]["hooks"][0]["command"]
        self.assertIn("--event prompt.submit", command)
        self.assertNotIn("--event tool.pre", command)
        self.assertNotIn("matcher", entry[0])

    def test_a_disabled_or_tool_pre_policy_does_not_add_it(self) -> None:
        for doc in (document(prompt_policy(), enabled=False), document(prompt_policy(event="tool.pre"))):
            with self.subTest(doc=doc):
                self.put(doc)
                self.assertEqual(self._fragment()["hooks"]["UserPromptSubmit"], [])

    def test_a_harness_with_no_native_name_gets_no_extra_hook(self) -> None:
        self.put(document(prompt_policy()))
        for harness in ("codex", "cursor", "antigravity"):
            with self.subTest(harness=harness):
                _, fragment = coacus_install._guardrail_artifacts(REPO, harness, self.base / "cfg")
                text = json.dumps(fragment)
                self.assertNotIn("prompt.submit", text)

    def test_the_merge_drops_a_stale_hook_and_keeps_the_users_own(self) -> None:
        marker = f"{REPO.as_posix()}/scripts/coacus_guard.py"
        stale = {"hooks": [{"type": "command", "command": f"python {marker} --event prompt.submit"}]}
        theirs = {"hooks": [{"type": "command", "command": "my-own-hook"}]}
        markers = coacus_install._hook_owner_markers(REPO, "claude-code")
        merged = coacus_install._merge_hooks({"hooks": {"UserPromptSubmit": [stale, theirs]}},
                                             {"hooks": {"UserPromptSubmit": []}}, markers)
        self.assertEqual(merged["hooks"]["UserPromptSubmit"], [theirs])
        alone = coacus_install._merge_hooks({"hooks": {"UserPromptSubmit": [stale]}},
                                            {"hooks": {"UserPromptSubmit": []}}, markers)
        self.assertNotIn("UserPromptSubmit", alone["hooks"])
        fresh = coacus_install._merge_hooks({}, {"hooks": {"UserPromptSubmit": []}}, markers)
        self.assertNotIn("UserPromptSubmit", fresh.get("hooks", {}))

    def _install(self) -> Path:
        cfg = self.base / "cfg"
        cfg.mkdir(exist_ok=True)
        argv = ["claude-code", "--config-dir", str(cfg), "--skills", "using-coacus", "--agents", "general",
                "--browser-policy", "off", "--skills-mode", "copy", "--force", "--yes"]
        with mock.patch.object(coacus_install, "_is_interactive", return_value=False), \
                mock.patch.object(coacus_install, "_home", return_value=self.base / "home"), \
                contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(coacus_install.main(argv, REPO), 0)
        return cfg / "settings.json"

    def test_install_adds_the_hook_then_a_reinstall_without_the_policy_removes_it(self) -> None:
        self.put(document(prompt_policy()))
        settings = json.loads(self._install().read_text(encoding="utf-8"))
        self.assertIn("UserPromptSubmit", settings["hooks"])
        self.assertIn("--event prompt.submit", json.dumps(settings["hooks"]["UserPromptSubmit"]))
        (self.policies / "p.policy.json").unlink()
        settings = json.loads(self._install().read_text(encoding="utf-8"))
        self.assertNotIn("UserPromptSubmit", settings["hooks"])
        self.assertIn("PreToolUse", settings["hooks"])


if __name__ == "__main__":
    unittest.main()
