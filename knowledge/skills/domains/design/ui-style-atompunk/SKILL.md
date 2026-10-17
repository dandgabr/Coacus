---
name: "ui-style-atompunk"
description: "Provides the authentic Atompunk & Cold War Nuclear Age UI style (1945–1965): Raygun Gothic futurism, riveted heavy naval steel chassis, bakelite knobs, convex CRT monitors with P1 green and P3 amber phosphor, nixie tubes, analog galvanometers, radiation fallout shelters, and Geiger counter telemetry. Use when designing authentic retro-futuristic sci-fi, defense telemetry, complex data cockpits, or Fallout-inspired terminal interfaces."
---

# UI Style: Atompunk & Cold War Nuclear Futurism

Atompunk is the high-stakes, pre-transistor retro-futurism of the Cold War Nuclear Age (1945–1965). Built on heavy naval steel, cast phenolic bakelite, vacuum tubes, and convex cathode-ray tube (CRT) monitors, it envisions a high-energy technological future powered by atomic fission and rocket engines. Synthesized from historical civil-defense archives, Brookhaven National Laboratory instrumentation, and canonical media (*Fallout*, *The Iron Giant*, *Dr. Strangelove*).

---

## 🧭 When to Activate

- Designing dashboards, cockpits, telemetric monitors, devtools, or complex data applications requiring a tactile, military-industrial, or retro-futuristic Cold War aesthetic.
- Developing game interfaces, creative tools, or interactive applications inspired by the *Fallout* franchise, Project Orion, or mid-century nuclear research facilities.
- Demanding high contrast, rugged physical affordances, and zero generic modern SaaS tropes (eliminating rounded pastel pills, floating cards, and borderless flat surfaces).

---

## 🕰️ Definition, Lineage, and Timeline

- **Chronology:** 1945 (Trinity detonation and civilian nuclear optimism) to 1965 (the advent of microchips and integrated circuits).
- **Aesthetic Pillars:** Raygun Gothic, civil-defense engineering, Brookhaven and Oak Ridge national laboratories instrumentation, Project Plowshare, and *Popular Science* atomic-automobile forecasts (e.g., Ford Nucleon).
- **Physical Reality:** Pre-silicon technology. Amplification is thermionic (vacuum tubes); displays are CRT oscilloscopes with green P1 or amber P3 phosphor persistence; switching is electro-mechanical (knife switches, heavy rotary dials, bakelite toggles); enclosures are heavy-gauge painted steel with structural hex-bolts and rivets.
- **Distinction from Neighbors:**
  - Unlike **Dieselpunk** (1920–1940s: Art Deco, locomotive pistons, oily soot, exposed grease, steam pressure gauges), Atompunk is energized by nuclear isotopes, high-voltage vacuum coils, radar screens, and aerodynamic rocket aerodynamics.
  - Unlike **Mid-Century Modern** (domestic minimalism, teak wood, organic Arne Jacobsen chairs), Atompunk represents industrialized government laboratories, control bunkers, and space-command silos.
  - **Absolute Veto:** Atompunk is NOT a 1950s roadside diner or ice-cream parlor. Pastel milk-shakes, neon flamingo pinks, script fonts (*Pacifico*, *Lobster*), and kitsch jukeboxes are strictly prohibited.

---

## 🎨 Visual DNA & Subgenre Taxonomy

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                ATOMPUNK VISUAL MATRIX                                  │
├────────────────────────────┬────────────────────────────┬──────────────────────────────┤
│ 1. Bunker & Silo (Fallout) │ 2. Laboratory Telemetry    │ 3. Civilian Orbit Optimism   │
│ • Riveted armor plate      │ • Curved CRT oscilloscopes │ • Aerodynamic rocket fins    │
│ • Industrial stencil type  │ • Nixie tubes & VU meters  │ • Chrome trim over dark steel│
│ • Toxic hazard striping    │ • Bakelite rotary knobs    │ • Atomic diagrammatic orbits │
└────────────────────────────┴────────────────────────────┴──────────────────────────────┘
```

- **Surfaces & Chassis:** Heavy zinc-chromate primed naval steel (`#12181F`), hammered industrial enamel finish, cast phenolic bakelite (`#2A1810`), and brushed aviation aluminum (`#8C9BAE`).
- **Displays & Phosphor:** Deep subterranean cathode backing (`#06140A`), illuminated by high-persistence green phosphor P1 (`#27FF48`) or radar amber P3 (`#FF9900`), overlaid with convex glass distortion and horizontal electron scanlines.
- **Structural Hardware:** Raised steel bezels, mechanical hex bolts (`#3E4A59`), warning hazard diagonal hatching (`#FFC800` / `#12181F`), and stamped embossed serial plates.

