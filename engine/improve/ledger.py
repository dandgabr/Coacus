"""The proposal ledger (F10 step 5) — artifact class C (committed-not-generated).

Two records, split (D6):

- the RUNTIME ledger, gitignored, per-session, timestamped, never drift-checked;
- the CURATED ledger, committed only after human review, like ``sources.lock.json``.

Neither is written by ``generate``; neither is in the generated surface. This
module only serializes and appends; the promotion (apply) is a separate, human,
PR-only step that does not exist in v1 (D7).
"""

from __future__ import annotations

import json
import os
from pathlib import Path

RUNTIME_LEDGER = "docs/temp/improvement/ledger.jsonl"
CURATED_LEDGER = "docs/decisions/proposals.jsonl"


def _append(path: Path, record: dict) -> None:
    """Atomically append one JSON record as a line."""
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(record, sort_keys=True) + "\n"
    with path.open("a", encoding="utf-8") as fh:
        fh.write(line)
        fh.flush()
        os.fsync(fh.fileno())


def append_runtime(root: Path, record: dict) -> Path:
    """Append a proposal record to the gitignored runtime ledger."""
    path = root / RUNTIME_LEDGER
    _append(path, record)
    return path


def read_runtime(root: Path) -> list[dict]:
    """Read the runtime ledger records (empty when absent)."""
    path = root / RUNTIME_LEDGER
    if not path.is_file():
        return []
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return records
