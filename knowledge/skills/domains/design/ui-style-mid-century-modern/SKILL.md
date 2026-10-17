---
name: "ui-style-mid-century-modern"
description: "Provides the mid-century modern UI style (1945-1970s origin, revival from the late 1990s): clean lines without embellishment, honest materials, warm walnut and teal-orange palettes, organic-geometric shapes and generous whitespace, covering tokens, type pairing, layout, motion and WCAG contrast handling. Use when designing warm, human, design-literate brand, furniture, editorial or lifestyle surfaces that want modernist clarity with warmth."
---

# UI Style: Mid-Century Modern (MCM)

> *"The details are not the details. They make the design."*  
> — Charles & Ray Eames (1950s)

Mid-Century Modern (MCM) translates the golden age of postwar residential architecture and organic industrial design (1945–1970) into clean, human digital spaces. Exemplified by the Case Study Houses of Southern California, Scandinavian bentwood furniture (Alvar Aalto, Hans Wegner), and the molded plywood breakthroughs of Charles and Ray Eames, MCM balances geometric discipline with tactile warmth: oiled American walnut, warm cream paper, burnt terracotta, ocean teal, and gentle biomorphic curves.

---

## 🧭 When to Activate

- Designing modern furniture showcases, architectural practices, interior design ateliers, and premium lifestyle journals.
- Building hospitality portals, boutique real estate platforms, and culinary/coffee roaster brand experiences.
- Crafting human-centered consumer applications that require modernist simplicity without the cold sterile clinicality of corporate minimalism.
- Designing reading sanctuaries and editorial layouts celebrating physical craft and authentic materials.

---

## 🕰️ Definition, Lineage, and Timeline

- **1945–1966 (The Case Study House Program):** *Arts & Architecture* magazine sponsors Case Study Houses in California (Richard Neutra, Pierre Koenig, Craig Ellwood, Charles & Ray Eames). Julius Shulman's photography immortalizes floor-to-ceiling glass walls, indoor-outdoor continuity, and post-and-beam construction.
- **1948–1956 (The Molded Material Revolution):** Charles and Ray Eames pioneer compound-curve molded plywood and fiberglass shells, culminating in the iconic 1956 *Eames Lounge Chair & Ottoman (Model 670/671)*. Eero Saarinen designs the pedestal-base *Tulip Chair* (1957) and the sculptural *TWA Flight Center*.
- **1950s (Scandinavian & Brazilian Synthesis):** Alvar Aalto, Arne Jacobsen, and Hans Wegner fuse machine production with Danish craft; in Brazil, Lina Bo Bardi and Oscar Niemeyer introduce sensual tropical concrete and native hardwoods.
- **1990s–Present (The Digital Renaissance):** Revived by Herman Miller and Dwell magazine, MCM establishes the aesthetic benchmark for refined, tasteful, timeless web design.

### Absolute Style Vetos (What Mid-Century Modern is NOT)
- ❌ **NOT Atompunk ([ui-style-atompunk](../ui-style-atompunk/SKILL.md)):** Atompunk is Cold War nuclear militarism, convex CRT tubes, radar scopes, and radioactive fallout shelters. MCM is domestic residential architecture, organic bentwood, and Californian sunlight.
- ❌ **NOT Postmodern Memphis ([ui-style-memphis](../ui-style-memphis/SKILL.md)):** Memphis is 1980s irony, neon plastic laminate, and clashing squiggles. MCM is 1950s honest natural materials, oiled walnut, and functional ergonomics.
- ❌ **NOT Cold Swiss Minimalism ([ui-style-swiss-web-minimalism](../ui-style-swiss-web-minimalism/SKILL.md)):** Swiss style is sterile, purely objective, and dominated by ink black on harsh white paper. MCM is warm, welcoming, and rooted in earth tones.

---

## 🎨 Visual DNA & Subgenre Taxonomy

```
+------------------------------------------------------------------------------------+
|                         MID-CENTURY MODERN TAXONOMY                                |
+------------------------------------------------------------------------------------+
| Californian Case Study Modernism     | Scandinavian Bentwood & Craft               |
| - Floor-to-ceiling architectural glass| - Molded walnut plywood & woven cane       |
| - Post-and-beam structural grid lines | - Organic kidney curves & tapered legs     |
| - Oiled American walnut & bone cream  | - Muted seafoam teal & mustard ochre       |
| - Indoor-outdoor organic continuity   | - Gentle humanist typography & wide margins|
+------------------------------------------------------------------------------------+
```

### Visual Pillars
1. **Material Honesty & Wood Grain Tones:** Surfaces evoke natural materials rather than artificial plastic:
   - **Oiled American Walnut:** `#5C3A21` (Rich dark wood grain)
   - **Warm Linen Paper:** `#F5EFE6` (Soft unbleached parchment)
   - **Burnt Terracotta:** `#C8553D` (Warm earthenware clay)
   - **Pacific Seafoam Teal:** `#2E7777` (Muted ocean mineral)
   - **Mustard Ochre:** `#D9A441` (Sun-baked pigment)
   - **Deep Charcoal Bark:** `#261D17` (Organic ink)
