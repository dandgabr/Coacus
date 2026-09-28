---
name: "ui-designer"
description: "Provides the UI design discipline craft (interface/visual design separated from UX): visual hierarchy and composition, 8pt spacing systems, type scales and legibility, semantic color tokens, component state design, design tokens (DTCG), dark mode and touch-target standards, art-direction-to-handoff process and UI evaluation checklists. Use when designing high-fidelity interfaces, building design systems, or reviewing visual craft."
---

# AI Skill: UI Design (Interface Craft)

The UI discipline: the surface craft — hierarchy, typography, color, layout, components, motion specs — that translates UX decisions into interfaces users find easy to use and pleasurable. Distinct from UX (see [ux-designer](../ux-designer/SKILL.md)): Don Norman & Jakob Nielsen explicitly instruct teams to distinguish the total user experience from the user interface. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Designing high-fidelity screens, components or design systems.
- Reviewing visual craft (hierarchy, spacing, type, color, states).
- Preparing design-to-development handoff (tokens, specs, assets).

---

## 🧭 Discipline Boundaries

- **UI owns the surface:** "the process designers use to build interfaces… focusing on looks or style" across GUI, voice (VUI) and gesture interfaces (IxDF). Deliverables: hi-fi designs, interactive prototypes, design systems/components, visual style guides, responsive layouts, dev specs and assets (IxDF roles guide; Figma).
- **UX owns the experience:** research, IA, flows, wireframes, usability findings (see ux-designer). The canonical handoff: UX wireframes → UI high-fidelity craft → dev-ready specs, iterating continuously.
- Shared: prototyping, design systems, user-centered validation. Figma's framing: UI is "a specialized subset of UX" — but the crafts, tools and deliverables are distinct.

---

## 🎨 Visual Design Fundamentals

