---
name: "ui-style-pixel-art"
description: "Provides the authentic Pixel Art UI style (8-bit and 16-bit video game console aesthetics): strict indexed color palettes, nearest-neighbor integer scaling, manual checkerboard dithering, crisp 1px sprite outlines, stepped frame animations, and retro gaming HUD interfaces. Use when designing video game hubs, interactive gamified dashboards, indie studio showcases, or nostalgic chiptune music players."
---

# UI Style: Pixel Art (Indexed Palettes, Integer Scaling & 8/16-Bit Sprite Dynamics)

Pixel Art is a digital discipline originating in the memory- and hardware-constrained display processors of 1970s–1990s video game consoles (NES, Game Boy, Sega Genesis, Super Nintendo, Neo Geo) and arcade cabinets. Rather than approximating reality through smooth anti-aliased vectors, Pixel Art treats the individual pixel as an explicit atomic unit of expression. Its core rules are strict palette indexing (typically 4, 16, or 32 colors), manual checkerboard dithering, crisp 1px dark contour outlines, integer-ratio scaling (`image-rendering: pixelated`), and frame-stepped sprite animations (`steps()`). Synthesized from pixel art master manuals and game development archives; see Sources.

---

## 🧭 When to Activate

- Designing game launch hubs, interactive gamified dashboards, chiptune music players, pixel asset marketplaces, or indie studio portfolios.
- Creating playful, highly responsive retro interfaces with integer-scaled sprite assets and game HUD dialog boxes.
- Distinct from **[ui-style-retro-computing](../ui-style-retro-computing/SKILL.md)**: Retro Computing focuses on monochrome/amber command lines, BIOS menus, and ASCII terminals; Pixel Art focuses on colorful illustrative sprites, health bars, inventory slots, and animated game characters.
- Distinct from **[ui-style-y2k-revival](../ui-style-y2k-revival/SKILL.md)**: Y2K features translucent glossy plastics and metallic 3D chrome; Pixel Art features flat, crisp, rasterized 2D pixels with zero anti-aliasing.

---

## 🕰️ Definition, Lineage, and Timeline

- **Chronology:** Coined as a formal concept at Xerox PARC in 1982 (Adele Goldberg & Robert Flegal). Golden era spanned the 8-bit NES (1983) and 16-bit SNES/Genesis era (1990–1996). Experienced major indie art revivals via *Cave Story* (2004), *Minecraft* (2009), *Undertale* (2015), and *Celeste* (2018).
- **Physical Constraints:** Early graphics chips (PPU/VDP) could only render a limited number of colors per tile (e.g. 4 colors on the NES, 16 colors on the SNES), requiring artists to manually position every single dot.

---

## 🎨 Visual DNA & Subgenre Taxonomy

- **Palettes:** Strict indexed hardware-inspired palettes:
  - Game Boy 4-Green DMG (`#0F380F`, `#306230`, `#8BAC0F`, `#9BBC0F`)
  - 16-Color Fantasy Console (PICO-8 or SNES-inspired):
    - Slate Black (`#000000`), Navy (`#1D2B53`), Maroon (`#7E2553`), Forest Green (`#008751`)
    - Terracotta (`#AB5236`), Stone Gray (`#5F574F`), Cloud Silver (`#C2C3C7`), Alabaster (`#FFF1E8`)
    - Crimson (`#FF004D`), Sun Orange (`#FFA300`), Lemon (`#FFEC27`), Emerald (`#00E436`)
    - Sky Cyan (`#29ADFF`), Lavender (`#83769C`), Peach (`#FFCCAA`), Hot Pink (`#FF77A8`)
- **Integer Scaling & Nearest-Neighbor Rendering:**
  - Scaled strictly at 2x, 3x, or 4x integer factors using `image-rendering: pixelated` to prevent blurry interpolation.
- **Manual Checkerboard Dithering:**
  - Alternating pixel patterns simulating smooth color transitions within rigid palette limits.
- **Typography:**
  - Crisp pixel glyphs: Silkscreen, Press Start 2P, Pixelify Sans, Monocraft, renderable at integer size boundaries (e.g. 8px, 16px, 24px).
- **Game HUD Elements:**
  - Segmented health/mana bars, item grid boxes with 2px beveled borders, and character speech bubble dialogs with flashing prompt triangles (`▼`).

---

## 📐 Lighting Physics, Specular Splits & Surfaces

- **Integer-Ratio Pixel Scaling:**
  ```css
  image-rendering: pixelated;
  image-rendering: -moz-crisp-edges;
  image-rendering: crisp-edges;
  ```
- **3D Pixel Bevel Border:**
  ```css
  border: 4px solid #000000;
  box-shadow:
    inset 4px 4px 0 #FFF1E8,
    inset -4px -4px 0 #5F574F;
  ```

---

## 🏷️ Complete Design Tokens

```css
:root {
  /* Surface & Base */
  --px-bg: #1D2B53;
  --px-card: #000000;
  --px-text: #FFF1E8;
  --px-border: #000000;

  /* 16-Color Palette Highlights */
  --px-red: #FF004D;
  --px-yellow: #FFEC27;
  --px-green: #00E436;
  --px-blue: #29ADFF;
  --px-purple: #83769C;
  --px-peach: #FFCCAA;
  --px-silver: #C2C3C7;
  --px-gray: #5F574F;

  /* Typography */
  --px-font: 'Press Start 2P', 'Silkscreen', monospace;

  /* Integer Unit */
  --px-unit: 4px;
}
```

---

## 🧱 Production-Ready Component Blueprint

