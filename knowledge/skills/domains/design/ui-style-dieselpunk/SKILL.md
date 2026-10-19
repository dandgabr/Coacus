---
name: "ui-style-dieselpunk"
description: "Provides the canonical Dieselpunk & Interwar Machine Age UI style (1918–1950s): Art Deco geometry, Streamline Moderne curves, heavy naval armor plates, diesel soot, combustion engines, noir shadowplay, military dossiers, and bold condensed typography. Use when designing alternate-history games, aviation or racing hubs, speakeasy noir experiences, or heavy industrial brand platforms."
---

# UI Style: Dieselpunk & Interwar Machine Age

**Dieselpunk** is the retrofuturism of the interwar Machine Age (roughly 1918 through the early 1950s). Powered by internal combustion engines, heavy diesel locomotives, aluminum zeppelins, and ocean liners, the genre spans two distinct aesthetic poles: the optimistic, streamlined glamour of the World's Fairs (Ottensian/Decopunk) and the grim, oil-stained, militarized industrialism of the wartime home front (Piecraftian/Oilpunk). In digital interfaces, Dieselpunk manifests as stepped Art Deco ziggurats, venetian-blind noir shadows, classified military dossiers, heavy rivet joints, and bold condensed typography.

---

## 🧭 When to Activate

- Designing components, navigation, and flows for narrative video games, films, or alternate-history worlds set between World War I and the onset of the Atomic Age.
- Automotive, aerospace, aviation history, cocktail lounge, or racing brand platforms demanding gritty machine elegance and high graphic punch.
- High-contrast, dark noir dashboards where heavy machinery and physical telemetry guide mission-critical user workflows.

---

## 🕰️ Definition, Lineage, and Timeline

