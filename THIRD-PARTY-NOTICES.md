# Third-Party Notices

Coacus is distributed under [AGPL-3.0](LICENSE). It also contains material
imported from other repositories. Those components remain under their original
licenses, reproduced below as their terms require.

Provenance for every imported file — source repository, commit, path and content
hash — is recorded in [`sources.lock.json`](sources.lock.json)
([provenance standard](docs/standards/provenance.md)).

## Superpowers — MIT

The process workflows at `methodology/workflows/brainstorming`,
`methodology/workflows/diagnosing-agent-sessions`,
`methodology/workflows/dispatching-parallel-agents`,
`methodology/workflows/executing-plans`,
`methodology/workflows/finishing-a-development-branch`,
`methodology/workflows/receiving-code-review`,
`methodology/workflows/requesting-code-review`,
`methodology/workflows/subagent-driven-development`,
`methodology/workflows/test-driven-development`,
`methodology/workflows/using-git-worktrees`,
`methodology/workflows/verification-before-completion`,
`methodology/workflows/writing-plans`, and `methodology/workflows/writing-skills`
are derived from the Superpowers workflow collection by Jesse Vincent
(<https://github.com/obra/superpowers>), imported at commit
`5bf4e78011075bcfc0dc295f0724994cd123ee71`. They are redistributed under the MIT
License, reproduced in full below.

The workflows are adapted for Coacus and use flat skill names; their plan and
spec output is redirected to `docs/temp/`. The systematic-debugging supporting
files were moved to `methodology/workflows/diagnosing-bugs/`, retaining their
Superpowers derivation. The MIT terms are unchanged.

```text
MIT License

Copyright (c) 2025 Jesse Vincent

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Skill-authoring references — MIT

The authoring discipline in
`methodology/workflows/writing-skills/references/writing-for-agents.md`
and `methodology/workflows/writing-skills/references/invocation-model.md` is adapted — paraphrased, not copied —
from the `mattpocock/skills` collection by Matt Pocock
(<https://github.com/mattpocock/skills>), MIT-licensed. The `skill-auditor`
agent's review vocabulary (severity tiers, rating, report shape) is inspired by the
Claude Code `plugin-dev` toolkit's `skill-reviewer` practice (declared MIT in that
plugin's README, <https://github.com/anthropics/claude-code>); it is likewise
paraphrased. The MIT terms govern both:

```text
MIT License

Copyright (c) 2026 Matt Pocock

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Process workflows — MIT

The process workflows `grilling`, `grill-me`, `grill-with-docs`, `handoff`,
`domain-modeling`, `diagnosing-bugs`, `to-spec`, `to-tickets`, `implement-spec`,
`two-axis-code-review`, `retro`, `phase-boundaries` and the `writing-for-agents`
skill are adapted — paraphrased, not copied — from the `mattpocock/skills`
collection by Matt Pocock (<https://github.com/mattpocock/skills>), MIT-licensed.
The MIT text reproduced under "Skill-authoring references — MIT" governs them.

## ARTEX patterns — upstream AGPL-3.0 (ideas only)

Some Coacus standards, references, eval scenarios and tests adapt design patterns
observed in the `ARTEX` repository at commit
`6337341602be6aa5860b1e83138f03bdd0b78f71`
(`https://github.com/BaaRai/ARTEX/tree/6337341602be6aa5860b1e83138f03bdd0b78f71`),
whose `LICENSE` at that commit is the GNU Affero General Public License v3.0. They
are rewritten in Coacus's own words; no code or prose is reproduced,
and each is checked for reused text before it merges. The URL is for attribution
only and must not be fetched by agents. The repository reports that it descends from
project `Autumn-27/ARTEX` (not fetched); the lineage and the original license are
reported, not verified, as of 2026-11-17. ADR 0009 records which ideas were taken and under which Coacus
names. Files that carry such an adaptation must cite this section.

## Skills corpus — GPL-3.0

The skills under `knowledge/skills/**` and the agents under `knowledge/agents/**`
are imported from the `skills` source repository
(<https://github.com/dandgabr/skills>), which is licensed under the GNU General
Public License v3.0. The license text is available in that repository and at
<https://www.gnu.org/licenses/gpl-3.0.txt>.

## Applying this notice

Any redistribution of Coacus, in whole or in part, must retain this file
alongside the imported components. The installer writes a copy to the skills
root of each harness it targets, so an installed corpus carries the same
notices as the repository.

## Brazilian privacy workflow research

The Brazilian privacy workflows and templates are Coacus-authored syntheses of
the cited Brazilian official sources and existing Coacus guidance. The
workflow and artifact selection were informed by
[`goul4rt/lgpd-skills`](https://github.com/goul4rt/lgpd-skills/tree/65e625daf56f84a2c8d9b8b063d1d70481abba3d),
reviewed at commit `65e625daf56f84a2c8d9b8b063d1d70481abba3d`.
The [original project is MIT licensed](https://github.com/goul4rt/lgpd-skills/blob/65e625daf56f84a2c8d9b8b063d1d70481abba3d/LICENSE).
