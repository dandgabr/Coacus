---
name: "ui-style-dadaism-montage"
description: "Provides the Dadaist anti-art and collage UI style (1916-1924 revival): anarchic typography, ransom-note mixed letterforms, distressed newsprint, misaligned photomontage and deliberate anti-harmony. Use when creating subversive artistic, punk or experimental web applications."
---

# UI Style: Dadaism & Anti-Art Montage

Rooted in the Cabaret Voltaire and the Zurich/Berlin Dada movements of 1916 (Hannah Höch, John Heartfield, Tristan Tzara, Raoul Hausmann). Rejects bourgeois aesthetic conformity through chaotic photomontage, ransom-note mixed typography, torn paper edges, rubber stamp marks, and nonsensical semantic juxtaposition. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Experimental art showcases, zines, underground cultural platforms, subversive music labels, or conceptual portfolios.
- Breaking standard grid predictability through purposeful, thought-provoking disorientation.
- Interfaces challenging digital polish and sanitized corporate perfection.

---

## 🕰️ Definition and Timeline

- **Origins:** Founded in Zurich in 1916 amidst the horrors of WWI. Dadaists responded to institutionalized madness with deliberate absurdity, inventing photomontage (Höch and Heartfield) and phonetic poetry.
- **Philosophy:** Anti-art (*anti-kunst*). A direct challenge to the idea that design must serve harmonious commerce. Embraces chance operations, collage, and disruptive visual noise.
- **Difference from neighbors:** Unlike [ui-style-acid-anti-design](../ui-style-acid-anti-design/SKILL.md), which is 1990s rave-techno, digital, and neon, Dadaism is early 20th-century analog, physical, paper-based, and tactile. Unlike [ui-style-collage-scrapbook](../ui-style-collage-scrapbook/SKILL.md), which is nostalgic and cute, Dada is politically sharp, absurd, and provocative.

---

## 🎨 Visual DNA

- **Palette:** Distressed newsprint gray (`#E8E6E1`), archival charcoal ink (`#1A1A1A`), aged book yellow (`#DCD3B8`), offset with sharp collisions of postal ink red (`#B82020`) and utilitarian cardboard brown (`#8A7356`).
- **Type:** Mixed typographic scales and typefaces within single sentences (the "ransom note" effect: combining heavy gothic blackletter, elegant Didot serif, grotesque sans, and monospaced typewriter letters).
- **Collage & Textures:** Cut-out photographic edges, torn paper deckles, adhesive masking tape, rubber postmark stamps, halftone newsprint clippings, and intentionally tilted containers (`transform: rotate(-2deg)`).
- **Depth:** Physical layered paper overlap with rough cutout drop shadows (`box-shadow: 6px 6px 0 rgba(184, 32, 32, 0.4)`).

---

## 🖱️ Interaction and Motion

- Jitter on hover: interactive elements tilt unpredictably (`transform: rotate(calc(var(--rand-rot, 2) * 1deg))`).
- Tactile paper lift: cards appear physically stuck down with masking tape; hover lifts one corner slightly.
- Under `prefers-reduced-motion: reduce`, disable all random rotational jitter.

---

## 🛠️ Implementation Notes

```css
#stage[data-style="dadaism-montage"] {
  --bg: #e8e6e1;
  --surface: #dfdbd0;
  --fg: #1a1a1a;
  --accent: #b82020;
  --accent-fg: #ffffff;
  --border: #1a1a1a;
  --radius: 0;
  --font-body: 'Times New Roman', serif;
  --font-display: 'Courier New', monospace;
  background-color: var(--bg);
}

#stage[data-style="dadaism-montage"] .card {
  background: var(--surface);
  border: 2px dashed var(--border);
  box-shadow: 8px 8px 0 rgba(184, 32, 32, 0.5);
  transform: rotate(-1.5deg);
}
```

---

## ♿ Accessibility

- **DOM semantics:** Ransom-note typography must be implemented using semantic HTML text (not flattened images) so screen readers read content smoothly.
- **Contrast compliance:** High contrast (> 9:1) between dark ink and aged newsprint ensures solid legibility.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** Independent publishers, underground arts initiatives, zines, punk music hubs, and satirical commentary.
- **Avoid:** Banking, corporate intranets, medical portals, and high-frequency productivity apps.

---

## 📚 Sources

- Tristan Tzara, *Dada Manifesto*, 1918.
- Hannah Höch, *Cut with the Kitchen Knife Dada through the Last Weimar Beer-Belly Cultural Epoch of Germany*, 1919.
- Dawn Ades, *Photomontage*, Thames & Hudson, 1986.

---

## 🔗 Integration with Other Skills

- Sibling avant-garde styles: [ui-style-constructivism-propaganda](../ui-style-constructivism-propaganda/SKILL.md), [ui-style-collage-scrapbook](../ui-style-collage-scrapbook/SKILL.md), [ui-style-acid-anti-design](../ui-style-acid-anti-design/SKILL.md).