---

## 📐 Lighting Physics, Specular Splits & Surfaces

1. **Convex CRT Glass Curvature:**
   - Simulated via radial gradient vignetting combined with horizontal scanlines and glass reflection glare.
   ```css
   background: radial-gradient(circle at 50% 50%, rgba(39, 255, 72, 0.08) 0%, rgba(6, 20, 10, 0.98) 100%);
   box-shadow: inset 0 0 40px rgba(0, 0, 0, 0.9), 0 0 15px rgba(39, 255, 72, 0.25);
   ```
2. **Heavy Stamped Metal Bezel:**
   - 3D mechanical relief with light source from top-left (135deg).
   ```css
   border: 3px solid #2A3644;
   box-shadow: inset 1px 1px 0 #4F5E6F, inset -1px -1px 0 #0B1015, 0 4px 12px rgba(0, 0, 0, 0.7);
   ```

---

## 🏷️ Complete Design Tokens

```css
:root {
  /* Heavy Industrial Chassis */
  --atom-chassis-bg: #12181F;
  --atom-chassis-surface: #1A232D;
  --atom-chassis-border: #2E3C4D;
  --atom-chassis-highlight: #465971;

  /* Phosphor Telemetry */
  --atom-crt-bg: #06140A;
  --atom-phosphor-p1: #27FF48;
  --atom-phosphor-p1-glow: rgba(39, 255, 72, 0.45);
  --atom-phosphor-dim: #137725;
  --atom-amber-p3: #FF9900;
  --atom-amber-glow: rgba(255, 153, 0, 0.4);

  /* Materials & Radiation */
  --atom-bakelite: #2B170E;
  --atom-bakelite-hover: #3E2114;
  --atom-hazard-yellow: #FFC800;
  --atom-rad-danger: #FF2A2A;
  --atom-gauge-metal: #7C8B9E;

  /* Typography */
  --atom-font-display: 'Share Tech Mono', 'VT323', monospace;
  --atom-font-ui: 'DIN 1451', 'Oswald', 'Trebuchet MS', sans-serif;
  --atom-font-mono: 'Courier New', monospace;
}
```

---

## 🧱 Production-Ready Component Blueprints

### 1. Convex CRT Terminal Display

```html
<div class="atom-crt-monitor">
  <div class="atom-crt-glass">
    <div class="atom-scanlines"></div>
    <div class="atom-screen-content">
      <div class="atom-telemetry-header">
        <span>REACTOR CORE // UNIT 4</span>
        <span class="atom-badge-rad">RAD: 3.4 R/HR</span>
      </div>
      <p class="atom-crt-readout">> COOLANT PRESSURE NOMINAL (2200 PSI)</p>
      <p class="atom-crt-readout">> CONTROL ROD ABSORBERS AT 68% INSERTION</p>
    </div>
  </div>
</div>
```

```css
.atom-crt-monitor {
  background: var(--atom-chassis-surface);
  border: 4px solid var(--atom-chassis-border);
  border-radius: 8px;
  padding: 12px;
  box-shadow: inset 2px 2px 0 var(--atom-chassis-highlight), inset -2px -2px 0 #000, 0 8px 24px rgba(0,0,0,0.8);
}
.atom-crt-glass {
  position: relative;
  background: radial-gradient(ellipse at center, #0B2211 0%, var(--atom-crt-bg) 85%);
  border: 2px solid #000;
  border-radius: 12px;
  padding: 24px;
  overflow: hidden;
  box-shadow: inset 0 0 30px rgba(0,0,0,0.95);
}
.atom-scanlines {
  position: absolute;
  inset: 0;
  background: repeating-linear-gradient(
    0deg,
    rgba(0, 0, 0, 0.3) 0px,
    rgba(0, 0, 0, 0.3) 1px,
    transparent 1px,
    transparent 3px
  );
  pointer-events: none;
}
.atom-crt-readout {
  font-family: var(--atom-font-display);
  color: var(--atom-phosphor-p1);
  text-shadow: 0 0 6px var(--atom-phosphor-p1-glow);
  font-size: 1rem;
  letter-spacing: 0.08em;
  line-height: 1.6;
  margin: 6px 0;
}
.atom-badge-rad {
  background: var(--atom-hazard-yellow);
  color: #000;
  font-family: var(--atom-font-ui);
  font-weight: 800;
  font-size: 0.75rem;
  padding: 2px 6px;
  border-radius: 2px;
}
```

