"""Two ask policies on the same action must not depend on file order."""

from __future__ import annotations

import itertools
import unittest

from engine.guardrail import evaluate as guard


def ask(policy_id: str, fallback, resource: str = "*.env") -> dict:
    policy = {"id": policy_id, "action": {"verb": "read", "resource": resource},
              "decision": "ask", "message": f"message {policy_id}"}
    if fallback is not None:
        policy["on_ask_unavailable"] = fallback
    return policy


def decide(policies: list[dict]) -> dict:
    return guard.evaluate(policies, "read", "repo/.env")


class TestAskFallbackPrecedence(unittest.TestCase):
    def test_deny_fallback_wins_in_both_orders(self) -> None:
        permissive, strict = ask("p-allow", "allow"), ask("p-deny", "deny")
        for order in itertools.permutations([permissive, strict]):
            with self.subTest(order=[p["id"] for p in order]):
                result = decide(list(order))
                self.assertEqual(result["decision"], "ask")
                self.assertEqual(result["on_ask_unavailable"], "deny")
                self.assertEqual(result["policy_id"], "p-deny")
                self.assertEqual(result["message"], "message p-deny")

    def test_allow_only_when_every_matching_ask_allows(self) -> None:
        for order in itertools.permutations([ask("a", "allow"), ask("b", "allow")]):
            result = decide(list(order))
            self.assertEqual(result["on_ask_unavailable"], "allow")
            self.assertEqual(result["policy_id"], order[0]["id"])

    def test_missing_or_invalid_fallback_counts_as_deny(self) -> None:
        for bad in (None, "ask", "note", "Deny", "", 5):
            for order in itertools.permutations([ask("p-allow", "allow"), ask("p-bad", bad)]):
                with self.subTest(bad=bad, order=[p["id"] for p in order]):
                    self.assertEqual(decide(list(order))["on_ask_unavailable"], "deny")

    def test_a_non_matching_ask_policy_does_not_count(self) -> None:
        result = decide([ask("p-allow", "allow"), ask("other", "deny", resource="*.pem")])
        self.assertEqual(result["on_ask_unavailable"], "allow")
        self.assertEqual(result["policy_id"], "p-allow")

    def test_a_winning_deny_ignores_ask_fallbacks(self) -> None:
        deny = {"id": "hard", "action": {"verb": "read", "resource": "*.env"},
                "decision": "deny", "message": "no"}
        for order in itertools.permutations([ask("p-allow", "allow"), deny]):
            result = decide(list(order))
            self.assertEqual(result["decision"], "deny")
            self.assertEqual(result["policy_id"], "hard")

    def test_a_single_ask_policy_keeps_its_own_fallback(self) -> None:
        self.assertEqual(decide([ask("only", "allow")])["on_ask_unavailable"], "allow")
        self.assertEqual(decide([ask("only", "deny")])["on_ask_unavailable"], "deny")


if __name__ == "__main__":
    unittest.main()
