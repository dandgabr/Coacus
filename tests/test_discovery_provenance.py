"""Tests for the discovery manifest validator and provenance schema."""

from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from engine import provenance
from engine.validators import discovery


def sample_repo(tmp: Path) -> tuple[Path, Path]:
    """Minimal repo with one agent source; returns (root, source)."""
    root = tmp / "repo"
    source = root / "knowledge/agents/roles/sample-agent/agent.source.md"
    source.parent.mkdir(parents=True)
    source.write_text(
        "---\nname: sample-agent\ncategory: roles\n"
        "description: >-\n  Samples.\nskills:\n  - knowledge/skills/roles/one/SKILL.md\n"
        "---\n\n# Sample Agent\n\nBody.\n",
        encoding="utf-8",
    )
    skill = root / "knowledge/skills/roles/one/SKILL.md"
    skill.parent.mkdir(parents=True)
    skill.write_text("---\nname: one\ndescription: x\n---\n\n# one\nbody\n", encoding="utf-8")
    return root, source


class TestDiscoveryValidator(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root, self.source = sample_repo(Path(self._tmp.name))
        self.dist = self.source.parent / "dist"
        self.dist.mkdir()
        (self.dist / "AGENT.md").write_text("# x\n", encoding="utf-8")
        self.manifest_dir = self.root / ".agents"
        self.manifest_dir.mkdir()

    def _entry(self) -> dict:
        return {
            "name": "sample-agent",
            "description": "Samples.",
            "category": "roles",
            "source": "knowledge/agents/roles/sample-agent/agent.source.md",
            "dist": "knowledge/agents/roles/sample-agent/dist",
            "fingerprint": hashlib.sha256(self.source.read_bytes()).hexdigest()[:16],
        }

    def _write(self, entry: dict) -> None:
        directory = self.root / ".agents" / "entries"
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "sample-agent.json").write_text(
            json.dumps(entry, indent=2) + "\n", encoding="utf-8"
        )

    def test_valid_manifest_passes(self) -> None:
        self._write(self._entry())
        self.assertEqual(discovery.validate(self.root), [])

    def test_missing_key_fails(self) -> None:
        entry = self._entry()
        del entry["fingerprint"]
        self._write(entry)
        errors = discovery.validate(self.root)
        self.assertTrue(any("missing key" in e for e in errors))

    def test_stale_fingerprint_fails(self) -> None:
        entry = self._entry()
        entry["fingerprint"] = "0" * 16
        self._write(entry)
        errors = discovery.validate(self.root)
        self.assertTrue(any("fingerprint mismatch" in e for e in errors))

    def test_missing_source_fails(self) -> None:
        entry = self._entry()
        entry["source"] = "knowledge/agents/roles/ghost/agent.source.md"
        self._write(entry)
        errors = discovery.validate(self.root)
        self.assertTrue(any("source does not exist" in e for e in errors))

    def test_stem_name_mismatch_fails(self) -> None:
        self._write(self._entry())
        (self.manifest_dir / "entries" / "sample-agent.json").rename(
            self.manifest_dir / "entries" / "other.json"
        )
        errors = discovery.validate(self.root)
        self.assertTrue(any("file stem" in e for e in errors))

    def test_no_manifests_is_clean(self) -> None:
        self.assertEqual(discovery.validate(self.root), [])

    def test_absolute_source_is_rejected(self) -> None:
        entry = self._entry()
        entry["source"] = "/etc/hostname"
        self._write(entry)
        errors = discovery.validate(self.root)
        self.assertTrue(any("relative in-repo path" in e for e in errors))

    def test_upward_escaping_source_is_rejected(self) -> None:
        entry = self._entry()
        entry["source"] = "../../outside.md"
        self._write(entry)
        errors = discovery.validate(self.root)
        self.assertTrue(any("relative in-repo path" in e for e in errors))


