---
name: "ui-style-y2k-revival"
description: "Provides the authentic Y2K Revival UI style (1998-2003 cyber-optimism and hardware dot-com aesthetic): translucent iMac G3 jelly polycarbonate, liquid chrome 3D typography, four-point starbursts, CD/DVD optical iridescence, and Cybercore futurism. Use when designing high-energy music album launches, futuristic fashion drops, millennium nostalgia portals, or creative digital toy experiences."
---

# UI Style: Y2K Revival (Translucent Jelly Polycarbonate, Liquid Chrome & Cybercore)

Y2K Revival captures the cyber-optimism and technophilic exuberance of the late 1990s through the turn of the millennium (1998–2003). Defined visually by the launch of Apple's translucent iMac G3 (Bondi Blue, Tangerine, Lime), liquid mercury chrome typography, high-gloss molded plastics, four-point starburst lens flares, optical disc iridescence, and the sleek digital aesthetic known as Cybercore. Rather than clean modern minimalism or blurred glassy skeuomorphism, Y2K is tangible, optimistic, reflective, and play-oriented. Synthesized from primary design archives including the Y2K Aesthetic Institute; see Sources.

---

## 🧭 When to Activate

- Designing fashion drop landing pages, music album microsites, retro gaming showcases, interactive merchandise portals, or millennium lifestyle platforms.
- Creating interfaces requiring liquid chrome reflection, jelly translucent casings, starburst highlights, and playful dot-com exuberance.
- Distinct from **[ui-style-frutiger-aero](../ui-style-frutiger-aero/SKILL.md)**: Frutiger Aero uses calm blue skies, green rolling fields, hyper-clear running water, and blurred glass; Y2K uses hard molded translucent plastic shells, chrome metallics, rave-inspired cyber hues, and techno-optimism.
- Distinct from **[ui-style-vaporwave](../ui-style-vaporwave/SKILL.md)**: Vaporwave is slow, melancholic, pastel-washed, and grounded in 90s corporate satire; Y2K is upbeat, high-energy, futuristic, and unironic in its love for technology.

---

## 🕰️ Definition, Lineage, and Timeline

- **Chronology:** Originates with Jonathan Ive's iMac G3 (May 1998) and the global anticipation of the Year 2000 (the Y2K bug), culminating in the early PlayStation 2 and dot-com boom era (1999–2002).
- **Aesthetic Movement:** Evan Collins and the Y2K Aesthetic Institute categorize this period into Cybercore (futuristic silver, tech meshes, sleek cybernetics) and Jelly/Blobject design (curved translucent plastics revealing internal circuitry).

---

## 🎨 Visual DNA & Subgenre Taxonomy

- **Jelly Plastic & Metallic Palettes:**
  - Bondi Blue Translucent (`#00A8B5` / `#007D8A`)
  - Tangerine Jelly (`#FF7A00`) and Cyber Lime (`#76FF03`)
  - Liquid Mercury Chrome (`#E0E5EC` to `#7A889B`)
  - High-Gloss Pure White (`#FFFFFF`) and Obsidian Silver (`#1A1C20`)
- **Blobjects & Molded Casings:**
  - Continuous organic pill-shaped containers with high specular highlights along top curves.
  - Translucent surfaces with visible internal ribbing or grid overlays (`opacity: 0.85` without heavy gaussian blurs).
- **Chrome Typography & Microcopy:**
  - Liquid metal display headers with high-contrast multi-stop vertical linear reflections.
  - Ultra-extended techno sans-serifs and geometric display faces (Bank Gothic, Eurostile Bold Extended, Microgramma).
- **Iconic Motifs:**
  - 4-point starburst sparkle flares positioned at the specular peak of buttons and headers.
  - Elliptical badge bubbles and optical disc diffraction gradients.

---

## 📐 Lighting Physics, Specular Splits & Surfaces

- **Liquid Chrome Reflective Type:**
  ```css
  /* Specular chrome horizon split */
  background: linear-gradient(
    180deg,
    #FFFFFF 0%,
    #D0D8E4 45%,
    #4A5568 49%,
    #FFFFFF 52%,
    #718096 75%,
    #2D3748 100%
  );
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.4));
  ```
