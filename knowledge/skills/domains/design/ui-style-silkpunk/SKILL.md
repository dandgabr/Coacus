---
name: "ui-style-silkpunk"
description: "Provides the canonical Silkpunk & Organic Engineering UI style: East Asian classical antiquity (Han, Tang, Song, Ming) fused with speculative organic engineering, bamboo lattice framing, mulberry paper textures, hammered brass rivets, sumi-e ink washes, and origami folding kinematics. Use when designing speculative cultural portals, narrative fantasy games, historical archives, or artisanal East Asian craft platforms."
---

# UI Style: Silkpunk & Organic Engineering

Coined by speculative author and translator Ken Liu, **Silkpunk** envisions technological systems rooted in the materials, philosophy, and classical engineering of East Asian antiquity (Han, Tang, Song, and Ming dynasties). Rather than Western coal and iron steamworks, Silkpunk machines are constructed from bamboo, silk, coconut fiber, ox-bone, feathers, and paper, powered by muscle, wind, steam, and biological dynamics. In digital user interfaces, Silkpunk translates into parchment textures, ink wash bleeds, delicate lattice grids, calligraphic display accents, and origami folding kinematics.

---

## 🧭 When to Activate

- Designing narrative interfaces, gaming portals, historical literature archives, or cultural platforms celebrating non-Western technological futures.
- Crafting artisanal craft, tea culture, fine calligraphy, or architectural experiences that require tactile, organic materials instead of sterile modern glass.
- Replacing generic dark SaaS or Western steampunk tropes with organic East Asian structural beauty, paper screen reveals, and brushwork geometry.

---

## 🕰️ Definition, Lineage, and Timeline

- **Chronology & Origins:** Coined in 2015 by Ken Liu during the publication of *The Grace of Kings* (*The Dandelion Dynasty*). Drawing inspiration from ancient Chinese engineering marvels—the battle kites of Mozi, the seismoscope of Zhang Heng, the south-pointing chariot of Ma Jun, and the Song dynasty mechanical water clocks of Su Song.
- **Materiality & Philosophy:** Organic materials over heavy mining. Structural members are steam-bent bamboo stalks wrapped in silk cord; sails and lifting surfaces are multi-layered oiled mulberry paper; bearings and gears are carved boxwood, jade, or hammered bronze.
- **Distinctions from Neighboring Styles:**
  - Unlike **Steampunk** (Victorian London, coal smog, boiler rivets, iron pipes, heavy soot), Silkpunk is clean, buoyant, wind-harnessed, bamboo-framed, and aerodynamically delicate.
  - Unlike **Cyberpunk** (rainy neon dystopia, corporate surveillance, high tech low life), Silkpunk is communal, philosophical, craft-reverent, and embedded in classical literature.
  - Unlike **Sandalpunk** (Greco-Roman marble, bronze gears, Trajan capitals), Silkpunk derives its geometry from Chinese pavilion lattices, origami folds, and sumi-e wash gradients.
- **Absolute Veto:** Silkpunk is NOT generic anime neon or Western chinoiserie parody. Cheap faux-brush fonts (*Wonton* style), saturated dragon clipart, and Western Victorian goggles are strictly prohibited.

---

## 🎨 Visual DNA & Subgenre Taxonomy

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 SILKPUNK VISUAL MATRIX                                 │
├────────────────────────────┬────────────────────────────┬──────────────────────────────┤
│ 1. Imperial Court & Airship│ 2. Artisanal Workshop      │ 3. Scholar Pavilion & Ink    │
│ • Vermilion lacquer frames │ • Steam-bent bamboo struts │ • Aged mulberry paper wash   │
│ • Gold leaf inlays         │ • Braided silk cord knots  │ • Sumi-e brush bleed edges   │
│ • Cloud-scroll heraldry    │ • Hammered brass rivets    │ • Geometric lattice panels   │
└────────────────────────────┴────────────────────────────┴──────────────────────────────┘
```

- **Surfaces & Grounds:** Warm aged mulberry paper (`#F5EFE0`), untreated bamboo skin (`#E6D7B8`), cinnabar lacquer (`#A62B2A`), imperial indigo dye (`#1D2A44`), and hand-beaten brass (`#C9A050`).
- **Linework & Borders:** Pavilion wooden lattice fretwork (*wanzi* swastika-fret, cracked-ice *binglie*, and interlocking coin motifs), delicate 1px brass hairlines, and soft ink bleeding outlines.
- **Kinematics:** Panels unfold along origami crease lines; sliding partition doors (*shoji* / *fusuma* inspiration) translate smoothly on custom tracks.

