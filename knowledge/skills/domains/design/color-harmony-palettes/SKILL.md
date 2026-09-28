---
name: "color-harmony-palettes"
description: "Provides color harmony and palette construction based on color-wheel history and modern practice: Newton/Goethe/Itten/Albers lineage, harmony schemes (monochromatic, analogous, complementary, split-complementary, triadic, tetradic, square), shade-ramp engineering (50-950 scales, tints/tones/shades, neutral casts), 60-30-10 as heuristic, palette tools and the honest evidence base of color psychology and brand color strategy. Use when building palettes, choosing harmony schemes or briefing brand color."
---

# AI Skill: Color Harmony and Palettes

How hue relationships work, how to build a real UI palette (ramps, neutrals, semantics), and what color psychology honestly supports. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Building a palette from a brand color or moodboard.
- Choosing a harmony scheme for a surface or campaign.
- Engineering shade ramps and neutral scales.
- Briefing brand color or color-psychology claims.

---

## 🎡 Color-Wheel Lineage (get the history right)

- **Newton, *Opticks* (1704):** first color circle, built on unequal Dorian-scale intervals and spectral hues only, as a *mixing calculator* — the prism experiments were 1666, the circle published 1704 (do not conflate).
- **Goethe, *Theory of Colours* (1810):** perception-first; a symmetric six-color wheel of reciprocally evoked pairs (yellow↔violet, orange↔blue, green↔purple), anticipating opponent-process theory; Eastlake's 1840 English translation censored the anti-Newton polemic.
- **Itten (Bauhaus, 1919–22):** the 12-hue Farbkreis (1961) and the seven contrasts — hue, value, temperature, complements, simultaneous, saturation, extension.
- **Albers, *Interaction of Color* (Yale, 1963):** color is the most relative medium; simultaneous-contrast exercises (make one color look like two) remain the core training.
- **UI consequence:** design tools use the additive RGB/OKLCH wheel, not the artist's RYB wheel — "opposites" differ (RGB: red↔cyan, green↔magenta, blue↔yellow).

---

## 🎨 Harmony Schemes

- **Monochromatic:** one hue, varied by tint/shade/tone — simplest, non-distracting; no hue channel left for encoding.
- **Analogous:** ~3 adjacent hues (~30° steps) — low tension; good for ambient surfaces and gradients.
- **Complementary:** ~180° apart — maximum vibrancy; standard for action + accent, but tune saturation/lightness instead of using raw complements at scale.
- **Split-complementary:** base + the two neighbors of its complement (complement ±30°) — keeps contrast, softens vibration; the safer default.
- **Triadic:** three hues at 120° — vibrant as a scheme; works for categorical data and playful brands; keep one hue dominant.
- **Tetradic (rectangle) / Square:** two complementary pairs / four hues at 90° — richest and hardest to balance; one color must dominate warm-vs-cool.
- **Cross-cutting rules:** pick one dominant color; temperature should match the message (warm = energy, cool = calm); never encode meaning in hue alone.

---

## 🪜 Palette Construction

- **What a UI palette contains** (Refactoring UI): **greys** dominate (8–10 shades: text, backgrounds, panels — start from near-black, not black); **one primary** (maybe two) with 5–10 shades for hover/active/text roles; **accents** for semantics and highlights, 5–10 shades each.
- **Define shades up front** — do not call `lighten()`/`darken()` ad hoc (that is how you get 35 near-identical blues). Anchor the ramp: base (button background), darkest (text), lightest (tint background), then bisect to fill (100–500–900 → 300/700 → 200/400/600/800).
- **Tint = hue + white; shade = hue + black; tone = hue + grey.** Bootstrap 5.3 documents the `mix()` mechanics; `lighten()`/`darken()` only move lightness — different behavior.
- **Perceptual ramps:** fix hue, step lightness in OKLCH/Oklab, and nudge chroma as lightness rises (per-hue gamut ceilings are physics). Tailwind v4 publishes its 50–950 ramps in `oklch()`; Radix's 12 steps are a usage contract (step 9 = purest solid, steps 11–12 = text guarantees).
- **Neutral scales carry deliberate casts:** Tailwind's slate (blue, ~258°), zinc (~286°), stone (warm) vs neutral (0 chroma) — pick a cast that harmonizes with the brand.
- **60-30-10** (60% dominant, 30% secondary, 10% accent) is a ubiquitous interior-design heuristic with **untraceable origin** — present it as a rule of thumb, not a citable principle.
- **Status colors are framework convention** (Bootstrap/Material/Tailwind): success=green, danger=red, warning=amber, info=blue; each needs foreground/background/border variants and light/dark subtle/emphasis forms. Deviating has real usability cost.

