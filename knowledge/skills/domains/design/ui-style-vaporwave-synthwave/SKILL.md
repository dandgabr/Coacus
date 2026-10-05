---
name: "ui-style-vaporwave-synthwave"
description: "Provides the vaporwave and synthwave UI styles (2010-present): two related nostalgia aesthetics, pastel-digital vaporwave and neon-night synthwave/outrun, covering shared retro-digital motifs, the two distinct palettes, glow and grid construction, scanline and sun motifs, contrast-safe neon and reduced-motion handling. Use when designing music, gaming, event or brand surfaces with 1980s-90s internet or arcade nostalgia."
---

# UI Style: Vaporwave and Synthwave (Retro-Digital Nostalgia)

One family, two palettes. Vaporwave is the ironic, pastel, 1990s-corporate-internet side; synthwave (retrowave/outrun) is the earnest, neon, 1980s-night-drive side. Both are internet aesthetics built on idealized memory, not period-accurate design. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Designing music, game, streaming, event or merch surfaces that borrow 1980s-90s digital nostalgia.
- Choosing between the soft vaporwave palette and the high-energy synthwave palette for one brief.
- Building glow, grid and sun motifs without breaking contrast or motion accessibility.

---

## 🕰️ Definition and Timeline

- **Vaporwave:** an internet microgenre of the early 2010s, an ironic offshoot of chillwave; blueprint works are Daniel Lopatin's *Chuck Person's Eccojams Vol. 1* (2010), James Ferraro's *Far Side Virtual* (2011) and Macintosh Plus's *Floral Shoppe* (2011). Visuals mix 1990s web design, glitch art, anime, Greco-Roman busts, Memphis shapes and early 3D renders.
- **Synthwave:** emerged in the mid-to-late 2000s, fed by *Grand Theft Auto: Vice City* (2002) nostalgia, *Blade Runner* (1982), Carpenter, Vangelis and Jarre scores; *Drive* (2011, Kavinsky's "Nightcall") brought it mainstream. Two visual strands: retrowave (80s album covers) and outrun (after Sega's 1986 *Out Run*).
- **Difference from neighbors:** [ui-style-y2k-revival](../ui-style-y2k-revival/SKILL.md) recreates optimistic 2000s product gloss; [ui-style-cyberpunk](../ui-style-cyberpunk/SKILL.md) is dystopian and data-dense. Vaporwave/synthwave is nostalgic and scenic: horizons, suns, grids, statues, not instrument panels.

---

## 🎨 Visual DNA

- **Vaporwave palette:** pastel pink `#FF9CDA`, teal `#01CDFE`, lavender `#B967FF`, mint `#05FFA1`, on soft gradients or checkerboard; lighter, flatter, hazy.
- **Synthwave palette:** near-black indigo `#120458` / `#1A0B3A`, magenta `#FF2A6D`, cyan `#05D9E8`, sunset orange-to-yellow sun; saturated, dark, glowing.
- **Type:** vaporwave: wide serif or Japanese katakana accents, Windows 95 system fonts, fullwidth letterspacing; synthwave: chrome-gradient italic display, wide geometric sans (Orbitron, Audiowide), script neon signs. One display face plus a clean body face.
- **Motifs:** perspective grid floor, striped sun, palm silhouettes, marble busts, wireframe 3D, scanlines, VHS tracking noise, window chrome.
- **Depth:** glow (`text-shadow` and `box-shadow` in the accent color), horizon gradients; no heavy drop shadows.

---

## 🖱️ Interaction and Motion

- Slow ambient loops: grid scrolling toward the horizon, sun pulse, gentle float on statues; 8-20s cycles, never frantic.
- Hover: glow intensifies, color shifts along the palette (0.2s); optional brief chromatic-offset flicker on headings.
- Vaporwave may add faux OS windows and cursor-trail touches; keep them decorative and skippable.

---

## 🛠️ Implementation Notes

