---
name: "ui-style-solarpunk-naturecore"
description: "Provides the naturecore and digital cottagecore UI style: warm woven linen textures, botanical watercolor elements, earthy terracotta and sage palettes, hand-stitched borders and tranquil organic rhythms. Use when designing eco-conscious, artisanal, wellbeing or sustainable lifestyle interfaces."
---

# UI Style: Naturecore & Digital Cottagecore

A serene, earth-grounded design philosophy prioritizing warmth, handmade craftsmanship, and botanical harmony. Responds to cold tech minimalism with woven linen textures, natural dye tones, pressed botanical accents, and tactile softness. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Sustainable fashion, organic agriculture, mindful lifestyle, herbalism, and artisanal craft stores.
- Creating an atmosphere of quiet tranquility, organic comfort, and human warmth.
- Designing eco-friendly brand portals that reject sleek corporate gloss.

---

## 🕰️ Definition and Timeline

- **Lineage:** Rooted in the 19th-century Arts and Crafts movement (William Morris), reviving in the 2020s through the digital "Cottagecore" aesthetic and pastoral internet subcultures.
- **Philosophy:** Digital slow living. Rejecting algorithmic urgency in favor of visual pacing that feels hand-crafted, peaceful, and grounded in the natural world.
- **Difference from neighbors:** Unlike [ui-style-solarpunk](../ui-style-solarpunk/SKILL.md), which is futuristic, high-tech, and solar-infrastructure driven, Naturecore is artisanal, pastoral, and tactile. Unlike [ui-style-calm-quiet-ui](../ui-style-calm-quiet-ui/SKILL.md), which is modern-minimalist and neutral-gray, Naturecore uses rich warm earth pigments and organic botanical textures.

---

## 🎨 Visual DNA

- **Palette:** Oatmeal linen (`#F7F4EE`), sage green (`#7D9D8B`), warm terracotta (`#C86D51`), soft mustard (`#E0B050`), and deep woodland pine (`#2C4235`).
- **Type:** Humanist serif fonts with calligraphic warmth (Fraunces, Cormorant Garamond, Lora) paired with soft sans-serif body copy (Quicksand, Nunito).
- **Textures:** Subtle paper grain, linen fabric weave, pressed botanical accents, and deckle paper edges.
- **Shapes:** Soft rounded cards (`border-radius: 16px` to `24px`), gently irregular organic contours, and pressed ribbon badges.
- **Depth:** Gentle, warm diffuse ambient shadows (`box-shadow: 0 8px 24px rgba(44, 66, 53, 0.06)`).

---

## 🖱️ Interaction and Motion

- Gentle organic ease: hover states transition with slow, natural deceleration (`transition: all 0.3s ease-out`).
- Tactile press: buttons settle smoothly without aggressive spring or bounce.
- Under `prefers-reduced-motion: reduce`, disable all parallax layer motion.

---

## 🛠️ Implementation Notes

```css
#stage[data-style="solarpunk-naturecore"] {
  --bg: #f7f4ee;
  --surface: #ffffff;
  --surface-2: #ece6d9;
  --fg: #2c4235;
  --muted: #5e7264;
  --accent: #c86d51;
  --accent-fg: #ffffff;
  --border: #d8d0c0;
  --radius: 16px;
  --radius-sm: 10px;
  --font-body: 'Fraunces', serif;
  --font-display: 'Fraunces', serif;
}
```

---

## ♿ Accessibility

- **Contrast verification:** Muted sage on oatmeal can fail contrast checks; always use deep woodland pine (`#2C4235`) for body text (> 7:1 ratio).
- **Focus states:** Provide visible, warm terracotta outline focus rings with 2px offset.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** Wellness, organic food, slow fashion, ecological initiatives, and craft studios.
- **Avoid:** High-speed financial trading, cyberpunk gaming, and developer API docs.

---

## 📚 Sources

- William Morris, *News from Nowhere and Selected Writings*, Penguin Classics, 1890/2004.
- Isabel Slone, "The Wholesome Brilliance of Cottagecore", *The New York Times*, 2020.
- Ellen Lupton, *Thinking with Type*, Princeton Architectural Press, 2014.

---

## 🔗 Integration with Other Skills

- Sibling organic styles: [ui-style-organic-biophilic](../ui-style-organic-biophilic/SKILL.md), [ui-style-solarpunk](../ui-style-solarpunk/SKILL.md), [ui-style-calm-quiet-ui](../ui-style-calm-quiet-ui/SKILL.md).
