---
name: flow-cytometry-research
description: >-
  Guides research flow-cytometry data integrity, compensation and gating review. Use when inspecting cytometry files, reproducing a gating strategy or comparing populations across samples.
---

# Flow-cytometry research

1. Record sample identity, acquisition settings, detector and marker labels, controls and biological replicate. Check for duplicate or ambiguous sample and channel identifiers; source metadata may contain sensitive information.
2. Establish whether values are raw, scaled, compensated or transformed. Verify that the spillover matrix corresponds to the detector channels and controls; do not apply compensation twice. Apply compensation before nonlinear transforms when using that workflow, and ensure gate coordinates use the same representation. Record the transformation and its parameters.
3. Preserve the gating hierarchy, parent populations, sample-specific settings and strategy version. Inspect controls and representative samples for gate placement and quality. A workspace that imports successfully is not by itself evidence of equivalent populations in another implementation.
4. Report counts and percentages with their denominator, excluded events and sample-level quality. Use independent biological samples, not individual events, as the replication unit for condition-level inference.
5. Preserve the input files, transformations, compensation and gating provenance. Treat computational population summaries as research results; they do not independently establish a diagnosis or clinical validation.

This guidance was informed by the upstream [file inspection](https://github.com/K-Dense-AI/scientific-agent-skills/blob/5f2bc0341354fd5590aef76a533ada1e1e5b4e62/skills/flowio/SKILL.md) and [gating workflow](https://github.com/K-Dense-AI/scientific-agent-skills/blob/5f2bc0341354fd5590aef76a533ada1e1e5b4e62/skills/flowkit/SKILL.md). Consult the selected instrument and analysis software documentation for actual format and transformation behavior.
