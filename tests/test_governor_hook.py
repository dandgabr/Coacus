"""Run the Antigravity Python hook against its real isolated ledger."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from engine.governor.ledger import Ledger


ROOT = Path(__file__).resolve().parents[1]


class TestGovernorHook(unittest.TestCase):
    def test_acquires_releases_and_parks_slots(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            env = dict(os.environ, GOVERNOR_STATE_DIR=tmp, ORCH_MAX_CONCURRENT="3")
            payload = {"toolCall": {"name": "invoke_subagent"}, "conversationId": "test", "stepIdx": 0}
            def run(mode: str) -> dict:
                result = subprocess.run(
                    [sys.executable, str(ROOT / "scripts/coacus_governor_hook.py"), mode],
                    input=json.dumps(payload), text=True, capture_output=True, env=env, check=True,
                )
                return json.loads(result.stdout)
            ledger = Ledger(Path(tmp), max_total=3)
            self.assertEqual(run("pretool"), {})
            self.assertEqual(ledger.status()["running"], 1)
            self.assertEqual(run("posttool"), {})
            self.assertEqual(ledger.status()["running"], 0)
            run("pretool")
            payload["error"] = "HTTP 429 Too Many Requests"
            self.assertIn("ephemeralMessage", run("posttool"))
            self.assertEqual(ledger.status()["running"], 0)
            self.assertEqual(ledger.status()["paused"], 1)
            self.assertIn("paused=1", run("preinv")["injectSteps"][0]["ephemeralMessage"])


if __name__ == "__main__":
    unittest.main()
