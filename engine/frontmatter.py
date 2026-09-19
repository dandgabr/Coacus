"""Minimal frontmatter parser for Coacus canonical sources.

Supports the strict subset used by canonical artifacts:

- ``key: value`` (single-line scalar, quotes optional)
- ``key: []`` (empty list)
- ``key: >-`` / ``>`` / ``|`` / ``|-`` followed by indented lines (block scalar,
  folded; ``|`` is treated as folded too — canonical bodies are prose)
- ``key:`` followed by ``  - item`` lines (list of scalars)

Frontmatter is delimited by a ``---`` line, then a closing ``---`` line.
Zero external dependencies (ADR-0011: deterministic stdlib-only infra).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


class FrontmatterError(ValueError):
    """Raised when frontmatter cannot be parsed."""


@dataclass
class Document:
    """Parsed canonical source: metadata plus markdown body."""

    meta: dict = field(default_factory=dict)
    body: str = ""

    @property
    def title(self) -> str:
        """First ``# H1`` of the body, or an empty string."""
        for line in self.body.splitlines():
            if line.startswith("# "):
                return line[2:].strip()
        return ""


_BLOCK_MARKERS = {"-", ">-", ">", "|", "|-"}
_KEY_LINE = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*)$")
_LIST_ITEM = re.compile(r"^\s+-\s+(.*)$")


def parse(text: str) -> Document:
    """Parse ``---``-delimited frontmatter plus a markdown body."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise FrontmatterError("missing opening '---' delimiter")
    close = None
    for i in range(1, len(lines)):
        if lines[i] == "---":  # closing delimiter must be at column 0
            close = i
            break
    if close is None:
        raise FrontmatterError("missing closing '---' delimiter")

    meta: dict = {}
    i = 1
    while i < close:
        raw = lines[i]
        if not raw.strip():
            i += 1
            continue
        match = _KEY_LINE.match(raw)
        if not match:
            raise FrontmatterError(f"cannot parse line {i + 1}: {raw!r}")
        key, value = match.group(1), match.group(2).strip()
        i += 1
        if value in _BLOCK_MARKERS:
            block: list[str] = []
            while i < close and (lines[i].startswith(("  ", "\t")) or not lines[i].strip()):
                block.append(lines[i].strip())
                i += 1
            while block and not block[-1]:
                block.pop()
            meta[key] = " ".join(part for part in block if part)
        elif value == "":
            items: list[str] = []
            while i < close:
                item = _LIST_ITEM.match(lines[i])
                if not item:
                    break
                items.append(item.group(1).strip().strip("'\""))
                i += 1
            meta[key] = items
        elif value == "[]":
            meta[key] = []
        elif value.startswith("["):
            raise FrontmatterError(
                f"line {i}: inline lists are not supported — use a block list"
            )
        else:
            meta[key] = value.strip("'\"")

    body = "\n".join(lines[close + 1:]).strip() + "\n"
    return Document(meta=meta, body=body)
