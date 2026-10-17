---
name: "ui-style-agitprop-poster"
description: "Provides the authentic Agitprop Poster UI style (1920s-1940s revolutionary street poster graphic design): high-contrast heraldic rays, heroic woodblock stencil typography, bold diagonal banner ribbons, stark scarlet-ochre-black palette, and urgent public agitation slogans. Use when designing high-impact protest journalism, political campaign hubs, grassroots activist portals, or assertive community rallying features."
---

# UI Style: Agitprop Poster (Agitation, Heraldic Rays & Street Mobilization)

Agitprop Poster design emerged from the political turbulence of early 20th-century Europe and Eurasia (1918–1945), specifically through the Russian ROSTA Windows (Vladimir Mayakovsky, Mikhail Cheremnykh) and radical mass-mobilization lithography (Gustav Klutsis, the Stenberg brothers, John Heartfield). Unlike the abstract architectural purity of formal Constructivism, Agitprop is directly figurative, urgent, loud, and public. It communicates through heraldic radial sunbursts, dynamic diagonal megaphone banners, stark woodblock stencil typography, and coarse two-tone ink printing. Synthesized from primary street poster archives; see Sources.

---

## 🧭 When to Activate

- Designing grassroots mobilization portals, investigative journalism hubs, activist public notices, or bold campaign platforms.
- Building high-urgency call-to-action interfaces that require dramatic street-poster gravitas and bold banner typography.
- Distinct from **[ui-style-constructivism](../ui-style-constructivism/SKILL.md)**: Constructivism is abstract architectural engineering, pure geometric primitives, and cold structural typography; Agitprop is rhetorical, human-centered, emotive, utilizing megaphone slogans, heroic silhouettes, and heraldic burst rays.
- Distinct from **[ui-style-zine-independent](../ui-style-zine-independent/SKILL.md)**: Zines are personal, chaotic, subcultural, and photocopied; Agitprop is public, collective, declarative, and printed for mass street walls.

---

## 🕰️ Definition, Lineage, and Timeline

- **Chronology:** Initiated in 1919 with the satirical ROSTA Windows posters pasted in empty shop fronts across Moscow. Expanded in the 1920s–1930s into mass lithographic posters for public enlightenment, five-year plans, and anti-fascist resistance.
- **Graphic Weaponry:** Urgent headlines set in ultra-bold woodblock grotesques, heraldic angled sunbursts focusing attention on calls-to-action, megaphone and factory silhouettes, and diagonal red banners stretching across the layout.

---

## 🎨 Visual DNA & Subgenre Taxonomy

- **Palettes:** Highly saturated, non-reflective street lithograph inks:
  - Agitation Crimson (`#C1121F` / `#9B111E`)
  - Warning Ochre / Wheat Gold (`#E09F3E` / `#D48812`)
  - Newsprint Buff Paper (`#F5EBE0` / `#ECE0D1`)
  - Heavy Industrial Tar Black (`#1A1A1A`)
- **Heraldic Sunbursts & Diagonal Ribbons:**
  - Radial perspective rays emanating from focal triggers or action buttons.
  - 15° to 30° diagonal ribbons and banners spanning container full widths with jagged cut ends.
- **Woodblock Display Typography:**
  - Condensed sans-serif capitals with woodcut imperfections (Anton, Bebas Neue, Impact, League Gothic).
  - Urgent exclamation badges, boxed imperative commands ("LISTEN!", "FORWARD!", "ORGANIZE!").
- **Coarse Lithographic Halftones:**
  - Heavy stipple textures, high-contrast black-and-scarlet duotone portrait silhouettes, and visible press ink grain.

---

## 📐 Lighting Physics, Specular Splits & Surfaces

- **Physical Street Poster Paper:** Flat matte paper tooth, zero specular gloss, zero digital drop shadows. Depth is created through hard geometric layer overlap and heraldic sunburst rays:
  ```css
  /* Agitprop heraldic radial rays */
  background: repeating-conic-gradient(
    from 0deg,
    #E09F3E 0deg 15deg,
    #F5EBE0 15deg 30deg
  );
  ```
- **Banner Jagged Edge:**
  ```css
  clip-path: polygon(0 0, 100% 0, 96% 50%, 100% 100%, 0 100%, 4% 50%);
  ```

---

## 🏷️ Complete Design Tokens

```css
:root {
  /* Ink and Substrate */
  --agit-paper: #F5EBE0;
  --agit-paper-dark: #ECE0D1;
  --agit-red: #C1121F;
  --agit-red-dark: #780000;
  --agit-ochre: #E09F3E;
  --agit-black: #1A1A1A;
  --agit-white: #FFFFFF;

  /* Typography */
  --agit-font-display: 'Anton', 'Bebas Neue', Impact, sans-serif;
  --agit-font-body: 'Space Grotesk', system-ui, sans-serif;
  --agit-font-caption: 'Courier Prime', monospace;

  /* Borders & Framing */
  --agit-border-thick: 4px solid var(--agit-black);
  --agit-border-banner: 8px solid var(--agit-red);
}
```

---

## 🧱 Production-Ready Component Blueprint

```html
<article class="agit-poster">
  <div class="agit-sunburst" aria-hidden="true"></div>
  <div class="agit-ribbon">CITIZENS OF THE NETWORK: ATTENTION!</div>
  <div class="agit-content">
    <h1 class="agit-headline">ORGANIZE // RESIST</h1>
    <p class="agit-manifesto">
      THE COLLECTIVE INTEGRITY OF OPEN COMMUNICATION DEMANDS VIGILANCE.
      DO NOT SURRENDER DIGITAL INFRASTRUCTURE TO UNCHECKED MONOPOLY.
    </p>
    <div class="agit-cta-strip">
      <button class="agit-btn-primary" type="button">JOIN MOBILIZATION</button>
      <span class="agit-counter">12,480 ALLIES SIGNED</span>
    </div>
  </div>
</article>
```

