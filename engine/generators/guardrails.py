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

EVALUATOR = "scripts/coacus_guard.py"


def _hook_fragment(harness: str) -> str:
    """The harness hook-config fragment that binds the guard script.

    Shape A harnesses share ``{"hooks": {...}}``; Antigravity keys by hook-set
    name. The fragment is merged by the installer (never written wholesale into a
    user config).
    """
    command = (
        f'__COACUS_PYTHON__ "__COACUS_ROOT__/{EVALUATOR}" '
        f'--harness {harness} --event tool.pre --root "__COACUS_ROOT__"'
    )
    if harness == "cursor":
        return json.dumps(
            {"version": 1, "hooks": {"preToolUse": [{"command": command}]}},
            indent=2,
        ) + "\n"
    if harness == "antigravity":
        # Antigravity keys PreToolUse by matcher group (a flat handler is the
        # shape of PreInvocation/Stop, not a tool event); ``"*"`` matches every
        # tool, so the guard still sees them all.
        return json.dumps(
            {
                "coacus-guard": {
                    "PreToolUse": [
                        {
                            "matcher": "*",
                            "hooks": [{"type": "command", "command": command}],
                        }
                    ]
                }
            },
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
    """OpenCode requires an in-process JS plugin that executes the Python evaluator.

    Blocking is a thrown error (OpenCode's only deny mechanism). On an evaluator
    failure the plugin stays silent, so a broken guard cannot brick the session.
    Asking works only through the V2 permission ``evaluate`` hook, which the plugin
    registers when the API exists and which may only tighten a decision (deny over
    ask over allow), never loosen it. Without that hook an ``ask`` is degraded by
    the guard, so a V1 install never turns an ask into an allow.
    """
    return (
        "// Coacus guardrail plugin for opencode (generated — do not edit).\n"
        "// Install: copy to <harness config>/plugins/coacus-guardrails.js.\n"
        "// Delegates the decision to scripts/coacus_guard.py (PAER). A deny throws\n"
        "// (OpenCode's only blocking mechanism); an ask is raised only through the\n"
        "// V2 permission evaluate hook and never loosens a decision it is handed.\n"
        "\n"
        "import { execFileSync } from 'node:child_process';\n"
        "\n"
        'const COACUS_ROOT = "__COACUS_ROOT__";\n'
        'const PYTHON = "__COACUS_PYTHON__";\n'
        "const GUARD = COACUS_ROOT + '/scripts/coacus_guard.py';\n"
        "const RANK = { allow: 0, ask: 1, deny: 2 };\n"
        "\n"
        "let evaluateRegistered = false;\n"
        "\n"
        "/** Run the guard once; return its parsed effect, or null on any failure. */\n"
        "function callGuard(channel, payload) {\n"
        "  try {\n"
        "    const out = execFileSync(PYTHON, ['-I', GUARD, '--harness', 'opencode', '--event', 'tool.pre',\n"
        "      '--channel', channel, '--root', COACUS_ROOT], { input: JSON.stringify(payload),\n"
        "      encoding: 'utf8', timeout: 5000, stdio: ['pipe', 'pipe', 'ignore'] }).trim();\n"
        "    const parsed = JSON.parse(out || '{}');\n"
        "    return parsed && typeof parsed === 'object' ? parsed : null;\n"
        "  } catch { return null; }\n"
        "}\n"
        "\n"
        "/**\n"
        " * Guardrail plugin: evaluate a tool call and abort it on a deny.\n"
        " *\n"
        " * @returns {Promise<object>} The plugin hook map.\n"
        " */\n"
        "export const CoacusGuardrails = async () => ({\n"
        "  'tool.execute.before': async (input, output) => {\n"
        "    const channel = evaluateRegistered ? 'before' : 'default';\n"
        "    const effect = callGuard(channel, { tool: input.tool, tool_input: output.args });\n"
        "    if (effect && effect.decision === 'deny') {\n"
        "      throw new Error('Coacus guardrail denied this tool call.');\n"
        "    }\n"
        "  },\n"
        "});\n"
        "\n"
        "/** Return the stricter of two effects; unknown values count as the current one. */\n"
        "function stricter(current, proposed) {\n"
        "  const a = RANK[current] ?? 0;\n"
        "  const b = RANK[proposed] ?? 0;\n"
        "  return b > a ? proposed : current;\n"
        "}\n"
        "\n"
        "// ponytail: dual v1/v2 export; upgrade to pure v2 package directory when v1 dropped\n"
        "export default {\n"
        "  id: 'coacus-guardrails',\n"
        "  server: CoacusGuardrails,\n"
        "  async setup(ctx) {\n"
        "    const v1 = await CoacusGuardrails();\n"
        "    await ctx.tool.hook('execute.before', (e) => v1['tool.execute.before'](e, { args: e.input ?? {} }));\n"
        "    try {\n"
        "      if (ctx.permission && typeof ctx.permission.hook === 'function') {\n"
        "        await ctx.permission.hook('evaluate', async (e) => {\n"
        "          try {\n"
        "            const effect = callGuard('evaluate', { action: e.action, resources: e.resources });\n"
        "            const proposed = effect && effect.decision;\n"
        "            if (proposed) e.effect = stricter(e.effect, proposed);\n"
        "          } catch { /* leave the effect as it came */ }\n"
        "          return e;\n"
        "        });\n"
        "        evaluateRegistered = true;\n"
        "      }\n"
        "    } catch { /* no permission API: asks degrade in the guard */ }\n"
        "  },\n"
        "};\n"
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
        rendered[f"{base}/guardrail-hooks.json"] = _hook_fragment(name)
    return rendered
