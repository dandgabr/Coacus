---
name: "ui-style-art-deco"
description: "Provides the Art Deco UI style (1910s-1930s lineage, revived for the web): symmetrical geometric ornament, sunbursts, chevrons and stepped forms in gold, black and jewel tones, covering tokens, line-art and SVG pattern construction, high-contrast display type, ceremonial motion and contrast pitfalls of metallic palettes. Use when designing luxury, hospitality, cinema, jazz-age or premium brand surfaces that need glamour with structure."
---

# UI Style: Art Deco (Style Moderne)

> *"Art Deco is the machine-age symphony: mathematical symmetry, ziggurat spires, polished brass, and the unapologetic celebration of metropolitan glamour and industrial optimism."*  
> — Parisian Decorative Arts Retrospectives (1925)

Art Deco (derived from the 1925 Paris *Exposition Internationale des Arts Décoratifs et Industriels Modernes*) represents the zenith of machine-age luxury, architectural geometry, and Jazz Age optimism. Rejecting both the sinuous botanical asymmetry of Art Nouveau and the spartan functionalism of Bauhaus, Art Deco combines monumental symmetry, stepped ziggurats, radiating sunbursts, and double-line gold filigree over midnight obsidian, imperial emerald, and champagne ivory.

---

## 🧭 When to Activate

- Designing luxury hotels, private cocktail lounges, heritage jewelry brands, and fine horology portals.
- Crafting cinema festivals, jazz club programs, theater ticketing platforms, and Great Gatsby gala invitations.
- Building high-prestige culinary and spirits brand pages where metallic refinement and structured ornamentation reign.
- Transforming standard promotional campaigns into majestic, ceremonial experiences.

---

## 🕰️ Definition, Lineage, and Timeline

- **1910s (Early Parisian Emergence):** Emerging from Cubism, the Ballets Russes, and the Vienna Secession, French designers (Paul Poiret, Émile-Jacques Ruhlmann) pioneer a new geometric decorative style.
- **November 1922 (The King Tutankhamun Catalyst):** Howard Carter unearths the tomb of Tutankhamun. Ancient Egyptian motifs—stepped pyramids, lotus fans, lapis lazuli, and gilded sarcophagi—fuse into European and American decorative art.
- **April–October 1925 (The Paris Expo):** The *Exposition Internationale des Arts Décoratifs et Industriels Modernes* in Paris establishes the global movement.
- **1930 (The Skyscraper Zenith):** William Van Alen completes the **Chrysler Building** in New York, crowning the skyline with radiating sunburst stainless-steel arches and eagle gargoyles.
- **1930s (Streamline Moderne Evolution):** The Great Depression tempers high ornament with aerodynamic industrial curves, nautical portholes, and speed lines.

### Absolute Style Vetos (What Art Deco is NOT)
- ❌ **NOT Art Nouveau ([ui-style-art-nouveau](../ui-style-art-nouveau/SKILL.md)):** Art Nouveau is organic, asymmetrical, and dominated by serpentine "whiplash" botanical curves and Mucha-style flowing hair. Art Deco is strictly geometric, machine-tooled, symmetrical, and architectural.
- ❌ **NOT Dieselpunk ([ui-style-dieselpunk](../ui-style-dieselpunk/SKILL.md)):** Dieselpunk is greasy, heavily riveted, dystopian, and militaristic. Art Deco is sparkling, high-society, refined, and celebratory.
- ❌ **NOT Bauhaus Functionalism ([ui-style-bauhaus](../ui-style-bauhaus/SKILL.md)):** Bauhaus rejects all ornament as dishonest bourgeois decoration. Art Deco embraces ornament as the highest expression of craft and metropolitan pride.

---

## 🎨 Visual DNA & Subgenre Taxonomy

```
+------------------------------------------------------------------------------------+
|                                ART DECO TAXONOMY                                   |
+------------------------------------------------------------------------------------+
| High Jazz Age Zigzag (1920-1929)     | Streamline Moderne (1930-1939)              |
| - Polished bullion gold & obsidian   | - Aerodynamic horizontal speed lines        |
| - Radiating sunbursts & chevron fans | - Rounded nautical corners and chrome rails |
| - Stepped ziggurat frame corners     | - Muted marine blues and silver foil        |
| - Concentric hairline border framing | - Low-profile condensed typography          |
+------------------------------------------------------------------------------------+
```

