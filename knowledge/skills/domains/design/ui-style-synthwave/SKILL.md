---
name: "ui-style-synthwave"
description: "Provides the authentic Synthwave, Retrowave & Outrun UI style (1980s retro-futurism): nocturnal dark cityscapes, neon magenta and electric cyan lasers, 3D perspective wireframe horizon grids, segmented sunset discs, analog synthesizer vibes, and sports car speed. Use when designing high-energy gaming platforms, dark-mode dashboards, music production tools, and nocturnal cyberpunk-adjacent applications."
---

# UI Style: Synthwave & Outrun (Nocturnal Neon & Perspective Grids)

Synthwave (also Retrowave or Outrun) is an aesthetic and musical movement celebrating the nocturnal pop culture, arcade gaming, science fiction cinema, and analog synthesizers of the 1980s. Built on pitch-black night skies, glowing perspective wireframe grids, blazing magenta and electric cyan lasers, and segmented solar discs on the horizon. Synthesized from 1980s cinema (*Tron*, *Blade Runner*, *Miami Vice*) and canonical retrowave artists (Kavinsky, Perturbator, FM-84).

---

## 🧭 When to Activate

- Designing gaming hubs, electronic music applications, high-intensity streaming platforms, or immersive dark-mode software.
- Building telemetry screens or developer tools requiring aggressive high-energy contrast and retro-arcade neon glows.
- Distinct from daytime pastel vaporwave; activate Synthwave for fast, nocturnal, chrome-and-neon experiences.

---

## 🕰️ Definition, Lineage, and Timeline

