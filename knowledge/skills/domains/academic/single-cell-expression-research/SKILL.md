---
name: single-cell-expression-research
description: >-
  Guides research analysis of single-cell expression data and annotated matrices. Use when preparing, combining or interpreting single-cell datasets and sample-level comparisons.
---

# Single-cell expression research

1. Record sample, donor, condition, batch and assay provenance. Preserve the meaning and origin of each matrix and layer; integer-looking values do not establish raw-count provenance.
2. Validate cell and feature identifiers, axis alignment, missing data and quality-control thresholds. Record removed cells and features and assess how filtering might affect the research question.
3. Before combining datasets, reconcile feature identifiers and record which features were measured in each dataset. An unmeasured feature is not necessarily a biological zero; preserve that distinction when a sparse outer join fills absent entries.
4. Record normalization, feature selection, dimensionality reduction, batch adjustment and clustering choices. Evaluate whether batch adjustment removes biological signal; embeddings and clusters are exploratory representations, not direct proof of cell identity or causal relationships.
5. For condition-level comparisons, preserve independent biological samples and donor pairing. Use an analysis appropriate for the experimental unit and count representation; many cells from one donor do not create independent biological replicates. Check design identifiability, uncertainty and multiple testing.
6. Record dataset releases and query filters for population-scale resources. Regulatory networks inferred from expression are candidate associations; assess input coverage and stability, and seek independent evidence. They do not by themselves establish direct regulation or causality.

The workflow was informed by the upstream [annotated matrix](https://github.com/K-Dense-AI/scientific-agent-skills/blob/5f2bc0341354fd5590aef76a533ada1e1e5b4e62/skills/anndata/SKILL.md) and [single-cell analysis](https://github.com/K-Dense-AI/scientific-agent-skills/blob/5f2bc0341354fd5590aef76a533ada1e1e5b4e62/skills/scanpy/SKILL.md) skills. Consult the selected format and method documentation for exact input contracts.
