"""Local authenticated brainstorming companion."""
import base64
import hashlib
import hmac
import json
import os
import queue
from pathlib import Path
import secrets
import socket
import stat
import struct
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, quote, urlsplit

HERE = Path(__file__).resolve().parent
ROOT = Path(os.environ.get('BRAINSTORM_DIR', ''))
CONTENT, STATE = ROOT / 'content', ROOT / 'state'
HOST = os.environ.get('BRAINSTORM_HOST', '127.0.0.1')
URL_HOST = os.environ.get('BRAINSTORM_URL_HOST', 'localhost' if HOST == '127.0.0.1' else HOST)
PORT_FILE = os.environ.get('BRAINSTORM_PORT_FILE')
TOKEN_FILE = os.environ.get('BRAINSTORM_TOKEN_FILE')
MAX_FRAME = 10 * 1024 * 1024
clients = set()
lock = threading.Lock()
last_activity = time.monotonic()
opened = False


def activity():
    global last_activity
    last_activity = time.monotonic()


def safe_read(name):
    """Open a single regular file without following links, including hard links."""
    if not name or '\0' in name or name.startswith('.') or name != Path(name).name:
        raise FileNotFoundError(name)
    flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_NONBLOCK', 0)
    directory = None
    path = CONTENT.absolute()
    if os.open in os.supports_dir_fd and hasattr(os, 'O_NOFOLLOW') and hasattr(os, 'O_DIRECTORY'):
        directory = os.open(path.anchor, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            for component in path.parts[1:]:
                next_fd = os.open(component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory)
                os.close(directory)
                directory = next_fd
            fd = os.open(name, flags, dir_fd=directory)
        except BaseException:
            os.close(directory)
            raise
    else:
        # Without dirfd/nofollow, lstat checks cannot prevent a concurrent local rename race.
        for parent in (path, *path.parents):
            if stat.S_ISLNK(os.lstat(parent).st_mode):
                raise FileNotFoundError(name)
        fd = os.open(path / name, flags)
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode) or st.st_nlink != 1:
            raise FileNotFoundError(name)
        lst = os.stat(name, dir_fd=directory, follow_symlinks=False) if directory is not None else os.lstat(path / name)
        if stat.S_ISLNK(lst.st_mode) or (lst.st_dev, lst.st_ino) != (st.st_dev, st.st_ino):
            raise FileNotFoundError(name)
        with os.fdopen(fd, 'rb') as f:
            fd = -1
            return f.read(), st.st_mtime_ns
    finally:
        if fd >= 0:
            os.close(fd)
        if directory is not None:
            os.close(directory)


def safe_state_write(name, text, append=False):
    return safe_file_write(STATE / name, text, append)


