"""Default episodic source: an explicitly supplied session transcript (F10).

Portable and harness-agnostic: the operator points at a JSONL file via
``--transcript``. Auto-discovery of harness-specific transcript locations is
deliberately NOT done in v1 — it is unstable and would silently read the wrong
file. An absent or malformed path is a fail-open no-op, proven by config (the
operator either passed a path or did not), never inferred from a failed probe.
"""

from __future__ import annotations

from pathlib import Path

from engine.improve.sources import Source, load_observations


class TranscriptSource(Source):
    """Read observations from a caller-supplied transcript file."""

    name = "transcript"

    def status(self, root: Path) -> str:
        """``present`` when a transcript path is configured for this run."""
        configured = root / ".coacus-transcript"
        if configured.is_file():
            return "present"
        return "absent_by_config"

    def read(self, root: Path, options: dict) -> list[dict]:
        """Read the transcript path from options; return [] when absent."""
        raw = options.get("transcript")
        if not raw:
            return []
        path = Path(raw)
        if not path.is_file():
            return []
        return load_observations(path)
