---
name: "ui-style-glitch"
description: "Provides the glitch UI style (mid-1990s-present): deliberate digital error as aesthetic, covering RGB channel splits, clipped slice displacement, datamosh and compression artifacts, CSS pseudo-element glitch text and photosensitivity-safe motion. Use when designing music, art, gaming, cyber or experimental surfaces that stage corruption, or when auditing glitch effects for seizure and legibility risk."
---

# UI Style: Glitch

Error as ornament: channel separation, displaced slices, scanline tears, compression blocks and stuttering type, staged on purpose. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Designing music, game, art, security-brand, cyber-culture or editorial-experimental surfaces.
- Adding brief glitch transitions or hover effects to an otherwise stable interface.
- Auditing glitch animation for photosensitive-seizure and readability risk.

---

## 🕰️ Definition and Timeline

- Glitch art is an art movement that uses digital or analog errors for aesthetic purposes; the term emerged in the mid-1990s from experimental electronic music, then VJs and visual artists. JODI's net.art broke website layouts early; methods include databending, datamoshing (removing I-frames from compressed video), misalignment, hardware failure and compression distortion. The first GLI.TC/H conference was held in Chicago in 2010.
- Rosa Menkman's "Glitch Studies Manifesto" (2009/2010) frames noise and artifacts as material and critique of "noiseless" media.
- Web craft: Chris Coyier's CSS-Tricks "Glitch Effect on Text / Images / SVG" (Sep 8, 2014) stacks pseudo-element copies with clipped, animated offsets.
- Difference from [ui-style-cyberpunk-hud](../ui-style-cyberpunk-hud/SKILL.md): cyberpunk is a futuristic HUD genre; glitch is a technique and attitude (corruption) usable in any genre. Versus [ui-style-acid-anti-design](../ui-style-acid-anti-design/SKILL.md): glitch simulates malfunction; acid is chaotic composition without that fiction. Versus [ui-style-kinetic-typography](../ui-style-kinetic-typography/SKILL.md): glitch type is broken, not choreographed.

---

## 🎨 Visual DNA

- **Channel split:** red/cyan (or magenta/cyan) offsets of 2-6px via `text-shadow` or layered copies.
- **Slices:** horizontal bands clipped and shifted (`clip-path: inset()`), tearing and scan lines.
- **Artifacts:** JPEG/DCT blocks, pixel sorting, datamosh smear, dead-pixel noise, posterized color.
- **Type:** monospace, condensed grotesk or blackletter; random character swaps (`#@%`).
- **Palette:** near-black base, acid RGB accents; or pure white with chromatic fringing.
- **Rhythm:** stable most of the time; glitch is the exception that gives it meaning.

---

## 🖱️ Interaction and Motion

- Short bursts: 80-300ms on hover, route change or loading; idle state calm.
- `steps()` timing and uneven keyframes; randomness from several offset animations with coprime durations.
- Never let glitch hide state changes: success, error and navigation must settle into a clear static frame.

---

## 🛠️ Implementation Notes

```css
.glitch { position: relative; color: #fff; }
.glitch::before, .glitch::after {
  content: attr(data-text); position: absolute; inset: 0; pointer-events: none;
}
.glitch::before { color: #0ff; transform: translate(-2px, 0); clip-path: inset(10% 0 60% 0); }
.glitch::after  { color: #f0f; transform: translate(2px, 0);  clip-path: inset(55% 0 10% 0); }
.glitch:is(:hover, :focus-visible)::before { animation: slice-a .3s steps(6) 1; }
.glitch:is(:hover, :focus-visible)::after  { animation: slice-b .3s steps(5) 1; }
@keyframes slice-a { 20% { clip-path: inset(30% 0 40% 0); } 60% { clip-path: inset(70% 0 5% 0); } }
@keyframes slice-b { 25% { clip-path: inset(5% 0 80% 0); }  70% { clip-path: inset(45% 0 30% 0); } }
@media (prefers-reduced-motion: reduce) {
  .glitch::before, .glitch::after { animation: none; display: none; }
}
```

- Pseudo-element text is not announced when `content` repeats; keep the real text in the DOM node and the visual copies decorative (generate copies in JS with `aria-hidden="true"` if screen-reader duplication appears).
- Prefer `transform`, `opacity` and `clip-path`; avoid animating layout. Cap SVG `feTurbulence`/`feDisplacementMap` areas for cost.
- Shader or canvas glitch: provide a static fallback.

---

## ♿ Accessibility

- 2.3.1 Three Flashes or Below Threshold (Level A): no more than three flashes in any one second, or stay below the general and red flash thresholds; fast full-screen strobing is the main glitch hazard.
- 2.2.2 Pause, Stop, Hide: any glitch lasting over 5 seconds and auto-starting needs a control; loops should end.
- 2.3.3 Animation from Interactions (AAA): offer a way to disable motion triggered by interaction.
- `prefers-reduced-motion: reduce`: remove displacement and flicker; keep static chromatic fringe if legible.
- 1.4.3 and 1.4.12: split colors and clipped copies lower effective contrast; keep the main text layer solid at 4.5:1 and readable when effects stop.
- Glitched text must remain real text (1.4.5); never glitch form labels, errors or legal copy.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** album and game sites, art portfolios, security and hacker brands, 404 and transition moments, festival identities.
- **Caution:** SaaS marketing hero (one accent moment, not constant).
- **Avoid:** healthcare, finance, government, education, anything where visual instability reads as a real failure.

---

## ⚠️ Pitfalls

- Constant effect that causes fatigue, seizures or vestibular discomfort.
- Users mistaking staged glitches for real bugs (and support tickets).
- Heavy filters and canvas loops draining battery on mobile.
- Clichéd RGB-split on every heading, killing hierarchy.

---

## 📚 Sources

- "Glitch art" (Wikipedia) — https://en.wikipedia.org/wiki/Glitch_art
- Rosa Menkman, "Glitch Studies Manifesto", 2009/2010 — https://beyondresolution.info/Glitch-Studies-Manifesto (the page labels the short version "2009/2010"; an extended version appeared in the Video Vortex reader, 2011)
- Chris Coyier, "Glitch Effect on Text / Images / SVG" (CSS-Tricks), Sep 8, 2014 — https://css-tricks.com/glitch-effect-text-images-svg/
- W3C, "Understanding SC 2.3.1: Three Flashes or Below Threshold" — https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold.html
- MDN, "prefers-reduced-motion" (Mozilla) — https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion

---

## 🔗 Integration with Other Skills

- For conformance discipline, see [web-accessibility-wcag](../../../engineering/practices/web-accessibility-wcag/SKILL.md).
- Sibling styles: [ui-style-cyberpunk-hud](../ui-style-cyberpunk-hud/SKILL.md), [ui-style-acid-anti-design](../ui-style-acid-anti-design/SKILL.md), [ui-style-kinetic-typography](../ui-style-kinetic-typography/SKILL.md), [ui-style-retro-computing-pixel](../ui-style-retro-computing-pixel/SKILL.md), [ui-style-vaporwave-synthwave](../ui-style-vaporwave-synthwave/SKILL.md).
