---
name: "ui-style-retro-computing-pixel"
description: "Provides the retro computing / pixel UI style (1980s aesthetics, web revival 2010s-present): bitmap fonts, restricted palettes, dithering, integer-scaled pixel art and classic OS chrome, covering nearest-neighbor scaling, palette constraints, 98.css-style bevels and accessible pixel typography. Use when designing game-adjacent, nostalgic or indie surfaces, retro OS metaphors or pixel-art interfaces."
---

# UI Style: Retro Computing / Pixel

Visible pixels as identity: bitmap type, tiny palettes, dithering and the chrome of 8/16-bit machines and 1990s desktop GUIs. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Designing game sites, indie tools, portfolios, nostalgia campaigns or pixel-art product UI.
- Recreating classic-OS windows, dialogs and bevels (Windows 9x, early Mac) on the web.
- Scaling bitmap art and fonts crisply across densities.

---

## 🕰️ Definition and Timeline

- Pixel art is digital art in which pixels are the only building block, with visible pixels and restricted palettes; the term was first published in 1982 (Goldberg and Flegal, Xerox PARC), practice dating to SuperPaint (1972).
- Arcade era (Space Invaders 1978, Pac-Man 1980), demoscene in the 1990s, indie resurgence in the 2010s (Undertale 2015, Stardew Valley 2016).
- Difference from [ui-style-y2k-revival](../ui-style-y2k-revival/SKILL.md): Y2K is glossy, chrome and translucent late-90s/2000s futurism; this style is hardware-constrained 1-bit to 16-bit pixels and early GUI bevels. Versus [ui-style-terminal-tui](../ui-style-terminal-tui/SKILL.md): this style draws pixels and windows, not text cells.

---

## 🎨 Visual DNA

- **Type:** bitmap or pixel fonts (Press Start 2P, VT323, Silkscreen, Pixelify Sans) used at native multiples; bitmap fonts look best at native size and degrade when scaled non-integrally.
- **Palette:** hardware-style limits (Game Boy 4 greens, C64 16, EGA 16, Mac 1-bit); define as tokens, 4-16 colors total.
- **Rendering:** hard edges, no anti-aliased gradients; dithering patterns to fake tone; 1px outlines.
- **Chrome:** raised/sunken 2px bevels, title bars, dithered desktop backgrounds, dialog boxes, pixel cursors and icons on 16/32px grids.
- **Layout:** integer coordinates; grid from the base pixel unit (e.g. 4px "art pixel").

---

## 🖱️ Interaction and Motion

- Frame-stepped animation (`steps()`), 2-4 frame sprite cycles, 8-12 fps feel; no easing.
- Press states shift bevel and offset 1 art-pixel; hover swaps palette entries.
- Sound optional and opt-in; boot-sequence or loading bars as brief brand moments, skippable.

---

## 🛠️ Implementation Notes

```css
:root { --px: 4px; --c0: #0f380f; --c1: #306230; --c2: #8bac0f; --c3: #9bbc0f; }
.sprite, .pixel-img { image-rendering: pixelated; image-rendering: crisp-edges; }
.pixel-img { width: calc(32px * 4); height: auto; }   /* integer multiple only */
body { font: 16px/1.5 "Silkscreen", monospace; -webkit-font-smoothing: none; }
.win { border: 2px solid #000; box-shadow: inset 2px 2px #fff, inset -2px -2px #808080; background: #c0c0c0; }
.win .btn:active { box-shadow: inset 2px 2px #808080, inset -2px -2px #fff; }
.walk { animation: walk .6s steps(4) infinite; }
@media (prefers-reduced-motion: reduce) { .walk { animation: none; } }
```

- `image-rendering: pixelated` scales to the nearest integer multiple with nearest-neighbor, then smooths remaining distance; `crisp-edges` keeps edges sharp without smoothing. It only affects scaled images.
- Export art at 1x, scale in CSS by whole numbers; pair `devicePixelRatio` changes with integer factors.
- 98.css is a pure stylesheet for Windows 98 recreation and states accessibility as a primary goal: use real `<button>`, labeled inputs, `aria-label` on icon buttons.

---

## ♿ Accessibility

- Pixel fonts at body size hurt legibility; use them for display text and keep body copy in a readable face or at 16px+ with tested contrast (1.4.3, 4.5:1). Palette limits often fail contrast: check each pair.
- 1.4.5 images of text: render real text; pixel text baked into PNG needs an alternative or avoid.
- 1.1.1: alt text for sprites and icons; decorative ones `alt=""`.
- 2.3.1 and 2.2.2: no flashing above three per second; auto-playing sprite loops need a pause control.
- 2.5.8: 16px pixel icons need 24px minimum hit areas.
- `prefers-reduced-motion: reduce`: freeze sprites on a still frame.
- Bevels alone do not meet 1.4.11 (3:1) unless the edge colors contrast; add a solid outline.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** games, indie dev portfolios, creative coding, retro hardware communities, nostalgia campaigns.
- **Caution:** SaaS marketing (novelty fades), data-dense apps.
- **Avoid:** health, finance and public services; audiences with low vision needs for long text.

---

## ⚠️ Pitfalls

- Non-integer scaling producing uneven pixel sizes and shimmer.
- Mixing pixel densities (a 1px-art logo beside 4px-art icons).
- Blurry bitmap fonts from default smoothing; photo textures breaking the spell.
- Nostalgia as the only idea: window metaphors that make real tasks slower.

---

## 📚 Sources

- "Pixel art" (Wikipedia) — https://en.wikipedia.org/wiki/Pixel_art
- MDN, "image-rendering" (Mozilla) — https://developer.mozilla.org/en-US/docs/Web/CSS/image-rendering
- "Computer font" (Wikipedia; bitmap font scaling) — https://en.wikipedia.org/wiki/Bitmap_font
- 98.css project, "98.css" — https://jdan.github.io/98.css/ (created by Jordan Scales per GIGAZINE, "CSS '98.css'", Apr 23, 2020 — https://gigazine.net/gsc_news/en/20200423-98-css/)
- W3C, "Understanding SC 2.3.1: Three Flashes or Below Threshold" — https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold.html

---

## 🔗 Integration with Other Skills

- For conformance discipline, see [web-accessibility-wcag](../../../engineering/practices/web-accessibility-wcag/SKILL.md).
- Sibling styles: [ui-style-y2k-revival](../ui-style-y2k-revival/SKILL.md), [ui-style-terminal-tui](../ui-style-terminal-tui/SKILL.md), [ui-style-skeuomorphism](../ui-style-skeuomorphism/SKILL.md), [ui-style-indie-web-revival](../ui-style-indie-web-revival/SKILL.md), [ui-style-glitch](../ui-style-glitch/SKILL.md).
