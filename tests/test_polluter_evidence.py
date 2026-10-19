"""The diagnostic must distinguish an inconclusive run from a clean run."""
import contextlib
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('polluter', ROOT / 'methodology/workflows/superpowers-systematic-debugging/find_polluter.py')
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class PolluterEvidenceTests(unittest.TestCase):
    def invoke(self, root, runner):
        with patch.object(MODULE.subprocess, 'run', runner), contextlib.redirect_stdout(io.StringIO()) as output:
            result = MODULE.main([str(root / 'pollution'), str(root / '*.test')])
        return result, output.getvalue()

    def test_no_matches_is_inconclusive(self):
        with tempfile.TemporaryDirectory() as tmp:
            result, output = self.invoke(Path(tmp), lambda *a, **k: None)
            self.assertEqual(result, 2)
            self.assertIn('inconclusive', output.lower())

    def test_preexisting_pollution_never_claims_clean(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'a.test').touch()
            (root / 'pollution').touch()
            def forbidden(*a, **k):
                self.fail('runner must not execute against preexisting pollution')
            result, output = self.invoke(root, forbidden)
            self.assertEqual(result, 2)
            self.assertIn('executed=0', output)

    def test_runner_failure_is_inconclusive(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'a.test').touch()
            result, output = self.invoke(root, lambda *a, **k: type('Result', (), {'returncode': 7})())
            self.assertEqual(result, 2)
            self.assertIn('failed=1', output)

    def test_clean_and_polluting_runs_are_distinct(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'a.test').touch()
            ok = type('Result', (), {'returncode': 0})()
            result, output = self.invoke(root, lambda *a, **k: ok)
            self.assertEqual(result, 0)
            self.assertIn('executed=1', output)
            def pollute(*a, **k):
                (root / 'pollution').touch()
                return ok
            result, output = self.invoke(root, pollute)
            self.assertEqual(result, 1)
            self.assertIn('FOUND POLLUTER', output)
