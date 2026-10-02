"""Render the SessionStart bootstrap per harness from a single canonical body (D8).

One canonical wrapper (`methodology/bootstrap/session-start.canonical.md`) plus
the entry skill body are rendered into the native artifact(s) each harness
expects, driven by data in `harnesses/<h>/harness.json` (OCP: a new harness is a
new data file; a new shape is an engine change).

Shapes:
- A (hook): a JSON payload emitted by the Python session-start runner, plus the
  harness hook config. Claude Code and Codex read
  ``hookSpecificOutput.additionalContext``; Cursor reads the top-level
  ``additional_context``. The native key and the hook config come from
  ``harness.json``; the forbidden alias is never emitted (session-start-bootstrap).
- B (in-process): a JS module that injects the bootstrap into the first user
  message, with an anti-reinjection guard.
- C (instructions-file / rule): a markdown context file plus the plugin manifest
  that declares it. Antigravity rules are capped at 12,000 characters.
- native-discovery: nothing rendered (the harness surfaces skills natively).

Plugin artifacts (the governor gate, guardrails) are rendered by
``engine/generators/plugins.py`` and are reachable even when a harness does not
support a bootstrap, so a hooks-only harness is representable (D8).

Rendered artifacts are committed and drift-checked (generated-artifacts); no timestamps.
"""

from __future__ import annotations

import json
from pathlib import Path

from engine.frontmatter import parse
from engine.generators import plugins

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


def _native_json(harness: dict, text: str, event_name: str = "SessionStart") -> str:
    """Build the single-key native JSON payload declared by ``native_key``.

    Delegates to ``plugins.native_context_json`` so the payload shape has a
    single source; the emitted object carries exactly one native context key
    plus, for the nested form, the required ``hookEventName``. It never
    contains a key listed in ``forbidden_keys``.
    """
    bootstrap = harness["bootstrap"]
    native_key = bootstrap.get("native_key", "additionalContext")
    forbidden = set(bootstrap.get("forbidden_keys", []))
    if native_key in forbidden:
        raise ValueError(
            f"{harness['name']}: native_key {native_key!r} is also forbidden"
        )
    if "." in native_key:
        outer, inner = native_key.split(".", 1)
        if outer in forbidden or inner in forbidden:
            raise ValueError(f"{harness['name']}: forbidden key inside {native_key!r}")
    return plugins.native_context_json(native_key, event_name, text)


def _render_shape_a(harness: dict, text: str) -> dict[str, str]:
    """Shape A emits a native payload plus the harness hook config JSON.

    The hook config location, command template and matcher come from
    ``harness.json`` so Claude Code and Codex share the shape while Cursor uses
    its own ``sessionStart`` config.
    """
    bootstrap = harness["bootstrap"]
    payload = _native_json(harness, text) + "\n"
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
                                        '__COACUS_PYTHON__ "__COACUS_ROOT__/scripts/coacus_session_start.py" "__COACUS_PLUGIN_ROOT__/bootstrap/session-start.json"',
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
        rendered[out["path"]] = hooks_json if out["path"].endswith("/hooks.json") else payload
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
        'const COACUS_ROOT = "__COACUS_ROOT__";\n'
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


def render(harness: dict, root: Path) -> dict[str, str]:
    """Compute rendered files for one harness (repo-relative path -> content).

    Bootstrap artifacts are rendered only when the harness declares bootstrap
    support; plugin artifacts (governor gate, guardrails) are ALWAYS rendered,
    so a hooks-only harness is representable (D8).
    """
    bootstrap = harness.get("bootstrap", {})
    outputs = bootstrap.get("outputs", [])
    mapping = harness.get("tool_mapping", {})

    rendered: dict[str, str] = {}
    if bootstrap.get("supported"):
        shape = bootstrap.get("shape")
        text = _bootstrap_text(root, mapping)
        if shape == "A":
            rendered.update(_render_shape_a(harness, text))
        elif shape == "B":
            for out in outputs:
                rendered[out["path"]] = _render_shape_b(harness, text, mapping)
        elif shape == "C":
            rendered.update(_render_shape_c(harness, text))
        elif shape == "native-discovery":
            pass
        else:
            raise ValueError(f"unknown bootstrap shape: {shape!r}")

    rendered.update(plugins.render_plugins(harness, root))
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
