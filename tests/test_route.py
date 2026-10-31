import json
import tempfile
import unittest
from pathlib import Path

from engine import router
from engine.generators.routing import ROUTING_PATH, build


ROOT = Path(__file__).resolve().parents[1]


class RoutingMigrationTests(unittest.TestCase):
    def test_harness_triggers_route_and_removed_agents_have_no_lexicon_entries(self):
        agents = json.loads((ROOT / "knowledge/routing/lexicon.json").read_text())["agents"]
        self.assertNotIn("general", agents)
        self.assertNotIn("self", agents)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            index = root / ROUTING_PATH
            index.parent.mkdir(parents=True, exist_ok=True)
            index.write_text(json.dumps(build(ROOT)))
            for prompt in ("configure opencode", "claude desktop", "cursor configuration", "codex cli"):
                with self.subTest(prompt=prompt):
                    self.assertEqual(router.rank(root, prompt)[0].name, "harness-specialist")
                    self.assertEqual(router.rank(root, prompt), router.rank(root, prompt))


if __name__ == "__main__":
    unittest.main()
