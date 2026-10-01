#!/usr/bin/env python3
"""SessionStart bootstrap runner for Shape A harnesses (cross-platform, stdlib only).

Emits the exact single-key native JSON payload:
- additionalContext (for Claude Code, Codex, Command Code)
- additional_context (for Cursor)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    """Emit the single-key native JSON SessionStart payload."""
    args = argv if argv is not None else sys.argv[1:]
    # Either pass json path directly or emit piped payload
    if args:
        payload_path = Path(args[0])
        if payload_path.is_file():
            sys.stdout.write(payload_path.read_text(encoding="utf-8"))
            return 0

    print("Usage: python3 session_start.py <path_to_payload.json>")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
