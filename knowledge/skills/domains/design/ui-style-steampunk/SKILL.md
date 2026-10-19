---
name: "ui-style-steampunk"
description: "Provides the canonical Steampunk & Victorian Industrial UI style (1987-present): Victorian engineering retrofuturism of polished brass, hammered copper, riveted boiler plates, aged oxblood leather, analog pressure gauges, mechanical lever toggles, and differential gear trains. Use when designing alternate-19th-century product worlds, maker storefronts, heritage brands, or narrative game interfaces."
---

# UI Style: Steampunk & Victorian Industrial

**Steampunk** is the retrofuturism of the 19th-century Industrial Revolution imagined as if steam power, clockwork, and mechanical computation never gave way to the internal combustion engine or microchip silicon. In digital user interfaces, Steampunk manifests through tactile materiality: warm polished brass bezels, hammered copper pipes, aged vellum and leather substrates, riveted iron boilerplate panels, and mechanical affordances (pressure dials with needle damping, knurled knobs, and lever switches).

---

## 🧭 When to Activate

- Designing components, navigation, and flows for narrative worlds, video games, conventions, or tabletop RPGs set in an alternate Victorian or Edwardian era.
- Crafting e-commerce storefronts for bespoke horology, artisanal leatherwork, fine spirits, or handmade mechanical goods emphasizing provenance and craft.
- Explaining telemetry or complex systems through analog mechanical metaphors (boiler temperature, chamber pressure, valve release) with strict usability baselines.

---

## 🕰️ Definition, Lineage, and Timeline

- **Coinage & Roots:** Coined in April 1987 by author K. W. Jeter in a letter to *Locus Magazine* to describe the Victorian-era speculative fiction written by himself, Tim Powers (*The Anubis Gates*, 1983), and James Blaylock (*Homunculus*, 1986). Seminal canon includes William Gibson and Bruce Sterling's *The Difference Engine* (1990) and Hayao Miyazaki's *Laputa: Castle in the Sky* (1986).
- **Ethos & Philosophy:** The "punk" in Steampunk represents artisanal defiance against sealed, disposable consumer electronics. Machines are exposed, repairable, ornamented, and celebrate the visible ingenuity of the human hand over sterile mass production.
- **Distinctions from Neighboring Styles:**
  - Unlike **Dieselpunk** (1918–1940s: Art Deco streamlining, heavy naval armor, diesel soot, aviation props, noir shadows), Steampunk is strictly 19th-century Victorian, featuring exposed copper pipework, mahogany woodwork, and coal-fired boilers.
  - Unlike **Clockpunk** (Renaissance, Da Vinci parchment sketches, delicate watch springs, no steam boilers), Steampunk is heavy, pressurized, thermal, and industrial.
  - Unlike **Atompunk** (1945–1965: Cold War atomic fission, convex CRT phosphor screens, bakelite dials, Raygun Gothic), Steampunk is pre-electrical or early galvanic (Leyden jars, brass galvanometers).
- **Absolute Veto:** Steampunk is NOT "gluing random plastic gears to top hats". Purely ornamental, non-functional gear confetti that clutters navigation or obscures legibility is strictly prohibited. Every gear and valve must convey mechanical purpose.

---

## 🎨 Visual DNA & Subgenre Taxonomy

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 STEAMPUNK VISUAL MATRIX                                │
├────────────────────────────┬────────────────────────────┬──────────────────────────────┤
│ 1. Ironworks & Boiler Room │ 2. Airship Bridge          │ 3. Naturalist & Gentleman    │
│ • Riveted boiler plates    │ • Polished brass bezels    │ • Aged vellum parchment      │
│ • Pressure release valves  │ • Compass & navigation dials│ • Hand-engraved typography   │
│ • Heavy cast iron soot     │ • Mahogany wood backing    │ • Deep oxblood leather trim  │
└────────────────────────────┴────────────────────────────┴──────────────────────────────┘
```

- **Materials & Palette:** Aged parchment ground (`#EFE3C8`), deep sepia ink (`#2B1D12`), polished brass (`#B5893A`), hammered copper (`#B4633A`), oxidized verdigris patina (`#4F8A78`), rich oxblood leather (`#5B2A22`), and coal soot black (`#1B1612`).
- **Framing & Surfaces:** Bolted boilerplates, cartouche header brackets, engraved filigree borders, and stepped brass bezels with inset specular reflections.
- **Iconography:** Thin-line engraved patent diagrams, manometer pressure dials, lever toggles, pipe couplers, airship compass roses, and mechanical escapements.

---

## 📐 Lighting Physics, Specular Splits & Surfaces