- **Translucent Jelly Shell:**
  ```css
  background: linear-gradient(135deg, rgba(0, 168, 181, 0.85) 0%, rgba(0, 95, 105, 0.9) 100%);
  border: 2px solid rgba(255, 255, 255, 0.7);
  box-shadow:
    inset 0 2px 4px rgba(255, 255, 255, 0.8),
    inset 0 -2px 6px rgba(0, 0, 0, 0.4),
    0 8px 24px rgba(0, 168, 181, 0.35);
  border-radius: 24px;
  ```

---

## 🏷️ Complete Design Tokens

```css
:root {
  /* Translucent Polycarbonate */
  --y2k-bondi: #00A8B5;
  --y2k-bondi-dark: #006D77;
  --y2k-tangerine: #FF7A00;
  --y2k-lime: #76FF03;
  --y2k-purple: #8A2BE2;

  /* Chrome Metals */
  --y2k-chrome-light: #FFFFFF;
  --y2k-chrome-mid: #CBD5E1;
  --y2k-chrome-dark: #475569;
  --y2k-shell-bg: #0F141C;

  /* Typography */
  --y2k-font-display: 'Eurostile', 'Syne', system-ui, sans-serif;
  --y2k-font-body: 'Plus Jakarta Sans', system-ui, sans-serif;
  --y2k-font-mono: 'Space Mono', monospace;

  /* Border & Radii */
  --y2k-radius-pill: 999px;
  --y2k-radius-blob: 28px;
}
```

---

## 🧱 Production-Ready Component Blueprint

```html
<section class="y2k-device">
  <div class="y2k-sparkle-fx" aria-hidden="true">✦</div>
  <header class="y2k-header">
    <span class="y2k-pill-badge">CYBER-CORE 2000</span>
    <span class="y2k-model">SERIES: G3-BONDI</span>
  </header>
  <div class="y2k-screen-pod">
    <h1 class="y2k-display-chrome">FUTURE // CONNECT</h1>
    <p class="y2k-tagline">
      High-velocity optical data streams encased in translucent injection-molded polycarbonate.
    </p>
    <div class="y2k-spec-strip">
      <div class="y2k-spec-pill">SPEED: 400 MHz</div>
      <div class="y2k-spec-pill">OPTICAL: 24X CD</div>
    </div>
  </div>
  <footer class="y2k-actions">
    <button class="y2k-btn y2k-btn-primary" type="button">LAUNCH TERMINAL</button>
    <button class="y2k-btn y2k-btn-secondary" type="button">EXPLORE SPECS</button>
  </footer>
</section>
```

