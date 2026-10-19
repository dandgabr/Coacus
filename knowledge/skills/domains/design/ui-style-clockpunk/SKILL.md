---
name: "ui-style-clockpunk"
description: "Provides the canonical Clockpunk & Renaissance Horology UI style: Early Modern (16th-18th century) retrofuturism of mainsprings, escapements, astronomical orreries, Leonardo da Vinci codex marginalia, iron-gall ink on laid parchment, and interlocking gear ratios. Use when designing museum archives, horology portals, astronomy calculators, educational explainers, or puzzle interfaces."
---

# UI Style: Clockpunk & Renaissance Horology

**Clockpunk** is the retrofuturism of the Renaissance and Enlightenment (roughly the 16th through early 18th centuries) imagined as if precision mechanical horology—escapements, gear trains, spiral balance springs, weights, and cams—evolved into advanced computation and autonomous machines. In digital user interfaces, Clockpunk rejects modern electronic displays in favor of hand-drafted engineering plates: laid parchment substrates, iron-gall ink linework, astronomical astrolabe dials, Da Vincian marginal annotations, and mathematically coupled gear ratios.

---

## 🧭 When to Activate

- Designing components, navigation, and timelines for watchmaking ateliers, horological collections, astronomical observatories, or science-history museums.
- Interactive educational explainers, calendar calculators, mechanical puzzle games, or Renaissance-era narrative fiction.
- Replacing heavy industrial Victorian steam with delicate, hand-drawn Da Vincian drafting lines, mechanical escapement rhythms, and humanist calligraphy.

---

## 🕰️ Definition, Lineage, and Timeline

- **Origins & Historical Anchor:** Coined in tabletop roleplaying supplements (such as *GURPS Steampunk*). Inspired historically by the master clockmakers of Renaissance Europe (Peter Henlein, Jost Bürgi, Christiaan Huygens) and the mechanical sketchbooks of Leonardo da Vinci (the *Codex Atlanticus*, 1478–1519, and *Paris Manuscript B*).
- **Literary Canon:** Margaret Cavendish's *The Blazing World* (1666), Jay Lake's *Mainspring* (2007; a clockwork Earth wound by an orbital brass key), and Ian Tregillis's *The Mechanical* (2015).
- **Distinctions from Neighboring Styles:**
  - Unlike **Steampunk** (Victorian London, coal-fired steam boilers, heavy iron rivets, dark soot, oxblood leather), Clockpunk is clean, spring-driven, quiet, delicate, and set in the Renaissance.
  - Unlike **Sandalpunk** (Greco-Roman antiquity, bronze mechanisms, marble steles, Trajan monumental capitals), Clockpunk features intricate coiled steel mainsprings, pendulum clocks, and Renaissance italic script.
  - Unlike **Atompunk** (Cold War nuclear fission, vacuum tubes, convex CRT phosphor screens), Clockpunk is purely mechanical and anachronistically hand-crafted.
- **Absolute Veto:** Clockpunk is NOT spinning decorative plastic cogs that have no teeth or drive no shafts. Every gear in a Clockpunk interface must honor physical mechanical logic (matching tooth modules, proper pitch diameters, and mathematically locked gear ratios).

---

## 🎨 Visual DNA & Subgenre Taxonomy

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 CLOCKPUNK VISUAL MATRIX                                │
├────────────────────────────┬────────────────────────────┬──────────────────────────────┤
│ 1. Da Vinci Codex Folio    │ 2. Astronomical Astrolabe  │ 3. Master Horology Atelier   │
│ • Laid-parchment ground    │ • Concentric zodiac rings  │ • Burnished brass escapements│
│ • Iron-gall ink linework   │ • Fine coordinate reticles │ • Coiled blued-steel springs │
│ • Humanist margin sketches │ • Lapis lazuli star charts │ • Jewels & ruby pivot caps   │
└────────────────────────────┴────────────────────────────┴──────────────────────────────┘
```

- **Palette & Inks:** Aged laid parchment (`#F1E6CC`), sepia paper wash (`#E6D7B5`), iron-gall ink (`#2A2118`), faded rubric red (`#A63A2B`), lapis lazuli pigment (`#27437A`), and burnished leaf gold (`#B8923A`).
- **Linework & Draftsmanship:** Constant 1px to 1.5px hair-thin vector drafting lines, compass construction circles, tangent guide arcs, and handwritten margin callouts.
- **Iconography:** Astronomical orreries, anchor escapements, fusee chains, sun-and-moon dials, compass roses, and engraved gear profiles.

