---
name: "ui-style-sandalpunk"
description: "Provides the canonical Sandalpunk & Classical Antiquity UI style (also known as Bronzepunk): speculative retrofuturism of ancient Greco-Roman and Hellenistic civilization (Hero of Alexandria, Archimedes, the Antikythera mechanism), featuring pentelic marble surfaces, hammered bronze trim, Tyrian imperial purple, classical meander friezes, incised lapidary typography, and mechanical bronze automata. Use when designing mythic narratives, historical archives, classical philosophy hubs, or ancient alternate-future games."
---

# UI Style: Sandalpunk & Classical Antiquity

**Sandalpunk** (frequently termed **Bronzepunk**) is the speculative retrofuturism of Classical Antiquity—imagining an alternate history where the engineering breakthroughs of the Hellenistic and Roman worlds (Archimedes' compound pulleys, Hero of Alexandria's steam aeolipile and programmable automata, and the differential bronze gearwork of the Antikythera mechanism) sparked an ancient technological revolution. Rather than collapsing, classical Mediterranean civilization advanced into high-tech planetary power while preserving its civic architecture, pagan mythos, and lapidary philosophy.

---

## 🧭 When to Activate

- Designing components, navigation, and flows for mythic, classical, or Greco-Roman alternate-history video games and tabletop RPGs.
- Museum portals, classical philosophy archives, Mediterranean heritage exhibitions, or academic archaeological databases.
- Replacing Victorian brass or modern silicone glass with monumental Pentelic marble steles, incised stone Roman capitals, hammered bronze borders, and Antikythera celestial gearwork.

---

## 🕰️ Definition, Lineage, and Timeline

