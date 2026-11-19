"""Shell constructs and the shipped browser policy under command deny rules.

Two guarantees: a construct that wraps a blocked command never hides it, and a
mere mention of a name never matches. The browser policy is the only shipped
user of ``"match": "command"``, so it is exercised through the real catalog.
"""

from __future__ import annotations

import json
import os
import random
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from engine.guardrail import browsers
from engine.guardrail import evaluate as guard

ROOT = Path(__file__).resolve().parents[1]
TARGET = "blockedbin"
POLICY = {
    "id": "no-blockedbin",
    "action": {"verb": "exec", "resource": TARGET, "match": "command"},
    "decision": "deny",
}

# Each wrapper takes a command string and returns a longer one that still runs it.
WRAPPERS = {
    "plain": lambda c: c,
    "brace group": lambda c: "{ " + c + "; }",
    "subshell": lambda c: "(" + c + ")",
    "sh -c": lambda c: "sh -c '" + c.replace("'", "'\\''") + "'",
    "eval": lambda c: "eval '" + c.replace("'", "'\\''") + "'",
    "env -S": lambda c: "env -S '" + c.replace("'", "'\\''") + "'",
    "if": lambda c: "if " + c + "; then true; fi",
    "redirected": lambda c: ">/dev/null " + c,
    "sudo sh -c": lambda c: "sudo sh -c '" + c.replace("'", "'\\''") + "'",
    "nohup bash -c": lambda c: "nohup bash -c '" + c.replace("'", "'\\''") + "'",
    "then": lambda c: "if true; then " + c + "; fi",
    "while": lambda c: "while " + c + "; do true; done",
    "negation": lambda c: "! " + c,
    "command substitution": lambda c: "echo $(" + c + ")",
    "backticks": lambda c: "echo `" + c + "`",
    "after semicolon": lambda c: "true; " + c,
    "after pipe": lambda c: "echo x | " + c,
    "after and": lambda c: "true && " + c,
    "process substitution": lambda c: "cat <(" + c + ")",
    "find -exec": lambda c: "find . -exec " + c + " ;",
}


# Prefix wrappers only make sense directly in front of a simple command, so they are
# applied first and never around a compound construct.
PREFIXES = {
    "sudo": lambda c: "sudo " + c,
    "nohup": lambda c: "nohup " + c,
    "timeout": lambda c: "timeout 5 " + c,
    "assignment": lambda c: "X=1 " + c,
    "two assignments": lambda c: "X=1 Y=2 " + c,
    "assignment with substitution": lambda c: "X=$(true) " + c,
}

# Known false positive (see KNOWN_FALSE_POSITIVES in the corpus): a prefix wrapper
# reads its first words as candidates, so a mention behind one still matches.
MENTION_SAFE = set(WRAPPERS)


def denied(command: str, policy: dict = POLICY) -> bool:
    return guard.evaluate([policy], "exec", command)["decision"] == "deny"


class TestWrappingNeverHidesTheCommand(unittest.TestCase):
    def test_every_single_wrapper_is_looked_through(self) -> None:
        for label, wrap in {**WRAPPERS, **PREFIXES}.items():
            with self.subTest(wrapper=label):
                self.assertTrue(denied(wrap(TARGET + " --flag")))

    def test_seeded_random_compositions_are_looked_through(self) -> None:
        rng = random.Random(20261118)
        labels = sorted(set(WRAPPERS) - {"backticks"})  # nested backticks need escaping
        for _ in range(300):
            chosen = [rng.choice(labels) for _ in range(rng.randint(1, 3))]
            command = TARGET + " --flag"
            if rng.random() < 0.4:
                prefix = rng.choice(sorted(PREFIXES))
                chosen = [prefix] + chosen
                command = PREFIXES[prefix](command)
            for label in chosen[(1 if chosen[0] in PREFIXES else 0):]:
                command = WRAPPERS[label](command)
            with self.subTest(chain=chosen):
                names, unresolved = guard.resolve_command(command)
                self.assertTrue(TARGET in names or unresolved, command)

    def test_the_same_wrappers_do_not_turn_a_mention_into_a_match(self) -> None:
        for label, wrap in WRAPPERS.items():
            with self.subTest(wrapper=label):
                self.assertFalse(denied(wrap("echo " + TARGET)))
                self.assertFalse(denied(wrap("grep " + TARGET + " notes.txt")))

    def test_nested_eval_beyond_the_limit_fails_closed(self) -> None:
        command = TARGET
        for _ in range(guard._MAX_DEPTH + 3):
            command = WRAPPERS["eval"](command)
        self.assertTrue(denied(command))

    def test_parsing_never_raises_on_random_garbage(self) -> None:
        rng = random.Random(7)
        alphabet = list("ab ;|&()<>{}!$`'\"\\\n-=") + ["eval ", "sh -c ", "find ", "-exec ", "env -S "]
        for _ in range(500):
            text = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 60)))
            names, unresolved = guard.resolve_command(text)
            self.assertIsInstance(names, list)
            self.assertIsInstance(unresolved, bool)