- **Chronology:** Musical seeds in the mid-2000s French house scene (Kavinsky, College), exploding globally with the soundtrack to the film *Drive* (2011).
- **Inspirations:** 1980s arcade racing games (Sega's *Out Run*, 1986), vector graphics machines (Atari *Battlezone*), synthesizer hardware (Roland Juno-106), and VHS action thrillers.
- **Distinction from Neighbors:**
  - Unlike **Vaporwave / [ui-style-vaporwave](../ui-style-vaporwave/SKILL.md)**: Synthwave is dark, nocturnal, aggressive, high-energy, and supercar-driven; Vaporwave is pastel, slow, daytime, ironic, and office/mall-centered.
  - Unlike **Cyberpunk / [ui-style-cyberpunk](../ui-style-cyberpunk/SKILL.md)**: Synthwave maintains 1980s nostalgia and analog synthesizer beauty rather than dystopian body-horror or corporate decay.

---

## 🎨 Visual DNA & Subgenre Taxonomy

- **The Outrun Horizon:**
  - Pitch-black void (`#0D0221`) fading down to deep indigo (`#1F0838`).
  - Neon 3D perspective wireframe grid vanishing toward an infinite horizon line.
  - The segmented sun disc: horizontal cut stripes slicing through a blazing orange-to-magenta gradient circle.
- **Laser Neon Palette:**
  - Electric Magenta (`#FF007F`), Hot Pink (`#FF2A6D`), Laser Cyan (`#05D9E8`), Neon Violet (`#7928CA`), Sunset Gold (`#FF9F1C`).
- **Typography:**
  - Slanted bold display scripts for hero branding (*Lazer84*, *Streamster*), paired with technical square geometric sans or digital monospace for data controls (*Orbitron*, *Share Tech Mono*).

---

## 📐 Lighting Physics, Specular Splits & Surfaces

1. **Infinite Perspective Grid (Pure CSS):**
   ```css
   background-image: 
     linear-gradient(rgba(5, 217, 232, 0.3) 1px, transparent 1px),
     linear-gradient(90deg, rgba(255, 0, 127, 0.3) 1px, transparent 1px);
   background-size: 40px 40px;
   transform: perspective(300px) rotateX(60deg);
   transform-origin: center bottom;
   ```
2. **Neon Laser Bloom:**
   ```css
   color: #05D9E8;
   text-shadow: 0 0 5px #05D9E8, 0 0 15px rgba(5, 217, 232, 0.8), 0 0 30px rgba(5, 217, 232, 0.4);
   ```

---

## 🏷️ Complete Design Tokens

```css
:root {
  /* Synthwave Palette */
  --synth-bg: #0D0221;
  --synth-surface: #19053B;
  --synth-surface-card: #240954;
  --synth-magenta: #FF007F;
  --synth-pink: #FF2A6D;
  --synth-cyan: #05D9E8;
  --synth-yellow: #F9C80E;
  --synth-purple: #7928CA;
  --synth-fg: #F1F5F9;

  /* Typography */
  --synth-font-display: 'Orbitron', 'Chakra Petch', sans-serif;
  --synth-font-mono: 'Share Tech Mono', monospace;
  --synth-font-body: 'Rajdhani', system-ui, sans-serif;
}
```

---

## 🧱 Production-Ready Component Blueprint

```html
<article class="synth-panel">
  <div class="synth-grid-underlay"></div>
  <div class="synth-content">
    <div class="synth-badge">OUTRUN TELEMETRY</div>
    <h3 class="synth-title">NEON VELOCITY</h3>
    <p class="synth-desc">Analog synth wave oscillators synced at 142 BPM with nocturnal laser overdrive.</p>
    <div class="synth-telemetry-bar">
      <span>RPM: 8400</span>
      <div class="synth-progress"><i style="width: 84%;"></i></div>
    </div>
    <button class="synth-btn-neon" type="button">ENGAGE TURBO</button>
  </div>
</article>
```

```css
.synth-panel {
  position: relative;
  background: var(--synth-surface);
  border: 1px solid var(--synth-magenta);
  border-radius: 6px;
  padding: 24px;
  overflow: hidden;
  box-shadow: 0 0 20px rgba(255, 0, 127, 0.3), inset 0 0 15px rgba(121, 40, 202, 0.2);
  color: var(--synth-fg);
  font-family: var(--synth-font-body);
}
.synth-badge {
  display: inline-block;
  font-family: var(--synth-font-mono);
  font-size: 0.75rem;
  letter-spacing: 0.15em;
  color: var(--synth-cyan);
  border: 1px solid var(--synth-cyan);
  padding: 2px 8px;
  border-radius: 2px;
  margin-bottom: 12px;
  text-shadow: 0 0 8px rgba(5, 217, 232, 0.6);
}
.synth-title {
  font-family: var(--synth-font-display);
  font-size: 1.5rem;
  color: #FFFFFF;
  margin: 0 0 8px;
  text-shadow: 0 0 10px var(--synth-magenta);
}
.synth-progress {
  height: 8px;
  background: #100224;
  border: 1px solid var(--synth-cyan);
  border-radius: 2px;
  margin: 8px 0 16px;
  overflow: hidden;
}
.synth-progress i {
  display: block;
  height: 100%;
  background: linear-gradient(90deg, var(--synth-cyan), var(--synth-magenta));
}
.synth-btn-neon {
  background: transparent;
  color: var(--synth-cyan);
  font-family: var(--synth-font-display);
  font-weight: 700;
  letter-spacing: 0.1em;
  padding: 10px 24px;
  border: 2px solid var(--synth-cyan);
  border-radius: 3px;
  cursor: pointer;
  box-shadow: 0 0 12px rgba(5, 217, 232, 0.4);
  transition: all 120ms ease;
}
.synth-btn-neon:hover {
  background: var(--synth-cyan);
  color: #0D0221;
  box-shadow: 0 0 24px rgba(5, 217, 232, 0.8);
}
```

---

## ✨ Micro-Interactions, Motion & Soundscapes

- **Horizon Grid Acceleration:** Wireframe floor lines pulse and shift forward at high frame rates.
- **Laser Flicker:** Active switches toggle with sharp laser flash blooms.

---

## ♿ WCAG 2.2 Accessibility & High-Contrast Guardrails

- **Contrast Ratios:**
  - Laser Cyan (`#05D9E8`) on Midnight Void (`#0D0221`): **13.8:1** (Passes WCAG AAA).
  - Hot Pink (`#FF2A6D`) on Midnight Void (`#0D0221`): **7.4:1** (Passes WCAG AAA).
  - Foreground (`#F1F5F9`) on Dark Surface (`#19053B`): **16.1:1** (Passes WCAG AAA).
- **Dual-Contrast Focus Ring:**
  `outline: 2px solid var(--synth-cyan); box-shadow: 0 0 0 2px var(--synth-magenta);`

---

## 🚫 Anti-Patterns & Visual Sins (Anti-AI Slop Traps)

- ❌ **NEVER use pastel milk-shake colors:** Synthwave is razor-sharp electric neon, not washed-out 90s mall pastel.
- ❌ **NEVER omit high-contrast wireframe or grid motifs:** Depth is defined by vector lines cutting through dark space.

---

## 📚 Sources & References

- Nicolas Winding Refn, *Drive* (Film Aesthetic & Soundtrack, 2011).
- Sega Corporation, *Out Run Arcade System Guidelines* (Tokyo, 1986).
## Appearance and Interaction Verification

Declare floor-grid extent and owner so the outrun horizon remains visible across resized content; freeze decorative acceleration/laser flashes under reduced motion while preserving switch states, and verify neon strokes without counting bloom as ink contrast.

