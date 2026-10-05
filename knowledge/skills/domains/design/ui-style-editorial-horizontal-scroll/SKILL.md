---
name: "ui-style-editorial-horizontal-scroll"
description: "Provides the horizontal scroll gallery and editorial ribbon UI style: lateral cinematic navigation, continuous filmstrip pacing, architectural column spreads and gallery curatorial rhythm. Use when crafting fine art, photography, fashion or architecture monographs."
---

# UI Style: Horizontal Gallery & Editorial Ribbon

Replaces traditional vertical scrolling with a curated lateral journey. Translates the experience of walking through an art gallery, paging through an expansive luxury monograph, or moving along a cinematic film reel.

---

## 🧭 When to Activate

- Fine art galleries, architectural portfolio walk-throughs, fashion lookbooks, and luxury editorial showcases.
- Pacing content horizontally with curated spatial pauses and panoramic photography.

---

## 🎨 Visual DNA

- **Flow:** Lateral track movement across horizontal viewport dimensions, smooth snapping to card focal points.
- **Type:** Refined classical serif display (Didot, Bodoni, Ogg) paired with austere monospaced footnotes and index numbers.
- **Layout:** Asymmetric panel heights, hanging horizontal baselines, and white-cube museum gallery pacing.

---

## 🛠️ Implementation Notes

```css
.horizontal-scroll-container {
  display: flex;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  height: 100vh;
}
.horizontal-panel {
  flex: 0 0 70vw;
  scroll-snap-align: start;
  padding: 4rem;
}
```

---

## ♿ Accessibility

- Provide clear keyboard navigation support (Left/Right arrow keys) in addition to wheel/trackpad scrolling.
- Offer alternative standard vertical navigation or jump-to-section index for users with motor difficulties.
