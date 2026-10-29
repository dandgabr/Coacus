---
name: measurement-units-uncertainty
description: >-
  Guides dimensional checks and measurement uncertainty evaluation. Use when converting scientific quantities, evaluating a measurement model, reporting uncertainty or checking physical plausibility.
---

# Measurement units and uncertainty

## Workflow

1. Identify the measurand, measurement model, input quantities, units, corrections and intended use. Record the origins of the input estimates and uncertainties, including shared sources of correlation. Do not invent missing uncertainties.
2. Check dimensions at every calculation boundary. Apply conversion factors to both estimates and uncertainties. For an affine conversion, apply scale and offset to each value or interval endpoint, but only the absolute scale factor to an uncertainty or interval width. For example, 20 ± 1 °C corresponds to 293.15 ± 1 K, and the endpoints 19 °C and 21 °C become 292.15 K and 294.15 K.
3. Choose an uncertainty propagation method suited to the measurement model and available information. Account for correlated inputs; state assumptions about distributions and any linear approximation. If inputs or assumptions are insufficient, identify what is missing rather than reporting a fabricated uncertainty.
4. Report the estimate and units together with the uncertainty type and method. If reporting an expanded uncertainty or coverage interval, state the coverage factor or probability and the assumptions supporting it. Round consistently with the uncertainty.
5. Check the result against an appropriate physical scale and document model limitations. Dimensional consistency or numerical convergence alone does not prove a result is physically valid.

## References

Consult the [BIPM guides to measurement uncertainty](https://www.bipm.org/en/publications/guides) and [NIST conversion factors](https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b9) for the applicable measurement. The workflow was informed by the [upstream uncertainty-and-units skill](https://github.com/K-Dense-AI/scientific-agent-skills/blob/5f2bc0341354fd5590aef76a533ada1e1e5b4e62/skills/uncertainty-and-units/SKILL.md).
