---
name: "ui-style-split-screen-dualism"
description: "Provides the split-screen dualism and asymmetric polarity UI style: 50/50 dual vertical canvas, contrasting color themes, synchronized scroll choreography and polarized storytelling. Use when comparing two worlds, products, personas or thematic narratives."
---

# UI Style: Split-Screen Dualism & Asymmetric Polarity

Dividing the viewport vertically into two distinct, communicating halves (often light vs. dark, analog vs. digital, problem vs. solution). The two sides interact dynamically, with pinned scrolling, alternating content beats, or cursor-driven cross-boundary transitions.

---

## 🧭 When to Activate

- Comparative product landings (e.g. Creator vs. Enterprise), before/after showcases, dual-narrative brand storytelling.
- Creating dramatic compositional tension between two complementary or opposing concepts.

---

## 🎨 Visual DNA

- **Layout:** Strict 50/50 vertical division (or asymmetric 60/40 golden cut), with a razor-sharp vertical meridian border.
- **Palette:** Inverted complementary duality: Left = Crisp White / Charcoal; Right = Deep Obsidian / Electric Accent.
- **Choreography:** Synchronized vertical scroll where one side moves while the other pins, or dual parallax scrolling at differing speeds.

---

## 🛠️ Implementation Notes

```css
.split-screen-layout {
  display: flex;
  min-height: 100vh;
}
.split-side-left {
  flex: 1;
  background: #ffffff;
  color: #111111;
  padding: 4rem;
}
.split-side-right {
  flex: 1;
  background: #0f1115;
  color: #f1f3f5;
  padding: 4rem;
}
```

---

## ♿ Accessibility

- Ensure seamless responsive breakdown on mobile screens (stacking left and right gracefully into sequential vertical blocks).
- Logical DOM tab order must follow semantic document reading flow regardless of visual side-by-side positioning.
