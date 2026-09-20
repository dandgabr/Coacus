"""Enforce the docstring convention (PEP 257) on the framework's public API.

Every public module, top-level function/class and public method under
``engine/``, ``scripts/`` and ``verticals/`` must carry a docstring. This is the
same surface the generated ``docs/reference/python-api.md`` documents, so a
missing docstring is both a style gap and a hole in the reference.

Verbatim third-party assets (the imported Superpowers JS/TS under
``methodology/``) are out of scope: they are byte-identical upstream copies
recorded in ``sources.lock.json`` and must not be edited.
"""

from __future__ import annotations

import ast
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN_DIRS = ("engine", "scripts", "verticals")


def _public_modules() -> list[Path]:
    modules: list[Path] = []
    for top in SCAN_DIRS:
        base = ROOT / top
        if base.is_dir():
            modules.extend(
                p for p in sorted(base.rglob("*.py")) if "__pycache__" not in p.parts
            )
    return modules


class TestDocstringConvention(unittest.TestCase):
    def test_public_modules_have_docstrings(self) -> None:
        missing: list[str] = []
        for path in _public_modules():
            tree = ast.parse(path.read_text(encoding="utf-8"))
            if not ast.get_docstring(tree):
                missing.append(path.relative_to(ROOT).as_posix())
        self.assertEqual(missing, [], f"modules missing a docstring: {missing}")

    def test_public_defs_and_methods_have_docstrings(self) -> None:
        missing: list[str] = []
        for path in _public_modules():
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    if node.name.startswith("_"):
                        continue
                    if not ast.get_docstring(node):
                        missing.append(
                            f"{path.relative_to(ROOT).as_posix()}:{node.lineno} {node.name}"
                        )
                    if isinstance(node, ast.ClassDef):
                        for child in node.body:
                            if isinstance(child, ast.FunctionDef) and not child.name.startswith("_"):
                                if not ast.get_docstring(child):
                                    missing.append(
                                        f"{path.relative_to(ROOT).as_posix()}"
                                        f":{child.lineno} {node.name}.{child.name}"
                                    )
        self.assertEqual(missing, [], f"public defs missing a docstring: {missing}")


if __name__ == "__main__":
    unittest.main()
