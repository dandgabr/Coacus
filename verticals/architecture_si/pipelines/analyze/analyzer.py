"""Analyze Markdown documents: outline, metrics, diagrams, security keywords.

Ported from the `agente-arquitetura-si` analyzer (F6c), translated and placed
under the vertical pipeline. Dual output: human report or stable JSON, ready to
be exposed as an MCP tool.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

SECURITY_KEYWORDS: dict[str, list[str]] = {
    "STRIDE": ["spoofing", "tampering", "repudiation", "information disclosure",
               "denial of service", "elevation of privilege"],
    "Standards": ["asvs", "owasp", "lgpd", "gdpr", "hipaa", "iso 27001", "nist", "sabsa"],
    "Protocols & Controls": ["mtls", "tls 1.3", "oauth2", "oidc", "jwt", "waf", "kms",
                             "argon2", "aes-256", "zero trust"],
    "Severity Levels": ["p0", "p1", "p2", "p3", "critical", "high", "blocker"],
}


@dataclass
class Analysis:
    """Structured result of analysing one Markdown document."""

    file_name: str
    file_path: str
    total_lines: int
    word_count: int
    char_count: int
    estimated_reading_minutes: int
    headings: list[dict] = field(default_factory=list)
    code_blocks_count: int = 0
    mermaid_diagrams_count: int = 0
    tables_count: int = 0
    security_keywords_detected: dict[str, list[str]] = field(default_factory=dict)


def _has_term(text_lower: str, term: str) -> bool:
    """Word-boundary match for short/ambiguous terms (p0-p3, high, low)."""
    if len(term) <= 4 and term.isalnum():
        return re.search(rf"(?<![a-z0-9]){re.escape(term)}(?![a-z0-9])", text_lower) is not None
    return term in text_lower


def analyze_markdown(file_path: str) -> Analysis:
    """Analyse a Markdown file and return its metrics, outline and detected terms."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"file not found: {file_path}")
    content = path.read_text(encoding="utf-8", errors="replace")
    lines = content.splitlines()
    word_count = len(content.split())

    headings: list[dict] = []
    for line in lines:
        match = re.match(r"^(#{1,6})\s+(.*)", line)
        if match:
            headings.append({"level": len(match.group(1)), "title": match.group(2).strip()})

    code_blocks = re.findall(r"```([a-zA-Z0-9_-]*)\n(.*?)```", content, re.DOTALL)
    mermaid = [b for b in code_blocks if b[0].lower() in ("mermaid", "c4context", "c4container")]
    tables = re.findall(r"(\|.+?\|\n\|[-:| ]+\|\n(?:\|.+?\|\n?)+)", content)

    content_lower = content.lower()
    detected = {
        category: [term for term in terms if _has_term(content_lower, term)]
        for category, terms in SECURITY_KEYWORDS.items()
    }
    detected = {k: v for k, v in detected.items() if v}

    return Analysis(
        file_name=path.name,
        file_path=path.resolve().as_posix(),
        total_lines=len(lines),
        word_count=word_count,
        char_count=len(content),
        estimated_reading_minutes=max(1, round(word_count / 200)),
        headings=headings,
        code_blocks_count=len(code_blocks),
        mermaid_diagrams_count=len(mermaid),
        tables_count=len(tables),
        security_keywords_detected=detected,
    )


def human_report(analysis: Analysis) -> str:
    """Render an analysis as a human-readable text report."""
    parts = [
        "=" * 50,
        f"Analysis report: {analysis.file_name}",
        "=" * 50,
        f"Lines: {analysis.total_lines} | Words: {analysis.word_count} | "
        f"Est. reading: ~{analysis.estimated_reading_minutes} min",
        f"Headings: {len(analysis.headings)} | Tables: {analysis.tables_count} | "
        f"Mermaid diagrams: {analysis.mermaid_diagrams_count}",
    ]
    if analysis.security_keywords_detected:
        parts.append("\nSecurity & architecture terms detected:")
        for category, terms in analysis.security_keywords_detected.items():
            parts.append(f"  - {category}: {', '.join(terms)}")
    if analysis.headings:
        parts.append("\nOutline (extracted):")
        for heading in analysis.headings[:15]:
            parts.append("  " * (heading["level"] - 1) + f"- {heading['title']}")
        if len(analysis.headings) > 15:
            parts.append(f"  ... and {len(analysis.headings) - 15} more.")
    parts.append("=" * 50)
    return "\n".join(parts)


def analyze_dir(directory: str, as_json: bool) -> str:
    """Analyse every ``*.md`` file in ``directory``, as JSON or human reports."""
    files = sorted(Path(directory).glob("*.md"))
    chunks: list[str] = []
    for path in files:
        analysis = analyze_markdown(str(path))
        chunks.append(
            json.dumps(asdict(analysis), indent=2, ensure_ascii=False)
            if as_json else human_report(analysis)
        )
    return "\n".join(chunks)
