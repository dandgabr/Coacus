"""Validate the advisory security-pattern catalogue (lifecycle-guardrails).

The catalogue is DATA; this validator keeps it well-formed and append-only:
unique positive integer ids, known fields and operators, compiling regexes, a
reminder (the mitigation) on every rule, and every frozen id still present.
"""

from __future__ import annotations

from pathlib import Path

from engine.guardrail import rules


def validate(root: Path) -> list[str]:
    """Return catalogue errors; empty means valid (or absent — see below)."""
    catalogue = rules.load_catalogue(root)
    if catalogue is None:
        # A missing file is not an error here: the catalogue is optional data.
        return []
    return rules.lint_errors(catalogue)


def warnings(root: Path) -> list[str]:
    """Return non-blocking findings; empty means clean."""
    catalogue = rules.load_catalogue(root)
    if catalogue is None:
        return []
    return rules.lint_warnings(catalogue)
