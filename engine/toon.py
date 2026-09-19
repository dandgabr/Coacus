"""TOON (Token-Oriented Object Notation) payload parsing and validation (D7/ADR-0008).

TOON is the compact handoff format between agents:

    @FROM: <emitter>
    @TO: <receiver-or-orchestrator>
    @STATUS: <OK | CONFLICT | BLOCKED | NEED_INFO>
    @CTX: <context id>
    @FILES: <path:lines>;<path:lines>       (optional, relative paths only)
    @SUMMARY: <compact summary>
    @ACTION_NEEDED: <objective next step>    (optional)

JSON is reserved for machine contracts; TOON is for prose handoffs.
"""

from __future__ import annotations

import re

STATUSES = ("OK", "CONFLICT", "BLOCKED", "NEED_INFO")
REQUIRED = ("@FROM", "@TO", "@STATUS", "@CTX", "@SUMMARY")
OPTIONAL = ("@FILES", "@ACTION_NEEDED")

_LINE = re.compile(r"^(@[A-Z_]+):\s*(.*)$")
# Any absolute path: POSIX root, Windows drive, home expansion, or `..` escape.
_ABSOLUTE_PATH = re.compile(r"^(/|[A-Za-z]:[/\\]|~|\.\.)")
_SECRETS = re.compile(
    r"(AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{20,}|xox[baprs]-[A-Za-z0-9-]{10,}"
    r"|-----BEGIN [A-Z ]*PRIVATE KEY-----)"
)


def parse(text: str) -> dict[str, str]:
    """Parse a TOON payload into a field->value mapping (duplicates: last wins)."""
    fields: dict[str, str] = {}
    for raw in text.splitlines():
        match = _LINE.match(raw.strip())
        if match:
            fields[match.group(1)] = match.group(2).strip()
    return fields


def _duplicates(text: str) -> list[str]:
    seen: set[str] = set()
    dupes: list[str] = []
    for raw in text.splitlines():
        match = _LINE.match(raw.strip())
        if match:
            field = match.group(1)
            if field in seen and field not in dupes:
                dupes.append(field)
            seen.add(field)
    return dupes


def validate(text: str) -> list[str]:
    """Return a list of error strings; empty list means a valid payload."""
    errors: list[str] = []
    fields = parse(text)
    if not fields:
        return ["payload has no @FIELD lines"]

    for field in _duplicates(text):
        errors.append(f"duplicate field {field}")

    for field in REQUIRED:
        if field not in fields:
            errors.append(f"missing required field {field}")
        elif not fields[field]:
            errors.append(f"{field} is empty")

    status = fields.get("@STATUS", "")
    if status and status not in STATUSES:
        errors.append(f"@STATUS must be one of {STATUSES}, got {status!r}")

    unknown = set(fields) - set(REQUIRED) - set(OPTIONAL)
    for field in sorted(unknown):
        errors.append(f"unknown field {field}")

    # Secrets must not appear in ANY field (summary/action included).
    for field, value in fields.items():
        if _SECRETS.search(value):
            errors.append(f"{field} contains a secret-like literal")

    files = fields.get("@FILES", "")
    if files:
        for entry in files.split(";"):
            entry = entry.strip()
            if not entry:
                continue
            # Keep the full entry for the secret scan; a trailing `:<range>`
            # (or a bare `:N`) is not part of the path.
            path = re.sub(r"(:\d+(-\d+)?)?$", "", entry)
            if not path:
                errors.append(f"@FILES entry has no path: {entry!r}")
                continue
            if _ABSOLUTE_PATH.match(path):
                errors.append(f"@FILES path must be relative: {path!r}")
            if ".." in path.split("/"):
                errors.append(f"@FILES path must not escape upward: {path!r}")
    return errors


def is_valid(text: str) -> bool:
    return not validate(text)