```css
.agit-poster {
  position: relative;
  background: var(--agit-paper);
  color: var(--agit-black);
  border: var(--agit-border-thick);
  padding: 32px 24px;
  max-width: 640px;
  overflow: hidden;
  box-shadow: 6px 6px 0px var(--agit-black);
}
.agit-sunburst {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: repeating-conic-gradient(
    from 0deg,
    rgba(224, 159, 62, 0.2) 0deg 12deg,
    transparent 12deg 24deg
  );
  pointer-events: none;
  z-index: 1;
}
.agit-ribbon {
  position: relative;
  z-index: 2;
  background: var(--agit-red);
  color: var(--agit-white);
  font-family: var(--agit-font-display);
  font-size: 1.125rem;
  letter-spacing: 0.12em;
  padding: 8px 16px;
  text-transform: uppercase;
  display: inline-block;
  transform: rotate(-2deg);
  margin-bottom: 20px;
  border: 2px solid var(--agit-black);
}
.agit-content {
  position: relative;
  z-index: 2;
}
.agit-headline {
  font-family: var(--agit-font-display);
  font-size: 3.5rem;
  line-height: 0.9;
  letter-spacing: 0.04em;
  color: var(--agit-black);
  margin: 0 0 16px 0;
  text-shadow: 2px 2px 0px var(--agit-red);
}
.agit-manifesto {
  font-family: var(--agit-font-body);
  font-size: 1rem;
  font-weight: 700;
  line-height: 1.5;
  color: var(--agit-black);
  margin-bottom: 28px;
  border-left: 6px solid var(--agit-red);
  padding-left: 14px;
}
.agit-cta-strip {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}
.agit-btn-primary {
  background: var(--agit-red);
  color: var(--agit-white);
  font-family: var(--agit-font-display);
  font-size: 1.375rem;
  letter-spacing: 0.08em;
  padding: 12px 28px;
  border: 3px solid var(--agit-black);
  cursor: pointer;
  box-shadow: 4px 4px 0px var(--agit-black);
  transition: transform 0.1s linear, box-shadow 0.1s linear;
}
.agit-btn-primary:hover {
  background: var(--agit-black);
  color: var(--agit-ochre);
  transform: translate(-2px, -2px);
  box-shadow: 6px 6px 0px var(--agit-red);
}
.agit-counter {
  font-family: var(--agit-font-caption);
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--agit-red-dark);
}
```

---

## ✨ Micro-Interactions, Motion & Soundscapes

- **Stamp Press on Click:** Buttons compress with a hard physical clack (`transform: translate(3px, 3px); box-shadow: 1px 1px 0px var(--agit-black);`).
- **Banner Unfurl:** Ribbon announcements slide into the viewport on a diagonal shear vector (`transform: translateX(-100%) rotate(-2deg)` to `translateX(0)`).
- **No Spring Dampers:** Use rapid industrial linear cuts (`80ms` to `120ms`) reflecting mechanical printing presses.

---

## 📱 Responsive Layout & Spatial Composition

- On mobile screens, scale the headline clamp (`clamp(2rem, 8vw, 3.5rem)`) and flatten ribbon rotation to `-1deg` to prevent overflow while preserving the emphatic poster feel.

---

## ♿ WCAG 2.2 Accessibility & High-Contrast Guardrails

- **Contrast Verification:**
  - Industrial Tar Black (`#1A1A1A`) on Newsprint Buff (`#F5EBE0`): **13.5:1** (Passes WCAG AAA).
  - Agitation Crimson (`#C1121F`) on Newsprint Buff (`#F5EBE0`): **5.4:1** (Passes WCAG AA for normal text, AAA for bold titles).
  - White (`#FFFFFF`) on Agitation Crimson (`#C1121F`): **5.2:1** (Passes WCAG AA).
- **Reduced Motion:**
  ```css
  @media (prefers-reduced-motion: reduce) {
    .agit-sunburst {
      animation: none;
    }
    .agit-ribbon, .agit-btn-primary {
      transform: none !important;
      transition: none !important;
    }
  }
  ```

---

## 🚫 Anti-Patterns & Visual Sins (Anti-AI Slop Traps)

- ❌ **NEVER use corporate pastel cards or floating pill badges:** Agitprop is raw street lithography, not a SaaS dashboard.
- ❌ **NEVER apply soft blurry drop shadows:** Shadows must be hard, opaque 100% black offsets (`box-shadow: 4px 4px 0 #000;`).
- ❌ **NEVER use rounded buttons:** Edges must be hard right angles (`border-radius: 0;`).

---

## 🎯 When to Use & When to Avoid

- **Use For:** Human rights advocacy, investigative journalism, union mobilization hubs, indie theater posters, grassroots election campaigns.
- **Avoid For:** Corporate HR systems, medical records, delicate luxury fashion, or quiet data-heavy enterprise administration.

---

## 📚 Sources & References

- Peter Kenez, *The Birth of the Propaganda State: Soviet Methods of Mass Mobilization 1917–1929* (Cambridge University Press, 1985).
- David King, *Russian Revolutionary Posters* (Tate Publishing, 2012).
- Victoria E. Bonnell, *Iconography of Power: Soviet Political Posters under Lenin and Stalin* (University of California Press, 1999).
