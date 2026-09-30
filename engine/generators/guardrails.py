"""Render the canonical guardrail policy layer into each harness's native hook.

This is the 'Rendering effect' layer of PAER. Policies are authored once
(``methodology/lifecycle/policies/*.policy.json``); the runtime evaluator is
``scripts/coacus_guard.py``; this generator emits, per harness, the native hook
that calls the evaluator at the bound event.

One producer per path (outputs): guardrail artifacts are DISJOINT from the
bootstrap ``hooks.json`` — they live in ``coacus-guard.*`` and
``guardrail-hooks.json`` so no two generators write the same file. The installer
merges the fragment into the user hook config.

Capability gating (D3): where a harness cannot block, deny policies are rendered
as advisory and the capability matrix records it; where an event has no native
home, the binding is simply absent. Enforcement claims are never fabricated here.
"""

from __future__ import annotations

import json
from pathlib import Path

SHELL_HARNESSES = ("claude-code", "codex", "cursor", "command-code")
EVALUATOR = "scripts/coacus_guard.py"


def _guard_script(harness: str) -> str:
    """A POSIX wrapper that pipes the trigger payload to the evaluator.

    On any internal failure it emits no opinion and exits 0; the evaluator owns
    the fail-open/deny semantics (D4) so the wrapper never becomes a second,
    divergent decision point.
    """
    return (
        "#!/usr/bin/env bash\n"
        f"# Coacus guardrail hook for {harness} (generated — do not edit).\n"
        "# Calls the PAER evaluator and prints its native effect JSON.\n"
        "set -euo pipefail\n"
        'COACUS_ROOT="__COACUS_ROOT__"\n'
        'PAYLOAD="$(cat)"\n'
        f'printf "%s" "$PAYLOAD" | python3 "$COACUS_ROOT/{EVALUATOR}" '
        f'--harness {harness} --event tool.pre --root "$COACUS_ROOT" 2>/dev/null '
        "|| echo '{}'\n"
    )


def _hook_fragment(harness: str) -> str:
    """The harness hook-config fragment that binds the guard script.

    Shape A harnesses share ``{"hooks": {...}}``; Antigravity keys by hook-set
    name. The fragment is merged by the installer (never written wholesale into a
    user config).
    """
    command = f'"__COACUS_ROOT__/harnesses/{harness}/bootstrap/coacus-guard.sh"'
    if harness == "cursor":
        return json.dumps(
            {"version": 1, "hooks": {"preToolUse": [{"command": command}]}},
            indent=2,
        ) + "\n"
    if harness == "antigravity":
        return json.dumps(
            {"coacus-guard": {"PreToolUse": [{"type": "command", "command": command}]}},
            indent=2,
        ) + "\n"
    return json.dumps(
        {
            "hooks": {
                "PreToolUse": [
                    {"hooks": [{"type": "command", "command": command}]}
                ]
            }
        },
        indent=2,
    ) + "\n"


def _opencode_plugin() -> str:
    """OpenCode has no shell hooks: a JS plugin that shells to the evaluator.

    Blocking is a thrown error (OpenCode's only deny mechanism). On an evaluator
    failure the plugin stays silent, so a broken guard cannot brick the session.
    """
    return (
        "// Coacus guardrail plugin for opencode (generated — do not edit).\n"
        "// Install: copy to <harness config>/plugins/coacus-guardrails.js.\n"
        "// Delegates the decision to scripts/coacus_guard.py (PAER) and throws on\n"
        "// a deny (OpenCode's only blocking mechanism — orchestration-governance).\n"
        "\n"
        "import { execFileSync } from 'node:child_process';\n"
        "\n"
        "const COACUS_ROOT = '__COACUS_ROOT__';\n"
        "const GUARD = COACUS_ROOT + '/scripts/coacus_guard.py';\n"
        "\n"
        "/**\n"
        " * Guardrail plugin: evaluate a tool call and abort it on a deny.\n"
        " *\n"
        " * @returns {Promise<object>} The plugin hook map.\n"
        " */\n"
        "export const CoacusGuardrails = async () => ({\n"
        "  'tool.execute.before': async (input, output) => {\n"
        "    const payload = JSON.stringify({ tool: input.tool, tool_input: output.args });\n"
        "    let effect = '{}';\n"
        "    try {\n"
        "      effect = execFileSync('python3', [GUARD, '--harness', 'opencode', '--event', 'tool.pre',\n"
        "        '--root', COACUS_ROOT], { input: payload, encoding: 'utf8', timeout: 5000,\n"
        "        stdio: ['pipe', 'pipe', 'ignore'] }).trim();\n"
        "    } catch { return; }\n"
        "    // OpenCode has no native effect JSON: only a throw blocks.\n"
        "    if (effect.includes('\"deny\"')) {\n"
        "      throw new Error('Coacus guardrail denied this tool call.');\n"
        "    }\n"
        "  },\n"
        "});\n"
    )


def render(harness: dict, root: Path) -> dict[str, str]:
    """Render guardrail artifacts for a harness declaring a ``guardrail`` plugin."""
    name = harness["name"]
    plugin = next(
        (p for p in harness.get("plugins", []) if p.get("kind") == "guardrail"), None
    )
    if plugin is None:
        return {}
    lifecycle = harness.get("lifecycle", {})
    if not lifecycle.get("supported", False):
        return {}

    base = f"harnesses/{name}/bootstrap"
    rendered: dict[str, str] = {}
    if name == "opencode":
        rendered[f"{base}/coacus-guardrails.js"] = _opencode_plugin()
    else:
        rendered[f"{base}/coacus-guard.sh"] = _guard_script(name)
        rendered[f"{base}/guardrail-hooks.json"] = _hook_fragment(name)
    return rendered
