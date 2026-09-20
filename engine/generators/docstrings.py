"""Generate a Python API reference from module/function/class docstrings (F7).

Docstrings are the single source of truth (the "disk is the truth" principle):
this generator walks the framework's Python modules, extracts signatures and
docstrings via the stdlib ``ast`` parser, and writes a Markdown reference. The
output is committed and drift-checked (generated-artifacts) like any other generated
artifact, so documentation cannot fall out of sync with the code.
"""

from __future__ import annotations

import ast
from pathlib import Path

DOCS_PATH = "docs/reference/python-api.md"
SCAN_DIRS = ("engine", "scripts", "verticals")


def _iter_modules(root: Path) -> list[Path]:
    modules: list[Path] = []
    for top in SCAN_DIRS:
        base = root / top
        if base.is_dir():
            modules.extend(sorted(base.rglob("*.py")))
    return [m for m in modules if "__pycache__" not in m.parts and m.name != "__init__.py"]


def _signature(node: ast.AST) -> str:
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        prefix = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"
        args = ast.unparse(node.args)
        returns = f" -> {ast.unparse(node.returns)}" if node.returns else ""
        return f"{prefix} {node.name}({args}){returns}"
    if isinstance(node, ast.ClassDef):
        return f"class {node.name}"
    return getattr(node, "name", "?")


def _doc(node: ast.AST) -> str:
    try:
        return (ast.get_docstring(node) or "").strip()
    except TypeError:
        return ""


def _render_module(root: Path, path: Path) -> list[str]:
    rel = path.relative_to(root).as_posix()
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except SyntaxError as exc:  # pragma: no cover - defensive
        return [f"### `{rel}`", "", f"_Could not parse: {exc}_", ""]

    lines = [f"### `{rel}`", "", _doc(tree) or "_No module docstring._", ""]
    public = [
        node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        and not node.name.startswith("_")
    ]
    for node in public:
        lines.append(f"#### `{_signature(node)}`")
        lines.append("")
        lines.append(_doc(node) or "_No docstring._")
        lines.append("")
        if isinstance(node, ast.ClassDef):
            for child in node.body:
                if (
                    isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef))
                    and not child.name.startswith("_")
                ):
                    lines.append(f"- `{_signature(child)}` — {_doc(child).splitlines()[0] if _doc(child) else 'no docstring'}")
            lines.append("")
    return lines


def build(root: Path) -> str:
    """Render the Markdown API reference from the sources' docstrings."""
    lines = [
        "# Python API Reference",
        "",
        "> GENERATED from source docstrings by `scripts/coacus.py generate` — do not edit.",
        "> Source of truth: the docstrings themselves.",
        "",
    ]
    for module in _iter_modules(root):
        lines.extend(_render_module(root, module))
    return "\n".join(lines).rstrip() + "\n"


def write(root: Path) -> Path:
    """Write the generated API reference to disk and return its path."""
    out = root / DOCS_PATH
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build(root), encoding="utf-8")
    return out


def check(root: Path) -> list[str]:
    """Drift check for the generated API reference (generated-artifacts)."""
    target = root / DOCS_PATH
    if not target.is_file():
        return [f"{DOCS_PATH}: missing (run generate)"]
    if target.read_text(encoding="utf-8") != build(root):
        return [f"{DOCS_PATH}: out of date (run generate)"]
    return []
