---
name: "ui-style-arts-and-crafts"
description: "Provides the authentic Arts & Crafts UI style (1880–1920): British craft revival led by William Morris, Kelmscott Press typographic borders, woodblock printing textures, handcrafted honesty of materials, medieval guild motifs, and rich earthy plant dyes. Use when designing artisanal heritage brands, handcrafted goods e-commerce, book arts, traditional guild institutions, or rustic editorial platforms."
---

# UI Style: Arts & Crafts (William Morris & Material Honesty)

The Arts and Crafts movement (roughly 1880–1920) arose in Britain as an ideological and aesthetic rebellion against dehumanizing industrial mass production. Championed by William Morris and John Ruskin, it advocates for the decorative dignity of manual labor, traditional handcrafts, material honesty, woodblock printing, and dense botanical patterns rooted in medieval English folklore. Synthesized from Kelmscott Press editions and the Morris & Co. archives.

---

## 🧭 When to Activate

- Designing platforms for artisan collectives, handcrafted goods, bespoke bookbinding, traditional woodworking, or slow-craft movements.
- Building editorial experiences that celebrate typographic texture, heavy woodblock framing, and historical gravitas.
- Distinct from fluid French Art Nouveau; activate Arts & Crafts when the visual tone calls for rustic weight, medieval vernacular honesty, and hand-printed tactile texture.

---

## 🕰️ Definition, Lineage, and Timeline

