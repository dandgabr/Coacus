"""Render the SessionStart bootstrap per harness from a single canonical body (D8).

One canonical wrapper (`methodology/bootstrap/session-start.canonical.md`) plus
the entry skill body are rendered into the native artifact(s) each harness
expects, driven by data in `harnesses/<h>/harness.json` (OCP: a new harness is a
new data file; a new shape is an engine change).

Shapes:
- A (hook): a POSIX shell script that emits ONE native JSON field, plus the
  harness hook config. Claude Code and Codex read
  ``hookSpecificOutput.additionalContext``; Cursor reads the top-level
  ``additional_context``. The native key and the hook config come from
  ``harness.json``; the forbidden alias is never emitted (session-start-bootstrap).
- B (in-process): a JS module that injects the bootstrap into the first user
  message, with an anti-reinjection guard.
- C (instructions-file / rule): a markdown context file plus the plugin manifest
  that declares it. Antigravity rules are capped at 12,000 characters.
- native-discovery: nothing rendered (the harness surfaces skills natively).

Rendered artifacts are committed and drift-checked (generated-artifacts); no timestamps.
"""

from __future__ import annotations

import json
from pathlib import Path

from engine.frontmatter import parse

BOOTSTRAP_SOURCE = "methodology/bootstrap/session-start.canonical.md"
ENTRY_SKILL = "methodology/workflows/using-coacus/SKILL.md"
SHAPES = ("A", "B", "C", "native-discovery")


def discover_harnesses(root: Path) -> list[Path]:
    """All harness manifests except the authoring template."""
    harnesses_dir = root / "harnesses"
    if not harnesses_dir.is_dir():
        return []
    return sorted(
        path
        for path in harnesses_dir.glob("*/harness.json")
        if path.parent.name != "_template"
    )


