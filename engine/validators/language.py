"""Language policy check (english-only).

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

# Per-file exemptions for the FENCED-CODE sweep. Wider than LANGUAGE_EXEMPT
# because a fence can legitimately quote PT: example inputs for the bilingual
# router, quoted upstream PT samples, and the linguistic teaching material.
FENCE_EXEMPT = frozenset({
    "knowledge/skills/domains/linguistics/linguistic-pt-br/SKILL.md",
    "knowledge/skills/domains/linguistics/linguistic-es-latam/SKILL.md",
    "knowledge/skills/engineering/practices/documentation-designer/SKILL.md",
    "knowledge/skills/engineering/practices/documentation-designer/examples/mermaid_diagram_samples.md",
    "knowledge/skills/engineering/practices/documentation-designer/references/mermaid_syntax_complete_guide.md",
    "knowledge/skills/engineering/practices/documentation-designer/references/anti-ai-technical-writing-guide.md",
    "knowledge/skills/security/operations/security-technical-opinion/examples/parecer_tecnico_sample.md",
    "knowledge/skills/security/operations/security-technical-opinion/references/parecer_tecnico_guidelines.md",
    "knowledge/skills/languages/lang-rust/SKILL.md",
    "knowledge/skills/languages/lang-rust/references/rust-book-guide.md",
    "knowledge/skills/engineering/practices/python-performance-parallelism/SKILL.md",
})

# Per-line exemptions inside a fence: a Brazilian place name or a quoted PT
# sample that must stay Portuguese (data, not prose). Matched as substrings.
FENCE_LINE_ALLOW = (
    "Ribeirão Preto",
    "O paciente João Silva",
)

# Markers strong enough to flag a LINE inside a fence without false positives.
FENCE_MARKERS = ("ção", "ções", "ã", "õ", "Atua como", "Especialista em")


def fence_hits(text: str) -> list[tuple[int, str]]:
    """Non-English markers inside fenced code blocks (diagrams, comments, strings).

    ``_prose_only`` deliberately drops fences, so contamination in an ASCII
    diagram, a code comment or a string literal used to pass the gate. This
    sweep closes that gap; ``FENCE_EXEMPT`` lists the files whose fences
    legitimately quote Portuguese.
    """
    hits: list[tuple[int, str]] = []
    in_fence = False
    for lineno, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence and any(marker in line for marker in FENCE_MARKERS):
            if any(allow in line for allow in FENCE_LINE_ALLOW):
                continue
            hits.append((lineno, line.strip()))
    return hits



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
                warnings.append(f"{rel}: non-English prose (english-only)")
    return warnings


def fence_errors(root: Path) -> list[str]:
    """Non-English content inside code fences (english-only).

    Blocking: after the F6 translation the corpus is English-clean, so a fence
    that carries Portuguese means a regression the reviewer must fix. Runs in
    ``source_errors`` (generate pre-flight) and ``validate``.
    """
    errors: list[str] = []
    for pattern in SCAN_GLOBS:
        for path in sorted(root.glob(pattern)):
            rel = path.relative_to(root).as_posix()
            if rel in FENCE_EXEMPT:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            for lineno, line in fence_hits(text):
                errors.append(
                    f"{rel}:{lineno}: non-English content in a code fence "
                    f"(english-only): {line[:80]}"
                )
    return errors
