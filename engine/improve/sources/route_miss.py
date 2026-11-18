"""Route-miss source: requests the router could not match, recorded by code.

A skill-gap is only as trustworthy as the channel and the session behind it, and
those used to be read from the record, so whoever wrote the record chose them. Here
the producer and the reader assign them in code:

- ``record_miss`` is called by the router when no agent matches. It is off unless
  ``COACUS_ROUTE_MISS_LOG=1``, because it keeps a short piece of the user's prompt.
- ``RouteMissSource.read`` rebuilds every observation itself. The ``kind`` is always
  ``route-miss``. The channel is ``human-user-turn`` only when the router ran with a
  terminal on both ends; any other run, such as a harness that composed the prompt and
  ran the router without a terminal, is ``model-assistant`` and can never support a gap.
  The session is the UTC day of the miss, so a gap needs the same request on three
  different days. Nothing else in a stored line is read.
- The log lives in the user's state directory (``COACUS_STATE_DIR``, else
  ``$XDG_STATE_HOME/coacus``, else ``~/.local/state/coacus``), never in a repository:
  a repository someone else wrote cannot ship a log, no ``.gitignore`` has to be right,
  and the file is private (``0600`` in a ``0700`` directory, no symlink followed).

Threat model: this keeps text that an agent was fed from becoming trusted evidence
without a person at a terminal on three days. It does not stop an agent that has a
shell and deliberately forges the log (a pseudo-terminal passes the terminal test, and
the same agent could edit a policy); a person still reviews every proposal and nothing
is applied. The source needs POSIX; on Windows the producer writes nothing.
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path

from engine.improve.sources import Source

ENV_SWITCH = "COACUS_ROUTE_MISS_LOG"
LOG_NAME = "route-misses.jsonl"
MAX_CLAIM = 200
MAX_LINES = 2000
MAX_BYTES = 1_000_000
_SESSION = re.compile(r"[^A-Za-z0-9._:-]")


def _enabled() -> bool:
    return os.environ.get(ENV_SWITCH, "").strip().lower() not in ("", "0", "false", "no", "off")


def log_path() -> Path:
    """The miss log: in the user's state directory, never inside a repository."""
    base = os.environ.get("COACUS_STATE_DIR")
    if base:
        return Path(base) / LOG_NAME
    state = os.environ.get("XDG_STATE_HOME") or str(Path.home() / ".local" / "state")
    return Path(state) / "coacus" / LOG_NAME


def _session_id() -> str:
    """The UTC day, made in code: a gap needs the same request on three different days."""
    return "route:" + time.strftime("%Y-%m-%d", time.gmtime())


def _lines(path: Path) -> list[bytes]:
    """Whole lines of the log, from at most the first ``MAX_BYTES`` bytes (a cut last line is dropped)."""
    with open(path, "rb") as handle:
        data = handle.read(MAX_BYTES + 1)
    lines = data.split(b"\n")
    if len(data) > MAX_BYTES or not data.endswith(b"\n"):
        lines = lines[:-1]
    return [line for line in lines if line.strip()][:MAX_LINES]


def _open_private(path: Path, flags: int):
    return os.open(path, flags | os.O_NOFOLLOW | getattr(os, "O_CLOEXEC", 0), 0o600)


def record_miss(root: Path, prompt: str, interactive: bool | None = None) -> bool:
    """Append one miss to the log; True when written. Never raises, never blocks the router.

    ``root`` is accepted for the caller's convenience and ignored: the log is per user.
    """
    if os.name != "posix" or not _enabled() or not isinstance(prompt, str) or not prompt.strip():
        return False
    if interactive is None:
        interactive = bool(sys.stdin.isatty() and sys.stdout.isatty())
    line = json.dumps(
        {"text": prompt.strip()[:MAX_CLAIM], "interactive": bool(interactive), "session": _session_id()},
        ensure_ascii=False,
    ).encode("utf-8", "replace") + b"\n"
    path = log_path()
    try:
        path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        kept: list[bytes] = []
        if path.exists():
            kept = _lines(path)
            size = sum(len(item) + 1 for item in kept) + len(line)
            if len(kept) >= MAX_LINES or size > MAX_BYTES:
                # Full: keep the newest half so the log never stops recording or grows without bound.
                kept = kept[len(kept) // 2:]
                temporary = path.with_name(path.name + f".{os.getpid()}.tmp")
                fd = _open_private(temporary, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
                with os.fdopen(fd, "wb") as handle:
                    handle.write(b"".join(item + b"\n" for item in kept))
                os.replace(temporary, path)
        fd = _open_private(path, os.O_WRONLY | os.O_APPEND | os.O_CREAT)
        with os.fdopen(fd, "wb") as handle:
            handle.write(line)
    except (OSError, UnicodeError):
        return False
    return True


class RouteMissSource(Source):
    """Read the router's own miss log; every trust field is set here, never copied."""

    name = "route-miss"

    def status(self, root: Path) -> str:
        """``present`` when a log exists; a missing log is a safe skip, not an alarm."""
        return "present" if log_path().is_file() else "absent_by_config"

    def read(self, root: Path, options: dict) -> list[dict]:
        """Rebuild each logged miss as an observation with code-assigned kind, channel, session."""
        path = log_path()
        try:
            if os.name != "posix" or path.is_symlink() or not path.is_file():
                return []
            lines = _lines(path)
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
