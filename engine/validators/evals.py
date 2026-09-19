"""Validate behavior-eval scenarios (D10/ADR-0011).

Scenarios live at ``evals/scenarios/<id>/scenario.json``. The static validator
is deterministic (no LLM) and safe for CI; it checks the schema, that the
target harness exists, that every check is well-formed, and that no scenario
string carries a secret or an absolute path (D12).
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from engine.validators.hygiene import ABSOLUTE_PATH, SECRET_PATTERNS

SCENARIOS_DIR = "evals/scenarios"
CHECK_KINDS = ("contains", "not_contains", "regex")
REQUIRED = ("id", "title", "harness", "prompt", "checks", "rubric", "acceptance")
STRING_KEYS = ("id", "title", "harness", "prompt", "acceptance")


def discover(root: Path) -> list[Path]:
    base = root / SCENARIOS_DIR
    if not base.is_dir():
        return []
    return sorted(base.glob("*/scenario.json"))


def _harness_names(root: Path) -> tuple[set[str], list[str]]:
    names: set[str] = set()
    errors: list[str] = []
    harnesses_dir = root / "harnesses"
    if harnesses_dir.is_dir():
        for manifest in harnesses_dir.glob("*/harness.json"):
            try:
                names.add(json.loads(manifest.read_text(encoding="utf-8"))["name"])
            except (json.JSONDecodeError, KeyError, OSError) as exc:
                errors.append(
                    f"{manifest.relative_to(root).as_posix()}: unreadable harness manifest ({exc})"
                )
    return names, errors


def _scan_text(rel: str, field: str, value: str, errors: list[str]) -> None:
    if ABSOLUTE_PATH.search(value):
        errors.append(f"{rel}: {field} contains an absolute path (D12)")
    for label, pattern in SECRET_PATTERNS:
        if pattern.search(value):
            errors.append(f"{rel}: {field} contains a {label} (D12)")


def _all_strings(data: dict) -> list[tuple[str, str]]:
    """Every human-readable string in the scenario, for the D12 scan."""
    strings: list[tuple[str, str]] = []
    for key in STRING_KEYS:
        if isinstance(data.get(key), str):
            strings.append((key, data[key]))
    for index, check in enumerate(data.get("checks", [])):
        if isinstance(check, dict) and isinstance(check.get("value"), str):
            strings.append((f"checks[{index}].value", check["value"]))
        if isinstance(check, dict) and isinstance(check.get("reason"), str):
            strings.append((f"checks[{index}].reason", check["reason"]))
    for index, item in enumerate(data.get("rubric", [])):
        if isinstance(item, str):
            strings.append((f"rubric[{index}]", item))
    return strings


def validate(root: Path) -> list[str]:
    """Return a list of error strings; empty list means valid."""
    errors: list[str] = []
    harnesses, harness_errors = _harness_names(root)
    errors.extend(harness_errors)

    for path in discover(root):
        rel = path.relative_to(root).as_posix()
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            errors.append(f"{rel}: unreadable scenario ({exc})")
            continue
        if not isinstance(data, dict):
            errors.append(f"{rel}: scenario must be a JSON object")
            continue

        for key in REQUIRED:
            if key not in data:
                errors.append(f"{rel}: missing key {key!r}")

        for key in STRING_KEYS:
            if key in data and not isinstance(data[key], str):
                errors.append(f"{rel}: {key!r} must be a string")
        scenario_id = data.get("id")
        if isinstance(scenario_id, str) and scenario_id and scenario_id != path.parent.name:
            errors.append(
                f"{rel}: 'id' {scenario_id!r} != directory name {path.parent.name!r}"
            )
        harness = data.get("harness")
        if harness is not None:
            if not isinstance(harness, str):
                errors.append(f"{rel}: 'harness' must be a string")
            elif harness not in harnesses:
                errors.append(f"{rel}: unknown harness {harness!r}")

        checks = data.get("checks", [])
        if not isinstance(checks, list) or not checks:
            errors.append(f"{rel}: 'checks' must be a non-empty list")
        else:
            for index, check in enumerate(checks):
                if not isinstance(check, dict) or check.get("kind") not in CHECK_KINDS:
                    errors.append(f"{rel}: check {index} needs a 'kind' in {CHECK_KINDS}")
                    continue
                value = check.get("value")
                if not isinstance(value, str) or not value:
                    errors.append(f"{rel}: check {index} needs a non-empty string 'value'")
                    continue
                if check["kind"] == "regex":
                    try:
                        re.compile(value)
                    except re.error as exc:
                        errors.append(f"{rel}: check {index} bad regex ({exc})")

        rubric = data.get("rubric", [])
        if not isinstance(rubric, list) or not rubric or not all(
            isinstance(item, str) and item for item in rubric
        ):
            errors.append(f"{rel}: 'rubric' must be a non-empty list of strings")

        if not isinstance(data.get("prompt"), str) or not data.get("prompt"):
            errors.append(f"{rel}: 'prompt' is required")

        for field, value in _all_strings(data):
            _scan_text(rel, field, value, errors)
    return errors
