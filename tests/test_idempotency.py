"""Idempotency golden tests (D3/ADR-0014): generate twice, zero diff."""

from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path

from engine.generators import agent_manifests, catalog

from tests.support import make_repo


def snapshot(root: Path) -> dict[str, str]:
    """Content hash of every generated file in the repo."""
    hashes: dict[str, str] = {}
    for rel in agent_manifests.expected_outputs(root):
        path = root / rel
        if path.is_file():
            hashes[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
    catalog_path = root / catalog.CATALOG_PATH
    if catalog_path.is_file():
        hashes[catalog.CATALOG_PATH] = hashlib.sha256(
            catalog_path.read_bytes()
        ).hexdigest()
    return hashes


class TestIdempotency(unittest.TestCase):
    def test_generate_twice_produces_identical_tree(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            agent_manifests.write_all(root)
            catalog.write(root)
            first = snapshot(root)
            agent_manifests.write_all(root)
            catalog.write(root)
            second = snapshot(root)
            self.assertEqual(first, second)
            self.assertTrue(first)  # sanity: something was generated

    def test_generated_files_contain_no_timestamps(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            agent_manifests.write_all(root)
            catalog.write(root)
            for rel, digest in snapshot(root).items():  # noqa: B007
                path = root / rel
                text = path.read_text(encoding="utf-8")
                self.assertNotIn("generated_at", text, rel)
                self.assertNotIn("timestamp", text.lower(), rel)
                self.assertTrue(digest)  # non-empty content hashed


if __name__ == "__main__":
    unittest.main()
