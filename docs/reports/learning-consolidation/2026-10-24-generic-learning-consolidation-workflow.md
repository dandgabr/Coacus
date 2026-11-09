# Generic learning-consolidation workflow

## Scope and duplicate audit

The existing `methodology/workflows/retro/SKILL.md` ranks possible improvements and recommends checks or standards notes. It does not carry a selected lesson through evidence review, canonical-owner selection, human approval and promotion. The existing reports `2026-10-08-elfvision-learning-consolidation.md` and `2026-10-08-gnome-quota-delivery-learnings.md` document project-specific transfers, not a reusable consolidation procedure. The new workflow fills that gap and leaves `retro` focused on discovery.

## Canonical destination

- `methodology/workflows/learning-consolidation/SKILL.md` defines the reusable process: capture only relevant lessons, distinguish observed facts from inference, protect sensitive material, reuse one canonical owner, propose before editing, and verify approved changes through Coacus generation and validation.
- `evals/scenarios/learning-consolidation/scenario.json` exercises a repeated evidence-backed reporting failure, an unsupported one-off preference, private details, canonical-owner selection and the human-approval boundary.
- The authored workflow is recorded in `sources.lock.json` by `coacus.py generate`. Catalog, discovery and README counts are generated or reconciled from repository sources; generated files are not hand-edited.

## Verification

The final run used the repository `.venv` and completed `coacus.py refresh`, `generate`, `validate`, `check`, `completeness`, `coacus_eval.py validate`, `python -m unittest discover -s tests`, and `git diff --check` successfully. The deterministic suite reported 594 tests passing. The eval was statically validated; no live harness run or harness installation was performed.
