---
name: "ui-style-clay-stop-motion"
description: "Provides the clay stop-motion and plasticine texture UI style: tactile handcrafted fingerprint textures, stepped frame-rate animations, organic molded volumes and warm artisanal charm. Use when creating animation studio, gaming or playful handcrafted websites."
---

# UI Style: Clay Stop-Motion & Plasticine

Draws from stop-motion clay animation (Aardman, Laika). Combines 3D plasticine volumes with handmade tactile imperfections, subtle fingerprint indentations, and stepped (choppy 12fps) frame rate animations that feel physically sculpted by human hands.

---

## 🧭 When to Activate

- Animation studios, children's digital books, indie claymation games, craft brands, and whimsical creative portfolios.
- Radiating warmth, physical human craftsmanship, and artistic play.

---

## 🎨 Visual DNA

- **Palette:** Terracotta, clay red, mustard plasticine, sky blue, and earthy olive.
- **Textures:** Subtle matte clay grain, fingerprint dents along borders, and slightly uneven hand-pressed edges.
- **Animation:** Stepped 10–12 fps transitions (`animation-timing-function: steps(6)`), giving an authentic stop-motion feel.

---

## 🛠️ Implementation Notes

```css
.clay-sculpted-btn {
  background: #e76f51;
  color: #fff;
  border-radius: 28px 24px 30px 22px;
  box-shadow: inset -4px -4px 8px rgba(0, 0, 0, 0.2), inset 4px 4px 8px rgba(255, 255, 255, 0.4), 0 8px 16px rgba(0, 0, 0, 0.15);
}
.stop-motion-anim {
  animation: wiggle 0.6s steps(4) infinite;
}
```

---

## ♿ Accessibility

- Ensure stepped animations can be completely paused via `prefers-reduced-motion: reduce`.
