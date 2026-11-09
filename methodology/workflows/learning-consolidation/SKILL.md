---
name: learning-consolidation
description: >-
  Consolidates an evidence-backed lesson selected by retro or explicitly
  requested into a proposal for human review.
---

# Learning Consolidation

Turn a selected lesson from completed work into a reviewable proposal for Coacus. This workflow promotes reusable knowledge; it does not train model weights or preserve a task transcript.

## When to activate

Activate after `retro` selects a relevant candidate or when a user explicitly requests consolidation. Do not run it automatically for every completed task. If no candidate can change a future decision, report that there is no reusable learning and stop.

## Establish the evidence

1. Record the observed outcome, expected outcome, and the evidence that connects them. Identify source files, revisions, test results, or authoritative references precisely enough for another reviewer to verify them.
2. Separate measured or directly observed facts from hypotheses and causal inferences. Do not promote an inference as fact. If evidence conflicts, is stale, or cannot be checked, state the uncertainty and stop before proposing a rule.
3. Keep only information needed to explain the reusable lesson. Remove secrets, personal data, private project details, and machine-specific paths. If safe redaction would change the meaning, do not retain the material.
4. Require recurrence, substantial impact, or an explicit user request. Do not generalize a one-off preference or a task-specific sequence into framework guidance.

## Find the canonical owner

1. Search the canonical sources for the concept and its aliases. Treat generated catalogs and manifests as navigation aids, not edit targets.
2. Reuse one existing owner whenever it covers the same decision. Update that source instead of creating a parallel rule, and link to it from other relevant locations rather than copying the rule.
3. Apply the mechanical-versus-judgment classification and destination rule from [`retro`](../retro/SKILL.md) without weakening or redefining it. This workflow verifies the canonical owner and manages evidence review and promotion.
4. Create a new canonical artifact only when the lesson has a distinct trigger and responsibility and no existing source can own it.
5. Keep canonical guidance harness-agnostic. Use the repository's authoring template and source conventions for any new artifact. External claims require a traceable authoritative source; imported artifacts use the provenance workflow.

## Prepare a proposal

Before changing any canonical source, prepare a concise proposal under `docs/temp/reports/learning-consolidation/`. Include:

- The observed facts and their evidence, separate from inferences.
- The generalized rule, its boundaries, and why it will change a future decision.
- The canonical owner to update, or the reason a distinct new owner is needed.
- The proposed diff and the behavioral case that would demonstrate the improvement.
- Unresolved questions, freshness limits, or evidence that could change the conclusion.

Present the proposal for human review. Do not edit canonical sources, generated artifacts, or harness installations before approval. If it is declined, make no canonical change. If the review requests changes, revise the proposal and request review again.

## Apply and verify an approved proposal

1. Apply the approved change to the selected canonical source. Add or update an evaluation when the change is intended to alter observable agent behavior. Do not copy the entire work history into the knowledge body.
2. For an accepted consolidation, write a short durable record under `docs/reports/learning-consolidation/` with the evidence, canonical destination, decision, and validation outcome. Do not publish rejected or unresolved proposals as canonical reports.
3. Refresh provenance through the repository's supported workflow when imported sources change. Never hand-edit generated catalog, discovery, or harness output; regenerate it from canonical sources.
4. Validate the changed source, generated-artifact drift, catalog completeness, and relevant behavioral scenarios. Distinguish static validation from a live harness run, and report unavailable checks rather than implying they passed.
5. Leave harness installation and activation as separate actions unless the user explicitly requests them.

If review or validation shows the lesson is already covered, prefer a justified no-change result over duplicate guidance. Record what existing source owns the concept and why it is sufficient.

## Related guidance

- [`retro`](../retro/SKILL.md) identifies and ranks possible improvements; this workflow consolidates a selected lesson.
- [Skill authoring](../../../docs/standards/skill-authoring.md) defines canonical skill structure and reuse.
- [Provenance](../../../docs/standards/provenance.md) governs imported knowledge sources.
- [Generated artifacts](../../../docs/standards/generated-artifacts.md) defines regeneration and drift checks.
