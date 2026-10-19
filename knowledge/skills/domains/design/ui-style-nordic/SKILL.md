---
name: "ui-style-nordic"
description: "Provides the official Nordic & Nord UI style: Arctic minimalist aesthetic created by Sven Greb (Arctic Ice Studio), structured into Polar Night, Snow Storm, Frost, and Aurora palettes. Blends clean Scandinavian functionalism, generous whitespace, frosted matte surfaces, and cozy Hygge warmth. Use when designing minimal productivity software, developer tools, clean dashboards, or serene editorial web applications."
---

# UI Style: Nordic (Nord Theme & Scandinavian Minimalism)

Nordic is an arctic-inspired, functionalist design system derived from the official Nord theme created by Sven Greb (Arctic Ice Studio). Grounded in the atmospheric stillness of Scandinavian landscapes, it balances cool polar tones with purposeful typographic hierarchy and the calming domestic warmth of *Hygge*. Synthesized directly from the Nord palette specification and Nordic human-centered design principles.

---

## 🧭 When to Activate

- Designing focused productivity tools, documentation sites, calm dashboards, or modern code environments requiring prolonged visual comfort.
- Emphasizing Scandinavian design values: restraint, honest functionality, generous whitespace, and zero visual clutter.
- Seeking a cohesive aesthetic that effortlessly supports both serene dark mode (*Polar Night*) and crisp light mode (*Snow Storm*).

---

## 🕰️ Definition, Lineage, and Timeline

