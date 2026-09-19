"""Repository hygiene validators (D2 anti-tools, D12 paths/secrets).

Scans canonical source directories (never ``dist/`` derived content, never
``docs/`` evidence) for:

- absolute paths (``/home/``, ``/Users/``, ``/root/``, ``C:\\``) — D12
- secret-shaped literals — D12 (use ``{env:VAR}``)
- harness tool names inside canonical skill bodies — D2

The tool-name denylist is seeded built-in; once ``harnesses/*/harness.json``
vocabularies exist (F3+), the denylist is derived from them instead.
"""

from __future__ import annotations

import re
from pathlib import Path

SCAN_ROOTS = ("knowledge", "methodology", "verticals", "harnesses", "templates")

ABSOLUTE_PATH = re.compile(r"(/home/|/Users/|/root/|[A-Za-z]:[/\\]|~[A-Za-z0-9_.-]*/)")

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

# Seed denylist of harness tool names (ADR-0003). Canonical content must
# prescribe ACTIONS, not these names. Ambiguous English words
# (Read/Write/Edit/Task/Glob/Grep) are intentionally excluded to avoid false
# positives on legitimate prose; extend via harness vocabularies later.
BUILTIN_TOOL_NAMES = [
    "Bash", "MultiEdit", "WebFetch", "WebSearch", "TodoWrite", "NotebookEdit",
    "google_web_search", "read_file", "write_file", "list_directory",
    "run_command",
]

_tool_reference = re.compile(
    r"(?<![`\w])(" + "|".join(re.escape(t) for t in BUILTIN_TOOL_NAMES) + r")(?![`\w])"
)

# Anti-tools applies to canonical skill bodies and authoring templates only.
ANTI_TOOL_ROOTS = ("knowledge/skills", "templates/authoring", "methodology/workflows")


def validate(root: Path) -> list[str]:
    """Return a list of error strings; empty list means clean."""
    errors: list[str] = []
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
                    errors.append(
                        f"{rel}:{lineno}: absolute path detected (D12)"
                    )
                for label, pattern in SECRET_PATTERNS:
                    if pattern.search(line):
                        errors.append(
                            f"{rel}:{lineno}: possible {label} — use {{env:VAR}} (D12)"
                        )
            if rel.startswith(ANTI_TOOL_ROOTS):
                for lineno, line in enumerate(text.splitlines(), 1):
                    hit = _tool_reference.search(line)
                    if hit:
                        errors.append(
                            f"{rel}:{lineno}: harness tool name in canonical "
                            f"content: {hit.group(1)} (D2)"
                        )
    return errors
