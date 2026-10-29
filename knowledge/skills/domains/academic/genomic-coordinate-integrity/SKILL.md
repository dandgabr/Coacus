---
name: genomic-coordinate-integrity
description: >-
  Checks genomic interval and variant coordinates across file formats and reference assemblies. Use when joining genomic datasets, converting intervals, reconciling contig names, or investigating potential off-by-one and reference mismatches.
---

# Genomic coordinate integrity

Use this skill for coordinate interpretation and data integration. Do not infer a clinical interpretation from a coordinate match.

## Workflow

1. Record the reference assembly, contig, coordinate convention, interval semantics, and source format for each input. Resolve missing information before joining datasets; similar assembly names are not proof of identical sequences.
2. Validate positions and interval order against the source convention and known contig length before conversion. For a nonempty interval on the same reference, convert a one-based inclusive interval `[start, end]` to a zero-based half-open interval `[start - 1, end)`. The inverse adds one to the start. Verify length is unchanged and check a known single-base example. Do not apply this rule blindly to zero-length insertions, circular intervals, or transcript coordinates; a valid zero-length feature requires its own format-specific semantics.
3. Compare contig dictionaries and reference sequences. A name prefix change is not an assembly conversion. Assembly changes require an appropriate mapping and explicit reporting of unmapped, ambiguous, or split intervals.
4. Treat variants as alleles with reference context, not only intervals. Confirm reference alleles against the correct sequence; normalize comparable representations with a validated tool and record its settings. Do not merge symbolic or complex alleles merely because their positions coincide.
   For interval operations, specify whether touching boundaries count as overlaps, whether strand matters and whether the result represents a consensus interval or basewise support; validate those semantics with small examples.
5. Report input and output conventions, reference identifiers, transformations, rejected records, unresolved mismatches, and limitations. Keep the original records available for audit.

## Source for further review

The workflow was informed by the [genomic-coordinates skill at the reviewed upstream commit](https://github.com/K-Dense-AI/scientific-agent-skills/blob/5f2bc0341354fd5590aef76a533ada1e1e5b4e62/skills/genomic-coordinates/SKILL.md). Consult the authoritative specification of each actual input format and tool before applying conversions.