def load_harness(path: Path, root: Path) -> dict:
    """Parse a ``harness.json``; a malformed file raises a readable ValueError."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        rel = path.relative_to(root).as_posix() if path.is_relative_to(root) else path
        raise ValueError(f"{rel}: invalid harness manifest ({exc})") from exc
    if not isinstance(data, dict) or "name" not in data:
        raise ValueError(f"{path.name}: harness manifest must be an object with a 'name'")
    return data


def _entry_body(root: Path) -> str:
    doc = parse((root / ENTRY_SKILL).read_text(encoding="utf-8"))
    return doc.body.strip()


def _wrapper(root: Path) -> str:
    return (root / BOOTSTRAP_SOURCE).read_text(encoding="utf-8")


def _tool_mapping_block(mapping: dict) -> str:
    if not mapping:
        return ""
    lines = ["**Tool mapping for this harness:**"]
    lines += [f"- {action} -> {tool}" for action, tool in mapping.items()]
    return "\n".join(lines)


def _bootstrap_text(root: Path, mapping: dict) -> str:
    wrapper = _wrapper(root)
    return wrapper.replace("{entry_skill_body}", _entry_body(root)).replace(
        "{tool_mapping}", _tool_mapping_block(mapping)
    )


def _json_escape(text: str) -> str:
    return json.dumps(text)[1:-1]


def _native_json(harness: dict, text: str) -> str:
    """Build the single-key native JSON payload declared by ``native_key``.

    Supports a nested key (``hookSpecificOutput.additionalContext``) and a
    flat key (``additional_context``). The emitted object carries exactly one
    native context key plus, for the nested form, the required
    ``hookEventName``. It never contains a key listed in ``forbidden_keys``.
    """
    bootstrap = harness["bootstrap"]
    native_key = bootstrap.get("native_key", "additionalContext")
    forbidden = set(bootstrap.get("forbidden_keys", []))
    if native_key in forbidden:
        raise ValueError(
            f"{harness['name']}: native_key {native_key!r} is also forbidden"
        )
    escaped = _json_escape(text)
    if "." in native_key:
        outer, inner = native_key.split(".", 1)
        if outer in forbidden or inner in forbidden:
            raise ValueError(f"{harness['name']}: forbidden key inside {native_key!r}")
        return (
            "{\n"
            f'  "{outer}": {{\n'
            '    "hookEventName": "SessionStart",\n'
            f'    "{inner}": "{escaped}"\n'
            "  }\n"
            "}"
        )
    return '{\n  "' + native_key + '": "' + escaped + '"\n}'


def _render_hook_script(harness: dict, text: str) -> str:
    native_json = _native_json(harness, text)
    return (
        "#!/usr/bin/env bash\n"
        f"# SessionStart bootstrap for {harness['name']} (generated — do not edit).\n"
        "# Emits exactly ONE native JSON field; the forbidden alias is never\n"
        "# emitted (some harnesses read both fields without dedup — session-start-bootstrap).\n"
        "set -euo pipefail\n"
        "cat <<'COACUS_EOF'\n"
        f"{native_json}\n"
        "COACUS_EOF\n"
    )


def _render_shape_a(harness: dict, text: str) -> dict[str, str]:
    """Shape A emits a shell script plus the harness hook config JSON.

    The hook config location, command template and matcher come from
    ``harness.json`` so Claude Code and Codex share the shape while Cursor uses
    its own ``sessionStart`` config.
    """
    bootstrap = harness["bootstrap"]
    script = _render_hook_script(harness, text)
    hooks = bootstrap.get("hooks_config")
    hooks_json = (
        json.dumps(hooks, indent=2) + "\n"
        if hooks
        else json.dumps(
            {
                "hooks": {
                    "SessionStart": [
                        {
                            "matcher": "startup|clear|compact",
                            "hooks": [
                                {
                                    "type": "command",
                                    "command": bootstrap.get(
                                        "command",
                                        '"${CLAUDE_PLUGIN_ROOT:-.}/bootstrap/session-start.sh"',
                                    ),
                                    "async": False,
                                }
                            ],
                        }
                    ]
                }
            },
            indent=2,
        )
        + "\n"
    )
    rendered: dict[str, str] = {}
    for out in bootstrap.get("outputs", []):
        rendered[out["path"]] = hooks_json if out["format"] == "json" else script
    return rendered


def _render_shape_b(harness: dict, text: str, mapping: dict) -> str:
    """Render the in-process plugin (shape B) with a JSDoc'd exported hook.

    The JS follows the JSDoc convention: the exported plugin factory and its
    callbacks document parameters and return contracts with ``@param``/``@returns``.
    """
    name = harness["name"]
    return (
        "// Coacus bootstrap for harness '" + name + "' (generated — do not edit).\n"
        "// Install: copy to <harness config>/plugins/coacus.js. The installer\n"
        "// substitutes __COACUS_ROOT__ with the repository path; the plugin then\n"
        "// injects the bootstrap into the first user message with an anti-\n"
        "// reinjection guard (session-start-bootstrap). Skills are NOT registered\n"
        "// from the repo root: the harness discovers the installed skills tree\n"
        "// natively, so registering the repo root would bypass a partial install.\n"
        "\n"
        "const COACUS_ROOT = '__COACUS_ROOT__';\n"
        "const BOOTSTRAP = " + json.dumps(text) + ";\n"
        "const GUARD = 'EXTREMELY_IMPORTANT';\n"
        "\n"
        "/**\n"
        " * Inject the Coacus entry guidance into the first user message.\n"
        " *\n"
        " * @param {object} _input - The transform input (unused).\n"
        " * @param {{ messages: Array<{ info: { role: string }, parts: Array<object> }> }} output\n"
        " *   - The message list to mutate in place; the bootstrap is unshifted onto\n"
        " *     the first user message unless the anti-reinjection guard is present.\n"
        " * @returns {Promise<void>} Resolves after the (possibly) mutated list is written.\n"
        " */\n"
        "export const CoacusPlugin = async () => ({\n"
        "  'experimental.chat.messages.transform': async (_input, output) => {\n"
        "    if (!output.messages.length) return;\n"
        "    const firstUser = output.messages.find((m) => m.info.role === 'user');\n"
        "    if (!firstUser || !firstUser.parts.length) return;\n"
        "    if (firstUser.parts.some((p) => p.type === 'text' && p.text.includes(GUARD))) return;\n"
        "    const ref = firstUser.parts[0];\n"
        "    firstUser.parts.unshift({ ...ref, type: 'text', text: BOOTSTRAP });\n"
        "  },\n"
        "});\n"
    )


def _render_shape_c(harness: dict, text: str) -> dict[str, str]:
    """Shape C emits an instructions/rule markdown file plus a plugin manifest.

    Antigravity's ``plugin.json`` schema is strict (``name`` + ``description``
    only, ``additionalProperties: false``), so the manifest carries no
    ``contextFileName``. Activation comes from a workspace/global
    ``.agents/rules/*.md`` (``activation: always_on``) or a plugin-bundled
    ``rules/`` file; rules are capped at 12,000 characters.
    """
    name = harness["name"]
    files = harness["bootstrap"].get("outputs", [])
    manifest = json.dumps(
        {
            "name": f"coacus-{name}",
            "description": "Coacus agentic framework bootstrap.",
        },
        indent=2,
    ) + "\n"
    body = text
    if len(text) > 12000:
        body = text[:11500].rstrip() + "\n\n<!-- truncated: rule length cap -->\n"
    rule = (
        "---\n"
        "activation: always_on\n"
        "description: Coacus agentic framework bootstrap rule.\n"
        "---\n\n"
        f"{body}\n"
    )
    rendered: dict[str, str] = {}
    for out in files:
        rendered[out["path"]] = manifest if out["format"] == "json" else rule
    return rendered


def _render_antigravity_governor_hook() -> str:
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


def _render_governor_gate(harness: dict) -> dict[str, str]:
    """Render harness plugin files that gate subagent spawn via the governor."""
    name = harness["name"]
    rendered: dict[str, str] = {}
    for plugin in harness.get("plugins", []):
        if plugin.get("kind") != "governor-gate":
            continue
        if name == "antigravity":
            rendered[plugin["path"]] = _render_antigravity_governor_hook()
        elif name == "opencode":
            rendered[plugin["path"]] = (
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
    return rendered


def _render_router_hook(harness: dict) -> dict[str, str]:
    """Render the OPT-IN routing hook plugin declared in ``harness.json``.

    The plugin runs the offline router on the incoming user message and appends a
    short list of candidate agents to the prompt, so the orchestrator proposes the
    right specialists without a manual lookup. It is opt-in: it only renders when
    the harness declares a ``router-hook`` plugin, and the caller decides whether
    to install it. The router never spawns anything.
    """
    name = harness["name"]
    rendered: dict[str, str] = {}
    for plugin in harness.get("plugins", []):
        if plugin.get("kind") != "router-hook":
            continue
        if name == "opencode":
            rendered[plugin["path"]] = (
                "// Coacus router hook for opencode (generated — do not edit).\n"
                "// OPT-IN: install by copying to <harness config>/plugins/coacus-router.js.\n"
                "// On each user message it runs the offline router over the prompt and\n"
                "// appends the ranked candidate agents, so the orchestrator proposes\n"
                "// the right specialists without a manual lookup (routing). It never\n"
                "// spawns an agent; concurrency stays the governor's job.\n"
                "\n"
                "import { execFileSync } from 'node:child_process';\n"
                "\n"
                "const COACUS_ROOT = '__COACUS_ROOT__';\n"
                "const ROUTE = COACUS_ROOT + '/scripts/coacus_route.py';\n"
                "const TOP = String(process.env.COACUS_ROUTE_TOP ?? 4);\n"
                "\n"
                "/**\n"
                " * Run the router for one prompt and return its candidate lines.\n"
                " *\n"
                " * @param {string} prompt - The user's message text.\n"
                " * @returns {string[]} Candidate rows (score, name, category, matched).\n"
                " */\n"
                "const route = (prompt) => {\n"
                "  try {\n"
                "    return execFileSync('python3', [ROUTE, '--stdin', '--top', TOP],\n"
                "      { input: prompt, encoding: 'utf8', stdio: ['pipe', 'pipe', 'ignore'],\n"
                "        timeout: 20000 },\n"
                "    ).trim().split('\\n').filter(Boolean);\n"
                "  } catch { return []; }\n"
                "};\n"
                "\n"
                "/**\n"
                " * Router hook plugin: suggest agents for the incoming message.\n"
                " *\n"
                " * @returns {Promise<object>} The plugin hook map.\n"
                " */\n"
                "export const CoacusRouter = async () => ({\n"
                "  'chat.message': async (input, output) => {\n"
                "    const textPart = (output.parts ?? []).find((p) => p.type === 'text');\n"
                "    if (!textPart || !textPart.text?.trim()) return;\n"
                "    const candidates = route(textPart.text);\n"
                "    if (!candidates.length) return;\n"
                "    const suggestion = [\n"
                "      '\\n\\n<coacus-routing>',\n"
                "      'Deterministic agent candidates for this request (routing):',\n"
                "      ...candidates.map((c) => '- ' + c),\n"
                "      'Confirm or adjust; do not spawn more than the free governor slots.',\n"
                "      '</coacus-routing>',\n"
                "    ].join('\\n');\n"
                "    textPart.text += suggestion;\n"
                "  },\n"
                "});\n"
            )
    return rendered


