"""Custom source failures must not disclose exception contents."""

import os
import tempfile
import unittest
from pathlib import Path

from engine.improve import loop, sources


class CustomSource:
    def __init__(self, name, *, status_error=False, read_error=False):
        self.name = name
        self.status_error = status_error
        self.read_error = read_error

    def status(self, root):
        if self.status_error:
            raise RuntimeError("sensitive-status-detail")
        return "present"

    def read(self, root, options):
        if self.read_error:
            raise RuntimeError("sensitive-read-detail")
        return []


class CustomSourceErrors(unittest.TestCase):
    def test_status_failure_selected_and_unselected(self):
        for selected in (True, False):
            with self.subTest(selected=selected), tempfile.TemporaryDirectory() as tmp:
                registry = sources.SourceRegistry()
                registry.register(CustomSource("broken", status_error=True))
                registry.register(CustomSource("healthy"))
                result = loop.run(Path(tmp), {"source": "broken" if selected else "healthy"}, registry)
                self.assertEqual(result["ok"], not selected)
                self.assertTrue(any("broken" in alarm for alarm in result["alarms"]))
                self.assertNotIn("sensitive-status-detail", str(result))
                self.assertEqual(result["proposals"], [])

    @unittest.skipUnless(os.name == "posix", "custom sources require private storage")
    def test_selected_read_failure_preserves_other_source_alarm(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = sources.SourceRegistry()
            registry.register(CustomSource("broken", status_error=True))
            registry.register(CustomSource("selected", read_error=True))
            result = loop.run(Path(tmp), {"source": "selected"}, registry)
            self.assertFalse(result["ok"])
            self.assertTrue(any("broken" in alarm for alarm in result["alarms"]))
            self.assertNotIn("sensitive-read-detail", str(result))
            self.assertEqual(result["proposals"], [])


if __name__ == "__main__":
    unittest.main()
