"""Generate multi-harness agent representations from canonical sources (D1).

One canonical ``agent.source.md`` per agent yields, under a ``dist/`` folder:

- ``AGENT.md``     markdown profile (harness system-prompt consumers)
- ``agent.yaml``   ADK/Antigravity profile (``model: inherit``)
- ``agent.json``   neutral manifest for frameworks and APIs
- ``plugin.json``  plugin shim

plus a ``.agents/entries/<name>.json`` discovery entry (D5).

Generated files contain no timestamps so regeneration is byte-idempotent
(generated-artifacts). ``model`` is never emitted for AGENT.md/agent.json; the yaml
profile uses ``model: inherit``.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path

from engine.frontmatter import Document, parse

SOURCE_NAME = "agent.source.md"
AGENT_FILES = ("AGENT.md", "agent.yaml", "agent.json", "plugin.json")


def discover_sources(root: Path) -> list[Path]:
    """All canonical agent sources: knowledge/agents/<category>/<name>/."""
    agents_dir = root / "knowledge" / "agents"
    if not agents_dir.is_dir():
        return []
    return sorted(agents_dir.glob("*/*/" + SOURCE_NAME))


def _rel(target: Path, start: Path) -> str:
    """POSIX-style relative path from ``start`` to ``target``."""
    return Path(os.path.relpath(target, start)).as_posix()


def _strip_first_h1(body: str) -> str:
    """Body without its leading ``# H1`` line (title lives in the header)."""
    lines = body.splitlines()
    if lines and lines[0].startswith("# "):
        return "\n".join(lines[1:]).strip()
    return body.strip()


_MD_LINK = re.compile(r"\]\(([^)\s]+)(#[^)]*)?\)")


def _rerelativize_links(body: str, root: Path, dist: Path) -> str:
    """Re-point repo-root-relative markdown links so they resolve from ``dist/``.

    Canonical agent bodies link skills as ``knowledge/skills/...`` (root-relative
    per the agent contract); the generated ``dist/AGENT.md`` lives four levels
    below the root, so those links must be rewritten against ``dist/``.
    """
    def repl(match: re.Match) -> str:
        target, anchor = match.group(1), match.group(2) or ""
        if target.startswith(("http://", "https://", "#", "mailto:")):
            return match.group(0)
        candidate = root / target.split("#", 1)[0]
        if not candidate.exists():
            return match.group(0)
        rel = Path(os.path.relpath(candidate, dist)).as_posix()
        return f"]({rel}{anchor})"

    return _MD_LINK.sub(repl, _strip_first_h1(body))


def generate(source_path: Path, root: Path) -> dict[str, str]:
    """Compute generated files for one source.

    Returns a mapping of repo-relative path to file content. Nothing is
    written here; ``write_all`` materializes the outputs.
    """
    doc = parse(source_path.read_text(encoding="utf-8"))
    meta = doc.meta
    name = str(meta.get("name", "")).strip()
    category = str(meta.get("category", "")).strip()
    description = str(meta.get("description", "")).strip()
    raw_skills = meta.get("skills", [])
    if not isinstance(raw_skills, list):
        raise ValueError(
            f"{source_path}: 'skills' must be a block list, got {raw_skills!r}"
        )
    skills = [str(s) for s in raw_skills if str(s).strip()]

    dist = source_path.parent / "dist"
    dist_rel = dist.relative_to(root).as_posix()
    outputs: dict[str, str] = {}

    skill_links = "\n".join(
        f"- [{Path(skill).parent.name}]({_rel(root / skill, dist)})"
        for skill in skills
    )
    outputs[f"{dist_rel}/AGENT.md"] = (
        f"# {doc.title or name}\n\n"
        f"{description}\n\n"
        "## Skills\n\n"
        "<!-- coacus:generated:skills -->\n"
        f"{skill_links}\n"
        "<!-- /coacus:generated:skills -->\n\n"
        f"{_rerelativize_links(doc.body, root, dist)}\n"
    )

    tools = "".join(
        f"  - type: skill_integration\n    path: {_rel(root / skill, dist)}\n"
        for skill in skills
    )
    instruction = "\n".join(
        ("  " + line) if line else ""
        for line in _strip_first_h1(doc.body).splitlines()
    ).rstrip("\n")
    outputs[f"{dist_rel}/agent.yaml"] = (
        f"name: {name}\n"
        "model: inherit\n"
        f"description: >-\n  {description}\n"
        "instruction: >\n"
        f"{instruction}\n"
        "tools:\n"
        f"{tools}"
    )

    outputs[f"{dist_rel}/agent.json"] = json.dumps(
        {
            "name": name,
            "description": description,
            "instruction": doc.body.strip(),
            "skills": skills,
            "category": category,
        },
        indent=2,
    ) + "\n"

    outputs[f"{dist_rel}/plugin.json"] = json.dumps(
        {
            "name": name,
            "version": "0.1.0",
            "description": description,
            "entrypoint": "AGENT.md",
        },
        indent=2,
    ) + "\n"

    fingerprint = hashlib.sha256(source_path.read_bytes()).hexdigest()[:16]
    outputs[f".agents/entries/{name}.json"] = json.dumps(
        {
            "name": name,
            "description": description,
            "category": category,
            "source": _rel(source_path, root),
            "dist": dist_rel,
            "fingerprint": fingerprint,
        },
        indent=2,
    ) + "\n"

    return outputs


def expected_outputs(root: Path) -> dict[str, str]:
    """Union of generated content for every canonical source."""
    outputs: dict[str, str] = {}
    for source in discover_sources(root):
        outputs.update(generate(source, root))
    return outputs


def write_all(root: Path) -> list[str]:
    """Materialize all generated files. Returns repo-relative paths written."""
    written: list[str] = []
    for rel, content in expected_outputs(root).items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        written.append(rel)
    return sorted(written)


def check(root: Path) -> list[str]:
    """Drift check (generated-artifacts): disk vs a fresh regeneration, plus orphans."""
    drift: list[str] = []
    expected = expected_outputs(root)
    for rel, content in expected.items():
        path = root / rel
        if not path.is_file():
            drift.append(f"{rel}: missing (run generate)")
        elif path.read_text(encoding="utf-8") != content:
            drift.append(f"{rel}: out of date (run generate)")

    agents_dir = root / "knowledge" / "agents"
    actual_dist: set[str] = set()
    if agents_dir.is_dir():
        for dist in agents_dir.glob("*/*/dist"):
            for path in dist.rglob("*"):
                if path.is_file():
                    actual_dist.add(path.relative_to(root).as_posix())
    for rel in sorted(actual_dist - set(expected)):
        drift.append(f"{rel}: orphan (source removed — delete or restore it)")

    actual_manifests: set[str] = set()
    manifest_dir = root / ".agents" / "entries"
    if manifest_dir.is_dir():
        for path in manifest_dir.glob("*.json"):
            actual_manifests.add(path.relative_to(root).as_posix())
    for rel in sorted(actual_manifests - set(expected)):
        drift.append(f"{rel}: orphan (source removed — delete or restore it)")

    return sorted(drift)
