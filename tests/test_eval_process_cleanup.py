import os
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

from scripts import coacus_eval


class ProcessCleanupTests(unittest.TestCase):
    @unittest.skipUnless(os.name == 'posix', 'requires POSIX process groups')
    def test_successful_parent_cleans_up_redirected_descendant(self):
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / 'survived'
            child = f'import time; from pathlib import Path; time.sleep(1); Path({str(marker)!r}).touch()'
            parent = ('import subprocess, sys; '
                      f'subprocess.Popen([sys.executable, "-c", {child!r}], '
                      'stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); '
                      'print("ok")')
            result = coacus_eval._bounded_run([sys.executable, '-c', parent], 5)
            self.assertEqual((result[0].strip(), result[3]), ('ok', None))
            time.sleep(1.2)
            self.assertFalse(marker.exists())

    @unittest.skipUnless(os.name == 'posix', 'requires POSIX process groups')
    def test_keyboard_interrupt_terminates_and_reaps_process(self):
        processes = []
        popen = coacus_eval.subprocess.Popen

        def start(*args, **kwargs):
            proc = popen(*args, **kwargs)
            processes.append(proc)
            return proc

        with mock.patch.object(coacus_eval.subprocess, 'Popen', side_effect=start), \
             mock.patch.object(coacus_eval.time, 'sleep', side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                coacus_eval._bounded_run([sys.executable, '-c', 'import time; time.sleep(30)'], 5)
        try:
            self.assertIsNotNone(processes[0].poll())
        finally:
            if processes[0].poll() is None:
                os.killpg(processes[0].pid, 9)
                processes[0].wait()

    def test_non_executable_harness_reports_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            executable = Path(directory) / 'runner'
            executable.write_text('not executable', encoding='utf-8')
            executable.chmod(0o644)
            transcript, status = coacus_eval._run_harness(
                {'harness': 'test', 'prompt': ''}, 5, {'test': [str(executable)]})
        self.assertEqual(transcript, '')
        self.assertEqual(status, 'RUNNER_ERROR (PermissionError)')

    def test_unsupported_platform_returns_explicit_status(self):
        with mock.patch.object(coacus_eval.os, 'name', 'nt'):
            result = coacus_eval._run_harness({'harness': 'test', 'prompt': ''}, 5, {'test': [sys.executable]})
        self.assertEqual(result, ('', 'UNSUPPORTED_PLATFORM'))

    def test_unsupported_platform_reported_by_strict_judge(self):
        with mock.patch.object(coacus_eval.os, 'name', 'nt'):
            result = coacus_eval._strict_judge({'rubric': ['rule']}, 'ok', 'judge', False, {})
        self.assertFalse(result['passed'])
        self.assertIn('UNSUPPORTED_PLATFORM', result['verdict'])
