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
        'const COACUS_ROOT = "__COACUS_ROOT__";\n'
        'const PYTHON = "__COACUS_PYTHON__";\n'
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
        "      PYTHON,\n"
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
        if name == "opencode":
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
