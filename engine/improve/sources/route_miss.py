"""Route-miss source: requests the router could not match, recorded by code.

A skill-gap is only as trustworthy as the channel and the session behind it, and
those used to be read from the record, so whoever wrote the record chose them. Here
the producer and the reader assign them in code:

- ``record_miss`` is called by the router when no agent matches. It is off unless
  ``COACUS_ROUTE_MISS_LOG=1``, because it keeps a short piece of the user's prompt.
- ``RouteMissSource.read`` rebuilds every observation itself. The ``kind`` is always
  ``route-miss``. The channel is ``human-user-turn`` only when the router ran with a
  terminal on both ends (a person typed the prompt); any other run, such as an agent
  that composed the prompt, is ``model-assistant`` and can never support a gap. The
  session comes from the producer and the claim is cut to a short length; nothing
  else in a stored record is read.

This is owner-local state under a git-ignored directory. It resists a record that
claims a channel it did not earn, not someone who can write the file and the
interactive flag together; a person still reviews every proposal.
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
LOG_PATH = Path("docs/temp/improvement/route-misses.jsonl")
MAX_CLAIM = 200
MAX_LINES = 2000
MAX_BYTES = 1_000_000
_SESSION = re.compile(r"[^A-Za-z0-9._:-]")


def _enabled() -> bool:
    return os.environ.get(ENV_SWITCH, "").strip().lower() not in ("", "0", "false", "no", "off")


def _session_id() -> str:
    """A run identifier made in code: the day and the parent process, not model text."""
    return f"route:{time.strftime('%Y-%m-%d', time.gmtime())}:{os.getppid()}"


def record_miss(root: Path, prompt: str, interactive: bool | None = None) -> bool:
    """Append one miss to the log; True when written. Never raises, never blocks the router."""
    if not _enabled() or not isinstance(prompt, str) or not prompt.strip():
        return False
    if interactive is None:
        interactive = bool(sys.stdin.isatty() and sys.stdout.isatty())
    line = json.dumps(
        {"text": prompt.strip()[:MAX_CLAIM], "interactive": bool(interactive), "session": _session_id()},
        ensure_ascii=False,
    )
    path = Path(root) / LOG_PATH
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() and (path.stat().st_size > MAX_BYTES or sum(1 for _ in path.open("rb")) >= MAX_LINES):
            return False
        with path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")
    except OSError:
        return False
    return True


class RouteMissSource(Source):
    """Read the router's own miss log; every trust field is set here, never copied."""

    name = "route-miss"

    def status(self, root: Path) -> str:
        """``present`` when a log exists; a missing log is a safe skip, not an alarm."""
        return "present" if (Path(root) / LOG_PATH).is_file() else "absent_by_config"

    def read(self, root: Path, options: dict) -> list[dict]:
        """Rebuild each logged miss as an observation with code-assigned kind, channel, session."""
        path = Path(root) / LOG_PATH
        try:
            if not path.is_file() or path.stat().st_size > MAX_BYTES:
                return []
            lines = path.read_text(encoding="utf-8").split("\n")
        except (OSError, UnicodeError):
            return []
        observations: list[dict] = []
        for line in lines[:MAX_LINES]:
            try:
                raw = json.loads(line)
            except ValueError:
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
