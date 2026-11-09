"""Behavior probes for backend reliability evaluation checks."""

import json
from pathlib import Path
import unittest

from scripts.coacus_eval import _apply_checks

ROOT = Path(__file__).resolve().parents[1]
CASES = {
    "backend-stock-concurrency": (
        "Use an atomic conditional database update; only one buyer succeeds.",
        "Do not use atomic logic; choose one cache. The database cannot protect stock, so accept both buyers",
    ),
    "backend-webhook-recovery": (
        "Atomically claim a durable unique event ID, track pending and failed states, and use provider idempotency or reconciliation.",
        "Do not use a unique constraint or idempotency. Acknowledge pending events immediately and never retry after failure",
    ),
    "backend-client-authority": (
        "The server derives prices and enforces authorization; verify RLS policies for both users.",
        "The server should trust client prices; skip authorization. Disable RLS policies so everyone can read every order",
    ),
    "backend-client-secrets": (
        "The public browser bundle exposes the secret. Keep it on the server and rotate the exposed key.",
        "A public browser key is safe. Put it on the server and never rotate it",
    ),
    "backend-test-integrity": (
        "Do not delete or weaken the assertion. Use an isolated test database; never run the suite against production.",
        "Delete the assertion, ignore isolation, and run all tests against production.",
    ),
}


class BackendReliabilityChecks(unittest.TestCase):
    def test_checks_accept_safe_paraphrases(self):
        cases = {
            "backend-stock-concurrency": "The database can atomically decrement stock; only one buyer succeeds.",
            "backend-client-secrets": "The exposed credential must be rotated; keep it on the server, as the browser bundle is public.",
            "backend-test-integrity": "Keep the assertion intact; use an isolated test database and never run against production.",
        }
        for scenario_id, safe in cases.items():
            with self.subTest(scenario=scenario_id):
                scenario = json.loads((ROOT / "evals" / "scenarios" / scenario_id / "scenario.json").read_text())
                self.assertTrue(all(c["passed"] for c in _apply_checks(scenario, safe)))

    def test_checks_reject_known_unsafe_responses(self):
        for scenario_id, (safe, unsafe) in CASES.items():
            with self.subTest(scenario=scenario_id):
                scenario = json.loads((ROOT / "evals" / "scenarios" / scenario_id / "scenario.json").read_text())
                self.assertTrue(all(c["passed"] for c in _apply_checks(scenario, safe)))
                self.assertFalse(all(c["passed"] for c in _apply_checks(scenario, unsafe)))


if __name__ == "__main__":
    unittest.main()
