---
name: "ui-style-cyberpunk"
description: "Provides the canonical Cyberpunk & Sci-Fi Tactical HUD UI style (1980s-present): high-tech low-life neon-noir dystopia fused with Territory Studio cinematic tactical instrumentation (FUI), 45-degree chamfered polygon cards, horizontal CRT scanlines, cryptographic decoding reveals, electric cyan, acid yellow, and telemetry coordinate reticles. Use when designing game cockpits, esports streaming platforms, cybersecurity dashboards, web3 developer tools, or sci-fi entertainment portals."
---

# UI Style: Cyberpunk & Sci-Fi Tactical HUD

**Cyberpunk** translates the quintessential "high tech, low life" ethos into user interface design: the sensory overload of rain-slicked neon alleys, corporate surveillance monopolies, and underground hacker networks colliding with the hyper-dense, angular telemetry of cinematic Fantasy User Interfaces (FUI). In digital software, Cyberpunk combines near-black obsidian substrates with volumetric neon glow, 45-degree chamfered corner geometry (`clip-path: polygon`), CRT scanline overlays, cryptographic character-decoding transitions, and tactical reticle targeting grids.

---

## 🧭 When to Activate

- Designing game interfaces, esports competition hubs, gaming companion apps, or sci-fi narrative portals.
- Cybersecurity monitoring consoles, terminal hacker playgrounds, blockchain/web3 analytics, and developer tools seeking an aggressive, electric aesthetic.
- Mission-critical cockpits, tactical telemetry grids, radar sweeps, and high-density technical readouts.

---

## 🕰️ Definition, Lineage, and Timeline

- **Literary & Cinematic Canon:** Coined in 1983 by Bruce Bethke in his short story *"Cyberpunk"*; popularized by Gardner Dozois. Core canon: Ridley Scott & Syd Mead's *Blade Runner* (1982), William Gibson's *Neuromancer* (1984), Katsuhiro Otomo's *Akira* (1988), and Masamune Shirow's *Ghost in the Shell* (1995).
- **The Cinematic FUI Lineage:** Pioneered by Ron Cobb's graphical user interfaces in *Alien* (1979) and Mark Coleran's tactical consoles in *Children of Men* (2006). Industrialized and standardized by Territory Studio (*The Martian* 2015, *Blade Runner 2049* 2017) and CD Projekt Red's *Cyberpunk 2077* (2020).
- **Distinctions from Neighboring Styles:**
  - Unlike **Synthwave** (nostalgic 1980s outrun, purple sunsets, palm trees, Ferrari Testarossas, chrome vector scripts), Cyberpunk is gritty, hostile, surveillance-heavy, militarized, and dystopian.
  - Unlike **Atompunk** (1950s vacuum tubes, bakelite knobs, convex analog oscilloscopes, Cold War nuclear fallout), Cyberpunk is high-bandwidth, digital, optic-fiber, and cybernetic.
  - Unlike **Terminal TUI** (plain ASCII character matrix), Cyberpunk HUD features multi-layered vector geometry, glowing holographic overlays, and polygon chamfers.
- **Absolute Veto:** Blinding illegible chromatic aberration filters that distort body copy into unreadable mush are strictly forbidden. Chromatic glitch effects must be reserved for micro-interactions (hover/click) and non-text visual frames.

---

## 🎨 Visual DNA & Subgenre Taxonomy

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 CYBERPUNK VISUAL MATRIX                                │
├────────────────────────────┬────────────────────────────┬──────────────────────────────┤
│ 1. Dystopian Neon-Noir     │ 2. Tactical FUI / HUD      │ 3. Postcyberpunk Clean State │
│ • Electric cyan & magenta  │ • 45° chamfered polygon box│ • Polished white & gunmetal  │
│ • CRT scanline persistence │ • Targeting reticle axes   │ • High-efficiency daylight UI│
│ • Volumetric rain reflections│• Micro-telemetry readouts│ • Seamless cyberware sync    │
└────────────────────────────┴────────────────────────────┴──────────────────────────────┘
```

- **Palette & Radiance:** Subterranean obsidian (`#05060A`), tactical slate surface (`#0D1017`), electric neon cyan (`#00F0FF`), acid hazard yellow (`#FCEE0A`), hot laser magenta (`#FF003C`), warning amber (`#FF5500`), and luminescent pale lavender text (`#E8EAFF`).
- **Angular Geometry:** 45-degree corner chamfers (`clip-path: polygon(0 0, calc(100% - 14px) 0, 100% 14px, 100% 100%, 14px 100%, 0 calc(100% - 14px))`), 1px luminescent border hairlines, and calibration corner brackets.
- **HUD Overlays:** Horizontal electron scanlines, barcode tags, warning diagonal stripes, and coordinate crosshairs (`[ 34.882 // 118.441 ]`).

