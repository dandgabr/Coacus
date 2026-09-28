---
name: "ux-designer"
description: "Provides the UX design discipline (experience design separated from UI craft): the ISO 9241-210 definition and UX honeycomb, process frameworks (Double Diamond, design thinking, Lean UX, JTBD, continuous discovery), the user-research method map, usability heuristics and metrics (Nielsen's 10, SUS, HEART), information architecture and journey mapping, and ethics (WCAG as baseline, deceptive patterns). Use when planning research, structuring experiences, evaluating usability or governing UX ethics."
---

# AI Skill: UX Design (Experience Discipline)

The UX discipline: all aspects of the end-user's interaction with a company, its services and its products (Norman & Nielsen) — "a person's perceptions and responses that result from the use or anticipated use of a product, system or service" (ISO 9241-210:2019). Distinct from UI craft (see [ui-designer](../ui-designer/SKILL.md)): usability and interface design are subsets of the whole experience. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Planning discovery, research or usability evaluation.
- Structuring information architecture, flows or journeys.
- Defining UX metrics tied to business KPIs.
- Governing ethical design (dark-pattern review).

---

## 🧭 Discipline Boundaries

- **UX owns the whole journey:** branding, function, usability, acquisition through reflection (IxDF; Norman's "no product is an island"). Deliverables: research reports, personas, journey maps, "how might we" statements, user stories, IA/sitemaps, flows, wireframes, usability and heuristic-evaluation reports.
- **UI owns the surface** — the canonical handoff is UX wireframes → UI hi-fi craft → dev specs, iterating continuously (see ui-designer).
- **UX honeycomb** (Morville, 2004): useful, usable, desirable, findable, accessible, credible, valuable — still the standard evaluative model; each facet forces explicit trade-offs.
- **Layered model:** Garrett's five planes (strategy → scope → structure → skeleton → surface) map the discipline's deliverables.

---

## 🔁 Process Frameworks

- **Double Diamond** (Design Council, 2004): Discover → Define → Develop → Deliver; divergent→convergent twice; the Framework for Innovation adds four principles (people first; communicate visually; co-create; iterate) and a methods bank.
- **Design thinking** (IDEO/d.school): human-centered, integrating desirability, feasibility, viability; the empathize/define/ideate/prototype/test loop is the de-facto UX process.
- **Lean UX** (Gothelf & Seiden, 2013/2021): assumptions → hypotheses → MVPs → measured outcomes; "outcomes over outputs".
- **Jobs-to-be-Done** (Christensen et al., HBR 2016): customers "hire" products to make progress in a circumstance; optimize the job, not attributes.
- **Continuous discovery** (Torres, 2021): weekly customer touchpoints by the product trio; the opportunity solution tree links outcome → opportunities → solutions → assumption tests.

---

## 🔬 User Research Methods

- **Method map** (Rohrer, NN/g): position every method on attitudinal vs behavioral, qualitative vs quantitative, and context of use; time phases — generative (field studies, diaries, interviews, surveys), formative (card sorting, tree testing, usability tests), summative (benchmarks, A/B, analytics). Qual answers *why/how to fix*; quant answers *how many/how much*.
- **Interviews:** attitudinal; interview past behavior and circumstances, not hypotheticals (Torres). **Contextual inquiry** (Beyer & Holtzblatt): master–apprentice field method; principles — context, partnership, interpretation, focus.
- **Card sorting:** open for discovery, closed to validate existing IA (prefer tree testing for that); 30–50 cards; ≥15 participants qualitative, 30–50 quantitative; analyze via similarity matrices/dendrograms.
- **Tree testing:** label-only hierarchy evaluation — success, time, directness; standard recipe: usability-test the current site → card sort options → tree-test the candidate hierarchy.
- **Diary studies** for longitudinal behavior; **analytics/funnels** for instrumented behavioral quant; **A/B tests** for causal comparisons.
- **Sample sizes (Nielsen):** with ~31% per-user discovery rate, 5 users find ~85% of problems per iteration — run 3 studies × 5 users, redesigning between rounds; ~20 users for quantitative studies; known critiques (Faulkner 2003: five users under-count cumulative problems across a full user population) — apply the rule only to iterative qualitative discovery.

---

## 📏 Usability and Evaluation

- **Nielsen's 10 heuristics** (1994; refined from Molich & Nielsen 1990): visibility of system status; match with the real world; user control; consistency and standards; error prevention; recognition over recall; flexibility and efficiency; aesthetic and minimalist design; error recognition/recovery; help and documentation. Used for heuristic evaluation (3–5 evaluators).
- **Interaction laws:** Fitts's law (bigger/closer targets are faster — underpins WCAG 2.5.8); Hick's law (RT grows with equally probable choices — simplify menus, progressive disclosure); cognitive load (intrinsic vs extraneous — minimize clutter, build on existing mental models, offload memory).
- **Metrics:** SUS (10-item, 0–100; corpus average ≈ 68 as the "good" benchmark [standard figure, not re-verified]); Google HEART (Rodden, Hutchinson & Fu, CHI 2010 — happiness, engagement, adoption, retention, task success via goals→signals→metrics); task success and time-on-task as the core usability metrics.
- **Usability testing** (Moran, NN/g): facilitator + tasks + participant; realistic scenario tasks that don't leak answers; think-aloud as the default protocol; qualitative ~5 users vs quantitative benchmarks; remote moderated/unmoderated; a "discount" study is ~3 days.

---

## 🗺️ Information Architecture and Flows

- **IA canon:** Rosenfeld & Morville (*Information Architecture for the World Wide Web*); the repo's dedicated IA chapter lives in [ui-ux-principles](../../engineering/practices/ui-ux-principles/SKILL.md).
- **Flows hierarchy:** task flows (single-goal steps) → user flows (end-to-end paths) → journey maps (experience layer with emotion/mindset); journey maps have five components (actor; scenario + expectations; phases; actions/mindsets/emotions; opportunities) — one persona per map.
- **Service blueprints:** customer actions, frontstage, backstage, support processes across the lines of interaction, visibility and internal interaction — best for omnichannel journeys.
- **Mental models** (NN/g): what users *believe* about a system, shaped by other products; remediate by matching the system to the model or teaching a better one. **Wayfinding:** Lynch's five elements (paths, edges, districts, nodes, landmarks) applied to navigation.

---

## ⚖️ UX Writing, Accessibility and Ethics

- **UX writing:** 79% of users scan; concise + scannable + objective language improved usability 124% (Nielsen, 1997); scannable text, meaningful subheads, one idea per paragraph, inverted pyramid, ~half the word count, no marketese; error microcopy per heuristic #9 (plain language, precise problem, constructive solution).
- **Accessibility as UX baseline:** WCAG 2.2 (W3C Recommendation, Dec 12, 2024) — 4 principles, 13 guidelines; conformance "will also often make web content more usable" in general; default target AA. Inclusive design (Microsoft): recognize exclusion; learn from diversity; solve for one, extend to many.
- **Ethics:** the persuasion/deception boundary — authentic social proof vs hidden choices; dark-pattern taxonomy (Gray et al., CHI 2018: nagging, obstruction, sneaking, interface interference, forced action); deceptive patterns on >10% of 11k crawled shopping sites (Mathur et al., 2019); regulatory teeth (FTC actions, GDPR consent); mitigation: cognitive walkthrough with the most vulnerable persona in mind. Sludge (Thaler & Sunstein) names the aggregate cost.

---

## ⚠️ Pitfalls

- Treating usability testing as validation theater instead of iteration fuel; misapplying the 5-user rule to quantitative or single-shot studies.
- Journey maps without a metrics layer (buy-in dies); one map for multiple personas.
- Interviewing hypotheticals instead of past behavior; hybrid card sorts that bias participants.
- Optimizing attributes instead of jobs; shipping deceptive patterns that convert today and sue tomorrow.

---

## 📚 Sources

- IxDF, "What is User Experience (UX) Design?", updated 2026 — https://www.interaction-design.org/literature/topics/ux-design
- ISO 9241-210:2019, ISO — https://www.iso.org/standard/77520.html
- Peter Morville, "User Experience Design" (honeycomb), Semantic Studios, 2004 — https://semanticstudios.com/user_experience_design/
- Don Norman & Jakob Nielsen, "The Definition of User Experience (UX)", NN/g, 1998 — https://www.nngroup.com/articles/definition-user-experience/
- Design Council, "Framework for Innovation" (Double Diamond) — https://www.designcouncil.org.uk/resources/framework-for-innovation/
- Jeff Gothelf & Josh Seiden, *Lean UX*, O'Reilly, 2013/2021 — https://www.jeffgothelf.com/
- Christensen, Hall, Dillon & Duncan, "Know Your Customers' 'Jobs to Be Done'", HBR, 2016 — https://hbr.org/2016/09/know-your-customers-jobs-to-be-done
- Teresa Torres, *Continuous Discovery Habits*, 2021 — https://www.producttalk.org/
- Christian Rohrer, "When to Use Which User-Experience Research Methods", NN/g, 2022 — https://www.nngroup.com/articles/which-ux-research-methods/
- Tankala & Sherwin, "Card Sorting", NN/g, 2024 — https://www.nngroup.com/articles/card-sorting-definition/
- Page Laubheimer, "Tree Testing", NN/g, 2023 — https://www.nngroup.com/articles/tree-testing/
- Jakob Nielsen, "Why You Only Need to Test with 5 Users", NN/g, 2000 — https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/
- Jakob Nielsen, "10 Usability Heuristics for User Interface Design", NN/g, 1994/2024 — https://www.nngroup.com/articles/ten-usability-heuristics/
- Kate Moran, "Usability Testing 101", NN/g, 2019 — https://www.nngroup.com/articles/usability-testing-101/
- Rodden, Hutchinson & Fu, "Measuring the user experience on a large scale" (HEART), CHI 2010 — https://doi.org/10.1145/1753326.1753687
- Sarah Gibbons, "Journey Mapping 101", NN/g, 2018 — https://www.nngroup.com/articles/journey-mapping-101/
- Sarah Gibbons, "Service Blueprints: Definition", NN/g, 2017 — https://www.nngroup.com/articles/service-blueprints-definition/
- Jakob Nielsen, "How Users Read on the Web", NN/g, 1997 — https://www.nngroup.com/articles/how-users-read-on-the-web/
- W3C, "WCAG 2.2", Recommendation, Dec 12, 2024 — https://www.w3.org/TR/WCAG22/
- Microsoft Inclusive Design — https://inclusive.microsoft.design/
- Colleen Gray et al., "The Dark (Patterns) Side of UX Design", CHI 2018 — https://doi.org/10.1145/3173574.3174108
- Meta Rosala, "Deceptive Patterns in UX", NN/g, 2023 — https://www.nngroup.com/articles/deceptive-patterns/

---

## 🔗 Integration with Other Skills

- For the surface craft this discipline feeds, see [ui-designer](../ui-designer/SKILL.md).
- For the orchestrating generalist role, see [ui-ux-designer](../ui-ux-designer/SKILL.md).
- For research synthesis discipline, see [ai-model-evaluation](../../domains/industry/ai-model-evaluation/SKILL.md) and [human-in-the-loop-ml](../../data/human-in-the-loop-ml/SKILL.md).
- For conformance depth, see [web-accessibility-wcag](../../engineering/practices/web-accessibility-wcag/SKILL.md).
