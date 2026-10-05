---
name: "ui-style-tactile-brutalism"
description: "Provides the tactile brutalism UI style (2020s, B2B and developer tools): hairline borders, exposed grids, mono labels, restrained palettes and mechanical precision, covering the engineered-minimalism token system, border-as-structure layering, crisp state feedback and contrast-safe hairlines. Use when designing precise, instrument-like interfaces for developer, infrastructure and enterprise products that want rawness without neo-brutalist loudness."
---

# UI Style: Tactile Brutalism (Engineered Minimalism)

Honest structure, shown at hairline weight: 1px rules, visible grids, mono metadata, near-monochrome palettes and mechanical, snap-quick feedback. It borrows brutalism's "show the construction" ethos and discards its shouting. "Tactile brutalism" is a practitioner label, not a formal movement: `unverified` as a canonical term. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Designing B2B, DevTools, infra, fintech-backoffice or data products that need an instrument-panel feel.
- Wanting visible structure and personality without gradients, glass or thick outlines.
- Building token systems where borders, not shadows, carry hierarchy.

---

## 🕰️ Definition and Timeline

- Roots: web brutalism (Pascal Deville's Brutalist Websites, 2014) and Swiss grid rigor; refined by developer-platform design systems such as Vercel's Geist (Geist Sans and Geist Mono, border-driven materials).
- Difference from [ui-style-neo-brutalism](../ui-style-neo-brutalism/SKILL.md): neo-brutalism uses 2-4px black borders, hard offset shadows and saturated flats; tactile brutalism uses 1px hairlines, no offset shadows, one accent. It differs from [ui-style-swiss-web-minimalism](../ui-style-swiss-web-minimalism/SKILL.md) by exposing the scaffolding (grid lines, crosshair marks, index numbers) as ornament.
- Distinct from [ui-style-web-brutalism](../ui-style-web-brutalism/SKILL.md): ordered and professional, not anti-design.

---

## 🎨 Visual DNA

- **Type:** one grotesk or neo-grotesk for text (Geist Sans, Inter, Söhne-like) plus a mono for labels, IDs, numbers, coordinates; small uppercase mono captions with tracking.
- **Color:** paper/ink neutrals with a stepped gray ramp; one signal accent; Geist-style scales assign steps by role (component backgrounds, borders, high-contrast fills, text).
- **Structure:** 1px borders (`0.5px` only on high-density displays, with a 1px fallback), visible column rules, dashed dividers, corner ticks, section indices (`01 / Overview`).
- **Shapes:** radius 0-4px; sharp or barely softened.
- **Depth:** none or flat; layering via border and background step, never blur.
- **Data:** tabular numerals, dense tables, status dots, sparklines at one stroke weight.

---

## 🖱️ Interaction and Motion

- State change is immediate: 80-150ms, `linear` or `steps`; border color and background step shift, no bounce.
- Hover darkens one ramp step; active inverts (ink background, paper text); focus is a 2px offset ring.
- Keyboard shortcuts shown inline as mono keycaps; cursor-aware crosshair or row highlight in tables.

---

## 🛠️ Implementation Notes

```css
:root {
  --paper: #fafaf9; --ink: #111110;
  --line: #c9c8c4;      /* hairline, >=3:1 vs paper where it marks a control */
  --line-strong: #8a8984;
  --accent: #0b5fff;
  --font-mono: "Geist Mono", ui-monospace, monospace;
}
.panel { border: 1px solid var(--line); background: var(--paper); }
.panel + .panel { border-top: 0; }
.label { font: 500 11px/1 var(--font-mono); letter-spacing: .08em; text-transform: uppercase; }
.btn { border: 1px solid var(--ink); background: transparent; transition: background .1s linear, color .1s linear; }
.btn:hover { background: color-mix(in srgb, var(--ink) 8%, transparent); }
.btn:active { background: var(--ink); color: var(--paper); }
.btn:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
td { font-variant-numeric: tabular-nums; }
```

- Avoid double borders: collapse adjacent panels. Use CSS grid with `gap: 1px` over a line-colored parent for lattice rules.

---

## ♿ Accessibility

- 1.4.11 Non-text Contrast (3:1): decorative hairlines may be faint, but borders that identify inputs and buttons must reach 3:1; pale `#e5e5e5` fields on white fail.
- 1.4.3 for tiny mono captions: 11px uppercase still needs 4.5:1; avoid gray-on-gray metadata.
- 1.4.12 text spacing and 1.4.4 resize: no fixed-height rows that clip when text scales.
- 2.5.8 target size (24px minimum): dense tables and keycap controls need padded hit areas.
- 2.4.7 and 2.4.11 focus visibility: ring must not be clipped by `overflow:hidden` panels.
- Respect `prefers-reduced-motion`; transitions are short but remove row-highlight animation when reduced.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** developer platforms, observability, API docs, internal admin, analytics, technical SaaS.
- **Caution:** consumer products wanting warmth; long-form reading (add generous leading).
- **Avoid:** playful kids/lifestyle brands, luxury editorial, anything needing emotional softness.

---

## ⚠️ Pitfalls

- Low-contrast hairlines that disappear on cheap displays and fail 1.4.11.
- Decorative grid lines and crosshairs becoming noise or screen-reader clutter (hide with `aria-hidden`).
- Sameness: every dev-tool site converging on mono caption plus gray ramp; the accent and copy voice must differ.
- Over-density: instrument feel is not license for 11px everywhere.

---

## 📚 Sources

- Vercel, "Geist Design System: Introduction" — https://vercel.com/geist/introduction
- Vercel, "Geist: Colors" (10 color scales; steps mapped to backgrounds, borders, text) — https://vercel.com/geist/colors
- Brutalist Websites, Pascal Deville, 2014 — https://brutalistwebsites.com/
- W3C, "Understanding SC 1.4.11: Non-text Contrast" (WCAG 2.2) — https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
- MDN, "font-variant-numeric" (Mozilla) — https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-numeric
- Style label and token values above are synthesis, not a single source: `unverified`.

---

## 🔗 Integration with Other Skills

- For conformance discipline, see [web-accessibility-wcag](../../../engineering/practices/web-accessibility-wcag/SKILL.md).
- Sibling styles: [ui-style-neo-brutalism](../ui-style-neo-brutalism/SKILL.md), [ui-style-web-brutalism](../ui-style-web-brutalism/SKILL.md), [ui-style-swiss-web-minimalism](../ui-style-swiss-web-minimalism/SKILL.md), [ui-style-linear-saas](../ui-style-linear-saas/SKILL.md), [ui-style-terminal-tui](../ui-style-terminal-tui/SKILL.md).
