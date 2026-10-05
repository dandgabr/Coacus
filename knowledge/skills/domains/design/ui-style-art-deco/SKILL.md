---
name: "ui-style-art-deco"
description: "Provides the Art Deco UI style (1910s-1930s lineage, revived for the web): symmetrical geometric ornament, sunbursts, chevrons and stepped forms in gold, black and jewel tones, covering tokens, line-art and SVG pattern construction, high-contrast display type, ceremonial motion and contrast pitfalls of metallic palettes. Use when designing luxury, hospitality, cinema, jazz-age or premium brand surfaces that need glamour with structure."
---

# UI Style: Art Deco

The glamour of the 1920s-30s: bold geometry, symmetry, stepped and radiating forms, rich materials (gold, black, ivory, chrome) and fine linework. On the web it reads as framed layouts, ornamental dividers, metallic accents and elegant display type. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Designing luxury, hotel, cocktail bar, cinema, theatre, jewelry or heritage-premium brands.
- Building event or editorial pages with a jazz-age or "Great Gatsby" tone.
- Adding structured ornament to a restrained layout without sliding into kitsch.

---

## 🕰️ Definition and Timeline

- Art Deco (short for Arts decoratifs) appeared in Paris in the 1910s and flourished in the 1920s and early 1930s; the name spread after the 1925 International Exhibition of Modern Decorative and Industrial Arts in Paris (the label "Art deco" itself appeared in print only in 1966).
- Influences: Cubism, Fauvism, Vienna Secession. Materials: ebony, ivory, chrome, stainless steel. Landmarks: Chrysler Building, Empire State Building; Miami Beach holds the largest concentration of Art Deco architecture (per Wikipedia).
- Depression-era evolution: Streamline Moderne, with curves and speed lines.
- **Differences:** [ui-style-bauhaus](../ui-style-bauhaus/SKILL.md) rejects ornament and prizes function; Art Deco embraces ornament, luxury and symmetry. [ui-style-art-nouveau-arts-crafts](../ui-style-art-nouveau-arts-crafts/SKILL.md) is organic and whiplash-curved; Art Deco is geometric and machine-age. [ui-style-editorial-archive-luxury](../ui-style-editorial-archive-luxury/SKILL.md) is restrained typography-led luxury; Art Deco is ornament-led.

---

## 🎨 Visual DNA

- **Palette:** black or deep navy / emerald / burgundy base, gold `#C9A227`-ish and champagne accents, ivory text; metallics rendered as flat gold or subtle linear gradient, not bevel.
- **Motifs:** sunburst/fan, chevron, zigzag, stepped (ziggurat) corners, concentric arcs, scalloped shells, fluting; inline gold hairlines (1-2px) doubling borders.
- **Type:** high-contrast display sans or caps with geometric forms (Poiret One, Limelight, Josefin Sans, Playfair Display for pairing), wide letterspacing, all caps headings; condensed tall sans for marquee text.
- **Layout:** centered, symmetrical, framed; vertical emphasis (tall columns, stepped skyline silhouettes); ornamental dividers between sections.
- **Depth:** flat ornament and thin outlines; glow only as a gold edge highlight.

---

## 🖱️ Interaction and Motion

- Ceremonial, measured motion: curtain-style reveals, sunburst rays that fan out once, gold line drawing along borders (`stroke-dashoffset`), 400-700ms ease-out.
- Hover brightens gold or extends an underline from the center outward; avoid bounce.
- Ornament animates once on entry, not as a loop.

---

## 🛠️ Implementation Notes

```css
:root { --ink: #0e0e12; --ivory: #f5ecd7; --gold: #c9a227; --emerald: #0f3d34; }
body { background: var(--ink); color: var(--ivory); font-family: "Josefin Sans", sans-serif; }
h1 { font-family: "Poiret One", serif; letter-spacing: .18em; text-transform: uppercase; color: var(--gold); }
.frame { border: 1px solid var(--gold); outline: 1px solid var(--gold); outline-offset: 6px; padding: 2rem; }
.sunburst {
  background: repeating-conic-gradient(from 0deg at 50% 100%, var(--gold) 0 4deg, transparent 4deg 12deg);
  mask: linear-gradient(to top, #000, transparent 85%);
}
.btn { border: 1px solid var(--gold); color: var(--gold); background: transparent; letter-spacing: .12em; }
.btn:hover { background: var(--gold); color: var(--ink); transition: background .25s ease-out; }
.btn:focus-visible { outline: 3px solid var(--ivory); outline-offset: 4px; }
@media (prefers-reduced-motion: reduce) { .btn { transition: none; } }
```