- **Coinage & History:** Coined in 2001 by game designer Lewis Pollak for the tabletop RPG *Children of the Sun*. Canonical works include *BioShock* (Rapture's decaying Art Deco), *Sky Captain and the World of Tomorrow* (2004), *The Rocketeer* (1991), and *The Man in the High Castle*.
- **The Two Schools of Dieselpunk:**
  1. *Ottensian (Optimistic & Streamlined):* Named after author Nick Ottens. Celebrates 1930s World's Fair futurism, Streamline Moderne teardrop curves, polished chrome, ivory panels, and heroic technological progress.
  2. *Piecraftian (Dystopian & Industrial):* Named after author Piecraft. Focuses on total war mobilization, steel armor, oil stains, barbed wire, diesel fumes, sirens, and classified bureaucratic dossiers.
- **Distinctions from Neighboring Styles:**
  - Unlike **Steampunk** (Victorian 19th-century, brass gears, steam boilers, oxblood leather), Dieselpunk is 20th-century interwar, featuring combustion pistons, diesel fuel, radio vacuum tubes, and Art Deco geometry.
  - Unlike **Atompunk** (1945–1965: Nuclear Age, convex CRT phosphor screens, bakelite dials, Raygun Gothic spaceflight), Dieselpunk precedes nuclear fission, grounded in heavy oil, iron foundries, and propeller aircraft.
- **Absolute Veto & Ethical Boundary:** Real-world totalitarian propaganda insignia (swastikas, fascist fasces, or hate symbols) are strictly forbidden. Interfaces must celebrate the fictional mechanical design, noir atmosphere, and geometric craft of the era without glorifying authoritarian regimes.

---

## 🎨 Visual DNA & Subgenre Taxonomy

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 DIESELPUNK VISUAL MATRIX                               │
├────────────────────────────┬────────────────────────────┬──────────────────────────────┤
│ 1. Classified Dossier (War)│ 2. Streamline Moderne (Deco│ 3. Petro-Industrial (Oilpunk)│
│ • Stamped kraft paper      │ • Chrome & ivory curves    │ • Oil slicks & gunmetal plate│
│ • Venetian-blind shadows   │ • Stepped ziggurat headers │ • Heavy cast-iron rivets     │
│ • Red stencil "CONFIDENTIAL│ • Champagne gold hairlines │ • Combustion exhaust rust    │
└────────────────────────────┴────────────────────────────┴──────────────────────────────┘
```

- **Palette & Finishes:** Gunmetal steel (`#2E3338`), engine oil black (`#14161A`), industrial rust (`#9C4A28`), military olive drab (`#5B6038`), aged tobacco paper (`#D9CBA8`), signal red (`#C2301F`), champagne Deco gold (`#D4B26A`), and cold chromium (`#C8D1D9`).
- **Geometry & Framing:** Stepped 45-degree ziggurat corners, aerodynamic speed lines, radial sunburst rays, and heavy iron perimeter borders.
- **Surface Textures:** Halftone newspaper dot patterns, fine film grain, diagonal shadow slashes, and stamped military serial codes.

---

## 📐 Lighting Physics, Specular Splits & Surfaces

1. **Noir Venetian-Blind Shadows:**
   - Sharp, dramatic high-contrast light slashes cutting across dark industrial surfaces.
   ```css
   background-color: #14161a;
   background-image: repeating-linear-gradient(145deg, rgba(255, 255, 255, 0.04) 0 20px, transparent 20px 48px);
   box-shadow: inset 0 0 60px rgba(0, 0, 0, 0.85);
   ```
2. **Stepped Chrome Bezel (Decopunk):**
   - High-specular horizontal reflection band typical of Streamline Moderne locomotive bumpers.
   ```css
   background: linear-gradient(180deg, #E8ECEF 0%, #A4B0BE 48%, #57606F 52%, #CBD5E1 100%);
   border: 1px solid #2F3542;
   box-shadow: inset 0 1px 0 #FFFFFF, 0 3px 8px rgba(0, 0, 0, 0.45);
   ```

---

## 🏷️ Complete Design Tokens

```css
:root {
  /* Chassis & Grounds */
  --diesel-oil-black: #14161A;
  --diesel-gunmetal: #2E3338;
  --diesel-slate-surface: #1E2328;
  --diesel-paper-bg: #D9CBA8;
  --diesel-paper-card: #E5D9BC;

  /* Typography & Signals */
  --diesel-ink-primary: #14161A;
  --diesel-text-light: #E8ECEF;
  --diesel-signal-red: #C2301F;
  --diesel-signal-amber: #D97706;
  --diesel-rust: #9C4A28;

  /* Decopunk Metals & Accents */
  --diesel-gold-deco: #D4B26A;
  --diesel-gold-shadow: #8A6D33;
  --diesel-chrome: #C8D1D9;
  --diesel-olive: #5B6038;

  /* Typography */
  --diesel-font-display: 'Oswald', 'Bebas Neue', 'League Gothic', sans-serif;
  --diesel-font-deco: 'Limelight', 'Poiret One', sans-serif;
  --diesel-font-body: 'Franklin Gothic Medium', 'Arial Narrow', sans-serif;
  --diesel-font-mono: 'Special Elite', 'Courier Prime', monospace;

  /* Structural Dimensions */
  --diesel-border-width: 2px;
  --diesel-panel-radius: 2px;
}
```

---

## 🔤 Typography & Lettering Architecture

- **Primary Display Headings:** Condensed, tall architectural grotesques (*Oswald*, *Bebas Neue*, *League Gothic*) set in all-caps with tight letter-spacing (0.02em to 0.05em), evoking interwar newspaper headlines and industrial locomotive plates.
- **Deco Accent Titles:** Geometric Streamline Moderne fonts (*Limelight*, *Poiret One*) featuring extreme thick-thin contrast and sweeping circular geometry.
- **Body & Editorial:** Sturdy, highly legible grotesque faces (*Franklin Gothic*, *DIN 1451*) set with solid contrast against dark gunmetal or light tobacco paper.
- **Dossier Markings:** Distressed typewriter mono (*Special Elite*) for timestamps, classification levels, and unit serial codes.

---

## 🖱️ Interaction Dynamics, Sound Cues & Motion

- **Piston-Stroke Press:** Buttons depress instantaneously without elastic rubber-band easing (`transform: translate(3px, 3px); transition: transform 0.08s ease-out`).
- **Heavy Shutter Wipes:** Drawer panels and modal dialogues transition with rapid, mechanical shutter slides mimicking heavy steel blast doors.
- **Chrome Sheen Sweep:** On initial load or state completion, a single specular light highlight sweeps across metallic header bands.
- **Motion Reduction:** When `prefers-reduced-motion: reduce` is enabled, shutter wipes and metallic sheen animations are bypassed in favor of instant state toggles.

---

## 🧩 Canonical Component Specifications

### 1. Military Dossier Card (`.diesel-dossier`)
A classified case-file container finished with tobacco kraft paper and red stencil markings.
```html
<article class="diesel-dossier">
  <div class="diesel-dossier-stamp">CLASSIFIED // EYES ONLY</div>
  <h3 class="diesel-dossier-title">VANGUARD PROPULSION REPORT</h3>
  <p class="diesel-dossier-meta">REF: DE-8842-X • DATE: 14 OCT 1938</p>
  <p class="diesel-dossier-text">Twin supercharged radial engines cleared for full-altitude trial runs.</p>
</article>
```
```css
.diesel-dossier {
  background: var(--diesel-paper-card);
  color: var(--diesel-ink-primary);
  border: 2px solid #8C7B58;
  box-shadow: 4px 4px 0 rgba(0, 0, 0, 0.4), inset 0 0 25px rgba(140, 123, 88, 0.2);
  padding: 1.75rem;
  position: relative;
}
.diesel-dossier-stamp {
  display: inline-block;
  color: var(--diesel-signal-red);
  border: 2px solid var(--diesel-signal-red);
  font-family: var(--diesel-font-display);
  font-weight: bold;
  font-size: 0.75rem;
  padding: 0.2rem 0.5rem;
  letter-spacing: 0.12em;
  transform: rotate(-3deg);
  margin-bottom: 0.75rem;
}
```

### 2. Cast Iron Primary Button (`.diesel-btn`)
A heavy, stamped action button with hard drop-shadow and tactile active translation.
```css
.diesel-btn {
  background: var(--diesel-signal-red);
  color: #FFFFFF;
  font-family: var(--diesel-font-display);
  font-size: 1.1rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: 0.75rem 1.75rem;
  border: 2px solid var(--diesel-oil-black);
  box-shadow: 4px 4px 0 #000000;
  cursor: pointer;
  transition: transform 0.08s ease-out, box-shadow 0.08s ease-out;
}
.diesel-btn:hover {
  background: #D93826;
}
.diesel-btn:active {
  transform: translate(3px, 3px);
  box-shadow: 1px 1px 0 #000000;
}
.diesel-btn:focus-visible {
  outline: 3px solid var(--diesel-gold-deco);
  outline-offset: 3px;
}
```

### 3. Stepped Art Deco Header (`.diesel-header-deco`)
An architectural ziggurat banner finished with champagne gold border trim.

### 4. Halftone Metric Meter (`.diesel-meter`)
A progress bar rendered with mechanical halftone screening and a physical needle indicator.

---

## ♿ Accessibility & Environmental Contrast (WCAG 2.2)

- **Contrast Mathematics:** Cream text (`#E8ECEF`) on gunmetal (`#2E3338`) achieves 7.8:1; deep black (`#14161A`) on tobacco paper (`#D9CBA8`) achieves 10.2:1 (exceeding WCAG AAA 7:1).
- **Non-Text UI Contrast:** Red signal buttons and gold active borders maintain at least 3.5:1 against adjacent chassis tones, satisfying WCAG 1.4.11.
- **Text Readability:** Avoid setting multi-line body paragraphs in condensed all-caps display type; keep condensed type strictly for headings and short badges.
- **Focus Rings:** High-visibility gold outline (`outline: 3px solid var(--diesel-gold-deco); outline-offset: 2px;`).

---

## ✅ When to Use / ❌ When to Avoid

### Ideal Use Cases
- Alternate-history video games, diesel racing simulators, and flight combat interfaces.
- Noir cinema companions, speakeasy brand sites, and bespoke industrial cocktail bars.
- Engineering retrospectives and Machine Age museum exhibitions.

### Anti-Patterns & Prohibitions
- Modern clinical health portals or patient medical records.
- Generic SaaS administrative tools requiring soft, low-contrast pastel palettes.
- Any glorification of historical totalitarianism or militaristic atrocities.

---

## 📚 Authoritative Sources & Historical Artifacts

- Lewis Pollak, *Children of the Sun*, Misguided Games, 2001 (origin of "dieselpunk").
- Nick Ottens, *The Gatehouse*, "Discovering Dieselpunk", 2008.
- Alastair Duncan, *Art Deco Complete: The Definitive Guide to the Decorative Arts of the 1920s and 1930s*, Thames & Hudson, 2009.
- Donald Albrecht, *Designing Dreams: Modern Architecture in the Movies*, Harper & Row, 1986.

---

## 🔗 Cross-Skill Integration & Dialect Relations

- **Sibling Machine Age Styles:** [ui-style-steampunk](../ui-style-steampunk/SKILL.md), [ui-style-atompunk](../ui-style-atompunk/SKILL.md), [ui-style-art-deco](../ui-style-art-deco/SKILL.md).
- **High-Contrast & Noir Peers:** [ui-style-dark-mode-first](../ui-style-dark-mode-first/SKILL.md), [ui-style-grain-noise-texture](../ui-style-grain-noise-texture/SKILL.md), [ui-style-analog-newspaper-broadsheet](../ui-style-analog-newspaper-broadsheet/SKILL.md).
## Appearance and Interaction Verification

Choose focus ink separately on tobacco dossiers and oil-black chassis, and inspect label paint over venetian stripes/chrome bands; retain both optimistic ivory/streamline and grim gunmetal schools rather than forcing one polarity.