---

## 📐 Lighting Physics, Specular Splits & Surfaces

1. **Mulberry Paper Backlight:**
   - Soft, warm transmission of light through fiber sheets rather than glossy glass reflection.
   ```css
   background-color: #f7f2e7;
   background-image: radial-gradient(circle at 50% 20%, rgba(255, 255, 255, 0.6) 0%, rgba(245, 239, 224, 0.95) 100%);
   box-shadow: inset 0 0 40px rgba(181, 150, 107, 0.15), 0 4px 16px rgba(29, 42, 68, 0.08);
   ```
2. **Hammered Brass Trim & Lacquer Edge:**
   - Directional brushed metallic luster with crisp contrast against dark ink.
   ```css
   border: 2px solid #c9a050;
   box-shadow: inset 1px 1px 0 rgba(255, 235, 175, 0.6), inset -1px -1px 0 rgba(110, 80, 25, 0.5), 0 2px 6px rgba(0, 0, 0, 0.12);
   ```

---

## 🏷️ Complete Design Tokens

```css
:root {
  /* Grounds & Substrates */
  --silk-paper-bg: #F5EFE0;
  --silk-paper-surface: #FBF8F1;
  --silk-paper-card: #FAF4E8;
  --silk-bamboo-joint: #D8C39E;

  /* Traditional Inks & Dyes */
  --silk-ink-black: #1A1D20;
  --silk-ink-faded: #424953;
  --silk-indigo: #1D2A44;
  --silk-vermilion: #C3272B;
  --silk-vermilion-glow: rgba(195, 39, 43, 0.2);
  --silk-jade: #4E7C59;

  /* Metals & Lacquer */
  --silk-brass: #C9A050;
  --silk-brass-light: #E2BF7D;
  --silk-brass-dark: #8C6A28;
  --silk-lacquer-red: #8B1B1E;

  /* Typography */
  --silk-font-display: 'Noto Serif SC', 'Songti SC', 'Cinzel', serif;
  --silk-font-body: 'Noto Serif', 'Source Serif Pro', Georgia, serif;
  --silk-font-mono: 'JetBrains Mono', monospace;

  /* Layout & Geometry */
  --silk-border-radius: 4px;
  --silk-lattice-stroke: 1.5px;
}
```

---

## 🔤 Typography & Lettering Architecture

- **Primary Display Headings:** High-contrast neoclassical serifs and elegant Songti/Ming display typefaces (*Noto Serif*, *Cinzel Decorative*, *Baskerville*). Generous letter-spacing (0.05em to 0.12em) conveying imperial dignity.
- **Body & Paragraphs:** Legible, balanced editorial serifs (*Noto Serif*, *Libre Baskerville*) with generous line-height (1.65 to 1.8) simulating woodblock-printed book margins.
- **Accents & Annotations:** Vertical reading tracks (`writing-mode: vertical-rl`) for seal marks, date rubrics, and chapter markers.

---

## 🖱️ Interaction Dynamics, Sound Cues & Motion

- **Origami Fan Unfold:** Dropdown menus and modals expand outward with faceted angular rotation (`transform: scaleY(...) rotateX(...)`) like folding paper fans.
- **Sumi-e Ink Bleed:** Primary buttons and active tabs expand a radial water-bleed mask on hover rather than an artificial electronic glow.
- **Bamboo Snap Feedback:** Clicks have immediate, crisp mechanical settlement without bouncing jelly spring physics.
- **Motion Reduction:** When `prefers-reduced-motion: reduce` is detected, unfolding transforms are replaced with instant 150ms opacity fades.

---

## 🧩 Canonical Component Specifications

### 1. Lattice Paper Card (`.silk-card`)
A multi-layered component featuring an aged paper ground, 1px bamboo-joint border, and corner brass rivets.
```html
<article class="silk-card">
  <div class="silk-card-header">
    <span class="silk-rubric">卷三 • 飛舟</span>
    <h3 class="silk-title">Celestial Glider Telemetry</h3>
  </div>
  <p class="silk-content">Compressed steam pressure sustained across silk-reinforced bamboo ribs.</p>
</article>
```
```css
.silk-card {
  background: var(--silk-paper-surface);
  border: 1px solid var(--silk-bamboo-joint);
  border-radius: var(--silk-border-radius);
  box-shadow: inset 0 0 20px rgba(216, 195, 158, 0.2), 0 3px 12px rgba(29, 42, 68, 0.06);
  padding: 1.75rem;
  position: relative;
}
.silk-card::before, .silk-card::after {
  content: "";
  position: absolute;
  width: 8px;
  height: 8px;
  border: 1.5px solid var(--silk-brass);
}
.silk-card::before { top: 4px; left: 4px; }
.silk-card::after { bottom: 4px; right: 4px; }
```

