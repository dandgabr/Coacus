---
name: "ui-style-pop-art-halftone"
description: "Provides the Pop Art and Ben-Day dot halftone UI style: exaggerated comic book halftone patterns, heavy black ink outlines, primary CMYK palettes, speech bubbles and onomatopoeia punch. Use when building playful, comic-inspired or pop culture web experiences."
---

# UI Style: Pop Art & Ben-Day Halftone

Inspired by 1960s Pop Art (Roy Lichtenstein, Andy Warhol) and vintage comic book commercial printing processes. Defined by oversized Ben-Day dot screens, bold black ink outlines, primary print ink colors, and expressive graphic callouts.

---

## 🧭 When to Activate

- Playful e-commerce drops, comic and gaming platforms, creative agencies, and bold consumer apps.
- Interfaces seeking unmistakable retro-comic book energy and vibrant optimism.

---

## 🎨 Visual DNA

- **Palette:** Process CMYK: Cyan (`#00AEEF`), Magenta (`#EC008C`), Process Yellow (`#FFF200`), solid Black (`#000000`), and crisp White (`#FFFFFF`).
- **Type:** Comic display caps (Bangers, Komika, Action Man), heavy condensed grotesques, and bold slab serifs.
- **Patterns:** Ben-Day dot halftone gradients, diagonal comic speed lines, action starbursts, and speech bubble containers.
- **Borders:** Heavy 3px–5px solid black outlines with offset solid black drop shadows.

---

## 🛠️ Implementation Notes

```css
.halftone-bg {
  background: radial-gradient(#000 15%, transparent 16%) 0 0 / 12px 12px;
  background-color: #fff200;
}
.comic-bubble {
  border: 4px solid #000;
  border-radius: 20px;
  box-shadow: 6px 6px 0 #000;
  background: #ffffff;
}
```

---

## ♿ Accessibility

- Avoid animated movement on large Ben-Day dot backgrounds to prevent visual vertigo or optical triggers.
- Ensure text placed within comic bubbles satisfies WCAG AA (black text on white or bright yellow bubbles achieves > 10:1 ratio).
