"""Tests for the concurrency governor (D6/ADR-0007)."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path

from engine.governor.ledger import Ledger

ROOT = Path(__file__).resolve().parents[1]


class TestGovernor(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.dir = Path(self._tmp.name)

    def test_acquire_release_roundtrip(self) -> None:
        ledger = Ledger(self.dir, max_total=2)
        self.assertIsNotNone(ledger.acquire("a"))
        self.assertEqual(ledger.status()["running"], 1)
        ledger.release("a")
        self.assertEqual(ledger.status()["running"], 0)

    def test_acquire_is_idempotent_per_exact_caller(self) -> None:
        ledger = Ledger(self.dir, max_total=2)
        self.assertEqual(ledger.acquire("a"), ledger.acquire("a"))
        self.assertEqual(ledger.status()["running"], 1)

    def test_prefix_callers_are_distinct(self) -> None:
        # Regression: "a" must not match the row of "a b".
        ledger = Ledger(self.dir, max_total=3)
        ledger.acquire("a")
        ledger.acquire("a-b")
        ledger.release("a")
        status = ledger.status()
        self.assertEqual(status["running"], 1)
        self.assertIn("a-b", status["ledger"][0])

    def test_cap_is_never_exceeded_and_matches_exactly(self) -> None:
        ledger = Ledger(self.dir, max_total=3)
        acquired = [ledger.acquire(name) for name in ("a", "b", "c")]
        self.assertTrue(all(acquired))
        self.assertIsNone(ledger.acquire("d", timeout=0.3))
        self.assertEqual(ledger.status()["running"], 3)

    def test_timeout_does_not_leak_a_slot(self) -> None:
        ledger = Ledger(self.dir, max_total=1)
        ledger.acquire("a")
        self.assertIsNone(ledger.acquire("b", timeout=0.2))
        self.assertEqual(ledger.status()["running"], 1)

    def test_blocked_acquirer_proceeds_after_release(self) -> None:
        ledger = Ledger(self.dir, max_total=1)
        ledger.acquire("a")
        result: dict = {}

        def waiter() -> None:
            result["token"] = ledger.acquire("b", timeout=5)

        thread = threading.Thread(target=waiter)
        thread.start()
        time.sleep(0.4)
        ledger.release("a")
        thread.join(timeout=5)
        self.assertIsNotNone(result.get("token"))

    def test_fail_is_idempotent_and_frees_slot(self) -> None:
        ledger = Ledger(self.dir, max_total=1)
        ledger.acquire("a")
        ledger.fail("a")
        ledger.fail("a")  # second call must not duplicate the PAUSED row
        status = ledger.status()
        self.assertEqual(status["running"], 0)
        self.assertEqual(status["paused"], 1)
        self.assertEqual(len(ledger.paused()), 1)

    def test_fail_on_unknown_caller_creates_no_paused_row(self) -> None:
        ledger = Ledger(self.dir, max_total=2)
        ledger.fail("ghost")
        self.assertEqual(ledger.status()["paused"], 0)

    def test_paused_reports_backoff(self) -> None:
        ledger = Ledger(self.dir, max_total=2)
        ledger.acquire("a")
        ledger.fail("a")
        row = ledger.paused()[0]
        self.assertEqual(row["caller"], "a")
        self.assertGreaterEqual(row["retry_after_s"], 2)

    def test_stale_slot_beyond_lease_is_reaped(self) -> None:
        import time as _time

        ledger = Ledger(self.dir, max_total=1, lease_seconds=1)
        # Forge a RUNNING row that started well past the lease.
        old = int(_time.time()) - 3600
        ledger.path.write_text(
            f"MAX 1\nRUNNING crashed no tok 999999 {old}\n", encoding="utf-8"
        )
        # The expired holder must not block a real acquirer.
        self.assertIsNotNone(ledger.acquire("live", timeout=0.5))
        self.assertEqual(ledger.status()["running"], 1)

    def test_cap_cannot_be_raised_by_a_later_caller(self) -> None:
        Ledger(self.dir, max_total=2).acquire("a")  # persists MAX 2
        greedy = Ledger(self.dir, max_total=100)
        self.assertEqual(greedy.status()["max"], 2)
        greedy.acquire("b")
        self.assertIsNone(greedy.acquire("c", timeout=0.2))

    def test_invalid_caller_is_rejected(self) -> None:
        ledger = Ledger(self.dir, max_total=2)
        with self.assertRaises(ValueError):
            ledger.acquire("bad caller\nRUNNING evil no t 1 1")

    def test_reset_clears_ledger(self) -> None:
        ledger = Ledger(self.dir, max_total=2)
        ledger.acquire("a")
        ledger.reset()
        self.assertEqual(ledger.status()["running"], 0)

    def test_orchestrator_flag_is_recorded(self) -> None:
        ledger = Ledger(self.dir, max_total=5)
        ledger.acquire("orch", orchestrator=True)
        self.assertTrue(ledger.status()["orchestrator_present"])


class TestGovernorCrossProcess(unittest.TestCase):
    """flock is per open-file-description, so cross-process is the real contract."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.dir = Path(self._tmp.name)

    def test_multi_process_cap(self) -> None:
        # 6 independent processes race for a cap of 3 and HOLD their slots.
        # Assert the peak observed concurrency never exceeds the cap.
        import json

        child = (
            "import sys, time, os; sys.path.insert(0, '.'); "
            "from engine.governor.ledger import Ledger; "
            "t = Ledger().acquire(sys.argv[1], timeout=2); "
            "print('TOKEN' if t else 'FULL', flush=True); "
            "time.sleep(6) if t else None"
        )
        child_env = {
            "GOVERNOR_STATE_DIR": str(self.dir),
            "ORCH_MAX_CONCURRENT": "3",
            "PATH": "/usr/bin:/bin",
        }
        procs = [
            subprocess.Popen(
                [sys.executable, "-c", child, f"p{i}"],
                cwd=ROOT,
                env=child_env,
                stdout=subprocess.PIPE,
                text=True,
            )
            for i in range(6)
        ]
        # Sample the ledger while the children hold their slots.
        ledger = Ledger(self.dir, max_total=3)
        peak = 0
        for _ in range(25):
            time.sleep(0.15)
            peak = max(peak, ledger.status()["running"])
        holders = 0
        for proc in procs:
            out, _ = proc.communicate(timeout=15)
            if out.strip() == "TOKEN":
                holders += 1
        self.assertLessEqual(peak, 3, f"peak concurrency {peak} exceeded cap")
        self.assertEqual(holders, 3, "exactly the cap should acquire, the rest wait")


if __name__ == "__main__":
    unittest.main()
