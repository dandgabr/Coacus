# UI Style Architecture Standard

**Status:** normative  
**Scope:** every visual design skill under `knowledge/skills/domains/design/ui-style-*` and related showcase assets.

## Purpose

This standard defines the mandatory architecture, structural sections, physical lighting models, token specifications, and accessibility guarantees for all 82 canonical UI visual styles in Coacus. It ensures that generative agents operating across any AI harness produce authentic, production-grade, anti-slop interfaces rooted in verified design history rather than generic AI cliches.

---

## 1. Architectural Integrity & Single Style Purity

1. **Pure Standalone Entity:** Every UI style skill represents a single, cohesive, uncompromised aesthetic movement or historical lineage. Composite or hybrid skills (grouping two distinct traditions under one slug) are strictly prohibited.
2. **Anti-AI Slop Mandate:** A canonical UI style MUST NOT rely on generic AI design crutches:
   - Floating pastel pill badges with arbitrary sparkle emojis.
   - Ungrounded, blurred ambient black drop shadows applied uniformly to every card.
   - Meaningless 1px borders without physical, structural, or typographic rationale.
   - Arbitrary elastic bounce curves applied indiscriminately to all interactive triggers.
3. **Deterministic Verification:** Every UI style skill must pass `coacus.py validate`, `coacus_design_lint.py`, and the standard unit test suite.

---

## 2. Canonical 12-Section Architecture

Every `SKILL.md` under `knowledge/skills/domains/design/ui-style-*` MUST implement the following structural sections in sequential order:

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
2. **Title & Historical Epigraph:** Canonical title accompanied by a verified historical quote from a founding figure or recognized manifesto of the movement.
3. **When to Activate:** Bulleted list of concrete project scenarios, operational requirements, and user experience objectives that trigger this skill.
4. **Definition, Lineage, and Timeline:** Accurate chronological history (genesis, apex, evolution). MUST include an explicit **Absolute Style Vetos** subsection detailing what the style is NOT and preventing common agent distortions.
5. **Visual DNA & Subgenre Taxonomy:** High-level aesthetic pillars accompanied by a structured ASCII matrix contrasting two subgenres or historical phases of the style.
6. **Lighting Physics, Specular Splits & Surfaces:** Precise definition of the optical world: light source angle, specular highlights, surface elevation mechanics, and shader/gradient mathematics.
7. **Complete Design Tokens:** Exhaustive `:root` and dark mode `[data-theme="dark"]` CSS custom property tokens covering backgrounds, typography inks, accents, borders, radii, shadows, and easing curves.
8. **Typography & Lettering Architecture:** Prescribed font stacks, weight hierarchies, display vs body pairings, letter-spacing tracking deltas, and OpenType feature flags.
9. **Interaction Dynamics, Sound Cues & Motion:** State change behavior (hover, focus, active), timing curves, and acoustic feedback profiles (frequency, duration, timbre).
10. **Canonical Component Specifications:** At least two fully realized, production-ready components featuring clean semantic HTML and modular CSS classes.
11. **Accessibility & Environmental Contrast:** Mathematical verification of contrast ratios conforming to WCAG 2.2 Level AA (minimum 4.5:1 text, 3:1 non-text controls) or Level AAA, focus indicator styling, and `prefers-reduced-motion` compliance.
12. **When to Use / When to Avoid:** Explicit binary recommendations preventing misapplication in inappropriate product contexts.
13. **Authoritative Sources & Historical Artifacts:** Primary historical texts, museum monographs, architectural specifications, or design patents.
14. **Cross-Skill Integration & Dialect Relations:** Clear pointers to related or opposing styles within the Coacus design corpus.

---

## 3. Showcase Integration Contract

Each canonical UI style in Coacus maintains a corresponding pure CSS file in the partner showcase (`estilos-visuais/styles/<slug>.css`) and an entry in `estilos-visuais/styles/registry.js`. When a style introduces motion effects, it must supply a modular FX engine (`estilos-visuais/styles/fx/<slug>.js`) complying with:
- Immediate early return when `matchMedia('(prefers-reduced-motion: reduce)').matches` is true.
- Standard lifecycle: `export default function mount(stage)` returning a cleanup closure `() => { ... }` that clears all timers, animation frames, event listeners, and injected DOM nodes.

Before merging changes that affect the partner showcase, apply the pre-deployment checks in [Rendered Interface Verification](../../knowledge/skills/engineering/practices/ui-design-craftsmanship/references/rendered-interface-verification.md): verify selectors against rendered nesting, measure spacing and control bounds at compact and wide viewports, and assert visible output from scroll effects. Once a deployed preview is available, run its published-asset freshness checks against the HTML and dynamically loaded assets.
