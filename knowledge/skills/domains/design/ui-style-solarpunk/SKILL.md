---
name: "ui-style-solarpunk"
description: "Provides the canonical Solarpunk & Biomorphic Ecological UI style (2008-present): optimistic ecological futurism, solar energy infrastructure, stained-glass photovoltaics, biomorphic Voronoi cell partitioning, warm oatmeal and sun-gold palettes, low-carbon performance budgets, and civic collective empowerment. Use when designing renewable energy platforms, climate technology, organic agriculture portals, or sustainable civic cooperatives."
---

# UI Style: Solarpunk & Biomorphic Ecological

**Solarpunk** is the definitive ecological retro-futurism and socio-technical movement answering dystopian cyberpunk with tangible, solar-powered optimism. Envisioning a world where human civilization has achieved ecological symbiosis with planetary ecosystems, Solarpunk merges renewable energy infrastructure (stained-glass solar panels, wind harvesters) with biomimetic parametric engineering (Voronoi cellular partitioning, Fibonacci distributions) and warm botanical craftsmanship (natural linen textures, terracotta clay, leaf chlorophyll).

---

## 🧭 When to Activate

- Designing climate software, renewable microgrid monitors, carbon tracking tools, or municipal energy-sharing portals.
- Sustainable fashion storefronts, regenerative agriculture platforms, mutual-aid networks, or civic-tech cooperatives.
- Replacing sterile corporate "greenwashing" with authentic low-carbon web engineering, transparent environmental metrics, and empowering collective copy.

---

## 🕰️ Definition, Lineage, and Timeline

- **Origins & Manifestos:** Coined in 2008 in the blog essay *"From Steampunk to Solarpunk"*. Solidified in Adam Flynn's *"Solarpunk: Notes toward a manifesto"* (Project Hieroglyph, 2014) and the collective 2019 *Solarpunk Manifesto*.
- **The Biomimetic & Architectural Heritage:** Draws inspiration from the Art Nouveau architecture of Antoni Gaudí and Hector Guimard, the organic structural engineering of Frei Otto, and modern parametric biomimicry (Neri Oxman, MIT Media Lab).
- **Distinctions from Neighboring Styles:**
  - Unlike **Organic / Biophilic** (neutral corporate wellness, soothing houseplants in modern offices, calm retreat), Solarpunk is an active sociopolitical movement celebrating civic agency, clean technology, and decentralized solar infrastructure.
  - Unlike **Lunarpunk** (nocturnal, encrypted, privacy-focused, zero-knowledge cryptography, dark starlight forest), Solarpunk is daytime, sunlit, transparent, collective, and radiant.
  - Unlike **Biopunk** (dystopian, gene-editing black clinics, fluorescent GFP biohazard tension), Solarpunk is clean, life-affirming, and harmonious.
- **Absolute Veto:** Superficial "greenwashing" consisting of stock leaf photos pasted onto bloated, heavy corporate landing pages. Solarpunk interfaces must adhere to strict low-carbon performance budgets (sub-500KB page transfers, efficient SVG rendering, zero wasteful autoplay video).

---

## 🎨 Visual DNA & Subgenre Taxonomy

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 SOLARPUNK VISUAL MATRIX                                │
├────────────────────────────┬────────────────────────────┬──────────────────────────────┤
│ 1. Civic Solar Grid        │ 2. Artisanal Pastoral      │ 3. Parametric Biomimetic     │
│ • Photovoltaic glass panels│ • Oatmeal linen grounds    │ • Voronoi cellular meshes    │
│ • Sun-gold & photosynthetic│ • Terracotta clay accents  │ • Leaf venation branch paths │
│ • Renewable energy meters  │ • Warm humanist serifs     │ • Asymmetric organic curves  │
└────────────────────────────┴────────────────────────────┴──────────────────────────────┘
```

- **Palettes:**
  - *Solar Radiance:* Sunbeam gold (`#F2B632`), photovoltaic amber (`#F77F00`), terracotta tile (`#C8643B`).
  - *Photosynthetic Life:* Leaf chlorophyll green (`#2F7D4F`), moss green (`#8CC084`), bio-luminescent cyan (`#00F5D4`).
  - *Natural Grounds:* Oatmeal linen (`#F7F4EE`), warm fertile cream (`#FBF6E9`), and deep rich forest loam (`#0B1D19`) for dark mode.