```css
:root {
  --bg: #140a2e; --ink: #f4eaff;
  --magenta: #ff2a6d; --cyan: #05d9e8; --sun: #ffb347;
}
body { background: linear-gradient(#140a2e 55%, #3a0d5c); color: var(--ink); }
.grid-floor {
  background:
    linear-gradient(var(--magenta) 1px, transparent 1px) 0 0 / 100% 40px,
    linear-gradient(90deg, var(--magenta) 1px, transparent 1px) 0 0 / 40px 100%;
  transform: perspective(300px) rotateX(60deg);
  animation: scroll 12s linear infinite;
}
.neon { color: var(--ink); text-shadow: 0 0 6px var(--cyan), 0 0 18px var(--magenta); }
@keyframes scroll { to { background-position-y: 40px; } }
@media (prefers-reduced-motion: reduce) { .grid-floor { animation: none; } }
```

- Keep glow as decoration over a solid readable text color; never use the neon hue itself for body copy.
- Build suns and grids with CSS gradients or inline SVG; avoid heavy video loops.

---

## ♿ Accessibility

- Neon on dark usually passes 4.5:1 (1.4.3), but pastel-on-pastel vaporwave often fails: test every pair; set body text near-white on deep indigo or near-black on pastel.
- Glow and low-alpha outlines can hide control boundaries; keep a 3:1 border for inputs and buttons (1.4.11) and a solid focus ring (2.4.7, 2.4.11).
- Looping grids, scanlines and flicker: provide pause (2.2.2), honor `prefers-reduced-motion`, and never flash more than three times per second (2.3.1).
- Fullwidth or katakana decorative text needs `aria-hidden` or a plain-text equivalent; do not rely on color alone for state (1.4.1).

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** music releases, indie games, nightlife and festival pages, retro-tech brands, portfolios, lo-fi/streaming experiences.
- **Caution:** SaaS marketing (hero only), e-commerce (brand zone, not checkout).
- **Avoid:** finance, healthcare, government, dense documentation, long-form reading.

---

## ⚠️ Pitfalls

- Mixing both palettes without intent (muddy, neither ironic nor energetic).
- Genre clichés (statue + palm + grid on every page) read as template; vary one element.
- Heavy blur and glow layers hurt paint performance on low-end devices.
- Unlicensed 80s/90s brand imagery, logos or anime stills in the collage.

---

## 📚 Sources

- Wikipedia, "Vaporwave" (Wikimedia Foundation), accessed 2026 — https://en.wikipedia.org/wiki/Vaporwave
- Wikipedia, "Synthwave" (Wikimedia Foundation), accessed 2026 — https://en.wikipedia.org/wiki/Synthwave
- Wikipedia, "Outrun" disambiguation (Wikimedia Foundation), accessed 2026 — https://en.wikipedia.org/wiki/Outrun
- MDN, "prefers-reduced-motion" (Mozilla), accessed 2026 — https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
- W3C, "Web Content Accessibility Guidelines (WCAG) 2.2" (W3C), 2023 — https://www.w3.org/TR/WCAG22/
- Hex values and font names above are common practice, not taken from a cited source: `unverified` as canonical.

---

## 🔗 Integration with Other Skills

- For conformance discipline, see [web-accessibility-wcag](../../../engineering/practices/web-accessibility-wcag/SKILL.md).
- Sibling styles: [ui-style-y2k-revival](../ui-style-y2k-revival/SKILL.md), [ui-style-cyberpunk](../ui-style-cyberpunk/SKILL.md), [ui-style-retro-computing-pixel](../ui-style-retro-computing-pixel/SKILL.md), [ui-style-glitch](../ui-style-glitch/SKILL.md), [ui-style-atompunk](../ui-style-atompunk/SKILL.md).
- Related -punk styles: [ui-style-cyberpunk](../ui-style-cyberpunk/SKILL.md).
