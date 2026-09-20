"""Shared test helpers: build a minimal Coacus repo under a tmp directory."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SAMPLE_SKILL = (
    "---\n"
    "name: sample-skill\n"
    "description: >-\n"
    "  Samples artifacts when asked to.\n"
    "tags: []\n"
    "---\n"
    "\n"
    "# Sample Skill\n"
    "\n"
    "Sample the thing.\n"
)

SAMPLE_AGENT = (
    "---\n"
    "name: sample-agent\n"
    "category: roles\n"
    "description: >-\n"
    "  Samples things when asked to sample.\n"
    "skills:\n"
    "  - knowledge/skills/roles/sample-skill/SKILL.md\n"
    "tags:\n"
    "  - sample\n"
    "---\n"
    "\n"
    "# Sample Agent\n"
    "\n"
    "Sample instruction body.\n"
)

EXPECTED_SKILL_REL = "knowledge/skills/roles/sample-skill/SKILL.md"
# dist/ lives at knowledge/agents/<cat>/<name>/dist -> 4 levels up = knowledge/
EXPECTED_REL_FROM_DIST = "../../../../skills/roles/sample-skill/SKILL.md"


def make_repo(tmp_path: Path) -> Path:
    """Create a tiny valid repo: one skill + one agent referencing it."""
    root = tmp_path / "repo"
    agent_dir = root / "knowledge" / "agents" / "roles" / "sample-agent"
    skill_dir = root / "knowledge" / "skills" / "roles" / "sample-skill"
    routing_dir = root / "knowledge" / "routing"
    agent_dir.mkdir(parents=True)
    skill_dir.mkdir(parents=True)
    routing_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(SAMPLE_SKILL, encoding="utf-8")
    (agent_dir / "agent.source.md").write_text(SAMPLE_AGENT, encoding="utf-8")
    (routing_dir / "lexicon.json").write_text(
        '{\n  "schema": 1,\n  "agents": {\n    "sample-agent": ["sample", "amostra"]\n  }\n}\n',
        encoding="utf-8",
    )
    return root
