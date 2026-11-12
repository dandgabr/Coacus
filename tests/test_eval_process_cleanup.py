import os
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

from scripts import coacus_eval


class ProcessCleanupTests(unittest.TestCase):
    def test_npm_opencode_shim_does_not_substitute_adjacent_executable(self):
        with tempfile.TemporaryDirectory(prefix='shim space ') as directory:
            shim = Path(directory) / 'opencode.cmd'
            shim.touch()
            native = Path(directory) / 'node_modules' / '@opencode' / 'cli' / 'bin' / 'opencode.exe'
            native.parent.mkdir(parents=True)
            native.touch()
            windows_os = mock.Mock(wraps=os)
            windows_os.name = 'nt'
            prompt = '"quoted" & echo INJECTED\n%PATH% ! ^'
            with mock.patch.object(coacus_eval, 'os', windows_os), \
                 mock.patch.object(coacus_eval.shutil, 'which', return_value=str(shim)), \
                 mock.patch.object(coacus_eval, '_bounded_run', return_value=('ok', '', 0, None)) as run:
                self.assertEqual(coacus_eval._run_harness(
                    {'harness': 'opencode', 'prompt': prompt}, 5,
                    {'opencode': ['opencode', 'run']}), ('', 'UNSAFE_CLI_ARGUMENT'))
            run.assert_not_called()

    def test_explicit_native_executable_receives_arbitrary_prompt(self):
        windows_os = mock.Mock(wraps=os)
        windows_os.name = 'nt'
        prompt = '"quoted" & echo INJECTED\n%PATH% ! ^'
        native = r'C:\trusted path\opencode.exe'
        with mock.patch.object(coacus_eval, 'os', windows_os), \
             mock.patch.object(coacus_eval.shutil, 'which', return_value=native), \
             mock.patch.object(coacus_eval, '_bounded_run', return_value=('ok', '', 0, None)) as run:
            self.assertEqual(coacus_eval._run_harness(
                {'harness': 'opencode', 'prompt': prompt}, 5,
                {'opencode': [native, 'run']}), ('ok', 'OK'))
        self.assertEqual(run.call_args.args[0], [native, 'run', prompt])

    def test_native_override_requires_absolute_executable_path(self):
        windows_os = mock.Mock(wraps=os)
        windows_os.name = 'nt'
        with tempfile.TemporaryDirectory() as directory, mock.patch.object(coacus_eval, 'os', windows_os):
            with mock.patch.dict(os.environ, {'COACUS_EVAL_OPENCODE_EXE': r'C:\trusted path\opencode.exe'}):
                self.assertEqual(coacus_eval._live_clis(Path(directory))['opencode'],
                                 [r'C:\trusted path\opencode.exe', 'run'])
            for value in ('opencode.exe', r'C:\temp\runner.cmd'):
                with mock.patch.dict(os.environ, {'COACUS_EVAL_OPENCODE_EXE': value}):
                    with self.assertRaises(ValueError):
                        coacus_eval._live_clis(Path(directory))

    @unittest.skipUnless(os.name == 'nt', 'requires Windows cmd')
    def test_windows_cmd_shim_with_spaces_and_rejects_injection(self):
        with tempfile.TemporaryDirectory(prefix='shim space ') as directory:
            shim = Path(directory) / 'runner.cmd'
            shim.write_text('@echo off\r\necho %1\r\n', encoding='ascii')
            with mock.patch.dict(os.environ, {'PATH': directory + os.pathsep + os.environ.get('PATH', '')}):
                out, status = coacus_eval._run_harness(
                    {'harness': 'test', 'prompt': 'hello world'}, 5, {'test': ['runner']})
                self.assertEqual(status, 'OK')
                self.assertIn('hello world', out)
                for prompt in ('a&echo INJECTED', '%PATH%', 'a"&echo INJECTED', 'a\nwhoami'):
                    out, status = coacus_eval._run_harness(
                        {'harness': 'test', 'prompt': prompt}, 5, {'test': ['runner']})
                    self.assertEqual(out, '')
                    self.assertEqual(status, 'UNSAFE_CLI_ARGUMENT')

    @unittest.skipUnless(os.name == 'nt', 'requires Windows job objects')
    def test_windows_runs_contained_process(self):
        result = coacus_eval._bounded_run([sys.executable, '-c', 'print("ok")'], 5)
        self.assertEqual((result[0].strip(), result[3]), ('ok', None))

    @unittest.skipUnless(os.name == 'nt', 'requires Windows job objects')
    def test_windows_exited_leader_with_closed_descendant_streams_waits_for_job(self):
        with tempfile.TemporaryDirectory() as directory:
            ready = Path(directory) / 'ready'
            marker = Path(directory) / 'survived'
            child = (f'from pathlib import Path; import time; Path({str(ready)!r}).touch(); '
                     f'time.sleep(1); Path({str(marker)!r}).touch()')
            parent = ('import subprocess, sys, time; from pathlib import Path; '
                      f'subprocess.Popen([sys.executable, "-c", {child!r}], '
                      'stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); '
                      f'p=Path({str(ready)!r}); '
                      'exec("while not p.exists():\\n time.sleep(.01)"); print("ok")')
            real_wait = coacus_eval._wait_windows_job_empty
            with mock.patch.object(coacus_eval, '_wait_windows_job_empty', wraps=real_wait) as wait:
                result = coacus_eval._bounded_run([sys.executable, '-c', parent], 5)
            self.assertEqual((result[0].strip(), result[3]), ('ok', None))
            wait.assert_called_once()
            time.sleep(1.2)
            self.assertFalse(marker.exists())

    def test_windows_setup_failure_closes_job_when_process_cleanup_raises(self):
        for failing_method in ('kill', 'wait'):
            with self.subTest(failing_method=failing_method):
                kernel = mock.Mock()
                kernel.AssignProcessToJobObject.side_effect = OSError('setup failed')
                proc = mock.Mock()
                proc._handle = 123
                getattr(proc, failing_method).side_effect = OSError('cleanup failed')
                windows_os = mock.Mock(wraps=os, name='windows_os')
                windows_os.name = 'nt'
                with mock.patch.object(coacus_eval, 'os', windows_os), \
                     mock.patch.object(coacus_eval, '_windows_job', return_value=(kernel, 42)), \
                     mock.patch.object(coacus_eval.subprocess, 'Popen', return_value=proc):
                    with self.assertRaises((OSError, RuntimeError)):
                        coacus_eval._bounded_run(['runner'], 5)
                kernel.CloseHandle.assert_called_once_with(42)

    def test_assignment_failure_retries_termination_and_reaps(self):
        kernel = mock.Mock()
        kernel.AssignProcessToJobObject.side_effect = OSError('assignment failed')
        kernel.TerminateProcess.return_value = 1
        proc = mock.Mock()
        proc._handle = 123
        proc.kill.side_effect = OSError('kill failed')
        windows_os = mock.Mock(wraps=os)
        windows_os.name = 'nt'
        with mock.patch.object(coacus_eval, 'os', windows_os), \
             mock.patch.object(coacus_eval, '_windows_job', return_value=(kernel, 42)), \
             mock.patch.object(coacus_eval.subprocess, 'Popen', return_value=proc):
            with self.assertRaisesRegex(OSError, 'assignment failed'):
                coacus_eval._bounded_run(['runner'], 5)
        kernel.TerminateProcess.assert_called_once_with(123, 1)
        proc.wait.assert_called_once_with(timeout=5)

    def test_assignment_failure_reports_unterminated_process(self):
        kernel = mock.Mock()
        kernel.AssignProcessToJobObject.side_effect = OSError('assignment failed')
        kernel.TerminateProcess.return_value = 0
        proc = mock.Mock()
        proc._handle = 123
        proc.pid = 456
        proc.kill.side_effect = OSError('kill failed')
        proc.poll.return_value = None
        windows_os = mock.Mock(wraps=os)
        windows_os.name = 'nt'
        with mock.patch.object(coacus_eval, 'os', windows_os), \
             mock.patch.object(coacus_eval, '_windows_job', return_value=(kernel, 42)), \
             mock.patch.object(coacus_eval.subprocess, 'Popen', return_value=proc):
            with self.assertRaisesRegex(RuntimeError, 'process 456; it may still be running'):
                coacus_eval._bounded_run(['runner'], 5)
        kernel.CloseHandle.assert_called_once_with(42)

    def test_windows_job_wait_checks_active_processes_and_reports_failures(self):
        import ctypes

        kernel = mock.Mock()
        counts = iter([2, 1, 0])

        def query(job, kind, info, size, returned):
            ctypes.cast(info, ctypes.POINTER(coacus_eval._JobAccounting)).contents.ActiveProcesses = next(counts)
            return 1

        kernel.QueryInformationJobObject.side_effect = query
        coacus_eval._wait_windows_job_empty(kernel, 42, 1)
        self.assertEqual(kernel.QueryInformationJobObject.call_count, 3)
        kernel.QueryInformationJobObject.side_effect = None
        kernel.QueryInformationJobObject.return_value = 0
        with self.assertRaisesRegex(RuntimeError, 'QueryInformationJobObject'):
            coacus_eval._wait_windows_job_empty(kernel, 42, 1)
        kernel.QueryInformationJobObject.side_effect = lambda *args: (
            setattr(ctypes.cast(args[2], ctypes.POINTER(coacus_eval._JobAccounting)).contents,
                    'ActiveProcesses', 1) or 1)
        with self.assertRaisesRegex(RuntimeError, 'job.*active'):
            coacus_eval._wait_windows_job_empty(kernel, 42, 0)

    def test_windows_cleanup_failures_are_reported_and_wait_is_bounded(self):
        import ctypes
        import io
        import subprocess

        for failure in ('terminate', 'close', 'wait', 'job_wait'):
            with self.subTest(failure=failure):
                kernel = mock.Mock()
                kernel.AssignProcessToJobObject.return_value = 1
                kernel.TerminateJobObject.return_value = failure != 'terminate'
                kernel.CloseHandle.return_value = failure != 'close'
                proc = mock.Mock(_handle=123, pid=456, stdin=None,
                                 stdout=io.BytesIO(), stderr=io.BytesIO(), returncode=0)
                proc.poll.return_value = 0
                if failure == 'wait':
                    proc.wait.side_effect = subprocess.TimeoutExpired('runner', 5)
                windows_os = mock.Mock(wraps=os)
                windows_os.name = 'nt'
                ntdll = mock.Mock()
                ntdll.NtResumeProcess.return_value = 0
                with mock.patch.object(coacus_eval, 'os', windows_os), \
                     mock.patch.object(coacus_eval, '_windows_job', return_value=(kernel, 42)), \
                     mock.patch.object(coacus_eval.subprocess, 'Popen', return_value=proc), \
                     mock.patch.object(coacus_eval, '_wait_windows_job_empty',
                                       side_effect=RuntimeError('job wait failed') if failure == 'job_wait' else None) as job_wait, \
                     mock.patch.object(ctypes, 'WinDLL', return_value=ntdll, create=True):
                    with self.assertRaisesRegex(RuntimeError, 'cleanup|termination'):
                        coacus_eval._bounded_run(['runner'], 5)
                job_wait.assert_called_once_with(kernel, 42, 5)
                kernel.CloseHandle.assert_called_once_with(42)
                proc.wait.assert_called_once_with(timeout=5)

    @unittest.skipUnless(os.name == 'nt', 'requires native Windows')
    def test_windows_assignment_failure_kill_error_terminates_suspended_process(self):
        processes = []
        popen = coacus_eval.subprocess.Popen
        real_job = coacus_eval._windows_job

        def start(*args, **kwargs):
            proc = popen(*args, **kwargs)
            processes.append(proc)
            proc.kill = mock.Mock(side_effect=OSError('forced kill failure'))
            return proc

        def job_with_failed_assignment():
            kernel, job = real_job()
            wrapper = mock.Mock(wraps=kernel)
            wrapper.AssignProcessToJobObject.side_effect = OSError('forced assignment failure')
            return wrapper, job

        try:
            with mock.patch.object(coacus_eval, '_windows_job', side_effect=job_with_failed_assignment), \
                 mock.patch.object(coacus_eval.subprocess, 'Popen', side_effect=start):
                with self.assertRaisesRegex(OSError, 'forced assignment failure'):
                    coacus_eval._bounded_run([sys.executable, '-c', 'import time; time.sleep(30)'], 5)
            self.assertIsNotNone(processes[0].poll())
        finally:
            if processes and processes[0].poll() is None:
                popen.kill(processes[0])
                processes[0].wait()

    @unittest.skipUnless(os.name in ('posix', 'nt'), 'requires process containment')
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
        waited = []
        popen = coacus_eval.subprocess.Popen

        def start(*args, **kwargs):
            proc = popen(*args, **kwargs)
            processes.append(proc)
            wait = proc.wait

            def wait_with_fallback(*args, **kwargs):
                time.sleep(.001)  # Exercise the sleep used by subprocess.wait's fallback.
                result = wait(*args, **kwargs)
                waited.append(True)
                return result

            proc.wait = mock.Mock(side_effect=wait_with_fallback)
            return proc

        eval_time = mock.Mock(wraps=time)
        eval_time.sleep.side_effect = KeyboardInterrupt
        try:
            with mock.patch.object(coacus_eval.subprocess, 'Popen', side_effect=start), \
                 mock.patch.object(coacus_eval, 'time', eval_time):
                with self.assertRaises(KeyboardInterrupt):
                    coacus_eval._bounded_run([sys.executable, '-c', 'import time; time.sleep(30)'], 5)
            eval_time.sleep.assert_called_once_with(.01)
            processes[0].wait.assert_called_once_with(timeout=5)
            self.assertEqual(waited, [True])
            self.assertIsNotNone(processes[0].returncode)
        finally:
            if processes and processes[0].poll() is None:
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
        self.assertEqual(status, 'RUNNER_ERROR (OSError)' if os.name == 'nt'
                         else 'RUNNER_ERROR (PermissionError)')

    def test_unsupported_platform_returns_explicit_status(self):
        with mock.patch.object(coacus_eval.os, 'name', 'unsupported'):
            result = coacus_eval._run_harness({'harness': 'test', 'prompt': ''}, 5, {'test': [sys.executable]})
        self.assertEqual(result, ('', 'UNSUPPORTED_PLATFORM'))

    def test_unsupported_platform_reported_by_strict_judge(self):
        with mock.patch.object(coacus_eval.os, 'name', 'unsupported'):
            result = coacus_eval._strict_judge({'rubric': ['rule']}, 'ok', 'judge', False, {})
        self.assertFalse(result['passed'])
        self.assertIn('UNSUPPORTED_PLATFORM', result['verdict'])
