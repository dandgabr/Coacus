---
name: "ui-style-silkpunk"
description: "Provides the silkpunk speculative UI style: East Asian classical antiquity fused with organic engineering, mulberry paper textures, bamboo and hammered brass accents, sumi-e ink washes and origami geometric folds. Use when creating speculative cultural, gaming or East Asian literature web experiences."
---

# UI Style: Silkpunk & Organic Engineering

Coined by author Ken Liu, silkpunk blends East Asian classical antiquity (Han, Tang, and Song dynasties) with speculative organic engineering. Features structures built of bamboo, silk, coconut fiber, paper lanterns, and steam or wind dynamics, articulated in sumi-e ink washes and origami geometry. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Cultural literature platforms, East Asian fantasy and sci-fi games, historical archives, and expressive artistic sites.
- Synthesizing organic Asian traditional craftsmanship with futuristic mechanical interfaces.
- Crafting visual narratives celebrating non-Western technological futures.

---

## 🕰️ Definition and Timeline

- **Origins:** Coined by author and translator Ken Liu in 2015 to describe the aesthetic of his *Dandelion Dynasty* novels (*The Grace of Kings*).
- **Philosophy:** A technology system based on organic materials and mechanical principles native to East Asian antiquity rather than Western brass and coal (steampunk). Technology made of silk, bamboo, sinew, ox-bone, and paper.
- **Difference from neighbors:** Unlike [ui-style-steampunk](../ui-style-steampunk/SKILL.md), which is Victorian London, heavy brass, and dark coal smoke, Silkpunk is light, wind-driven, paper-and-bamboo constructed, and fluid. Unlike [ui-style-cyberpunk](../ui-style-cyberpunk/SKILL.md), which is neon-dystopian, Silkpunk is classical, harmonious, and organic.

---

## 🎨 Visual DNA

- **Palette:** Vermilion lacquer red (`#C3272B`), indigo dye blue (`#1D2A44`), bamboo stalk green (`#6A8D73`), aged mulberry paper (`#F5EFE0`), and hammered brass gold (`#C9A050`).
- **Type:** Calligraphic brush display fonts, elegant high-contrast serifs (Noto Serif CJK, Cinzel Decorative), paired with clean Asian grotesques.
- **Motifs & Textures:** Origami geometric fold seams, sumi-e ink wash gradients, cloud patterns (cloud scrolls), and bamboo-joint dividing bars.
- **Structure:** Vertical text reading tracks, pavilion lattice grids, and paper screen sliding panel animations.

---

## 🖱️ Interaction and Motion

- Paper fan unfolding: navigation panels open with crisp geometric fan-out animations.
- Ink wash bleed: hover states trigger soft watercolor bleeds rather than sharp digital glows.
- Under `prefers-reduced-motion: reduce`, replace unfolding animations with simple opacity fades.

---

## 🛠️ Implementation Notes

```css
#stage[data-style="silkpunk"] {
  --bg: #f5efe0;
  --surface: #fbf7ee;
  --fg: #1d2a44;
  --accent: #c3272b;
  --accent-fg: #ffffff;
  --border: #c9a050;
  --radius: 6px;
  --font-body: 'Noto Serif', Georgia, serif;
  --font-display: 'Noto Serif', serif;
  background-color: var(--bg);
}
```

---

## ♿ Accessibility

- **Typography legibility:** Restrict decorative brush typography strictly to major titles; body paragraphs and navigational buttons must use legible serif or sans-serif fonts.
- **Contrast compliance:** Archival indigo on mulberry paper achieves contrast ratios exceeding 11:1.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** East Asian cultural portals, speculative fiction publications, narrative RPGs, and artisanal tea/craft platforms.
- **Avoid:** Generic B2B software, corporate banking, and standard SaaS dashboards.

---

## 📚 Sources

- Ken Liu, "Silkpunk: An Introduction", *io9*, 2015.
- Joseph Needham, *Science and Civilisation in China*, Cambridge University Press, 1954–2008.
- Laurence Sickman & Alexander Soper, *The Art and Architecture of China*, Penguin Books, 1971.

---

## 🔗 Integration with Other Skills

- Sibling speculative styles: [ui-style-steampunk](../ui-style-steampunk/SKILL.md), [ui-style-solarpunk](../ui-style-solarpunk/SKILL.md), [ui-style-clockpunk](../ui-style-clockpunk/SKILL.md).