---

## 📐 Lighting Physics, Specular Splits & Surfaces

1. **Laid Parchment Texture & Ink Bleed:**
   - Subtle tactile laid-paper ribbing with natural iron-gall ink absorption.
   ```css
   background-color: #f1e6cc;
   background-image: repeating-linear-gradient(0deg, transparent 0 31px, rgba(42, 33, 24, 0.08) 31px 32px);
   box-shadow: inset 0 0 45px rgba(184, 146, 58, 0.15), 0 3px 12px rgba(42, 33, 24, 0.1);
   ```
2. **Burnished Gold Leaf Bezel:**
   - Elegant, low-specular metallic reflection highlighting concentric dial rings.
   ```css
   border: 1.5px solid #b8923a;
   box-shadow: inset 0 0 6px rgba(184, 146, 58, 0.25), 0 2px 6px rgba(42, 33, 24, 0.15);
   ```

---

## 🏷️ Complete Design Tokens

```css
:root {
  /* Substrates & Folios */
  --clock-parchment-bg: #F1E6CC;
  --clock-parchment-surface: #F8F1DF;
  --clock-parchment-card: #EFE4CA;

  /* Inks & Natural Pigments */
  --clock-ink-primary: #2A2118;
  --clock-ink-faded: #544432;
  --clock-rubric-red: #A63A2B;
  --clock-lapis-blue: #27437A;
  --clock-blued-steel: #3B4B61;

  /* Horological Metals */
  --clock-gold-leaf: #B8923A;
  --clock-gold-highlight: #E5C578;
  --clock-brass-gear: #9E792B;
  --clock-ruby-bearing: #9B111E;

  /* Typography */
  --clock-font-display: 'EB Garamond', 'Cormorant Garamond', serif;
  --clock-font-body: 'Cormorant', 'Baskerville', Georgia, serif;
  --clock-font-marginalia: 'Italianno', cursive;

  /* Geometry & Mechanical Metrics */
  --clock-stroke-width: 1.5px;
  --clock-border-radius: 3px;
}
```

---

## 🔤 Typography & Lettering Architecture

- **Primary Display Headings:** Humanist and Renaissance serifs (*EB Garamond*, *Cormorant Garamond*) with small-caps styling, classical proportions, and generous letter-spacing (0.05em to 0.12em).
- **Body & Explanatory Prose:** Graceful Renaissance book type (*Cormorant*, *Libre Baskerville*) set in iron-gall ink (`#2A2118`) with 1.7 line-height, emulating early printed folios.
- **Marginalia & Engineering Notes:** Italicized script or calligraphic annotations (*Italianno*, *IM Fell DW Pica Italic*) placed in margins with leader lines pointing to diagram nodes.

---

## 🖱️ Interaction Dynamics, Sound Cues & Motion

- **Escapement Ticking Motion:** Dial indicators and gear trains advance with discrete, stepped mechanical escapement pulses (`animation-timing-function: steps(12)` or `steps(60)`), never artificial smooth continuous tweens.
- **Gear Train Coupling:** When one gear rotates by user interaction, all connected secondary dials rotate proportionally according to exact physical gear ratios (e.g. 12:1 hour/minute ratio).
- **Ink Underline Draw:** Hovering over links or buttons animates an ink stroke drawing horizontally across the base.
- **Motion Reduction:** When `prefers-reduced-motion: reduce` is enabled, all gear rotations and ticking animations freeze into pristine, static vector diagrams.

---

## 🧩 Canonical Component Specifications

### 1. Da Vinci Codex Container (`.clock-codex-card`)
An annotated folio component featuring laid parchment texture, iron-gall rules, and marginal notes.
```html
<article class="clock-codex-card">
  <div class="clock-card-folio">FOLIO 14-R // FIG. 3</div>
  <h3 class="clock-title">Isochronous Escapement Study</h3>
  <p class="clock-text">Oscillation period governed strictly by pendulum length independent of arc amplitude.</p>
</article>
```
```css
.clock-codex-card {
  background: var(--clock-parchment-surface);
  color: var(--clock-ink-primary);
  border: 1.5px solid var(--clock-brass-gear);
  border-radius: var(--clock-border-radius);
  box-shadow: inset 0 0 25px rgba(184, 146, 58, 0.12), 0 3px 12px rgba(42, 33, 24, 0.08);
  padding: 1.75rem;
  position: relative;
}
.clock-card-folio {
  font-family: var(--clock-font-display);
  font-size: 0.75rem;
  color: var(--clock-rubric-red);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin-bottom: 0.5rem;
}
```