### Visual Pillars
1. **Geometric Symmetry & Stepped Ziggurats:** Layouts are axially balanced, drawing the eye upwards through stepped vertical pillars, chevron spires, and cascading archways.
2. **Double-Hairline Filigree:** Cards and containers feature parallel 1px gold rules separated by a 4px–6px offset channel (`outline: 1px solid var(--deco-gold); outline-offset: 4px`).
3. **The Metropolitan Jewel Palette:**
   - **Obsidian Black:** `#0D0E12` (Deep lacquered ebony)
   - **Bullion Gold:** `#D4AF37` / `#C9A227` (Polished yellow brass)
   - **Champagne Ivory:** `#F5ECD7` (Warm velvet parchment)
   - **Imperial Emerald:** `#0C2E25` (Dark malachite jewel tone)
   - **Midnight Sapphire:** `#09182B` (Deep nocturnal ocean)

---

## 📐 Lighting Physics, Specular Splits & Surfaces

Art Deco renders surfaces as polished machine-age architectural metals:
- **Specular Gleam:** Linear specular gradients simulating brushed brass and mirror-polished bronze: `linear-gradient(135deg, #ECC86A 0%, #C9A227 40%, #7A5C10 70%, #C9A227 100%)`.
- **Surface Elevation:** Expressed through layered metallic borders and inset shadows, rather than soft diffuse Gaussian blurs.
- **Sunburst Shader:**
  ```css
  background: repeating-conic-gradient(
    from 0deg at 50% 100%,
    var(--deco-gold) 0deg 2deg,
    transparent 2deg 10deg
  );
  mask: linear-gradient(to top, rgba(0,0,0,1) 0%, transparent 80%);
  ```

---

## 🏷️ Complete Design Tokens

```css
:root {
  /* Rich Nocturnal Jewel Base */
  --deco-bg-canvas: #0D0E12;         /* Lacquered Obsidian */
  --deco-bg-surface: #14171E;        /* Elevated Ebony Panel */
  --deco-bg-emerald: #0C2E25;        /* Imperial Malachite */

  /* Gilded Metallics */
  --deco-gold-bright: #F3DC82;       /* Polished Gilt Highlight */
  --deco-gold-core: #D4AF37;         /* Classic Bullion Gold */
  --deco-gold-dark: #8E701D;         /* Antique Bronze */
  --deco-gold-linear: linear-gradient(135deg, #F3DC82 0%, #D4AF37 50%, #8E701D 100%);

  /* Typography Colors */
  --deco-text-gold: #D4AF37;
  --deco-title-ink: #D4AF37;
  --deco-detail-ink: #F3DC82;
  --deco-action-ink: #D4AF37;
  --deco-text-ivory: #F5ECD7;
  --deco-text-muted: #8E8A7D;

  /* Architectural Framing */
  --deco-border-gold: 1px solid var(--deco-gold-core);
  --deco-border-dual: 1px solid var(--deco-gold-core);
  --deco-offset-gap: 4px;

  /* Ceremonial Motion */
  --deco-ease: cubic-bezier(0.16, 1, 0.3, 1);
  --deco-duration: 450ms;
}

[data-theme="light"] {
  /* High-Society Champagne Daylight */
  --deco-bg-canvas: #FAF6ED;
  --deco-bg-surface: #FFFFFF;
  --deco-text-ivory: #0D0E12;
  --deco-text-muted: #665F52;
  --deco-title-ink: #0D0E12;
  --deco-detail-ink: #665F52;
  --deco-action-ink: #0D0E12;
}
```

---

## 🔤 Typography & Lettering Architecture

Art Deco typography embodies the grand marquee displays of Broadway and Paris:
- **Primary Display Titles:** High-contrast geometric capitals (`"Poiret One"`, `"Broadway"`, `"Limelight"`, or `"Josefin Sans"`). Set in uppercase (`text-transform: uppercase`), with expansive tracking (`letter-spacing: 0.18em`) and high stem-to-crossbar ratios.
- **Section Eyebrows & Metadata:** Clean geometric sans (`"Josefin Sans"`, `"Futura"`), `600` weight, `11px`, `letter-spacing: 0.22em`, centered.
- **Body Text:** Transitional serif or refined sans (`"Playfair Display"`, `"Cormorant"`), `400` weight, `15px` to `16px`, line-height `1.6`, centered or justified within framed borders.

---

## 🖱️ Interaction Dynamics, Sound Cues & Motion

- **Ceremonial Border Draw:** Interactive cards enter with a gold line drawing around their perimeter using SVG `stroke-dashoffset` over `500ms`.
- **Center-Out Underline Expansion:** Interactive menu links expand a gilded underline outwards from the center on hover (`transform: scaleX(0) -> scaleX(1)`).
- **Acoustic Profile:** Heavy crystal-glass and brass chime: a delicate 35ms bell chime (`1800Hz` bell harmonic) upon trigger activation.

---

## 🧩 Canonical Component Specifications

### 1. Symmetrical Gilded Portal Frame Card

