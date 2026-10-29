---
name: bulk-rna-seq-research
description: >-
  Guides reproducible bulk RNA sequencing analysis from sample metadata to differential expression. Use when preparing bulk RNA-seq reads, quantification results, count matrices or downstream comparisons.
---

# Bulk RNA sequencing research

This skill covers research workflows for bulk samples. Single-cell analysis and clinical interpretation require different methods and additional review.

1. Define the biological question, biological replicates, experimental unit, contrast and potential batch effects. Check that the design can distinguish the intended effect from confounding, that the model matrix is identifiable, and that sufficient residual degrees of freedom remain; document missing samples and metadata.
2. Validate sample identities, file pairing, sequencing layout and strandedness. Record quality-control findings and investigate unexpected read quality, contamination or sample swaps before interpreting results.
3. Record reference genome and annotation releases, quantification method, tool versions and parameters. Use a consistent quantification approach across the comparison and retain the transcript-to-gene mapping where relevant.
4. Assemble the count matrix with exact sample and feature identifiers; check duplicates, missing values and agreement with metadata. Preserve the count type and any length correction or offsets required by the downstream method. Do not pass normalized expression values as raw counts or apply a correction twice.
5. Fit an analysis suitable for the design and input representation. Check quality diagnostics, report effect estimates and uncertainty, account for multiple testing, and separate exploratory findings from prespecified contrasts. A differentially expressed gene or enriched pathway is not by itself evidence of causation.
6. For pathway analysis, preserve identifier mappings and the tested-gene universe. Choose a method suited to the selected or ranked input and report the multiple-testing family. Expression direction or enrichment alone does not establish pathway activation.

The workflow was informed by the upstream [bulk RNA-seq](https://github.com/K-Dense-AI/scientific-agent-skills/blob/5f2bc0341354fd5590aef76a533ada1e1e5b4e62/skills/bulk-rnaseq/SKILL.md) and [pathway enrichment](https://github.com/K-Dense-AI/scientific-agent-skills/blob/5f2bc0341354fd5590aef76a533ada1e1e5b4e62/skills/pathway-enrichment/SKILL.md) skills. Consult the current documentation of the selected pipeline and analysis methods for their exact input contracts.
