---
name: "ui-style-skeuomorphic-y2k-cyber"
description: "Provides the Y2K Cyber Aqua and early Mac OS X glossy UI style: luminous water-drop buttons, translucent colored plastics (iMac G3), brushed aluminum and optimistic cyber-whimsical gloss. Use when creating playful retro-tech, music player or 2000s nostalgic platforms."
---

# UI Style: Y2K Cyber Aqua & iMac Gloss

Captures the iconic aesthetic of the turn of the millennium (2000–2005): Apple's Aqua interface, translucent candy-colored plastics of the iMac G3, gel drop buttons, and brushed metal textures. Optimistic, friendly, and deliciously glossy.

---

## 🧭 When to Activate

- Nostalgic media players, creative software, playful consumer applications, and early-2000s retro portals.
- Bringing tactile fun, candy gloss, and bubbly computer optimism to modern web experiences.

---

## 🎨 Visual DNA

- **Palette:** Bondi blue (`#0095B6`), lime green (`#8EE53F`), tangerine orange (`#FFA000`), grape purple (`#7D3F98`), and high-gloss aquatic blue (`#2EA5FF`).
- **Effects:** Curvature highlights, top specular glass reflection crescents, dropped inner pill shadows, and subtle horizontal scan stripes.
- **Elements:** Luminous aquatic jelly buttons (Aqua pill), brushed aluminum window headers, and bubble indicators.

---

## 🛠️ Implementation Notes

```css
.aqua-pill-btn {
  background: linear-gradient(to bottom, #7fcbfb 0%, #2998f4 50%, #0c7de6 51%, #1ca2f9 100%);
  border: 1px solid #005bb7;
  border-radius: 20px;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.7), 0 2px 4px rgba(0, 0, 0, 0.2);
  color: white;
  text-shadow: 0 -1px 1px #004b99;
}
```

---

## ♿ Accessibility

- Glossy white text on blue aqua pills requires dark outline text-shadows to ensure compliance with WCAG AA.
