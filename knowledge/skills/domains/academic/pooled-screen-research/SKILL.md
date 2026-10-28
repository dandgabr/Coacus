---
name: pooled-screen-research
description: >-
  Guides research analysis of existing pooled perturbation screen counts. Use when validating guide libraries, sample contrasts, replicate quality or gene-level enrichment and depletion results.
---

# Pooled perturbation screen research

1. Record the supplied library, perturbation modality, sample identifiers, selection, time points, baseline, controls and biological replicates. Specify the treatment and comparison explicitly; sequencing lanes are not independent biological replicates.
2. Verify guide and gene identifiers, library coverage, count quality, sample alignment and duplicate or missing records. Inspect replicate consistency and normalization assumptions before fitting a contrast.
3. Choose a method suited to the design and controls. Report guide and gene effects, the direction of the contrast, uncertainty and the multiple-testing family; keep enrichment and depletion interpretations distinct.
4. Preserve the input counts, library release, parameters and quality exclusions. A screen hit is a hypothesis requiring appropriate follow-up, not proof of a gene's function or mechanism.

This guidance was informed by the [upstream pooled-screen analysis skill](https://github.com/K-Dense-AI/scientific-agent-skills/blob/5f2bc0341354fd5590aef76a533ada1e1e5b4e62/skills/mageck/SKILL.md). Consult the selected analysis method's documentation for its input and statistical assumptions.
