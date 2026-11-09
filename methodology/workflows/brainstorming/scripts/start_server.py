#!/usr/bin/env python3
"""Start the brainstorm server and output connection info.

Usage: python3 start_server.py [--project-dir <path>] [--host <bind-host>] [--url-host <display-host>] [--foreground] [--background]
"""

from __future__ import annotations

import argparse
import json
import os
import secrets
import signal
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path


def is_port_in_use(port: int, host: str = "127.0.0.1") -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0


def default_session_dir(session_id: str) -> Path:
    """Return the per-session directory beneath the platform temp directory."""
    return Path(tempfile.gettempdir()).resolve() / f"brainstorm-{session_id}"


def supports_safe_stop() -> bool:
    return (sys.platform == "linux" and hasattr(os, "pidfd_open")
            and hasattr(signal, "pidfd_send_signal") and Path("/proc/self/cmdline").is_file())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Start the brainstorm server")
    parser.add_argument("--project-dir", default="")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--url-host", default="")
    parser.add_argument("--idle-timeout-minutes", type=int, default=240)
    parser.add_argument("--open", action="store_true")
    parser.add_argument("--foreground", "--no-daemon", action="store_true")
    parser.add_argument("--background", "--daemon", action="store_true")
    args = parser.parse_args(argv)

    url_host = args.url_host
    if not url_host:
        url_host = "localhost" if args.host in ("127.0.0.1", "localhost") else args.host

    foreground = args.foreground
    if not foreground and not args.background:
        if os.environ.get("CODEX_CI") or not supports_safe_stop():
            foreground = True

    if not foreground and not supports_safe_stop():
        print(json.dumps({"error": "Background mode requires Linux pidfd and procfs; use --foreground"}))
        return 1

    session_id = f"{os.getpid()}-{int(time.time())}"
    if args.project_dir:
        project_root = Path(args.project_dir) / ".coacus" / "brainstorm"
        project_root.mkdir(parents=True, exist_ok=True)
        session_dir = Path(tempfile.mkdtemp(prefix=f"{session_id}-", dir=project_root))
        port_file = str(Path(args.project_dir) / ".coacus" / "brainstorm" / ".last-port")
        token_file = str(Path(args.project_dir) / ".coacus" / "brainstorm" / ".last-token")
    else:
        session_dir = Path(tempfile.mkdtemp(prefix="brainstorm-"))
        port_file = ""
        token_file = None

    state_dir = session_dir / "state"
    pid_file = state_dir / "server.pid"
    log_file = state_dir / "server.log"
    server_id_file = state_dir / "server-instance-id"

    (session_dir / "content").mkdir(parents=True, exist_ok=True)
    state_dir.mkdir(parents=True, exist_ok=True)

    if pid_file.exists():
        print(json.dumps({"error": "Session PID file already exists; refusing to replace it"}))
        return 1

    server_id = secrets.token_hex(24)
    server_id_file.write_text(server_id + "\n", encoding="utf-8")
    if os.name != "nt":
        try:
            os.chmod(server_id_file, 0o600)
        except Exception:
            pass

    script_dir = Path(__file__).resolve().parent
    env = dict(os.environ)
    env["BRAINSTORM_DIR"] = str(session_dir)
    env["BRAINSTORM_HOST"] = args.host
    env["BRAINSTORM_URL_HOST"] = url_host
    if args.open:
        env["BRAINSTORM_OPEN"] = "1"
    if args.idle_timeout_minutes:
        env["BRAINSTORM_IDLE_TIMEOUT_MS"] = str(args.idle_timeout_minutes * 60 * 1000)
    if port_file:
        env["BRAINSTORM_PORT_FILE"] = port_file
    if token_file:
        env["BRAINSTORM_TOKEN_FILE"] = token_file

    server_cmd = [sys.executable, "server.py", f"--brainstorm-server-id={server_id}"]

    if foreground:
        proc = subprocess.Popen(server_cmd, cwd=script_dir, env=env)
        pid_file.write_text(str(proc.pid), encoding="utf-8")
        return proc.wait()

    # Background spawn
    with open(log_file, "w", encoding="utf-8") as out:
        proc = subprocess.Popen(
            server_cmd,
            cwd=script_dir,
            env=env,
            stdout=out,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )

    pid_file.write_text(str(proc.pid), encoding="utf-8")

    # Wait for server-started in log
    for _ in range(50):
        if log_file.is_file():
            text = log_file.read_text(encoding="utf-8", errors="replace")
            for line in text.splitlines():
                if "server-started" in line:
                    time.sleep(0.2)
                    if proc.poll() is not None:
                        print(json.dumps({"error": "Server started but exited prematurely."}))
                        return 1
                    print(line)
                    return 0
        time.sleep(0.1)

    print(json.dumps({"error": "Server failed to start within 5 seconds"}))
    return 1


if __name__ == "__main__":
    import tempfile
    raise SystemExit(main())
