---
name: "ui-style-de-stijl"
description: "Provides the De Stijl / Neoplasticism UI style (1917-1931 lineage, revived for the web): orthogonal black grid lines, flat primary-color planes on white and asymmetric balance, covering Mondrian's neoplastic rules, the 1923 diagonal schism, grid-as-composition CSS, and differences from Bauhaus and Swiss style. Use when designing rigorous grid-based compositions, color-block layouts, portfolios or editorial pages that treat the layout itself as the artwork."
---

# UI Style: De Stijl (Neoplasticism)

Radical reduction: only horizontal and vertical lines, flat rectangles of red, yellow and blue plus black, white and gray, balanced asymmetrically. Where Bauhaus is a school and Swiss style a typographic system, De Stijl is a compositional doctrine: the grid is the image. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Designing color-block layouts, card grids and hero compositions where division of space is the visual idea.
- Building portfolio, gallery, editorial or brand pages that cite Mondrian, Rietveld or van Doesburg.
- Needing a strictly orthogonal system with a tiny token set.

---

## 🕰️ Definition and Timeline

- 1917: Piet Mondrian and Theo van Doesburg found De Stijl (Dutch for "style") as a publication; van Doesburg ran it until 1931. Members included Bart van der Leck, Georges Vantongerloo, J.J.P. Oud and Gerrit Rietveld (Rietveld joined in 1918).
- Mondrian's term Neoplasticism (Nieuwe Beelding) describes purified abstraction: straight lines, primary colors, asymmetric balance achieved by proportion, not symmetry.
- 1923 schism: Mondrian withdrew after van Doesburg introduced diagonals (Elementarism).
- Architecture and design: Rietveld Schroder House (1924, Utrecht; UNESCO 2000); Red and Blue Chair (designed 1917, colored after 1919 per Wikipedia).
- **Differences:** [ui-style-bauhaus](../ui-style-bauhaus/SKILL.md) allows circles, triangles, diagonals, photomontage and craft; De Stijl forbids them in its orthodox form and is a collective doctrine, not an institution. [ui-style-swiss-web-minimalism](../ui-style-swiss-web-minimalism/SKILL.md) organizes text on a modular grid with neutral color; De Stijl organizes color planes and lines, text is secondary.

---

## 🎨 Visual DNA

- **Palette:** red `#C8102E`-ish, yellow `#F7D117`-ish, blue `#0B3D91`-ish, plus white (dominant, often most of the area), black and light gray. Flat fills, no gradients, no tints beyond gray.
- **Lines:** thick black rules (4-10px) running edge to edge, never touching a curve; some planes stop short of the border.
- **Proportion:** unequal rectangles; large white fields balance small intense color planes; color use is sparse, not equal.
- **Type:** blocky geometric or constructed sans, uppercase allowed; an orthodox variant uses letterforms built from rectangles (van Doesburg-style). Text sits in white cells.
- **Depth:** none; hierarchy comes from size, color weight and position.

---

## 🖱️ Interaction and Motion

- Instant or very short (100-200ms) fills; hover flips a white cell to a primary, or expands a cell by redistributing grid tracks.
- Transitions animate `grid-template-columns` or `flex-grow`, so the composition rebalances; strictly linear, orthogonal movement, no rotation.
- Keep one asymmetric balance at every state: if one cell grows, another shrinks.

---

## 🛠️ Implementation Notes

```css
:root { --white: #fafafa; --black: #111; --red: #c8102e; --yellow: #f7d117; --blue: #0b3d91; --rule: 6px; }
.composition {
  display: grid; gap: var(--rule); background: var(--black);
  grid-template-columns: 2fr 5fr 3fr; grid-template-rows: 3fr 2fr 4fr;
}
.composition > * { background: var(--white); padding: 1rem; }
.cell--red { background: var(--red); } .cell--blue { background: var(--blue); color: #fff; }
.cell--yellow { background: var(--yellow); }
.cell { transition: background .15s linear; }
.cell:hover { background: var(--yellow); }
.cell:focus-visible { outline: 4px solid var(--black); outline-offset: -8px; }
@media (prefers-reduced-motion: reduce) { .cell { transition: none; } }
```

- The black `gap` trick yields the rules for free; spans (`grid-column: span 2`) create the neoplastic proportions.
- Collapse to a single column on narrow screens, keeping one color accent per row.

---

## ♿ Accessibility

- Yellow with white text fails 1.4.3; red/blue pairs on each other fail; use black on yellow, white on blue and test white on red.
- Black grid rules are non-text contrast anchors (1.4.11); do not remove them in the name of "airiness".
- Color planes must not carry meaning alone (1.4.1); label cells and keep logical DOM order despite asymmetric spans (1.3.2).
- Reflow at 320px (1.4.10); never rely on fixed-height cells for text (1.4.4, 1.4.12); target size at least 24px (2.5.8); respect `prefers-reduced-motion`.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** portfolios, art and architecture sites, editorial front pages, dashboards with a few sections, brand microsites, 404 or splash pages.
- **Caution:** content-heavy apps (keep the grid as a frame, not a constraint on text).
- **Avoid:** organic, warm or handcrafted brand voices; contexts needing many semantic colors (status palettes conflict with a three-color doctrine).

---

## ⚠️ Pitfalls

- "Mondrian wallpaper": copying the famous composition without a grid system behind it.
- Using all three primaries in equal amounts; the doctrine depends on white dominance.
- Adding rounded corners, shadows or gradients and still calling it De Stijl.
- Hover effects that break asymmetric balance or cause layout shift.

---

## 📚 Sources

- Wikipedia, "De Stijl" (Wikimedia Foundation), accessed 2026 — https://en.wikipedia.org/wiki/De_Stijl
- Tate, "De Stijl" (Tate), accessed 2026 — https://www.tate.org.uk/art/art-terms/d/de-stijl
- Wikipedia, "Neoplasticism" (Wikimedia Foundation), accessed 2026 — https://en.wikipedia.org/wiki/Neoplasticism
- Wikipedia, "Gerrit Rietveld" (Wikimedia Foundation), accessed 2026 — https://en.wikipedia.org/wiki/Gerrit_Rietveld
- W3C, "Web Content Accessibility Guidelines (WCAG) 2.2" (W3C), 2023 — https://www.w3.org/TR/WCAG22/
- Hex values and the grid-track implementation are practice suggestions: `unverified` as canonical.

---

## 🔗 Integration with Other Skills

- For conformance discipline, see [web-accessibility-wcag](../../../engineering/practices/web-accessibility-wcag/SKILL.md).
- Sibling styles: [ui-style-bauhaus](../ui-style-bauhaus/SKILL.md), [ui-style-swiss-web-minimalism](../ui-style-swiss-web-minimalism/SKILL.md), [ui-style-bento-grid](../ui-style-bento-grid/SKILL.md), [ui-style-flat-design](../ui-style-flat-design/SKILL.md), [ui-style-metro-modern-ui](../ui-style-metro-modern-ui/SKILL.md).