class TestFailClosedEdges(unittest.TestCase):
    def test_a_quoted_argument_spanning_lines_is_read_not_guessed(self) -> None:
        command = "sh -c 'echo x\n" + TARGET + "'"
        names, unresolved = guard.resolve_command(command)
        self.assertFalse(unresolved)
        self.assertIn(TARGET, names)

    def test_an_unbalanced_quote_is_unresolved_and_denied(self) -> None:
        self.assertTrue(guard.resolve_command("echo 'unterminated")[1])
        self.assertTrue(denied("echo 'unterminated"))

    def test_many_trailing_newlines_do_not_crash_the_matcher(self) -> None:
        # Only one trailing newline is ignored, and the matcher must not recurse.
        many = "git push --force" + "\n" * 5000
        self.assertFalse(guard._resource_matches("*--force", many))
        self.assertTrue(guard._resource_matches("*--force", "git push --force\n"))
        policy = {"id": "p", "action": {"verb": "exec", "resource": "*push*--force*"}, "decision": "deny"}
        self.assertEqual(guard.evaluate([policy], "exec", many)["decision"], "deny")

    def test_a_pathological_wrapper_tree_stops_at_the_step_limit(self) -> None:
        command = "nice " * 7 + "echo hi"
        names, unresolved = guard.resolve_command(command)
        self.assertIsInstance(names, list)
        big = "; ".join(["sudo sudo sudo sudo sudo sudo sudo sudo nice nice nice true"] * 40)
        self.assertTrue(guard.resolve_command(big)[1])

    def test_scan_marks_the_depth_limit_directly(self) -> None:
        state = {"unresolved": False}
        guard._scan("echo hi", guard._MAX_DEPTH + 1, state)
        self.assertTrue(state["unresolved"])

    def test_a_value_over_the_cap_matches_every_pattern(self) -> None:
        self.assertTrue(guard._resource_matches("*never*", "a" * (guard._MAX_COMMAND_CHARS + 1)))

    def test_one_trailing_newline_is_ignored(self) -> None:
        self.assertTrue(guard._resource_matches("*--force", "git push --force\n"))
        self.assertFalse(guard._resource_matches("*--force", "git push --force\nmore"))


class TestShippedBrowserPolicy(unittest.TestCase):
    """The catalog-driven deny policy must keep blocking and keep allowing."""

    def setUp(self) -> None:
        self.catalog = browsers.load_catalog(ROOT)
        entries = self.catalog["browsers"]
        self.allowed = entries[0]
        self.policy = browsers.build_policy(self.catalog, {"primary": self.allowed["id"]})
        self.blocked = [e for e in entries[1:] if e.get("binaries")]
        self.assertTrue(self.blocked, "the catalog must list more than one browser")

    def _exec_policies(self) -> list[dict]:
        return [p for p in self.policy["policies"] if p["action"]["verb"] == "exec"]

    def test_every_blocked_binary_is_denied_through_every_wrapper(self) -> None:
        for entry in self.blocked:
            for binary in entry["binaries"]:
                for label, wrap in WRAPPERS.items():
                    with self.subTest(browser=entry["id"], binary=binary, wrapper=label):
                        decision = guard.evaluate(self._exec_policies(), "exec", wrap(binary + " --flag"))
                        self.assertEqual(decision["decision"], "deny")

    def test_the_selected_browser_is_never_denied(self) -> None:
        for binary in self.allowed["binaries"]:
            for label, wrap in WRAPPERS.items():
                with self.subTest(binary=binary, wrapper=label):
                    decision = guard.evaluate(self._exec_policies(), "exec", wrap(binary + " --flag"))
                    self.assertEqual(decision["decision"], "allow")

    def test_a_mention_of_a_blocked_binary_is_allowed(self) -> None:
        for entry in self.blocked:
            binary = entry["binaries"][0]
            for command in (f"grep {binary} notes.txt", f"echo {binary}", f"cat < {binary}",
                            f"find . -name {binary}", f'git commit -m "{binary}"',
                            f"eval echo {binary}", f"env -S 'echo {binary}'"):
                with self.subTest(browser=entry["id"], command=command):
                    decision = guard.evaluate(self._exec_policies(), "exec", command)
                    self.assertEqual(decision["decision"], "allow")


