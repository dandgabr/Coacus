---
name: "ui-style-collage-scrapbook"
description: "Provides the collage / scrapbook UI style (art lineage 1912-present, web revival 2010s-present): cut-out photos, torn paper edges, tape, stickers and layered mixed media, covering photomontage history, clip-path cut-outs, drop-shadow layering, rotation rules and reading-order safety. Use when designing expressive, personal, mixed-media surfaces such as portfolios, zines, music and culture sites."
---

# UI Style: Collage and Scrapbook

Interfaces assembled from cut, pasted and overlapped fragments: photo cut-outs, torn paper, tape, stamps, stickers and handwritten notes. Meaning comes from juxtaposition, and the surface reads as handmade and personal. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Portfolios, culture, music, fashion and event sites that want a handmade, mixed-media voice.
- Landing pages built around cut-out imagery and sticker-like accents.
- Translating physical scrapbook, zine or photomontage material to the screen.

---

## 🕰️ Definition and Timeline

- 1912: Braque and Picasso introduce papier collé; Picasso's *Still Life with Chair Caning* pastes oilcloth onto canvas (Wikipedia, Collage).
- 1916-1919: Heartfield and Grosz claim to have invented photomontage in 1916; Hannah Höch's 1919 Dada work is the canonical example; Heartfield later made 240 anti-Nazi photomontages for AIZ (1930-1938).
- Web revival follows the cut-and-paste aesthetic of 2010s editorial and music design (`unverified` for specific sites).
- Distinct from [ui-style-maximalism](../ui-style-maximalism/SKILL.md): collage is about physical cut-out layering and visible edges, not abundance in general. Distinct from [ui-style-hand-drawn-sketch](../ui-style-hand-drawn-sketch/SKILL.md): mixed media, not a single pen voice. Closer to [ui-style-risograph-zine](../ui-style-risograph-zine/SKILL.md) in spirit but without the print-process constraint.

---

## 🎨 Visual DNA

- **Cut-outs:** subjects isolated from photos with rough, white-bordered or torn edges.
- **Layering:** overlap with stacked shadows; paper stock variety (newsprint, kraft, graph paper, tape).
- **Rotation:** each fragment tilted -6 to +6 degrees; no two the same.
- **Color:** limited base (paper tones) with spot colors; halftone or duotone photos for unity.
- **Type:** mix of cut-out letters, typewriter, and marker; keep one readable body face.
- **Ornament:** tape strips, paper clips, stamps, stars, scribbled arrows.

---

## 🖱️ Interaction and Motion

- Hover lifts a piece (translate -4px, scale 1.02, shadow deepens) and straightens the rotation slightly; 150-250ms.
- Optional drag-to-rearrange for playful boards; always offer a non-drag alternative.
- Stop-motion feel: step-timed entrance at 6-12 fps for a few hero items only.
- Under `prefers-reduced-motion: reduce`, remove drift, stop-motion and parallax; keep static compositions.

---

## 🛠️ Implementation Notes

```css
.scrap {
  background: #f4efe4; padding: .75rem; transform: rotate(var(--tilt, -2deg));
  filter: drop-shadow(2px 4px 0 rgb(0 0 0 / .25));
}
.torn {
  clip-path: polygon(0 3%, 6% 0, 14% 4%, 25% 1%, 40% 4%, 60% 0, 78% 3%, 92% 0, 100% 3%,
                     100% 97%, 92% 100%, 75% 96%, 55% 100%, 35% 97%, 15% 100%, 0 96%);
}
.scrap:hover, .scrap:focus-visible { transform: rotate(0) translateY(-4px); }
.scrap img { mix-blend-mode: multiply; }
@media (prefers-reduced-motion: reduce) { .scrap { transition: none; } }
```

- Use `filter: drop-shadow()` rather than `box-shadow` so shadows follow the clipped (alpha) shape.
- `clip-path: polygon()` gives torn edges; keep focus outlines on an unclipped wrapper, since clipping can cut them.
- Cut out subjects ahead of time as transparent WebP/PNG; avoid runtime masking of large photos.
- Lay out with CSS Grid placement or a few absolutely positioned decorative layers; keep content in DOM reading order.

---

## ♿ Accessibility

- 1.4.3 Contrast (Minimum) and 1.4.11 Non-text Contrast: text on patterned paper needs a flat plate; check each overlap area.
- 1.3.2 Meaningful Sequence and 2.4.3 Focus Order: visual shuffling must not reorder content semantically.
- 2.4.7 Focus Visible and 2.4.11 Focus Not Obscured: clipped or overlapped pieces must keep a visible, unobscured focus indicator.
- 1.4.10 Reflow and 1.4.4 Resize Text: rotated blocks must not clip text at 200% zoom or 320px width.
- Decorative tape, stickers and stamps: empty `alt` or `aria-hidden`; informative cut-outs get real alternatives.
- Honor `prefers-reduced-motion`; avoid drag as the only interaction (2.5.7 Dragging Movements).

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** portfolios, music and culture sites, editorial features, campaigns, personal blogs.
- **Caution:** commerce (brand shell yes, product detail no), long text pages.
- **Avoid:** forms, dashboards, regulated or trust-critical flows; anywhere clutter harms task completion.

---

## ⚠️ Pitfalls

- Everything rotated and shadowed equally: hierarchy disappears.
- Heavy raster cut-outs bloat page weight; compress and size responsively.
- Clipped edges cut off focus rings and text on zoom.
- Digital "tape and stickers" clichés read as template; vary materials and source imagery.
- Copyright: cut-out imagery needs cleared sources.

---

## 📚 Sources

- Wikipedia, "Collage" (Wikimedia) — https://en.wikipedia.org/wiki/Collage
- Wikipedia, "Photomontage" (Wikimedia) — https://en.wikipedia.org/wiki/Photomontage
- MDN Web Docs, "clip-path" (Mozilla) — https://developer.mozilla.org/en-US/docs/Web/CSS/clip-path
- MDN Web Docs, "drop-shadow()" (Mozilla) — https://developer.mozilla.org/en-US/docs/Web/CSS/filter-function/drop-shadow
- MDN Web Docs, "mix-blend-mode" (Mozilla) — https://developer.mozilla.org/en-US/docs/Web/CSS/mix-blend-mode
- W3C, "Web Content Accessibility Guidelines (WCAG) 2.2", Recommendation 12 Dec 2024 — https://www.w3.org/TR/WCAG22/

---

## 🔗 Integration with Other Skills

- For conformance discipline, see [web-accessibility-wcag](../../../engineering/practices/web-accessibility-wcag/SKILL.md).
- Sibling styles: [ui-style-risograph-zine](../ui-style-risograph-zine/SKILL.md), [ui-style-hand-drawn-sketch](../ui-style-hand-drawn-sketch/SKILL.md), [ui-style-broken-grid](../ui-style-broken-grid/SKILL.md), [ui-style-maximalism](../ui-style-maximalism/SKILL.md), [ui-style-grain-noise-texture](../ui-style-grain-noise-texture/SKILL.md).
