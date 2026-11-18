"""The evaluator must fail closed: a hard input may never turn into an allow."""

from __future__ import annotations

import time
import unittest

from engine.guardrail import evaluate as guard

TARGET = "blockedbin"
COMMAND_DENY = {
    "id": "no-blockedbin",
    "action": {"verb": "exec", "resource": TARGET, "match": "command"},
    "decision": "deny",
    "message": "blocked",
}


def nested_shell(depth: int, inner: str) -> str:
    """Wrap ``inner`` in ``depth`` levels of ``sh -c`` with growing quotes."""
    command = inner
    for _ in range(depth):
        command = "sh -c " + "'" + command.replace("'", "'\\''") + "'"
    return command


class TestResourceMatchingIsBounded(unittest.TestCase):
    def test_hostile_glob_returns_quickly(self) -> None:
        start = time.monotonic()
        self.assertFalse(guard._resource_matches("*a*a*a*a*a*a*a*b*", "a" * 4000))
        self.assertLess(time.monotonic() - start, 5.0)

    def test_star_matching_keeps_its_meaning(self) -> None:
        cases = [
            ("git push*--force*", "git push origin --force", True),
            ("git push*--force*", "git push origin", False),
            ("*.env", "repo/.env", True),
            ("a*b*c", "a--b--c", True),
            ("a*b*c", "a--b--d", False),
            ("literal[1]*", "literal[1] tail", True),
        ]
        for pattern, value, expected in cases:
            with self.subTest(pattern=pattern, value=value):
                self.assertEqual(guard._resource_matches(pattern, value), expected)
                self.assertEqual(guard._star_match(pattern, value) if "*" in pattern else True,
                                 expected if "*" in pattern else True)

    def test_star_match_agrees_with_a_regex_oracle_on_small_inputs(self) -> None:
        import itertools
        import re
        alphabet = "ab*"
        for plen in range(0, 5):
            for pattern in map("".join, itertools.product(alphabet, repeat=plen)):
                regex = re.compile("(?s)" + ".*".join(map(re.escape, pattern.split("*"))) + r"\Z")
                for vlen in range(0, 5):
                    for value in map("".join, itertools.product("ab", repeat=vlen)):
                        self.assertEqual(guard._star_match(pattern, value), bool(regex.match(value)),
                                         (pattern, value))


class TestUnresolvedCommandsFailClosed(unittest.TestCase):
    def _decision(self, command: str) -> str:
        return guard.evaluate([COMMAND_DENY], "exec", command)["decision"]

    def test_moderate_nesting_is_still_resolved(self) -> None:
        self.assertEqual(self._decision(nested_shell(3, TARGET)), "deny")
        self.assertEqual(self._decision(nested_shell(3, "echo hi")), "allow")

    def test_nesting_beyond_the_limit_is_denied(self) -> None:
        deep = nested_shell(guard._MAX_DEPTH + 3, "echo hi")
        names, unresolved = guard.resolve_command(deep)
        self.assertTrue(unresolved)
        self.assertEqual(self._decision(deep), "deny")

    def test_long_wrapper_chain_beyond_the_limit_is_denied(self) -> None:
        chain = " ".join(["nice"] * (guard._MAX_DEPTH + 3)) + " echo hi"
        self.assertEqual(self._decision(chain), "deny")

    def test_oversize_command_is_denied(self) -> None:
        huge = "echo " + "a" * (guard._MAX_COMMAND_CHARS + 1)
        self.assertEqual(self._decision(huge), "deny")

    def test_resolvable_commands_are_not_marked_unresolved(self) -> None:
        for command in ("echo hi", f"sudo -u root {TARGET}", "", "   "):
            with self.subTest(command=command):
                self.assertFalse(guard.resolve_command(command)[1])

    def test_policies_without_command_match_are_not_affected(self) -> None:
        plain = {"id": "p", "action": {"verb": "exec", "resource": "*rm -rf*"}, "decision": "deny"}
        deep = nested_shell(guard._MAX_DEPTH + 3, "echo hi")
        self.assertEqual(guard.evaluate([plain], "exec", deep)["decision"], "allow")

    def test_command_candidates_never_raises_on_odd_input(self) -> None:
        for command in ("'", '"', "$(", "`", "$(" * 50, ";" * 1000, "\x00", "a" * 10):
            with self.subTest(command=command[:10]):
                self.assertIsInstance(guard.command_candidates(command), list)


class TestUnknownDecisionsDeny(unittest.TestCase):
    def test_misspelled_or_unknown_decisions_deny(self) -> None:
        for decision in ("Deny", "block", "", "DENY ", "permit"):
            with self.subTest(decision=decision):
                policy = {"id": "p", "action": {"verb": "read", "resource": "*.env"}, "decision": decision}
                self.assertEqual(guard.evaluate([policy], "read", "repo/.env")["decision"], "deny")

    def test_known_decisions_keep_their_rank(self) -> None:
        for decision in ("allow", "deny", "ask"):
            with self.subTest(decision=decision):
                policy = {"id": "p", "action": {"verb": "read", "resource": "*.env"}, "decision": decision}
                self.assertEqual(guard.evaluate([policy], "read", "repo/.env")["decision"], decision)


if __name__ == "__main__":
    unittest.main()