# Each template puts ``@`` where the shell starts a command, right after a control word.
OPENERS = {
    "then": "if true; then @; fi",
    "else": "if false; then true; else @; fi",
    "elif": "if false; then true; elif true; then @; fi",
    "for do": "for b in a; do @; done",
    "while do": "while true; do @; done",
    "until do": "until false; do @; done",
    "brace group": "{ @; }",
    "negation": "! @",
    "if condition": "if @; then true; fi",
    "while condition": "while @; do true; done",
    "coproc": "coproc @",
}
ASSIGNMENTS = ["X=1 ", "X=1 Y=2 ", "X+=1 ", "arr[0]=1 ", "X=$(true) ", "X=`true` ", 'X="a b" ', "X='a b' "]
GUARD_SCRIPT = ROOT / "scripts" / "coacus_guard.py"


class TestAssignmentAfterAControlWord(unittest.TestCase):
    """A ``NAME=value`` prefix after ``then``, ``do``, ``{`` and the rest never hides the command."""

    def test_the_command_behind_an_assignment_is_always_seen(self) -> None:
        for opener, template in OPENERS.items():
            for assignment in ASSIGNMENTS:
                command = template.replace("@", assignment + TARGET + " --flag")
                with self.subTest(opener=opener, assignment=assignment):
                    names, unresolved = guard.resolve_command(command)
                    self.assertIn(TARGET, names, command)
                    self.assertFalse(unresolved, command)
                    self.assertTrue(denied(command), command)

    def test_an_assignment_alone_is_not_a_command_name(self) -> None:
        for opener, template in OPENERS.items():
            for body in ("t=$(ls)", "t=`ls`", "t=1"):
                command = template.replace("@", body)
                with self.subTest(opener=opener, body=body):
                    names, unresolved = guard.resolve_command(command)
                    self.assertFalse(unresolved, command)
                    self.assertNotIn(body, names)
                    self.assertFalse(denied(command), command)

    def test_the_substitution_inside_an_assignment_is_still_examined(self) -> None:
        for opener, template in OPENERS.items():
            for body in (f"t=$({TARGET})", f"t=`{TARGET}`"):
                command = template.replace("@", body)
                with self.subTest(opener=opener, body=body):
                    self.assertTrue(denied(command), command)

    def test_a_mention_behind_an_assignment_is_not_a_match(self) -> None:
        for opener, template in OPENERS.items():
            for assignment in ASSIGNMENTS:
                command = template.replace("@", assignment + "echo " + TARGET)
                with self.subTest(opener=opener, assignment=assignment):
                    self.assertFalse(denied(command), command)

    def test_several_control_words_in_a_row_are_peeled_in_turn(self) -> None:
        for command in (f"if true; then ! X=1 {TARGET}; fi", f"while true; do {{ X=1 Y=2 {TARGET}; }}; done",
                        f"if true; then ! ! X=1 {TARGET}; fi"):
            with self.subTest(command=command):
                self.assertTrue(denied(command), command)

    def test_the_peeling_loop_always_ends(self) -> None:
        for command in ("then " * 500 + "X=1 " * 500, "X=1 " * 3000, "! " * 3000 + TARGET):
            with self.subTest(size=len(command)):
                names, unresolved = guard.resolve_command(command)
                self.assertIsInstance(names, list)
                self.assertIsInstance(unresolved, bool)


    def test_a_command_variable_after_a_control_word_is_still_scanned(self) -> None:
        # PAGER names a program that git runs, so its value is a command like any other.
        for opener, template in OPENERS.items():
            with self.subTest(opener=opener):
                self.assertTrue(denied(template.replace("@", f"PAGER={TARGET} git log")))
                self.assertTrue(denied(template.replace("@", f"PAGER={TARGET}")))
                self.assertTrue(guard.resolve_command(template.replace("@", "LD_PRELOAD=/x true"))[1])

    def test_a_bare_number_at_the_end_is_not_a_redirection(self) -> None:
        for command in ("if true; then 5; fi", "then 2", "2", "do 7 8"):
            with self.subTest(command=command):
                names, unresolved = guard.resolve_command(command)
                self.assertIsInstance(names, list)
                self.assertFalse(denied(command), command)

    def test_the_depth_limit_still_holds_behind_an_assignment(self) -> None:
        command = "if true; then X=1 " + TARGET + "; fi"
        for _ in range(guard._MAX_DEPTH + 1):
            command = WRAPPERS["sh -c"](command)
        self.assertTrue(denied(command))

    def test_other_shapes_that_put_an_assignment_in_front(self) -> None:
        shapes = (
            f"time X=1 {TARGET}", f"! time X=1 {TARGET}", f"case x in a) X=1 {TARGET};; esac",
            f"case x in (a) X=1 {TARGET};; esac", f"select s in a; do X=1 {TARGET}; done",
            f"if true; then >f X=1 {TARGET}; fi", f"if true; then 2>/dev/null X=1 {TARGET}; fi",
            f"X=1 >f {TARGET}", f"if a; then while b; do X=1 {TARGET}; done; fi",
            f"{{ X=1 {{ X=2 {TARGET}; }}; }}", f"if true; then echo `X=1 {TARGET}`; fi",
            f"if true; then X=1 env {TARGET}; fi", f"if true; then X=1 command {TARGET}; fi",
            f"if true; then X=1 sudo {TARGET}; fi", f"if true; then X=1 \\\n{TARGET}; fi",
        )
        for command in shapes:
            with self.subTest(command=command):
                self.assertTrue(denied(command), command)

    def test_the_redirection_patterns_read_descriptors_and_operators(self) -> None:
        for word in ("{fd}>file", "3>file", ">|file", "<<<word", "<>file", "<<EOF", "<<-EOF", "&>>log", "2>&1"):
            with self.subTest(word=word):
                self.assertTrue(guard._REDIRECT.match(word))
        for word in ("{fd}>", "3>", ">|", "<<<", "<>", "<<", "<<-", "&>>", ">", "<", ">>"):
            with self.subTest(bare=word):
                self.assertTrue(guard._BARE_REDIRECT.match(word))
        for word in ("{fd}>file", ">|file", "<<EOF", "prog", "X=1", "{fd}"):
            with self.subTest(not_bare=word):
                self.assertFalse(guard._BARE_REDIRECT.match(word))

    def test_a_redirection_operator_takes_its_target_with_it(self) -> None:
        redirections = ("<<< word", "<>file", "<> file", ">|file", ">| file", "{fd}>file", "{fd}> file",
                        "2>&1", "&>>log", "<< EOF", "<<-EOF", "<<EOF", ">&2", "<&0")
        for redirection in redirections:
            for template in ("@", "if true; then @; fi", "for b in a; do @; done"):
                for assignment in ("", "X=1 "):
                    command = template.replace("@", f"{redirection} {assignment}{TARGET} --flag")
                    with self.subTest(command=command):
                        names, _ = guard.resolve_command(command)
                        self.assertIn(TARGET, names, command)
                        self.assertTrue(denied(command), command)
                    mention = template.replace("@", f"{redirection} {assignment}echo {TARGET}")
                    with self.subTest(command=mention):
                        self.assertFalse(denied(mention), mention)


