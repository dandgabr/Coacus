"""Per-harness plugin renderers, dispatched by a data-driven kind registry (D8).

Before this module the plugin seam lived inside ``bootstrap.py`` and was keyed by
harness NAME with Python-literal bodies, and it was unreachable whenever
``bootstrap.supported`` was false. That made a peer lifecycle layer (guardrails)
impossible: a harness with hooks but no bootstrap could not be rendered.

This module owns the algorithm; ``harness.json`` owns the facts:

- ``plugins[]`` entries declare ``kind`` and an output ``path``.
- ``_REGISTRY`` maps a ``kind`` to a renderer.
- An unknown kind renders nothing (a deliberate, test-pinned contract: routing is
  user-invoked only, so a declared ``router-hook`` must not silently render).

``guardrails`` registers its kind on import; a new kind is a new registration
(OCP: data changes when new data arrives, the engine changes when a new CONCEPT
arrives).
"""

from __future__ import annotations

import json
from pathlib import Path

_REGISTRY: dict[str, "object"] = {}


def register(kind: str, renderer) -> None:
    """Register a renderer for a plugin kind (idempotent overwrite)."""
    _REGISTRY[kind] = renderer


def registered_kinds() -> list[str]:
    """Known plugin kinds, sorted (for validators and tests)."""
    return sorted(_REGISTRY)


def native_context_json(native_key: str, event_name: str, text: str) -> str:
    """Build a single-key native JSON context payload.

    Supports a nested key (``hookSpecificOutput.additionalContext``, which needs
    ``hookEventName``) and a flat key (``additional_context``). The emitted
    object carries exactly one native context key (session-start-bootstrap).
    ``event_name`` is parameterised so a guardrail bound to ``PreToolUse`` does
    not inherit the bootstrap's ``SessionStart`` literal.
    """
    escaped = json.dumps(text)[1:-1]
    if "." in native_key:
        outer, inner = native_key.split(".", 1)
        return (
            "{\n"
            f'  "{outer}": {{\n'
            f'    "hookEventName": "{event_name}",\n'
            f'    "{inner}": "{escaped}"\n'
            "  }\n"
            "}"
        )
    return '{\n  "' + native_key + '": "' + escaped + '"\n}'


def _antigravity_governor_hook() -> str:
    """The Antigravity governor hook: bridges lifecycle hooks to the governor.

    Antigravity has no in-process module, so governance is a shell hook wired via
    ``hooks.json`` (key ``coacus-governor``). It reads the protojson payload on
    stdin (``toolCall.name``, ``conversationId``, ``stepIdx``, ``error``) and
    calls ``scripts/coacus_governor.py`` (orchestration-governance).
    """
    return r'''#!/usr/bin/env bash
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
'''


