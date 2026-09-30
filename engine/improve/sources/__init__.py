"""Pluggable episodic-source registry (F10).

Unlike ``engine/dispatcher``'s module-global registry, this is an INSTANTIABLE
object with explicit ``register``/``clear`` so the loop is unit-testable in
isolation and carries no import-order state.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Protocol

SOURCE_STATUSES = ("present", "absent_by_config", "absent_unexpectedly")


class Source(Protocol):
    """An episodic source: a name, a status probe, and a read of observations."""

    name: str

    def status(self, root: Path) -> str:
        """Return one of ``SOURCE_STATUSES`` for this machine."""
        ...

    def read(self, root: Path, options: dict) -> list[dict]:
        """Return raw observations for a session (empty list when unavailable)."""
        ...


class SourceRegistry:
    """An instantiable registry of episodic sources."""

    def __init__(self) -> None:
        self._sources: dict[str, Source] = {}

    def register(self, source: Source) -> None:
        """Register a source under its name (idempotent overwrite)."""
        self._sources[source.name] = source

    def clear(self) -> None:
        """Forget every registered source (test isolation)."""
        self._sources.clear()

    def names(self) -> list[str]:
        """Registered source names, sorted."""
        return sorted(self._sources)

    def get(self, name: str) -> Source | None:
        """Return a registered source or None."""
        return self._sources.get(name)

    def available(self, root: Path) -> list[str]:
        """Names whose status is ``present`` for this machine."""
        return sorted(
            name for name, src in self._sources.items() if src.status(root) == "present"
        )


def load_observations(path: Path) -> list[dict]:
    """Read a transcript JSONL into observations; malformed lines are skipped.

    The contract is deliberately minimal and explicit: one JSON object per line.
    A malformed file is rejected by the caller (fail-open no-op), never crashed
    on.
    """
    observations: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            observations.append(obj)
    return observations


def register_builtin(registry: SourceRegistry) -> None:
    """Register the built-in sources (transcript default; ai-memory optional)."""
    from engine.improve.sources.ai_memory import AiMemorySource
    from engine.improve.sources.transcript import TranscriptSource

    registry.register(TranscriptSource())
    registry.register(AiMemorySource())
