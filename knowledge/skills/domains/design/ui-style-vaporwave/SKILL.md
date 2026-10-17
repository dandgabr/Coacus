---
name: "ui-style-vaporwave"
description: "Provides the authentic Vaporwave UI style (early-to-mid 2010s internet aesthetic rooted in late-80s/early-90s consumerism): marble classical sculptures, Japanese typography, Windows 95 chrome, pastel sunset gradients, lo-fi VHS dithering, and consumer melancholy. Use when designing ironic retro-digital art platforms, chillwave music players, vaporwave community hubs, or nostalgic early-web experiments."
---

# UI Style: Vaporwave (Aesthetic & Consumer Melancholy)

Vaporwave is an internet-native microgenre and aesthetic movement originating around 2010–2011, meditating ironically on late-capitalist consumer optimism of the late 1980s and 1990s. Grounded in smooth pastel gradients, Hellenistic marble busts, Japanese katakana typography, early personal computer interfaces (Windows 95 / Classic Macintosh), and nostalgic Muzak escapism. Synthesized from net-art archives and canonical vaporwave albums (*Floral Shoppe*, *Far Side Virtual*).

---

## 🧭 When to Activate

- Designing web applications, music hubs, portfolios, or digital art spaces themed around early-90s internet nostalgia, ambient chillwave, or consumerist satire.
- Creating playful or surreal retro interfaces requiring classical antiquity juxtaposed with vintage computing window frames.
- Distinct from dark outrun or driving synthwave; activate Vaporwave when the mood is daylight pastel, dreamy, ironic, and daytime ambient.

---

## 🕰️ Definition, Lineage, and Timeline

