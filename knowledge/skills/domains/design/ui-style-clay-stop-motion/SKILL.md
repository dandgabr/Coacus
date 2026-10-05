---
name: "ui-style-clay-stop-motion"
description: "Provides the clay stop-motion and plasticine texture UI style: tactile handcrafted fingerprint textures, stepped frame-rate animations, organic molded 3D volumes and warm artisanal charm. Use when creating animation studio, gaming or playful handcrafted websites."
---

# UI Style: Clay Stop-Motion & Plasticine

Draws from stop-motion clay animation (Aardman Animations, Laika, Will Vinton). Combines 3D plasticine volumes with handmade tactile imperfections, subtle fingerprint indentations, matte clay materials, and stepped (choppy 12fps) frame rate animations that feel physically sculpted by human hands. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Animation studios, children's digital books, indie claymation games, craft brands, and whimsical creative portfolios.
- Radiating warmth, physical human craftsmanship, and artistic play.
- Replacing sterile computerized 3D renders with the charm of physical plasticine modeling.

---

## 🕰️ Definition and Timeline

- **Origins:** Originates in cinematic clay animation (Will Vinton's *Claymation*, 1974; Nick Park's *Wallace & Gromit*, 1989), arriving in digital interfaces through physical clay scanning, 3D clay shaders, and stepped CSS animation curves.
- **Philosophy:** Tactile humanity in a digital world. Celebrating the beauty of visible human thumbprints, clay seams, and organic material imperfections.
- **Difference from neighbors:** Unlike digital [ui-style-claymorphism](../ui-style-claymorphism/SKILL.md), which uses smooth mathematical CSS shadows, Clay Stop-Motion emphasizes physical fingerprints, matte earth clays, and stepped frame-rate animations.

---

## 🎨 Visual DNA

- **Palette:** Terracotta clay (`#E76F51`), mustard plasticine (`#E9C46A`), river stone clay (`#2A9D8F`), baked clay white (`#FDFAF6`), and earthy loam (`#3D2B1F`).
- **Textures & Shading:** Subtle matte clay grain, fingerprint dents along borders, dual-direction inner shadows (`inset -4px -4px 8px rgba(0,0,0,0.1), inset 4px 4px 8px rgba(255,255,255,0.7)`).
- **Shapes:** Organic, hand-pressed irregular rounded corners (`border-radius: 30px 22px 28px 24px`).
- **Depth:** Soft physical clay drops onto the table surface.

---

## 🖱️ Interaction and Motion

- Stepped frame rate: hover animations move in choppy 10–12 fps steps (`animation-timing-function: steps(5)`), giving an authentic stop-motion film feel.
- Clay depression: buttons squish with uneven hand-pressed indentations when clicked.
- Under `prefers-reduced-motion: reduce`, disable all stepped wiggles and frame shifts.

---

## 🛠️ Implementation Notes

```css
#stage[data-style="clay-stop-motion"] {
  --bg: #f4ece1;
  --surface: #fdfaf6;
  --fg: #3d2b1f;
  --muted: #7d6b5e;
  --accent: #e76f51;
  --accent-fg: #ffffff;
  --border: #e8dec8;
  --radius: 28px;
  --shadow: inset -4px -4px 8px rgba(0,0,0,.08), inset 4px 4px 8px rgba(255,255,255,.8), 0 8px 18px rgba(61,43,31,.1);
  --font-body: 'Baloo 2', 'Nunito', sans-serif;
  --font-display: 'Baloo 2', sans-serif;
  background-color: var(--bg);
}
```

---

## ♿ Accessibility

- **High-contrast typography:** Ensure clay-toned buttons maintain crisp white or dark chocolate text exceeding 5:1 contrast.
- **Reduced motion protection:** Stepped animations can irritate some users; always honor `prefers-reduced-motion: reduce` by replacing steps with static states.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** Animation festivals, children's creative apps, craft marketplaces, indie video games, and creative agencies.
- **Avoid:** Corporate accounting, medical devices, and high-frequency data portals.

---

## 📚 Sources

- Nick Park, *The Making of Wallace & Gromit*, Pavilion Books, 1997.
- Will Vinton, *Claymation: The Art of Dimensional Animation*, 1980.
- Richard Williams, *The Animator's Survival Kit*, Faber & Faber, 2001.

---

## 🔗 Integration with Other Skills

- Sibling tactile styles: [ui-style-claymorphism](../ui-style-claymorphism/SKILL.md), [ui-style-hand-drawn-sketch](../ui-style-hand-drawn-sketch/SKILL.md).
