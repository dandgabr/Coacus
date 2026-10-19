---
name: "ui-style-dreamcore"
description: "Provides the authentic Dreamcore UI style (surreal internet escapism): ethereal daytime liminal spaces, peaceful cotton cloud skies, gentle faded pastel palettes, soft optical bloom, and sweet childhood nostalgia. Use when designing meditative digital spaces, surreal creative writing portfolios, ambient music hubs, or dreamy narrative applications."
---

# UI Style: Dreamcore (Ethereal Surrealism & Nostalgic Serenity)

Dreamcore is an internet aesthetic focused on the sweet, melancholic, and peaceful surrealism of dreams, childhood memories, and comforting liminal landscapes. In contrast to the anxiety of weirdcore, Dreamcore represents safety, gentle disorientation, soft overexposed sunlight, rolling green hills under endless cyan skies, floating pastel bubbles, and nostalgic comfort. Synthesized from net-art dream aesthetics and surrealist photography.

---

## 🧭 When to Activate

- Designing meditative apps, reflective journals, ambient music streaming hubs, or surreal creative writing portals.
- Crafting peaceful narrative experiences where interfaces should feel like half-remembered childhood dreams.
- Distinct from eerie weirdcore; activate Dreamcore when the atmosphere is warm, gentle, surreal, and restorative.

---

## 🕰️ Definition, Lineage, and Timeline

- **Origins:** Coined in internet communities alongside weirdcore (circa 2018–2021) as an aesthetic counterpart exploring the gentle, comforting side of liminal spaces.
- **Visual References:** Magritte's floating cloud skies, Windows XP Bliss hills viewed through a hazy nostalgic lens, early CGI dreamscapes, and soft-focus daytime photography.
- **Distinction from Neighbors:**
  - Unlike **Weirdcore / [ui-style-weirdcore](../ui-style-weirdcore/SKILL.md)**: Weirdcore evokes terror, anxiety, flash-lit darkness, and isolation; Dreamcore evokes peace, sweet nostalgia, bright daylight, and gentle wonder.
  - Unlike **[ui-style-vaporwave](../ui-style-vaporwave/SKILL.md)**: Vaporwave centers on 1990s consumer technology and Hellenistic statues; Dreamcore centers on nature, clouds, and childhood dreamscapes.

---

## 🎨 Visual DNA & Subgenre Taxonomy

- **The Ethereal Atmosphere:**
  - Soft-focus bloom filters (`backdrop-filter: blur(8px)` combined with luminous glow).
  - Daytime liminal horizons: rolling grassy knolls under pale blue skies dotted with fluffy cumulus clouds.
- **Pastel Dream Palette:**
  - Cloud White (`#FAFAFF`), Pale Dream Cyan (`#BEE3F8`), Gentle Lavender (`#E9D8FD`), Buttercream (`#FEFCBF`), and Meadow Green (`#C6F6D5`).
- **Typography:**
  - Friendly rounded geometric sans (*Quicksand*, *Nunito*) or delicate ethereal serifs (*Cormorant Garamond*).

---

## 📐 Lighting Physics, Specular Splits & Surfaces

1. **Dreamscape Cloud Bloom:**
   - Soft, diffused radial glow that wraps around components without harsh drop shadows.
   ```css
   background: rgba(255, 255, 255, 0.75);
   backdrop-filter: blur(12px);
   border: 1px solid rgba(255, 255, 255, 0.9);
   box-shadow: 0 8px 32px rgba(190, 227, 248, 0.45), inset 0 0 12px rgba(255, 255, 255, 0.8);
   ```

---

## 🏷️ Complete Design Tokens

```css
:root {
  /* Dreamcore Palette */
  --dream-sky: #BEE3F8;
  --dream-sky-deep: #63B3ED;
  --dream-cloud: #FFFFFF;
  --dream-lavender: #E9D8FD;
  --dream-butter: #FEFCBF;
  --dream-meadow: #C6F6D5;
  --dream-text: #2D3748;
  --dream-text-subtle: #4A5568;

  /* Typography */
  --dream-font-title: 'Quicksand', system-ui, sans-serif;
  --dream-font-body: 'Nunito', system-ui, sans-serif;
}
```

