"""Repository hygiene validators (D2 anti-tools, D12 paths/secrets).

Scans canonical source directories (never ``dist/`` derived content, never
``docs/`` evidence) for:

- absolute paths (``/home/``, ``/Users/``, ``/root/``, ``~``, ``C:\\``/``C:/``)
- secret-shaped literals — use ``{env:VAR}``
- harness tool names inside canonical skill bodies (D2). ``references/``
  directories are exempt: they are the sanctioned home for tool mappings.

The tool-name denylist is the union of the built-in seed and every
``harnesses/*/harness.json`` ``tool_denylist`` (D2 derivation, F3).
"""

from __future__ import annotations

import json
import re
from pathlib import Path

SCAN_ROOTS = ("knowledge", "methodology", "verticals", "harnesses", "templates")

ABSOLUTE_PATH = re.compile(
    r"(/home/|/Users/|/root/|(?<![A-Za-z0-9])[A-Za-z]:[/\\]|~[A-Za-z0-9_.-]*/)"
)

SECRET_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("aws-access-key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("github-token", re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}")),
    ("slack-token", re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}")),
    ("private-key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    (
        "credential-assignment",
        re.compile(
            r"(?i)\b(api[_-]?key|secret|password|passwd|token)\b\s*[:=]\s*"
            r"[\"']?(?!\{env:)(?!\$\{)[^\s\"']{8,}"
        ),
    ),
]

# Seed denylist of harness tool names (ADR-0003). Ambiguous English words
# (Read/Write/Edit/Task/Glob/Grep) are intentionally excluded to avoid false
# positives on legitimate prose. Harness vocabularies extend this set.
BUILTIN_TOOL_NAMES = [
    "Bash", "MultiEdit", "WebFetch", "WebSearch", "TodoWrite", "NotebookEdit",
    "google_web_search", "read_file", "write_file", "list_directory",
    "run_command",
]

# Anti-tools applies to canonical skill bodies, authoring templates, the
# bootstrap wrapper and the workflow skills. ``references/`` directories are
# exempt (the sanctioned home for tool mappings).
ANTI_TOOL_ROOTS = (
    "knowledge/skills",
    "methodology/workflows",
    "methodology/bootstrap",
    "templates/authoring",
)


def _harness_tool_names(root: Path) -> set[str]:
    names: set[str] = set()
    harnesses_dir = root / "harnesses"
    if not harnesses_dir.is_dir():
        return names
    for manifest in harnesses_dir.glob("*/harness.json"):
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        for name in data.get("tool_denylist", []) or []:
            names.add(str(name))
    return names


def _tool_reference(root: Path) -> re.Pattern[str]:
    names = sorted(set(BUILTIN_TOOL_NAMES) | _harness_tool_names(root))
    return re.compile(
        r"(?<![`\w])(" + "|".join(re.escape(n) for n in names) + r")(?![`\w])"
    )


def validate(root: Path) -> list[str]:
    """Return a list of error strings; empty list means clean."""
    errors: list[str] = []
    tool_reference = _tool_reference(root)
    for top in SCAN_ROOTS:
        base = root / top
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.md")):
            rel = path.relative_to(root).as_posix()
            if "/dist/" in f"/{rel}":
                continue  # derived content is checked by drift, not hygiene
            text = path.read_text(encoding="utf-8", errors="replace")
            for lineno, line in enumerate(text.splitlines(), 1):
                if ABSOLUTE_PATH.search(line):
                    errors.append(f"{rel}:{lineno}: absolute path detected (D12)")
                for label, pattern in SECRET_PATTERNS:
                    if pattern.search(line):
                        errors.append(
                            f"{rel}:{lineno}: possible {label} — use {{env:VAR}} (D12)"
                        )
            is_canonical_skill = rel.startswith(ANTI_TOOL_ROOTS)
            if is_canonical_skill and "/references/" not in f"/{rel}":
                for lineno, line in enumerate(text.splitlines(), 1):
                    hit = tool_reference.search(line)
                    if hit:
                        errors.append(
                            f"{rel}:{lineno}: harness tool name in canonical "
                            f"content: {hit.group(1)} (D2)"
                        )
    return errors
