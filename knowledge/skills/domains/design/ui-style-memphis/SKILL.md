---
name: "ui-style-memphis"
description: "Provides the Memphis Design UI style (1980-1987 origin, recurring revival): clashing pastel and primary palettes, squiggles, terrazzo and plastic-laminate patterns, asymmetric geometry and playful rule-breaking, covering tokens, pattern layers, shape kits and WCAG-safe color handling. Use when designing youthful, irreverent brand, campaign or education surfaces that need postmodern playfulness rather than modernist restraint."
---

# UI Style: Memphis Design (Milano Postmodernism)

> *"When I was young, all we ever heard about was functionalism, functionalism, functionalism. It's not enough. Design should also be sensual and exciting."*  
> — Ettore Sottsass, Founder of the Memphis Group (Milan, 1981)

Born on an evening in Milan on December 11, 1980, the **Memphis Group** shattered the dogmatic severity of Bauhaus and International Style functionalism. Spearheaded by Ettore Sottsass, Michele De Lucchi, and Nathalie du Pasquier, Memphis celebrated vibrant vulgarity: clashing pastel and neon palettes, chaotic squiggles, plastic laminate textures (Abet Laminati's *Bacterio* pattern), terrazzo chip speckles, and irreverent geometric collisions. In user interfaces, Memphis delivers joyful energy, tactile humor, and radical visual freedom.

---

## 🧭 When to Activate

- Designing youth brands, creative festival landing pages, indie game showcases, and educational edtech tools that demand joyful engagement.
- Crafting illustrated onboarding sequences, playful empty states, and celebratory reward screens.
- Building marketing campaigns that deliberately defy the homogeneous "bland corporate SaaS" look in favor of vibrant postmodern wit.
- Art directing lifestyle, fashion, music streaming, and cultural event portals.

---

## 🕰️ Definition, Lineage, and Timeline

- **December 11, 1980 (The Milan Genesis):** Ettore Sottsass gathers young international designers (Michele De Lucchi, Martine Bedin, Nathalie du Pasquier, George Sowden) in his Milan apartment. Listening repeatedly to Bob Dylan's *"Stuck Inside of Mobile with the Memphis Blues Again"*, they christen the movement "Memphis".
- **September 1981 (Salone del Mobile Debut):** The Arc '74 gallery exhibition electrifies the design world. Sottsass's *Carlton* room divider (a polychrome laminate totem) and *Beverly* cabinet challenge every rule of good bourgeois taste.
- **1985–1987 (Disbandment & Global Saturation):** Sottsass departs in 1985 to establish Sottsass Associati; the group formally disbands in 1987. However, the aesthetic spreads like wildfire through pop culture (*Pee-wee's Playhouse*, Swatch watches, MTV bumpers, and *Saved by the Bell*).
- **2015–Present (The Digital Memphis Wave):** Designers revive Memphis geometry on the web (popularized as "neo-memphis" or "nostalgia chic"), combining SVG squiggles with responsive CSS Grid.

### Absolute Style Vetos (What Memphis is NOT)
- ❌ **NOT Neo-Brutalism ([ui-style-neo-brutalism](../ui-style-neo-brutalism/SKILL.md)):** Neo-brutalism is dominated by thick 2px–3px solid black outlines around every container, cynical ironic memes, and hard-edged 100% black drop shadows. Memphis is celebratory, decorative, and painterly, celebrating clashing surface patterns and colorful laminate inlays.
- ❌ **NOT Y2K Revival ([ui-style-y2k-revival](../ui-style-y2k-revival/SKILL.md)):** Zero liquid mercury chrome, zero translucent iMac G3 jelly plastic, zero futuristic matrix grids. Memphis is analog plastic laminate, wood, and terrazzo.
- ❌ **NOT Bauhaus Functionalism ([ui-style-bauhaus](../ui-style-bauhaus/SKILL.md)):** Bauhaus insists that form must strictly follow function. Memphis insists that ornamentation and emotion *are* function.

---

## 🎨 Visual DNA & Subgenre Taxonomy

```
+------------------------------------------------------------------------------------+
|                                 MEMPHIS TAXONOMY                                   |
+------------------------------------------------------------------------------------+
| High Milanese Postmodernism (1981-1987)| 1990s Pop Culture "Saved by the Bell"     |
| - Architectural laminate furniture     | - Wild squiggles, confetti triangles & dots|
| - Bacterio amoeba pattern & terrazzo   | - Clashing pastel neons (teal, hot pink)   |
| - Asymmetric totems and arches         | - Playful floating background shapes       |
| - High-craft provocation of "bad taste"| - Quirky, energetic bouncy micro-motion    |
+------------------------------------------------------------------------------------+
```

### Visual Pillars
1. **The Polychrome Clashing Palette:** Neon pastels balanced against punchy primaries: Flamingo Pink (`#FF71CE`), Electric Cyan (`#01CDFE`), Solar Yellow (`#FFD400`), Lavender Purple (`#B967FF`), grounded by Jet Black (`#111111`) and Crisp White (`#FFFFFF`).
2. **Iconic Memphis Patterns:**
   - **Bacterio:** Organic squiggling amoeba worms floating over a contrasting ground.
   - **Terrazzo:** Multi-colored geometric chips scattered randomly over stone.
   - **Zebra Diagonals & Polka Dots:** High-contrast black-and-white geometric fields used as regional inlays.
3. **Asymmetrical Floating Confetti:** Backgrounds are activated by floating decorative shapes: floating 3D spheres, wireframe cubes, zigzags, and tilted arches.

---

## 📐 Lighting Physics, Specular Splits & Surfaces

Memphis interfaces simulate physical plastic laminate (*Formica / Abet Laminati*) and cast composite stone:
- **Surface Material:** Matte laminate sheets. Soft, low specular sheen (`oklch(1 0 0 / 0.15)`), uniform flat color planes.
- **Drop Shadows:** Softly displaced colorful drop shadows (e.g. `box-shadow: 6px 6px 0px var(--memphis-black), 12px 12px 0px var(--memphis-pink)`).
- **Edge Boundaries:** Mixed radii: perfectly round corners on one side (`border-radius: 24px 0 24px 0`) juxtaposed with sharp right angles.

---

## 🏷️ Complete Design Tokens

```css
:root {
  /* Memphis Saturated Palette */
  --memphis-pink: #FF71CE;          /* Flamingo Neon Pink */
  --memphis-teal: #01CDFE;          /* Electric Swimming Pool Teal */
  --memphis-yellow: #FFD400;        /* Vivid Sunflower */
  --memphis-purple: #B967FF;        /* Electric Lavender */
  --memphis-coral: #FF5E5B;         /* Postmodern Salmon Coral */
  --memphis-mint: #05FFA1;          /* Acid Mint */

  /* Structural Stabilizers */
  --memphis-black: #111111;         /* Deep Carbon Black */
  --memphis-white: #FFFFFF;         /* Crisp Bleached Paper */
  --memphis-canvas: #FDF9F2;        /* Soft Cream Base */

  /* Memphis Pattern Shaders */
  --memphis-pattern-dots: radial-gradient(var(--memphis-black) 2px, transparent 2px);
  --memphis-pattern-stripes: repeating-linear-gradient(
    45deg,
    var(--memphis-black),
    var(--memphis-black) 6px,
    var(--memphis-white) 6px,
    var(--memphis-white) 12px
  );

  /* Geometry & Corners */
  --memphis-radius-playful: 16px 4px 20px 8px;
  --memphis-radius-pill: 9999px;

  /* Playful Spring Transitions */
  --memphis-spring: cubic-bezier(0.34, 1.56, 0.64, 1.0);
  --memphis-duration: 250ms;
}
```

---

## 🔤 Typography & Lettering Architecture

Memphis typography is bold, punchy, and expressive:
- **Display Headlines:** Chubby geometric sans-serifs or display novelties (`"Righteous"`, `"Syne"`, `"Dela Gothic One"`, or `"Futura Bold"`), `800` weight, sentence case or uppercase, often paired with offset drop-shadow text effects (`text-shadow: 3px 3px 0 var(--memphis-teal)`).
- **Body Text:** Clean, readable geometric sans (`"Jost"`, `"Inter"`), `400` weight, `15px` to `16px`, line-height `1.5`, set on pure white or black backgrounds for guaranteed legibility.

---

## 🖱️ Interaction Dynamics, Sound Cues & Motion

- **Overshoot Spring Hover:** Buttons and cards react with a playful 8% scale bounce (`transform: scale(1.08) rotate(-1.5deg)`) using `--memphis-spring`.
- **Pattern Jiggle:** Decorative squiggles and confetti elements undergo a subtle 2-degree periodic oscillation on hover.
- **Acoustic Feedback:** High-pitched, playful cartoon pops: an 18ms rubbery bubble click (`680Hz` rising pitch) upon activation.

---

## 🧩 Canonical Component Specifications

### 1. Polychrome Memphis Card with Pattern Inset

```html
<article class="memphis-card">
  <div class="memphis-card-badge">HOT RELEASE</div>
  <div class="memphis-card-header">
    <div class="memphis-pattern-strip" aria-hidden="true"></div>
    <h3 class="memphis-card-title">Polyphonic Synth Studio</h3>
  </div>
  <p class="memphis-card-desc">Compose modular electronic melodies with vintage analog oscillators, ladder filters, and chaotic step sequencers.</p>
  <div class="memphis-card-footer">
    <button class="memphis-btn memphis-btn-yellow">Launch Tool</button>
    <div class="memphis-confetti-circle" aria-hidden="true"></div>
  </div>
</article>
```

```css
.memphis-card {
  background-color: var(--memphis-white);
  border: 3px solid var(--memphis-black);
  border-radius: var(--memphis-radius-playful);
  padding: 24px;
  max-width: 360px;
  box-shadow: 8px 8px 0px var(--memphis-black), 14px 14px 0px var(--memphis-pink);
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 16px;
  transition: transform var(--memphis-duration) var(--memphis-spring);
}

.memphis-card:hover {
  transform: translate(-3px, -3px) rotate(1deg);
  box-shadow: 11px 11px 0px var(--memphis-black), 18px 18px 0px var(--memphis-pink);
}

.memphis-card-badge {
  position: absolute;
  top: -12px;
  right: 16px;
  background-color: var(--memphis-teal);
  color: var(--memphis-black);
  font-family: "Righteous", sans-serif;
  font-size: 11px;
  font-weight: 700;
  padding: 4px 10px;
  border: 2px solid var(--memphis-black);
  border-radius: var(--memphis-radius-pill);
}

.memphis-pattern-strip {
  width: 100%;
  height: 12px;
  background: var(--memphis-pattern-stripes);
  border: 1px solid var(--memphis-black);
  margin-bottom: 12px;
}

.memphis-card-title {
  font-family: "Righteous", "Syne", sans-serif;
  font-size: 22px;
  font-weight: 700;
  color: var(--memphis-black);
  margin: 0;
}

.memphis-card-desc {
  font-size: 14px;
  line-height: 1.5;
  color: var(--memphis-black);
  margin: 0;
}

.memphis-card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 8px;
}

.memphis-btn-yellow {
  background-color: var(--memphis-yellow);
  color: var(--memphis-black);
  border: 2px solid var(--memphis-black);
  font-family: "Righteous", sans-serif;
  font-size: 13px;
  font-weight: 700;
  padding: 8px 18px;
  border-radius: var(--memphis-radius-pill);
  cursor: pointer;
  transition: background-color 150ms ease;
}

.memphis-btn-yellow:hover {
  background-color: var(--memphis-mint);
}

.memphis-confetti-circle {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background-color: var(--memphis-purple);
  border: 2px solid var(--memphis-black);
}
```

---

## ♿ Accessibility & Environmental Contrast

- **The Pattern Background Trap:** Text must NEVER be set directly over complex zebra stripes, polka dots, or Bacterio squiggles. All body text and critical labels MUST sit inside solid, high-opacity white or dark containers (`background: #FFFFFF`).
- **Contrast Ratios on Pastels:**
  - Ink black (`#111111`) over `--memphis-yellow` (`#FFD400`) yields **12.1:1** (WCAG AAA).
  - Ink black over `--memphis-teal` (`#01CDFE`) yields **8.6:1** (WCAG AAA).
  - Ink black over `--memphis-pink` (`#FF71CE`) yields **5.4:1** (WCAG AA).
- **Reduced Motion Conformance:** When `prefers-reduced-motion: reduce` is enabled, all bounce spring animations and floating background shapes freeze immediately.

---

## ✅ When to Use / ❌ When to Avoid

### Appropriate Scenarios
- Youth lifestyle portals, music streaming apps, toy/gaming e-commerce.
- Creative agency landing pages and interactive portfolios.
- Product onboarding tours that benefit from cheerful, disarming visual humor.

### Inappropriate Scenarios
- Serious enterprise infrastructure consoles, medical diagnostic displays, banking apps.
- Contexts where high emotional sobriety and conservative corporate trust are required.

---

## 📚 Authoritative Sources & Historical Artifacts

1. **Radice, Barbara (1984):** *Memphis: Research, Experiences, Results, Failures and Successes of New Design*, Rizzoli.
2. **Sottsass, Ettore (1988):** *Design Metaphors*, Idea Books.
3. **Horn, Richard (1985):** *Fifties Style: Then and Now*, Quick Fox (documenting the 1980s retro-modernist intersection).

---

## 🔗 Cross-Skill Integration & Dialect Relations

- Direct postmodern antithesis to [ui-style-bauhaus](../ui-style-bauhaus/SKILL.md) and [ui-style-swiss-web-minimalism](../ui-style-swiss-web-minimalism/SKILL.md).
- Contrasts with [ui-style-neo-brutalism](../ui-style-neo-brutalism/SKILL.md) by trading cynical punk edge for colorful, joyful laminate maximalism.
## Appearance and Interaction Verification

Preserve Bacterio/terrazzo and solid reading panels; make footer/badge labels wrap under localization and reserve clearance for 8% hover scale and hard shadows without hiding content or focus.
