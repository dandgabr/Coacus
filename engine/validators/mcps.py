"""Validate canonical MCP sources (D4/ADR-0005 as amended at F3).

Source contract only; the generated dist/ coherence and orphan detection live
in ``engine.generators.mcp_configs.check`` (artifact layer), so an edited source
never deadlocks ``generate``.
"""

from __future__ import annotations

import re
from pathlib import Path

from engine.frontmatter import FrontmatterError, parse
from engine.generators.mcp_configs import TRANSPORTS, discover_sources

KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
ENV_NAME = re.compile(r"^[A-Z][A-Z0-9_]*$")


def validate(root: Path) -> list[str]:
    """Return a list of error strings; empty list means valid."""
    errors: list[str] = []
    seen: set[str] = set()
    for source in discover_sources(root):
        rel = source.relative_to(root).as_posix()
        try:
            doc = parse(source.read_text(encoding="utf-8"))
        except FrontmatterError as exc:
            errors.append(f"{rel}: {exc}")
            continue
        meta = doc.meta
        name = str(meta.get("name", "")).strip()
        transport = str(meta.get("transport", "")).strip()

        if not KEBAB.match(name):
            errors.append(f"{rel}: 'name' must be kebab-case, got {name!r}")
        if source.parent.name != name:
            errors.append(
                f"{rel}: directory name {source.parent.name!r} != name {name!r}"
            )
        if name in seen:
            errors.append(f"{rel}: duplicate MCP name {name!r} (flat namespace)")
        seen.add(name)
        if not str(meta.get("description", "")).strip():
            errors.append(f"{rel}: 'description' is required")
        if transport not in TRANSPORTS:
            errors.append(
                f"{rel}: 'transport' must be one of {TRANSPORTS}, got {transport!r}"
            )

        has_command = bool(str(meta.get("command", "")).strip())
        has_url = bool(str(meta.get("remote_url", "")).strip())
        if transport == "stdio" and not has_command:
            errors.append(f"{rel}: stdio transport requires 'command'")
        if transport in ("http", "streamable-http", "sse") and not has_url:
            errors.append(f"{rel}: {transport} transport requires 'remote_url'")

        capabilities = meta.get("capabilities")
        if capabilities is not None and not isinstance(capabilities, dict):
            errors.append(f"{rel}: 'capabilities' must be a mapping")

        env_vars = meta.get("env_vars")
        if env_vars is not None and not isinstance(env_vars, list):
            errors.append(f"{rel}: 'env_vars' must be a list of names")
        else:
            for var in env_vars or []:
                if not ENV_NAME.match(str(var)):
                    errors.append(
                        f"{rel}: env var {var!r} must be an upper-case name "
                        "(values never live in the repository)"
                    )
    return errors
