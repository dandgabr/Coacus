"""Shell constructs and the shipped browser policy under command deny rules.

Two guarantees: a construct that wraps a blocked command never hides it, and a
mere mention of a name never matches. The browser policy is the only shipped
user of ``"match": "command"``, so it is exercised through the real catalog.
"""

from __future__ import annotations

import random
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


if __name__ == "__main__":
    unittest.main()