1. **Machined Brass Bezel & Rivet Relief:**
   - 135-degree overhead light source creating a sharp golden highlight along the top-left edge and deep umber shadow beneath.
   ```css
   background: linear-gradient(145deg, #D2A95A 0%, #8E6A2B 55%, #C79B49 100%);
   border: 2px solid #4A3512;
   box-shadow: inset 1px 1px 0 #F2D690, inset -1px -2px 4px rgba(0, 0, 0, 0.4), 0 4px 10px rgba(27, 22, 18, 0.35);
   ```
2. **Convex Glass Gauge Face:**
   - Simulated spherical lens glare across an aged dial face with needle parallax.
   ```css
   background: radial-gradient(circle at 35% 30%, rgba(255, 255, 255, 0.4) 0%, rgba(239, 227, 200, 0.1) 40%, rgba(43, 29, 18, 0.6) 100%);
   box-shadow: inset 0 0 15px rgba(0, 0, 0, 0.6), 0 2px 8px rgba(0, 0, 0, 0.4);
   ```

---

## 🏷️ Complete Design Tokens

```css
:root {
  /* Substrates & Parchment */
  --steam-paper-bg: #EFE3C8;
  --steam-paper-surface: #F5EBD7;
  --steam-leather-bg: #5B2A22;
  --steam-soot-bg: #1B1612;

  /* Inks & Text */
  --steam-ink-primary: #2B1D12;
  --steam-ink-secondary: #574130;
  --steam-ink-light: #EFE3C8;

  /* Metals & Alloys */
  --steam-brass-highlight: #F2D690;
  --steam-brass-primary: #B5893A;
  --steam-brass-shadow: #5A4118;
  --steam-copper: #B4633A;
  --steam-copper-glow: rgba(180, 99, 58, 0.3);
  --steam-iron-plate: #332B25;
  --steam-iron-border: #4A3E36;
  --steam-verdigris: #4F8A78;

  /* Typography */
  --steam-font-display: 'Playfair Display', 'Abril Fatface', 'Cinzel', serif;
  --steam-font-body: 'Libre Baskerville', 'Source Serif Pro', Georgia, serif;
  --steam-font-mono: 'Courier Prime', 'Courier New', monospace;

  /* Geometry & Mechanical Metrics */
  --steam-border-radius: 4px;
  --steam-bezel-width: 3px;
}
```

---

## 🔤 Typography & Lettering Architecture

- **Primary Display Headings:** Victorian high-contrast display type (*Playfair Display*, *Abril Fatface*, *IM Fell English*) with carved serifs, dramatic thick-thin stroke modulation, and traditional small-caps styling.
- **Body & Paragraphs:** Humanist Victorian book serifs (*Libre Baskerville*, *Source Serif Pro*) set in deep sepia ink (`#2B1D12`) on warm parchment with 1.65 line-height. Never use ornate or gothic blackletter for multi-sentence reading blocks.
- **Technical & Patent Numbers:** Classic mono typefaces (*Courier Prime*) simulating manual typewriter mechanisms or punch-card telegraphy.

---

## 🖱️ Interaction Dynamics, Sound Cues & Motion

- **Escapement & Ratchet Motion:** Progress spinners and gear trains rotate in discrete mechanical increments (`animation-timing-function: steps(8)`) rather than continuous electronic sweeps.
- **Needle Damping & Overshoot:** Pressure needles respond to state changes with physical spring damping (`transition: transform 0.6s cubic-bezier(0.3, 1.4, 0.5, 1)`), momentarily overshooting before settling.
- **Tactile Valve Clicks:** Button active states depress physically into the chassis (`transform: translate(2px, 2px)`), accompanied by shadow collapse.
- **Motion Reduction:** When `prefers-reduced-motion: reduce` is active, gear rotations halt immediately and pressure needles transition without overshoot.

---

## 🧩 Canonical Component Specifications

### 1. Riveted Boilerplate Container (`.steam-panel`)
A heavy plate component finished with industrial rivets and bolted corner brackets.
```html
<section class="steam-panel">
  <div class="steam-panel-header">
    <span class="steam-spec-no">PATENT NO. 4188-B</span>
    <h3 class="steam-heading">Combustion Manifold</h3>
  </div>
  <p class="steam-body">Steam pressure regulated at 142 PSI. Condensation purge valve armed.</p>
</section>
```
```css
.steam-panel {
  background: var(--steam-paper-surface);
  color: var(--steam-ink-primary);
  border: 2px solid var(--steam-brass-shadow);
  border-radius: var(--steam-border-radius);
  box-shadow: inset 0 0 20px rgba(90, 65, 24, 0.15), 0 4px 14px rgba(27, 22, 18, 0.25);
  padding: 1.75rem;
  position: relative;
}
.steam-panel::before {
  content: "";
  position: absolute;
  inset: 4px;
  border: 1px dashed rgba(181, 137, 58, 0.6);
  pointer-events: none;
}
```