class TestProvenance(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name) / "repo"
        self.root.mkdir()

    def test_seed_validates_clean(self) -> None:
        provenance.write(self.root)
        self.assertEqual(provenance.validate(self.root), [])
        self.assertEqual(provenance.load(self.root), {"schema": 1, "entries": []})

    def test_entry_missing_key_fails(self) -> None:
        provenance.write(self.root, {"schema": 1, "entries": [{"source_repo": "x"}]})
        errors = provenance.validate(self.root)
        self.assertTrue(any("missing" in e for e in errors))

    def test_entry_missing_target_file_fails(self) -> None:
        entry = {key: "x" for key in provenance.REQUIRED_ENTRY_KEYS}
        entry["target_path"] = "knowledge/skills/roles/ghost/SKILL.md"
        provenance.write(self.root, {"schema": 1, "entries": [entry]})
        errors = provenance.validate(self.root)
        self.assertTrue(any("target does not exist" in e for e in errors))

    def test_absent_manifest_is_clean(self) -> None:
        self.assertEqual(provenance.validate(self.root), [])

    def test_non_object_root_is_reported(self) -> None:
        (self.root / provenance.LOCK_PATH).write_text(
            json.dumps(["not", "a", "dict"]), encoding="utf-8"
        )
        errors = provenance.validate(self.root)
        self.assertTrue(any("root must be a JSON object" in e for e in errors))

    def test_entries_not_a_list_is_reported(self) -> None:
        (self.root / provenance.LOCK_PATH).write_text(
            json.dumps({"schema": 1, "entries": "oops"}), encoding="utf-8"
        )
        errors = provenance.validate(self.root)
        self.assertTrue(any("'entries' must be a list" in e for e in errors))

    def test_non_object_entry_is_reported(self) -> None:
        (self.root / provenance.LOCK_PATH).write_text(
            json.dumps({"schema": 1, "entries": ["not-a-dict"]}), encoding="utf-8"
        )
        errors = provenance.validate(self.root)
        self.assertTrue(any("entry 0 must be a JSON object" in e for e in errors))

    def test_aliases_must_be_a_list(self) -> None:
        entry = {key: "x" for key in provenance.REQUIRED_ENTRY_KEYS}
        entry["target_path"] = ""
        entry["aliases"] = "not-a-list"
        provenance.write(self.root, {"schema": 1, "entries": [entry]})
        errors = provenance.validate(self.root)
        self.assertTrue(any("'aliases' must be a list" in e for e in errors))


class TestProvenanceDrift(unittest.TestCase):
    """The target_sha256 drift key and the refresh path (provenance.md)."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name) / "repo"
        self.root.mkdir()

    def _entry(self, target: str, digest: str, *, in_place: bool = True) -> dict:
        entry = {key: "x" for key in provenance.REQUIRED_ENTRY_KEYS}
        entry["target_path"] = target
        entry["target_sha256"] = digest
        entry["source_sha256"] = digest if in_place else "a" * 64
        return entry

    def _write_target(self, rel: str, text: str) -> str:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return provenance._sha256(path)

    def test_matching_hash_validates_clean(self) -> None:
        rel = "knowledge/skills/roles/one/SKILL.md"
        digest = self._write_target(rel, "body\n")
        provenance.write(self.root, {"schema": 1, "entries": [self._entry(rel, digest)]})
        self.assertEqual(provenance.validate(self.root), [])

    def test_stale_hash_fails(self) -> None:
        rel = "knowledge/skills/roles/one/SKILL.md"
        self._write_target(rel, "body\n")
        provenance.write(self.root, {"schema": 1, "entries": [self._entry(rel, "0" * 64)]})
        errors = provenance.validate(self.root)
        self.assertTrue(any("target_sha256 mismatch" in e for e in errors))

    def test_refresh_advances_in_place_entry(self) -> None:
        rel = "knowledge/skills/roles/one/SKILL.md"
        digest = self._write_target(rel, "body\n")
        provenance.write(self.root, {"schema": 1, "entries": [self._entry(rel, "0" * 64)]})
        refreshed = provenance.refresh_targets(self.root)
        self.assertEqual(refreshed, [rel])
        entry = provenance.load(self.root)["entries"][0]
        self.assertEqual(entry["target_sha256"], digest)
        self.assertEqual(entry["source_sha256"], digest)
        self.assertEqual(provenance.validate(self.root), [])

    def test_refresh_keeps_transformed_source_hash(self) -> None:
        rel = "knowledge/skills/roles/one/SKILL.md"
        digest = self._write_target(rel, "body\n")
        provenance.write(
            self.root, {"schema": 1, "entries": [self._entry(rel, "0" * 64, in_place=False)]}
        )
        provenance.refresh_targets(self.root)
        entry = provenance.load(self.root)["entries"][0]
        self.assertEqual(entry["target_sha256"], digest)
        self.assertEqual(entry["source_sha256"], "a" * 64)

    def test_refresh_is_idempotent(self) -> None:
        rel = "knowledge/skills/roles/one/SKILL.md"
        digest = self._write_target(rel, "body\n")
        provenance.write(self.root, {"schema": 1, "entries": [self._entry(rel, digest)]})
        before = (self.root / provenance.LOCK_PATH).read_text(encoding="utf-8")
        self.assertEqual(provenance.refresh_targets(self.root), [])
        after = (self.root / provenance.LOCK_PATH).read_text(encoding="utf-8")
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
