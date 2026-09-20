"""JSON / YAML to a fenced Markdown code block."""

from __future__ import annotations

from pathlib import Path

from engine.dispatcher import register_converter

from verticals.architecture_si.pipelines.ingest.handlers import _common as common


@register_converter(".json", ".yaml", ".yml")
def handle_structured(input_path: str, output_path: str | None = None) -> str:
    """Convert a JSON/YAML file to a fenced Markdown block; return the path."""
    ext = Path(input_path).suffix.lower()
    with open(input_path, "r", encoding="utf-8", errors="replace") as handle:
        content = handle.read()
    lang = "json" if ext == ".json" else "yaml"
    md = f"# Configuration / Structure: {Path(input_path).name}\n\n```{lang}\n{content}\n```\n"
    return common.write_markdown(md, output_path, input_path)
