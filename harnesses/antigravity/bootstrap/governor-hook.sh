#!/usr/bin/env bash
# Coacus governor hook for Antigravity (generated — do not edit).
# Install: copy to <config>/config/plugins/coacus/governor-hook.sh and wire it in
# ~/.gemini/config/hooks.json under the "coacus-governor" key (or the plugin's
# hooks.json). Bridges Antigravity lifecycle hooks to the shared Coacus governor
# (scripts/coacus_governor.py). The payload on stdin is protojson camelCase:
# toolCall.name, conversationId, stepIdx, error.
#   - pretool : acquire a slot before a subagent spawn.
#   - posttool: release the slot, or mark PAUSED on a rate-limit (429).
#   - preinv  : inject the concurrency budget + retry contract.

set -euo pipefail

COACUS_ROOT="__COACUS_ROOT__"
GOV="${ORCH_GOVERNOR:-${COACUS_ROOT}/scripts/coacus_governor.py}"
MAX_TOTAL="${ORCH_MAX_CONCURRENT:-5}"

PAY_FILE="$(mktemp)"
cat > "$PAY_FILE"
trap 'rm -f "$PAY_FILE"' EXIT

json_value() {
  GO_PATH="$1" python3 - "$PAY_FILE" <<'PYEOF'
import json, os, sys
path = os.environ["GO_PATH"].split(".")
try:
    cur = json.load(open(sys.argv[1]))
except Exception:
    sys.exit(0)
for p in path:
    if isinstance(cur, dict) and p in cur:
        cur = cur[p]
    else:
        sys.exit(0)
if isinstance(cur, (str, int, float)) or cur is None:
    sys.stdout.write("" if cur is None else str(cur))
PYEOF
}

slot_id() {
  local conv step
  conv="$(json_value conversationId || true)"
  step="$(json_value stepIdx || true)"
  echo "agy-${conv:-none}-${step:-none}"
}

RATE_RE='(429|Too Many Requests|rate.?limit|quota exceeded|RPM|TPM|tokens_per_minute|tokens per minute)'

case "${1:-}" in
  pretool)
    tool="$(json_value toolCall.name || true)"
    case "$tool" in
      invoke_subagent|manage_subagents|task)
        python3 "$GOV" acquire "$(slot_id)" no 30 "$MAX_TOTAL" >/dev/null 2>&1 || true
        echo '{}'
        ;;
      *) echo '{}' ;;
    esac
    ;;
  posttool)
    err="$(json_value error || true)"
    if [ -n "$err" ] && echo "$err" | grep -qiE "$RATE_RE"; then
      python3 "$GOV" fail "$(slot_id)" 2>/dev/null || true
      GO_MSG="Rate-limit (429) detected in a spawned agent. Mark that task PAUSED, wait until fewer than ${MAX_TOTAL} agents run (counting you), then relaunch it with exponential backoff. Do NOT relaunch while the cap is saturated." \
        python3 -c 'import json, os; print(json.dumps({"ephemeralMessage": os.environ["GO_MSG"]}))'
    else
      python3 "$GOV" release "$(slot_id)" 2>/dev/null || true
      echo '{}'
    fi
    ;;
  preinv)
    status="$(python3 "$GOV" status "$MAX_TOTAL" 2>/dev/null | head -1 || echo "running=0 paused=0 max=$MAX_TOTAL slots_free=$MAX_TOTAL")"
    GO_STATUS="$status" GO_CAP="$MAX_TOTAL" python3 -c 'import json, os
cap = os.environ["GO_CAP"]; status = os.environ["GO_STATUS"]
msg = ("[CONCURRENCY GOVERNOR] Max concurrent agents counting the orchestrator = " + cap
       + ". Current ledger: " + status
       + ". Do not spawn a new subagent while running >= cap: enqueue it (QUEUED) and wait"
       + " for a running agent to finish. If a subagent fails with HTTP 429 / Too Many"
       + " Requests / quota, kill it, mark it PAUSED, wait until running < cap and relaunch"
       + " with exponential backoff.")
print(json.dumps({"injectSteps": [{"ephemeralMessage": msg}]}))'
    ;;
  *) echo '{}' ;;
esac
exit 0