```html
<article class="deco-frame-card">
  <div class="deco-corner-accent top-left"></div>
  <div class="deco-corner-accent top-right"></div>
  <div class="deco-card-content">
    <span class="deco-eyebrow">GRAND SOIREE · EST. 1925</span>
    <h3 class="deco-card-title">THE CHRYSLER SALON</h3>
    <div class="deco-chevron-divider" aria-hidden="true">◆ ◆ ◆</div>
    <p class="deco-card-desc">An evening of bespoke jazz orchestration, vintage champagne vintages, and high-society architectural conversation.</p>
    <a href="#reserve" class="deco-btn">RESERVE TABLE</a>
  </div>
  <div class="deco-corner-accent bottom-left"></div>
  <div class="deco-corner-accent bottom-right"></div>
</article>
```

```css
.deco-frame-card {
  background-color: var(--deco-bg-surface);
  border: var(--deco-border-gold);
  outline: 1px solid var(--deco-gold-core);
  outline-offset: var(--deco-offset-gap);
  padding: 40px 32px;
  max-width: 440px;
  margin: 20px auto;
  position: relative;
  text-align: center;
  box-shadow: 0 12px 30px -10px rgba(0, 0, 0, 0.7);
}

.deco-card-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 14px;
}

.deco-eyebrow {
  font-family: "Josefin Sans", sans-serif;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.22em;
  color: var(--deco-detail-ink);
}

.deco-card-title {
  font-family: "Poiret One", serif;
  font-size: 28px;
  font-weight: 700;
  letter-spacing: 0.15em;
  color: var(--deco-title-ink);
  margin: 0;
}

.deco-chevron-divider {
  color: var(--deco-detail-ink);
  font-size: 10px;
  letter-spacing: 0.3em;
  margin: 4px 0;
}

.deco-card-desc {
  font-family: "Playfair Display", Georgia, serif;
  font-size: 14px;
  line-height: 1.6;
  color: var(--deco-text-ivory);
  margin: 0 0 12px 0;
}

.deco-btn {
  display: inline-block;
  background: transparent;
  color: var(--deco-action-ink);
  border: var(--deco-border-gold);
  font-family: "Josefin Sans", sans-serif;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.20em;
  padding: 10px 24px;
  text-decoration: none;
  transition: all var(--deco-duration) var(--deco-ease);
}

.deco-btn:hover {
  background-color: var(--deco-gold-core);
  color: #0D0E12;
  box-shadow: 0 0 15px rgba(212, 175, 55, 0.4);
}
```

---

## ♿ Accessibility & Environmental Contrast

- **WCAG 2.2 Gold Contrast Compliance:** Pale gold on pure white yields low contrast. To meet accessibility standards:
  - Gold text (`--deco-text-gold` `#D4AF37`) over Obsidian Black (`#0D0E12`) yields an outstanding **8.2:1** contrast ratio (WCAG AAA).
  - Champagne Ivory (`#F5ECD7`) over Obsidian yields **14.1:1** (WCAG AAA).
  - On light mode canvases, text must switch to deep Obsidian ink, using gold strictly for borders and non-text elements.
- **Focus Rings:** Buttons and interactive links receive a solid ivory outline: `outline: 2px solid var(--deco-text-ivory); outline-offset: 4px;`.
- **Reduced Motion:** Complex conic sunbursts and line-draw animations freeze immediately when `prefers-reduced-motion: reduce` is detected.

---

## ✅ When to Use / ❌ When to Avoid

### Appropriate Scenarios
- Luxury hospitality, five-star heritage hotels, Michelin-starred fine dining.
- Cinema and performing arts galas, high-end spirits distillers, luxury horology.
- High-society charity auctions and classical music festivals.

### Inappropriate Scenarios
- Casual low-cost fast food apps or utility budgeting tools.
- Modern software developer tooling, continuous integration consoles, or terminal monitors.

---

## 📚 Authoritative Sources & Historical Artifacts

1. **Benton, Charlotte, Benton, Tim & Wood, Ghislaine (2003):** *Art Deco 1910–1939*, Victoria and Albert Museum.
2. **Van Alen, William (1930):** *Architectural Drawings and Spire Sunburst Specifications of the Chrysler Building*.
3. **Duncan, Alastair (1988):** *Art Deco Style*, Thames & Hudson.

---

## 🔗 Cross-Skill Integration & Dialect Relations

- Historical and aesthetic successor to [ui-style-art-nouveau](../ui-style-art-nouveau/SKILL.md) and contemporary foil to [ui-style-bauhaus](../ui-style-bauhaus/SKILL.md).
- Contrasts with [ui-style-dieselpunk](../ui-style-dieselpunk/SKILL.md) through metropolitan sophistication and gilded cleanliness.
## Appearance and Interaction Verification

Introduce semantic title, eyebrow and action ink roles and retarget gilded card selectors for daylight; preserve gold filigree while validating hover foreground/background as a pair and retaining readable dark ink.