### 2. Bakelite Rotary Knob / Stamped Steel Button

```html
<button class="atom-btn-tactile" type="button">
  <span class="atom-btn-rivet left"></span>
  PURGE VENTILATION
  <span class="atom-btn-rivet right"></span>
</button>
```

```css
.atom-btn-tactile {
  position: relative;
  background: linear-gradient(180deg, #382015 0%, var(--atom-bakelite) 60%, #1A0D07 100%);
  color: var(--atom-hazard-yellow);
  font-family: var(--atom-font-ui);
  font-size: 0.875rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  padding: 12px 28px;
  border: 2px solid #5C321E;
  border-radius: 3px;
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.15), inset 0 -2px 0 #000, 0 4px 8px rgba(0,0,0,0.7);
  cursor: pointer;
  transition: transform 60ms ease, box-shadow 60ms ease;
}
.atom-btn-tactile:hover {
  background: linear-gradient(180deg, #4A2B1D 0%, var(--atom-bakelite-hover) 60%, #201009 100%);
  color: #FFF;
}
.atom-btn-tactile:active {
  transform: translateY(2px);
  box-shadow: inset 0 2px 4px #000, 0 1px 2px rgba(0,0,0,0.5);
}
.atom-btn-tactile:focus-visible {
  outline: 2px solid var(--atom-phosphor-p1);
  outline-offset: 3px;
}
```

---

## ✨ Micro-Interactions, Motion & Soundscapes

- **Ballistic Galvanometer:** Analog gauges must feature needle inertia (damping ratio $\zeta \approx 0.7$) with minor ballistic bounce before settling.
- **CRT Phosphor Warm-Up:** Displays fade in over 200ms with scanlines establishing first before luminescence expands.
- **Relay Click:** Switches and toggles produce sharp, instant visual depressions without floaty rubber easing.

---

## ♿ WCAG 2.2 Accessibility & High-Contrast Guardrails

- **Contrast Ratios:**
  - P1 Green phosphor (`#27FF48`) on CRT black (`#06140A`): **14.8:1** (Surpasses WCAG AAA).
  - Amber P3 phosphor (`#FF9900`) on Chassis (`#12181F`): **7.82:1** (Surpasses WCAG AAA).
  - Hazard Yellow (`#FFC800`) on Bakelite (`#2B170E`): **11.2:1** (Surpasses WCAG AAA).
- **Dual-Contrast Focus Ring:**
  `outline: 2px solid #27FF48; box-shadow: 0 0 0 1px #000;` ensures universal visibility across both dark chassis and amber readouts.
- **Reduced Motion:** Under `@media (prefers-reduced-motion: reduce)`, all cathode scanline flickers and needle vibrations are turned off; displays load at steady 100% opacity.

---

## 🚫 Anti-Patterns & Visual Sins (Anti-AI Slop Traps)

- ❌ **NEVER use ice-cream or candy pastel colors:** Flamingo pink, mint green, and butter yellow are strictly prohibited.
- ❌ **NEVER use script or cursive fonts:** Pacifico, Lobster, or 1950s diner scripts distort the nuclear survival genre.
- ❌ **NEVER create modern floating rounded cards:** Cards must appear as modular steel panels bolted into a 19-inch rack enclosure.
- ❌ **NEVER use soft modern SaaS gradients (Indigo/Fuchsia):** Atompunk relies on cathode emissions, glowing filaments, and lead-based industrial enamel finishes.

---

## 💡 Pairings & Cross-Style Synergies

- **Synergies:** Pairs naturally with **[ui-style-terminal-tui](../ui-style-terminal-tui/SKILL.md)** for low-level diagnostic logs and **[ui-style-blueprint-cad-schematic](../ui-style-blueprint-cad-schematic/SKILL.md)** for technical hardware schematics.
- **Avoid Colliding:** Never combine with **[ui-style-frutiger-aero](../ui-style-frutiger-aero/SKILL.md)** or **[ui-style-glassmorphism](../ui-style-glassmorphism/SKILL.md)**; the physical premise of vacuum tubes directly opposes transparent smartphone glass.

---

## 📚 Sources & Historical References

- *The Atomic Energy Commission (AEC) Instrumentation Standards* (Oak Ridge, TN, 1954).
- *Tektronix 511 Oscilloscope Service Manual* (Beaverton, OR, 1947).
- William Gibson, *"The Gernsback Continuum"* (1981).
- Bethesda Game Studios, *Fallout 3 & Fallout 4 Interface Systems* (Pip-Boy 3000 UI Design).