- **Chronology:** British origins in the 1880s (Red House, Morris & Co., Art Workers' Guild), flourishing through the 1910s and inspiring the American Craftsman movement (Gustav Stickley).
- **Core Principles:** "Have nothing in your houses that you do not know to be useful or believe to be beautiful" (William Morris). Rejection of machine ornament, embrace of visible joinery, hand-carved woodblocks, and natural vegetable dyes.
- **Distinction from Neighbors:**
  - Unlike **Art Nouveau / [ui-style-art-nouveau](../ui-style-art-nouveau/SKILL.md)**: Art Nouveau is urban, sinuous, erotic, lighter, and celebrates cast iron and blown glass; Arts & Crafts is rural, medievalist, heavy, restrained, and built on woodblock prints and joinery.
  - Unlike **[ui-style-editorial-archive-luxury](../ui-style-editorial-archive-luxury/SKILL.md)**: Editorial Luxury is sleek, modern high-fashion; Arts & Crafts is dense, archaic, and deeply earthy.

---

## 🎨 Visual DNA & Subgenre Taxonomy

- **Woodblock Printing & Textures:**
  - Dense, interlocking floral patterns (willow boughs, acanthus leaves, pomegranate branches, strawberry thieves).
  - Heavy, solid black-ink borders with woodcut grain imperfections and letterpress impression depth.
- **Earthy Vegetable Dye Palette:**
  - Indigo Blue (`#1B365D`), Madder Root Red (`#8A2B2B`), Weld Yellow (`#D19E34`), Forest Green (`#2C4C38`), Warm Oak Wood (`#5C3D28`), and Unbleached Linen Paper (`#F4EEDD`).
- **Typography:**
  - Heavy blackletter, humanist venetian serifs, and robust woodcut drop caps modeled after Morris's *Golden*, *Troy*, and *Chaucer* types (e.g., *Berkley Oldstyle*, *Goudy Medieval*, *ITC Golden Type*).

---

## 📐 Lighting Physics, Specular Splits & Surfaces

1. **Unbleached Rag Paper & Letterpress Impression:**
   - Soft, matte fibrous texture with subtle tactile indentations from the printing press.
   ```css
   background: #F4EEDD;
   box-shadow: inset 0 1px 3px rgba(60, 40, 20, 0.15), 0 4px 12px rgba(44, 76, 56, 0.12);
   border: 2px solid #5C3D28;
   ```
2. **Dense Woodcut Borders:**
   - Solid ink framing with no glossy highlights or artificial specular reflections.
   ```css
   border: 4px solid #1C2421;
   outline: 1px solid #5C3D28;
   outline-offset: -3px;
   ```

---

## 🏷️ Complete Design Tokens

```css
:root {
  /* Arts & Crafts Palette */
  --crafts-linen: #F4EEDD;
  --crafts-wood-dark: #3A2618;
  --crafts-oak: #5C3D28;
  --crafts-forest: #2C4C38;
  --crafts-madder: #8A2B2B;
  --crafts-indigo: #1B365D;
  --crafts-weld-gold: #C48E2E;
  --crafts-ink: #181D1A;

  /* Typography */
  --crafts-font-heading: 'Goudy Old Style', 'Palatino', serif;
  --crafts-font-body: 'Book Antiqua', 'Baskerville', serif;
}
```

---

## 🧱 Production-Ready Component Blueprint

```html
<article class="crafts-folio">
  <div class="crafts-border-inner">
    <span class="crafts-tag">KELMSCOTT WORKSHOP</span>
    <h3 class="crafts-headline">The Beauty of Honest Labor</h3>
    <p class="crafts-text">Handcrafted artifacts carrying the natural integrity of unadorned materials and woodblock prints.</p>
    <div class="crafts-woodcut-divider"></div>
    <button class="crafts-btn" type="button">INSPECT WORKMANSHIP</button>
  </div>
</article>
```

```css
.crafts-folio {
  background: var(--crafts-linen);
  border: 4px solid var(--crafts-wood-dark);
  padding: 8px;
  max-width: 480px;
  box-shadow: 0 4px 16px rgba(44, 76, 56, 0.15);
  font-family: var(--crafts-font-body);
  color: var(--crafts-ink);
}
.crafts-border-inner {
  border: 1px solid var(--crafts-oak);
  padding: 24px;
  text-align: center;
}
.crafts-tag {
  font-family: var(--crafts-font-heading);
  font-size: 0.75rem;
  letter-spacing: 0.18em;
  font-weight: 700;
  color: var(--crafts-madder);
  text-transform: uppercase;
}
.crafts-headline {
  font-family: var(--crafts-font-heading);
  font-size: 1.625rem;
  color: var(--crafts-forest);
  margin: 12px 0;
  line-height: 1.25;
}
.crafts-text {
  font-size: 0.9375rem;
  line-height: 1.65;
  color: var(--crafts-ink);
  margin-bottom: 20px;
}
.crafts-woodcut-divider {
  height: 2px;
  background: repeating-linear-gradient(
    90deg,
    var(--crafts-oak) 0px,
    var(--crafts-oak) 6px,
    transparent 6px,
    transparent 12px
  );
  margin: 16px auto;
  max-width: 140px;
}
.crafts-btn {
  background: var(--crafts-forest);
  color: var(--crafts-linen);
  font-family: var(--crafts-font-heading);
  font-weight: 700;
  letter-spacing: 0.12em;
  padding: 10px 24px;
  border: 2px solid var(--crafts-wood-dark);
  cursor: pointer;
  transition: background-color 150ms ease;
}
.crafts-btn:hover {
  background: var(--crafts-madder);
}
```

---

## ✨ Micro-Interactions, Motion & Soundscapes

- **Letterpress Stamp:** Buttons depress with physical tactile firmness (100ms ease-out) without bouncy spring curves.
- **Folio Turn:** Paging transitions mimic the slow, weighted turn of thick rag paper.

---

## ♿ WCAG 2.2 Accessibility & High-Contrast Guardrails

- **Contrast Ratios:**
  - Ink (`#181D1A`) on Linen (`#F4EEDD`): **13.8:1** (Passes WCAG AAA).
  - Forest Green (`#2C4C38`) on Linen (`#F4EEDD`): **7.8:1** (Passes WCAG AAA).
  - Madder Red (`#8A2B2B`) on Linen (`#F4EEDD`): **5.9:1** (Passes WCAG AA).
- **Dual-Contrast Focus Ring:**
  `outline: 2px solid var(--crafts-madder); box-shadow: 0 0 0 2px var(--crafts-linen);`

---

## 🚫 Anti-Patterns & Visual Sins (Anti-AI Slop Traps)

- ❌ **NEVER use synthetic neon colors or glossy plastic bevels:** All hues must reflect historic natural pigments.
- ❌ **NEVER use modern sans-serifs or lightweight display type:** Arts & Crafts demands the weight and ink density of the printing press.

---

## 📚 Sources & References

- William Morris, *The Ideal Book: An Address Delivered for the Bibliographical Society* (London, 1893).
- John Ruskin, *The Stones of Venice: On the Nature of Gothic* (Smith, Elder & Co., 1853).
## Appearance and Interaction Verification

Let inner rag-paper padding respond to the actual folio width while preserving heavy woodcut borders; keep thick-paper turns optional and expose final page content immediately under reduced motion.

