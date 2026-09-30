"""Generate the harness lifecycle/capability matrix (F9.3).

Writes ``docs/reference/lifecycle-matrix.md`` from every ``harness.json``
``lifecycle`` block, joining the canonical event taxonomy
(``methodology/lifecycle/events.json``) with each harness's declared capability.

Every cell carries its EVIDENCE CLASS and resolved anchor — a generated boolean
would launder an unverified vendor claim into apparent authority, which the
version-freshness rule forbids. The output is timestamp-free and drift-checked
like every other generated artifact (generated-artifacts).
"""

from __future__ import annotations

import json
from pathlib import Path

from engine.generators.bootstrap import discover_harnesses, load_harness
from engine.guardrail import evaluate as guard_eval

MATRIX_PATH = "docs/reference/lifecycle-matrix.md"


def _events(root: Path) -> list[dict]:
    path = root / guard_eval.EVENTS_PATH
    if not path.is_file():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("events", [])


def build(root: Path) -> str:
    """Render the capability matrix as Markdown."""
    events = _events(root)
    harnesses = []
    for manifest_path in discover_harnesses(root):
        harness = load_harness(manifest_path, root)
        harnesses.append(harness)
    harnesses.sort(key=lambda h: h["name"])

    lines = [
        "# Harness Lifecycle Capability Matrix",
        "",
        "> GENERATED from `harnesses/*/harness.json` and "
        "`methodology/lifecycle/events.json` by `scripts/coacus.py generate` — do not edit.",
        "",
        "Each cell is `support / can_block / effect / evidence`. A harness without",
        "a `lifecycle` block is a closed capability (no events, nothing installable).",
        "",
    ]
    header = "| Event | Class | " + " | ".join(h["name"] for h in harnesses) + " |"
    divider = "|---|---|" + "---|" * len(harnesses)
    lines += [header, divider]
    for event in events:
        row = [f"`{event['id']}`", event.get("class", "")]
        for harness in harnesses:
            lifecycle = harness.get("lifecycle", {})
            cap = (lifecycle.get("events", {}) or {}).get(event["id"])
            if not lifecycle.get("supported"):
                row.append("closed")
            elif not cap:
                row.append("unsupported")
            else:
                support = cap.get("support", "none")
                block = "B" if cap.get("can_block") else "-"
                effect = cap.get("effect") or "-"
                evidence = cap.get("evidence", "unverified")
                row.append(f"{support} / {block} / {effect} / {evidence}")
        lines.append("| " + " | ".join(row) + " |")

    lines += [
        "",
        "## Declared gaps",
        "",
    ]
    for harness in harnesses:
        gaps = harness.get("lifecycle", {}).get("gaps", []) or []
        for gap in gaps:
            lines.append(
                f"- **{harness['name']}** `{gap.get('event')}` — {gap.get('status')}: "
                f"{gap.get('reason')}"
            )
    lines.append("")
    return "\n".join(lines)


def write(root: Path) -> Path:
    """Write the matrix to disk and return its path."""
    out = root / MATRIX_PATH
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build(root), encoding="utf-8")
    return out


def check(root: Path) -> list[str]:
    """Drift check for the generated matrix (generated-artifacts)."""
    target = root / MATRIX_PATH
    if not target.is_file():
        return [f"{MATRIX_PATH}: missing (run generate)"]
    if target.read_text(encoding="utf-8") != build(root):
        return [f"{MATRIX_PATH}: out of date (run generate)"]
    return []
