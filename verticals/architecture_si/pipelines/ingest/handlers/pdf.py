"""PDF to structured Markdown, with PyMuPDF → pypdf fallback (knowledge-ingestion).

Preserves the upstream behavior: TOC/bookmark map, per-page anchors, list and
code heuristics, and the ``--toc-only`` / ``--split-chapters`` options. The
dependency is auto-detected so the framework runs with either library.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, Optional

from engine.dispatcher import register_converter

from verticals.architecture_si.pipelines.ingest.handlers import _common as common

try:  # pragma: no cover - environment dependent
    import fitz  # PyMuPDF
    HAVE_FITZ = True
except ImportError:  # pragma: no cover
    HAVE_FITZ = False

HAVE_PYPDF = False
if not HAVE_FITZ:  # pragma: no cover
    try:
        import pypdf
        HAVE_PYPDF = True
    except ImportError:
        pass

_CODE_KEYWORDS = ("def ", "import ", "class ", "const ", "function ",
                  "public class", "SELECT ", "FROM ")
_LIST_PREFIXES = ("•", "-", "*", "1.", "2.", "3.", "4.", "5.")


def clean_text(text: str) -> str:
    """Fix hyphenation across line breaks and normalize whitespace."""
    text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _toc_map(doc: Any) -> Dict[int, str]:
    toc_map: Dict[int, str] = {}
    try:
        toc = doc.get_toc() or []
    except Exception:  # pragma: no cover - malformed PDF metadata
        return toc_map
    for level, title, page in toc:
        if page > 0:
            toc_map[page] = "#" * min(max(level, 1), 6) + " " + title.strip()
    return toc_map


def convert_pdf_with_fitz(
    pdf_path: str,
    output_path: Optional[str] = None,
    split_chapters: bool = False,
    toc_only: bool = False,
) -> str:
    """Convert a PDF to Markdown using PyMuPDF (per-page anchors, TOC map).

    ``toc_only`` emits just the outline; ``split_chapters`` is accepted for
    interface parity with the upstream converter.
    """
    doc = fitz.open(pdf_path)
    base = Path(pdf_path).stem
    if output_path is None:
        output_path = str(Path(pdf_path).with_suffix(".md"))

    toc_list = doc.get_toc()
    toc_map = _toc_map(doc)

    if toc_only:
        lines = [f"# Table of Contents: {base}\n"]
        if toc_list:
            for level, title, page in toc_list:
                lines.append("  " * (max(level, 1) - 1) + f"- **{title.strip()}** (p. {page})")
        else:
            lines.append("_No internal table of contents (TOC/bookmarks) found._")
        return common.write_markdown("\n".join(lines), output_path, pdf_path)

    md_lines = [f"# {base}\n", "> Document converted from PDF to Markdown for architecture and security analysis.\n"]
    if toc_list:
        md_lines.append("## Document Outline\n")
        for level, title, page in toc_list[:60]:
            md_lines.append("  " * (max(level, 1) - 1) + f"- [{title.strip()}](#p{page})")
        md_lines.append("\n---\n")

    for page_idx in range(len(doc)):
        page_num = page_idx + 1
        header = f"\n<a id='p{page_num}'></a>\n<!-- Page {page_num} -->\n"
        if page_num in toc_map:
            header += f"\n{toc_map[page_num]}\n\n"
        md_lines.append(header)
        for block in doc[page_idx].get_text("blocks"):
            if block[6] != 0:
                continue
            text = block[4].strip()
            if not text:
                continue
            if text.startswith(_LIST_PREFIXES):
                md_lines.append(text)
            elif any(kw in text for kw in _CODE_KEYWORDS):
                md_lines.append(f"```\n{text}\n```")
            else:
                md_lines.append(text + "\n")

    return common.write_markdown(clean_text("\n".join(md_lines)), output_path, pdf_path)


def convert_pdf_with_pypdf(pdf_path: str, output_path: Optional[str] = None) -> str:
    """Convert a PDF to Markdown using pypdf (plain per-page text extraction)."""
    reader = pypdf.PdfReader(pdf_path)
    base = Path(pdf_path).stem
    if output_path is None:
        output_path = str(Path(pdf_path).with_suffix(".md"))
    md_lines = [f"# {base}\n", "> Document converted from PDF to Markdown via pypdf.\n\n---\n"]
    for idx, page in enumerate(reader.pages):
        md_lines.append(f"\n<a id='p{idx + 1}'></a>\n<!-- Page {idx + 1} -->\n")
        md_lines.append((page.extract_text() or "") + "\n")
    return common.write_markdown(clean_text("\n".join(md_lines)), output_path, pdf_path)


def convert_pdf_to_markdown(
    pdf_path: str, output_path: Optional[str] = None, **kwargs: Any
) -> str:
    """Convert a PDF to Markdown, selecting PyMuPDF or pypdf by availability."""
    if not Path(pdf_path).exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    if HAVE_FITZ:
        return convert_pdf_with_fitz(pdf_path, output_path, **kwargs)
    if HAVE_PYPDF:
        return convert_pdf_with_pypdf(pdf_path, output_path)
    raise RuntimeError("No PDF library available: pip install PyMuPDF or pip install pypdf")


@register_converter(".pdf")
def handle_pdf(input_path: str, output_path: str | None = None) -> str:
    """Convert a PDF to Markdown and return the written path."""
    return convert_pdf_to_markdown(input_path, output_path)
