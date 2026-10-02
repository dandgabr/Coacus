#!/usr/bin/env python3
"""SessionStart bootstrap runner for Shape A harnesses (cross-platform, stdlib only).

Emits the exact single-key native JSON payload:
- hookSpecificOutput.additionalContext (for Claude Code, Codex, Command Code)
- additional_context (for Cursor)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    """Emit the single-key native JSON SessionStart payload."""
    args = argv if argv is not None else sys.argv[1:]
    if args:
        payload_path = Path(args[0])
        if payload_path.is_file():
            root = Path(__file__).resolve().parents[1].as_posix()
            def resolve(value):
                if isinstance(value, str):
                    return value.replace("__COACUS_ROOT__", root)
                if isinstance(value, dict):
                    return {key: resolve(item) for key, item in value.items()}
                if isinstance(value, list):
                    return [resolve(item) for item in value]
                return value
            payload = json.loads(payload_path.read_text(encoding="utf-8"))
            sys.stdout.write(json.dumps(resolve(payload)) + "\n")
            return 0

    print("Usage: python coacus_session_start.py <path_to_payload.json>", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
