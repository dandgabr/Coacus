"""A policy can ask the agent to keep going once when it tries to stop."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path

from engine.guardrail import evaluate as engine
from scripts import coacus_guard, coacus_install

REPO = Path(__file__).resolve().parents[1]


def stop_policy(decision="deny", resource="*", event="turn.stop", **extra) -> dict:
    policy = {"id": "verify-first", "event": event, "action": {"verb": "stop", "resource": resource},
              "decision": decision, "message": "Run the tests before you finish."}
    policy.update(extra)
    return policy


def document(*policies: dict, enabled: bool = True) -> dict:
    return {"schema": 1, "enabled": enabled, "policies": list(policies)}


class Case(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.base = Path(self._tmp.name)
        self.policies = self.base / "policies"
        self.policies.mkdir()
        env = {k: v for k, v in os.environ.items() if k not in ("CI", "COACUS_GUARD_ASK", "COACUS_GUARD_NO_ASK")}
        env["COACUS_POLICY_DIR"] = str(self.policies)
        patcher = unittest.mock.patch.dict(os.environ, env, clear=True)
        patcher.start()
        self.addCleanup(patcher.stop)

    def put(self, doc: dict) -> None:
        (self.policies / "p.policy.json").write_text(json.dumps(doc), encoding="utf-8")

    def run_guard(self, payload: dict, harness="claude-code") -> dict:
        return json.loads(coacus_guard.run(harness, "turn.stop", json.dumps(payload), REPO))


class TestStopDecision(Case):
    def test_a_deny_asks_the_agent_to_continue_with_the_reason(self) -> None:
        self.put(document(stop_policy()))
        for harness in ("claude-code", "codex"):
            with self.subTest(harness=harness):
                out = self.run_guard({"hook_event_name": "Stop", "stop_hook_active": False, "last_assistant_message": "All done."}, harness)
                self.assertEqual(out, {"decision": "block", "reason": "Run the tests before you finish."})

    def test_anything_but_an_explicit_false_is_doubt_and_allows(self) -> None:
        self.put(document(stop_policy()))
        for flag in (True, None, "true", "false", 1, 0, []):
            for harness in ("claude-code", "codex"):
                with self.subTest(flag=flag, harness=harness):
                    self.assertEqual(self.run_guard({"stop_hook_active": flag, "last_assistant_message": "x"}, harness), {})
        self.assertEqual(self.run_guard({"last_assistant_message": "x"}, "codex"), {})

    def test_text_that_grows_when_folded_does_not_match_every_rule(self) -> None:
        self.put(document(stop_policy(resource="*tests failed*")))
        message = "All good. " + "\ufdfa" * 6000
        self.assertEqual(self.run_guard({"stop_hook_active": False, "last_assistant_message": message}), {})

    def test_it_asks_only_once_per_turn(self) -> None:
        self.put(document(stop_policy()))
        self.assertEqual(self.run_guard({"stop_hook_active": True, "last_assistant_message": "Done."}), {})

    def test_the_pattern_reads_the_final_message_case_insensitively(self) -> None:
        self.put(document(stop_policy(resource="*all done*")))
        self.assertIn("decision", self.run_guard({"stop_hook_active": False, "last_assistant_message": "ALL DONE here"}))
        self.assertEqual(self.run_guard({"stop_hook_active": False, "last_assistant_message": "still working"}), {})

    def test_a_catch_all_rule_also_matches_a_missing_or_odd_message(self) -> None:
        self.put(document(stop_policy()))
        for message in (None, 5, ""):
            payload = {"stop_hook_active": False, "last_assistant_message": message}
            with self.subTest(payload=payload):
                self.assertIn("decision", self.run_guard(payload))
        self.assertIn("decision", self.run_guard({"stop_hook_active": False}))

    def test_a_very_long_message_is_read_from_its_end(self) -> None:
        self.put(document(stop_policy(resource="*needle")))
        self.assertIn("decision", self.run_guard({"stop_hook_active": False, "last_assistant_message": "a" * 300000 + "needle"}))
        self.assertEqual(self.run_guard({"stop_hook_active": False, "last_assistant_message": "needle" + "a" * 300000}), {})

    def test_an_ask_degrades_to_its_fallback(self) -> None:
        self.put(document(stop_policy(decision="ask", on_ask_unavailable="deny")))
        self.assertIn("decision", self.run_guard({"stop_hook_active": False, "last_assistant_message": "x"}))
        self.put(document(stop_policy(decision="ask", on_ask_unavailable="allow")))
        self.assertEqual(self.run_guard({"stop_hook_active": False, "last_assistant_message": "x"}), {})

    def test_note_allow_disabled_and_other_events_say_nothing(self) -> None:
        for doc in (document(stop_policy(decision="note")), document(stop_policy(decision="allow")),
                    document(stop_policy(), enabled=False)):
            self.put(doc)
            self.assertEqual(self.run_guard({"stop_hook_active": False, "last_assistant_message": "x"}), {})

    def test_another_event_name_is_ignored(self) -> None:
        self.put(document(stop_policy()))
        self.assertEqual(self.run_guard({"hook_event_name": "SubagentStop", "stop_hook_active": False, "last_assistant_message": "x"}), {})

    def test_a_harness_without_the_hook_gets_the_explicit_allow_it_expects(self) -> None:
        self.put(document(stop_policy()))
        self.assertEqual(self.run_guard({}, "antigravity"), {"decision": "allow"})
        for harness in ("cursor", "opencode"):
            self.assertIn(self.run_guard({}, harness), ({}, {"decision": "allow"}))

    def test_garbage_input_never_raises(self) -> None:
        self.put(document(stop_policy()))
        for text in ("", "not json", "[]", "null"):
            json.loads(coacus_guard.run("claude-code", "turn.stop", text, REPO))


class TestEventAndVerbStayApart(Case):
    def test_a_stop_rule_without_an_event_binds_turn_stop(self) -> None:
        policy = stop_policy()
        del policy["event"]
        self.put(document(policy))
        self.assertIn("decision", self.run_guard({"stop_hook_active": False, "last_assistant_message": "x"}))

    def test_a_stop_rule_never_fires_on_a_tool_call_or_a_prompt(self) -> None:
        self.put(document(stop_policy(event="tool.pre")))
        pre = {"tool_name": "Bash", "tool_input": {"command": "ls"}}
        self.assertEqual(json.loads(coacus_guard.run("claude-code", "tool.pre", json.dumps(pre), REPO)), {})
        self.assertEqual(json.loads(coacus_guard.run("claude-code", "prompt.submit", json.dumps({"prompt": "x"}), REPO)), {})

    def test_a_tool_rule_bound_to_turn_stop_never_fires(self) -> None:
        policy = stop_policy()
        policy["action"] = {"verb": "exec", "resource": "*"}
        self.put(document(policy))
        self.assertEqual(self.run_guard({"stop_hook_active": False, "last_assistant_message": "x"}), {})

    def test_evaluate_matches_by_verb_and_event(self) -> None:
        self.assertEqual(engine.evaluate([stop_policy()], "stop", "x", "turn.stop")["decision"], "deny")
        self.assertEqual(engine.evaluate([stop_policy()], "stop", "x", "tool.pre")["decision"], "allow")

    def test_the_script_runs_end_to_end(self) -> None:
        self.put(document(stop_policy()))
        proc = subprocess.run(
            [sys.executable, str(REPO / "scripts/coacus_guard.py"), "--harness", "claude-code", "--event", "turn.stop",
             "--root", str(REPO)], input=json.dumps({"stop_hook_active": False, "last_assistant_message": "x"}), capture_output=True, text=True,
            env=dict(os.environ), timeout=60)
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(json.loads(proc.stdout)["decision"], "block")


class TestInstall(Case):
    def _fragment(self, harness="claude-code") -> dict:
        _, fragment = coacus_install._guardrail_artifacts(REPO, harness, self.base / "cfg")
        return fragment

    def test_no_policy_means_no_hook_process(self) -> None:
        self.assertEqual(self._fragment()["hooks"]["Stop"], [])
        self.assertEqual(self._fragment("codex")["hooks"]["Stop"], [])

    def test_an_enabled_deny_adds_the_stop_hook_on_both_harnesses(self) -> None:
        self.put(document(stop_policy()))
        for harness in ("claude-code", "codex"):
            with self.subTest(harness=harness):
                entry = self._fragment(harness)["hooks"]["Stop"]
                command = entry[0]["hooks"][0]["command"]
                self.assertIn(f"--harness {harness} --event turn.stop", command)
                self.assertNotIn("matcher", entry[0])

    def test_only_a_deny_or_ask_on_stop_adds_it(self) -> None:
        for policy in (stop_policy(decision="note"), stop_policy(decision="allow"), stop_policy(event="tool.pre")):
            with self.subTest(decision=policy["decision"], event=policy["event"]):
                self.put(document(policy))
                self.assertEqual(self._fragment()["hooks"]["Stop"], [])

    def test_a_stop_rule_with_no_event_or_a_typo_still_binds_turn_stop(self) -> None:
        for event in (None, "turn.stpo"):
            policy = stop_policy()
            if event is None:
                del policy["event"]
            else:
                policy["event"] = event
            with self.subTest(event=event):
                self.put(document(policy))
                self.assertEqual(len(self._fragment()["hooks"]["Stop"]), 1)

    def test_a_rule_on_the_wrong_event_or_a_misspelled_decision(self) -> None:
        wrong = stop_policy(event="prompt.submit")
        self.put(document(wrong))
        self.assertEqual(self._fragment()["hooks"]["Stop"], [])
        self.assertEqual(self._fragment()["hooks"]["UserPromptSubmit"], [])
        self.put(document(stop_policy(decision="Deny")))
        self.assertEqual(len(self._fragment()["hooks"]["Stop"]), 1)

    def test_a_deny_with_no_event_is_refused_where_the_harness_cannot_block_a_stop(self) -> None:
        policy = stop_policy()
        del policy["event"]
        for harness in ("opencode", "cursor"):
            with self.subTest(harness=harness):
                reasons = coacus_install._refuse_unenforceable(REPO, harness, [document(policy)])
                self.assertTrue(any("turn.stop" in r for r in reasons))
        self.assertEqual(coacus_install._refuse_unenforceable(REPO, "claude-code", [document(policy)]), [])

    def test_disabling_the_policy_removes_both_codex_hooks(self) -> None:
        marker = f"{REPO.as_posix()}/scripts/coacus_guard.py"
        self.put(document(stop_policy(), {**stop_policy(), "id": "p", "event": "prompt.submit",
                                          "action": {"verb": "prompt", "resource": "*x*"}}))
        on = self._fragment("codex")["hooks"]
        self.assertEqual((len(on["Stop"]), len(on["UserPromptSubmit"])), (1, 1))
        installed = {"hooks": {"Stop": on["Stop"], "UserPromptSubmit": on["UserPromptSubmit"]}}
        self.put(document(stop_policy(), enabled=False))
        off = self._fragment("codex")
        merged = coacus_install._merge_hooks(installed, off, {marker})
        self.assertEqual(merged["hooks"].get("Stop", []), [])
        self.assertEqual(merged["hooks"].get("UserPromptSubmit", []), [])

    def test_other_harnesses_get_no_stop_hook(self) -> None:
        self.put(document(stop_policy()))
        for harness in ("cursor", "antigravity"):
            _, fragment = coacus_install._guardrail_artifacts(REPO, harness, self.base / "cfg")
            self.assertNotIn("turn.stop", json.dumps(fragment))


if __name__ == "__main__":
    unittest.main()
