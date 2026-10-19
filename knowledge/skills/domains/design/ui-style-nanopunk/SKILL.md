---
name: "ui-style-nanopunk"
description: "Provides the canonical Nanopunk & Molecular Engineering UI style (1990s-present): microscopic science fiction of self-assembling nanites, diamondoid crystal structures, carbon nanotube meshes, atomic force microscopy, scale-shift navigation, and crystalline luminescence. Use when designing materials science platforms, semiconductor telemetry, quantum computing interfaces, or deep-tech research portals."
---

# UI Style: Nanopunk & Molecular Engineering

**Nanopunk** is the speculative design language of microscopic engineering: worlds where self-replicating nanobots, programmable matter, and diamondoid molecular mechanics operate at the nanometer scale ($10^{-9}$ m). Rather than the street-level neon grit of Cyberpunk or the wet genetic flesh of Biopunk, Nanopunk is pristine, mathematical, crystalline, and defined by **scale-shift navigation** (transitioning seamlessly from macro objects to cellular lattices to individual atoms).

---

## 🧭 When to Activate

- Designing deep-tech dashboards, materials science platforms, semiconductor nanofabrication tools, or quantum computing control suites.
- Visualizing atomic structures, crystalline lattices, carbon allotropes (graphene, nanotubes, buckyballs), or molecular assembler telemetry.
- Building high-precision developer tools, scientific simulations, or sci-fi games focused on programmable matter and nanotech swarms.

---

## 🕰️ Definition, Lineage, and Timeline

- **Origins & Foundations:** Grounded in Richard Feynman's visionary 1959 lecture *"There's Plenty of Room at the Bottom"* and formalized by K. Eric Drexler in *Engines of Creation: The Coming Era of Nanotechnology* (1986).
- **Literary Canon:** Neal Stephenson's *The Diamond Age: Or, A Young Lady's Illustrated Primer* (1995; matter compilers, rod logic, smart dust), Kathleen Ann Goonan's *Queen City Jazz* (1994), and Michael Crichton's *Prey* (2002).
- **Distinctions from Neighboring Styles:**
  - Unlike **Cyberpunk** (macro-scale computer terminals, neon-lit alleys, cybernetic limbs, corporate cable clutter), Nanopunk operates at the molecular scale where matter itself becomes intelligent.
  - Unlike **Biopunk** (wet biological organs, enzymatic fluids, DNA plasmids, messy cellular membranes), Nanopunk is dry, crystalline, diamondoid, and mathematically structured.
  - Unlike **Terminal TUI** (flat text strings and ASCII frames), Nanopunk utilizes multi-layered vector meshes, electron-microscopy depth-of-field, and coordinate axes.
- **Absolute Veto:** Nanopunk is NOT generic "glowing crypto network dots" or stock blockchain lines. Every lattice node, scale bar, and coordinate grid must represent genuine physical geometry (nanometers, angstroms, crystal bond angles).

---

## 🎨 Visual DNA & Subgenre Taxonomy

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 NANOPUNK VISUAL MATRIX                                 │
├────────────────────────────┬────────────────────────────┬──────────────────────────────┤
│ 1. Diamondoid Precision    │ 2. Smart Dust & Swarm      │ 3. Atomic Force Microscopy   │
│ • Hexagonal carbon lattices│ • Dispersed particle fields│ • False-color electron heat  │
│ • Crystalline refraction   │ • Coalescing data clouds   │ • Nanometer scale markers    │
│ • Crisp cyan & silver lines│ • Vector velocity vectors  │ • Atomic coordinate crosshairs│
└────────────────────────────┴────────────────────────────┴──────────────────────────────┘
```

- **Palette & Radiance:** Deep void carbon (`#070A0F`), laboratory graphite (`#0F151F`), cold atomic cyan (`#4DE3FF`), crystalline silver (`#D8E4EC`), quantum fluorophore green (`#36F1CD`), and ultraviolet laser violet (`#8B5CF6`).
- **Lattices & Structures:** Hexagonal graphene honeycomb grids, 60-degree isometric axes, molecular valence bonds, and nanoscale measurement callouts.
- **Micro-textures:** Scanning Electron Microscopy (SEM) stipple noise, atomic force probe reticles, and sub-pixel particle fields.

---

## 📐 Lighting Physics, Specular Splits & Surfaces

