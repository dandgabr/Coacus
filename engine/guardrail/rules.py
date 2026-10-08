"""Declarative content rules for the guardrail layer (PAER observe extension).

A rule is ``field x operator x pattern``, with all conditions AND-combined,
evaluated against a payload mapping. A match produces an ADVISORY — this layer
never denies (an observe binding can only surface, never block). Rules are pure
data in ``methodology/lifecycle/patterns/``; this module is the stdlib-only
evaluator and the lint that keeps the data honest.

Registry hygiene: rule ids are FROZEN and append-only. ``FROZEN_RULE_IDS`` records
the ids that must exist; adding a rule means a new id, never a renumber, so an
id that disappears is a build error rather than a silent shift.

Failure is fail-open and visible: a bad regex yields a lint error, and at runtime
a non-compiling pattern simply does not match.
"""

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path

CATALOGUE_PATH = "methodology/lifecycle/patterns/security_patterns.json"
FIELDS = ("command", "content", "new_text", "file_path", "old_text", "user_prompt")
OPERATORS = (
    "regex_match",
    "contains",
    "equals",
    "not_contains",
    "starts_with",
    "ends_with",
)
# Frozen at authoring: every id below MUST remain present. New rules append.
FROZEN_RULE_IDS = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)


def load_catalogue(root: Path) -> dict | None:
    """Load the security-pattern catalogue; ``None`` when the file is missing."""
    path = root / CATALOGUE_PATH
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


@lru_cache(maxsize=256)
def _compiled(pattern: str) -> re.Pattern[str] | None:
    """Compile a regex once; ``None`` when it does not compile (fail-open)."""
    try:
        return re.compile(pattern, re.IGNORECASE)
    except re.error:
        return None


def _values(payload: dict, field: str) -> list[str]:
    value = payload.get(field)
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        return [str(item) for item in value]
    return [str(value)]


def _match_one(operator: str, pattern: str, value: str) -> bool:
    if operator == "contains":
        return pattern in value
    if operator == "not_contains":
        return pattern not in value
    if operator == "equals":
        return value == pattern
    if operator == "starts_with":
        return value.startswith(pattern)
    if operator == "ends_with":
        return value.endswith(pattern)
    if operator == "regex_match":
        compiled = _compiled(pattern)
        return compiled is not None and compiled.search(value) is not None
    return False


def matches(rule: dict, payload: dict) -> bool:
    """True when every field condition of the rule matches the payload."""
    operator = str(rule.get("operator", ""))
    pattern = str(rule.get("pattern", ""))
    field = str(rule.get("field", ""))
    values = _values(payload, field)
    if not values:
        return False
    return any(_match_one(operator, pattern, value) for value in values)


def evaluate(payload: dict, catalogue: dict) -> list[dict]:
    """Return the matching rules as advisory records (id, rule, severity, reminder)."""
    hits: list[dict] = []
    for rule in catalogue.get("patterns", []):
        if matches(rule, payload):
            hits.append(
                {
                    "id": rule.get("id"),
                    "rule": rule.get("rule"),
                    "severity": rule.get("severity", "medium"),
                    "reminder": rule.get("reminder", ""),
                }
            )
    return hits


def _is_over_broad(rule: dict) -> bool:
    """A one- or two-character pattern matches far too much to be signal."""
    operator = str(rule.get("operator", ""))
    pattern = str(rule.get("pattern", ""))
    return operator in ("regex_match", "contains") and len(pattern) < 3


def lint_errors(catalogue: dict) -> list[str]:
    """Structural errors in the catalogue (blocking)."""
    errors: list[str] = []
    seen: set[int] = set()
    patterns = catalogue.get("patterns", [])
    if not isinstance(patterns, list):
        return [f"{CATALOGUE_PATH}: 'patterns' must be a list"]
    for index, rule in enumerate(patterns):
        where = f"{CATALOGUE_PATH}[{index}]"
        rid = rule.get("id")
        if not isinstance(rid, int) or rid < 1:
            errors.append(f"{where}: 'id' must be a positive integer")
        elif rid in seen:
            errors.append(f"{where}: duplicate rule id {rid}")
        else:
            seen.add(rid)
        if not str(rule.get("rule", "")).strip():
            errors.append(f"{where}: 'rule' name is required")
        if str(rule.get("field", "")) not in FIELDS:
            errors.append(f"{where}: unknown field {rule.get('field')!r}")
        operator = str(rule.get("operator", ""))
        if operator not in OPERATORS:
            errors.append(f"{where}: unknown operator {operator!r}")
        if not str(rule.get("pattern", "")).strip():
            errors.append(f"{where}: 'pattern' is required")
        elif operator == "regex_match" and _compiled(str(rule["pattern"])) is None:
            errors.append(f"{where}: 'pattern' is not a valid regular expression")
        if not str(rule.get("reminder", "")).strip():
            errors.append(f"{where}: 'reminder' (the mitigation) is required")
    missing = set(FROZEN_RULE_IDS) - seen
    if missing:
        errors.append(
            f"{CATALOGUE_PATH}: frozen rule id(s) removed: {sorted(missing)} "
            "(ids are frozen and append-only)"
        )
    return errors


def lint_warnings(catalogue: dict) -> list[str]:
    """Non-blocking findings: a pattern too broad to carry signal."""
    notes: list[str] = []
    for index, rule in enumerate(catalogue.get("patterns", [])):
        if _is_over_broad(rule):
            notes.append(
                f"{CATALOGUE_PATH}[{index}]: pattern {rule.get('pattern')!r} is too "
                "broad and will match unrelated content"
            )
    return notes