### 2. Gilt Horology Action Button (`.clock-btn`)
An action button finished in gold-leaf borders and iron-gall lettering.
```css
.clock-btn {
  background: linear-gradient(180deg, #F8F1DF 0%, #EFE4CA 100%);
  color: var(--clock-ink-primary);
  border: 1.5px solid var(--clock-gold-leaf);
  font-family: var(--clock-font-display);
  font-size: 1rem;
  font-weight: 600;
  letter-spacing: 0.06em;
  padding: 0.65rem 1.6rem;
  border-radius: 2px;
  cursor: pointer;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.8), 0 2px 5px rgba(42, 33, 24, 0.15);
  transition: border-color 0.15s ease, transform 0.1s ease;
}
.clock-btn:hover {
  border-color: var(--clock-rubric-red);
  color: var(--clock-rubric-red);
  transform: translateY(-1px);
}
.clock-btn:active {
  transform: translateY(1px);
}
```

### 3. Astronomical Astrolabe Dial (`.clock-astrolabe`)
A circular celestial calculation dial rendered in concentric SVG coordinate rings.

### 4. Stepped Escapement Progress Wheel (`.clock-progress`)
A progress indicator styled as an escapement wheel ticking in discrete steps towards completion.

---

## ♿ Accessibility & Environmental Contrast (WCAG 2.2)

- **Contrast Mathematics:** Iron-gall ink (`#2A2118`) on laid parchment (`#F1E6CC`) delivers a 9.2:1 contrast ratio, easily surpassing WCAG AAA requirements (7:1).
- **Colored Inks:** Rubric red (`#A63A2B`) achieves 5.2:1 against parchment, fully complying with WCAG AA.
- **Linework Legibility:** Fine 1px diagram lines must maintain at least 3.0:1 contrast against adjacent grounds (WCAG 1.4.11).
- **Focus Indicators:** High-contrast lapis outline with 2px offset (`outline: 2px solid var(--clock-lapis-blue); outline-offset: 3px;`).

---

## ✅ When to Use / ❌ When to Avoid

### Ideal Use Cases
- Museums of the history of science, planetarium websites, and horology archives.
- Mechanical puzzle video games, Renaissance worldbuilding wikis, and historical alternate-timeline fiction.
- Interactive explainers on physics, orbital mechanics, or timekeeping mathematics.

### Anti-Patterns & Prohibitions
- Modern high-volume e-commerce checkouts where decorative clockwork slows user purchase completion.
- Generic corporate business landing pages.
- Continuous endless ticking audio that distracts or distresses users.

---

## 📚 Authoritative Sources & Historical Artifacts

- Leonardo da Vinci, *Codex Atlanticus* (1478–1519), Biblioteca Ambrosiana, Milan.
- Christiaan Huygens, *Horologium Oscillatorium* (The Pendulum Clock), 1673.
- Margaret Cavendish, *The Blazing World*, 1666.
- David S. Landes, *Revolution in Time: Clocks and the Making of the Modern World*, Harvard University Press, 1983.

---

## 🔗 Cross-Skill Integration & Dialect Relations

- **Sibling Speculative Styles:** [ui-style-steampunk](../ui-style-steampunk/SKILL.md), [ui-style-sandalpunk](../ui-style-sandalpunk/SKILL.md), [ui-style-silkpunk](../ui-style-silkpunk/SKILL.md).
- **Archival & Bookcraft Peers:** [ui-style-editorial-archive-luxury](../ui-style-editorial-archive-luxury/SKILL.md), [ui-style-arts-and-crafts](../ui-style-arts-and-crafts/SKILL.md), [ui-style-grain-noise-texture](../ui-style-grain-noise-texture/SKILL.md).
## Appearance and Interaction Verification

Freeze ornamental escapement loops while continuing meaningful dial/progress updates without interpolated travel; expose values and keyboard alternatives to astronomical rings so reduced motion retains the mechanism explanation and final state.
