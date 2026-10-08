"""Generate the Agent Skills discovery index.

Writes ``.well-known/agent-skills/index.json``: a versioned index of every
published skill, each with a ``type`` and a content ``digest`` a client can verify
before use. A skill whose directory holds only ``SKILL.md`` is ``skill-md``; a
skill with any extra file is ``archive`` (a deterministic tar.gz built in memory,
never written to the tree — the index is committed and drift-checked, the
artifacts are release-only).

Determinism is the contract (generated-artifacts): the archive uses fixed
metadata and no timestamp, so two builds are byte-identical and ``check`` can
prove it. A skill marked ``internal: true`` in frontmatter is excluded.
"""

from __future__ import annotations

import gzip
import hashlib
import io
import json
import tarfile
from pathlib import Path

from engine.frontmatter import FrontmatterError, parse

INDEX_PATH = ".well-known/agent-skills/index.json"
SCHEMA = "https://schemas.agentskills.io/discovery/0.2.0/schema.json"


def _skill_sources(root: Path) -> list[Path]:
    found: list[Path] = []
    for top in ("knowledge/skills", "methodology/workflows"):
        base = root / top
        if base.is_dir():
            found += sorted(base.rglob("SKILL.md"))
    return found


def is_internal(meta: dict) -> bool:
    """True when frontmatter declares ``metadata.internal: true``."""
    metadata = meta.get("metadata")
    return isinstance(metadata, dict) and str(metadata.get("internal", "")).lower() == "true"


def _artifact_type(skill_dir: Path) -> str:
    extras = [
        p
        for p in skill_dir.rglob("*")
        if p.is_file() and p.name != "SKILL.md"
    ]
    return "archive" if extras else "skill-md"


def _digest_skill_md(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _digest_archive(skill_dir: Path) -> str:
    """SHA-256 of a deterministic tar.gz of the skill directory."""
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w") as tar:
        for path in sorted(skill_dir.rglob("*")):
            if not path.is_file():
                continue
            info = tar.gettarinfo(str(path), arcname=path.relative_to(skill_dir).as_posix())
            info.mtime = 0
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            info.mode = 0o644
            with path.open("rb") as handle:
                tar.addfile(info, handle)
    compressed = gzip.compress(buffer.getvalue(), mtime=0)
    return "sha256:" + hashlib.sha256(compressed).hexdigest()


def build(root: Path) -> dict:
    """Build the discovery index structure from disk."""
    skills: list[dict] = []
    seen: set[str] = set()
    for source in _skill_sources(root):
        try:
            doc = parse(source.read_text(encoding="utf-8"))
        except FrontmatterError:
            continue
        if is_internal(doc.meta):
            continue
        name = str(doc.meta.get("name", source.parent.name))
        if name in seen:
            raise ValueError(f"duplicate skill name in discovery index: {name}")
        seen.add(name)
        artifact_type = _artifact_type(source.parent)
        skills.append(
            {
                "name": name,
                "description": str(doc.meta.get("description", "")).strip(),
                "type": artifact_type,
                "url": source.relative_to(root).as_posix(),
                "digest": (
                    _digest_skill_md(source)
                    if artifact_type == "skill-md"
                    else _digest_archive(source.parent)
                ),
            }
        )
    skills.sort(key=lambda item: item["name"])
    return {"$schema": SCHEMA, "skills": skills}


def _content(root: Path) -> str:
    return json.dumps(build(root), indent=2) + "\n"


def write(root: Path) -> list[Path]:
    """Write the discovery index; return the written path."""
    target = root / INDEX_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(_content(root), encoding="utf-8")
    return [target]


def check(root: Path) -> list[str]:
    """Drift check for the discovery index (generated-artifacts)."""
    target = root / INDEX_PATH
    if not target.is_file():
        return [f"{INDEX_PATH}: missing (run generate)"]
    if target.read_text(encoding="utf-8") != _content(root):
        return [f"{INDEX_PATH}: out of date (run generate)"]
    return []