2. **Organic Biomorphic Curvature:** Kidney-table silhouettes, boomerang curves, and asymmetric corner radii (`border-radius: 28px 4px 28px 4px`).
3. **Architectural Post-and-Beam Cadence:** Structural sections are bounded by warm walnut rules and wide panoramic margins simulating floor-to-ceiling glass pavilions.

---

## 📐 Lighting Physics, Specular Splits & Surfaces

MCM simulates warm, natural afternoon sunlight streaming through expansive architectural windows:
- **Lighting Model:** Warm directional ambient daylight (color temperature ~`3500K`). Soft, diffused contact shadows indicating physical wooden weight.
- **Surface Elevation:** Expressed through delicate wood elevation: `box-shadow: 0 4px 20px -2px rgba(38, 29, 23, 0.08)`.
- **Material Edge:** Clean 1px hairlines in soft walnut or bone: `border: 1px solid oklch(0.35 0.04 55 / 0.15)`.

---

## 🏷️ Complete Design Tokens

```css
:root {
  /* Architectural Material Palette */
  --mcm-bg-canvas: #F5EFE6;          /* Warm Bone Linen */
  --mcm-bg-surface: #FFFFFF;         /* Crisp Plaster White */
  --mcm-bg-wood: #5C3A21;            /* Oiled American Walnut */
  --mcm-bg-subtle: #EAE2D5;          /* Sandy Travertine */

  /* Typographic Inks */
  --mcm-text-ink: #261D17;           /* Deep Charcoal Bark */
  --mcm-text-secondary: #5C5248;     /* Soft Umber */
  --mcm-text-muted: #8A7E73;         /* Weathered Cane */

  /* Iconic Mid-Century Accents */
  --mcm-accent-teal: #2E7777;        /* Pacific Seafoam Teal */
  --mcm-accent-orange: #C8553D;      /* Burnt Terracotta */
  --mcm-accent-mustard: #D9A441;     /* Mustard Ochre */

  /* Structural Geometry */
  --mcm-radius-organic: 28px 4px 28px 4px;
  --mcm-radius-pill: 9999px;
  --mcm-border-soft: 1px solid oklch(0.25 0.03 55 / 0.10);
  --mcm-border-wood: 2px solid var(--mcm-bg-wood);

  /* Calm & Measured Transitions */
  --mcm-ease: cubic-bezier(0.25, 0.8, 0.25, 1.0);
  --mcm-duration: 260ms;
}

[data-theme="dark"] {
  /* Evening Lounge Mode */
  --mcm-bg-canvas: #1B1512;          /* Night Walnut Interior */
  --mcm-bg-surface: #241C18;         /* Dark Leather Panel */
  --mcm-bg-subtle: #2E2420;
  --mcm-text-ink: #F5EFE6;
  --mcm-text-secondary: #A89E94;
  --mcm-text-muted: #6E6359;
  --mcm-border-soft: 1px solid oklch(0.95 0.02 75 / 0.10);
}
```

---

## 🔤 Typography & Lettering Architecture

Typography pairs geometric modernist display caps with graceful humanist body text:
- **Display Headlines:** Geometric sans-serifs inspired by early California modernism (`"Josefin Sans"`, `"Neutraface"`, `"Futura"`), `600` or `700` weight, relaxed tracking (`0.05em`), uppercase or sentence case.
- **Section Subheadings:** Warm, human transitional serifs (`"Source Serif 4"`, `"Charter"`), `500` weight, `20px` to `24px`.
- **Body & Essays:** `"Source Serif 4"`, `"Georgia"`, `400` weight, `16px` to `18px`, `line-height: 1.65`, optimal measure `64ch`.

---

## 🖱️ Interaction Dynamics, Sound Cues & Motion

- **Sliding Panel Transition:** State changes and card expansions glide with the measured grace of solid wood sliding shoji doors (`260ms var(--mcm-ease)`).
- **Subtle Wood Accent Shift:** Hovering links or cards expands an organic terracotta or teal indicator line from the left edge.
- **Acoustic Profile:** Rich wooden haptic resonance: a warm 30ms hollow walnut tap (`280Hz` wood resonance) upon card activation.

---

## 🧩 Canonical Component Specifications

### 1. Organic Bentwood Furniture Showcase Card

```html
<article class="mcm-card">
  <div class="mcm-card-media">
    <img src="eames-lounge.jpg" alt="Molded Plywood Lounge Chair" class="mcm-img" loading="lazy" />
    <span class="mcm-pill">Iconic Design · 1956</span>
  </div>
  <div class="mcm-card-content">
    <div class="mcm-eyebrow">CHARLES &amp; RAY EAMES</div>
    <h3 class="mcm-card-title">Molded Plywood Lounge Chair &amp; Ottoman</h3>
    <p class="mcm-card-desc">Seven-ply Santos Palisander veneer with supple full-grain black leather upholstery and cast aluminum swivel base.</p>
    <div class="mcm-card-footer">
      <span class="mcm-spec">Manufactured by Herman Miller</span>
      <button class="mcm-btn">Explore Specification</button>
    </div>
  </div>
</article>
```

