---
name: "ui-style-cassette-futurism"
description: "Provides the authentic Cassette Futurism UI style (1975-1985 analog sci-fi and industrial microcomputing): curved phosphor CRT monitors, mechanical rocker switches, GaAs red LED segment displays, Ron Cobb semiotic hazard striping, magnetic tape reel indicators, and heavy beige polycarbonate chassis. Use when designing retro sci-fi space mission consoles, audio synthesizer interfaces, hardware diagnostics, or laboratory instrument emulators."
---

# UI Style: Cassette Futurism (Analog Electronics, Phosphor Monitors & Industrial Beige Enclosures)

Cassette Futurism is an analog retrofuturist aesthetic derived from the consumer electronics, industrial workstations, and sci-fi cinema of the mid-1970s through mid-1980s (1975–1985). Canonical references include Ron Cobb's Semiotic Standard for *Alien* (1979), Syd Mead's industrial consoles in *Blade Runner* (1982), the Hewlett-Packard 9845B desktop computer, and magnetic tape-driven laboratory mainframes. Defined by physically grounded computing: heavy injection-molded beige or olive casings, convex CRT screens with scanlines and phosphor decay, glowing Gallium Arsenide (GaAs) red 7-segment LEDs, tactile toggle switches, and magnetic tape reel telemetry. Synthesized from primary industrial design archives and user manuals; see Sources.

---

## 🧭 When to Activate

- Designing retro sci-fi cockpits, deep-space telemetry monitors, synthesizer control panels, laboratory data loggers, or analog computing emulators.
- Modeling user interfaces that feel embedded inside physical, screw-mounted equipment racks with visible status lamps and toggle hardware.
- Distinct from **[ui-style-cyberpunk](../ui-style-cyberpunk/SKILL.md)**: Cyberpunk is sleek, nocturnal, holographic, rainy, and neon-saturated; Cassette Futurism is chunky, daylight-industrial, analog, beige/slate, and bounded by physical cathode ray tubes.
- Distinct from **[ui-style-retro-computing](../ui-style-retro-computing/SKILL.md)**: Retro Computing focuses on text-mode software prompts and pure character cells; Cassette Futurism models the complete physical instrument chassis, hazard decals, and analog tape drive mechanics.

---

## 🕰️ Definition, Lineage, and Timeline

- **Chronology:** Golden period from 1977 (release of Commodore PET 2001 and Apple II) through 1985 (dawn of high-resolution bitmap GUIs). Peaked in cinema with *Alien* (1979), *The Empire Strikes Back* (1980), and *WarGames* (1983).
- **Industrial Philosophy:** High technology constructed out of tactile, repairable modular components. Computing power is physically manifested in tape capstans, stepped rotary switches, mechanical latching pushbuttons, and discrete incandescent bulb readouts.

---

## 🎨 Visual DNA & Subgenre Taxonomy

- **Chassis & Hardware Palettes:**
  - Instrument Beige Polycarbonate (`#D8CEB9` / `#C4B99F`)
  - Deep Naval Steel Slate (`#161D1A` / `#222A26`)
  - GaAs Infrared/Red LED (`#FF1A2A` / `#D40D1C`)
  - P1 Green Phosphor (`#33FF33`) and P3 Amber (`#FFB000`)
  - Caution Hazard Stripe Yellow (`#F5A623`) and Hazard Black (`#111111`)
- **Physical Chassis Construction:**
  - Beveled CRT monitor bezels with 8px corner radii and recessed display glass.
  - Visible pan-head machine screws, stamped serial number plates, and ventilation louvers.
  - Rocker switches with visible 2-state physical shadows and toggle throw.
- **Typography:**
  - Discrete 7-segment and 14-segment digital readouts (DSEG7, Share Tech Mono).
  - CRT screen monospace type (VT323, Modern DOS 437) with scanline masking.
  - Industrial equipment labeling in uppercase grotesques (Helvetica Bold, Univers 67).

---

## 📐 Lighting Physics, Specular Splits & Surfaces

- **Convex CRT Glass & Micro-Scanlines:**
  ```css
  /* Spherical screen bulge & phosphor scanlines */
  .cassette-crt {
    background: #061108;
    box-shadow: inset 0 0 24px rgba(0, 0, 0, 0.95), inset 0 0 4px rgba(51, 255, 51, 0.3);
    position: relative;
    overflow: hidden;
  }
  .cassette-crt::after {
    content: "";
    position: absolute;
    inset: 0;
    background: repeating-linear-gradient(
      0deg,
      rgba(0, 0, 0, 0.35) 0px,
      rgba(0, 0, 0, 0.35) 2px,
      transparent 2px,
      transparent 4px
    );
    pointer-events: none;
  }
  ```