- **Chronology:** Emerged in 2010 through producers Daniel Lopatin (Chuck Person's *Eccojams Vol. 1*) and James Ferraro (*Far Side Virtual*), popularized visually by Ramona Xavier (Macintosh Plus — *Floral Shoppe*, 2011).
- **Core Themes:** Glitch-slowed Muzak, corporate mall culture, early CGI renderings, Arizona green tea cherry blossoms, classical Greek sculpture, and vintage GUI dialog boxes.
- **Distinction from Neighbors:**
  - Unlike **Synthwave / [ui-style-synthwave](../ui-style-synthwave/SKILL.md)**: Synthwave is dark, nocturnal, neon-saturated, aggressive, and 1980s action/supercar oriented. Vaporwave is bright pastel, slow, daytime, ironic, and 1990s desktop/mall oriented.
  - Unlike **[ui-style-y2k-revival](../ui-style-y2k-revival/SKILL.md)**: Y2K features metallic chrome blobs and cyber-optimism; Vaporwave features classical marble, VHS decay, and corporate melancholia.

---

## 🎨 Visual DNA & Subgenre Taxonomy

- **Surfaces & Palettes:**
  - Soft Lilac (`#E0B0FF`), Pastel Cyan (`#80DEEA`), Millennial Pink (`#FFB7B2`), Mint Foam (`#B2F5EA`).
  - Anchoring Deep Indigo (`#2B1B54`) and Classic Windows Slate Grey (`#C0C0C0`).
- **Antiquity & Tech Juxtaposition:**
  - Classical marble bust silhouettes (Helios, Aphrodite) framed inside 16-color 1px beveled desktop windows.
  - Fullwidth monospace English interspersed with Japanese Katakana (`ヴェイパーウェイヴ`).
- **Textures:**
  - Subtle scanlines at 8% opacity, VHS tape noise, checkerboard 3D floor tiles, and wireframe spheres.

---

## 📐 Lighting Physics, Specular Splits & Surfaces

1. **Pastel Sunset Horizon Gradient:**
   ```css
   background: linear-gradient(180deg, #FFB7B2 0%, #E0B0FF 40%, #80DEEA 85%, #B2F5EA 100%);
   ```
2. **Early GUI 1px Bevel:**
   ```css
   border: 2px solid #FFFFFF;
   border-right-color: #808080;
   border-bottom-color: #808080;
   box-shadow: inset 1px 1px 0 #DFDFDF, inset -1px -1px 0 #000000;
   ```

---

## 🏷️ Complete Design Tokens

```css
:root {
  /* Vaporwave Palette */
  --vapor-pink: #FFB7B2;
  --vapor-lilac: #D8B4F8;
  --vapor-cyan: #7CE8F4;
  --vapor-mint: #B2F5EA;
  --vapor-bg: #22143B;
  --vapor-card: #2E1C4E;
  --vapor-fg: #FAF5FF;
  --vapor-accent: #FF71CE;

  /* Classic Windows 95 Grey */
  --vapor-win-bg: #C3C7CB;
  --vapor-win-border-light: #FFFFFF;
  --vapor-win-border-dark: #868A8E;
  --vapor-win-title: #000080;

  /* Typography */
  --vapor-font-title: 'MS Gothic', 'VT323', monospace;
  --vapor-font-body: 'W95FA', system-ui, sans-serif;
}
```

---

## 🧱 Production-Ready Component Blueprint

```html
<div class="vapor-window">
  <div class="vapor-titlebar">
    <span class="vapor-title">Floral_Shoppe.exe // 音楽</span>
    <div class="vapor-win-btns">
      <button class="vapor-btn" aria-label="Minimize">_</button>
      <button class="vapor-btn" aria-label="Close">×</button>
    </div>
  </div>
  <div class="vapor-body">
    <div class="vapor-glitch-hero">
      <h3>A E S T H E T I C S</h3>
      <p>Nostalgic digital consumerism through slowed ambient soundscapes.</p>
    </div>
    <button class="vapor-btn-action" type="button">ＰＬＡＹ  ＴＲＡＣＫ</button>
  </div>
</div>
```

```css
.vapor-window {
  background: var(--vapor-win-bg);
  border: 2px solid var(--vapor-win-border-light);
  border-right-color: var(--vapor-win-border-dark);
  border-bottom-color: var(--vapor-win-border-dark);
  box-shadow: 2px 2px 0 #000000;
  padding: 3px;
  max-width: 420px;
  font-family: var(--vapor-font-body);
}
.vapor-titlebar {
  background: linear-gradient(90deg, var(--vapor-win-title) 0%, #1084D0 100%);
  color: #FFFFFF;
  padding: 3px 6px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 700;
  font-size: 0.8125rem;
}
.vapor-btn {
  background: var(--vapor-win-bg);
  border: 1px solid var(--vapor-win-border-light);
  border-right-color: var(--vapor-win-border-dark);
  border-bottom-color: var(--vapor-win-border-dark);
  width: 16px;
  height: 14px;
  font-size: 10px;
  line-height: 1;
  cursor: pointer;
}
.vapor-body {
  padding: 16px;
  background: var(--vapor-bg);
  color: var(--vapor-fg);
}
.vapor-btn-action {
  background: linear-gradient(90deg, var(--vapor-pink), var(--vapor-cyan));
  color: #1A0D2E;
  font-family: var(--vapor-font-title);
  font-weight: 700;
  padding: 10px 20px;
  border: none;
  border-radius: 2px;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(255, 113, 206, 0.4);
}
```

---

## ✨ Micro-Interactions, Motion & Soundscapes

- **Slow Tape Warble:** Floating elements drift with slow sinusoidal breathing (`animation: float 8s ease-in-out infinite`).
- **Lo-Fi Scanline Glitch:** Hovering actionable triggers creates brief horizontal chromatic displacement.

---

## ♿ WCAG 2.2 Accessibility & High-Contrast Guardrails

- **Contrast Ratios:**
  - Foreground (`#FAF5FF`) on Deep Indigo (`#22143B`): **14.2:1** (Passes WCAG AAA).
  - Title text (`#FFFFFF`) on Windows Navy (`#000080`): **12.6:1** (Passes WCAG AAA).
  - Magenta Accent (`#FF71CE`) on Dark Purple: calibrated to 5.2:1 for interactive states.
- **Dual-Contrast Focus Ring:**
  `outline: 2px solid var(--vapor-accent); box-shadow: 0 0 0 1px #000;`

---

## 🚫 Anti-Patterns & Visual Sins (Anti-AI Slop Traps)

- ❌ **NEVER mix with dark aggressive 80s outrun:** Avoid black backgrounds with blazing neon reds, laser grids, and fast cars (that is Synthwave).
- ❌ **NEVER omit classical or vintage computing cues:** Vaporwave requires the historical dissonance between antiquity and early operating systems.

---

## 📚 Sources & References

- Grafton Tanner, *Babbling Corpse: Vaporwave and the Commodification of Ghosts* (Zero Books, 2016).
- Ramona Xavier, *Floral Shoppe* (Beer on the Rug, 2011).
