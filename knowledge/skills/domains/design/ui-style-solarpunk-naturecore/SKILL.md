---
name: "ui-style-solarpunk-naturecore"
description: "Provides the naturecore and digital cottagecore UI style: warm linen textures, botanical watercolor elements, earthy natural palettes, hand-stitched borders and tranquil organic rhythms. Use when designing eco-conscious, artisanal, wellbeing or sustainable lifestyle interfaces."
---

# UI Style: Naturecore & Digital Cottagecore

A serene, earth-grounded design philosophy prioritizing warmth, handmade craftsmanship, and botanical harmony. Responds to cold tech minimalism with woven linen textures, natural dye tones, pressed flower motifs, and tactile softness.

---

## 🧭 When to Activate

- Sustainable fashion, herbalism, organic agriculture, mindful lifestyle, and artisanal craft stores.
- Creating an atmosphere of quiet tranquility, organic comfort, and warmth.

---

## 🎨 Visual DNA

- **Palette:** Oatmeal linen (`#F7F4EE`), sage green (`#7D9D8B`), warm terracotta (`#C86D51`), soft mustard (`#E0B050`), and deep woodland pine (`#2C4235`).
- **Type:** Humanist serif fonts with calligraphic warmth (Cormorant Garamond, Fraunces, Lora) paired with soft sans-serif body copy.
- **Textures:** Subtle paper grain, linen fabric weave, hand-drawn botanical branch accents, and deckle paper edges.
- **Shapes:** Soft rounded cards, gently irregular organic contours, and pressed ribbon badges.

---

## 🛠️ Implementation Notes

```css
:root {
  --linen-bg: #f7f4ee;
  --sage-accent: #7d9d8b;
  --terracotta: #c86d51;
  --woodland: #2c4235;
}
.nature-card {
  background: #ffffff;
  border: 1px solid rgba(125, 157, 139, 0.25);
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(44, 66, 53, 0.05);
}
```

---

## ♿ Accessibility

- Verify that muted earthy colors (such as sage on oatmeal) are not used for essential body text; reserve dark woodland (`#2C4235`) for high contrast readability (> 7:1).