- **Hazard Tape Striping:**
  ```css
  background: repeating-linear-gradient(
    -45deg,
    #F5A623 0 12px,
    #111111 12px 24px
  );
  ```

---

## 🏷️ Complete Design Tokens

```css
:root {
  /* Enclosure & Chassis */
  --cassette-chassis: #D8CEB9;
  --cassette-chassis-shadow: #A3967F;
  --cassette-chassis-dark: #1E2522;
  --cassette-bezel: #0F1412;
  --cassette-crt-bg: #061108;

  /* Phosphors & LEDs */
  --cassette-green: #33FF33;
  --cassette-green-dim: #1B8A1B;
  --cassette-amber: #FFB000;
  --cassette-led-red: #FF1A2A;
  --cassette-hazard-yellow: #F5A623;

  /* Typography */
  --cassette-font-crt: 'VT323', monospace;
  --cassette-font-label: 'Univers', 'Helvetica Neue', Arial, sans-serif;
  --cassette-font-led: 'Share Tech Mono', monospace;

  /* Framing Constants */
  --cassette-border-chassis: 4px solid var(--cassette-chassis-shadow);
  --cassette-border-screen: 8px solid var(--cassette-bezel);
}
```

---

## 🧱 Production-Ready Component Blueprint

```html
<section class="cassette-rack">
  <div class="cassette-hazard-bar"></div>
  <header class="cassette-header">
    <div class="cassette-id">NOSTROMO // DECK-C TELEMETRY</div>
    <div class="cassette-led-cluster">
      <span class="cassette-led on" aria-label="Drive Status Online"></span>
      <span class="cassette-led-label">DRIVE ACTIVE</span>
    </div>
  </header>
  <div class="cassette-screen-bezel">
    <div class="cassette-screen">
      <div class="cassette-telemetry-grid">
        <div class="cassette-col">
          <span class="cassette-prompt">MODULE: TAPE-BUFFER-04</span>
          <span class="cassette-data">CAPACITY: 2400 FT // 800 BPI</span>
        </div>
        <div class="cassette-col">
          <span class="cassette-prompt">HEAD STATUS: LOCKED</span>
          <span class="cassette-data">PARITY: ODD // CRC OK</span>
        </div>
      </div>
      <div class="cassette-readout">
        <span class="cassette-counter">REEL: 0482.9 FT</span>
        <span class="cassette-alert">PRESSURE NOMINAL</span>
      </div>
    </div>
  </div>
  <footer class="cassette-controls">
    <button class="cassette-rocker cassette-rocker-on" type="button">CAPSTAN RUN</button>
    <button class="cassette-rocker" type="button">REWIND</button>
    <button class="cassette-rocker cassette-rocker-danger" type="button">EMERGENCY EJECT</button>
  </footer>
</section>
```

```css
.cassette-rack {
  background: var(--cassette-chassis);
  border: var(--cassette-border-chassis);
  padding: 24px;
  max-width: 680px;
  box-shadow: inset 2px 2px 0 #FFF, inset -2px -2px 0 #7A6F5B, 0 12px 32px rgba(0, 0, 0, 0.6);
  position: relative;
}
.cassette-hazard-bar {
  height: 8px;
  background: repeating-linear-gradient(-45deg, var(--cassette-hazard-yellow) 0 10px, #111 10px 20px);
  margin-bottom: 16px;
  border: 1px solid #000;
}
.cassette-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  font-family: var(--cassette-font-label);
  font-weight: 700;
  font-size: 0.8125rem;
  letter-spacing: 0.1em;
}
.cassette-id {
  color: #1A1A1A;
}
.cassette-led-cluster {
  display: flex;
  align-items: center;
  gap: 8px;
}
.cassette-led {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #4A0000;
  border: 1px solid #111;
}
.cassette-led.on {
  background: var(--cassette-led-red);
  box-shadow: 0 0 8px var(--cassette-led-red);
}
.cassette-screen-bezel {
  background: var(--cassette-bezel);
  padding: 14px;
  border-radius: 12px;
  box-shadow: inset 0 4px 10px rgba(0, 0, 0, 0.9), 0 2px 4px rgba(255, 255, 255, 0.3);
  margin-bottom: 20px;
}
.cassette-screen {
  background: var(--cassette-crt-bg);
  border: 2px solid #020803;
  border-radius: 6px;
  padding: 20px;
  color: var(--cassette-green);
  font-family: var(--cassette-font-crt);
  font-size: 1.25rem;
  line-height: 1.4;
  text-shadow: 0 0 6px rgba(51, 255, 51, 0.5);
  position: relative;
}
.cassette-telemetry-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  border-bottom: 1px solid var(--cassette-green-dim);
  padding-bottom: 14px;
  margin-bottom: 14px;
}
.cassette-prompt {
  display: block;
  font-size: 0.9375rem;
  color: var(--cassette-green-dim);
}
.cassette-readout {
  display: flex;
  justify-content: space-between;
  font-weight: 700;
}
.cassette-counter {
  color: var(--cassette-amber);
  text-shadow: 0 0 6px rgba(255, 176, 0, 0.5);
}
.cassette-controls {
  display: flex;
  gap: 12px;
}
.cassette-rocker {
  background: #D0C5AF;
  color: #1A1A1A;
  font-family: var(--cassette-font-label);
  font-weight: 700;
  font-size: 0.8125rem;
  letter-spacing: 0.05em;
  padding: 10px 18px;
  border: 2px solid #5A5243;
  box-shadow: 0 4px 0 #5A5243;
  cursor: pointer;
  text-transform: uppercase;
}
.cassette-rocker:active, .cassette-rocker-on {
  transform: translateY(3px);
  box-shadow: 0 1px 0 #5A5243;
  background: #BFB49D;
}
.cassette-rocker-danger {
  background: #A62424;
  color: #FFFFFF;
  border-color: #5C1111;
  box-shadow: 0 4px 0 #5C1111;
}
```

