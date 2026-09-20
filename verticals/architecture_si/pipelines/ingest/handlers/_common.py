"""Shared formatting helpers for ingest handlers."""

from __future__ import annotations

from pathlib import Path
from typing import List


def format_markdown_table(rows: List[List[str]]) -> str:
    """Format a 2D list of strings as a GitHub-flavored Markdown table."""
    if not rows:
        return ""
    num_cols = max(len(r) for r in rows)
    norm_rows = [r + [""] * (num_cols - len(r)) for r in rows]
    header = norm_rows[0]
    separator = ["---"] * num_cols
    md_table = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(separator) + " |",
    ]
    for row in norm_rows[1:]:
        md_table.append("| " + " | ".join(row) + " |")
    return "\n".join(md_table)


def write_markdown(content: str, output_path: str | None, source: str) -> str:
    """Write ``content`` to ``output_path``.

    Default output keeps the original extension to avoid stem collisions in a
    mixed directory (e.g. ``data.csv`` -> ``data.csv.md``), so ``a.txt`` and
    ``a.csv`` never overwrite each other.
    """
    if output_path is None:
        source_path = Path(source)
        output_path = str(source_path.with_suffix(source_path.suffix + ".md"))
    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write(content.strip() + "\n")
    return output_path
