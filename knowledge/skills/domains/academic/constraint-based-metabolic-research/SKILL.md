---
name: constraint-based-metabolic-research
description: >-
  Guides research interpretation of constraint-based metabolic network models. Use when assessing flux balance, feasible flux ranges, medium assumptions or model-based perturbation results.
---

# Constraint-based metabolic research

1. Record the model source and revision, compartment and reaction definitions, units, medium, bounds, objective, solver and numerical tolerances. Check mass and charge consistency where the model provides the information needed.
2. Check solver status and feasibility before reporting an optimum. Compare results against biologically justified media and constraints; an arbitrary objective or bound can change the prediction.
3. Interpret flux variability bounds as separate optimizations: extrema for different reactions need not occur together in one feasible solution. Record sampling settings and assess whether they explore the intended feasible region.
4. Distinguish constraint-based predictions from measured fluxes, kinetic rates and experimentally confirmed growth. Report alternate optima, untested assumptions and missing thermodynamic or regulatory constraints.

Consult the selected model and solver documentation for the applicable contract. The upstream [constraint-based modeling skill](https://github.com/K-Dense-AI/scientific-agent-skills/blob/5f2bc0341354fd5590aef76a533ada1e1e5b4e62/skills/cobrapy/SKILL.md) informed the research-scope comparison; its code and examples are not incorporated here.
