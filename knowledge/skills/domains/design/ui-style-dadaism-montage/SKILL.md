---
name: "ui-style-dadaism-montage"
description: "Provides the Dadaist anti-art and collage UI style: anarchic typography, ransom-note letterforms, newsprint texture, misaligned photomontage and deliberate anti-harmony. Use when creating subversive artistic, punk or experimental web applications."
---

# UI Style: Dadaism & Anti-Art Montage

Rooted in the Cabaret Voltaire and the Zurich/Berlin Dada movements of 1916 (Hannah Höch, John Heartfield, Tristan Tzara). Rejects bourgeois aesthetic rules through collage, disjointed typography, mixed letterforms, and nonsensical juxtaposition.

---

## 🧭 When to Activate

- Experimental art showcases, zines, underground cultural platforms, or conceptual portfolio experiences.
- Breaking standard grid predictability through purposeful, thought-provoking disorientation.

---

## 🎨 Visual DNA

- **Palette:** Distressed newsprint gray (`#E8E6E1`), charcoal ink (`#1A1A1A`), aged paper yellow (`#DCD3B8`), with sharp collisions of postal ink red (`#B82020`).
- **Type:** Mixed typographic scales and typefaces within single sentences (ransom note effect: combining serif, sans, blackletter, and monospaced letters).
- **Collage:** Cut-out photograph edges, tape textures, halftone newsprint clippings, ripped edges, and overlapping tilted frames.

---

## 🛠️ Implementation Notes

```css
.ransom-char {
  display: inline-block;
  padding: 2px 4px;
  background: #111;
  color: #fff;
  transform: rotate(calc(var(--rand-rot, 0) * 1deg));
}
.ransom-char:nth-child(even) {
  background: #b82020;
  font-family: serif;
}
```

---

## ♿ Accessibility

- Ransom-style text must be implemented using standard DOM text (never image-only text) so assistive technologies parse content seamlessly.
- Maintain high luminance contrast between letter background chips and glyph colors.
