"""Regression corpus for how deny rules read shell commands.

A deny rule with ``"match": "command"`` must see the executable a command line
would run, through wrappers, ``sh -c`` strings, command substitution, pipes and
symlinks, and must not fire on a mere mention of the name. These tests lock the
current behaviour of ``engine/guardrail/evaluate.py`` so a change cannot weaken a
deny rule unnoticed.

Only deny rules are covered. The shapes in ``KNOWN_BYPASSES`` are real gaps found
by measuring the evaluator: each is marked ``expectedFailure`` so the suite stays
green today and fails loudly (an unexpected success) once a shape is fixed, which
forces the mark to be removed. Two end-to-end tests assert the JSON the guard
prints, because the guard always exits with code 0 and the exit code proves nothing.

``tool.post`` is never evaluated by the guard today; nothing here relies on it.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from engine.guardrail import evaluate as guard

REPO = Path(__file__).resolve().parents[1]
GUARD_CLI = REPO / "scripts/coacus_guard.py"

# A neutral binary name, so no real tool is mentioned.
TARGET = "blockedbin"

POLICY = {
    "id": "no-blockedbin",
    "action": {"verb": "exec", "resource": TARGET, "match": "command"},
    "decision": "deny",
    "on_ask_unavailable": "deny",
    "message": "blocked by the corpus policy",
}

# Command lines that must resolve to the target executable.
MUST_MATCH = {
    "plain": f"{TARGET} --flag",
    "absolute path": f"/usr/bin/{TARGET}",
    "env wrapper": f"env FOO=1 {TARGET}",
    "assignment prefix": f"FOO=1 {TARGET}",
    "sudo with option value": f"sudo -u root {TARGET}",
    "nohup": f"nohup {TARGET} &",
    "command builtin": f"command {TARGET}",
    "exec builtin": f"exec {TARGET}",
    "time": f"time {TARGET}",
    "sh -c": f"sh -c '{TARGET} --flag'",
    "bash -lc": f'bash -lc "{TARGET}"',
    "dollar substitution": f"echo $({TARGET})",
    "backtick substitution": f"echo `{TARGET}`",
    "nested dollar substitution": f"echo $(echo $({TARGET}))",
    "second stage of a pipe": f"echo hi | {TARGET}",
    "after and": f"true && {TARGET}",
    "after semicolon": f"true; {TARGET}",
    "after newline": f"true\n{TARGET}",
    "parenthesised": f"({TARGET})",
    "quoted name": f"'{TARGET}'",
    "backslash name": f"\\{TARGET}",
    "xargs": f"echo x | xargs {TARGET}",
}

# Command lines that only mention the name and must not match.
MUST_NOT_MATCH = {
    "grep argument": f"grep {TARGET} notes.txt",
    "commit message": f'git commit -m "{TARGET}"',
    "echo argument": f"echo {TARGET}",
    "similar name": f"{TARGET}-helper --flag",
    "empty": "",
    "blank": "   ",
}

# Shapes measured as NOT caught today. Each one is a bypass of a command deny rule.
KNOWN_BYPASSES = {
    "brace group": "{ " + TARGET + "; }",
    "process substitution": f"cat <({TARGET})",
    "eval": f"eval {TARGET}",
    "here-string": f"bash <<< {TARGET}",
    "find -exec": f"find . -exec {TARGET} ;",
    "env -S": f"env -S '{TARGET} --flag'",
    "variable indirection": f"x={TARGET}; $x",
}


def names(command: str) -> list[str]:
    return guard.command_candidates(command)


class TestCommandCorpus(unittest.TestCase):
    def test_golden_positives_resolve_to_the_target(self) -> None:
        for label, command in MUST_MATCH.items():
            with self.subTest(label=label):
                self.assertIn(TARGET, names(command))
                self.assertEqual(guard.evaluate([POLICY], "exec", command)["decision"], "deny")

    def test_golden_negatives_do_not_match(self) -> None:
        for label, command in MUST_NOT_MATCH.items():
            with self.subTest(label=label):
                self.assertNotIn(TARGET, names(command))
                self.assertEqual(guard.evaluate([POLICY], "exec", command)["decision"], "allow")

    def test_symlink_to_the_target_is_resolved(self) -> None:
        if not hasattr(os, "symlink"):
            self.skipTest("symlinks are not available on this platform")
        with tempfile.TemporaryDirectory() as tmp:
            real = Path(tmp) / TARGET
            real.write_text("", encoding="utf-8")
            link = Path(tmp) / "harmless-name"
            try:
                link.symlink_to(real)
            except OSError:
                self.skipTest("symlinks cannot be created here")
            self.assertIn(TARGET, names(str(link)))

    def test_oversize_command_returns_without_raising(self) -> None:
        # Behaviour only: no timing assertion, so the test cannot flake.
        huge = "echo " + "a" * 200_000 + f" | {TARGET}"
        self.assertIsInstance(names(huge), list)

    def test_unbalanced_quotes_do_not_raise(self) -> None:
        self.assertIsInstance(names(f"echo 'unterminated {TARGET}"), list)

    def test_non_command_policy_still_matches_the_whole_string(self) -> None:
        plain = {**POLICY, "action": {"verb": "exec", "resource": f"*{TARGET}*"}}
        self.assertEqual(guard.evaluate([plain], "exec", f"grep {TARGET} notes.txt")["decision"], "deny")


class TestKnownBypasses(unittest.TestCase):
    """Each test passes only once its shape is fixed; remove the mark then."""

    def _assert_denied(self, command: str) -> None:
        self.assertEqual(guard.evaluate([POLICY], "exec", command)["decision"], "deny")

    @unittest.expectedFailure
    def test_brace_group(self) -> None:
        self._assert_denied(KNOWN_BYPASSES["brace group"])

    @unittest.expectedFailure
    def test_process_substitution(self) -> None:
        self._assert_denied(KNOWN_BYPASSES["process substitution"])

    @unittest.expectedFailure
    def test_eval(self) -> None:
        self._assert_denied(KNOWN_BYPASSES["eval"])

    @unittest.expectedFailure
    def test_here_string(self) -> None:
        self._assert_denied(KNOWN_BYPASSES["here-string"])

    @unittest.expectedFailure
    def test_find_exec(self) -> None:
        self._assert_denied(KNOWN_BYPASSES["find -exec"])

    @unittest.expectedFailure
    def test_env_split_string(self) -> None:
        self._assert_denied(KNOWN_BYPASSES["env -S"])

    @unittest.expectedFailure
    def test_variable_indirection(self) -> None:
        self._assert_denied(KNOWN_BYPASSES["variable indirection"])

    def test_every_listed_bypass_has_a_test(self) -> None:
        marked = {name for name in dir(self) if name.startswith("test_") and name != "test_every_listed_bypass_has_a_test"}
        self.assertEqual(len(marked), len(KNOWN_BYPASSES))


class TestGuardEndToEnd(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        policies = self.root / "methodology/lifecycle/policies"
        policies.mkdir(parents=True)
        document = {"schema": 1, "enabled": True, "policies": [POLICY]}
        (policies / "corpus.policy.json").write_text(json.dumps(document), encoding="utf-8")

    def _run(self, command: str) -> tuple[dict, int]:
        env = {key: value for key, value in os.environ.items()
               if key not in ("COACUS_POLICY_DIR", "CI", "COACUS_GUARD_ASK", "COACUS_GUARD_NO_ASK")}
        env["COACUS_POLICY_DIR"] = str(self.root / "no-user-policies")
        proc = subprocess.run(
            [sys.executable, str(GUARD_CLI), "--harness", "claude-code", "--event", "tool.pre",
             "--root", str(self.root)],
            input=json.dumps({"tool": "bash", "tool_input": {"command": command}}),
            capture_output=True, text=True, env=env, timeout=60,
        )
        return json.loads(proc.stdout.strip()), proc.returncode

    def test_a_wrapped_target_is_denied_in_the_printed_json(self) -> None:
        for label in ("sudo with option value", "sh -c", "dollar substitution", "second stage of a pipe"):
            with self.subTest(label=label):
                out, code = self._run(MUST_MATCH[label])
                self.assertEqual(code, 0)
                self.assertEqual(out["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_a_mere_mention_is_allowed_in_the_printed_json(self) -> None:
        out, code = self._run(MUST_NOT_MATCH["commit message"])
        self.assertEqual(code, 0)
        self.assertEqual(out, {})


if __name__ == "__main__":
    unittest.main()
