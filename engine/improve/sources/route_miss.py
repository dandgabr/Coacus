"""Route-miss source: requests the router could not match, recorded by code.

A skill-gap is only as trustworthy as the channel and the session behind it, and
those used to be read from the record, so whoever wrote the record chose them. Here
the producer and the reader assign them in code:

- ``record_miss`` is called by the router when no agent matches. It is off unless
  ``COACUS_ROUTE_MISS_LOG=1``, because it keeps a short piece of the user's prompt.
- ``RouteMissSource.read`` rebuilds every observation itself. The ``kind`` is always
  ``route-miss``. The channel is ``human-user-turn`` only when the router ran with a
  terminal on both ends and no harness session marker in the environment; any other run
  is ``model-assistant`` and can never support a gap. The session is the UTC date of the
  miss, so a gap needs the same request on three different dates. The reader trusts the
  ``interactive`` and ``session`` values the producer wrote, and nothing else in a line.
- The log lives in the user's state directory (``COACUS_STATE_DIR``, else
  ``$XDG_STATE_HOME/coacus``, else ``~/.local/state/coacus``), never in a repository:
  a repository someone else wrote cannot ship a log, no ``.gitignore`` has to be right,
  and the file is private: the directory and the file must be owned by the user and not
  readable or writable by anyone else, and no symlink is followed. A location that is
  relative, inside the repository being read, or not private is refused, so an
  environment variable set by a cloned repository cannot point the loop at its own log.

Threat model: this keeps text that an agent was fed from becoming trusted evidence
without a person at a terminal on three dates. The terminal test is a heuristic: a harness
that runs commands under a pseudo-terminal and sets no session marker passes it, and so
does an agent that forges the log or edits a policy. A person still reviews every
proposal and nothing is applied. The source needs POSIX; on Windows the producer writes nothing.
"""

from __future__ import annotations

import json
import os
import re
import stat
import sys
import tempfile
import time
from pathlib import Path

from engine.improve.sources import Source

try:
    import fcntl
except ImportError:  # Windows: the producer is off there
    fcntl = None

ENV_SWITCH = "COACUS_ROUTE_MISS_LOG"
LOG_NAME = "route-misses.jsonl"
MAX_CLAIM = 200
MAX_LINES = 2000
MAX_BYTES = 1_000_000
_SESSION = re.compile(r"[^A-Za-z0-9._:-]")


def _enabled() -> bool:
    return os.environ.get(ENV_SWITCH, "").strip().lower() not in ("", "0", "false", "no", "off")


def log_path(root: Path | None = None) -> Path | None:
    """The miss log in the user's state directory, or None when the location is refused.

    Refused: a relative path, and any path inside ``root`` (the repository being read).
    """
    base = os.environ.get("COACUS_STATE_DIR")
    if base:
        path = Path(base) / LOG_NAME
    else:
        state = os.environ.get("XDG_STATE_HOME") or str(Path.home() / ".local" / "state")
        path = Path(state) / "coacus" / LOG_NAME
    if not path.is_absolute():
        return None
    if root is not None:
        try:
            path.resolve().relative_to(Path(root).resolve())
            return None
        except ValueError:
            pass
    return path


def _private(info: os.stat_result, directory: bool) -> bool:
    """True for an entry owned by this user that no one else can read or write."""
    kind = stat.S_ISDIR(info.st_mode) if directory else stat.S_ISREG(info.st_mode)
    return kind and info.st_uid == os.geteuid() and info.st_mode & 0o077 == 0


def _directory_ok(directory: Path) -> bool:
    """Create the state directory private, and refuse a symlink or a shared one."""
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    return _private(os.lstat(directory), True)


def _tail_lines(fd: int) -> list[bytes]:
    """Whole lines from the last ``MAX_BYTES`` of an open log, newest last, at most ``MAX_LINES``."""
    size = os.fstat(fd).st_size
    os.lseek(fd, max(0, size - MAX_BYTES), os.SEEK_SET)
    data = os.read(fd, MAX_BYTES) if size else b""
    lines = data.split(b"\n")
    if size > MAX_BYTES:
        lines = lines[1:]  # the first line is cut
    if not data.endswith(b"\n"):
        lines = lines[:-1]  # the last line is unfinished
    return [line for line in lines if line.strip()][-MAX_LINES:]


def _open_log(path: Path, flags: int) -> int:
    """Open without following a symlink or blocking on a FIFO; refuse anything not private."""
    fd = os.open(path, flags | os.O_NOFOLLOW | os.O_NONBLOCK | getattr(os, "O_CLOEXEC", 0), 0o600)
    try:
        if not _private(os.fstat(fd), False):
            raise OSError("miss log is not a private regular file")
    except BaseException:
        os.close(fd)
        raise
    return fd


