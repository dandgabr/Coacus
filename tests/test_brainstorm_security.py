import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / 'methodology/workflows/brainstorming/scripts'
spec = importlib.util.spec_from_file_location('brainstorm_stop', SCRIPTS / 'stop_server.py')
stop = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stop)
start_spec = importlib.util.spec_from_file_location('brainstorm_start', SCRIPTS / 'start_server.py')
start = importlib.util.module_from_spec(start_spec)
start_spec.loader.exec_module(start)


class BrainstormSecurityTests(unittest.TestCase):
    def test_symlink_session_and_state_are_rejected_without_modification(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            external = root / 'external'
            external.mkdir()
            (external / 'server.pid').write_text('99999999')
            (external / 'server-instance-id').write_text('a' * 48)
            (external / 'server-info').write_text('user data')
            original = {p.name: p.read_bytes() for p in external.iterdir()}
            session = root / 'session'
            session.mkdir()
            (session / 'state').symlink_to(external, target_is_directory=True)
            self.assertNotEqual(stop.main([str(session)]), 0)
            self.assertEqual({p.name: p.read_bytes() for p in external.iterdir()}, original)
            actual = root / 'actual'
            actual.mkdir()
            (actual / 'state').mkdir()
            alias = root / 'alias'
            alias.symlink_to(actual, target_is_directory=True)
            self.assertNotEqual(stop.main([str(alias)]), 0)
            self.assertEqual(list((actual / 'state').iterdir()), [])

    def test_invalid_and_unverified_pids_never_signalled(self):
        for pid in ('0', '-1', str(os.getpid())):
            with self.subTest(pid=pid), tempfile.TemporaryDirectory() as tmp:
                state = Path(tmp) / 'state'
                state.mkdir()
                (state / 'server.pid').write_text(pid)
                (state / 'server-instance-id').write_text('a' * 48)
                with mock.patch.object(stop.signal, 'pidfd_send_signal', create=True) as send:
                    self.assertNotEqual(stop.main([tmp]), 0)
                    send.assert_not_called()
                self.assertTrue((state / 'server.pid').exists())

    @unittest.skipUnless(sys.platform == 'linux' and hasattr(os, 'pidfd_open'), 'requires Linux pidfd')
    def test_verified_server_can_stop(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run([sys.executable, str(SCRIPTS / 'start_server.py'), '--project-dir', tmp, '--background'], capture_output=True, text=True, timeout=15)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            info = json.loads(result.stdout.strip().splitlines()[-1])
            session = str(Path(info['state_dir']).parent)
            result = subprocess.run([sys.executable, str(SCRIPTS / 'stop_server.py'), session], capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(json.loads(result.stdout)['status'], 'stopped')

    def test_unsupported_background_rejected_foreground_allowed(self):
        with mock.patch.object(start, 'supports_safe_stop', return_value=False), tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(start.main(['--background', '--project-dir', tmp]), 1)
            with mock.patch.object(start.subprocess, 'Popen') as popen:
                popen.return_value.pid = 12345
                popen.return_value.wait.return_value = 0
                self.assertEqual(start.main(['--foreground', '--project-dir', tmp]), 0)

    def test_default_foreground_when_platform_lacks_safe_stop(self):
        for platform in ('darwin', 'win32'):
            with self.subTest(platform=platform), tempfile.TemporaryDirectory() as tmp:
                with mock.patch.object(start.sys, 'platform', platform), mock.patch.object(start.subprocess, 'Popen') as popen:
                    popen.return_value.pid = 12345
                    popen.return_value.wait.return_value = 0
                    self.assertEqual(start.main(['--project-dir', tmp]), 0)
                    popen.return_value.wait.assert_called_once()

    @unittest.skipUnless(sys.platform == 'linux' and hasattr(os, 'pidfd_open'), 'requires Linux pidfd')
    def test_dead_pid_is_cleaned_without_signal(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / 'state'
            state.mkdir()
            (state / 'server.pid').write_text('99999999')
            (state / 'server-instance-id').write_text('a' * 48)
            with mock.patch.object(stop.signal, 'pidfd_send_signal') as send:
                self.assertEqual(stop.main([tmp]), 0)
                send.assert_not_called()
            self.assertFalse((state / 'server.pid').exists())
            self.assertTrue((state / 'server-stopped').exists())

    @unittest.skipUnless(sys.platform == 'linux' and hasattr(os, 'pidfd_open'), 'requires Linux pidfd')
    def test_signal_failure_closes_pidfd_and_preserves_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run([sys.executable, str(SCRIPTS / 'start_server.py'), '--project-dir', tmp, '--background'], capture_output=True, text=True, timeout=15)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            session = Path(json.loads(result.stdout.strip().splitlines()[-1])['state_dir']).parent
            real_close = os.close
            closed = []
            def record_close(fd):
                closed.append(fd)
                real_close(fd)
            try:
                with mock.patch.object(stop.signal, 'pidfd_send_signal', side_effect=PermissionError()), mock.patch.object(stop.os, 'close', side_effect=record_close):
                    self.assertEqual(stop.main([str(session)]), 1)
                self.assertEqual(len(closed), 1)
                self.assertTrue((session / 'state/server.pid').exists())
            finally:
                subprocess.run([sys.executable, str(SCRIPTS / 'stop_server.py'), str(session)], capture_output=True, timeout=10)

    @unittest.skipIf(os.name == 'nt', 'requires executable shebang')
    def test_python_server_launcher_receives_hostile_url_as_one_argument(self):
        with tempfile.TemporaryDirectory() as tmp:
            launcher = Path(tmp) / 'launcher'
            output = Path(tmp) / 'args.json'
            launcher.write_text('#!' + sys.executable + '\nimport json, os, sys\nwith open(os.environ["ARGS_OUTPUT"], "w") as f: json.dump(sys.argv[1:], f)\n')
            launcher.chmod(0o700)
            env = dict(os.environ, BRAINSTORM_DIR=tmp, BRAINSTORM_PORT='0', BRAINSTORM_TOKEN='a' * 64,
                       BRAINSTORM_OPEN='1', BRAINSTORM_OPEN_CMD=str(launcher),
                       BRAINSTORM_URL_HOST='localhost;$(touch PWNED)', ARGS_OUTPUT=str(output))
            proc = subprocess.Popen([sys.executable, str(SCRIPTS / 'server.py')], cwd=tmp, env=env,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            try:
                json.loads(proc.stdout.readline())
                (Path(tmp) / 'content' / 'screen.html').write_text('screen')
                import time
                deadline = time.monotonic() + 5
                while not output.exists() and time.monotonic() < deadline:
                    time.sleep(.05)
                args = json.loads(output.read_text())
                self.assertEqual(len(args), 1)
                self.assertIn('$(touch PWNED)', args[0])
                self.assertFalse((Path(tmp) / 'PWNED').exists())
            finally:
                proc.terminate()
                proc.wait(timeout=5)
                proc.stdout.close()
                proc.stderr.close()

    @unittest.skipUnless(sys.platform == 'linux' and hasattr(os, 'pidfd_open'), 'requires Linux pidfd')
    def test_forged_temp_session_is_never_recursively_deleted(self):
        with tempfile.TemporaryDirectory(prefix='brainstorm-') as tmp:
            state = Path(tmp) / 'state'
            state.mkdir()
            (Path(tmp) / 'user-data').write_text('keep')
            (state / 'server.pid').write_text('99999999')
            (state / 'server-instance-id').write_text('a' * 48)
            (state / 'owned').write_text('brainstorm')
            self.assertEqual(stop.main([tmp]), 0)
            self.assertEqual((Path(tmp) / 'user-data').read_text(), 'keep')

    @unittest.skipUnless(sys.platform == 'linux' and hasattr(os, 'pidfd_open'), 'requires Linux pidfd')
    def test_owned_temp_session_preserves_content_after_stop(self):
        result = subprocess.run([sys.executable, str(SCRIPTS / 'start_server.py'), '--background'], capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        session = Path(json.loads(result.stdout.splitlines()[-1])['state_dir']).parent
        try:
            (session / 'content' / 'user.html').write_text('keep')
            result = subprocess.run([sys.executable, str(SCRIPTS / 'stop_server.py'), str(session)], capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual((session / 'content' / 'user.html').read_text(), 'keep')
        finally:
            import shutil
            shutil.rmtree(session, ignore_errors=True)

    def test_default_session_creation_does_not_adopt_existing(self):
        with tempfile.TemporaryDirectory() as tmp:
            existing = Path(tmp) / 'brainstorm-fixed'
            existing.mkdir()
            (existing / 'user-data').write_text('keep')
            with mock.patch.object(start.tempfile, 'gettempdir', return_value=tmp), mock.patch.object(start.secrets, 'token_hex', return_value='a' * 48), mock.patch.object(start.subprocess, 'Popen') as popen:
                popen.return_value.pid = 12345
                popen.return_value.wait.return_value = 0
                self.assertEqual(start.main(['--foreground']), 0)
                created = Path(popen.call_args.kwargs['env']['BRAINSTORM_DIR'])
                self.assertNotEqual(created, existing)
                self.assertEqual((existing / 'user-data').read_text(), 'keep')
                self.assertEqual(created.parent, Path(tmp))

    def test_no_external_image_beacon(self):
        for name in ('helper.js', 'frame-template.html'):
            text = (SCRIPTS / name).read_text()
            self.assertNotRegex(text, r'https?://[^\s\"\']+')


if __name__ == '__main__':
    unittest.main()
