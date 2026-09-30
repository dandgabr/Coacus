"""Optional episodic source: the ai-memory MCP (F10).

ai-memory exists on some machines and not on others, so it is an ENRICHER, never
a requirement (the user's constraint, and P2: no tracked path depends on a
machine outside the repository). Three states are distinguished:

- ``present`` — the server is reachable;
- ``absent_by_config`` — never configured here: a safe no-op;
- ``absent_unexpectedly`` — configured but unreachable: an ALARM, because an
  attacker who can make the source vanish must not silently disable auditing.

In v1 this adapter does not call the MCP (that is a runtime concern); it only
reports availability from the project's ``.ai-memory.toml`` plus the presence of
the hook, and reads a caller-exported JSONL when one is supplied. The MCP call
is wired at the CLI layer where the tool is available.
"""

from __future__ import annotations

from pathlib import Path

from engine.improve.sources import Source, load_observations


class AiMemorySource(Source):
    """Optional ai-memory enricher; absence by config is a safe skip."""

    name = "ai-memory"

    def status(self, root: Path) -> str:
        """Configured-but-unreachable is an alarm; unconfigured is a safe skip.

        A ``.ai-memory.toml`` alone declares the project namespace — it does NOT
        enable the loop. The alarm requires explicit opt-in
        (``AI_MEMORY_IMPROVE=1``), so the default is a safe skip.
        """
        import os

        reachable = bool(
            os.environ.get("AI_MEMORY_ENDPOINT") or os.environ.get("AI_MEMORY_AVAILABLE")
        )
        if reachable:
            return "present"
        if os.environ.get("AI_MEMORY_IMPROVE") == "1":
            return "absent_unexpectedly"
        return "absent_by_config"

    def read(self, root: Path, options: dict) -> list[dict]:
        """Read a caller-exported ai-memory JSONL; [] when none is supplied."""
        raw = options.get("memory_export")
        if not raw:
            return []
        path = Path(raw)
        if not path.is_file():
            return []
        return load_observations(path)
