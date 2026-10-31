"""Keep reviewed Python conversions across upstream workflow imports."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import coacus_import as importer


class TestPythonImports(unittest.TestCase):
    def test_reimport_preserves_conversion_and_rejects_changed_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "coacus"
            upstream = Path(tmp) / "upstream"
            source = upstream / "workflow"
            target = root / "methodology/workflows/workflow"
            source.mkdir(parents=True)
            target.mkdir(parents=True)
            (source / "SKILL.md").write_text("---\nname: workflow\n---\nEnglish text.\n")
            (source / "helper").write_text("#!/bin/bash\necho legacy\n")
            (target / "helper.py").write_text("print('portable')\n")
            lock = {"schema": 1, "entries": [{
                "source_repo": "superpowers", "source_path": "workflow/helper",
                "source_sha256": importer._sha256(source / "helper"),
                "target_path": "methodology/workflows/workflow/helper.py",
                "transform": ["imported", "converted:python"],
            }]}
            (root / "sources.lock.json").write_text(json.dumps(lock))
            actions = [{"action": "import-workflow", "source": source, "target": target}]
            with patch.object(importer, "ROOT", root), patch.object(importer, "_source_dir", return_value=upstream):
                preserved = importer._preserved_python({} , actions)
                self.assertEqual(preserved[target / "helper.py"]["content"], b"print('portable')\n")
                (source / "helper").write_text("#!/bin/bash\necho changed\n")
                with self.assertRaisesRegex(ValueError, "conversion.*review"):
                    importer._preserved_python({}, actions)

    def test_helper_command_adaptation_is_idempotent(self):
        text = "Run `scripts/task-start PLAN 1` and `../subagent-driven-development/scripts/task-brief PLAN 1`."
        result = importer._adapt_workflow_text(text)
        self.assertIn("python3 scripts/task-start.py PLAN 1", result)
        self.assertIn("python3 ../subagent-driven-development/scripts/task-brief.py PLAN 1", result)
        self.assertEqual(importer._adapt_workflow_text(result), result)
