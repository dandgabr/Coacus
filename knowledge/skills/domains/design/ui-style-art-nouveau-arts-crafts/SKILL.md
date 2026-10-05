---
name: "ui-style-art-nouveau-arts-crafts"
description: "Provides the Art Nouveau and Arts and Crafts revival UI style (c.1880s-1914 lineage, web revival 2020s): whiplash curves, botanical ornament, hand-lettered display type, muted earthy palettes and craft-honest surfaces, covering SVG path ornament, frames, type pairing, motion and WCAG contrast handling. Use when designing botanical, artisanal, heritage or tea-and-books brands that need ornamental warmth without looking like generic floral clip art."
---

# UI Style: Art Nouveau and Arts and Crafts

Two linked late-19th-century reforms translated to screens: Art Nouveau's sinuous plant-derived line and Arts and Crafts' honest, handmade pattern. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Brand sites for botanicals, tea, books, ceramics, textiles, boutique hotels, cultural venues.
- Posters, event pages and editorial covers that need decorative frames and illustrated headers.
- Requests for "Mucha", "William Morris pattern", "whiplash line" or "craft revival" looks.

---

## 🕰️ Definition and Timeline

- Arts and Crafts: emerged 1880s in Britain, flourished to about 1920; William Morris, Ruskin and Walter Crane argued for craftsmanship over machinery, truth to materials and unity of design and making.
- Art Nouveau: roughly 1883-1914, peak 1890-1910; Horta, Guimard, Mucha, Tiffany, Gallé, Lalique; zenith at the 1900 Paris Exposition Universelle. Goal: erase the line between fine and applied arts.
- Distinction from [ui-style-organic-biophilic](../ui-style-organic-biophilic/SKILL.md): that style borrows nature's calm textures and soft shapes; this one is historically specific ornament (whiplash curves, repeating botanical pattern, framed panels).
- Distinction from [ui-style-editorial-archive-luxury](../ui-style-editorial-archive-luxury/SKILL.md): luxury editorial is restrained; this style is deliberately ornamented.

---

## 🎨 Visual DNA

- **Line:** asymmetrical whiplash curves, stems and tendrils that flow into frames, borders and initials; line weight varies like a pen or woodblock.
- **Type:** hand-drawn or quirky display faces (Art Nouveau lettering) over a sturdy book serif for body; avoid pairing two decorative faces.
- **Color:** muted, earthy, dye-like: moss, indigo, madder red, ochre, cream paper (`#F3EAD7`), deep ink (`#1F2A24`); gold only as a thin accent.
- **Pattern:** Morris-style repeating botanicals with interlocking stems; one pattern per surface, kept low-contrast behind text.
- **Layout:** panels with ornate frames, vertical poster proportions, a figure or flower breaking the frame edge.
- **Materials:** paper grain, flat inked color, stained-glass segmentation lines (Tiffany) as dividers.

---

## 🖱️ Interaction and Motion

- Growth metaphor: vines draw on via SVG `stroke-dashoffset` on section entry, 600-900ms, ease-out; never loop.
- Hover on links: an ornament slides in or underline becomes a small curved flourish; keep 150-250ms.
- Scroll reveals limited to border and divider drawing; text stays static.

---

## 🛠️ Implementation Notes

```css
:root {
  --paper: #f3ead7; --ink: #1f2a24; --moss: #4a5d3a; --madder: #8c2f2b;
  --display: "Cormorant Garamond", Georgia, serif;
}
body { background: var(--paper) url("pattern.svg") repeat; color: var(--ink); }
.frame { border: 2px solid var(--ink); border-radius: 48% 48% 6px 6px / 20% 20% 6px 6px; padding: 2rem; background: var(--paper); }
.vine path { stroke-dasharray: 1; stroke-dashoffset: 1; animation: grow 800ms ease-out forwards; }
@keyframes grow { to { stroke-dashoffset: 0; } }
@media (prefers-reduced-motion: reduce) { .vine path { animation: none; stroke-dashoffset: 0; } }
```

- Ship ornaments as inline or referenced SVG with `pathLength="1"`; mark decorative SVG `aria-hidden="true"`.
- Put patterns on a layer behind a solid text panel rather than behind raw text.

---

## ♿ Accessibility

- Contrast: body text 4.5:1 and large text 3:1 (1.4.3); earthy mid-tones (ochre on cream) often fail, so test every pair; ornament that conveys meaning needs 3:1 (1.4.11).
- Decorative display lettering harms readability; keep it for headings only and keep real text in HTML (1.4.5, no images of text).
- Pattern backgrounds must not reduce text contrast (1.4.3) and must survive text spacing and 200% reflow (1.4.4, 1.4.10, 1.4.12).
- Honor `prefers-reduced-motion`: draw-on animations render in final state; no auto-playing loops (2.2.2, 2.3.3).
- Focus rings stay visible against ornament (2.4.7, 2.4.11 not obscured).

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** heritage and craft brands, publishers, museums, festivals, hospitality, editorial features.
- **Caution:** e-commerce (ornament on brand pages, plain product grids), long-form reading (limit pattern).
- **Avoid:** dense dashboards, data tools, emergency or financial flows where ornament competes with task clarity.

---

## ⚠️ Pitfalls

- Clip-art florals pasted on a flat template; no line-weight variation so the curves look vector-generic.
- Pattern noise under body copy; too many typefaces; ornament slowing page weight (optimize SVG).
- Treating the movement as pure aesthetics: its core claim was honesty of material and making, so avoid fake-handmade effects that hide a bland system.

---

## 📚 Sources

- Wikipedia contributors, "Art Nouveau" (Wikipedia), accessed 2026-10-05 — https://en.wikipedia.org/wiki/Art_Nouveau
- Wikipedia contributors, "Arts and Crafts movement" (Wikipedia), accessed 2026-10-05 — https://en.wikipedia.org/wiki/Arts_and_Crafts_movement
- W3C, "Web Content Accessibility Guidelines (WCAG) 2.2" (W3C Recommendation), 12 Dec 2024 — https://www.w3.org/TR/WCAG22/
- Victoria and Albert Museum, "Art Nouveau – an international style" (V&A), updated 25 Feb 2025 — https://www.vam.ac.uk/articles/art-nouveau-an-international-style (natural forms, fluid lines, asymmetry; Brussels, Paris and Munich as centers; Jugendstil, Stile Liberty and Tiffany style; Arts and Crafts influence).
- Specific claims about Mucha, Morris and Tiffany lettering conventions beyond the above remain `unverified`; the Metropolitan Museum essay returned HTTP 429 and is not cited.

---

## 🔗 Integration with Other Skills

- For conformance discipline, see [web-accessibility-wcag](../../../engineering/practices/web-accessibility-wcag/SKILL.md).
- Neighbors: [ui-style-organic-biophilic](../ui-style-organic-biophilic/SKILL.md), [ui-style-art-deco](../ui-style-art-deco/SKILL.md), [ui-style-editorial-archive-luxury](../ui-style-editorial-archive-luxury/SKILL.md), [ui-style-hand-drawn-sketch](../ui-style-hand-drawn-sketch/SKILL.md), [ui-style-bauhaus](../ui-style-bauhaus/SKILL.md).
- Related -punk styles: [ui-style-steampunk](../ui-style-steampunk/SKILL.md), [ui-style-solarpunk](../ui-style-solarpunk/SKILL.md).