```css
.mcm-card {
  background-color: var(--mcm-bg-surface);
  border: var(--mcm-border-soft);
  border-radius: var(--mcm-radius-organic);
  overflow: hidden;
  max-width: 420px;
  box-shadow: 0 4px 20px -4px rgba(38, 29, 23, 0.06);
  display: flex;
  flex-direction: column;
  transition: transform var(--mcm-duration) var(--mcm-ease),
              box-shadow var(--mcm-duration) var(--mcm-ease);
}

.mcm-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 30px -6px rgba(38, 29, 23, 0.12);
}

.mcm-card-media {
  position: relative;
  width: 100%;
  aspect-ratio: 4 / 3;
  background-color: var(--mcm-bg-subtle);
  overflow: hidden;
}

.mcm-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 500ms var(--mcm-ease);
}

.mcm-card:hover .mcm-img {
  transform: scale(1.02);
}

.mcm-pill {
  position: absolute;
  top: 14px;
  right: 14px;
  background-color: var(--mcm-bg-canvas);
  color: var(--mcm-text-ink);
  font-family: "Josefin Sans", sans-serif;
  font-size: 11px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: var(--mcm-radius-pill);
  border: var(--mcm-border-soft);
}

.mcm-card-content {
  padding: 28px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.mcm-eyebrow {
  font-family: "Josefin Sans", sans-serif;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.12em;
  color: var(--mcm-accent-orange);
}

.mcm-card-title {
  font-family: "Josefin Sans", sans-serif;
  font-size: 22px;
  font-weight: 700;
  line-height: 1.25;
  color: var(--mcm-text-ink);
  margin: 0;
}

.mcm-card-desc {
  font-family: "Source Serif 4", Georgia, serif;
  font-size: 14px;
  line-height: 1.6;
  color: var(--mcm-text-secondary);
  margin: 0 0 12px 0;
}

.mcm-card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 16px;
  border-top: var(--mcm-border-soft);
}

.mcm-spec {
  font-size: 11px;
  color: var(--mcm-text-muted);
}

.mcm-btn {
  background-color: var(--mcm-accent-teal);
  color: #FFFFFF;
  border: none;
  font-family: "Josefin Sans", sans-serif;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.05em;
  padding: 8px 16px;
  border-radius: var(--mcm-radius-pill);
  cursor: pointer;
  transition: opacity 150ms ease;
}

.mcm-btn:hover {
  opacity: 0.90;
}
```

---

## ♿ Accessibility & Environmental Contrast

- **WCAG 2.2 Contrast Math on Warm Linen:**
  - Charcoal ink (`--mcm-text-ink` `#261D17`) over warm linen canvas (`#F5EFE6`) delivers an exceptional **11.4:1** contrast ratio (WCAG AAA).
  - Pacific Seafoam Teal (`--mcm-accent-teal` `#2E7777`) over linen delivers **4.8:1** (conforming to WCAG AA for normal text).
  - Mustard Ochre (`#D9A441`) must NOT be used for small body text over white or linen; it is strictly an accent for badges, icons, and non-text focus indicators.
- **Focus Rings:** Interactive elements receive a clear, high-contrast focus indicator: `outline: 3px solid var(--mcm-accent-teal); outline-offset: 3px;`.
- **Reduced Motion:** Sliding transitions and image zoom scales resolve instantly when `prefers-reduced-motion: reduce` is detected.

---

## ✅ When to Use / ❌ When to Avoid

### Appropriate Scenarios
- Architecture and interior design studios, furniture and decor e-commerce.
- Cultural magazines, culinary and boutique roaster brands, lifestyle blogs.
- Consumer applications seeking warmth, approachability, and mid-century elegance.

### Inappropriate Scenarios
- Gritty military combat gaming or dark cyberpunk neon themes.
- Cold, utilitarian corporate compliance portals or server terminal logs.

---

## 📚 Authoritative Sources & Historical Artifacts

1. **Eames, Charles & Ray (1950s–1970s):** *Design Monograph and Archives*, Eames Office / Vitra Design Museum.
2. **Smith, Elizabeth A.T. (2002):** *Case Study Houses: The Complete CSH Program 1945–1966*, Taschen.
3. **Shulman, Julius (1998):** *Architecture and its Photography*, Taschen.

---

## 🔗 Cross-Skill Integration & Dialect Relations

- Direct cousin to [ui-style-nordic](../ui-style-nordic/SKILL.md) and [ui-style-calm-quiet-ui](../ui-style-calm-quiet-ui/SKILL.md).
- Contrasts with [ui-style-atompunk](../ui-style-atompunk/SKILL.md) through domestic organic warmth rather than Cold War industrial militarism.
