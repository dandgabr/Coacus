"""The OpenCode plugin asks only through the V2 permission evaluate hook.

These drive the generated plugin under Node with a FAKE ``ctx``: they prove how the
plugin and the guard behave against the documented hook contract (a hook may change
the effect to allow, ask or deny), not against a live OpenCode V2 run, which is not
available here. The properties that matter: a V1 install (no permission API) never
turns an ask into an allow, and the evaluate hook never loosens a decision.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / "harnesses/opencode/bootstrap/coacus-guardrails.js"

DRIVER = """
import plugin, { CoacusGuardrails } from './plugin.mjs';
const scenario = JSON.parse(process.env.SCENARIO);
const out = {};
let evaluate = null;
const ctx = { tool: { hook: async () => {} } };
if (scenario.v2) {
  ctx.permission = { hook: async (name, fn) => {
    if (scenario.registerThrows) throw new Error('no permission API');
    if (name === 'evaluate') evaluate = fn;
  } };
}
const before = [];
ctx.tool.hook = async (name, fn) => { before.push(fn); };
await plugin.setup(ctx);
const call = scenario.call || { tool: 'read', input: { filePath: 'repo/.env' } };
const run = async () => {
  try { await before[0](call); return 'passed'; }
  catch (e) { return 'blocked'; }
};
out.before = await run();
out.registered = evaluate !== null;
if (evaluate) {
  const event = { effect: scenario.incoming, action: scenario.action || 'read',
    resources: scenario.resources || ['repo/.env'] };
  const result = await evaluate(event);
  out.effect = event.effect;
  out.returned = result && result.effect;
}
console.log(JSON.stringify(out));
"""


def ask_policy(fallback: str) -> dict:
    # A suffix pattern holds for any path shape the hook may report.
    return {"id": "ask-env", "action": {"verb": "read", "resource": "*.env"},
            "decision": "ask", "on_ask_unavailable": fallback, "message": "needs a person"}


def deny_policy() -> dict:
    return {"id": "deny-env", "action": {"verb": "read", "resource": "**/.env"},
            "decision": "deny", "on_ask_unavailable": "deny", "message": "blocked"}


def node_or_fail(case: unittest.TestCase) -> None:
    if not shutil.which("node"):
        if os.environ.get("CI", "").strip().lower() not in ("", "0", "false", "no", "off"):
            case.fail("node is required in CI for the OpenCode plugin tests")
        case.skipTest("node is not installed")


class TestOpenCodeAskEvaluate(unittest.TestCase):
    def setUp(self) -> None:
        node_or_fail(self)
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        shutil.copytree(REPO / "engine", self.root / "engine")
        shutil.copytree(REPO / "harnesses/opencode", self.root / "harnesses/opencode")
        (self.root / "scripts").mkdir()
        shutil.copy(REPO / "scripts/coacus_guard.py", self.root / "scripts/coacus_guard.py")
        text = PLUGIN.read_text(encoding="utf-8")
        text = text.replace("__COACUS_ROOT__", str(self.root)).replace("__COACUS_PYTHON__", sys.executable)
        (self.root / "plugin.mjs").write_text(text, encoding="utf-8")
        (self.root / "driver.mjs").write_text(DRIVER, encoding="utf-8")

    def _policies(self, *policies: dict) -> None:
        directory = self.root / "methodology/lifecycle/policies"
        directory.mkdir(parents=True, exist_ok=True)
        document = {"schema": 1, "enabled": True, "policies": list(policies)}
        (directory / "t.policy.json").write_text(json.dumps(document), encoding="utf-8")

    def _run(self, *, v2: bool, incoming: str = "allow", opt_in: bool = False,
             register_throws: bool = False, extra: dict | None = None, **env: str) -> dict:
        base = {k: v for k, v in os.environ.items()
                if k not in ("CI", "COACUS_GUARD_ASK", "COACUS_GUARD_NO_ASK", "COACUS_POLICY_DIR")}
        base["COACUS_POLICY_DIR"] = str(self.root / "no-user-policies")
        if opt_in:
            base["COACUS_GUARD_ASK"] = "1"
        base.update(env)
        base["SCENARIO"] = json.dumps({"v2": v2, "incoming": incoming,
                                       "registerThrows": register_throws, **(extra or {})})
        proc = subprocess.run(["node", "driver.mjs"], cwd=self.root, capture_output=True,
                              text=True, env=base, timeout=60)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return json.loads(proc.stdout.strip())

    # Without the permission API an ask cannot be deferred to the evaluate hook.
    def test_v1_ask_with_deny_fallback_is_blocked_even_when_opted_in(self) -> None:
        self._policies(ask_policy("deny"))
        out = self._run(v2=False, opt_in=True)
        self.assertEqual(out["before"], "blocked")
        self.assertFalse(out["registered"])

    def test_v1_ask_with_allow_fallback_follows_the_fallback(self) -> None:
        self._policies(ask_policy("allow"))
        self.assertEqual(self._run(v2=False, opt_in=True)["before"], "passed")

    def test_a_failing_permission_registration_behaves_like_v1(self) -> None:
        self._policies(ask_policy("deny"))
        out = self._run(v2=True, opt_in=True, register_throws=True)
        self.assertEqual(out["before"], "blocked")
        self.assertFalse(out["registered"])

    # With the evaluate hook an ask is deferred to the permission prompt.
    def test_v2_opted_in_ask_defers_to_the_hook_and_prompts(self) -> None:
        self._policies(ask_policy("deny"))
        out = self._run(v2=True, opt_in=True, incoming="allow")
        self.assertEqual(out["before"], "passed")
        self.assertTrue(out["registered"])
        self.assertEqual(out["effect"], "ask")

    def test_v2_not_opted_in_degrades_in_both_hooks(self) -> None:
        self._policies(ask_policy("deny"))
        out = self._run(v2=True, opt_in=False, incoming="allow")
        self.assertEqual(out["before"], "blocked")
        self.assertEqual(out["effect"], "deny")

    def test_v2_not_opted_in_with_allow_fallback_changes_nothing(self) -> None:
        self._policies(ask_policy("allow"))
        out = self._run(v2=True, opt_in=False, incoming="allow")
        self.assertEqual(out["before"], "passed")
        self.assertEqual(out["effect"], "allow")

    def test_the_off_switches_win_over_the_opt_in(self) -> None:
        self._policies(ask_policy("deny"))
        for name in ("CI", "COACUS_GUARD_NO_ASK"):
            with self.subTest(switch=name):
                out = self._run(v2=True, opt_in=True, incoming="allow", **{name: "1"})
                self.assertEqual(out["before"], "blocked")
                self.assertEqual(out["effect"], "deny")

    def test_a_deny_policy_denies_in_the_hook_too(self) -> None:
        self._policies(deny_policy())
        out = self._run(v2=True, opt_in=True, incoming="allow")
        self.assertEqual(out["before"], "blocked")
        self.assertEqual(out["effect"], "deny")

    # Only a read and a write are deferred to the evaluate hook.
    def test_a_shell_ask_is_not_deferred_and_follows_its_fallback(self) -> None:
        self._policies({"id": "ask-shell", "action": {"verb": "exec", "resource": "*deploy*"},
                        "decision": "ask", "on_ask_unavailable": "deny", "message": "m"})
        call = {"tool": "bash", "input": {"command": "run deploy now"}}
        out = self._run(v2=True, opt_in=True, extra={
            "call": call, "action": "shell", "resources": ["run deploy now"]})
        self.assertEqual(out["before"], "blocked")  # degraded to deny, not allowed
        self.assertEqual(out["effect"], "ask")      # the hook may still raise it

    def test_a_subagent_ask_is_not_deferred(self) -> None:
        self._policies({"id": "ask-spawn", "action": {"verb": "spawn", "resource": "*"},
                        "decision": "ask", "on_ask_unavailable": "deny", "message": "m"})
        out = self._run(v2=True, opt_in=True, extra={
            "call": {"tool": "task", "input": {"prompt": "do it"}}, "action": "subagent",
            "resources": ["do it"]})
        self.assertEqual(out["before"], "blocked")

    def test_an_ask_anchored_on_one_path_shape_is_not_deferred(self) -> None:
        for pattern, path in (("sub/*", "sub/.env"), ("*/.env", "w/.env"), ("*/sub/*", "a/sub/.env")):
            with self.subTest(pattern=pattern):
                self._policies({"id": "ask-shape", "action": {"verb": "read", "resource": pattern},
                                "decision": "ask", "on_ask_unavailable": "deny", "message": "m"})
                out = self._run(v2=True, opt_in=True, extra={
                    "call": {"tool": "read", "input": {"filePath": path}}, "resources": [path]})
                self.assertEqual(out["before"], "blocked")

    def test_a_shape_independent_ask_is_deferred(self) -> None:
        self._policies({"id": "ask-any", "action": {"verb": "read", "resource": "*.env"},
                        "decision": "ask", "on_ask_unavailable": "deny", "message": "m"})
        out = self._run(v2=True, opt_in=True, extra={
            "call": {"tool": "read", "input": {"filePath": "w/sub/prod.env"}},
            "resources": ["prod.env"]})
        self.assertEqual(out["before"], "passed")
        self.assertEqual(out["effect"], "ask")

    def test_an_ask_anchored_on_an_absolute_path_is_not_deferred(self) -> None:
        # The hook sees a relative path, so an absolute anchor could miss there.
        self._policies({"id": "ask-abs", "action": {"verb": "read", "resource": "/srv/secret/*"},
                        "decision": "ask", "on_ask_unavailable": "deny", "message": "m"})
        out = self._run(v2=True, opt_in=True, extra={
            "call": {"tool": "read", "input": {"filePath": "/srv/secret/key"}},
            "resources": ["srv/secret/key"]})
        self.assertEqual(out["before"], "blocked")

    # The evaluate hook never loosens a decision it was given.
    def test_the_hook_never_loosens_an_incoming_effect(self) -> None:
        self._policies(ask_policy("allow"))  # the guard says allow when nobody can be asked
        for incoming in ("deny", "ask", "allow"):
            with self.subTest(incoming=incoming):
                out = self._run(v2=True, opt_in=False, incoming=incoming)
                self.assertEqual(out["effect"], incoming)

    def test_an_incoming_ask_is_not_turned_into_allow_when_the_guard_allows(self) -> None:
        self._policies()  # no policy matches
        self.assertEqual(self._run(v2=True, incoming="ask")["effect"], "ask")

    def test_a_guard_failure_leaves_the_effect_unchanged(self) -> None:
        self._policies(ask_policy("deny"))
        shutil.rmtree(self.root / "engine")  # the guard cannot start its evaluator
        for incoming in ("allow", "ask", "deny"):
            with self.subTest(incoming=incoming):
                self.assertEqual(self._run(v2=True, opt_in=True, incoming=incoming)["effect"], incoming)


class TestEvaluateHookWithAStubGuard(unittest.TestCase):
    """Feed the hook every guard answer, including ones the real guard never prints."""

    def setUp(self) -> None:
        node_or_fail(self)
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        (self.root / "scripts").mkdir()
        (self.root / "scripts/coacus_guard.py").write_text(
            "import os\nprint(os.environ['STUB_OUT'])\n", encoding="utf-8")
        text = PLUGIN.read_text(encoding="utf-8")
        text = text.replace("__COACUS_ROOT__", str(self.root)).replace("__COACUS_PYTHON__", sys.executable)
        (self.root / "plugin.mjs").write_text(text, encoding="utf-8")
        (self.root / "driver.mjs").write_text(DRIVER, encoding="utf-8")

    def _effect(self, incoming: str, stub_out: str) -> str:
        env = dict(os.environ, STUB_OUT=stub_out,
                   SCENARIO=json.dumps({"v2": True, "incoming": incoming, "registerThrows": False}))
        proc = subprocess.run(["node", "driver.mjs"], cwd=self.root, capture_output=True,
                              text=True, env=env, timeout=60)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return json.loads(proc.stdout.strip())["effect"]

    def test_the_effect_is_the_stricter_of_incoming_and_guard(self) -> None:
        table = {
            ("allow", "allow"): "allow", ("allow", "ask"): "ask", ("allow", "deny"): "deny",
            ("ask", "allow"): "ask", ("ask", "ask"): "ask", ("ask", "deny"): "deny",
            ("deny", "allow"): "deny", ("deny", "ask"): "deny", ("deny", "deny"): "deny",
        }
        for (incoming, guard_says), expected in table.items():
            with self.subTest(incoming=incoming, guard=guard_says):
                out = json.dumps({"decision": guard_says})
                self.assertEqual(self._effect(incoming, out), expected)

    def test_garbage_or_unknown_guard_output_changes_nothing(self) -> None:
        for stub in ("not json", "{}", "[]", "null", json.dumps({"decision": "permit"}),
                     json.dumps({"decision": 5}), ""):
            for incoming in ("allow", "ask", "deny"):
                with self.subTest(stub=stub, incoming=incoming):
                    self.assertEqual(self._effect(incoming, stub), incoming)


class TestPermissionMapping(unittest.TestCase):
    def setUp(self) -> None:
        sys.path.insert(0, str(REPO))
        from scripts import coacus_guard
        self.guard = coacus_guard

    def test_documented_v2_names_map_to_canonical_verbs(self) -> None:
        cases = {"read": "read", "edit": "write", "patch": "write", "shell": "exec",
                 "subagent": "spawn", "bash": "exec", "task": "spawn"}
        for action, verb in cases.items():
            with self.subTest(action=action):
                self.assertEqual(self.guard._permission_actions(
                    {"action": action, "resources": ["x"]}), [(verb, "x")])

    def test_unmapped_or_malformed_requests_map_to_nothing(self) -> None:
        for payload in ({"action": "glob", "resources": ["x"]}, {"action": "grep", "resources": ["x"]},
                        {"action": "read"}, {"action": "read", "resources": "x"}, {}, {"action": 5}):
            with self.subTest(payload=payload):
                self.assertEqual(self.guard._permission_actions(payload), [])


class TestCapabilityData(unittest.TestCase):
    def test_opencode_asks_only_on_the_evaluate_channel(self) -> None:
        sys.path.insert(0, str(REPO))
        from scripts import coacus_guard
        saved = {k: os.environ.get(k) for k in
                 ("COACUS_GUARD_ASK", "COACUS_GUARD_ASK_EXPERIMENTAL", "COACUS_GUARD_NO_ASK", "CI")}
        try:
            os.environ["COACUS_GUARD_ASK"] = "1"
            os.environ.pop("COACUS_GUARD_NO_ASK", None)
            os.environ.pop("CI", None)
            self.assertFalse(coacus_guard._can_ask(REPO, "opencode", "tool.pre", "default"))
            self.assertTrue(coacus_guard._can_ask(REPO, "opencode", "tool.pre", "evaluate"))
            self.assertTrue(coacus_guard._can_ask(REPO, "opencode", "tool.pre", "before"))
            # A harness without an ask channel never asks on the OpenCode-only channels.
            self.assertFalse(coacus_guard._can_ask(REPO, "claude-code", "tool.pre", "evaluate"))
            # The retired opt-in changes nothing, whether it is set or not.
            os.environ["COACUS_GUARD_ASK_EXPERIMENTAL"] = "0"
            self.assertTrue(coacus_guard._can_ask(REPO, "opencode", "tool.pre", "evaluate"))
            os.environ.pop("COACUS_GUARD_ASK")
            self.assertFalse(coacus_guard._can_ask(REPO, "opencode", "tool.pre", "evaluate"))
            self.assertFalse(coacus_guard._can_ask(REPO, "opencode", "tool.pre", "before"))
            os.environ["COACUS_GUARD_ASK"] = "1"
            self.assertTrue(coacus_guard._can_ask(REPO, "claude-code", "tool.pre", "default"))
        finally:
            for key, value in saved.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value


if __name__ == "__main__":
    unittest.main()