- **Visual hierarchy** (NN/g): organize elements so the eye consumes them in intended-importance order. Levers: color/contrast (value and saturation against context — not hue alone), scale (bigger = more important), grouping (proximity, common region). Rules of thumb: ~2 primary + 2 secondary colors; ≤3 contrast variations ("if everything is contrasted, nothing stands out"); ≤3 type sizes (body 14–16px, subheader 18–22px, header up to 32px); ≤2 large elements per layout. Verify with the squint/blur test.
- **Spacing:** the 8-point grid — dimensions, padding and margin in multiples of 8 (Material's 4/8pt base); hard grid (snap to visible grid) or soft grid (8pt increments between elements); pair with a 4pt baseline grid for text; work at @1x.
- **Typography:** type scale with named roles (Material 3: display/headline/title/body/label × large/medium/small = 15 styles); line spacing 120–145% of point size (unitless `line-height`); measure 45–90 characters per line (Practical UI prescribes 40–80); clean typefaces — stylized faces reduce legibility (NN/g).
- **Color systems:** build shades up front (HSL); semantic color roles mapped for emphasis and container relationships (Material 3: 26 color roles generating light/dark schemes); tokens as "the single source of truth to name and store decisions about the user interface" (Atlassian); OKLCH for wide-gamut palettes (Tailwind v4 default). The 60-30-10 rule is practitioner folklore [unverified as a standard].
- **Elevation/depth:** emulate a light source; two-part shadows; overlap for layers; in dark themes replace shadow-as-elevation with lighter surface overlays (shadows lack contrast on dark).

---

## 🧩 Component and State Craft

- Design **every state** per component: default, hover, focus, active/pressed, disabled, loading, error — plus ARIA semantics (tri-state checkbox, pressed buttons per the ARIA APG patterns).
- **Focus is non-negotiable:** WCAG 2.2 requires visible focus (2.4.7); disabled controls are contrast-exempt but must read as inactive.
- **Design tokens:** the W3C DTCG format (current release 2025.10) — name/value pairs with `$type`, aliases, composite tokens (typography, shadow, border, transition); translation via Style Dictionary-class tooling. Tokens are how dark mode scales: one role set, two schemes.
- **Dark mode:** dark gray over pure black; desaturate brand accents (avoid "visual vibration"); ~3 grays for text hierarchy; elevation as lightness (Material 3).
- **Touch targets:** 24×24 CSS px minimum (WCAG 2.2 AA, 2.5.8), 44×44 (AAA / Apple HIG), 48dp Android with 8dp spacing — design at 44–48px with ≥8px separation.
- **Motion specs:** duration tiers (Material 3: 75/150/200/250/300/350ms) and easing families (standard `cubic-bezier(0.4, 0, 0.2, 1)`, emphasized, decelerate, accelerate); Doherty Threshold (<400ms response) as the responsiveness budget.

---

## 🔄 Process: Art Direction → Handoff

1. **Art direction:** mood boards (colors, textures, imagery, type treatments, UI components) to set visual direction and lower revision cost; Refactoring UI's "choose a personality" (fonts/color/shape language per brand personality).
2. **Wireframe → hi-fi:** transform UX wireframes/prototypes into refined, high-fidelity designs (IxDF task list).
3. **Handoff as tokens + components, not redlines:** specs derive from the file (Dev Mode/inspect-class tooling); Code Connect and MCP servers feed design specs into coding assistants — prerequisite: a design system organized enough for tooling to reference (Figma, 2026).
4. **Stay through the build:** review what ships against what was designed; launch-phase drift is a named failure mode.

---

## ✅ UI Evaluation Checklist

- Visual consistency review against foundations (tokens, color, type, spacing, grid, iconography, elevation — the Atlassian foundations taxonomy doubles as the audit dimensions).
- Hierarchy verification (squint test, including content-driven hierarchy accidents).
- Contrast and legibility: 4.5:1 normal / 3:1 large text (WCAG 1.4.3); non-text elements 3:1 (1.4.11); legibility checklist — adequate default size, high contrast on plain background, clean typeface (NN/g).
- Touch-target and motor checks (24/44/48px + spacing circles for undersized targets).
- Component state coverage vs the ARIA APG pattern definitions; component API sanity (role-based token naming over raw hex).
- Copy legibility: plain words, short sentences, scannable structure (users read ~28% of page words — NN/g).

---

## ⚠️ Pitfalls

- Designing the interface as if it were the whole experience — UI ⊂ UX; a perfect surface cannot fix a broken flow.
- Hue-only hierarchy (fails color-blind users); more than three contrast levels; skipping focus/disabled/error states.
- Redline-era handoff (static pixel specs) instead of token-driven, tool-consumable systems.
- Treating automation as a substitute for documenting design intent.

---

## 📚 Sources

- Don Norman & Jakob Nielsen, "The Definition of User Experience (UX)", NN/g, 1998 — https://www.nngroup.com/articles/definition-user-experience/
- IxDF, "What is User Interface (UI) Design?", updated 2026 — https://www.interaction-design.org/literature/topics/ui-design
- Figma, "What is Product Design", 2026 — https://www.figma.com/resource-library/what-is-product-design/
- Kelley Gordon, "Visual Hierarchy in UX: Definition", NN/g, Jan 2021 — https://www.nngroup.com/articles/visual-hierarchy-ux-definition/
- Jakob Nielsen, "Legibility, Readability, and Comprehension", NN/g, 2015 — https://www.nngroup.com/articles/legibility-readability-comprehension/
- "The 8-Point Grid", Spec — https://spec.fm/specifics/8-pt-grid
- Adam Wathan & Steve Schoger, *Refactoring UI*, 2018 — https://www.refactoringui.com/
- Adham Dannaway, *Practical UI* — https://www.practical-ui.com/
- Jon Yablonski, *Laws of UX* — https://lawsofux.com/
- W3C DTCG, "Design Tokens Format Module 2025.10" — https://www.designtokens.org/TR/2025.10/format/
- W3C WAI, "Understanding SC 2.5.8 Target Size (Minimum)", WCAG 2.2 — https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
- Google, "Touch target size", Android Accessibility Help — https://support.google.com/accessibility/android/answer/7101858
- Material 3 guidelines — https://m3.material.io/
- Atlassian Design System, "Foundations" — https://atlassian.design/foundations
- W3C WAI, "ARIA Authoring Practices Guide — Patterns" — https://www.w3.org/WAI/ARIA/apg/patterns/
- Adam Wathan, "Tailwind CSS v4.0", Jan 2025 — https://tailwindcss.com/blog/tailwindcss-v4
- Matthew Butterick, *Practical Typography* — https://practicaltypography.com/

---

## 🔗 Integration with Other Skills

- For the experience discipline this craft serves, see [ux-designer](../ux-designer/SKILL.md).
- For the orchestrating generalist role, see [ui-ux-designer](../ui-ux-designer/SKILL.md).
- For the style vocabulary, see the [design style library](../../domains/design/ui-style-glassmorphism/SKILL.md) (30 `ui-style-*` skills).
- For accessibility conformance, see [web-accessibility-wcag](../../engineering/practices/web-accessibility-wcag/SKILL.md).
