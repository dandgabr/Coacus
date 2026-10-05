---
name: "ui-style-split-screen-dualism"
description: "Provides the split-screen dualism and asymmetric polarity UI style: 50/50 dual vertical canvas, contrasting color themes, synchronized scroll choreography and polarized storytelling. Use when comparing two worlds, products, personas or thematic narratives."
---

# UI Style: Split-Screen Dualism & Asymmetric Polarity

Dividing the viewport vertically into two distinct, communicating halves (often light vs. dark, analog vs. digital, problem vs. solution, or creator vs. enterprise). The two sides interact dynamically, with pinned scrolling, alternating content beats, or cursor-driven cross-boundary transitions. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Comparative product landings (e.g. Creator vs. Enterprise, Light Mode vs. Dark Mode), before/after showcases, dual-narrative brand storytelling.
- Creating dramatic compositional tension between two complementary or opposing concepts.
- Pacing user journeys where two parallel stories unfold simultaneously.

---

## 🕰️ Definition and Timeline

- **Origins:** Gained massive web popularity in the mid-2010s through award-winning agency portfolios and luxury brand launches (Dropbox 2017 rebrand, Engine Themes).
- **Philosophy:** Dualistic harmony. Rejecting the single linear vertical scroll in favor of dialectical tension: thesis on the left, antithesis on the right, and synthesis through user interaction.
- **Difference from neighbors:** Unlike [ui-style-bento-grid](../ui-style-bento-grid/SKILL.md), which partitions content into many small modular tiles, Split-Screen Dualism divides the primary canvas into two monumental, contrasting hemispheres.

---

## 🎨 Visual DNA

- **Layout:** Strict 50/50 vertical division (or asymmetric 60/40 golden ratio), with a razor-sharp vertical meridian border.
- **Palette:** Inverted complementary duality: Left = Crisp White (`#FFFFFF`) with charcoal text; Right = Deep Obsidian (`#0F1115`) with neon or white text.
- **Typography:** Complementary pairings (e.g. geometric grotesque on the technical side, expressive serif on the human side).
- **Borders & Dividers:** Clean 1px or 2px vertical dividing meridian line.

---

## 🖱️ Interaction and Motion

- Synchronized scroll: one side pins in place while the opposing side scrolls, or both sides scroll in opposing directions.
- Cursor crossover: cursor changes color or shape when crossing the central meridian boundary.
- Responsive collapse: on viewports under 768px, gracefully collapse the dual columns into alternating stacked sections.

---

## 🛠️ Implementation Notes

```css
#stage[data-style="split-screen-dualism"] {
  --bg: #121316;
  --surface: #ffffff;
  --fg: #ffffff;
  --muted: #8c92a4;
  --accent: #ffffff;
  --accent-fg: #121316;
  --border: #282c37;
  --radius: 6px;
  --font-body: 'Space Grotesk', sans-serif;
  --font-display: 'Space Grotesk', sans-serif;
  background-color: var(--bg);
}
```

---

## ♿ Accessibility

- **DOM order:** Logical DOM tab order must follow semantic document reading flow regardless of visual side-by-side positioning.
- **Mobile responsiveness:** Ensure smooth column stacking on mobile screens without horizontal clipping.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** Product comparison pages, dual-service agencies, narrative storytelling, and brand rebrands.
- **Avoid:** Simple blog posts, dense table data dashboards, and multi-step checkout funnels.

---

## 📚 Sources

- Awwwards Site of the Day Collections, *Split Screen Layouts in Contemporary Web*, 2018–2022.
- Vitaly Friedman, *Creative Layouts and Grid Systems*, Smashing Magazine, 2019.

---

## 🔗 Integration with Other Skills

- Sibling layout styles: [ui-style-bento-grid](../ui-style-bento-grid/SKILL.md), [ui-style-broken-grid](../ui-style-broken-grid/SKILL.md), [ui-style-one-page-long-scroll](../ui-style-one-page-long-scroll/SKILL.md).