---

## 📐 Lighting Physics, Specular Splits & Surfaces

1. **Chamfered Tactical HUD Container with Luminescent Rim:**
   - 45-degree sliced corners with volumetric cyan neon glow and dark obsidian core.
   ```css
   background-color: #0d1017;
   border: 1px solid rgba(0, 240, 255, 0.45);
   clip-path: polygon(0 0, calc(100% - 14px) 0, 100% 14px, 100% 100%, 14px 100%, 0 calc(100% - 14px));
   box-shadow: 0 0 20px rgba(0, 240, 255, 0.15), inset 0 0 15px rgba(0, 240, 255, 0.05);
   ```
2. **Horizontal Scanline Telemetry Grid:**
   - Non-interactive pseudo-element simulating high-resolution CRT line scanning.
   ```css
   background: repeating-linear-gradient(0deg, rgba(0, 0, 0, 0.35) 0 1px, transparent 1px 3px);
   pointer-events: none;
   ```

---

## 🏷️ Complete Design Tokens

```css
:root {
  /* Substrates & Chassis */
  --cyber-obsidian-bg: #05060A;
  --cyber-slate-surface: #0D1017;
  --cyber-slate-card: #131722;
  --cyber-border-dim: #1E2536;

  /* Neon Radiances */
  --cyber-cyan: #00F0FF;
  --cyber-cyan-glow: rgba(0, 240, 255, 0.4);
  --cyber-yellow: #FCEE0A;
  --cyber-yellow-glow: rgba(252, 238, 10, 0.4);
  --cyber-magenta: #FF003C;
  --cyber-magenta-glow: rgba(255, 0, 60, 0.4);
  --cyber-amber-warn: #FF5500;

  /* Text & Telemetry */
  --cyber-text-primary: #E8EAFF;
  --cyber-text-dim: #9499B3;
  --cyber-text-dark: #05060A;

  /* Typography */
  --cyber-font-display: 'Rajdhani', 'Orbitron', sans-serif;
  --cyber-font-telemetry: 'Share Tech Mono', 'JetBrains Mono', monospace;
  --cyber-font-body: 'Inter', system-ui, sans-serif;

  /* Angular Chamfer Dimensions */
  --cyber-chamfer-size: 14px;
}
```

---

## 🔤 Typography & Lettering Architecture

- **Primary Display Headings:** High-tech industrial sans-serifs (*Rajdhani*, *Orbitron*) set with bold weights, crisp geometric angularity, and uppercase styling with 0.05em to 0.1em letter-spacing.
- **HUD Telemetry & Coordinate Data:** Monospaced technical fonts (*Share Tech Mono*, *JetBrains Mono*) for target IDs, memory addresses (`0x7FFF...`), and live latency readouts.
- **Body Text:** Clear, high-legibility grotesques (*Inter*, *Roboto*) ensuring effortless reading against dark obsidian surfaces without visual fatigue.

---

## 🖱️ Interaction Dynamics, Sound Cues & Motion

- **Cryptographic Decryption Reveal:** Headers decode on initial view through rapid character cycling (`&%#?*` resolving into readable glyphs over 250ms).
- **Glitch Slice on Hover:** Interactive buttons exhibit a brief, 80ms horizontal chromatic slice offset when hovered.
- **Targeting Reticle Lock:** Cursors and active targets acquire corner bracket calibration marks that snap inwards.
- **Motion Reduction:** When `prefers-reduced-motion: reduce` is enabled, all glitch animations, decoding scrambles, and scanline sweeps halt into clean, static illuminated HUD shapes.

---

## 🧩 Canonical Component Specifications

### 1. Chamfered Tactical HUD Card (`.cyber-hud-card`)
An angular container clipped with 45-degree polygon corners and illuminated by a cyan laser border.
```html
<article class="cyber-hud-card">
  <div class="cyber-card-header">
    <span class="cyber-target-id">[ TRG-8812 // ACTIVE ]</span>
    <h3 class="cyber-title">Sub-Orbital Uplink</h3>
  </div>
  <p class="cyber-text">Bandwidth allocated: 104.2 TB/s. Quantum encryption key verified.</p>
</article>
```
```css
.cyber-hud-card {
  background: var(--cyber-slate-card);
  color: var(--cyber-text-primary);
  border: 1px solid rgba(0, 240, 255, 0.35);
  clip-path: polygon(0 0, calc(100% - var(--cyber-chamfer-size)) 0, 100% var(--cyber-chamfer-size), 100% 100%, var(--cyber-chamfer-size) 100%, 0 calc(100% - var(--cyber-chamfer-size)));
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6), inset 0 0 15px rgba(0, 240, 255, 0.04);
  padding: 1.75rem;
  position: relative;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
.cyber-hud-card:hover {
  border-color: var(--cyber-cyan);
  box-shadow: 0 6px 25px var(--cyber-cyan-glow), inset 0 0 20px rgba(0, 240, 255, 0.08);
}
.cyber-target-id {
  font-family: var(--cyber-font-telemetry);
  font-size: 0.75rem;
  color: var(--cyber-yellow);
  letter-spacing: 0.1em;
  display: block;
  margin-bottom: 0.5rem;
}
```

