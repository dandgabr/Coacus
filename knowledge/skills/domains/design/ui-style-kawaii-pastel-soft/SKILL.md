---
name: "ui-style-kawaii-pastel-soft"
description: "Provides the kawaii pastel and cute aesthetic UI style: ultra-soft marshmallow shapes, pillowy candy shadows, pastel rainbow palette and whimsical sticker microcopy. Use when building welcoming consumer apps, children educational games or creative lifestyle hubs."
---

# UI Style: Kawaii Pastel & Soft Aesthetic

A warm, playful aesthetic celebrating cuteness, approachability, and comforting gentleness. Features pillowy marshmallow radius shapes, soothing pastel tones, charming sticker accents, and friendly micro-interactions.

---

## 🧭 When to Activate

- Children's educational tools, wellness and self-care trackers, casual mobile-first web apps, creative craft stores.
- Removing all intimidation from technology, fostering an inviting, heartwarming atmosphere.

---

## 🎨 Visual DNA

- **Palette:** Baby pink (`#FFB3C6`), soft lavender (`#D8BBFF`), buttercup yellow (`#FFF099`), mint cream (`#BFFCC6`), and sky blue (`#C4F0FF`).
- **Type:** Rounded friendly typefaces (Nunito, Quicksand, Baloo 2, Fredoka).
- **Cards & Buttons:** Generous pillowy radius (24px–36px), soft puffy drop shadows with colored ambient glow, and rounded borders.

---

## 🛠️ Implementation Notes

```css
.kawaii-btn {
  background: #ffb3c6;
  color: #5c3d46;
  border-radius: 9999px;
  border: 3px solid #ffffff;
  box-shadow: 0 6px 0 #ff8fab, 0 10px 15px rgba(255, 143, 171, 0.3);
  font-family: 'Nunito', sans-serif;
  font-weight: 800;
}
.kawaii-btn:active {
  transform: translateY(4px);
  box-shadow: 0 2px 0 #ff8fab;
}
```

---

## ♿ Accessibility

- Pastel backgrounds can easily produce low contrast with white text; always pair pastels with deep berry or dark chocolate text (`#5C3D46`) to maintain WCAG AA compliance.