- **Organic Partitions:** Asymmetric curved containers (`border-radius: 28px 14px 32px 16px`), Voronoi polygon cell boundaries, and delicate 1px brass/leaf outlines.
- **Surface Textures:** Natural woven linen texture, stained-glass solar cell tessellation, and sunlight radial gradients.

---

## 📐 Lighting Physics, Specular Splits & Surfaces

1. **Sunlit Solar Gradient:**
   - Warm overhead sunlight filtering through leafy canopy onto clean surfaces.
   ```css
   background-color: #fbf6e9;
   background-image: radial-gradient(circle at 80% 10%, rgba(242, 182, 50, 0.25) 0%, transparent 60%);
   box-shadow: 0 8px 24px rgba(27, 58, 42, 0.08);
   ```
2. **Photovoltaic Glass Bezel:**
   - Subtle geometric hexagonal or Voronoi membrane line catching the light.
   ```css
   border: 1.5px solid rgba(47, 125, 79, 0.35);
   box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.6), 0 4px 16px rgba(47, 125, 79, 0.1);
   ```

---

## 🏷️ Complete Design Tokens

```css
:root {
  /* Natural Substrates */
  --solar-paper-bg: #FBF6E9;
  --solar-paper-surface: #FFFFFF;
  --solar-paper-card: #F7F4EE;
  --solar-loam-dark: #0B1D19;

  /* Solar Energy & Plant Dyes */
  --solar-gold: #F2B632;
  --solar-gold-glow: rgba(242, 182, 50, 0.35);
  --solar-amber: #F77F00;
  --solar-terracotta: #C8643B;
  --solar-leaf-green: #2F7D4F;
  --solar-moss: #8CC084;
  --solar-cyan-energy: #00F5D4;

  /* Text & Loam Ink */
  --solar-ink-primary: #1B3A2A;
  --solar-ink-muted: #4A6B59;
  --solar-ink-light: #F7F4EE;

  /* Geometry & Radius */
  --solar-radius-organic: 28px 14px 32px 16px;
  --solar-radius-pill: 9999px;
  --solar-border: 1.5px solid var(--solar-moss);

  /* Typography */
  --solar-font-display: 'Fraunces', 'Cormorant Garamond', serif;
  --solar-font-body: 'Plus Jakarta Sans', 'Nunito', system-ui, sans-serif;
  --solar-font-mono: 'Space Mono', monospace;
}
```

---

## 🔤 Typography & Lettering Architecture

- **Primary Display Headings:** Warm, calligraphic humanist serifs (*Fraunces*, *Cormorant Garamond*, *Recoleta*) featuring soft organic curves and optical weight axes.
- **Body & Paragraphs:** Clear, approachable contemporary sans (*Plus Jakarta Sans*, *Nunito*) set in deep forest loam (`#1B3A2A`) with 1.65 line-height.
- **Telemetry & Energy Metrics:** Fixed-pitch monospaced fonts (*Space Mono*) for kilowatt-hour readouts (kWh), solar panel efficiency percentages, and carbon offsets.

---

## 🖱️ Interaction Dynamics, Sound Cues & Motion

- **Sprouting Growth Reveals:** Elements enter the viewport with gentle organic scaling (`transform: scale(0.96) -> scale(1.0)` over 350ms ease-out).
- **Living Circadian Pulse:** Solar energy indicators pulse with a slow, 4-second biological breathing cycle.
- **Smooth Leaf Settle:** Interactive buttons settle with soft organic deceleration rather than harsh mechanical snapping.
- **Motion Gating:** When `prefers-reduced-motion: reduce` is enabled, all growth transforms and breathing pulses freeze into static, clean layouts.

---

## 🧩 Canonical Component Specifications