### 2. Acid Yellow Tactical Button (`.cyber-btn-yellow`)
A high-visibility chamfered action button styled in hazard acid yellow.
```css
.cyber-btn-yellow {
  background: var(--cyber-yellow);
  color: var(--cyber-text-dark);
  font-family: var(--cyber-font-display);
  font-size: 1.05rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: 0.7rem 1.8rem;
  border: none;
  clip-path: polygon(10px 0, 100% 0, calc(100% - 10px) 100%, 0 100%);
  cursor: pointer;
  box-shadow: 0 0 14px var(--cyber-yellow-glow);
  transition: background 0.15s ease, box-shadow 0.15s ease, transform 0.1s ease;
}
.cyber-btn-yellow:hover {
  background: var(--cyber-cyan);
  box-shadow: 0 0 22px var(--cyber-cyan-glow);
  transform: translateY(-1px);
}
.cyber-btn-yellow:active {
  transform: translateY(1px);
}
```

### 3. Targeting Reticle Frame (`.cyber-reticle`)
A telemetry frame featuring corner crosshair brackets and coordinate axes.

### 4. Real-Time Telemetry Bar (`.cyber-telemetry-bar`)
A horizontal status indicator displaying live memory and network ping metrics.

---

## ♿ Accessibility & Environmental Contrast (WCAG 2.2)

- **Contrast Mathematics:** Acid yellow (`#FCEE0A`) on obsidian black (`#05060A`) delivers an outstanding 16.8:1 contrast ratio; electric cyan (`#00F0FF`) on obsidian reaches 13.5:1 (both far exceeding WCAG AAA 7:1).
- **Secondary Telemetry Text:** Lavender text (`#E8EAFF`) achieves 14.2:1; muted gray (`#9499B3`) delivers 6.2:1 against the dark background, satisfying WCAG AA for normal body copy.
- **Photosensitivity Safeguards (WCAG 2.3.1):** Never trigger full-screen flashing or intense chromatic strobe effects. All neon flicker animations must stay below 2.0 Hz and be fully disableable.
- **Focus Indicators:** High-visibility acid yellow outline (`outline: 2px solid var(--cyber-yellow); outline-offset: 3px;`).

---

## ✅ When to Use / ❌ When to Avoid

### Ideal Use Cases
- Esports competition platforms, gaming companion apps, and game development telemetry dashboards.
- Cybersecurity threat hunting consoles, dark web monitoring interfaces, and terminal playgrounds.
- Sci-fi media promotion, futuristic hardware product launches, and high-performance developer tools.

### Anti-Patterns & Prohibitions
- Calm meditation, healthcare wellness, or sleep assistance apps.
- Corporate accounting, human resources, or tax filing software.
- Excessively noisy glitch animations that render primary checkout actions invisible.

---

## 📚 Authoritative Sources & Historical Artifacts

- William Gibson, *Neuromancer*, Ace Books, 1984.
- Ridley Scott & Syd Mead, *Blade Runner*, Warner Bros., 1982.
- Territory Studio, *Blade Runner 2049* Screen Graphics Case Study, 2017.
- CD Projekt Red, *Cyberpunk 2077 Visual Design Guide*, 2020.

---

## 🔗 Cross-Skill Integration & Dialect Relations

- **Sibling Speculative Styles:** [ui-style-synthwave](../ui-style-synthwave/SKILL.md), [ui-style-atompunk](../ui-style-atompunk/SKILL.md), [ui-style-biopunk](../ui-style-biopunk/SKILL.md), [ui-style-nanopunk](../ui-style-nanopunk/SKILL.md).
- **Technical & Terminal Peers:** [ui-style-terminal-tui](../ui-style-terminal-tui/SKILL.md), [ui-style-dark-mode-first](../ui-style-dark-mode-first/SKILL.md), [ui-style-glitch](../ui-style-glitch/SKILL.md).
## Appearance and Interaction Verification

Use an unclipped focus owner or inset high-contrast bracket that survives polygon clipping; document daylight as an optional postcyberpunk material mapping with dark ink and subdued emission, rather than inheriting nocturnal card/scanline paint.