class TestShippedBrowserPolicyWithAssignments(unittest.TestCase):
    """The real catalog policy, which is what a user hits, handles loops with assignments."""

    def setUp(self) -> None:
        catalog = browsers.load_catalog(ROOT)
        entries = catalog["browsers"]
        policy = browsers.build_policy(catalog, {"primary": entries[0]["id"]})
        self.policies = [p for p in policy["policies"] if p["action"]["verb"] == "exec"]
        self.blocked = next(e for e in entries[1:] if e.get("binaries"))["binaries"][0]

    def test_a_loop_that_only_assigns_is_allowed(self) -> None:
        for command in ("for b in a; do t=$(ls); done",
                        "if true; then t=$(git rev-parse HEAD); echo $t; fi",
                        "while true; do t=`date`; break; done"):
            with self.subTest(command=command):
                self.assertEqual(guard.evaluate(self.policies, "exec", command)["decision"], "allow")

    def test_a_blocked_browser_behind_an_assignment_is_denied(self) -> None:
        for command in (f"if true; then X=1 {self.blocked} --flag; fi", f"for b in a; do X=1 {self.blocked}; done",
                        f"{{ X=1 {self.blocked}; }}", f"! X=1 {self.blocked}"):
            with self.subTest(command=command):
                self.assertEqual(guard.evaluate(self.policies, "exec", command)["decision"], "deny")


