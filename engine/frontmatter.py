"""Frontmatter parser for Coacus canonical sources.

Tolerant subset of YAML, sufficient for the reference corpus (testing:
stdlib only):

- single-line scalars, with indented continuation lines (multi-line plain)
- folded/literal block scalars: ``>-`` / ``>`` / ``|`` / ``|-``
- block lists (``- item``) and inline lists (``[a, b]`` / ``[]``)
- nested indented maps to any depth (e.g. the ``metadata:`` blocks found in
  49 of the 200 reference skills)

Unknown/extra keys are preserved as-is; the validators decide the canonical
contract. The closing ``---`` must sit at column 0.
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


_KEY_LINE = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*)$")
_BLOCK_MARKERS = {">-", ">", "|", "|-"}
_INLINE_LIST = re.compile(r"^\[.*\]$")


def _indent_of(line: str) -> int:
    return len(line) - len(line.lstrip())


def _scalar(text: str) -> str:
    text = text.strip()
    if len(text) >= 2 and text[0] == text[-1] and text[0] in "\"'":
        return text[1:-1]
    return text


def _inline_items(text: str) -> list[str]:
    inner = text.strip()[1:-1].strip()
    if not inner:
        return []
    return [_scalar(part) for part in _split_inline(inner) if part.strip()]


def _split_inline(text: str) -> list[str]:
    """Split an inline list on top-level commas (commas inside quotes survive)."""
    parts: list[str] = []
    current: list[str] = []
    quote: str | None = None
    for char in text:
        if quote:
            current.append(char)
            if char == quote:
                quote = None
        elif char in "\"'":
            quote = char
            current.append(char)
        elif char == ",":
            parts.append("".join(current))
            current = []
        else:
            current.append(char)
    parts.append("".join(current))
    return parts


def _parse_value(
    lines: list[str], i: int, end: int, value: str, parent_indent: int
) -> tuple[object, int]:
    """Parse the value of one key, consuming continuation/child lines."""
    if value in _BLOCK_MARKERS:
        block: list[str] = []
        while i < end and (not lines[i].strip() or _indent_of(lines[i]) > parent_indent):
            block.append(lines[i].strip())
            i += 1
        while block and not block[-1]:
            block.pop()
        return " ".join(part for part in block if part), i

    if _INLINE_LIST.match(value):
        return _inline_items(value), i

    if value == "":
        j = i
        while j < end and not lines[j].strip():
            j += 1
        if j < end:
            child = lines[j].strip()
            child_indent = _indent_of(lines[j])
            # block sequence may sit at the same indent as its parent key
            if child.startswith("- ") and child_indent >= parent_indent:
                return _parse_block(lines, i, end)
            if child_indent > parent_indent and _KEY_LINE.match(child):
                return _parse_block(lines, i, end)
        return _multiline_scalar(lines, i, end, parent_indent, first="")

    quoted = value[:1] in ('"', "'")
    text, i = _multiline_scalar(lines, i, end, parent_indent, first=_scalar(value))
    return (_scalar(text) if quoted else text), i


def _multiline_scalar(
    lines: list[str], i: int, end: int, parent_indent: int, first: str
) -> tuple[str, int]:
    parts = [first] if first else []
    while i < end and (not lines[i].strip() or _indent_of(lines[i]) > parent_indent):
        parts.append(lines[i].strip())
        i += 1
    while parts and not parts[-1]:
        parts.pop()
    return " ".join(part for part in parts if part), i


def _parse_block(lines: list[str], i: int, end: int) -> tuple[object, int]:
    """Parse an indented block (list or mapping) starting at index ``i``."""
    while i < end and not lines[i].strip():
        i += 1
    if i >= end:
        return "", i
    base_indent = _indent_of(lines[i])

    if lines[i].strip().startswith("- "):
        items: list[str] = []
        while i < end:
            line = lines[i]
            if not line.strip():
                i += 1
                continue
            ind = _indent_of(line)
            if ind < base_indent:
                break
            stripped = line.strip()
            if stripped.startswith("- ") and ind == base_indent:
                items.append(_scalar(stripped[2:]))
                i += 1
            elif ind > base_indent and items:
                items[-1] = f"{items[-1]} {_scalar(stripped)}"
                i += 1
            else:
                break
        return items, i

    result: dict = {}
    while i < end:
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if _indent_of(line) < base_indent:
            break
        match = _KEY_LINE.match(line.strip())
        if not match:
            break
        key, value = match.group(1), match.group(2).strip()
        i += 1
        parsed, i = _parse_value(lines, i, end, value, base_indent)
        result[key] = parsed
    return result, i


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

    meta, consumed = _parse_block(lines, 1, close)
    if consumed < close:
        leftover = next(
            (line for line in lines[consumed:close] if line.strip()), None
        )
        if leftover is not None:
            raise FrontmatterError(f"cannot parse line: {leftover!r}")
    if not isinstance(meta, dict):
        raise FrontmatterError("frontmatter root must be a mapping")

    body = "\n".join(lines[close + 1:]).strip() + "\n"
    return Document(meta=meta, body=body)
