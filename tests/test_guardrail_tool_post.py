"""A policy can attach a note to what a tool returned; it can never block, and the hook exists only while one is on."""

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
MARK = "ignore previous instructions"


def note_policy(decision="note", resource=f"*{MARK}*", event="tool.post", verb="output") -> dict:
    return {"id": "flag-injection", "event": event, "action": {"verb": verb, "resource": resource},
            "decision": decision, "message": "this tool output reads like an instruction"}


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

    def put(self, doc: dict, name: str = "p.policy.json") -> None:
        (self.policies / name).write_text(json.dumps(doc), encoding="utf-8")

    def run_guard(self, payload: dict, harness="claude-code", event="tool.post") -> dict:
        return json.loads(coacus_guard.run(harness, event, json.dumps(payload), REPO))


class TestNote(Case):
    def test_a_match_attaches_the_message_as_additional_context(self) -> None:
        self.put(document(note_policy()))
        out = self.run_guard({"hook_event_name": "PostToolUse", "tool_name": "Bash",
                              "tool_response": {"stdout": f"x {MARK.upper()} y", "stderr": ""}})
        self.assertEqual(out["hookSpecificOutput"]["hookEventName"], "PostToolUse")
        self.assertEqual(out["hookSpecificOutput"]["additionalContext"], "this tool output reads like an instruction")
        self.assertNotIn("decision", out)

    def test_stderr_and_other_response_shapes_are_scanned(self) -> None:
        self.put(document(note_policy()))
        for response in ({"stdout": "", "stderr": MARK}, MARK, {"content": [{"type": "text", "text": MARK}]},
                         [MARK], {"nested": {"deep": MARK}}):
            with self.subTest(response=response):
                self.assertIn("hookSpecificOutput", self.run_guard({"tool_response": response}))

    def test_no_match_or_no_response_is_silent(self) -> None:
        self.put(document(note_policy()))
        for payload in ({"tool_response": "fine"}, {"tool_response": None}, {}, {"tool_response": {"stdout": ""}}):
            with self.subTest(payload=payload):
                self.assertEqual(self.run_guard(payload), {})

    def test_folding_defeats_width_and_invisible_characters(self) -> None:
        self.put(document(note_policy()))
        text = "ｉgnore previous in​structions"
        self.assertIn("hookSpecificOutput", self.run_guard({"tool_response": text}))

    def test_a_marker_anywhere_in_a_long_output_is_found(self) -> None:
        self.put(document(note_policy()))
        filler = "a" * 150000
        for text in (MARK + filler, filler + MARK, filler + MARK + filler, "a" * 99000 + MARK + "b" * 99000):
            with self.subTest(length=len(text)):
                self.assertIn("hookSpecificOutput", self.run_guard({"tool_response": text}))
        self.assertEqual(self.run_guard({"tool_response": filler + "x" + filler}), {})

    def test_text_that_grows_when_folded_does_not_fire_every_rule(self) -> None:
        self.put(document(note_policy()))
        self.assertEqual(self.run_guard({"tool_response": "\ufdfa" * 20000}), {})

    def test_another_event_name_in_the_payload_is_ignored(self) -> None:
        self.put(document(note_policy()))
        self.assertEqual(self.run_guard({"hook_event_name": "PostToolUseFailure", "tool_response": MARK}), {})

    def test_other_harnesses_and_disabled_documents_stay_silent(self) -> None:
        self.put(document(note_policy()))
        for harness in ("codex", "cursor", "opencode"):
            self.assertEqual(self.run_guard({"tool_response": MARK}, harness=harness), {})
        # Antigravity reads a missing decision as a denial, so it gets an explicit allow.
        self.assertEqual(self.run_guard({"tool_response": MARK}, harness="antigravity"), {"decision": "allow"})
        self.put(document(note_policy(), enabled=False))
        self.assertEqual(self.run_guard({"tool_response": MARK}), {})

    def test_a_deny_policy_still_cannot_block_a_finished_tool(self) -> None:
        self.put(document(note_policy(decision="deny")))
        self.assertEqual(self.run_guard({"tool_response": MARK}), {})

    def test_the_note_is_capped(self) -> None:
        policy = note_policy()
        policy["message"] = "n" * 5000
        self.put(document(policy))
        out = self.run_guard({"tool_response": MARK})
        self.assertEqual(len(out["hookSpecificOutput"]["additionalContext"]), coacus_guard.OUTPUT_NOTE_CHARS)

    def test_garbage_input_never_raises(self) -> None:
        for text in ("", "not json", "[]", "null", '{"tool_response": 5}'):
            with self.subTest(text=text):
                json.loads(coacus_guard.run("claude-code", "tool.post", text, REPO))


