import os
import shlex
import tempfile
from pathlib import Path
import sys
import time
import unittest

from scripts import coacus_eval


def command(code):
    return [sys.executable, '-c', code]


class OutputLimitsTests(unittest.TestCase):
    def test_invalid_timeouts_rejected(self):
        for value in (float('nan'), float('inf'), -1.0, 0.0):
            with self.subTest(value=value), self.assertRaises(ValueError):
                coacus_eval._bounded_run(command('pass'), value)
        for value in ('nan', 'inf', '-1', '0'):
            with self.subTest(value=value), self.assertRaises(SystemExit):
                coacus_eval.main(['validate', '--timeout', value])

    @unittest.skipUnless(os.name == 'posix', 'requires POSIX process groups')
    def test_descendant_killed_after_parent_exits_with_inherited_pipe(self):
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / 'survived'
            child = f'import time; from pathlib import Path; time.sleep(1); Path({str(marker)!r}).touch()'
            parent = f'import subprocess, sys; subprocess.Popen([sys.executable, "-c", {child!r}])'
            result = coacus_eval._bounded_run(command(parent), .15)
            self.assertEqual(result[3], 'TIMEOUT')
            time.sleep(1.2)
            self.assertFalse(marker.exists())

    @unittest.skipUnless(os.name == 'posix', 'requires POSIX process groups')
    def test_descendant_killed_on_output_limit(self):
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / 'survived'
            child = f'import time; from pathlib import Path; time.sleep(1); Path({str(marker)!r}).touch()'
            parent = f'import subprocess, sys; subprocess.Popen([sys.executable, "-c", {child!r}]); sys.stdout.write("x" * 2000000); sys.stdout.flush()'
            result = coacus_eval._bounded_run(command(parent), 5)
            self.assertEqual(result[3], 'OUTPUT_LIMIT')
            time.sleep(1.2)
            self.assertFalse(marker.exists())

    def test_harness_rejects_oversized_stdout_and_stderr(self):
        for stream in ('stdout', 'stderr'):
            with self.subTest(stream=stream):
                scenario = {'harness': 'test', 'prompt': ''}
                code = f'import sys; sys.{stream}.write("x" * 2000000)'
                transcript, status = coacus_eval._run_harness(scenario, 5, {'test': command(code)})
                self.assertEqual(transcript, '')
                self.assertEqual(status, 'OUTPUT_LIMIT')

    def test_harness_timeout_and_normal_output(self):
        scenario = {'harness': 'test', 'prompt': ''}
        self.assertEqual(coacus_eval._run_harness(scenario, 5, {'test': command('print("ok")')}), ('ok', 'OK'))
        start = time.monotonic()
        self.assertEqual(coacus_eval._run_harness(scenario, .2, {'test': command('import time; time.sleep(5)')})[1], 'TIMEOUT')
        self.assertLess(time.monotonic() - start, 3)

    def test_strict_judge_rejects_oversized_output(self):
        scenario = {'rubric': ['rule']}
        for stream in ('stdout', 'stderr'):
            with self.subTest(stream=stream):
                code = f'import sys; sys.stdin.read(); sys.{stream}.write("x" * 2000000); print(\'{{"verdicts": [true]}}\')'
                result = coacus_eval._strict_judge(scenario, 'ok', shlex.join(command(code)), False, {})
                self.assertFalse(result['passed'])

    def test_strict_judge_accepts_valid_output(self):
        code = 'import sys; sys.stdin.read(); print(\'{"verdicts": [true]}\')'
        result = coacus_eval._strict_judge({'rubric': ['rule']}, 'ok', shlex.join(command(code)), False, {})
        self.assertTrue(result['passed'])
