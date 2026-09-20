"""Open-closed dispatcher for document ingestion (knowledge-ingestion).

Formats register themselves with ``@register_converter``; adding a new format
is a new handler file — the dispatcher never changes (OCP). Handlers live in
``verticals/architecture-si/pipelines/ingest/handlers/`` and declare the
extensions they own.
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable, Optional

# extension -> converter(input_path, output_path) -> output_path
_REGISTRY: dict[str, Callable[[str, Optional[str]], str]] = {}


def register_converter(*extensions: str):
    """Decorator: register a converter for one or more extensions."""

    def decorator(func: Callable[[str, Optional[str]], str]):
        for ext in extensions:
            _REGISTRY[ext.lower()] = func
        return func

    return decorator


def supported_extensions() -> list[str]:
    """Return the sorted list of file extensions with a registered converter."""
    return sorted(_REGISTRY)


def converter_for(path: str | Path) -> Callable[[str, Optional[str]], str] | None:
    """Return the converter registered for ``path``'s extension, or ``None``."""
    return _REGISTRY.get(Path(path).suffix.lower())


def convert(input_path: str, output_path: str | None = None, **options) -> str:
    """Dispatch conversion by extension using the registered handlers.

    Extra ``options`` (e.g. ``toc_only``, ``split_chapters``) are forwarded to
    the handler; handlers that do not accept them ignore extras.
    """
    source = Path(input_path)
    if not source.exists():
        raise FileNotFoundError(f"file not found: {input_path}")
    handler = converter_for(source)
    if handler is None:
        raise ValueError(
            f"unsupported format {source.suffix!r}; supported: {supported_extensions()}"
        )
    if options:
        try:
            return handler(str(source), output_path, **options)
        except TypeError:
            pass  # handler does not take these options; fall back to the 2-arg form
    return handler(str(source), output_path)


def load_handlers() -> None:
    """Import every handler module so their decorators run."""
    handlers_dir = (
        Path(__file__).resolve().parents[2]
        / "verticals"
        / "architecture_si"
        / "pipelines"
        / "ingest"
        / "handlers"
    )
    if not handlers_dir.is_dir():
        return
    import importlib

    package = "verticals.architecture_si.pipelines.ingest.handlers"
    for module in sorted(handlers_dir.glob("*.py")):
        if module.name.startswith("_"):
            continue
        importlib.import_module(f"{package}.{module.stem}")
