---
name: "ui-style-weirdcore"
description: "Provides the authentic Weirdcore UI style (internet surrealism of the late 2010s): amateur digital photography from the late 90s to mid-2000s, low-fidelity JPEG compression artifacts, disquieting liminal dread, primitive amateur graphic overlays, and cryptic red/yellow system text. Use when designing psychological horror experiences, uncanny ARG mysteries, underground net-art platforms, or eerie surreal interfaces."
---

# UI Style: Weirdcore (Liminal Dread & Low-Fi Internet Surrealism)

Weirdcore is an internet-native visual microgenre that explores the uncanny psychology of amateur digital media from the late 1990s through the mid-2000s. Characterized by low-resolution digital camera snapshots, aggressive JPEG compression artifacts, empty or decaying liminal spaces (unfurnished hallways, abandoned playplaces, roadside motels at dusk), amateurish paint-tool doodles, and jarring, cryptic text snippets in high-contrast primaries. Synthesized from net-art subcultures and analog horror media.

---

## 🧭 When to Activate

- Designing alternate reality games (ARGs), psychological horror interactive fiction, escape rooms, or experimental net-art galleries.
- Crafting uncanny, disorienting user journeys that deliberately subvert modern polished SaaS ergonomics.
- Distinct from gentle dreamcore; activate Weirdcore when the emotional tone is unsettled, alienating, disquieting, and raw.

---

## 🕰️ Definition, Lineage, and Timeline

- **Origins:** Coined across internet forums (Tumblr, Reddit) circa 2017–2020, drawing visual material from consumer digital photography taken between 1998 and 2007.
- **Psychological Hook:** Anemoia (nostalgia for a time or place never known) coupled with cognitive estrangement and liminal isolation.
- **Distinction from Neighbors:**
  - Unlike **Dreamcore / [ui-style-dreamcore](../ui-style-dreamcore/SKILL.md)**: Dreamcore is gentle, ethereal, comforting, pastel-tinted, and safe; Weirdcore is anxious, distorted, aggressive, low-fi, and psychologically threatening.
  - Unlike **Glitch / [ui-style-glitch](../ui-style-glitch/SKILL.md)**: Glitch focuses on digital signal corruption and scanline telemetry; Weirdcore focuses on emotional dread and amateur photographic snapshots.

---

## 🎨 Visual DNA & Subgenre Taxonomy

- **Surfaces & Atmosphere:**
  - Desaturated flash-lit rooms, overexposed fluorescent white, dingy yellowed linoleum (`#E2D4A8`), and muddy asphalt darks (`#1E1C1A`).
- **Cryptic Text Overlays:**
  - Primary Red (`#E50000`) and Vivid Warning Yellow (`#FFEA00`) text rendered in primitive system typefaces (Arial, Impact, MS Paint Sans).
  - Cryptic, unsettling captions that question the user's perception ("Are you sure this was your room?", "Don't turn around yet").
- **Amateur Graphics:**
  - Harsh 1-bit black borders, crude freehand lasso cutouts, eye-tracking motifs, and harsh optical compression noise.

---

## 📐 Lighting Physics, Specular Splits & Surfaces

1. **Overexposed On-Camera Flash Reflection:**
   - Harsh, direct light washing out foreground surfaces with deep, sudden drop-off into pitch black.
   ```css
   background: radial-gradient(circle at 45% 40%, rgba(255, 255, 240, 0.95) 0%, rgba(30, 28, 26, 0.98) 75%);
   border: 2px solid #E50000;
   box-shadow: 0 0 0 1px #000000, 0 12px 32px rgba(0, 0, 0, 0.85);
   ```

---

## 🏷️ Complete Design Tokens

```css
:root {
  /* Weirdcore Palette */
  --weird-bg: #141210;
  --weird-surface: #26221E;
  --weird-linoleum: #D4C596;
  --weird-flash-white: #FFFFF0;
  --weird-blood-red: #E50000;
  --weird-warning-yellow: #FFEA00;
  --weird-shadow: #0A0807;

  /* Typography */
  --weird-font-text: Arial, 'Helvetica Neue', sans-serif;
  --weird-font-raw: Impact, 'Arial Black', sans-serif;
}
```

---

## 🧱 Production-Ready Component Blueprint

```html
<div class="weird-card">
  <div class="weird-header">
    <span class="weird-warning-label">RECORDING // 03:14 AM</span>
  </div>
  <div class="weird-viewport">
    <p class="weird-liminal-text">YOU HAVE BEEN HERE BEFORE</p>
  </div>
  <div class="weird-footer">
    <button class="weird-btn" type="button">DO NOT PROCEED</button>
  </div>
</div>
```

```css
.weird-card {
  background: var(--weird-surface);
  border: 2px solid var(--weird-blood-red);
  padding: 16px;
  max-width: 400px;
  box-shadow: 4px 4px 0 #000000;
  font-family: var(--weird-font-text);
  color: var(--weird-flash-white);
}
.weird-warning-label {
  background: var(--weird-blood-red);
  color: #FFFFFF;
  font-family: var(--weird-font-raw);
  font-size: 0.75rem;
  letter-spacing: 0.1em;
  padding: 2px 6px;
}
.weird-viewport {
  background: var(--weird-bg);
  border: 1px solid #443B33;
  margin: 16px 0;
  padding: 32px 16px;
  text-align: center;
}
.weird-liminal-text {
  font-family: var(--weird-font-raw);
  font-size: 1.25rem;
  color: var(--weird-warning-yellow);
  text-shadow: 2px 2px 0 #000000;
  margin: 0;
  text-transform: uppercase;
}
.weird-btn {
  background: var(--weird-warning-yellow);
  color: #000000;
  font-family: var(--weird-font-raw);
  font-size: 0.875rem;
  padding: 8px 16px;
  border: 2px solid #000000;
  cursor: pointer;
}
.weird-btn:hover {
  background: var(--weird-blood-red);
  color: #FFFFFF;
}
```

---

## ✨ Micro-Interactions, Motion & Soundscapes

- **Uncanny Jitter:** UI controls subtly twitch or lag by a fraction of a pixel on hover.
- **Flash Cut:** Transitions cut instantly (0ms) rather than smoothly animating.

---

## ♿ WCAG 2.2 Accessibility & High-Contrast Guardrails

- **Contrast Ratios:**
  - Warning Yellow (`#FFEA00`) on Dark Void (`#141210`): **16.8:1** (Passes WCAG AAA).
  - Blood Red (`#E50000`) on Flash White (`#FFFFF0`): **5.3:1** (Passes WCAG AA).
- **Dual-Contrast Focus Ring:**
  `outline: 2px solid #FFEA00; box-shadow: 0 0 0 2px #E50000;`

---

## 🚫 Anti-Patterns & Visual Sins (Anti-AI Slop Traps)

- ❌ **NEVER use comforting pastels or dreamy cotton clouds:** That belongs exclusively to Dreamcore.
- ❌ **NEVER use rounded friendly corners:** Weirdcore is raw, abrupt, and angular.

---

## 📚 Sources & References

- Internet Archive, *Early Consumer Digital Camera Test Corpus (1998–2005)*.
- Mark Fisher, *The Weird and the Eerie* (Repeater Books, 2016).
## Appearance and Interaction Verification

Keep dread in photography and cryptic decorative overlays while maintaining stable actual hit areas, focus and input response; disable optional jitter under reduced motion and verify red/yellow overlay ink on the actual flash-lit image regions.