---

## 🧠 Color Psychology — the Honest Evidence

- **What research supports:** color can carry meaning and affect affect/cognition/behavior, especially in achievement and affiliation contexts (Elliot & Maier, *Annual Review of Psychology*, 2014) — but the authors state the literature "remains at a nascent stage" and that application recommendations are premature. Color-in-context theory: the *same* hue has different effects in different contexts.
- **Cross-cultural variation is quantified:** Jonauskaite et al. (*Royal Society Open Science*, 2019) show color–emotion associations are partially shared and partially culture-specific.
- **One influential study, not a law:** Mehta & Zhu (*Science*, 2009) — red boosts detail-oriented tasks, blue boosts creativity; cite with the boundary-condition caveat.
- **Folklore to flag, never assert:** "color increases brand recognition by 80%" (attributed to an untraceable "University of Loyola, Maryland study"), "60% of decisions are color-based", and deterministic single-hue personality mappings. Same for cultural meanings as absolutes: red = prosperity in China but mourning in South Africa; white is funerary in parts of East Asia; verify against the target market with research.

---

## 🏷️ Brand Color Strategy

- The brand hue is a small fraction of UI pixels; recognition comes from the *consistent pairing* of hue with brand, not the amount used. Structure: primary (+ maybe secondary), accents, status roles.
- Industry norms are observations, not laws (blue for Western finance, green for health) — out-of-category hues can buy distinctiveness at a risk you take knowingly.
- Rebrand risk: changing a recognition-bearing hue forfeits accumulated association; migrate secondary surfaces first and never reassign semantic status colors mid-flight. Color trademarks exist; mention qualitatively.

---

## 🛠️ Tools

- **Adobe Color / Coolors:** wheel-based scheme generation, image palette extraction, contrast checking (Coolors also previews palettes on real UI).
- **Material Theme Builder + material-color-utilities:** HCT tonal palettes, dynamic schemes from a seed or image, contrast utilities (the official M3 path).
- **Framework ramps as starting systems:** Tailwind v4 (22+ hues × 50–950, OKLCH, CSS-variable theming) and Bootstrap 5.3 (tint/shade + semantic theme map) are defaults to override, not just utilities.

---

## ⚠️ Pitfalls

- Generating palette shades at runtime instead of defining them; hue-only data encoding; raw complements at full saturation.
- Repeating untraceable psychology statistics in client work.
- Assuming one culture's color meanings are universal.

---

## 📚 Sources

- IxDF, "What is Color Theory?", updated 2026 — https://www.interaction-design.org/literature/topics/color-theory
- Wikipedia, "Color wheel" — https://en.wikipedia.org/wiki/Color_wheel
- Isaac Newton, *Opticks*, 1704 — https://www.gutenberg.org/files/33504/33504-h/33504-h.htm
- Wikipedia, "Theory of Colours" (Goethe, 1810) — https://en.wikipedia.org/wiki/Theory_of_Colours
- Wikipedia, "Johannes Itten" — https://en.wikipedia.org/wiki/Johannes_Itten
- Wikipedia, "Josef Albers" — https://en.wikipedia.org/wiki/Josef_Albers
- Elliot & Maier, "Color Psychology", *Annual Review of Psychology*, 2014 — https://doi.org/10.1146/annurev-psych-010213-115035
- Mehta & Zhu, "Blue or Red?", *Science*, 2009 — https://doi.org/10.1126/science.1169144
- Jonauskaite et al., *Royal Society Open Science*, 2019 — https://doi.org/10.1098/rsos.190741
- Refactoring UI, "Building Your Color Palette" — https://www.refactoringui.com/previews/building-your-color-palette
- Bootstrap v5.3, "Color" — https://getbootstrap.com/docs/5.3/customize/color/
- Tailwind CSS v4, "Colors" — https://tailwindcss.com/docs/customizing-colors
- Jill Morton (Colorcom), "Color & Branding" (origin of the 80% claim), 2012 — https://www.colormatters.com/color-and-marketing/color-and-branding
- Material Foundation, "Material Color Utilities" — https://github.com/material-foundation/material-color-utilities

---

## 🔗 Integration with Other Skills

- For the science under the wheel, see [color-theory-foundations](../color-theory-foundations/SKILL.md).
- For ramp contrast guarantees, see [color-contrast-accessibility](../color-contrast-accessibility/SKILL.md).
- For tokens and theming, see [color-ui-systems](../color-ui-systems/SKILL.md).