class TestUnresolvedCommandIsNamedAsSuch(unittest.TestCase):
    """A command the walk cannot read is held under the rule, but the reason says so."""

    UNREADABLE = "echo 'unterminated"

    def test_evaluate_marks_only_a_hold_that_no_name_explains(self) -> None:
        held = guard.evaluate([POLICY], "exec", self.UNREADABLE)
        self.assertEqual(held["decision"], "deny")
        self.assertTrue(held.get("unresolved"))
        real = guard.evaluate([POLICY], "exec", TARGET + " --flag")
        self.assertEqual(real["decision"], "deny")
        self.assertNotIn("unresolved", real)
        mixed = guard.evaluate([POLICY], "exec", TARGET + " --flag; eval \"$x\"")
        self.assertEqual(mixed["decision"], "deny")
        self.assertNotIn("unresolved", mixed)
        self.assertNotIn("unresolved", guard.evaluate([POLICY], "exec", "ls"))

    def test_a_text_policy_that_really_matches_is_never_marked(self) -> None:
        text = {"id": "no-unterminated", "action": {"verb": "exec", "resource": "*unterminated*"},
                "decision": "deny"}
        self.assertEqual(guard.evaluate([text], "exec", self.UNREADABLE)["decision"], "deny")
        self.assertNotIn("unresolved", guard.evaluate([text], "exec", self.UNREADABLE))

    def test_one_rule_that_really_matches_keeps_the_hold_unmarked(self) -> None:
        text = {"id": "no-unterminated", "action": {"verb": "exec", "resource": "*unterminated*"},
                "decision": "deny"}
        for policies in ([POLICY, text], [text, POLICY]):
            with self.subTest(order=[p["id"] for p in policies]):
                result = guard.evaluate(policies, "exec", self.UNREADABLE)
                self.assertEqual(result["decision"], "deny")
                self.assertNotIn("unresolved", result)

    def test_an_ask_hold_is_marked_too(self) -> None:
        asking = dict(POLICY, decision="ask")
        result = guard.evaluate([asking], "exec", self.UNREADABLE)
        self.assertEqual((result["decision"], result.get("unresolved")), ("ask", True))
        self.assertNotIn("unresolved", guard.evaluate([asking], "exec", TARGET))

    def test_the_mark_never_changes_the_decision(self) -> None:
        expected = {self.UNREADABLE: True, TARGET: True, "ls": False, "$X run": True}
        for decision in ("deny", "ask"):
            policy = dict(POLICY, decision=decision)
            for command, held in expected.items():
                with self.subTest(decision=decision, command=command):
                    result = guard.evaluate([policy], "exec", command)
                    self.assertEqual(result["decision"], decision if held else "allow")

    def _run_guard(self, command: str, **policy_fields) -> dict:
        env = {k: v for k, v in os.environ.items() if k not in ("CI", "COACUS_GUARD_ASK", "COACUS_GUARD_NO_ASK")}
        with tempfile.TemporaryDirectory() as directory:
            policy = dict(POLICY, message="Policy text that must not be blamed.", **policy_fields)
            Path(directory, "t.policy.json").write_text(
                json.dumps({"schema": 1, "enabled": True, "policies": [policy]}), encoding="utf-8")
            payload = {"hook_event_name": "PreToolUse", "tool_name": "Bash", "tool_input": {"command": command}}
            run = subprocess.run(
                [sys.executable, "-I", str(GUARD_SCRIPT), "--harness", "claude-code", "--event", "tool.pre",
                 "--root", str(ROOT)],
                input=json.dumps(payload), capture_output=True, text=True, timeout=60,
                env=dict(env, COACUS_POLICY_DIR=directory))
        self.assertEqual(run.returncode, 0, run.stderr)
        return json.loads(run.stdout)

    def test_the_guard_names_the_cause_and_the_rule_for_an_unreadable_command(self) -> None:
        out = self._run_guard(self.UNREADABLE)["hookSpecificOutput"]
        self.assertEqual(out.get("hookEventName"), "PreToolUse")
        self.assertEqual(out.get("permissionDecision"), "deny")
        reason = out.get("permissionDecisionReason", "")
        self.assertIn("could not tell", reason)
        self.assertIn(POLICY["id"], reason)
        self.assertNotIn("must not be blamed", reason)

    def test_an_ask_rule_degrades_to_a_denial_that_names_the_cause(self) -> None:
        out = self._run_guard(self.UNREADABLE, decision="ask")["hookSpecificOutput"]
        self.assertEqual(out.get("permissionDecision"), "deny")
        self.assertIn("could not tell", out.get("permissionDecisionReason", ""))

    def test_the_guard_keeps_the_rule_message_for_a_real_match(self) -> None:
        out = self._run_guard("if true; then X=1 " + TARGET + "; fi")["hookSpecificOutput"]
        self.assertEqual(out.get("permissionDecision"), "deny")
        self.assertEqual(out.get("permissionDecisionReason"), "Policy text that must not be blamed.")

    def test_the_guard_allows_a_loop_that_only_assigns(self) -> None:
        self.assertEqual(self._run_guard("for b in a; do t=$(ls); done"), {})


if __name__ == "__main__":
    unittest.main()
