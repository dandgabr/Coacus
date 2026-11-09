# UI Style Architecture Standard

**Status:** normative  
**Scope:** every visual design skill under `knowledge/skills/domains/design/ui-style-*` and related showcase assets.

## Purpose

This standard defines the capabilities a canonical visual-style skill must teach: identifiable lineage, surfaces and tokens, readable components, responsive composition, interaction and verifiable limits. The catalog supplies the current inventory. A showcase is a consumer of these skills, not their platform or component contract.

---

## 1. Architectural Integrity & Single Style Purity

1. **Identifiable lineage:** Preserve the named style's distinguishing signals and boundaries with neighboring traditions. Explain a documented dialect or adaptation explicitly; do not silently blend unrelated traditions. A historical reference can inform an adaptation without making two operating environments identical.
2. **Anti-AI Slop Mandate:** A canonical UI style MUST NOT rely on generic AI design crutches:
   - Floating pastel pill badges with arbitrary sparkle emojis.
   - Ungrounded, blurred ambient black drop shadows applied uniformly to every card.
   - Meaningless 1px borders without physical, structural, or typographic rationale.
   - Arbitrary elastic bounce curves applied indiscriminately to all interactive triggers.
3. **Deterministic Verification:** Every UI style skill must pass `coacus.py validate`, `coacus_design_lint.py`, and the standard unit test suite.

---

## 2. Canonical 14-Part Content Architecture

Every package under `knowledge/skills/domains/design/ui-style-*` must cover the following content. Keep identity, activation, essential constraints and routing in `SKILL.md`; place substantial implementation recipes and conditional material in linked references. The sequence is a reading guide, not a requirement to inflate a concise skill with irrelevant lighting or audio sections.

```
┌─────────────────────────────────────────────────────────────────┐
│              CANONICAL UI STYLE SECTION SEQUENCE                │
├─────────────────────────────────────────────────────────────────┤
│ 1. Frontmatter (YAML: name, description with triggers)          │
│ 2. Title & Historical Epigraph                                  │
│ 3. 🧭 When to Activate                                          │
│ 4. 🕰️ Definition, Lineage, and Timeline (Absolute Style Vetos)   │
│ 5. 🎨 Visual DNA & Subgenre Taxonomy (ASCII Comparison Matrix)  │
│ 6. 📐 Lighting Physics, Specular Splits & Surfaces              │
│ 7. 🏷️ Complete Design Tokens (CSS Custom Properties)            │
│ 8. 🔤 Typography & Lettering Architecture                       │
│ 9. 🖱️ Interaction Dynamics, Sound Cues & Motion                 │
│ 10. 🧩 Canonical Component Specifications (Concrete HTML & CSS) │
│ 11. ♿ Accessibility & Environmental Contrast (WCAG 2.2 AA/AAA)  │
│ 12. ✅ When to Use / ❌ When to Avoid                           │
│ 13. 📚 Authoritative Sources & Historical Artifacts             │
│ 14. 🔗 Cross-Skill Integration & Dialect Relations              │
└─────────────────────────────────────────────────────────────────┘
```

### Section Guidelines

1. **Frontmatter:** `name` in kebab-case matching the directory name (`ui-style-<slug>`). `description` in third person, trigger-oriented, under 1024 characters.
2. **Title & Historical Epigraph:** Use a clear canonical title. Include a historical quote only when its wording and attribution have been verified; an epigraph is optional.
3. **When to Activate:** Bulleted list of concrete project scenarios, operational requirements, and user experience objectives that trigger this skill.
4. **Definition, Lineage, and Timeline:** Distinguish verified history from interpretation. Explain neighboring styles and common misapplications. A style boundary does not override the user's functional requirements or accessibility constraints.
5. **Visual DNA & Subgenre Taxonomy:** High-level aesthetic pillars accompanied by a structured ASCII matrix contrasting two subgenres or historical phases of the style.
6. **Lighting Physics, Specular Splits & Surfaces:** Explain the surface model appropriate to the style, including intentionally flat or typographic treatments. Physical highlights, shaders and acoustic metaphors are conditional techniques, not universal requirements.
7. **Complete Design Tokens:** Define semantic canvas, surface, ink, accent, boundary and state roles. When multiple appearances are requested, account for the entire painted stack and component states in each. Root selectors, token syntax and theme attributes belong to platform examples; do not impose a consumer's DOM contract.
8. **Typography & Lettering Architecture:** Prescribed font stacks, weight hierarchies, display vs body pairings, letter-spacing tracking deltas, and OpenType feature flags.
9. **Interaction Dynamics, Sound Cues & Motion:** Define meaningful states and optional motion appropriate to the product. Sound requires an explicit use case and user control. An appearance variant need not change layout or add animation.
10. **Canonical Component Specifications:** Supply realistic, accessible component examples that demonstrate the style rather than isolated color swatches. Web examples use semantic HTML and scoped CSS; equivalent native components can implement the same principles.
11. **Accessibility & Environmental Contrast:** Verify the applicable contrast and interaction requirements on rendered output. Distinguish a token calculation, a sampled rendering audit and a conformance assessment. Include focus, reduced motion and access to content larger than the visible region.
12. **When to Use / When to Avoid:** Explicit binary recommendations preventing misapplication in inappropriate product contexts.
13. **Authoritative Sources & Historical Artifacts:** Primary historical texts, museum monographs, architectural specifications, or design patents.
14. **Cross-Skill Integration & Dialect Relations:** Clear pointers to related or opposing styles within the Coacus design corpus.

---

## 3. Consumer and Effect Lifecycle Contract

Consumers define their own component tree, style registry, appearance identifiers and mounting API. Keep any concrete showcase mapping in the consumer's integration documentation. Never infer that a valid style must contain a particular number of variants, use a particular root selector or run in a browser.

For effects, declare whether the layer belongs to the viewport, the scroll container or the complete content. Define mounting, updates, pause/resume and teardown. Release owned listeners, observers, timers, animation callbacks, drawing surfaces, nodes and temporary styles when the owning context changes. A higher numeric layer order does not escape an ancestor's stacking context.

Reduced motion may omit decorative effects. Essential content, navigation and state must still initialize and remain reachable; an early return is appropriate only when it preserves that contract. A static appearance must be complete without an animation finishing.

Before accepting interface changes, apply [Rendered Interface Verification](../../knowledge/skills/engineering/practices/ui-design-craftsmanship/references/rendered-interface-verification.md). Check the actual tree, reading surfaces, component states and available container dimensions, including wide/short and tall/narrow contexts. Verify the visible result of effects, not merely their state marker. For published interfaces, verify the revision actually served through the asset dependency graph.

## 4. Authority and Exceptions

Functional requirements and applicable accessibility obligations constrain visual direction. Style-specific identity guides the remaining choices; general taste heuristics are recommendations within that context. A deliberate monochrome, neon, multicolor or gradient treatment is not automatically a defect.

Record an exception's authority, scope, evaluated revision and residual limitations. A user may authorize a release with stated limitations; that authorization does not turn an unmeasured technical requirement into a passing result or retroactively approve a different revision.
