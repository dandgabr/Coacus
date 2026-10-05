---
name: "ui-style-broken-grid"
description: "Provides the broken grid / controlled asymmetry UI style (1980s print lineage, web 2010s-present): a visible underlying grid deliberately violated by overlap, offset and bleed, covering CSS Grid line-based overlap, layering, rhythm rules, reading-order safety and reflow. Use when designing editorial or portfolio layouts that need tension and movement without losing structure or accessibility."
---

# UI Style: Broken Grid

A layout approach that establishes a grid and then breaks it on purpose: images overlap text, headings bleed across columns, items sit off-axis. Tension comes from a legible system being violated in a few controlled places. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Editorial, portfolio, agency or campaign pages where uniform card grids feel generic.
- A layout needs overlap, offset and layering while staying responsive.
- Converting a print spread with overlapping elements into CSS.

---

## 🕰️ Definition and Timeline

- Post-war Swiss / International Typographic Style popularized rigorous grids through Josef Müller-Brockmann's *Grid Systems in Graphic Design*.
- By the 1980s designers reacted against dogmatic grids and their corporate association; personal computers enabled looser structures (Wikipedia, Grid (graphic design)).
- David Carson's work at Ray Gun (from about 1992, `unverified` exact year) is the canonical print example: layered photos and messy typography.
- Web: CSS Grid line-based placement lets items overlap by explicit placement, making the style systematic rather than hacked with negative margins.
- Distinct from [ui-style-swiss-web-minimalism](../ui-style-swiss-web-minimalism/SKILL.md), which obeys the grid; and from [ui-style-web-brutalism](../ui-style-web-brutalism/SKILL.md), where roughness is the point. Here the grid stays readable and breaks are rationed.

---

## 🎨 Visual DNA

- **Structure:** a 12-column (or custom) grid is the baseline; 2-4 elements per screen break it.
- **Overlap:** image over headline, headline over image, caption tucked under a crop.
- **Scale contrast:** oversized display type against small text; large empty fields next to dense clusters.
- **Offset and bleed:** items pushed half out of the container or off the viewport edge.
- **Rotation:** small angles (1-3 degrees) on a single accent element, not everywhere.
- **Color and type:** restrained palette so composition carries the energy.

---

## 🖱️ Interaction and Motion

- Subtle parallax or staggered reveal on offset elements (translate 16-40px, 300-600ms ease-out), once per element.
- Hover can nudge an overlapping layer forward (`z-index` swap or small translate), not rearrange layout.
- Under `prefers-reduced-motion: reduce`, drop parallax and reveals; layout remains static and intact.

---

## 🛠️ Implementation Notes

```css
.spread { display: grid; grid-template-columns: repeat(12, 1fr); column-gap: 1rem; }
.spread h1  { grid-column: 2 / span 8; grid-row: 1; z-index: 2; font-size: clamp(3rem, 9vw, 8rem); }
.spread .hero-img { grid-column: 6 / -1; grid-row: 1 / span 2; }          /* overlaps the heading */
.spread .note { grid-column: 1 / span 4; grid-row: 2; margin-top: -2rem; }  /* controlled offset */
@media (max-width: 40rem) {
  .spread { display: block; }
  .spread * { margin: 0 0 1rem; transform: none; }  /* collapse to one clean column */
}
```

- Overlap by explicit `grid-row`/`grid-column` placement, not absolute positioning, so the document flow survives.
- Write the DOM in reading order; reposition visually with grid only.
- Define the breaking rule in tokens (for example "one overlap per section") so the system stays consistent.
- Collapse to a single column at narrow widths; overlaps rarely survive mobile.

---

## ♿ Accessibility

- 1.3.2 Meaningful Sequence and 2.4.3 Focus Order: DOM order must match intended reading and tab order even when visual order differs.
- 1.4.3 Contrast (Minimum): text over images needs a measured plate, scrim or text-shadow-free solution; check the worst-case overlap pixel.
- 1.4.10 Reflow (320 CSS px) and 1.4.4 Resize Text: overlaps must not clip or hide text at 200% zoom.
- 1.4.12 Text Spacing: negative margins and fixed heights must not truncate content.
- 2.4.11 Focus Not Obscured (Minimum): overlapping layers must not cover focused controls; 2.5.8 Target Size (24px) for controls near edges.
- Motion honors `prefers-reduced-motion`.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** portfolios, magazines, fashion, event and campaign sites, case-study pages.
- **Caution:** e-commerce listings (product pages yes, comparison grids no), documentation landing pages.
- **Avoid:** forms, checkout, dashboards, data tables, any flow where scanning speed matters.

---

## ⚠️ Pitfalls

- Breaking everything: with no visible grid there is nothing to break.
- Overlap that hides text at certain viewport widths; test across breakpoints.
- Absolute positioning and negative margins that collapse flow and break zoom.
- Visual order diverging from DOM order, confusing screen readers and keyboard users.
- Looking accidental rather than intentional; sketch the grid and mark each deliberate break.

---

## 📚 Sources

- Wikipedia, "Grid (graphic design)" (Wikimedia) — https://en.wikipedia.org/wiki/Grid_(graphic_design)
- Wikipedia, "David Carson (graphic designer)" (Wikimedia) — https://en.wikipedia.org/wiki/David_Carson_(graphic_designer)
- MDN Web Docs, "Grid layout using line-based placement" (Mozilla) — https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout/Grid_layout_using_line-based_placement
- MDN Web Docs, "Layout using named grid lines" (Mozilla) — https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout/Grid_layout_using_named_grid_lines
- MDN Web Docs, "prefers-reduced-motion" (Mozilla) — https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
- W3C, "Web Content Accessibility Guidelines (WCAG) 2.2", Recommendation 12 Dec 2024 — https://www.w3.org/TR/WCAG22/

---

## 🔗 Integration with Other Skills

- For conformance discipline, see [web-accessibility-wcag](../../../engineering/practices/web-accessibility-wcag/SKILL.md).
- Sibling styles: [ui-style-swiss-web-minimalism](../ui-style-swiss-web-minimalism/SKILL.md), [ui-style-editorial-archive-luxury](../ui-style-editorial-archive-luxury/SKILL.md), [ui-style-collage-scrapbook](../ui-style-collage-scrapbook/SKILL.md), [ui-style-bento-grid](../ui-style-bento-grid/SKILL.md), [ui-style-expressive-variable-typography](../ui-style-expressive-variable-typography/SKILL.md).
