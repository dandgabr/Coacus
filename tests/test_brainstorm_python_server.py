import base64
import hashlib
import http.client
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import time
import unittest
from urllib.parse import urlsplit

SCRIPT = Path(__file__).resolve().parents[1] / 'methodology/workflows/brainstorming/scripts/server.py'


class PythonServerTests(unittest.TestCase):
    def test_safe_read_contains_names_and_rejects_links(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location('brainstorm_server_paths', SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = root / 'content'
            content.mkdir()
            (content / 'ok.txt').write_text('inside')
            outside = root / 'outside.txt'
            outside.write_text('outside')
            try:
                (content / 'symlink').symlink_to(outside)
            except OSError:
                pass
            os.link(outside, content / 'hardlink')
            module.CONTENT = content
            self.assertEqual(module.safe_read('ok.txt')[0], b'inside')
            for name in ('../outside.txt', str(outside), '.hidden', 'symlink', 'hardlink', 'bad\0name'):
                with self.subTest(name=name), self.assertRaises(OSError):
                    module.safe_read(name)

    def test_safe_read_rejects_symlinked_content_directory(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location('brainstorm_server_parent', SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            outside = root / 'outside'
            outside.mkdir()
            (outside / 'screen.html').write_text('outside')
            module.CONTENT = root / 'content'
            try:
                module.CONTENT.symlink_to(outside, target_is_directory=True)
            except OSError as exc:
                self.skipTest(f'symlinks unavailable: {exc}')
            with self.assertRaises(OSError):
                module.safe_read('screen.html')

    def test_state_writes_reject_links_and_preserve_targets(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location('brainstorm_server_write', SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            module.STATE = root / 'state'
            module.STATE.mkdir()
            outside = root / 'outside'
            outside.write_text('protected')
            for name in ('events', 'server-info'):
                target = module.STATE / name
                module.safe_state_write(name, 'first')
                module.safe_state_write(name, 'second', append=True)
                self.assertEqual(target.read_text(), 'firstsecond')
                if os.name == 'posix':
                    os.chmod(target, 0o644)
                    module.safe_state_write(name, 'private')
                    self.assertEqual(target.stat().st_mode & 0o777, 0o600)
                target.unlink()
                os.link(outside, target)
                with self.assertRaises(OSError):
                    module.safe_state_write(name, 'destroy')
                self.assertEqual(outside.read_text(), 'protected')
                target.unlink()
                try:
                    target.symlink_to(outside)
                except OSError:
                    continue
                with self.assertRaises(OSError):
                    module.safe_state_write(name, 'destroy')
                self.assertEqual(outside.read_text(), 'protected')
                target.unlink()

    def test_state_replace_failure_preserves_previous_content(self):
        import importlib.util
        from unittest import mock
        spec = importlib.util.spec_from_file_location('brainstorm_atomic_write', SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as tmp:
            module.STATE = Path(tmp)
            (module.STATE / 'server-info').write_text('original')
            with mock.patch.object(module.os, 'replace', side_effect=OSError('injected')):
                with self.assertRaises(OSError):
                    module.safe_state_write('server-info', 'replacement')
            self.assertEqual((module.STATE / 'server-info').read_text(), 'original')

    def test_configured_output_rejects_links_and_writes_normally(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location('brainstorm_output', SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            outside = root / 'outside'
            outside.write_text('protected')
            for filename in ('port', 'token'):
                output = root / filename
                module.safe_file_write(output, 'normal')
                self.assertEqual(output.read_text(), 'normal')
                output.unlink()
                os.link(outside, output)
                with self.assertRaises(OSError):
                    module.safe_file_write(output, 'replacement')
                self.assertEqual(outside.read_text(), 'protected')
                output.unlink()
                try:
                    output.symlink_to(outside)
                except OSError:
                    continue
                with self.assertRaises(OSError):
                    module.safe_file_write(output, 'replacement')
                self.assertEqual(outside.read_text(), 'protected')
                output.unlink()

    def test_server_requires_explicit_session_directory(self):
        env = dict(os.environ)
        env.pop('BRAINSTORM_DIR', None)
        result = subprocess.run([sys.executable, str(SCRIPT)], env=env, capture_output=True, text=True, timeout=5)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('BRAINSTORM_DIR is required', result.stderr)

    def test_first_screen_created_at_readiness_is_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            code = """import builtins, json, os, runpy, sys
original = builtins.print
def report(*args, **kwargs):
    if args and isinstance(args[0], str) and 'server-started' in args[0]:
        open(os.path.join(os.environ['BRAINSTORM_DIR'], 'content', 'first.html'), 'w').write('first')
    original(*args, **kwargs)
builtins.print = report
runpy.run_path(sys.argv[1], run_name='__main__')
"""
            env = dict(os.environ, BRAINSTORM_DIR=tmp, BRAINSTORM_PORT='0', BRAINSTORM_TOKEN='a' * 64)
            proc = subprocess.Popen([sys.executable, '-c', code, str(SCRIPT)], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            try:
                json.loads(proc.stdout.readline())
                import select
                self.assertTrue(select.select([proc.stdout], [], [], 3)[0])
                self.assertEqual(json.loads(proc.stdout.readline())['type'], 'screen-added')
            finally:
                proc.terminate()
                proc.wait(timeout=5)
                proc.stdout.close()
                proc.stderr.close()

    def test_token_written_when_port_file_write_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            token_path = Path(tmp) / 'token'
            env = dict(os.environ, BRAINSTORM_DIR=tmp, BRAINSTORM_PORT='0', BRAINSTORM_PORT_FILE=str(Path(tmp) / 'missing' / 'port'), BRAINSTORM_TOKEN_FILE=str(token_path))
            env.pop('BRAINSTORM_TOKEN', None)
            proc = subprocess.Popen([sys.executable, str(SCRIPT)], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            try:
                json.loads(proc.stdout.readline())
                self.assertTrue(token_path.is_file())
            finally:
                proc.terminate()
                proc.wait(timeout=5)
                proc.stdout.close()
                proc.stderr.close()

    def test_portable_serialized_frames(self):
        import importlib.util
        import threading
        from unittest import mock
        spec = importlib.util.spec_from_file_location('brainstorm_server', SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        left, right = socket.socketpair()
        right.settimeout(3)
        client = module.Client(left)
        try:
            with mock.patch.object(module.socket, 'MSG_DONTWAIT', None):
                with module.lock:
                    module.clients.add(client)
                module.broadcast()
                reload_frame = module.frame(1, b'{"type":"reload"}')
                self.assertEqual(right.recv(len(reload_frame)), reload_frame)
                threads = [threading.Thread(target=lambda: [client.send(module.frame(10, b'x' * 125)) for _ in range(20)]) for _ in range(2)]
                for thread in threads: thread.start()
                for thread in threads: thread.join()
                data = b''
                while len(data) < 40 * 127:
                    data += right.recv(8192)
                self.assertEqual(data, module.frame(10, b'x' * 125) * 40)
        finally:
            client.close()
            left.close()
            right.close()

    def test_monitor_survives_directory_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = dict(os.environ, BRAINSTORM_DIR=tmp, BRAINSTORM_PORT='0', BRAINSTORM_TOKEN='a' * 64,
                       BRAINSTORM_IDLE_TIMEOUT_MS='500', BRAINSTORM_LIFECYCLE_CHECK_MS='100')
            proc = subprocess.Popen([sys.executable, str(SCRIPT)], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            try:
                json.loads(proc.stdout.readline())
                (Path(tmp) / 'content').rmdir()
                self.assertEqual(proc.wait(timeout=4), 0)
                self.assertEqual(json.loads((Path(tmp) / 'state/server-stopped').read_text())['reason'], 'idle timeout')
            finally:
                if proc.poll() is None:
                    proc.terminate()
                    proc.wait(timeout=5)
                proc.stdout.close()
                proc.stderr.close()

    def test_recreated_screen_preserves_choices_and_same_mtime_update_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            content = Path(tmp) / 'content'
            content.mkdir()
            screen = content / 'screen.html'
            screen.write_text('first')
            env = dict(os.environ, BRAINSTORM_DIR=tmp, BRAINSTORM_PORT='0', BRAINSTORM_TOKEN='a' * 64)
            proc = subprocess.Popen([sys.executable, str(SCRIPT)], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            try:
                json.loads(proc.stdout.readline())
                time.sleep(.3)
                original_mtime = screen.stat().st_mtime_ns
                screen.write_text('other')
                os.utime(screen, ns=(original_mtime, original_mtime))
                import select
                self.assertTrue(select.select([proc.stdout], [], [], 3)[0], 'same-mtime update was missed')
                self.assertEqual(json.loads(proc.stdout.readline())['type'], 'screen-updated')
                events = Path(tmp) / 'state/events'
                events.write_text('{"choice":"yes"}\n')
                screen.unlink()
                time.sleep(.3)
                screen.write_text('again')
                self.assertTrue(select.select([proc.stdout], [], [], 3)[0], 'recreated screen was missed')
                self.assertEqual(json.loads(proc.stdout.readline())['type'], 'screen-updated')
                self.assertTrue(events.exists(), 'recreated screen erased choices')
            finally:
                proc.terminate()
                proc.wait(timeout=5)
                proc.stdout.close()
                proc.stderr.close()

    def test_dangling_link_does_not_stop_startup(self):
        with tempfile.TemporaryDirectory() as tmp:
            content = Path(tmp) / 'content'
            content.mkdir()
            try:
                (content / 'broken.html').symlink_to(content / 'missing')
            except OSError as exc:
                self.skipTest(f'symlinks unavailable: {exc}')
            env = dict(os.environ, BRAINSTORM_DIR=tmp, BRAINSTORM_PORT='0', BRAINSTORM_TOKEN='a' * 64)
            proc = subprocess.Popen([sys.executable, str(SCRIPT)], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            try:
                info = json.loads(proc.stdout.readline())
                time.sleep(.3)
                self.assertIsNone(proc.poll(), proc.stderr.read() if proc.poll() is not None else '')
                conn = http.client.HTTPConnection('127.0.0.1', info['port'], timeout=3)
                conn.request('GET', '/?key=' + 'a' * 64)
                self.assertEqual(conn.getresponse().status, 200)
                conn.close()
            finally:
                proc.terminate()
                proc.wait(timeout=5)
                proc.stdout.close()
                proc.stderr.close()

    def test_websocket_protocol_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = dict(os.environ, BRAINSTORM_DIR=tmp, BRAINSTORM_PORT='0', BRAINSTORM_TOKEN='a' * 64)
            proc = subprocess.Popen([sys.executable, str(SCRIPT)], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            try:
                port = json.loads(proc.stdout.readline())['port']
                valid_key = base64.b64encode(os.urandom(16)).decode()
                def handshake(key=valid_key, version='13'):
                    ws = socket.create_connection(('127.0.0.1', port), timeout=2)
                    ws.sendall((f'GET /?key={"a" * 64} HTTP/1.1\r\nHost: 127.0.0.1:{port}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: {version}\r\n\r\n').encode())
                    return ws, ws.recv(4096)
                for key, version in [('bad', '13'), (valid_key, '12')]:
                    ws, response = handshake(key, version)
                    with ws: self.assertNotIn(b'101 Switching Protocols', response)
                for data in [b'\x01\x80abcd', b'\xc1\x80abcd', b'\x89\xfe\x00\x7e', b'\x81\xff' + (10 * 1024 * 1024 + 1).to_bytes(8, 'big')]:
                    ws, response = handshake()
                    with ws:
                        self.assertIn(b'101 Switching Protocols', response)
                        ws.sendall(data)
                        self.assertEqual(ws.recv(2)[0] & 15, 8)
            finally:
                proc.terminate()
                proc.wait(timeout=5)
                proc.stdout.close()
                proc.stderr.close()

    def test_http_websocket_and_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = dict(os.environ, BRAINSTORM_DIR=tmp, BRAINSTORM_PORT='0', BRAINSTORM_TOKEN='a' * 64)
            proc = subprocess.Popen([sys.executable, str(SCRIPT)], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            try:
                info = json.loads(proc.stdout.readline())
                port = info['port']
                conn = http.client.HTTPConnection('127.0.0.1', port, timeout=3)
                conn.request('GET', '/')
                response = conn.getresponse()
                self.assertEqual(response.status, 403)
                response.read()
                conn.request('GET', '/?key=' + 'a' * 64)
                response = conn.getresponse()
                self.assertEqual(response.status, 200)
                cookie = response.getheader('Set-Cookie').split(';')[0]
                response.read()
                content = Path(tmp) / 'content'
                (content / 'screen.html').write_text('<h1>Example</h1>')
                conn.request('GET', '/', headers={'Cookie': cookie})
                response = conn.getresponse()
                self.assertIn(b'<h1>Example</h1>', response.read())
                outside = Path(tmp) / 'outside'
                outside.write_text('secret')
                try:
                    (content / 'link').symlink_to(outside)
                except OSError:
                    pass
                conn.request('GET', '/files/link', headers={'Cookie': cookie})
                response = conn.getresponse()
                self.assertEqual(response.status, 404)
                response.read()
                key = base64.b64encode(os.urandom(16)).decode()
                expected_accept = base64.b64encode(hashlib.sha1((key + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11').encode(), usedforsecurity=False).digest())
                with socket.create_connection(('127.0.0.1', port), timeout=3) as ws:
                    ws.sendall((f'GET / HTTP/1.1\r\nHost: 127.0.0.1:{port}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\nCookie: {cookie}\r\nOrigin: http://127.0.0.1:{port}\r\n\r\n').encode())
                    handshake = ws.recv(4096)
                    self.assertIn(b'101 Switching Protocols', handshake)
                    self.assertIn(b'Sec-WebSocket-Accept: ' + expected_accept, handshake)
                    payload = json.dumps({'choice': 'yes'}).encode()
                    mask = b'abcd'
                    ws.sendall(bytes([0x81, 0x80 | len(payload)]) + mask + bytes(b ^ mask[i % 4] for i, b in enumerate(payload)))
                    events = Path(tmp) / 'state/events'
                    for _ in range(30):
                        if events.exists(): break
                        time.sleep(.05)
                    self.assertEqual(json.loads(events.read_text())['choice'], 'yes')
                conn.close()
            finally:
                proc.terminate()
                proc.wait(timeout=5)
                proc.stdout.close()
                proc.stderr.close()


if __name__ == '__main__':
    unittest.main()
