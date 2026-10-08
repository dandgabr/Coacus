# GNOME quota delivery: consolidated practices

Date: 2026-10-08. Scope: the account, UI, security and release work after the
earlier GNOME development guidance landed. This is a historical curation record,
not an automatic improvement-loop promotion or a transcript archive.

## Sources and selection

The trusted user feedback distinguished adding from connecting, required theme
icons to describe defaults, reported raster/material/shadow problems, requested
separate configuration restoration and account deletion, and authorized a release.
The delivered [source revision](https://github.com/dandgabr/gnome-ai-quota/tree/223edf5fa9b6df886144e754ffd4955bed08a048)
and [release](https://github.com/dandgabr/gnome-ai-quota/releases/tag/v0.1) identify
the retained evidence. The reference documents cite immutable files and explain
the limits of synthetic verification.

The previous skill already covered pure-core separation, native load gates,
notifications, session lifecycle and translations. Those topics were retained
rather than copied into new generic skills. Provider-specific endpoints and exact
cost fields were left in the source project's provider guide: they require fresh
research and should not become permanent framework rules. Temporary paths, real
credentials, account identity and copied transcripts were not imported.

## Reusable practices and destinations

| Learning | Canonical destination |
| --- | --- |
| Saved configuration is not authentication; recognize intermediate states and route to the existing editor | [Account reference](../../knowledge/skills/engineering/practices/gnome-shell-extension-development/references/accounts-and-api-reporting.md) |
| Stable per-account identity, persisted synthetic examples, exact deletion scope, failed writes and delayed-operation fencing | Account reference |
| Ordinary API keys may not expose reporting; uncapped spend, capped allowance and prepaid balance differ | Account reference |
| Public bugs and private security reports must have separate destinations and failure behavior | Account reference |
| Decoration must not affect reading geometry; allocation-time child resizing can invalidate native foreground layout | [Rendering reference](../../knowledge/skills/engineering/practices/gnome-shell-extension-development/references/native-layout-and-effects.md) |
| Glyph/raster continuity, scroll-shadow gutters and whole-popup transparency need rendered evidence | Rendering reference |
| Default material/effect icons must match shared actual rendering, including optical presets outside JSON | Rendering reference |
| WebGL previews do not establish native popup effects; bounded motion needs source-bound frame and lifecycle evidence | Rendering reference |
| Native evaluation transport success is not a passing or completed probe | [Delivery reference](../../knowledge/skills/engineering/practices/gnome-shell-extension-development/references/verification-and-release.md) |
| Private bus alone is insufficient isolation; absent configuration differs from an invalid empty JSON file | Delivery reference |
| Standard ZIP layout, installed-directory loading, byte auditing, tag/manifest/checksum and public download verification | Delivery reference |
| On-disk installation and current-session loaded version are separate claims | Delivery reference |
| Green analysis jobs can coexist with a failed security alert aggregate; test assertions deserve triage | [Security scanning skill](../../knowledge/skills/engineering/practices/ci-security-scanning/SKILL.md) |

## Behavioral evaluation and review

A read-only independent evaluator first used the previous GNOME skill against
five concrete scenarios. It found that general guidance supported investigation
but did not explicitly address the disputed boundaries. This establishes coverage
gaps; it does not establish that an agent failed every scenario without guidance.

The updated skill was replayed against those scenarios and an additional
preview/native-output scenario. Review required clearer async completion contracts,
cross-process atomic ownership assumptions and product-specific performance
budgets. Those corrections were made; the targeted follow-up reported no remaining
findings. The review verified instructions, not the linked implementation's
runtime correctness.

The security skill had a separate baseline using green language analyses plus a
red CodeQL aggregate pointing to URL substring assertions. Its existing general
triage rule was retained and the missing boundary was made explicit.

The committed [delivery scenario](../../evals/scenarios/gnome-native-delivery-boundaries/scenario.json)
and [connector/theme scenario](../../evals/scenarios/gnome-connector-theme-contracts/scenario.json)
are advisory behavioral cases. Their regex checks are smoke checks; their semantic
rubrics distinguish correct conclusions from parroting input. Static scenario
validation is separate from a live harness run. The external-CLI live runner was
not invoked as part of this update.

Adding the scenarios exposed a fixed-inventory assertion in the deterministic
suite. The test now checks that seeded scenarios remain present and validates the
entire discovered set, allowing new valid cases without copying a new fixed count.

## Verification commands

The repository gate is the acceptance surface:

```sh
python3 scripts/coacus.py refresh
python3 scripts/coacus.py generate
python3 scripts/coacus.py validate
python3 scripts/coacus.py check
python3 scripts/coacus.py completeness
python3 scripts/coacus_eval.py validate
python3 -m unittest discover -s tests
```

The canonical skill frontmatter retains Coacus-supported tags. An auxiliary
Codex-only quick validator rejected that pre-existing field; the Coacus source
validator is authoritative for this repository, and its schema was not weakened
to accommodate the auxiliary tool. Existing word-budget warnings in unrelated
workflow bodies are not introduced by this update.

Generated indexes and provenance hashes are regenerated/refreshed by repository
tools; none are edited by hand. Local installation is refreshed through the
framework installer and its verification output distinguishes present harnesses
from absent ones. Installation does not claim that an already-running agent has
reloaded instructions held in its conversation context.

On this date, generation, source/artifact validation, drift checking,
completeness, static eval validation and the full deterministic suite passed.
Local installer verification passed for OpenCode, Claude Code, Antigravity,
Codex and Command Code, with no missing or drifted recorded files. Cursor was
not detected and was skipped; no install was forced. A second read-only
verification of each present harness also passed. The independent reviewer
accepted the inventory-test correction and found no material overstatement in
this record; it did not independently rerun the suite or installer.
