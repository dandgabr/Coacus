#!/usr/bin/env bash
# Coacus guardrail hook for codex (generated — do not edit).
# Calls the PAER evaluator and prints its native effect JSON.
set -euo pipefail
COACUS_ROOT="__COACUS_ROOT__"
PAYLOAD="$(cat)"
printf "%s" "$PAYLOAD" | python3 "$COACUS_ROOT/scripts/coacus_guard.py" --harness codex --event tool.pre --root "$COACUS_ROOT" 2>/dev/null || echo '{}'