1. **Carbon Nanotube Lattice & Honeycomb Backing:**
   - Procedural hexagonal dot matrix simulating an atomic graphene sheet.
   ```css
   background-color: #070a0f;
   background-image: radial-gradient(circle, rgba(77, 227, 255, 0.22) 1px, transparent 1.5px);
   background-size: 20px 20px;
   box-shadow: inset 0 0 80px rgba(0, 0, 0, 0.9);
   ```
2. **Crystalline Diamondoid Edge Reflection:**
   - 1px razor-sharp prismatic highlight simulating diamond-cleaved facets.
   ```css
   border: 1px solid rgba(77, 227, 255, 0.35);
   box-shadow: 0 0 16px rgba(77, 227, 255, 0.12), inset 0 1px 0 rgba(255, 255, 255, 0.4);
   backdrop-filter: blur(12px);
   ```

---

## 🏷️ Complete Design Tokens

```css
:root {
  /* Carbon Foundations */
  --nano-void-bg: #070A0F;
  --nano-graphite-surface: #0E141E;
  --nano-graphite-card: #151D2A;
  --nano-graphite-border: #223043;

  /* Quantum Signals & Luminescence */
  --nano-cyan-signal: #4DE3FF;
  --nano-cyan-glow: rgba(77, 227, 255, 0.35);
  --nano-teal-quantum: #36F1CD;
  --nano-silver-text: #D8E4EC;
  --nano-silver-dim: #8B9BB0;

  /* Lattices & Meshes */
  --nano-lattice-line: rgba(77, 227, 255, 0.18);
  --nano-lattice-dot: rgba(77, 227, 255, 0.3);
  --nano-border-radius: 3px;

  /* Typography */
  --nano-font-display: 'Space Grotesk', 'Syncopate', sans-serif;
  --nano-font-telemetry: 'IBM Plex Mono', 'Space Mono', monospace;
  --nano-font-body: 'Inter', -apple-system, sans-serif;
}
```

---

## 🔤 Typography & Lettering Architecture

- **Primary Display Headings:** Precision, wide geometric sans-serifs (*Space Grotesk*, *Syncopate*) featuring extended letter-spacing (0.08em to 0.15em) representing spacious molecular voids.
- **Nanometer Telemetry & Metrics:** Sharp monospaced fonts (*IBM Plex Mono*, *JetBrains Mono*) for physical constants ($\hbar$, $k_B$), bond lengths in angstroms (Å), and lattice constants.
- **Body & Scientific Text:** Clean, neutral high-legibility grotesques (*Inter*, *Roboto*) ensuring effortless reading against dark carbon surfaces.

---

## 🖱️ Interaction Dynamics, Sound Cues & Motion

- **Lattice Distortion on Hover:** Crystalline cards displace their underlying honeycomb grid slightly towards the cursor pointer like an atomic force microscope probe.
- **Particle Swarm Coalescence:** Data visualizations assemble from dispersed floating particles into rigid geometric shapes on state load.
- **Scale-Shift Transitions:** Zooming in changes dimensional units smoothly ($100\ \mu\text{m} \to 1\ \mu\text{m} \to 10\ \text{nm} \to 1\ \text{Å}$).
- **Motion Reduction:** When `prefers-reduced-motion: reduce` is detected, all particle drift and lattice animations halt into sharp static vector lines.

---

## 🧩 Canonical Component Specifications

### 1. Hexagonal Diamondoid Card (`.nano-card`)
A dark graphite card structured with carbon hairline borders and corner nanoscale calibration marks.
```html
<article class="nano-card">
  <div class="nano-card-scale">SCALE: 2.4 nm // 100,000x</div>
  <h3 class="nano-title">Fullerene Cage Assembly</h3>
  <p class="nano-data">Valence configuration: $sp^2$ hybridization • Yield: 99.98%</p>
</article>
```
```css
.nano-card {
  background: var(--nano-graphite-card);
  border: 1px solid var(--nano-graphite-border);
  border-radius: var(--nano-border-radius);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6), inset 0 0 20px rgba(77, 227, 255, 0.03);
  padding: 1.75rem;
  position: relative;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
.nano-card:hover {
  border-color: var(--nano-cyan-signal);
  box-shadow: 0 6px 25px rgba(77, 227, 255, 0.15), inset 0 0 25px rgba(77, 227, 255, 0.06);
}
.nano-card-scale {
  font-family: var(--nano-font-telemetry);
  font-size: 0.75rem;
  color: var(--nano-teal-quantum);
  letter-spacing: 0.1em;
  margin-bottom: 0.5rem;
}
```

