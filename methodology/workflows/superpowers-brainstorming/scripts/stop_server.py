#!/usr/bin/env python3
"""Stop the brainstorm server and clean up.

Usage: python3 stop_server.py <session_dir>
"""

from __future__ import annotations

import json
import os
import shutil
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

    session_dir = Path(args[0]).resolve()
    state_dir = session_dir / "state"
    pid_file = state_dir / "server.pid"
    server_id_file = state_dir / "server-instance-id"

    if not pid_file.is_file():
        print(json.dumps({"status": "not_running"}))
        return 0

    try:
        pid = int(pid_file.read_text(encoding="utf-8").strip())
    except Exception:
        pid_file.unlink(missing_ok=True)
        print(json.dumps({"status": "stale_pid"}))
        return 0

    # Try graceful termination
    try:
        os.kill(pid, signal.SIGTERM)
    except ProcessLookupError:
        pid_file.unlink(missing_ok=True)
        server_id_file.unlink(missing_ok=True)
        mark_stopped(state_dir, "stale_pid")
        print(json.dumps({"status": "stale_pid"}))
        return 0
    except Exception:
        pass

    # Wait up to 2s
    stopped = False
    for _ in range(20):
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            stopped = True
            break
        except Exception:
            pass
        time.sleep(0.1)

    # Force kill if still running
    if not stopped:
        try:
            os.kill(pid, signal.SIGKILL if hasattr(signal, "SIGKILL") else signal.SIGTERM)
            time.sleep(0.1)
        except Exception:
            pass

    pid_file.unlink(missing_ok=True)
    server_id_file.unlink(missing_ok=True)
    (state_dir / "server.log").unlink(missing_ok=True)
    mark_stopped(state_dir, "stop_server.py")

    # Clean up ephemeral /tmp session
    if str(session_dir).startswith("/tmp") or "brainstorm-" in session_dir.name:
        try:
            shutil.rmtree(session_dir, ignore_errors=True)
        except Exception:
            pass

    print(json.dumps({"status": "stopped"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