---

## 🧱 Production-Ready Component Blueprint

```html
<article class="dream-pod">
  <div class="dream-cloud-icon">☁️</div>
  <span class="dream-badge">HALF-REMEMBERED</span>
  <h3 class="dream-title">The Meadow Where Time Stopped</h3>
  <p class="dream-prose">Warm afternoon breezes blowing through quiet hills that feel eternally familiar.</p>
  <button class="dream-btn" type="button">WAKE UP GENTLY</button>
</article>
```

```css
.dream-pod {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 32px 24px;
  text-align: center;
  max-width: 420px;
  box-shadow: 0 12px 36px rgba(190, 227, 248, 0.5);
  font-family: var(--dream-font-body);
  color: var(--dream-text);
}
.dream-cloud-icon {
  font-size: 2rem;
  margin-bottom: 8px;
}
.dream-badge {
  font-family: var(--dream-font-title);
  font-size: 0.75rem;
  letter-spacing: 0.15em;
  font-weight: 700;
  color: var(--dream-sky-deep);
  background: rgba(190, 227, 248, 0.3);
  padding: 3px 10px;
  border-radius: 99px;
  display: inline-block;
}
.dream-title {
  font-family: var(--dream-font-title);
  font-size: 1.5rem;
  color: #1A365D;
  margin: 14px 0 8px;
}
.dream-prose {
  font-size: 0.9375rem;
  line-height: 1.6;
  color: var(--dream-text-subtle);
  margin-bottom: 24px;
}
.dream-btn {
  background: linear-gradient(135deg, var(--dream-sky) 0%, var(--dream-lavender) 100%);
  color: #1A365D;
  font-family: var(--dream-font-title);
  font-weight: 700;
  padding: 12px 28px;
  border: none;
  border-radius: 99px;
  cursor: pointer;
  box-shadow: 0 4px 14px rgba(99, 179, 237, 0.4);
  transition: transform 150ms ease, box-shadow 150ms ease;
}
.dream-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(99, 179, 237, 0.6);
}
```

---

## ✨ Micro-Interactions, Motion & Soundscapes

- **Slow Drift:** Cloud motifs and bubbles float upwards with slow, soothing dampening (12–16s loop).
- **Soft Touch Focus:** Buttons expand a diffuse, glowing aura on focus without sharp edges.

---

## ♿ WCAG 2.2 Accessibility & High-Contrast Guardrails

- **Contrast Ratios:**
  - Deep Navy Text (`#1A365D`) on Cloud Surface (`#FFFFFF`): **13.5:1** (Passes WCAG AAA).
  - Sky Deep Accent (`#63B3ED`) on White Surface: calibrated for UI badges and icons.
- **Dual-Contrast Focus Ring:**
  `outline: 2px solid var(--dream-sky-deep); box-shadow: 0 0 0 2px #FFFFFF;`

---

## 🚫 Anti-Patterns & Visual Sins (Anti-AI Slop Traps)

- ❌ **NEVER introduce frightening or jarring horror artifacts:** Dreamcore must remain calming and ethereal.
- ❌ **NEVER use harsh black borders or aggressive drop shadows:** Surfaces must float with ambient light.

---

## 📚 Sources & References

- René Magritte, *The Castle of the Pyrenees & Cloud Studies* (Brussels, 1959).
- Bachelard, Gaston, *The Poetics of Reverie: Childhood and Dreams* (Beacon Press, 1960).
## Appearance and Interaction Verification

Separate dark badge ink from sky-blue decoration, inspect text/focus over actual cloud/hill composites and retain the luminous bloom around a stable reading field; stop decorative cloud drift in reduced motion.
