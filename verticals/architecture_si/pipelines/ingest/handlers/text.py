"""Text-like formats: TXT, RTF, LOG, and the raw fallback."""

from __future__ import annotations

from pathlib import Path

from engine.dispatcher import register_converter

from verticals.architecture_si.pipelines.ingest.handlers import _common as common


def convert_txt_to_md(txt_path: str) -> str:
    """Read a text-like file and return it as Markdown with an H1 title."""
    with open(txt_path, "r", encoding="utf-8", errors="replace") as handle:
        content = handle.read()
    return f"# {Path(txt_path).stem}\n\n{content}\n"


@register_converter(".txt", ".rtf", ".log")
def handle_text(input_path: str, output_path: str | None = None) -> str:
    """Convert a text-like file to Markdown and return the written path."""
    return common.write_markdown(convert_txt_to_md(input_path), output_path, input_path)