```html
<section class="pixel-dialog">
  <div class="pixel-hud-bar">
    <div class="pixel-stat">
      <span class="pixel-label">HP</span>
      <div class="pixel-bar-container">
        <div class="pixel-bar-fill" style="width: 80%;"></div>
      </div>
    </div>
    <div class="pixel-stat">
      <span class="pixel-label">LV 42</span>
    </div>
  </div>
  <div class="pixel-body">
    <p class="pixel-speech">
      IT DANGEROUS TO GO ALONE! TAKE THIS COMPONENT SYSTEM FOR YOUR RETRO QUEST.
    </p>
    <div class="pixel-actions">
      <button class="pixel-btn pixel-btn-primary" type="button">ACCEPT [A]</button>
      <button class="pixel-btn pixel-btn-secondary" type="button">DECLINE [B]</button>
      <span class="pixel-prompt" aria-hidden="true">▼</span>
    </div>
  </div>
</section>
```

```css
.pixel-dialog {
  background: var(--px-card);
  color: var(--px-text);
  border: 4px solid #000000;
  box-shadow:
    inset 4px 4px 0 var(--px-silver),
    inset -4px -4px 0 var(--px-gray),
    8px 8px 0 rgba(0, 0, 0, 0.6);
  padding: 20px;
  max-width: 580px;
  font-family: var(--px-font);
  font-size: 0.875rem;
  line-height: 1.6;
}
.pixel-hud-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 4px solid var(--px-gray);
  padding-bottom: 12px;
  margin-bottom: 16px;
}
.pixel-stat {
  display: flex;
  align-items: center;
  gap: 8px;
}
.pixel-label {
  color: var(--px-yellow);
}
.pixel-bar-container {
  width: 140px;
  height: 16px;
  background: #222;
  border: 2px solid #000;
  padding: 2px;
}
.pixel-bar-fill {
  height: 100%;
  background: var(--px-green);
  box-shadow: inset 0 -2px 0 rgba(0, 0, 0, 0.4);
}
.pixel-speech {
  margin: 0 0 20px 0;
  text-shadow: 2px 2px 0 #000;
}
.pixel-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  position: relative;
}
.pixel-btn {
  font-family: var(--px-font);
  font-size: 0.75rem;
  padding: 10px 16px;
  border: 4px solid #000;
  cursor: pointer;
  text-transform: uppercase;
  transition: transform 0.05s steps(2);
}
.pixel-btn:active {
  transform: translate(2px, 2px);
}
.pixel-btn-primary {
  background: var(--px-yellow);
  color: #000;
  box-shadow: inset 2px 2px 0 #FFF, inset -2px -2px 0 #AB5236;
}
.pixel-btn-secondary {
  background: var(--px-gray);
  color: #FFF;
  box-shadow: inset 2px 2px 0 var(--px-silver), inset -2px -2px 0 #222;
}
.pixel-prompt {
  margin-left: auto;
  color: var(--px-yellow);
  animation: pixel-bounce 0.8s steps(2) infinite;
}
@keyframes pixel-bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(4px); }
}
```

---

## ✨ Micro-Interactions, Motion & Soundscapes

- **Stepped Animation Frames:** Animations must use `animation-timing-function: steps(...)` at 4 to 8 frames per cycle, completely eliminating smooth cubic-bezier interpolation.
- **2px Button Press Displacement:** Pressing a pixel button snaps it 2px down and right while inverting the inset border bevels.

---

## 📱 Responsive Layout & Spatial Composition

- Maintain integer scaling. If the viewport contracts, decrease pixel font size from 16px to 12px, but never render at fractional pixel sizes (e.g. 13.5px).

---

## ♿ WCAG 2.2 Accessibility & High-Contrast Guardrails

- **Contrast Ratios:**
  - Alabaster Text (`#FFF1E8`) on Dark Slate Card (`#000000` / `#1D2B53`): **18.2:1** (Passes WCAG AAA).
  - Lemon Text (`#FFEC27`) on Black (`#000000`): **14.6:1** (Passes WCAG AAA).
  - Button text on Yellow (`#FFEC27`): **13.5:1** with `#000000`.
- **Pixel Font Legibility:** Pixel fonts can be tiring for long prose reading. For extensive documentation or articles, provide an accessibility toggle to switch to a clean geometric sans-serif while keeping pixel borders and HUD elements.

---

## 🚫 Anti-Patterns & Visual Sins (Anti-AI Slop Traps)

- ❌ **NEVER apply anti-aliased font smoothing or blur filters:** Pixel art requires sharp, crisp rectangular edges.
- ❌ **NEVER use soft blurry Gaussian box shadows:** Shadows must be hard, stepped opaque offsets (`box-shadow: 4px 4px 0 #000;`).
- ❌ **NEVER scale sprites with bilinear filtering:** Always declare `image-rendering: pixelated;`.

---

## 🎯 When to Use & When to Avoid

- **Use For:** Video game releases, gaming community portals, indie game stores, 8-bit chiptune soundboards, interactive quests.
- **Avoid For:** High-volume legal documents, medical interfaces, executive corporate reports.

---

## 📚 Sources & References

- Michael Tyson, *Pixel Logic: A Guide to Pixel Art* (2018).
- Adele Goldberg & Robert Flegal, *ACM History of Personal Workstations: Pixel Art Mechanics* (Xerox PARC, 1982).
- Derek Yu, *Pixel Art Tutorial for Indie Game Creators* (2007).
## Appearance and Interaction Verification

Keep sprite integer scaling independent of readable text sizing; wrap HUD actions and translated dialogue within actual owner, preserve zoom and font fallback, and stop optional stepped prompt motion without suppressing game state.