def safe_file_write(target, text, append=False):
    """Write without following links or truncating unvalidated files."""
    target = Path(target).absolute()
    name = target.name
    if not name or '\0' in name or name in ('.', '..'):
        raise FileNotFoundError(name)
    if os.open not in os.supports_dir_fd or not hasattr(os, 'O_NOFOLLOW') or not hasattr(os, 'O_DIRECTORY'):
        raise OSError('secure state writes are unavailable on this platform')
    path = target.parent
    directory = os.open(path.anchor, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for component in path.parts[1:]:
            next_fd = os.open(component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory)
            os.close(directory)
            directory = next_fd
        flags = os.O_WRONLY | os.O_CREAT | os.O_NOFOLLOW | getattr(os, 'O_NONBLOCK', 0)
        fd = os.open(name, flags | (os.O_APPEND if append else 0), 0o600, dir_fd=directory)
        try:
            st = os.fstat(fd)
            if not stat.S_ISREG(st.st_mode) or st.st_nlink != 1:
                raise OSError('unsafe state file')
            if append:
                os.fchmod(fd, 0o600)
                with os.fdopen(fd, 'w') as file:
                    fd = -1
                    file.write(text)
        finally:
            if fd >= 0:
                os.close(fd)
        if not append:
            temporary = '.state-' + secrets.token_hex(16)
            fd = os.open(temporary, flags | os.O_EXCL, 0o600, dir_fd=directory)
            try:
                os.fchmod(fd, 0o600)
                with os.fdopen(fd, 'w') as file:
                    fd = -1
                    file.write(text)
                os.replace(temporary, name, src_dir_fd=directory, dst_dir_fd=directory)
            finally:
                if fd >= 0:
                    os.close(fd)
                try:
                    os.unlink(temporary, dir_fd=directory)
                except FileNotFoundError:
                    pass
    finally:
        os.close(directory)


def frame(opcode, payload=b''):
    n = len(payload)
    header = bytes([0x80 | opcode])
    return header + (bytes([n]) if n < 126 else b'\x7e' + struct.pack('!H', n) if n < 65536 else b'\x7f' + struct.pack('!Q', n)) + payload


def exact(stream, n):
    data = bytearray()
    while len(data) < n:
        part = stream.read(n - len(data))
        if not part:
            raise EOFError
        data.extend(part)
    return bytes(data)


class Client:
    """Serialize frames through a bounded queue; slow clients are disconnected."""
    def __init__(self, connection):
        self.connection = connection
        self.queue = queue.Queue(maxsize=128)
        self.closed = threading.Event()
        threading.Thread(target=self._write, daemon=True).start()

    def _write(self):
        try:
            while not self.closed.is_set():
                item = self.queue.get()
                if item is None:
                    return
                data, done = item
                try:
                    self.connection.sendall(data)
                finally:
                    done.set()
        except OSError:
            self.close()

    def send(self, data, wait=False):
        if self.closed.is_set():
            return False
        done = threading.Event()
        try:
            self.queue.put_nowait((data, done))
        except queue.Full:
            self.close()
            return False
        if wait and not done.wait(0.5):
            self.close()
            return False
        return not self.closed.is_set()

    def close(self):
        if self.closed.is_set():
            return
        self.closed.set()
        with lock:
            clients.discard(self)
        try:
            self.connection.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        try:
            self.queue.put_nowait(None)
        except queue.Full:
            pass


def broadcast():
    data = frame(1, b'{"type":"reload"}')
    with lock:
        snapshot = list(clients)
    for client in snapshot:
        client.send(data)


def url():
    host = URL_HOST if ':' not in URL_HOST or URL_HOST.startswith('[') else '[' + URL_HOST + ']'
    return f'http://{host}:{server.server_port}/?key={quote(token, safe="")}'


def maybe_open():
    global opened
    if opened:
        return
    opened = True
    if not os.environ.get('BRAINSTORM_OPEN') or HOST not in ('127.0.0.1', 'localhost') or clients:
        return
    cmd = os.environ.get('BRAINSTORM_OPEN_CMD')
    if cmd:
        args = [cmd, url()]
    elif sys.platform == 'darwin':
        args = ['open', url()]
    elif sys.platform == 'win32' or (sys.platform.startswith('linux') and 'microsoft' in os.uname().release.lower()):
        args = ['rundll32.exe', 'url.dll,FileProtocolHandler', url()]
    elif os.environ.get('DISPLAY') or os.environ.get('WAYLAND_DISPLAY'):
        args = ['xdg-open', url()]
    else:
        return
    try:
        subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except OSError:
        pass


class Handler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def log_message(self, *args):
        pass

    def authorized(self):
        params = parse_qs(urlsplit(self.path).query, keep_blank_values=True)
        if 'key' in params:
            candidate = params['key'][0]
        else:
            cookies = dict(p.strip().split('=', 1) for p in self.headers.get('Cookie', '').split(';') if '=' in p)
            candidate = cookies.get('brainstorm-key-' + str(server.server_port), '')
        return bool(candidate) and hmac.compare_digest(candidate.encode(), token.encode())

    def respond(self, status, body, content_type='text/plain', cookie=False):
        if isinstance(body, str):
            body = body.encode()
        self.send_response(status)
        for key, value in {'Referrer-Policy': 'no-referrer', 'Cache-Control': 'no-store', 'X-Frame-Options': 'DENY', 'Content-Security-Policy': "frame-ancestors 'none'", 'Cross-Origin-Resource-Policy': 'same-origin', 'Content-Type': content_type, 'Content-Length': str(len(body))}.items():
            self.send_header(key, value)
        if cookie:
            self.send_header('Set-Cookie', f'brainstorm-key-{server.server_port}={token}; HttpOnly; SameSite=Strict; Path=/')
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.headers.get('Upgrade', '').lower() == 'websocket':
            self.websocket()
            return
        if not self.authorized():
            self.respond(403, 'Session key required', 'text/html; charset=utf-8')
            return
        activity()
        parts = urlsplit(self.path)
        if parts.path == '/' and 'key' in parse_qs(parts.query, keep_blank_values=True):
            encoded = json.dumps(token).replace('<', '\\u003c')
            self.respond(200, f"<!DOCTYPE html><title>Opening Brainstorm Companion</title><script>try {{ sessionStorage.setItem('brainstorm-session-key', {encoded}); }} catch (e) {{}} location.replace('/');</script>", 'text/html; charset=utf-8', True)
        elif parts.path == '/':
            screens = []
            for path in CONTENT.iterdir():
                if not path.name.startswith('.') and path.name.endswith('.html'):
                    try:
                        data, mtime = safe_read(path.name)
                        screens.append ( (mtime, data))
                    except OSError:
                        pass
            if screens:
                html = max(screens, key=lambda item: item[0])[1].decode('utf-8', errors='replace')
                if not html.lstrip().lower().startswith(('<!doctype', '<html')):
                    html = (HERE / 'frame-template.html').read_text().replace('<!-- CONTENT -->', html)
            else:
                html = '<!DOCTYPE html><html><body><!-- BRANDING --><h1>Brainstorm Companion</h1><p>Waiting for the agent to push a screen...</p></body></html>'
            html = html.replace('<!-- BRANDING -->', '<div class="brand"><span class="brand-copy">Visual Brainstorming</span></div>')
            helper = '<script>\n' + (HERE / 'helper.js').read_text() + '\n</script>'
            html = html.replace('</body>', helper + '\n</body>', 1) if '</body>' in html else html + helper
            self.respond(200, html, 'text/html; charset=utf-8', True)
        elif parts.path.startswith('/files/'):
            name = parts.path[7:].split('/')[-1]
            try:
                data, _ = safe_read(name)
            except OSError:
                self.respond(404, 'Not found', cookie=True)
                return
            types = {'.html':'text/html', '.css':'text/css', '.js':'application/javascript', '.json':'application/json', '.png':'image/png', '.jpg':'image/jpeg', '.jpeg':'image/jpeg', '.gif':'image/gif', '.svg':'image/svg+xml'}
            self.respond(200, data, types.get(Path(name).suffix.lower(), 'application/octet-stream'), True)
        else:
            self.respond(404, 'Not found', cookie=True)

    def websocket(self):
        origin = self.headers.get('Origin')
        key = self.headers.get('Sec-WebSocket-Key')
        try:
            valid_key = bool(key) and len(base64.b64decode(key, validate=True)) == 16
        except (ValueError, TypeError):
            valid_key = False
        connection = [part.strip().lower() for part in self.headers.get('Connection', '').split(',')]
        if (not self.authorized() or (origin and origin != 'http://' + self.headers.get('Host', ''))
                or not valid_key or self.headers.get('Sec-WebSocket-Version') != '13'
                or 'upgrade' not in connection):
            self.respond(400, 'Invalid WebSocket handshake')
            self.close_connection = True
            return
        # The WebSocket handshake specifies SHA-1 for protocol interoperability, not authentication.
        accept = base64.b64encode(hashlib.sha1((key + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11').encode(), usedforsecurity=False).digest()).decode()
        self.send_response(101, 'Switching Protocols')
        self.send_header('Upgrade', 'websocket')
        self.send_header('Connection', 'Upgrade')
        self.send_header('Sec-WebSocket-Accept', accept)
        self.end_headers()
        client = Client(self.connection)
        with lock:
            clients.add(client)
        try:
            while True:
                first, second = exact(self.rfile, 2)
                opcode = first & 15
                length = second & 127
                if (not second & 128 or not first & 128 or first & 0x70
                        or opcode not in (1, 8, 9, 10) or (opcode >= 8 and length > 125)):
                    client.send(frame(8, struct.pack('!H', 1002)), wait=True); break
                if length == 126:
                    length = struct.unpack('!H', exact(self.rfile, 2))[0]
                    if length < 126:
                        client.send(frame(8, struct.pack('!H', 1002)), wait=True); break
                elif length == 127:
                    length = struct.unpack('!Q', exact(self.rfile, 8))[0]
                    if length < 65536 or length & (1 << 63):
                        client.send(frame(8, struct.pack('!H', 1002)), wait=True); break
                if length > MAX_FRAME:
                    client.send(frame(8, struct.pack('!H', 1009)), wait=True); break
                if opcode == 8 and length == 1:
                    client.send(frame(8, struct.pack('!H', 1002)), wait=True); break
                mask = exact(self.rfile, 4)
                data = bytes(b ^ mask[i % 4] for i, b in enumerate(exact(self.rfile, length)))
                opcode = first & 15
                if opcode == 8:
                    client.send(frame(8), wait=True); break
                if opcode == 9:
                    client.send(frame(10, data))
                elif opcode == 1:
                    try:
                        event = json.loads(data.decode('utf-8', errors='replace'))
                        activity()
                        if isinstance(event, dict) and event.get('choice'):
                            safe_state_write('events', json.dumps(event) + '\n', append=True)
                        print(json.dumps({'source': 'user-event', **(event if isinstance(event, dict) else {})}), flush=True)
                    except OSError:
                        print('Failed to save user choice', file=sys.stderr, flush=True)
                        client.send(frame(1, b'{"type":"error","message":"Failed to save choice"}'))
                    except ValueError:
                        pass
                elif opcode != 10:
                    client.send(frame(8, struct.pack('!H', 1003)), wait=True); break
        except (EOFError, OSError):
            pass
        finally:
            client.close()
            self.close_connection = True

    def do_POST(self):
        self.respond(404 if self.authorized() else 403, 'Not found')


def main():
    global token, server
    if not os.environ.get('BRAINSTORM_DIR'):
        raise SystemExit('BRAINSTORM_DIR is required')
    CONTENT.mkdir(parents=True, exist_ok=True)
    STATE.mkdir(parents=True, exist_ok=True)
    token = os.environ.get('BRAINSTORM_TOKEN', '')
    source = 'env' if token else 'generated'
    if not token and TOKEN_FILE:
        try:
            candidate = Path(TOKEN_FILE).read_text().strip()
            if len(candidate) >= 32 and all(c in '0123456789abcdefABCDEF' for c in candidate):
                token, source = candidate, 'file'
        except OSError: pass
    if not token: token = secrets.token_hex(32)
    try:
        port = int(os.environ.get('BRAINSTORM_PORT', ''))
    except ValueError:
        try:
            port = int(Path(PORT_FILE).read_text()) if PORT_FILE else 0
            if not 1023 < port < 65536: port = 0
        except (OSError, ValueError): port = 0
    class Server(ThreadingHTTPServer):
        daemon_threads = True
        address_family = socket.AF_INET6 if ':' in HOST else socket.AF_INET
    fallback = False
    try:
        server = Server((HOST, port), Handler)
    except OSError as exc:
        if exc.errno != __import__('errno').EADDRINUSE or source == 'env': raise
        fallback = True
        if source == 'file': token = secrets.token_hex(32)
        server = Server((HOST, 0), Handler)
    if not fallback and PORT_FILE:
        try:
            safe_file_write(PORT_FILE, str(server.server_port))
        except OSError:
            pass
        if TOKEN_FILE:
            try:
                safe_file_write(TOKEN_FILE, token)
            except OSError:
                pass
    idle = positive('BRAINSTORM_IDLE_TIMEOUT_MS', 14400000) / 1000
    interval = positive('BRAINSTORM_LIFECYCLE_CHECK_MS', 60000) / 1000
    known = {}
    for path in CONTENT.iterdir():
        if not path.name.startswith('.') and path.name.endswith('.html'):
            try:
                data, mtime = safe_read(path.name)
                known[path.name] = (mtime, hashlib.sha256(data).digest())
            except OSError:
                pass
    info = dict(type='server-started', port=server.server_port, host=HOST, url_host=URL_HOST, url=url(), screen_dir=str(CONTENT), state_dir=str(STATE), idle_timeout_ms=idle * 1000)
    safe_state_write('server-info', json.dumps(info) + '\n')
    print(json.dumps(info), flush=True)
    owner = int(os.environ.get('BRAINSTORM_OWNER_PID', '0') or 0)
    def alive(pid):
        try: os.kill(pid, 0); return True
        except PermissionError: return True
        except OSError: return False
    if owner and not alive(owner):
        print(json.dumps(dict(type='owner-pid-invalid', pid=owner, reason='dead at startup')), flush=True)
        owner = 0
    def monitor():
        nonlocal known
        # Polling cannot observe changes that appear and disappear between scans.
        seen = set(known)
        pending = {}
        check = time.monotonic() + interval
        while True:
            time.sleep(.1)
            try:
                current = {}
                now = time.monotonic()
                for p in CONTENT.iterdir():
                    if p.name.startswith('.') or not p.name.endswith('.html'): continue
                    try:
                        data, mtime = safe_read(p.name)
                        current[p.name] = (mtime, hashlib.sha256(data).digest())
                    except OSError: continue
                    signature = current[p.name]
                    if known.get(p.name) == signature:
                        pending.pop(p.name, None)
                        continue
                    if p.name not in pending or pending[p.name][0] != signature:
                        pending[p.name] = (signature, now)
                        continue
                    if now - pending[p.name][1] < .1:
                        continue
                    activity()
                    added = p.name not in seen
                    if added:
                        seen.add(p.name)
                        (STATE / 'events').unlink(missing_ok=True)
                        maybe_open()
                    print(json.dumps(dict(type='screen-added' if added else 'screen-updated', file=str(p))), flush=True)
                    broadcast()
                    known[p.name] = signature
                    pending.pop(p.name, None)
                for name in set(known) - set(current):
                    known.pop(name, None)
                for name in set(pending) - set(current):
                    pending.pop(name, None)
            except OSError as exc:
                print('screen watch error: ' + str(exc), file=sys.stderr, flush=True)
            if time.monotonic() >= check:
                reason = 'owner process exited' if owner and not alive(owner) else 'idle timeout' if time.monotonic() - last_activity > idle else None
                if reason:
                    print(json.dumps(dict(type='server-stopped', reason=reason)), flush=True)
                    try:
                        (STATE / 'server-info').unlink(missing_ok=True)
                        (STATE / 'server-stopped').write_text(json.dumps(dict(reason=reason, timestamp=int(time.time()*1000))) + '\n')
                    except OSError as exc:
                        print('shutdown state error: ' + str(exc), file=sys.stderr, flush=True)
                    with lock:
                        snapshot = list(clients)
                    for client in snapshot:
                        client.close()
                    server.shutdown()
                    return
                check = time.monotonic() + interval
    threading.Thread(target=monitor, daemon=True).start()
    server.serve_forever()
    server.server_close()


def positive(name, default):
    try:
        value = float(os.environ.get(name, ''))
        return value if 0 < value < float('inf') else default
    except ValueError: return default


if __name__ == '__main__':
    main()