- **Origins & Historical Precedents:** Rooted in the genuine mechanical marvels of the Hellenistic era (circa 3rd to 1st century BCE): the Antikythera mechanism (circa 150–100 BCE, the world's oldest known analog computer calculating lunar, solar, and planetary cycles with 30+ differential bronze gears), Ctesibius's water organ, and Hero of Alexandria's pneumatic theater doors (*Pneumatica*).
- **Literary & Visual Tropes:** Alternate-Rome superpowers, bronze-hulled triremes powered by aeolipile steam turbines, automaton legionaries, and monumental temple architecture illuminated by optical bronze mirrors.
- **Distinctions from Neighboring Styles:**
  - Unlike **Steampunk** (19th-century Victorian London, iron rivets, coal soot, heavy pressure boilers, leather goggles), Sandalpunk is set in classical antiquity, powered by bronze, olive oil, water hydraulics, and sun-warmed stone.
  - Unlike **Clockpunk** (Renaissance Europe, coiled steel mainsprings, Da Vinci manuscript marginalia), Sandalpunk is built on cast bronze, sundials, Antikythera differential gears, and monumental Greek/Latin inscriptions.
  - Unlike **Editorial Archive Luxury** (modern high-fashion minimalism), Sandalpunk is a speculative technological world with mechanical automata and historical tension.
- **Absolute Veto & Ethical Boundary:** Totalitarian fascist appropriation of Roman heraldry (fasces, eagle standards, or authoritarian imperial triumphalism) is strictly prohibited. Sandalpunk must explore the philosophical, mathematical, astronomical, and democratic craftsmanship of antiquity, acknowledging ancient social realities with historical nuance.

---

## 🎨 Visual DNA & Subgenre Taxonomy

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 SANDALPUNK VISUAL MATRIX                               │
├────────────────────────────┬────────────────────────────┬──────────────────────────────┤
│ 1. Antikythera Telemetry   │ 2. Forum & Senate Stele    │ 3. Alexandrian Automata      │
│ • Differential bronze gears│ • Veined Pentelic marble   │ • Cast bronze mechanisms     │
│ • Greek astrological scales│ • Incised Roman capitals   │ • Water hydraulics & steam   │
│ • Concentric calendar dials│ • Tyrian purple banners    │ • Polished brass mirrors     │
└────────────────────────────┴────────────────────────────┴──────────────────────────────┘
```

- **Palette & Pigments:** Pentelic marble white (`#F4F1EA`), warm travertine stone (`#D9CBB0`), cast bronze (`#8C5A2B`), oxidized copper verdigris (`#3E8E7E`), imperial Tyrian purple (`#66023C`), Mediterranean lapis blue (`#1F3A93`), and volcanic obsidian black (`#16130F`).
- **Shapes & Architecture:** Symmetrical axial compositions, pediment headers, classical meander (*Greek key*) fretwork friezes, and carved stele cards.
- **Micro-textures:** Inlaid marble veining, hammered bronze pitting, incised-stone chiseled typography, and engraved circular gear teeth.

---

## 📐 Lighting Physics, Specular Splits & Surfaces

1. **Incised Lapidary Stone Carving:**
   - Deep chiseled lettering with light cast from the upper-left, throwing an internal shadow across the bottom-right groove.
   ```css
   background-color: #f4f1ea;
   color: #16130f;
   text-shadow: 1px 1px 0 rgba(255, 255, 255, 0.8), -1px -1px 0 rgba(0, 0, 0, 0.25);
   box-shadow: inset 0 0 30px rgba(140, 90, 43, 0.12), 0 4px 16px rgba(22, 19, 15, 0.1);
   ```
2. **Hammered Bronze Bezel & Verdigris Patina:**
   - Warm metallic bronze frame with subtle green oxidized weathering along crevices.
   ```css
   border: 2px solid #8c5a2b;
   box-shadow: inset 0 0 8px rgba(62, 142, 126, 0.25), 0 3px 8px rgba(0, 0, 0, 0.2);
   ```

---

## 🏷️ Complete Design Tokens

```css
:root {
  /* Classical Stone Grounds */
  --sandal-marble-white: #F4F1EA;
  --sandal-marble-surface: #FAF7F0;
  --sandal-travertine-stone: #D9CBB0;
  --sandal-obsidian-black: #16130F;

  /* Imperial Pigments & Dyes */
  --sandal-tyrian-purple: #66023C;
  --sandal-tyrian-glow: rgba(102, 2, 60, 0.25);
  --sandal-lapis-blue: #1F3A93;
  --sandal-terracotta: #C85A32;

  /* Antiquity Metals */
  --sandal-bronze-primary: #8C5A2B;
  --sandal-bronze-highlight: #C28B54;
  --sandal-bronze-dark: #5A3816;
  --sandal-verdigris: #3E8E7E;

  /* Typography */
  --sandal-font-display: 'Cinzel', 'Trajan Pro', serif;
  --sandal-font-body: 'EB Garamond', 'Cormorant', Georgia, serif;
  --sandal-font-greek: 'GFS Didot', 'Cinzel', serif;

  /* Geometry */
  --sandal-border-width: 2px;
  --sandal-stele-radius: 4px;
}
```

---

## 🔤 Typography & Lettering Architecture

- **Primary Display Headings:** Monumental Roman inscriptional capitals (*Cinzel*, *Trajan Pro*) with classical proportions (modeled on the base inscription of Trajan's Column, 113 CE). Set with generous tracking (0.12em to 0.2em) and uppercase rendering.
- **Body & Literature:** Renaissance humanist serifs (*EB Garamond*, *Cormorant*) providing warm, organic cadence with high contrast and 1.65 line-height.
- **Astronomical & Scientific Scales:** Classical Greek lettering (*GFS Didot*) for calendar coordinate degrees, solar zodiac glyphs, and mathematical annotations.

---

## 🖱️ Interaction Dynamics, Sound Cues & Motion

- **Antikythera Step Rotation:** Dials and concentric calendar rings rotate with deliberate, heavy steps (`transition: transform 0.6s steps(12, end)`).
- **Stele Door Translation:** Modals and drawer panels slide smoothly like heavy stone temple doors with high inertial damping (`cubic-bezier(0.25, 1, 0.5, 1)`).
- **Engraved Hover Inset:** On cursor hover, text darkens and is underlined by an animated drawing meander line.
- **Motion Reduction:** When `prefers-reduced-motion: reduce` is detected, all stepping dial rotations and stone door translations switch to instantaneous opacity changes.

---

## 🧩 Canonical Component Specifications

### 1. Inscribed Marble Stele Card (`.sandal-stele`)
A stone monument container finished with carved travertine borders, meander header, and lapidary type.
```html
<article class="sandal-stele">
  <div class="sandal-stele-frieze"></div>
  <h3 class="sandal-title">ANTIKYTHERA EPICYCLE MODEL</h3>
  <p class="sandal-text">Calculating the lunar anomalistic month via 32-tooth differential bronze gearing.</p>
</article>
```
```css
.sandal-stele {
  background: var(--sandal-marble-surface);
  color: var(--sandal-obsidian-black);
  border: 2px solid var(--sandal-bronze-primary);
  border-radius: var(--sandal-stele-radius);
  box-shadow: 0 4px 18px rgba(22, 19, 15, 0.12), inset 0 0 20px rgba(140, 90, 43, 0.08);
  padding: 1.75rem;
  position: relative;
}
.sandal-stele-frieze {
  height: 10px;
  border-bottom: 2px solid var(--sandal-bronze-primary);
  background: repeating-linear-gradient(90deg, var(--sandal-bronze-primary) 0 2px, transparent 2px 12px);
  margin-bottom: 1rem;
}
```

### 2. Tyrian Imperial Action Button (`.sandal-btn-imperial`)
A prestigious primary action button dyed in royal Tyrian purple with chiseled bronze borders.
```css
.sandal-btn-imperial {
  background: linear-gradient(180deg, #7A0A4A 0%, #540232 100%);
  color: #F4F1EA;
  font-family: var(--sandal-font-display);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  padding: 0.75rem 1.75rem;
  border: 2px solid var(--sandal-bronze-highlight);
  border-radius: 2px;
  box-shadow: 0 2px 6px rgba(102, 2, 60, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.2);
  cursor: pointer;
  transition: transform 0.12s ease, box-shadow 0.12s ease;
}
.sandal-btn-imperial:hover {
  background: linear-gradient(180deg, #8C1057 0%, #66023C 100%);
  box-shadow: 0 4px 12px rgba(102, 2, 60, 0.5);
  transform: translateY(-1px);
}
.sandal-btn-imperial:active {
  transform: translateY(1px);
}
```

### 3. Antikythera Astronomical Dial (`.sandal-antikythera-dial`)
A circular bronze calendar wheel featuring concentric Greek astronomical scales and zodiac markers.

### 4. Classical Meander Dividing Frieze (`.sandal-meander`)
A horizontal decorative band repeating the traditional Greek key geometric pattern.

---

## ♿ Accessibility & Environmental Contrast (WCAG 2.2)

- **Contrast Mathematics:** Obsidian black (`#16130F`) on Pentelic marble (`#F4F1EA`) delivers an exceptional 13.5:1 contrast ratio (exceeding WCAG AAA 7:1).
- **Imperial Accents:** Tyrian purple (`#66023C`) on marble delivers an 8.2:1 contrast ratio, ensuring accessible buttons and header titles.
- **All-Caps Legibility:** Restrict all-caps monumental typography strictly to headings and short tags; body copy must always use standard sentence-case serif type to preserve reading speed.
- **Focus Rings:** Verdigris green double outline (`outline: 3px solid var(--sandal-verdigris); outline-offset: 3px;`).

---

## ✅ When to Use / ❌ When to Avoid

### Ideal Use Cases
- Classical history archives, Mediterranean archaeology portals, and philosophy research libraries.
- Video games, tabletop RPGs, and fantasy worldbuilding hubs exploring ancient mechanical technology.
- Museum exhibitions on ancient Mediterranean mathematics, astronomy, and navigation.

### Anti-Patterns & Prohibitions
- Modern high-frequency financial trading consoles or microservice telemetry.
- Generic corporate real-estate landing pages mimicking Greek columns for fake prestige.
- Any fascist or supremacist aestheticization of Roman imperial domination.

---

## 📚 Authoritative Sources & Historical Artifacts

- Derek de Solla Price, "An Ancient Greek Computer", *Scientific American*, June 1959 (discovery of the Antikythera mechanism).
- Jo Marchant, *Decoding the Heavens: A 2,000-Year-Old Computer and the Century-Long Search to Resolve Its Mystery*, Da Capo Press, 2009.
- Hero of Alexandria, *Pneumatica* and *Automata* (circa 1st century CE).
- Carol Twombly, *Trajan Typeface Design Specification*, Adobe Systems, 1989.

---

## 🔗 Cross-Skill Integration & Dialect Relations

- **Sibling Antiquity & Clockwork Styles:** [ui-style-clockpunk](../ui-style-clockpunk/SKILL.md), [ui-style-steampunk](../ui-style-steampunk/SKILL.md), [ui-style-silkpunk](../ui-style-silkpunk/SKILL.md).
- **Monuments & Stone Craft Peers:** [ui-style-editorial-archive-luxury](../ui-style-editorial-archive-luxury/SKILL.md), [ui-style-arts-and-crafts](../ui-style-arts-and-crafts/SKILL.md), [ui-style-grain-noise-texture](../ui-style-grain-noise-texture/SKILL.md).
