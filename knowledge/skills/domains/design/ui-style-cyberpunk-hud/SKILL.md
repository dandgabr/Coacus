---
name: "ui-style-cyberpunk-hud"
description: "Provides the cyberpunk / dark sci-fi HUD UI style (2015-present): cinematic FUI adapted to the web with neon-on-dark panels, scanlines, glow, glitch and telemetry motion, covering Territory Studio lineage, CSS techniques (clip-path chamfers, feTurbulence noise), WCAG 2.3.1 photosensitivity and appropriate audiences. Use when designing gaming, esports, web3 or sci-fi entertainment interfaces."
---

# UI Style: Cyberpunk / Dark Sci-Fi HUD

Web adaptation of cinematic FUI ("fantasy user interfaces"): near-black canvases, neon cyan/magenta/amber accents, chamfered panels, scanlines, glow, glitch and looping telemetry. Canon: Alien → Blade Runner → Minority Report → Iron Man HUDs; the 2015+ web wave rides Territory Studio (The Martian 2015, Blade Runner 2049) and Cyberpunk 2077's yellow/cyan identity (2020). Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Designing games, esports/streaming, web3, dev-tool or nightlife interfaces.
- Building scanlines, glow, chromatic aberration and glitch effects in CSS.
- Auditing flicker/glow designs against photosensitivity and contrast rules.

---

## 🕰️ Definition and Timeline

- Cinematic FUI canon: Alien (1979), Blade Runner (1982), Minority Report (2002), Iron Man (2008–2013). Territory Studio's BR2049 work (100+ assets, 15 sets, with Denis Villeneuve's art department) is the modern reference; Cyberpunk 2077 (released Dec 10, 2020) made the palette a web cliché (CyberCore CSS self-describes as BR2049/CP2077-inspired).
- Scholarship: Chris Noessel's scifiinterfaces.com (since 2012) and Shedroff & Noessel's *Make It So* (2012).

---

## 🎨 Visual DNA

- **Type:** techno/monospace faces (Orbitron, Share Tech Mono, Rajdhani class), small sizes, heavy letter-spacing.
- **Color:** near-black bases (`#05060a`–`#0a0e1a`) + neon accents; BR2049 palette logic is story-graded (utilitarian white-on-dark vs Wallace pure black/white).
- **Shapes:** chamfered corners, angular panels, HUD corner brackets, 1px hairlines, circular gauges.
- **Depth/light:** glow (bloom), holographic translucency, volumetric gradients.
- **Texture:** scanlines, CRT vignette, static noise, deliberate degradation (Territory aged K's spinner UI to signal disrepair).
- **Iconography:** crosshairs, telemetry readouts, waveforms, multilingual signage; **layout:** HUD framing, data-dense corner clusters.

---

## 🖱️ Interaction and Motion

- Boot/decryption typing reveals, glitch-slice transitions, radar sweeps, pulsing target locks, typewriter terminal text, looping telemetry micro-animations, parallax hologram depth, audio-reactive canvases.

---

## 🛠️ Implementation Notes

```css
.scanlines::after {
  content: ""; position: absolute; inset: 0; pointer-events: none;
  background: repeating-linear-gradient(0deg, rgb(0 0 0 / .25) 0 1px, transparent 1px 3px);
}
```

- Glow: stacked `text-shadow`/`box-shadow` or `filter: drop-shadow()` in the accent hue; chromatic aberration: dual pseudo-element copies offset ±2px in red/cyan (or SVG `feOffset`+`feBlend`); glitch: `clip-path` slicing on pseudo-elements (Codrops technique); chamfers: `clip-path: polygon(...)`; noise: `feTurbulence`; typing: `steps()` animations.

---

## ♿ Accessibility

- Flicker/glitch must respect WCAG 2.3.1 (no more than three flashes/second); glow smears glyph edges for low vision even at passing contrast; scanline overlays cut effective contrast of everything beneath; monospace body text reads measurably slower; dark-on-dark borders can fail 1.4.11 (3:1 non-text); constant telemetry motion requires `prefers-reduced-motion` gates.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** games, esports/streaming, crypto/web3, dev tools, nightlife/music, sci-fi entertainment marketing.
- **Avoid:** healthcare, banking, government, long-form editorial, older/general audiences.

---

## ⚠️ Pitfalls

- Total saturation — every neon grid looks alike; stacked-blur performance cost; genre drift into generic "neon sci-fi" strips the dystopian core; movie HUDs are famously anti-usable when transplanted into real product UI (the *Make It So* critique).

---

## 📚 Sources

- Territory Studio, "Blade Runner 2049" case study, 2018 — https://territorystudio.com/project/blade-runner-2049/
- Chris Noessel, Sci-fi Interfaces — https://scifiinterfaces.com/about/
- Nathan Shedroff & Christopher Noessel, *Make It So*, Rosenfeld Media, 2012 — http://rosenfeldmedia.com/books/make-it-so/
- HUDS+GUIS — https://www.hudsandguis.com/
- Codrops, CSS Glitch Effect — https://tympanus.net/Tutorials/CSSGlitchEffect/index3.html
- CYBERCORE CSS — https://sebyx07.github.io/cybercore-css/
- Typeset in the Future — https://typesetinthefuture.com/

---

## 🔗 Integration with Other Skills

- Sibling styles: [ui-style-y2k-revival](../ui-style-y2k-revival/SKILL.md), [ui-style-dark-mode-first](../ui-style-dark-mode-first/SKILL.md), [ui-style-acid-anti-design](../ui-style-acid-anti-design/SKILL.md).
- Newer sibling styles: [ui-style-terminal-tui](../ui-style-terminal-tui/SKILL.md), [ui-style-glitch](../ui-style-glitch/SKILL.md), [ui-style-vaporwave-synthwave](../ui-style-vaporwave-synthwave/SKILL.md).
- Related -punk styles: [ui-style-cyberpunk](../ui-style-cyberpunk/SKILL.md).
