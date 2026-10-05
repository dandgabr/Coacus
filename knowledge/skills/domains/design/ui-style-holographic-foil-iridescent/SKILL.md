---
name: "ui-style-holographic-foil-iridescent"
description: "Provides the holographic foil and iridescent chrome UI style: dynamic rainbow refraction angles, pearlescent shimmer, metallic specular highlights and shifting prism gradients. Use when designing collector drops, luxury cosmetics or futuristic fintech cards."
---

# UI Style: Holographic Foil & Iridescent Chrome

Recreates the shimmering optical effect of security holograms, trading card foils, and iridescent titanium coatings. Surface colors dynamically shift across the full rainbow spectrum as the cursor moves or device rotates. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Collector cards, web3 drops, high-fashion cosmetics, premium fintech card interfaces, and luxury youth culture platforms.
- Creating a sense of rarity, optical magic, and premium futuristic value.
- Elevating cards and badges with physical foil reflection textures.

---

## 🕰️ Definition and Timeline

- **Origins:** Originates in physical security holograms (Dennis Gabor, Nobel Prize 1971; American Bank Note Company, 1983) and 1990s collectible foil trading cards (Magic: The Gathering, Pokémon).
- **Digital revival:** Re-emerged in the 2020s through digital 3D card simulations, mobile accelerometer-driven shaders, and high-fashion web experiences.
- **Difference from neighbors:** Unlike [ui-style-glassmorphism](../ui-style-glassmorphism/SKILL.md), which is transparent and static, Holographic Foil is opaque, reflective, prismatic, and dynamic. Unlike [ui-style-gradient-duotone](../ui-style-gradient-duotone/SKILL.md), which uses two fixed static hues, Holographic cycles through the complete rainbow prism based on light angles.

---

## 🎨 Visual DNA

- **Palette:** Shifting rainbow prism: pearlescent violet (`#E0C3FC`), electric mint (`#8EC5FC`), radiant pink (`#FBC2EB`), holographic silver (`#F3F4F6`), and pitch obsidian canvas (`#0F1016`).
- **Prismatic Effects:** Multi-stop linear and conic gradients simulating thin-film optical interference, dynamic cursor-tracking light flares, and chromatic aberration fringe.
- **Depth:** Luminous specular flares, metallic border reflections, and soft ambient colored glow (`box-shadow: 0 10px 30px rgba(142, 197, 252, 0.3)`).
- **Type:** Sharp contemporary geometric sans-serif (Syne, Clash Display, Space Grotesk) with metallic foil fill gradients.

---

## 🖱️ Interaction and Motion

- Gyroscopic / cursor flare: moving the mouse across a card shifts the specular gradient highlight across the surface (`transform: translate(-100%)` to `translateX(100%)`).
- Tilt depth: 3D perspective card tilt tracking the pointer with spring damping.
- Under `prefers-reduced-motion: reduce`, disable continuous shimmer and 3D tilts, showing a static pearlescent gradient.

---

## 🛠️ Implementation Notes

```css
#stage[data-style="holographic-foil-iridescent"] {
  --bg: #0f1016;
  --surface: rgba(255, 255, 255, 0.08);
  --fg: #ffffff;
  --muted: #a0a5b8;
  --accent: #8ec5fc;
  --accent-fg: #0f1016;
  --border: rgba(255, 255, 255, 0.3);
  --radius: 20px;
  --font-body: 'Syne', sans-serif;
  --font-display: 'Syne', sans-serif;
  background-color: var(--bg);
}
```

---

## ♿ Accessibility

- **Text contrast protection:** Prismatic foil backgrounds must never sit directly beneath delicate body copy without an opaque backing or strong text shadow, ensuring WCAG AA contrast compliance.
- **Visual comfort:** Shimmer flares must remain smooth and subtle; avoid strobe-like frequency flashes (> 3 flashes/second).

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** Exclusive membership tiers, luxury fintech cards, collectible art drops, and beauty brand landings.
- **Avoid:** Dense informational documentation, medical dashboards, and enterprise administration consoles.

---

## 📚 Sources

- Dennis Gabor, *Holography, 1948-1971*, Nobel Lecture, 1971.
- Simon Garfield, *Mauve: How One Man Invented a Color That Changed the World*, Faber & Faber, 2000.
- Codrops, *Interactive Holographic Card Shaders*, 2022.

---

## 🔗 Integration with Other Skills

- Sibling material styles: [ui-style-glassmorphism](../ui-style-glassmorphism/SKILL.md), [ui-style-glassmorphism](../ui-style-glassmorphism/SKILL.md), [ui-style-gradient-duotone](../ui-style-gradient-duotone/SKILL.md).