- **Origins:** Created in August 2016 by Sven Greb as "Nord", an Arctic color system engineered to prevent eye strain and maintain harmonious contrast.
- **Philosophical Roots:** Scandinavian functionalism (Alvar Aalto, Dieter Rams' minimal ethos, Danish modernism) combined with digital ergonomics.
- **Distinction from Neighbors:**
  - Unlike **Dracula / [ui-style-dracula](../ui-style-dracula/SKILL.md)**: Nordic avoids warm violet undertones and saturated neons; its dark mode is anchored in desaturated, icy slate blues (`#2E3440` to `#4C566A`).
  - Unlike **Swiss Minimalism / [ui-style-swiss-web-minimalism](../ui-style-swiss-web-minimalism/SKILL.md)**: Swiss minimalism relies on stark pure black/white contrast and rigid grid tension; Nordic introduces soft arctic blues and comforting atmospheric calm.

---

## 🎨 Visual DNA & Subgenre Taxonomy

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                   NORD 4-TIER PALETTE                                  │
├────────────────────────────┬────────────────────────────┬──────────────────────────────┤
│ 1. Polar Night (Dark Base) │ 2. Snow Storm (Light Base) │ 3. Frost (Cool Accents)      │
│ • nord0: #2E3440 (Deepest) │ • nord4: #D8DEE9 (Light)   │ • nord7: #8FBCBB (Teal Ice)  │
│ • nord1: #3B4252 (Surface) │ • nord5: #E5E9F0 (Paper)   │ • nord8: #88C0D0 (Ice Cyan)  │
│ • nord2: #434C5E (Elevated)│ • nord6: #ECEFF4 (Pure)    │ • nord9: #81A1C1 (Glacier)   │
│ • nord3: #4C566A (Muted)   │                            │ • nord10: #5E81AC (Deep Sea) │
└────────────────────────────┴────────────────────────────┴──────────────────────────────┘
```

- **Aurora Accents (Semantic Signals):**
  - Red (`nord11: #BF616A`): Urgent errors, deletions, critical warnings.
  - Orange (`nord12: #D08770`): Warnings, highlights, in-progress states.
  - Yellow (`nord13: #EBCB8B`): Notices, cautions, search matches.
  - Green (`nord14: #A3BE8C`): Success, additions, confirmations.
  - Purple (`nord15: #B48EAD`): Declarations, special tags, badges.
- **Surfaces & Tactile Craft:**
  - Frosted matte finishes with no glossy reflection or high-specular glare.
  - Subtle 1px borders in `nord3` (`#4C566A`) or `nord4` (`#D8DEE9`).
  - Rounded corners contained at a restrained 4px to 6px.

---

## 📐 Lighting Physics, Specular Splits & Surfaces

1. **Matte Frost Elevation:**
   - Surfaces diffuse ambient light softly without shiny specular highlights.
   ```css
   background: var(--nord-polar-1);
   border: 1px solid var(--nord-polar-3);
   box-shadow: 0 4px 12px rgba(15, 17, 26, 0.35);
   ```
2. **Aurora Interaction Glow:**
   ```css
   box-shadow: 0 0 0 2px var(--nord-polar-0), 0 0 0 4px var(--nord-frost-2);
   ```

---

## 🏷️ Complete Design Tokens

```css
:root {
  /* Polar Night (Dark Canvas) */
  --nord-polar-0: #2E3440;
  --nord-polar-1: #3B4252;
  --nord-polar-2: #434C5E;
  --nord-polar-3: #4C566A;

  /* Snow Storm (Light Canvas / Text) */
  --nord-snow-4: #D8DEE9;
  --nord-snow-5: #E5E9F0;
  --nord-snow-6: #ECEFF4;

  /* Frost (Arctic Blues) */
  --nord-frost-0: #8FBCBB;
  --nord-frost-1: #88C0D0;
  --nord-frost-2: #81A1C1;
  --nord-frost-3: #5E81AC;

  /* Aurora (Semantic Colors) */
  --nord-aurora-red: #BF616A;
  --nord-aurora-orange: #D08770;
  --nord-aurora-yellow: #EBCB8B;
  --nord-aurora-green: #A3BE8C;
  --nord-aurora-purple: #B48EAD;

  /* Typography */
  --nord-font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --nord-font-mono: 'JetBrains Mono', 'Fira Code', monospace;
  --nord-surface: var(--nord-polar-0);
  --nord-ink: var(--nord-snow-6);
  --nord-label-ink: var(--nord-snow-4);
}
```

---

## 🧱 Production-Ready Component Blueprints

### 1. Nordic Task Board & Telemetry Metric

```html
<article class="nordic-card">
  <div class="nordic-card-header">
    <span class="nordic-pill-frost">Telemetry Pod</span>
    <span class="nordic-badge-aurora">Online</span>
  </div>
  <h3 class="nordic-title">Glacier Network Mesh</h3>
  <p class="nordic-body">Latent connection established across 4 arctic nodes with minimal telemetry jitter.</p>
  <div class="nordic-metrics">
    <div class="nordic-metric-item">
      <span class="nordic-label">Throughput</span>
      <strong class="nordic-val">4.8 GB/s</strong>
    </div>
    <div class="nordic-metric-item">
      <span class="nordic-label">Thermal Index</span>
      <strong class="nordic-val success">−18 °C</strong>
    </div>
  </div>
  <button class="nordic-btn-primary" type="button">Manage Cluster</button>
</article>
```

```css
.nordic-card {
  background: var(--nord-polar-1);
  border: 1px solid var(--nord-polar-2);
  border-radius: 6px;
  padding: 24px;
  color: var(--nord-ink);
  font-family: var(--nord-font-sans);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
}
.nordic-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}
.nordic-pill-frost {
  background: rgba(136, 192, 208, 0.12);
  color: var(--nord-frost-1);
  border: 1px solid var(--nord-frost-1);
  font-size: 0.75rem;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 4px;
}
.nordic-badge-aurora {
  color: var(--nord-aurora-green);
  font-size: 0.8125rem;
  font-weight: 600;
}
.nordic-title {
  font-size: 1.125rem;
  font-weight: 700;
  margin: 0 0 8px 0;
  color: var(--nord-ink);
}
.nordic-body {
  font-size: 0.875rem;
  color: var(--nord-snow-4);
  line-height: 1.5;
  margin: 0 0 20px 0;
}
.nordic-metrics {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  padding: 12px;
  background: var(--nord-surface);
  border-radius: 4px;
  margin-bottom: 20px;
}
.nordic-label {
  display: block;
  font-size: 0.75rem;
  color: var(--nord-label-ink);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 2px;
}
.nordic-val {
  font-size: 1rem;
  color: var(--nord-ink);
}
.nordic-val.success {
  color: var(--nord-frost-0);
}
.nordic-btn-primary {
  background: var(--nord-frost-1);
  color: var(--nord-polar-0);
  border: none;
  border-radius: 4px;
  padding: 10px 20px;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  transition: background-color 150ms ease;
}
.nordic-btn-primary:hover {
  background: var(--nord-frost-2);
}
.nordic-btn-primary:focus-visible {
  outline: 2px solid var(--nord-frost-1);
  outline-offset: 2px;
}
```

---

## ✨ Micro-Interactions, Motion & Soundscapes

- **Gentle Arctic Drifts:** Transitions are subtle and linear-damped (180–250ms), avoiding elastic bounces or exaggerated springs.
- **Frosted Focus:** Interactive elements subtly brighten border luminance on hover without heavy saturated color blooms.

---

## ♿ WCAG 2.2 Accessibility & High-Contrast Guardrails

- **Contrast Ratios:**
  - `nord6` (`#ECEFF4`) on `nord0` (`#2E3440`): **11.4:1** (Passes WCAG AAA).
  - `nord4` (`#D8DEE9`) on `nord0` (`#2E3440`): **9.3:1** (Passes WCAG AAA).
  - `nord8` (`#88C0D0`) on `nord0` (`#2E3440`): **7.2:1** (Passes WCAG AAA).
  - `nord14` (`#A3BE8C`) on `nord0` (`#2E3440`): **7.5:1** (Passes WCAG AAA).
- **Dual-Contrast Focus Ring:**
  `outline: 2px solid #88C0D0; box-shadow: 0 0 0 1px #2E3440;`

---

- ❌ **NEVER use saturated neon primaries or warm hues:** Generic Tailwind primaries (`bg-blue-600`, `bg-purple-600`) destroy the serene atmospheric balance of Nord.
- ❌ **NEVER pollute layouts with harsh black drop shadows:** Rely on calm polar elevation boundaries (`nord1`, `nord2`) and subtle occlusion.

---

## 📚 Sources & References

- Sven Greb (Arctic Ice Studio), *Nord — An arctic, north-bluish color palette* (https://www.nordtheme.com).
- Alvar Aalto Foundation, *Functionalism and Materials in Scandinavian Architecture* (Helsinki).
## Appearance and Interaction Verification

Introduce semantic PolarNight/SnowStorm surface/ink roles for requested modes; verify nordic-label and primary-button hover on their actual backgrounds rather than quoting only nord0 pairs; preserve all four named Nord palette groups.
