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
    name = harness["name"]
    return (
        "// Coacus bootstrap for harness '" + name + "' (generated — do not edit).\n"
        "// Install: copy to <harness config>/plugins/coacus.js. The installer\n"
        "// substitutes __COACUS_ROOT__ with the repository path; the plugin then\n"
        "// registers the skill paths (no user-config edit) and injects the\n"
        "// bootstrap into the first user message with an anti-reinjection guard\n"
        "// (session-start-bootstrap / session-start-bootstrap).\n"
        "\n"
        "const COACUS_ROOT = '__COACUS_ROOT__';\n"
        "const SKILL_PATHS = [\n"
        "  COACUS_ROOT + '/methodology/workflows',\n"
        "  COACUS_ROOT + '/knowledge/skills',\n"
        "];\n"
        "const BOOTSTRAP = " + json.dumps(text) + ";\n"
        "const GUARD = 'EXTREMELY_IMPORTANT';\n"
        "\n"
        "export const CoacusPlugin = async () => ({\n"
        "  config: async (config) => {\n"
        "    config.skills = config.skills || {};\n"
        "    config.skills.paths = config.skills.paths || [];\n"
        "    for (const p of SKILL_PATHS) {\n"
        "      if (!config.skills.paths.includes(p)) config.skills.paths.push(p);\n"
        "    }\n"
        "  },\n"
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


def _render_governor_gate(harness: dict) -> dict[str, str]:
    """Render harness plugin files that gate subagent spawn via the governor."""
    name = harness["name"]
    rendered: dict[str, str] = {}
    for plugin in harness.get("plugins", []):
        if plugin.get("kind") != "governor-gate":
            continue
        if name == "opencode":
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
