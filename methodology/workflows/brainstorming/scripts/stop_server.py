#!/usr/bin/env python3
"""Stop the brainstorm server and clean up.

Usage: python3 stop_server.py <session_dir>
"""

from __future__ import annotations

import json
import os
import select
import signal
import sys
import time
from pathlib import Path


def mark_stopped(state_dir: Path, reason: str) -> None:
    (state_dir / "server-info").unlink(missing_ok=True)
    payload = {"reason": reason, "timestamp": int(time.time())}
    (state_dir / "server-stopped").write_text(json.dumps(payload) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if not args:
        print(json.dumps({"error": "Usage: stop_server.py <session_dir>"}))
        return 1

    session_path = Path(os.path.abspath(args[0]))
    # Reject symlinks before resolving; resolving first loses the evidence.
    try:
        for component in (session_path, *session_path.parents):
            if component.is_symlink():
                raise ValueError("symlink in session path")
        if (session_path / "state").is_symlink():
            raise ValueError("symlink state directory")
    except (OSError, ValueError):
        print(json.dumps({"error": "Untrusted session or state directory"}))
        return 1
    session_dir = session_path
    state_dir = session_dir / "state"
    pid_file = state_dir / "server.pid"
    server_id_file = state_dir / "server-instance-id"

    if not pid_file.is_file():
        print(json.dumps({"status": "not_running"}))
        return 0

    try:
        pid = int(pid_file.read_text(encoding="utf-8").strip())
    except (OSError, ValueError):
        print(json.dumps({"error": "Invalid server PID"}))
        return 1

    # A pidfd prevents signalling a different process if the PID is reused.
    pidfd = None
    try:
        if pid <= 0 or not hasattr(os, "pidfd_open") or not hasattr(signal, "pidfd_send_signal"):
            raise ValueError("unverifiable PID")
        try:
            pidfd = os.pidfd_open(pid)
        except ProcessLookupError:
            pid_file.unlink(missing_ok=True)
            server_id_file.unlink(missing_ok=True)
            mark_stopped(state_dir, "stale_pid")
            print(json.dumps({"status": "stale_pid"}))
            return 0
        server_id = server_id_file.read_text(encoding="utf-8").strip()
        if len(server_id) != 48 or any(c not in "0123456789abcdef" for c in server_id):
            raise ValueError("invalid server identity")
        cmdline = Path(f"/proc/{pid}/cmdline").read_bytes().split(b"\0")
        if f"--brainstorm-server-id={server_id}".encode() not in cmdline or not any(
            Path(os.fsdecode(arg)).name in ("server.py", "server.cjs") for arg in cmdline
        ):
            raise ValueError("process identity mismatch")
    except (OSError, ValueError, OverflowError):
        if pidfd is not None:
            os.close(pidfd)
        print(json.dumps({"error": "Cannot verify server process identity"}))
        return 1

    # Try graceful termination
    try:
        signal.pidfd_send_signal(pidfd, signal.SIGTERM)
    except OSError:
        os.close(pidfd)
        print(json.dumps({"error": "Unable to signal server"}))
        return 1

    stopped = bool(select.select([pidfd], [], [], 2)[0])
    if not stopped:
        try:
            signal.pidfd_send_signal(pidfd, signal.SIGKILL)
            stopped = bool(select.select([pidfd], [], [], 2)[0])
        except OSError:
            pass
    os.close(pidfd)
    if not stopped:
        print(json.dumps({"error": "Server did not stop"}))
        return 1

    pid_file.unlink(missing_ok=True)
    server_id_file.unlink(missing_ok=True)
    (state_dir / "server.log").unlink(missing_ok=True)
    mark_stopped(state_dir, "stop_server.py")

    # Session contents are user data; a path or marker cannot prove ownership.
    print(json.dumps({"status": "stopped"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