def _opencode_governor_gate() -> str:
    """The OpenCode governor gate plugin (JS), moved out of bootstrap.py."""
    return (
        "// Coacus governor gate for opencode (generated — do not edit).\n"
        "// Install: copy to <harness config>/plugins/coacus-governor.js.\n"
        "// It intercepts `task` (subagent spawn), acquires a slot from the\n"
        "// Coacus governor and ABORTS the spawn when no slot is free (the\n"
        "// cap is enforced, not advisory). A rate-limit (429) in the result\n"
        "// parks the caller as PAUSED for the orchestrator to retry with\n"
        "// backoff (orchestration-governance).\n"
        "\n"
        "import { execFileSync } from 'node:child_process';\n"
        "\n"
        "const COACUS_ROOT = '__COACUS_ROOT__';\n"
        "const GOVERNOR = COACUS_ROOT + '/scripts/coacus_governor.py';\n"
        "const MAX_TOTAL = String(process.env.ORCH_MAX_CONCURRENT ?? 5);\n"
        "const MAX_CALLS = 3;\n"
        "const SPAWN_TOOLS = new Set(['task']);\n"
        "const RATE_LIMIT_RE = /(429|Too Many Requests|rate.?limit|quota exceeded|RPM|TPM)/i;\n"
        "\n"
        "// caller -> {token, calls}; kept on the plugin instance, never in args.\n"
        "const held = new Map();\n"
        "\n"
        "/**\n"
        " * Invoke the Coacus governor CLI.\n"
        " *\n"
        " * @param {string} action - Governor action (acquire, release, fail, ...).\n"
        " * @param {string} caller - Stable caller identity for the ledger slot.\n"
        " * @param {string} [timeout='5'] - Seconds to wait for a free slot.\n"
        " * @param {string} [orchestrator='no'] - 'yes' if the caller orchestrates.\n"
        " * @returns {string} The governor token on success, or '' on failure/cap.\n"
        " */\n"
        "const gov = (action, caller, timeout = '5', orchestrator = 'no') => {\n"
        "  try {\n"
        "    return execFileSync(\n"
        "      'python3',\n"
        "      [GOVERNOR, action, caller, orchestrator, timeout, MAX_TOTAL],\n"
        "      { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'], timeout: 70000 },\n"
        "    ).trim();\n"
        "  } catch { return ''; }\n"
        "};\n"
        "\n"
        "/**\n"
        " * Governor gate plugin: enforce the concurrency cap on subagent spawns.\n"
        " *\n"
        " * Acquires a ledger slot before a `task` spawn and aborts it when no slot\n"
        " * is free; releases the slot after, parking the caller as PAUSED on a\n"
        " * detected rate limit.\n"
        " *\n"
        " * @returns {Promise<object>} The plugin hook map.\n"
        " */\n"
        "export const CoacusGovernor = async () => ({\n"
        "  'tool.execute.before': async (input, output) => {\n"
        "    if (!SPAWN_TOOLS.has(input.tool ?? '')) return;\n"
        "    const caller = `${input.tool}-${input.sessionID ?? 'sess'}-${input.callID ?? Date.now()}`;\n"
        "    const token = gov('acquire', caller, '30');\n"
        "    if (!token) {\n"
        "      throw new Error(\n"
        "        'Coacus governor: concurrency cap reached; no slot free. ' +\n"
        "        'Retry after a running agent completes (cap = ' + MAX_TOTAL + ').',\n"
        "      );\n"
        "    }\n"
        "    held.set(caller, { token, calls: 0 });\n"
        "    // Do NOT mutate output.args (it would leak into the subagent payload).\n"
        "  },\n"
        "  'tool.execute.after': async (input, output) => {\n"
        "    if (!SPAWN_TOOLS.has(input.tool ?? '')) return;\n"
        "    const caller = `${input.tool}-${input.sessionID ?? 'sess'}-${input.callID ?? Date.now()}`;\n"
        "    const entry = held.get(caller) ?? { token: '', calls: 0 };\n"
        "    const text = `${output.output ?? ''} ${input.args?.prompt ?? ''}`;\n"
        "    if (RATE_LIMIT_RE.test(text)) {\n"
        "      held.delete(caller);\n"
        "      gov('fail', caller);\n"
        "      output.metadata = output.metadata || {};\n"
        "      output.metadata.coacus = 'paused_rate_limit';\n"
        "    } else {\n"
        "      held.delete(caller);\n"
        "      gov('release', caller);\n"
        "    }\n"
        "  },\n"
        "  // Safety net: release any slot still held when a new turn begins,\n"
        "  // so a cancelled/errored spawn (after-hook never ran) cannot leak it.\n"
        "  'chat.message': async () => {\n"
        "    for (const [caller] of held) gov('release', caller);\n"
        "    held.clear();\n"
        "  },\n"
        "});\n"
    )


def _render_governor_gate(harness: dict) -> dict[str, str]:
    """Render the governor-gate plugin files declared by a harness."""
    name = harness["name"]
    rendered: dict[str, str] = {}
    for plugin in harness.get("plugins", []):
        if plugin.get("kind") != "governor-gate":
            continue
        if name == "antigravity":
            rendered[plugin["path"]] = _antigravity_governor_hook()
        elif name == "opencode":
            rendered[plugin["path"]] = _opencode_governor_gate()
    return rendered


def render_plugins(harness: dict, root: Path) -> dict[str, str]:
    """Render every declared plugin for a harness, by kind.

    Renders regardless of whether the harness supports a bootstrap, so a
    hooks-only harness is representable. Unknown kinds render nothing
    (test-pinned: a declared router-hook must stay inert).
    """
    rendered: dict[str, str] = {}
    if any(p.get("kind") == "governor-gate" for p in harness.get("plugins", [])):
        rendered.update(_render_governor_gate(harness))
    if any(p.get("kind") == "guardrail" for p in harness.get("plugins", [])):
        from engine.generators import guardrails as _guardrails

        rendered.update(_guardrails.render(harness, root))
    return rendered


register("governor-gate", _render_governor_gate)