### 2. Analog Pressure Gauge (`.steam-gauge`)
A circular manometer readout displaying real system values with a mechanical needle.
```html
<div class="steam-gauge" role="meter" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100">
  <div class="steam-gauge-face">
    <div class="steam-needle" style="transform: rotate(45deg);"></div>
    <span class="steam-gauge-value">75 PSI</span>
  </div>
</div>
```
```css
.steam-gauge {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  border: 4px solid var(--steam-brass-primary);
  box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.7), 0 3px 8px rgba(0, 0, 0, 0.4);
  position: relative;
  background: radial-gradient(circle, #F5EBD7 0%, #D8C39E 100%);
}
.steam-needle {
  position: absolute;
  bottom: 50%;
  left: calc(50% - 1.5px);
  width: 3px;
  height: 44px;
  background: #C2301F;
  transform-origin: 50% 100%;
  transition: transform 0.5s cubic-bezier(0.3, 1.4, 0.5, 1);
}
```

### 3. Machined Brass Button (`.steam-btn`)
A heavy mechanical push-button stamped with golden metallic highlights.
```css
.steam-btn {
  background: linear-gradient(180deg, #D2A95A 0%, #8E6A2B 100%);
  color: #1B1612;
  font-family: var(--steam-font-display);
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 0.75rem 1.6rem;
  border: 2px solid #5A4118;
  border-radius: 3px;
  box-shadow: inset 0 1px 0 #F2D690, 0 3px 6px rgba(0, 0, 0, 0.35);
  cursor: pointer;
  transition: transform 0.1s ease, box-shadow 0.1s ease;
}
.steam-btn:active {
  transform: translate(2px, 2px);
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.6), 0 1px 2px rgba(0, 0, 0, 0.2);
}
```

### 4. Telegraph Lever Toggle (`.steam-toggle`)
An electrical knife-switch toggle replacing standard checkbox controls.

---

## ♿ Accessibility & Environmental Contrast (WCAG 2.2)

- **Contrast Ratios:** Deep sepia (`#2B1D12`) on parchment (`#EFE3C8`) delivers an 8.6:1 contrast ratio (exceeding WCAG AAA 7:1). Brass labels on soot background (`#1B1612`) reach 7.4:1.
- **Form Controls:** Text input fields must feature flat, high-contrast interior backgrounds (`#FBF8F1`) rather than heavily textured grunge to prevent eye strain.
- **Auditory & Visual Dual-Coding:** Every audio click or mechanical animation is mirrored by standard ARIA state attributes (`aria-pressed`, `aria-expanded`).
- **Focus Indicators:** Brass-accented dark outline with visible offset (`outline: 3px solid #5B2A22; outline-offset: 3px;`).

---

## ✅ When to Use / ❌ When to Avoid

### Ideal Use Cases
- Interactive video game interfaces, narrative fiction companion sites, and alternate-Victorian worldbuilding encyclopedias.
- Craft distillery, bespoke watchmaker, or leather atelier storefronts emphasizing traditional hand fabrication.
- Industrial museum exhibits, science-history interactive timelines, and maker festival portals.

### Anti-Patterns & Prohibitions
- Modern high-density cloud infrastructure management consoles.
- Fast checkout flows in mass-market consumer e-commerce where period ornament slows transactional throughput.
- Colonialist or imperialist romanticization without historical context.

---

## 📚 Authoritative Sources & Historical Artifacts

- K. W. Jeter, Letter to *Locus Magazine*, April 1987 (coining of "steam-punks").
- William Gibson & Bruce Sterling, *The Difference Engine*, Gollancz, 1990.
- Tim Powers, *The Anubis Gates*, Ace Books, 1983.
- Jakob Nielsen, *10 Usability Heuristics for User Interface Design*, Nielsen Norman Group, 1994.

---

## 🔗 Cross-Skill Integration & Dialect Relations

- **Sibling Industrial Styles:** [ui-style-dieselpunk](../ui-style-dieselpunk/SKILL.md), [ui-style-clockpunk](../ui-style-clockpunk/SKILL.md), [ui-style-atompunk](../ui-style-atompunk/SKILL.md).
- **Craft & Tactile Peers:** [ui-style-skeuomorphism](../ui-style-skeuomorphism/SKILL.md), [ui-style-arts-and-crafts](../ui-style-arts-and-crafts/SKILL.md), [ui-style-grain-noise-texture](../ui-style-grain-noise-texture/SKILL.md).
## Appearance and Interaction Verification

Name the pressure meter with its units and range; preserve lever/checkbox semantics and static value updates while decorative gears stop; verify engraved labels against convex-glass shading and keep ornament outside input interiors.

