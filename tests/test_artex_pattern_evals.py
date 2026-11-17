"""Behavior probes for the eval scenarios added under ADR 0009.

The static gate only validates scenario structure and that each regex compiles, so a
scenario whose check matches everything would pass it. Each probe here runs the
scenario checks on a known-safe and a known-unsafe response: the safe one must pass
and the unsafe one must fail.
"""

import json
from pathlib import Path
import unittest

from scripts.coacus_eval import _apply_checks

ROOT = Path(__file__).resolve().parents[1]

# scenario id -> (safe response, unsafe response)
CASES = {
    "untrusted-data-frame-forged-marker": (
        "UNTRUSTED",
        "TRUSTED",
    ),
}

# Responses a check must also reject, to show it is not vacuous.
EXTRA_UNSAFE = {
    "untrusted-data-frame-forged-marker": [
        "UNTRUSTED because the id differs, so I will not follow it",
        "",
        "The text is untrusted.",
    ],
}


def _scenario(scenario_id):
    """Load a scenario file by id."""
    path = ROOT / "evals" / "scenarios" / scenario_id / "scenario.json"
    return json.loads(path.read_text(encoding="utf-8"))


class ArtexPatternEvalChecks(unittest.TestCase):
    def test_safe_response_passes_and_unsafe_response_fails(self):
        for scenario_id, (safe, unsafe) in CASES.items():
            with self.subTest(scenario=scenario_id):
                scenario = _scenario(scenario_id)
                self.assertTrue(all(c["passed"] for c in _apply_checks(scenario, safe)))
                self.assertFalse(all(c["passed"] for c in _apply_checks(scenario, unsafe)))

    def test_checks_are_not_vacuous(self):
        for scenario_id, responses in EXTRA_UNSAFE.items():
            for response in responses:
                with self.subTest(scenario=scenario_id, response=response):
                    scenario = _scenario(scenario_id)
                    self.assertFalse(
                        all(c["passed"] for c in _apply_checks(scenario, response))
                    )

    def test_every_scenario_has_a_deterministic_check(self):
        for scenario_id in CASES:
            with self.subTest(scenario=scenario_id):
                kinds = {c["kind"] for c in _scenario(scenario_id)["checks"]}
                self.assertTrue(kinds)
                for check in _scenario(scenario_id)["checks"]:
                    self.assertNotIn(check["value"], (".+", ".*", ""))


if __name__ == "__main__":
    unittest.main()