def render(harness: dict, root: Path) -> dict[str, str]:
    """Compute rendered files for one harness (repo-relative path -> content)."""
    bootstrap = harness.get("bootstrap", {})
    if not bootstrap.get("supported"):
        return {}
    shape = bootstrap.get("shape")
    outputs = bootstrap.get("outputs", [])
    mapping = harness.get("tool_mapping", {})
    text = _bootstrap_text(root, mapping)

    rendered: dict[str, str] = {}
    if shape == "A":
        rendered.update(_render_shape_a(harness, text))
    elif shape == "B":
        for out in outputs:
            rendered[out["path"]] = _render_shape_b(harness, text, mapping)
    elif shape == "C":
        rendered.update(_render_shape_c(harness, text))
    elif shape == "native-discovery":
        return {}
    else:
        raise ValueError(f"unknown bootstrap shape: {shape!r}")
    rendered.update(_render_governor_gate(harness))
    rendered.update(_render_router_hook(harness))
    return rendered


def expected_outputs(root: Path) -> dict[str, str]:
    """Union of rendered content for every harness."""
    outputs: dict[str, str] = {}
    for manifest_path in discover_harnesses(root):
        harness = load_harness(manifest_path, root)
        outputs.update(render(harness, root))
    return outputs


def write_all(root: Path) -> list[str]:
    """Materialize all rendered bootstrap files. Returns repo-relative paths."""
    written: list[str] = []
    for rel, content in expected_outputs(root).items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        written.append(rel)
    return sorted(written)


def check(root: Path) -> list[str]:
    """Drift check: expected vs disk, plus orphan detection (generated-artifacts)."""
    drift: list[str] = []
    expected = expected_outputs(root)
    for rel, content in expected.items():
        path = root / rel
        if not path.is_file():
            drift.append(f"{rel}: missing (run generate)")
        elif path.read_text(encoding="utf-8") != content:
            drift.append(f"{rel}: out of date (run generate)")

    for manifest_path in discover_harnesses(root):
        harness = load_harness(manifest_path, root)
        bootstrap_dir = root / "harnesses" / harness["name"] / "bootstrap"
        if not bootstrap_dir.is_dir():
            continue
        for path in bootstrap_dir.rglob("*"):
            if path.is_file():
                rel = path.relative_to(root).as_posix()
                if rel not in expected:
                    drift.append(f"{rel}: orphan (no longer rendered)")
    return sorted(drift)
