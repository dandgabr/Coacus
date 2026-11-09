---
name: isotope-flux-research
description: >-
  Guides research interpretation of carbon isotope tracing and metabolic flux inference. Use when assessing isotope-labeling inputs, model assumptions, flux identifiability or uncertainty.
---

# Carbon isotope flux research

1. Define the biological question, network, compartments and flux units. Distinguish measured labeling and extracellular rates from inferred intracellular fluxes; an optimization result is not a direct flux measurement.
2. Document the tracer composition and purity, atom mappings, measured fragments, correction history, replicate structure and uncertainty. A stoichiometric network alone does not determine atom mappings. Do not invent missing mappings or measurement errors.
3. Establish whether the selected method assumes metabolic steady state, isotopic steady state or both. Stable metabolite abundance alone does not establish stable labeling; time-dependent experiments require an appropriate nonstationary model.
4. Specify mass-balance constraints, justified bounds, external flux information and measurement covariance where available. State whether results are absolute or relative; labeling fractions alone do not establish an absolute rate.
5. Check fit quality, alternative feasible solutions and flux identifiability with appropriate sensitivity or profile analyses. Report poorly constrained fluxes, model assumptions and missing evidence rather than treating one optimizer solution as unique biological truth.

This guidance was informed by the [upstream carbon-tracing workflow](https://github.com/K-Dense-AI/scientific-agent-skills/blob/5f2bc0341354fd5590aef76a533ada1e1e5b4e62/skills/13c-metabolic-flux/SKILL.md). Consult the selected method's documentation and domain experts for its assumptions and input contracts.