- Build repeated patterns (chevrons, fans, scallops) as inline SVG `<pattern>` or CSS gradients; keep files small.
- Symmetry: use one centered axis and mirrored columns; mirror ornament with CSS `transform: scaleX(-1)` on decorative pseudo-elements only.

---

## ♿ Accessibility

- Gold on black passes comfortably; gold on ivory or champagne fails 4.5:1 (1.4.3): test every metallic pair, and use dark ink text on light gold fills.
- Hairline gold borders, thin outlines and decorative linework are small non-text signals: keep 3:1 where they identify controls (1.4.11) and provide a thicker focus ring (2.4.7, 2.4.11).
- Wide letterspacing and all caps lower readability: keep body in sentence case, normal tracking; support text spacing overrides (1.4.12).
- Entrance and line-draw animations: honor `prefers-reduced-motion`, offer pause for any loop (2.2.2) and avoid motion that triggers on every scroll (2.3.3).
- Ornament is `aria-hidden`; meaning never lives in a pattern alone (1.4.1).

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** hotels, restaurants, cocktail and jazz venues, theatres and cinemas, wedding and gala invitations, jewelry, premium spirits, heritage fintech accent pages.
- **Caution:** SaaS marketing (hero and section dividers only), long forms.
- **Avoid:** minimalist, utilitarian or playful youth brands; dense data apps; contexts where gold-on-dark is hard to read in sunlight.

---

## ⚠️ Pitfalls

- Gatsby cliché overload: confetti, champagne glass, every border ornate.
- Fake-metal skeuomorphic gradients and bevels that clash with the flat, crisp original.
- Asymmetry or organic curves slipping in and diluting the geometric discipline.
- Heavy ornamental assets hurting LCP; unlicensed Deco display fonts.

---

## 📚 Sources

- Wikipedia, "Art Deco" (Wikimedia Foundation), accessed 2026 — https://en.wikipedia.org/wiki/Art_Deco
- Wikipedia, "Bauhaus" (Wikimedia Foundation), accessed 2026, used for the contrast with functional modernism — https://en.wikipedia.org/wiki/Bauhaus
- MDN, "prefers-reduced-motion" (Mozilla), accessed 2026 — https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
- W3C, "Web Content Accessibility Guidelines (WCAG) 2.2" (W3C), 2023 — https://www.w3.org/TR/WCAG22/
- María Villanueva Fernández and Héctor García-Diego Villarías, "Art Deco: 100 Years Since the Paris Exhibition That Revolutionized Modern Design" (JSTOR Daily, from The Conversation), May 29, 2025 — https://daily.jstor.org/art-deco-100-years-since-the-paris-exhibition-that-revolutionized-modern-design/ (exhibition opened 28 April 1925; geometric motifs and low-relief decoration; the term "Art Deco" dates from 1966).
- Hex values and font pairings are practice suggestions: `unverified`.

---

## 🔗 Integration with Other Skills

- For conformance discipline, see [web-accessibility-wcag](../../../engineering/practices/web-accessibility-wcag/SKILL.md).
- Sibling styles: [ui-style-editorial-archive-luxury](../ui-style-editorial-archive-luxury/SKILL.md), [ui-style-bauhaus](../ui-style-bauhaus/SKILL.md), [ui-style-art-nouveau-arts-crafts](../ui-style-art-nouveau-arts-crafts/SKILL.md), [ui-style-mid-century-modern](../ui-style-mid-century-modern/SKILL.md), [ui-style-atompunk](../ui-style-atompunk/SKILL.md).
- Related -punk styles: [ui-style-dieselpunk](../ui-style-dieselpunk/SKILL.md).