### 1. Organic Solar Cell Card (`.solar-card`)
An asymmetric container finished with moss green borders, sunlit gradient, and deep forest typography.
```html
<article class="solar-card">
  <div class="solar-card-header">
    <span class="solar-badge">CIVIC MICROGRID // DISTRICT 4</span>
    <h3 class="solar-title">Community Battery Reserve</h3>
  </div>
  <p class="solar-text">Solar generation surplus: 142.8 kWh stored across neighborhood lithium iron phosphate cells.</p>
</article>
```
```css
.solar-card {
  background: var(--solar-paper-surface);
  color: var(--solar-ink-primary);
  border: var(--solar-border);
  border-radius: var(--solar-radius-organic);
  box-shadow: 0 8px 24px rgba(27, 58, 42, 0.08);
  padding: 2rem;
  position: relative;
  transition: transform 0.25s ease-out, box-shadow 0.25s ease-out;
}
.solar-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 14px 32px rgba(27, 58, 42, 0.14);
}
.solar-badge {
  display: inline-block;
  background: var(--solar-gold);
  color: #1B3A2A;
  font-family: var(--solar-font-body);
  font-weight: 700;
  font-size: 0.75rem;
  padding: 0.25rem 0.75rem;
  border-radius: var(--solar-radius-pill);
  margin-bottom: 0.75rem;
}
```

### 2. Terracotta Action Button (`.solar-btn`)
An action trigger finished in warm clay terracotta with gold hover elevation.
```css
.solar-btn {
  background: var(--solar-terracotta);
  color: #FFFFFF;
  font-family: var(--solar-font-body);
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  padding: 0.75rem 1.8rem;
  border: none;
  border-radius: var(--solar-radius-pill);
  box-shadow: 0 4px 14px rgba(200, 100, 59, 0.3);
  cursor: pointer;
  transition: background 0.2s ease, transform 0.15s ease, box-shadow 0.15s ease;
}
.solar-btn:hover {
  background: #B85630;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(200, 100, 59, 0.4);
}
```

### 3. Low-Carbon Eco Switch (`.solar-eco-toggle`)
A toggle allowing visitors to disable decorative images and webfonts, cutting network transfer weight.

### 4. Stained-Glass Solar Banner (`.solar-glass-banner`)
A header ribbon featuring hexagonal Voronoi photovoltaic facets catching natural sunlight.

---

## ♿ Accessibility & Environmental Contrast (WCAG 2.2)

- **Contrast Mathematics:** Deep forest loam (`#1B3A2A`) on warm paper (`#FBF6E9`) delivers a 10.4:1 contrast ratio (exceeding WCAG AAA 7:1).
- **Color Independence (WCAG 1.4.1):** Never use green alone for success and red alone for error; always accompany solar metrics with clear textual descriptions and explicit icons.
- **Low-Carbon Performance Budget:** Respect low-bandwidth networks: eliminate render-blocking webfont chains, compress SVG assets, and keep total initial HTML+CSS+JS transfer under 250KB.
- **Focus Rings:** Unambiguous emerald outline (`outline: 3px solid var(--solar-leaf-green); outline-offset: 3px;`).

---

## ✅ When to Use / ❌ When to Avoid

### Ideal Use Cases
- Renewable energy platforms, microgrid cooperatives, and climate action dashboards.
- Regenerative agriculture, community gardens, organic food producers, and slow living blogs.
- Sustainable architecture, biomimicry engineering hubs, and ecological literature portals.

### Anti-Patterns & Prohibitions
- Fossil fuel corporations or non-sustainable entities seeking superficial greenwashing.
- High-frequency dark-mode financial trading desks where botanical curves waste critical telemetry real estate.
- Autoplaying heavy background video that consumes excess bandwidth and contradicts the low-carbon ethos.

---

## 📚 Authoritative Sources & Historical Artifacts

- Adam Flynn, "Solarpunk: Notes toward a manifesto", *Project Hieroglyph*, 2014.
- Neri Oxman, *Age of Entanglement*, MIT Media Lab, 2016.
- Sustainable Web Design, *Web Sustainability Guidelines (WSG)*, 2023.
- W3C, *Web Content Accessibility Guidelines 2.2* (1.4.1, 1.4.3).

---

## 🔗 Cross-Skill Integration & Dialect Relations

- **Sibling Ecological Styles:** [ui-style-lunarpunk](../ui-style-lunarpunk/SKILL.md), [ui-style-organic-biophilic](../ui-style-organic-biophilic/SKILL.md), [ui-style-silkpunk](../ui-style-silkpunk/SKILL.md).
- **Craft & Tactile Peers:** [ui-style-arts-and-crafts](../ui-style-arts-and-crafts/SKILL.md), [ui-style-art-nouveau](../ui-style-art-nouveau/SKILL.md), [ui-style-card-based-ui](../ui-style-card-based-ui/SKILL.md).