### 2. Quantum Dot Action Button (`.nano-btn`)
An action button glowing with cold cyan luminescence and sharp 1px diamondoid framing.
```css
.nano-btn {
  background: rgba(77, 227, 255, 0.08);
  color: var(--nano-cyan-signal);
  border: 1px solid var(--nano-cyan-signal);
  font-family: var(--nano-font-display);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  padding: 0.65rem 1.6rem;
  border-radius: 2px;
  cursor: pointer;
  box-shadow: 0 0 12px rgba(77, 227, 255, 0.2);
  transition: background 0.15s ease, box-shadow 0.15s ease, transform 0.1s ease;
}
.nano-btn:hover {
  background: var(--nano-cyan-signal);
  color: #070A0F;
  box-shadow: 0 0 22px rgba(77, 227, 255, 0.5);
  transform: translateY(-1px);
}
.nano-btn:active {
  transform: translateY(1px);
}
```

### 3. Nanoscale Zoom Rail (`.nano-scale-rail`)
A continuous dimensional zoom slider spanning macroscopic meters down to picometer subatomic ranges.

### 4. Graphene Honeycomb Container (`.nano-honeycomb`)
A telemetry container overlaid with an interactive SVG hexagonal bond lattice.

---

## ♿ Accessibility & Environmental Contrast (WCAG 2.2)

- **Contrast Mathematics:** Cold atomic cyan (`#4DE3FF`) and crystalline silver (`#D8E4EC`) on dark void graphite (`#070A0F`) deliver 13.8:1 and 14.6:1 contrast ratios (vastly surpassing WCAG AAA 7:1).
- **Secondary Telemetry Text:** Silver-dim text (`#8B9BB0`) achieves 5.4:1 against the background, exceeding WCAG AA minimums (4.5:1).
- **Photosensitivity Safeguards (WCAG 2.3.1):** Particle mesh movements must maintain subtle velocity and never flash or strobe above 2.0 Hz.
- **Focus Rings:** Luminous cyan outline with 2px offset (`outline: 2px solid var(--nano-cyan-signal); outline-offset: 2px;`).

---

## ✅ When to Use / ❌ When to Avoid

### Ideal Use Cases
- Nanotechnology research portals, quantum simulator cockpits, and advanced materials engineering tools.
- Speculative sci-fi games focused on programmable matter, grey goo containment, or assembler fabrication.
- Semiconductor physics documentation, cleanroom telemetry, and scanning probe microscopy interfaces.

### Anti-Patterns & Prohibitions
- Generic corporate landing pages trying to look "modern" with random disconnected node webs.
- Consumer e-commerce or lifestyle blogs where nanoscale scientific precision alienates casual audiences.
- Overusing complex particle canvas loops that degrade low-end mobile device performance.

---

## 📚 Authoritative Sources & Historical Artifacts

- Richard Feynman, "There's Plenty of Room at the Bottom", American Physical Society, 1959.
- K. Eric Drexler, *Engines of Creation: The Coming Era of Nanotechnology*, Anchor Books, 1986.
- Neal Stephenson, *The Diamond Age: Or, A Young Lady's Illustrated Primer*, Bantam Spectra, 1995.
- C. Joachim & L. Plevert, *Nanosciences: The Invisible Revolution*, World Scientific, 2008.

---

## 🔗 Cross-Skill Integration & Dialect Relations

- **Sibling Speculative Styles:** [ui-style-cyberpunk](../ui-style-cyberpunk/SKILL.md), [ui-style-biopunk](../ui-style-biopunk/SKILL.md), [ui-style-atompunk](../ui-style-atompunk/SKILL.md).
- **Precision & Structure Peers:** [ui-style-blueprint-cad-schematic](../ui-style-blueprint-cad-schematic/SKILL.md), [ui-style-terminal-tui](../ui-style-terminal-tui/SKILL.md), [ui-style-3d-immersive-webgl](../ui-style-3d-immersive-webgl/SKILL.md).
## Appearance and Interaction Verification

Keep physically meaningful scales and crystalline identity; ensure zoom-unit labels, measurement values and controls initialize in reduced motion before decorative particle assembly, and scope lattice clipping/lifecycle to the scientific viewport owner.
