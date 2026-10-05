---
name: "ui-style-collage-scrapbook"
description: "Provides the collage, scrapbook and Dadaist photomontage UI style (1912-present): cut-out photographic fragments, torn paper deckles, masking tape, rubber postmarks, ransom-note mixed typography and layered mixed media. Covers Braque/Picasso papier collé, Cabaret Voltaire Dada anti-art, CSS clip-path torn edges and accessibility. Use when designing expressive, subversive, punk, artistic or handcrafted scrapbook surfaces."
---

# UI Style: Collage, Scrapbook & Dadaist Photomontage

Interfaces assembled from cut, pasted, overlapped, and juxtaposed physical fragments: cut-out photographs, torn paper edges, adhesive masking tape, rubber postmarks, stamps, and mixed "ransom-note" typography. Spans the arc from early modernist paper collage (Picasso & Braque, 1912) and Dadaist anti-art protest (Hannah Höch, John Heartfield, 1916) to contemporary personal scrapbooks and subversive cultural zines. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Portfolios, underground culture zines, music labels, fashion lookbooks, and avant-garde art showcases.
- Subversive platforms breaking clean corporate grid conformity through deliberate anti-harmony and tactile grit.
- Translating physical mixed-media art, scrapbooking, or photomontage into interactive digital formats.

---

## 🕰️ Definition and Timeline

- **Modernist Origins (1912):** Braque and Picasso introduced *papier collé*; Picasso's *Still Life with Chair Caning* (1912) pasted oilcloth onto fine art canvas, initiating modern collage.
- **Dadaist Photomontage (1916–1924):** Founded at Cabaret Voltaire (Zurich) amidst WWI. Hannah Höch and John Heartfield invented political photomontage, juxtaposing newspaper clippings, mechanical parts, and ransom-note letterforms to challenge institutional complacency.
- **Contemporary Digital Revival:** Web revival through 2010s zine cultures, post-punk aesthetics, and scrapbooking communities seeking tactile humanity.
- **Difference from neighbors:** Unlike [ui-style-acid-anti-design](../ui-style-acid-anti-design/SKILL.md), which is neon, digital, and 1990s rave-inspired, Collage is analog, physical, paper-based, and tactile. Unlike [ui-style-risograph-zine](../ui-style-risograph-zine/SKILL.md), it is not restricted to spot-color print passes.

---

## 🎨 Visual DNA

- **Cut-Out Imagery:** Photographic subjects isolated with rough, torn, or white-bordered scissors edges.
- **Paper & Stock Variety:** Layered paper backgrounds (aged newsprint `#E8E6E1`, kraft cardboard, graph paper, ledger sheets).
- **Typography:** Anarchic typographic pairings (the ransom-note effect: pairing Didot serifs, gothic blackletter, monospaced typewriter fonts, and bold grotesques in single titles).
- **Torn Edges & Tape:** Adhesive masking tape strips, paperclips, postal stamps, and torn paper deckles (`clip-path: polygon(...)`).
- **Controlled Tilts:** Every container is slightly tilted (`transform: rotate(-1.5deg)` to `+2deg`), simulating papers laid casually on a desk.
- **Depth:** Layered physical drop shadows (`box-shadow: 6px 6px 0 rgba(0,0,0,0.25)`).

---

## 🖱️ Interaction and Motion

- **Tactile Paper Lift:** Hovering a fragment lifts it slightly (`transform: translateY(-4px) rotate(0deg)`), easing the tilt as if lifted by hand.
- **Jitter & Stop-Motion:** Step-timed entrances (10–12 fps) for hero stickers and stamps.
- Under `prefers-reduced-motion: reduce`, disable all random rotational wiggles and stop-motion shifts, keeping static overlapping arrangements.

---

## 🛠️ Implementation Notes

```css
:root {
  --scrap-bg: #e8e6e1;
  --scrap-paper: #f4efe4;
  --scrap-ink: #1a1a1a;
  --scrap-accent: #b82020;
}
body { background: var(--scrap-bg); color: var(--scrap-ink); }
.scrap-card {
  background: var(--scrap-paper);
  padding: 1.5rem;
  transform: rotate(-1.5deg);
  box-shadow: 6px 6px 0 rgba(0, 0, 0, 0.2);
  transition: transform 0.2s ease-out, box-shadow 0.2s ease-out;
}
.scrap-card:hover {
  transform: translateY(-4px) rotate(0deg);
  box-shadow: 8px 12px 0 rgba(0, 0, 0, 0.25);
}
.torn-edge {
  clip-path: polygon(0 2%, 5% 0, 15% 3%, 28% 1%, 42% 3%, 60% 0, 78% 2%, 92% 0, 100% 2%,
                     100% 98%, 90% 100%, 75% 97%, 55% 100%, 35% 97%, 15% 100%, 0 97%);
}
```

- Implement ransom-note headings using semantic HTML spans with distinct font classes, ensuring screen readers parse the heading smoothly as a continuous sentence.
- Use `filter: drop-shadow()` rather than `box-shadow` on clipped items so the shadow wraps around the irregular alpha edges.

---

## ♿ Accessibility

- **Reading Order (WCAG 1.3.2):** Visual shuffling and overlapping positions must strictly preserve logical DOM reading order.
- **Focus Visibility:** Rotated and clipped containers must not clip the browser focus ring (WCAG 2.4.7).
- **Contrast Integrity:** Ensure ransom-note text fragments maintain at least 4.5:1 contrast against their paper backgrounds.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** Artist portfolios, indie record labels, creative publishing, exhibition microsites, and counterculture commentary.
- **Avoid:** Online banking, medical diagnosis portals, legal documentation, and enterprise administrative tools.

---

## 📚 Sources

- Tristan Tzara, *Dada Manifesto*, 1918.
- Hannah Höch, *Photomontages and Collages*, 1919–1934.
- Dawn Ades, *Photomontage*, Thames & Hudson, 1986.
- W3C, *Web Content Accessibility Guidelines 2.2* — https://www.w3.org/TR/WCAG22/

---

## 🔗 Integration with Other Skills

- Sibling expressive styles: [ui-style-risograph-zine](../ui-style-risograph-zine/SKILL.md), [ui-style-hand-drawn-sketch](../ui-style-hand-drawn-sketch/SKILL.md), [ui-style-constructivism-propaganda](../ui-style-constructivism-propaganda/SKILL.md).