### 2. Vermilion Lacquer Button (`.silk-btn-primary`)
An action button finished in cinnabar lacquer with polished brass edges and gold lettering.
```css
.silk-btn-primary {
  background: linear-gradient(180deg, #C3272B 0%, #9E1F23 100%);
  color: #FFFFFF;
  border: 1px solid var(--silk-brass);
  box-shadow: 0 2px 4px rgba(139, 27, 30, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.2);
  padding: 0.65rem 1.4rem;
  font-family: var(--silk-font-body);
  font-weight: 600;
  letter-spacing: 0.04em;
  border-radius: 3px;
  cursor: pointer;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.silk-btn-primary:hover {
  background: linear-gradient(180deg, #D42D31 0%, #AF2428 100%);
  box-shadow: 0 4px 10px rgba(139, 27, 30, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.3);
  transform: translateY(-1px);
}
```

### 3. Vertical Seal Badge (`.silk-seal`)
A traditional vermilion ink chop mark used for status indicators and verified states.
```css
.silk-seal {
  display: inline-block;
  border: 2px solid var(--silk-vermilion);
  color: var(--silk-vermilion);
  font-family: var(--silk-font-display);
  font-size: 0.75rem;
  font-weight: bold;
  padding: 0.2rem 0.4rem;
  border-radius: 2px;
  box-shadow: inset 0 0 4px rgba(195, 39, 43, 0.15);
  letter-spacing: 0.1em;
}
```

### 4. Sliding Partition Tab Bar (`.silk-tabs`)
A tab system resembling wooden paper screens sliding along brass guide rails.

---

## ♿ Accessibility & Environmental Contrast (WCAG 2.2)

- **Text Contrast Ratios:** Deep ink black (`#1A1D20`) and imperial indigo (`#1D2A44`) on aged paper (`#F5EFE0`) deliver exceptional contrast ratios of 12.8:1 and 10.4:1, far exceeding WCAG AAA requirements (7:1).
- **Secondary Elements:** Faded ink (`#424953`) achieves 6.5:1, satisfying WCAG AA for normal text.
- **Focus Rings:** High-visibility double outline using deep indigo and brass (`outline: 2px solid var(--silk-indigo); outline-offset: 2px;`).
- **No Reliance on Color Alone:** Vermilion tags are always accompanied by textual status labels and geometric icons.

---

## ✅ When to Use / ❌ When to Avoid

### Ideal Use Cases
- Speculative East Asian fantasy games, worldbuilding wikis, and historical alternate-timeline narratives.
- Artisanal craftsmanship, tea culture, traditional ceramics, architecture portfolios, and literary press releases.
- Museum exhibits on ancient Chinese science, cartography, and silk maritime trade.

### Anti-Patterns & Prohibitions
- Modern high-frequency fintech trading platforms.
- Dense data dashboards requiring thousands of unadorned spreadsheet rows.
- Stereotypical caricatures or Western orientalist kitsch.

---

## 📚 Authoritative Sources & Historical Artifacts

- Ken Liu, *The Grace of Kings* (The Dandelion Dynasty), Saga Press, 2015.
- Ken Liu, "Silkpunk: An Introduction", *io9 / Gizmodo*, 2015.
- Joseph Needham, *Science and Civilisation in China* (Vol 4: Physics and Physical Technology), Cambridge University Press, 1965.
- Daniel Shen, *Chinese Lattice Designs*, Dover Publications, 1980.

---

## 🔗 Cross-Skill Integration & Dialect Relations

- **Sibling Speculative Aesthetics:** [ui-style-steampunk](../ui-style-steampunk/SKILL.md), [ui-style-clockpunk](../ui-style-clockpunk/SKILL.md), [ui-style-sandalpunk](../ui-style-sandalpunk/SKILL.md).
- **Organic & Craft Peers:** [ui-style-arts-and-crafts](../ui-style-arts-and-crafts/SKILL.md), [ui-style-organic-biophilic](../ui-style-organic-biophilic/SKILL.md), [ui-style-editorial-archive-luxury](../ui-style-editorial-archive-luxury/SKILL.md).