class TestEventAndVerbStayApart(Case):
    def test_an_output_rule_never_fires_on_a_tool_call_or_a_prompt(self) -> None:
        self.put(document(note_policy(event="tool.pre")))
        pre = {"tool_name": "Bash", "tool_input": {"command": MARK}}
        self.assertEqual(json.loads(coacus_guard.run("claude-code", "tool.pre", json.dumps(pre), REPO)), {})
        self.assertEqual(self.run_guard({"prompt": MARK}, event="prompt.submit"), {})

    def test_a_tool_rule_bound_to_tool_post_never_fires_on_output(self) -> None:
        self.put(document(note_policy(verb="exec", resource=f"*{MARK}*")))
        self.assertEqual(self.run_guard({"tool_response": MARK}), {})

    def test_notes_helper_ignores_other_decisions_and_events(self) -> None:
        policies = [note_policy(), note_policy(decision="deny"), note_policy(event="prompt.submit")]
        self.assertEqual(len(engine.notes(policies, "output", MARK, "tool.post")), 1)
        self.assertEqual(len(engine.notes(["junk", None, 5, *policies], "output", MARK, "tool.post")), 1)

    def test_evaluate_is_unchanged_for_notes(self) -> None:
        self.assertEqual(engine.evaluate([note_policy()], "output", MARK, "tool.post")["decision"], "allow")

    def test_the_script_runs_end_to_end(self) -> None:
        self.put(document(note_policy()))
        proc = subprocess.run(
            [sys.executable, str(REPO / "scripts/coacus_guard.py"), "--harness", "claude-code", "--event", "tool.post",
             "--root", str(REPO)], input=json.dumps({"tool_response": MARK}), capture_output=True, text=True,
            env=dict(os.environ), timeout=60)
        self.assertEqual(proc.returncode, 0)
        self.assertIn("additionalContext", proc.stdout)


class TestMerge(Case):
    def test_a_stale_entry_is_removed_and_the_users_own_hook_stays(self) -> None:
        marker = f"{REPO.as_posix()}/scripts/coacus_guard.py"
        ours = coacus_install._command([sys.executable, "@optional", marker, "--event", "tool.post"])
        mine = {"hooks": [{"type": "command", "command": "echo mine"}]}
        existing = {"hooks": {"PostToolUse": [{"hooks": [{"type": "command", "command": ours}]}, mine]}}
        merged = coacus_install._merge_hooks(existing, {"hooks": {"PostToolUse": []}}, {marker})
        self.assertEqual(merged["hooks"]["PostToolUse"], [mine])


class TestInstall(Case):
    def _fragment(self) -> dict:
        _, fragment = coacus_install._guardrail_artifacts(REPO, "claude-code", self.base / "cfg")
        return fragment

    def test_no_policy_means_no_hook_process(self) -> None:
        self.assertEqual(self._fragment()["hooks"]["PostToolUse"], [])

    def test_an_enabled_note_policy_adds_the_hook_with_the_swapped_event(self) -> None:
        self.put(document(note_policy()))
        entry = self._fragment()["hooks"]["PostToolUse"]
        command = entry[0]["hooks"][0]["command"]
        self.assertIn("--event tool.post", command)
        self.assertNotIn("--event tool.pre", command)
        self.assertNotIn("matcher", entry[0])

    def test_only_a_note_on_output_adds_it(self) -> None:
        for policy in (note_policy(decision="deny"), note_policy(decision="allow"), note_policy(verb="exec"),
                       note_policy(event="tool.pre")):
            with self.subTest(policy=policy["decision"] + policy["action"]["verb"] + policy["event"]):
                self.put(document(policy))
                self.assertEqual(self._fragment()["hooks"]["PostToolUse"], [])

    def test_a_deny_on_tool_post_is_refused_at_install(self) -> None:
        reasons = coacus_install._refuse_unenforceable(REPO, "claude-code", [document(note_policy(decision="deny"))])
        self.assertTrue(any("tool.post" in reason for reason in reasons))

    def test_an_output_note_without_an_event_or_with_a_typo_still_binds_tool_post(self) -> None:
        for event in (None, "tool.psot"):
            policy = note_policy()
            if event is None:
                del policy["event"]
            else:
                policy["event"] = event
            with self.subTest(event=event):
                self.put(document(policy))
                self.assertEqual(len(self._fragment()["hooks"]["PostToolUse"]), 1)
                if event is None:
                    self.assertIn("hookSpecificOutput", self.run_guard({"tool_response": MARK}))

    def test_other_harnesses_get_no_post_hook(self) -> None:
        self.put(document(note_policy()))
        for harness in ("codex", "cursor", "antigravity"):
            _, fragment = coacus_install._guardrail_artifacts(REPO, harness, self.base / "cfg")
            self.assertNotIn("PostToolUse", json.dumps(fragment))


if __name__ == "__main__":
    unittest.main()