def _agent_session(root: Path, environ) -> bool:
    """True when a harness session marker from the harness data is set in the environment."""
    try:
        for data in (Path(root) / "harnesses").glob("*/harness.json"):
            markers = json.loads(data.read_text(encoding="utf-8")).get("session_markers", [])
            if isinstance(markers, list) and any(isinstance(m, str) and environ.get(m) for m in markers):
                return True
    except (OSError, ValueError):
        return True  # cannot tell: do not claim a person
    return False


def record_miss(root: Path, prompt: str, interactive: bool | None = None) -> bool:
    """Append one miss to the log; True when written. Never raises, never blocks the router.

    ``root`` is the Coacus root: the log may not live inside it, and it holds the harness
    data that names the session markers.
    """
    if os.name != "posix" or fcntl is None or not _enabled() or not isinstance(prompt, str) or not prompt.strip():
        return False
    if interactive is None:
        interactive = bool(sys.stdin.isatty() and sys.stdout.isatty()) and not _agent_session(root, os.environ)
    path = log_path(root)
    if path is None:
        return False
    line = json.dumps(
        {"text": prompt.strip()[:MAX_CLAIM], "interactive": bool(interactive),
         "session": "route:" + time.strftime("%Y-%m-%d", time.gmtime())},
        ensure_ascii=False,
    ).encode("utf-8", "replace") + b"\n"
    temporary = None
    try:
        if not _directory_ok(path.parent):
            return False
        lock = os.open(path.parent / (LOG_NAME + ".lock"), os.O_WRONLY | os.O_CREAT | os.O_NOFOLLOW, 0o600)
        with os.fdopen(lock, "wb"):
            fcntl.flock(lock, fcntl.LOCK_EX)
            fd = _open_log(path, os.O_RDWR | os.O_CREAT)
            try:
                size = os.fstat(fd).st_size
                if size + len(line) > MAX_BYTES or size > 0 and len(_tail_lines(fd)) >= MAX_LINES:
                    kept = _tail_lines(fd)
                    kept = kept[len(kept) // 2:]  # full: keep the newest half
                    handle, temporary = tempfile.mkstemp(dir=path.parent, prefix=LOG_NAME + ".")
                    with os.fdopen(handle, "wb") as out:
                        out.write(b"".join(item + b"\n" for item in kept))
                        out.flush()
                        os.fsync(out.fileno())
                    os.replace(temporary, path)
                    temporary = None
                    os.close(fd)
                    fd = _open_log(path, os.O_WRONLY | os.O_APPEND)
                else:
                    os.lseek(fd, 0, os.SEEK_END)
                os.write(fd, line)
            finally:
                os.close(fd)
    except (OSError, UnicodeError, ValueError):
        return False
    finally:
        if temporary:
            try:
                os.unlink(temporary)
            except OSError:
                pass
    return True


class RouteMissSource(Source):
    """Read the router's own miss log; every trust field is set here, never copied."""

    name = "route-miss"

    def status(self, root: Path) -> str:
        """``present`` when a readable log exists; a missing one is a safe skip, not an alarm."""
        path = log_path(root)
        return "present" if path is not None and path.is_file() else "absent_by_config"

    def read(self, root: Path, options: dict) -> list[dict]:
        """Rebuild each logged miss as an observation with code-assigned kind, channel, session."""
        path = log_path(root)
        if os.name != "posix" or path is None:
            return []
        try:
            if not _private(os.lstat(path.parent), True):
                return []
            fd = _open_log(path, os.O_RDONLY)
            try:
                lines = _tail_lines(fd)
            finally:
                os.close(fd)
        except (OSError, UnicodeError):
            return []
        observations: list[dict] = []
        for line in lines:
            try:
                raw = json.loads(line.decode("utf-8"))
            except (ValueError, UnicodeError):
                continue
            text = raw.get("text") if isinstance(raw, dict) else None
            if not isinstance(text, str) or not text.strip():
                continue
            session = _SESSION.sub("", str(raw.get("session", "")))[:64] or "route:unknown"
            observations.append({
                "kind": "route-miss",
                "channel": "human-user-turn" if raw.get("interactive") is True else "model-assistant",
                "session_id": session,
                "text": text.strip()[:MAX_CLAIM],
                "id": f"route-miss-{len(observations) + 1}",
            })
        return observations