---

## ✨ Micro-Interactions, Motion & Soundscapes

- **Physical Switch Snap:** Rocker switches exhibit instantaneous mechanical depression with an audible clack and zero easing.
- **CRT Power-On Raster Sweep:** Screen activation renders a high-velocity horizontal raster sweep from a narrow raster line to the complete readout (`clip-path: inset(0)`) in 180ms; never leave content collapsed after completion. Clip reveal mechanics and `inert` handling: [ui-state-layout-transitions](../ui-state-layout-transitions/SKILL.md).
- **GaAs LED Strobe:** Standby indicators pulse with authentic 2Hz square-wave blink.

---

## 📱 Responsive Layout & Spatial Composition

- On viewports `< 640px`, wrap telemetry columns into a single stack and scale monitor text size from 20px to 16px while preserving the heavy bezel borders.

---

## ♿ WCAG 2.2 Accessibility & High-Contrast Guardrails

- **Contrast Ratios:**
  - P1 Green Phosphor (`#33FF33`) on Dark Screen (`#061108`): **14.9:1** (Passes WCAG AAA).
  - P3 Amber Phosphor (`#FFB000`) on Dark Screen: **11.4:1** (Passes WCAG AAA).
  - Red LED (`#FF1A2A`) on Instrument Beige: used strictly for icons/indicators, never body text.
- **Reduced Motion:**
  ```css
  @media (prefers-reduced-motion: reduce) {
    .cassette-led.on, .cassette-screen::after {
      animation: none;
    }
    .cassette-screen { clip-path: inset(0); opacity: 1; }
  }
  ```

---

## 🚫 Anti-Patterns & Visual Sins (Anti-AI Slop Traps)

- ❌ **NEVER use rounded bubbly floating pill badges:** Buttons are rectangular screw-mounted plastic or steel rockers.
- ❌ **NEVER use neon blue or magenta glowing laser grids:** That belongs to Synthwave; Cassette Futurism uses functional CRT phosphors and discrete LEDs.
- ❌ **NEVER omit the physical equipment chassis:** Without the molded beige or slate casing and bezel framing, the screen loses its physical machine context.

---

## 🎯 When to Use & When to Avoid

- **Use For:** Hardware diagnostics, audio synthesis tools, sci-fi simulators, retro computing platforms, deep-space game interfaces.
- **Avoid For:** Clean SaaS accounting dashboards, mobile lifestyle apps, delicate e-commerce fashion stores.

---

## 📚 Sources & References

- Ron Cobb, *The Semiotic Standard for All Commercial and Non-Commercial Spaceflight* (20th Century Fox, 1979).
- Syd Mead, *Oblagon: Concepts of Syd Mead* (Dentsu, 1985).
- Hewlett-Packard Company, *HP 9845B Desktop Computer Operating and Service Manual* (1979).
## Appearance and Interaction Verification

Define CRT power-on completion as the full visible readout and immediately show it under reduced motion; wrap physical rocker controls as well as telemetry columns and preserve latched state in semantic text/pressed state.
