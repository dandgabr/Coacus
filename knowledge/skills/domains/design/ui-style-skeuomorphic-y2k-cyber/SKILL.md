---
name: "ui-style-skeuomorphic-y2k-cyber"
description: "Provides the Y2K Cyber Aqua and early Mac OS X glossy UI style (2000-2005): luminous aquatic drop buttons, translucent colored plastics (iMac G3), brushed aluminum and optimistic cyber-whimsical gloss. Use when creating playful retro-tech, media player or 2000s nostalgic platforms."
---

# UI Style: Y2K Cyber Aqua & iMac Gloss

Captures the iconic consumer tech aesthetic of the turn of the millennium (2000–2005): Apple's Aqua interface, translucent candy-colored plastics of the iMac G3, liquid water-drop buttons, and brushed aluminum window headers. Optimistic, friendly, and deliciously glossy. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Nostalgic media players, creative software, playful consumer applications, and early-2000s retro portals.
- Bringing tactile fun, candy gloss, and bubbly computer optimism to modern web experiences.
- Crafting entertainment and music platforms that break away from sterile flat minimalism.

---

## 🕰️ Definition and Timeline

- **Origins:** Unveiled by Steve Jobs at Macworld San Francisco in January 2000 ("One of the design goals was: when you saw it you wanted to lick it"). Defined early Mac OS X (Cheetah through Tiger, 2001–2005).
- **Philosophy:** Joyful digital optimism. Translating physical jelly drops, candy translucency, and aquatic buoyancy into graphical software controls.
- **Difference from neighbors:** Unlike [ui-style-frutiger-aero](../ui-style-frutiger-aero/SKILL.md), which is late 2000s (2006–2012) with bright green lawns, cloudy blue skies, and Windows Vista glass, Y2K Cyber Aqua is specifically turn-of-the-millennium candy plastics, jelly gumdrop buttons, and brushed metal textures.

---

## 🎨 Visual DNA

- **Palette:** Bondi blue (`#0095B6`), lime green (`#8EE53F`), tangerine orange (`#FFA000`), aquatic blue (`#2998F4`), and brushed aluminum platinum (`#DCE4EC`).
- **Surface & Gloss:** Gel drop convex buttons with top white specular reflection crescents, inner pill shadows, and subtle horizontal pinstripe backgrounds.
- **Controls:** Gelatinous aquatic pill buttons, three-dimensional traffic-light window controls, and striped progress bars.
- **Depth:** Multi-layered specular highlights, soft aquatic drop shadows (`0 8px 20px rgba(41, 152, 244, 0.2)`), and beveled chrome borders.

---

## 🖱️ Interaction and Motion

- Aquatic pulse: buttons glow with soft breathing cyan pulses on focus.
- Satisfying click: jelly buttons compress with high gloss intensity on active click (`filter: brightness(0.92)`).
- Under `prefers-reduced-motion: reduce`, disable all breathing button pulses.

---

## 🛠️ Implementation Notes

```css
#stage[data-style="skeuomorphic-y2k-cyber"] {
  --bg: #d4e8f7;
  --surface: rgba(255, 255, 255, 0.88);
  --fg: #0a2d4d;
  --muted: #2d618c;
  --accent: #2998f4;
  --accent-fg: #ffffff;
  --border: #7cb5e2;
  --radius: 16px;
  --font-body: 'Lucida Grande', system-ui, sans-serif;
  --font-display: 'Lucida Grande', sans-serif;
  background: linear-gradient(to bottom, #dbeffc 0%, #c4e1f7 100%);
}
```

---

## ♿ Accessibility

- **Gloss text contrast:** White text on glossy blue buttons requires dark navy text-shadows (`text-shadow: 0 -1px 1px #004B99`) to meet WCAG AA contrast standards.
- **Focus state clarity:** Provide distinct, non-color-only focus rings around jelly buttons.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** Music streaming, retro media players, youth culture apparel, personal creative portfolios, and 2000s nostalgic projects.
- **Avoid:** Corporate B2B enterprise software, government portals, and medical dashboards.

---

## 📚 Sources

- Apple Inc., *Aqua Human Interface Guidelines*, Apple Computer, 2001.
- Steven Levy, *Insanely Great: The Life and Times of Macintosh*, Penguin Books, 2000.
- Jonathan Ive, *Design Philosophy of the iMac G3 and Aqua*, 2001.

---

## 🔗 Integration with Other Skills

- Sibling glossy styles: [ui-style-frutiger-aero](../ui-style-frutiger-aero/SKILL.md), [ui-style-y2k-revival](../ui-style-y2k-revival/SKILL.md), [ui-style-skeuomorphism](../ui-style-skeuomorphism/SKILL.md).
