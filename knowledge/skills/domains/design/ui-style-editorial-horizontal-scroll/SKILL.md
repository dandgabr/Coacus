---
name: "ui-style-editorial-horizontal-scroll"
description: "Provides the horizontal scroll gallery and editorial ribbon UI style: lateral cinematic navigation, continuous filmstrip pacing, architectural column spreads and gallery curatorial rhythm. Use when crafting fine art, photography, fashion or architecture monographs."
---

# UI Style: Horizontal Gallery & Editorial Ribbon

Replaces traditional vertical scrolling with a curated lateral journey. Translates the experience of walking through an art gallery, paging through an expansive luxury monograph, or moving along a cinematic film reel. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Fine art galleries, architectural portfolio walk-throughs, fashion lookbooks, and luxury editorial showcases.
- Pacing content horizontally with curated spatial pauses, large photography, and wide column spreads.
- Creating contemplative, immersive storytelling that breaks traditional web page scrolling habits.

---

## 🕰️ Definition and Timeline

- **Origins:** Pioneered by experimental Flash portfolios in the early 2000s, rehabilitated and perfected with modern CSS Scroll Snap and touch gestures in the late 2010s (Awwwards Site of the Year nominees, Gucci and Balenciaga fashion editorials).
- **Philosophy:** Spatial curation over speed. Resisting the mindless vertical thumb-scroll to invite users to pause, inspect details, and experience curated panoramic spreads.
- **Difference from neighbors:** Unlike [ui-style-editorial-archive-luxury](../ui-style-editorial-archive-luxury/SKILL.md), which uses classical vertical publication grids, Horizontal Scroll forces a lateral axis of movement. Unlike [ui-style-one-page-long-scroll](../ui-style-one-page-long-scroll/SKILL.md), the navigation axis is rotated 90 degrees.

---

## 🎨 Visual DNA

- **Flow & Orientation:** Lateral track movement across horizontal viewport dimensions (`scroll-snap-type: x mandatory`).
- **Type:** Refined classical serif display (Didot, Bodoni, Ogg, Playfair Display) paired with austere monospaced footnotes and index numbers.
- **Layout & Spreads:** Asymmetric panel heights, hanging horizontal baselines, wide white-cube museum gallery pacing, and numbered exhibition cards.
- **Palette:** Ivory gallery plaster (`#F6F5F2`), carbon ink (`#1F1E1D`), archival warm border (`#E2DFD7`), and gold leaf accents (`#C5A880`).
- **Depth:** Zero drop shadows; flat, pristine museum-wall mounting aesthetics.

---

## 🖱️ Interaction and Motion

- Snapping scroll: panels snap cleanly into place when dragging or scrolling horizontally (`scroll-snap-align: start`).
- Keyboard arrows: explicit Left and Right arrow navigation with smooth gliding velocity.
- Under `prefers-reduced-motion: reduce`, allow immediate instant snapping without momentum gliding.

---

## 🛠️ Implementation Notes

```css
#stage[data-style="editorial-horizontal-scroll"] {
  --bg: #f6f5f2;
  --surface: #ffffff;
  --fg: #1f1e1d;
  --muted: #737068;
  --accent: #1f1e1d;
  --accent-fg: #ffffff;
  --border: #e2dfd7;
  --radius: 2px;
  --font-body: 'Didot', 'Bodoni MT', Georgia, serif;
  --font-display: 'Didot', serif;
  background-color: var(--bg);
}
```

---

## ♿ Accessibility

- **Keyboard navigation:** Mandatory support for Left/Right arrow keys and Tab focus flow across horizontal panels.
- **Alternative navigation:** Provide an accessible vertical overview index or table of contents modal for users with motor impairments or trackpad difficulties.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** Art galleries, photography portfolios, architectural studies, fashion lookbooks, and luxury watchmaker showcases.
- **Avoid:** E-commerce checkouts, SaaS configuration panels, and high-frequency analytical data tools.

---

## 📚 Sources

- Awwwards Collections, *The Best Horizontal Websites*, 2021.
- Adrian Shaughnessy, *How to be a Graphic Designer Without Losing Your Soul*, Princeton Architectural Press, 2010.
- W3C, *CSS Scroll Snap Module Level 1*, 2021.

---

## 🔗 Integration with Other Skills

- Sibling editorial styles: [ui-style-editorial-archive-luxury](../ui-style-editorial-archive-luxury/SKILL.md), [ui-style-scrollytelling](../ui-style-scrollytelling/SKILL.md).
