"""Language policy check (ADR-0001).

Validates that imported CONTENT is English across skills, workflows, agents and
their reference/example assets. Prose only: fenced code blocks, inline code and
markdown link targets are excluded, because samples, identifiers and anchor
slugs are not prose.

Returns WARNINGS (non-blocking during import) — it becomes a hard gate once the
corpus is translated.
"""

from __future__ import annotations

import re
from pathlib import Path

from engine.frontmatter import FrontmatterError, parse
from engine.validators.skills import LANGUAGE_EXEMPT, PT_MARKERS, _prose_only

SCAN_GLOBS = (
    "knowledge/skills/**/*.md",
    "knowledge/agents/**/*.md",
    "methodology/workflows/**/*.md",
)

# Assets that are intentionally non-English (quoted examples, book titles,
# proper nouns). Same spirit as skills.LANGUAGE_EXEMPT, per file.
ASSET_EXEMPT = frozenset({
    "knowledge/skills/engineering/practices/documentation-designer/references/anti-ai-technical-writing-guide.md",
    "knowledge/skills/security/operations/security-technical-opinion/examples/parecer_tecnico_sample.md",
    "knowledge/skills/languages/lang-rust/references/rust-book-guide.md",
})


def _has_non_english(text: str) -> bool:
    return any(marker in _prose_only(text) for marker in PT_MARKERS)


def _strip_math_and_anchors(text: str) -> str:
    """Remove TeX math and bilingual anchor glosses from the prose sample.

    - ``$...$`` / ``$$...$$`` math can carry PT variable labels (notation, not prose).
    - ``Title (Gloss)`` headings keep a PT parenthetical to preserve anchor slugs.
    """
    text = re.sub(r"\$\$.*?\$\$", "", text, flags=re.DOTALL)
    text = re.sub(r"\$[^$]*\$", "", text)
    text = re.sub(r"\(([^()]*[ãõçáéíóúâêô][^()]*)\)", "()", text)
    return text


def validate(root: Path) -> list[str]:
    """Return a list of warning strings (empty = English-clean)."""
    warnings: list[str] = []
    for pattern in SCAN_GLOBS:
        for path in sorted(root.glob(pattern)):
            rel = path.relative_to(root).as_posix()
            if rel in LANGUAGE_EXEMPT or rel in ASSET_EXEMPT:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            if path.name in ("SKILL.md", "agent.source.md"):
                try:
                    doc = parse(text)
                except FrontmatterError:
                    continue
                sample = f"{doc.meta.get('description', '')} {_prose_only(doc.body)}"
            else:
                sample = _prose_only(text)
            if any(marker in _strip_math_and_anchors(sample) for marker in PT_MARKERS):
                warnings.append(f"{rel}: non-English prose (ADR-0001)")
    return warnings
