"""Regression tests for alarm preservation on failed improvement runs."""

import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from engine.improve import loop


class TestErrorAlarms(unittest.TestCase):
    @unittest.skipUnless(os.name == "posix" and hasattr(os, "O_NONBLOCK") and hasattr(os, "O_NOFOLLOW"), "requires secure POSIX source processing")
    def test_failures_preserve_computed_alarms(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "session.jsonl"
            source.write_text(
                '{"channel":"human-user-turn","session_id":"a","text":"review insight"}\n'
                '{"channel":"human-user-turn","session_id":"b","text":"review insight"}\n',
                encoding="utf-8",
            )
            cases = (
                ("read", {"transcript": str(root / "missing")}, "source unavailable or invalid"),
                ("association", {"transcript": str(source)}, "private source association unavailable"),
                ("publication", {"transcript": str(source)}, "proposal publication incomplete"),
            )
            for phase, options, reason in cases:
                with self.subTest(phase=phase), patch.object(loop, "_alarm_for", return_value=["degraded"]):
                    target = "_save_source" if phase == "association" else "append_runtime"
                    owner = loop if phase == "association" else loop.ledger
                    with patch.object(owner, target, side_effect=OSError("failure")):
                        result = loop.run(root, options)
                    self.assertFalse(result["ok"])
                    self.assertEqual(result["reason"], reason)
                    self.assertEqual(result["alarms"], ["degraded"])


    def test_unsupported_platform_refuses_source_and_preserves_alarms(self):
        with tempfile.TemporaryDirectory() as tmp, \
                patch.object(loop, "os", SimpleNamespace(name="unsupported")), \
                patch.object(loop, "_alarm_for", return_value=["degraded"]):
            result = loop.run(Path(tmp), {"transcript": "source.jsonl"})
        self.assertFalse(result["ok"])
        self.assertEqual(result["reason"], "source processing unavailable on unsupported platform")
        self.assertEqual(result["alarms"], ["degraded"])
        self.assertEqual(result["proposals"], [])


if __name__ == "__main__":
    unittest.main()
