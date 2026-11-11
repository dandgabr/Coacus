"""Reject invalid Unicode in source observations without exposing their contents."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from engine.improve import loop


class TestSurrogateRegression(unittest.TestCase):
    def test_isolated_surrogate_is_controlled_and_preserves_alarms(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "session.jsonl"
            source.write_text('{"text":"private-marker \\ud800"}\n', encoding="utf-8")
            with patch.object(loop, "_alarm_for", return_value=["degraded"]):
                result = loop.run(root, {"transcript": str(source)})
        self.assertEqual(result, {"ok": False, "reason": "source unavailable or invalid", "alarms": ["degraded"], "proposals": []})


if __name__ == "__main__":
    unittest.main()