```css
.y2k-device {
  position: relative;
  background: linear-gradient(145deg, rgba(0, 168, 181, 0.9) 0%, rgba(0, 95, 105, 0.95) 100%);
  border: 2px solid rgba(255, 255, 255, 0.8);
  border-radius: var(--y2k-radius-blob);
  padding: 32px 28px;
  max-width: 620px;
  box-shadow:
    inset 0 3px 6px rgba(255, 255, 255, 0.9),
    inset 0 -4px 10px rgba(0, 0, 0, 0.5),
    0 16px 40px rgba(0, 168, 181, 0.4);
  color: #FFFFFF;
  overflow: hidden;
}
.y2k-sparkle-fx {
  position: absolute;
  top: 18px;
  right: 28px;
  font-size: 2rem;
  color: #FFFFFF;
  text-shadow: 0 0 10px #FFFFFF, 0 0 20px var(--y2k-lime);
  pointer-events: none;
}
.y2k-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}
.y2k-pill-badge {
  background: var(--y2k-tangerine);
  color: #FFFFFF;
  font-family: var(--y2k-font-display);
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  padding: 4px 14px;
  border-radius: var(--y2k-radius-pill);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.6), 0 2px 6px rgba(0, 0, 0, 0.3);
}
.y2k-model {
  font-family: var(--y2k-font-mono);
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.8);
}
.y2k-screen-pod {
  background: rgba(15, 20, 28, 0.75);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.6);
}
.y2k-display-chrome {
  font-family: var(--y2k-font-display);
  font-size: clamp(2rem, 5.5vw, 3.2rem);
  font-weight: 900;
  letter-spacing: 0.05em;
  background: linear-gradient(180deg, #FFFFFF 0%, #CBD5E1 48%, #475569 50%, #FFFFFF 53%, #94A3B8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin: 0 0 12px 0;
}
.y2k-tagline {
  font-family: var(--y2k-font-body);
  font-size: 0.9375rem;
  line-height: 1.5;
  color: #E2E8F0;
  margin-bottom: 18px;
}
.y2k-spec-strip {
  display: flex;
  gap: 10px;
}
.y2k-spec-pill {
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: var(--y2k-radius-pill);
  padding: 4px 12px;
  font-family: var(--y2k-font-mono);
  font-size: 0.75rem;
  color: var(--y2k-lime);
}
.y2k-actions {
  display: flex;
  gap: 14px;
}
.y2k-btn {
  font-family: var(--y2k-font-display);
  font-weight: 700;
  font-size: 0.875rem;
  letter-spacing: 0.06em;
  padding: 12px 24px;
  border-radius: var(--y2k-radius-pill);
  cursor: pointer;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.y2k-btn-primary {
  background: linear-gradient(180deg, #FFFFFF 0%, #E2E8F0 50%, #94A3B8 100%);
  color: #0F172A;
  border: 1px solid #FFFFFF;
  box-shadow: inset 0 2px 2px #FFFFFF, 0 4px 12px rgba(0, 0, 0, 0.3);
}
.y2k-btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(255, 255, 255, 0.4);
}
.y2k-btn-secondary {
  background: rgba(255, 255, 255, 0.15);
  color: #FFFFFF;
  border: 1px solid rgba(255, 255, 255, 0.4);
}
```

---

## ✨ Micro-Interactions, Motion & Soundscapes

- **Jelly Button Compression:** Click interactions smoothly compress buttons with an elastic volume preservation (`transform: scale(0.96, 0.94)`).
- **Starburst Glimmer:** Four-point starbursts slowly rotate and pulsate in scale (`scale(0.8)` to `scale(1.2)` at 3s sinusoidal intervals).
- **CD Spin Transition:** Page switches incorporate subtle radial rainbow diffraction sweeps.

---

## 📱 Responsive Layout & Spatial Composition

- Use fluid pill cards with generous internal padding. If the viewport drops below 540px, stack action buttons vertically.

---

## ♿ WCAG 2.2 Accessibility & High-Contrast Guardrails

- **Contrast Safety:**
  - Chrome text gradients must only be used on prominent `<h1>` and `<h2>` headings with a guaranteed dark backing or dark text shadow.
  - Body text must never use chrome gradient masks; use pure high-contrast `#FFFFFF` or `#E2E8F0` on dark glass pods (contrast ratio **> 12:1**).
- **Reduced Motion:**
  ```css
  @media (prefers-reduced-motion: reduce) {
    .y2k-sparkle-fx {
      animation: none;
    }
    .y2k-btn {
      transition: none;
    }
  }
  ```

---

## 🚫 Anti-Patterns & Visual Sins (Anti-AI Slop Traps)

- ❌ **NEVER mix with Frutiger Aero nature themes:** Absolutely NO green grass, blue skies, floating koi fish, or water drops. Y2K is cyber, plastic, hardware, and electronic.
- ❌ **NEVER use frosted matte blurs everywhere:** Y2K plastic is glossy and translucent, not diffused iOS blur.
- ❌ **NEVER use drab corporate grays:** Retain saturated accents (Tangerine, Bondi Blue, Cyber Lime).

---

## 🎯 When to Use & When to Avoid

- **Use For:** High-energy fashion lookbooks, music festivals, consumer gadget promos, indie games, millennium art archives.
- **Avoid For:** Serious banking portals, legal compliance documentations, clinical health apps.

---

## 📚 Sources & References

- Evan Collins, *The Y2K Aesthetic: A Definitive Visual Taxonomy* (Y2K Aesthetic Institute / CARI, 2018).
- Paul Kunkel, *AppleDesign: The Work of the Apple Industrial Design Group* (Graphis, 1997).
- Xiaochun Yang, *Cybercore and the Return of Millennial Optimism* (Design Issues, 2023).
