"""Generate per-MCP harness declarations from a single canonical source (D4).

Supersedes the hand-authored MCP triple of ADR-0005: `knowledge/mcps/<mcp>/MCP.md`
is the single source; the generator derives:

- `dist/mcp.json`         server declaration (name, transport, command/url,
                          args, ``{env:VAR}`` placeholders, capabilities)
- `dist/mcp_config.json`  setup metadata (description, requires, env VAR names,
                          docs, author, license, version)

Generated files are committed and drift-checked (ADR-0014), contain no
timestamps, and never carry secret values.
"""

from __future__ import annotations

import json
from pathlib import Path

from engine.frontmatter import parse

SOURCE_NAME = "MCP.md"
DIST_DIR = "dist"
TRANSPORTS = ("stdio", "http", "streamable-http", "sse")
_CAPABILITY_KEYS = ("tools", "resources", "prompts")


def discover_sources(root: Path) -> list[Path]:
    """Canonical MCP sources: ``knowledge/mcps/<mcp>/MCP.md`` (flat)."""
    mcps_dir = root / "knowledge" / "mcps"
    if not mcps_dir.is_dir():
        return []
    return sorted(mcps_dir.glob(f"*/{SOURCE_NAME}"))


def _as_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if str(item).strip()]


def _as_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in ("true", "1", "yes", "on")


def generate(source_path: Path, root: Path) -> dict[str, str]:
    """Compute ``dist/mcp.json`` and ``dist/mcp_config.json`` for one MCP."""
    doc = parse(source_path.read_text(encoding="utf-8"))
    meta = doc.meta
    name = str(meta.get("name", "")).strip()
    transport = str(meta.get("transport", "")).strip()
    env_vars = _as_list(meta.get("env_vars"))
    command = str(meta.get("command", "")).strip()
    args = _as_list(meta.get("args"))
    remote_url = str(meta.get("remote_url", "")).strip()

    capabilities: dict[str, bool] = {}
    raw_capabilities = meta.get("capabilities")
    if isinstance(raw_capabilities, dict):
        for key in _CAPABILITY_KEYS:
            if key in raw_capabilities:
                capabilities[key] = _as_bool(raw_capabilities[key])

    server: dict[str, object] = {
        "name": name,
        "transport": transport,
        "capabilities": capabilities,
    }
    if command:
        server["command"] = command
    if args:
        server["args"] = args
    if remote_url:
        server["url"] = remote_url
    if env_vars:
        server["env"] = {var: "{env:" + var + "}" for var in env_vars}

    config: dict[str, object] = {
        "name": name,
        "description": str(meta.get("description", "")).strip(),
        "requires": _as_list(meta.get("requires")),
        "env_vars": env_vars,
    }
    for key in ("docs", "author", "license", "version"):
        value = str(meta.get(key, "")).strip()
        if value:
            config[key] = value

    dist_rel = (source_path.parent / DIST_DIR).relative_to(root).as_posix()
    return {
        f"{dist_rel}/mcp.json": json.dumps(server, indent=2) + "\n",
        f"{dist_rel}/mcp_config.json": json.dumps(config, indent=2) + "\n",
    }


def expected_outputs(root: Path) -> dict[str, str]:
    """Union of generated content for every canonical MCP source."""
    outputs: dict[str, str] = {}
    for source in discover_sources(root):
        outputs.update(generate(source, root))
    return outputs


def write_all(root: Path) -> list[str]:
    """Materialize all generated MCP files. Returns repo-relative paths."""
    written: list[str] = []
    for rel, content in expected_outputs(root).items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        written.append(rel)
    return sorted(written)


def check(root: Path) -> list[str]:
    """Drift check: expected vs disk, plus orphan detection (ADR-0014)."""
    drift: list[str] = []
    expected = expected_outputs(root)
    for rel, content in expected.items():
        path = root / rel
        if not path.is_file():
            drift.append(f"{rel}: missing (run generate)")
        elif path.read_text(encoding="utf-8") != content:
            drift.append(f"{rel}: out of date (run generate)")

    mcps_dir = root / "knowledge" / "mcps"
    actual: set[str] = set()
    if mcps_dir.is_dir():
        for dist in mcps_dir.glob(f"*/{DIST_DIR}"):
            for path in dist.rglob("*"):
                if path.is_file():
                    actual.add(path.relative_to(root).as_posix())
    for rel in sorted(actual - set(expected)):
        drift.append(f"{rel}: orphan (source removed — delete or restore it)")
    return sorted(drift)
