---
name: "ui-style-holographic-foil-iridescent"
description: "Provides the holographic foil and iridescent chrome UI style: dynamic rainbow refraction angles, pearlescent shimmer, metallic specular highlights and shifting prism gradients. Use when designing collector drops, luxury cosmetics or futuristic fintech cards."
---

# UI Style: Holographic Foil & Iridescent Chrome

Recreates the shimmering optical effect of security holograms, trading card holographic foils, and iridescent titanium coatings. Surface colors dynamically shift across the full rainbow spectrum as the cursor moves or device rotates.

---

## 🧭 When to Activate

- Collector cards, NFT/web3 drops, high-fashion cosmetics, premium fintech debit card interfaces, and luxury youth culture platforms.
- Creating a sense of rarity, optical magic, and premium futuristic value.

---

## 🎨 Visual DNA

- **Palette:** Shifting rainbow prism: pearlescent violet, electric mint, radiant pink, holographic silver, and prismatic gold.
- **Effects:** Conic gradients, specular flare sweeps, dynamic cursor-tracking light reflections, and chromatic aberration fringe.

---

## 🛠️ Implementation Notes

```css
.holographic-card {
  background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 50%, #fbc2eb 100%);
  background-size: 200% 200%;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(142, 197, 252, 0.3);
  position: relative;
  overflow: hidden;
}
.holographic-card::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(115deg, transparent 20%, rgba(255,255,255,0.7) 40%, transparent 60%);
  transform: translateX(-100%);
  transition: transform 0.6s ease;
}
.holographic-card:hover::before {
  transform: translateX(100%);
}
```

---

## ♿ Accessibility

- Prism reflections must not obscure content text. Keep text colors solid (e.g. deep black or crisp white) with sufficient background contrast.
