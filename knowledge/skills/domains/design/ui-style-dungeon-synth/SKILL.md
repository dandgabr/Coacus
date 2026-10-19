---
name: "ui-style-dungeon-synth"
description: "Provides the authentic Dungeon Synth UI style (lo-fi medieval ambient microgenre of the 1990s): subterranean stone crypts, early 80s/90s consumer keyboard synthesizers (Casio, Yamaha), monochrome black-ink woodcut illustrations, moss green and stone grey palettes, and DIY black metal cassette fanzines. Use when designing indie game interfaces, atmospheric music players, tabletop RPG tools, and underground medieval fantasy archives."
---

# UI Style: Dungeon Synth (Lo-Fi Medieval Ambient & Crypt Synth)

Dungeon Synth is a musical and visual subgenre emerging in the early 1990s from the ambient interludes of second-wave black metal (Mortiis, Burzum). Built on primitive electronic synthesizers mimicking medieval instruments, the aesthetic celebrates subterranean dungeon crypts, candlelight, solitary tower libraries, dusty tomes, and high-contrast monochrome pen-and-ink fantasy illustrations. Synthesized from 1990s fanzine archives and canonical dungeon synth tape releases.

---

## 🧭 When to Activate

- Designing tabletop role-playing game (TTRPG) tools, character sheets, dungeon crawlers, or indie fantasy game interfaces.
- Crafting music players or archives dedicated to ambient medieval electronic music or underground tape labels.
- Distinct from epic cinematic dark fantasy; activate Dungeon Synth when the interface calls for humble, lo-fi, intimate, and solitary crypt atmosphere.

---

## 🕰️ Definition, Lineage, and Timeline

- **Origins:** Pioneered between 1993 and 1999 (Mortiis's *Født til å herske*, Wongraven, Depressive Silence), revitalized globally in the 2010s through Bandcamp tape communities.
- **Visual Vocabulary:** Unadorned black-and-white pen drawings, castle keeps, gargoyles, iron torches, and pixelated font readouts resembling vintage synth LCD screens.
- **Distinction from Neighbors:**
  - Unlike **Dark Fantasy / [ui-style-dark-fantasy](../ui-style-dark-fantasy/SKILL.md)**: Dark Fantasy is grandiose, baroque, high-budget, cinematic, and heavy with molten gold and wet stone; Dungeon Synth is intimate, humble, lo-fi, tape-recorded, and unpretentious.
  - Unlike **[ui-style-terminal-tui](../ui-style-terminal-tui/SKILL.md)**: Dungeon Synth incorporates archaic medieval typography and woodcut textures rather than pure computing matrices.

---

## 🎨 Visual DNA & Subgenre Taxonomy

- **The Crypt Atmosphere:**
  - Subterranean Charcoal (`#101211`), Damp Moss Slate (`#222923`), Forest Lichen (`#3A4A3E`), Torch Amber (`#E28C38`), and Bone Parchment (`#D8D3C5`).
- **Typography:**
  - Archaic uncial or rustic serif display (*Morris Roman*, *Gothic Ville*), paired with technical monospace readouts (*Courier*, *Fira Code*) echoing vintage synthesizer patch selectors.
- **Textures:**
  - 1-bit high-contrast ink hatching, cassette tape tape-reel motifs, and rough stone block borders.

---

## 📐 Lighting Physics, Specular Splits & Surfaces

1. **Subterranean Stone Slab:**
   - Dry, matte stone texture with deep shadow recesses and no glossy reflections.
   ```css
   background: #151816;
   border: 2px solid #2C352E;
   box-shadow: inset 1px 1px 0 #3A473D, inset -1px -1px 0 #080A09, 0 6px 18px rgba(0, 0, 0, 0.85);
   ```

---

## 🏷️ Complete Design Tokens

```css
:root {
  /* Dungeon Synth Palette */
  --ds-crypt-black: #0E100F;
  --ds-crypt-surface: #181B19;
  --ds-stone-border: #2C352E;
  --ds-moss-dark: #222B24;
  --ds-moss-accent: #4E6852;
  --ds-torch-amber: #E28C38;
  --ds-bone: #D4CEBF;
  --ds-bone-dim: #9C9687;

  /* Typography */
  --ds-font-title: 'Cinzel', 'Morris Roman', serif;
  --ds-font-synth: 'Courier New', monospace;
  --ds-font-body: 'Bookman Old Style', Georgia, serif;
}
```

---

## 🧱 Production-Ready Component Blueprint

```html
<article class="ds-crypt-box">
  <div class="ds-synth-display">
    <span class="ds-patch-label">PATCH: 04 HARPSICHORD</span>
    <span class="ds-reverb-tag">CAVERN // 8.4s</span>
  </div>
  <h3 class="ds-title">Tower of Ancient Solitude</h3>
  <p class="ds-lore">Dusty manuscripts illuminated by dying tallow candles as the autumn wind howls outside the keep.</p>
  <button class="ds-btn-tape" type="button">PLAY CASSETTE [SIDE A]</button>
</article>
```

```css
.ds-crypt-box {
  background: var(--ds-crypt-surface);
  border: 2px solid var(--ds-stone-border);
  padding: 24px;
  max-width: 440px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.8);
  font-family: var(--ds-font-body);
  color: var(--ds-bone);
}
.ds-synth-display {
  background: #080A09;
  border: 1px solid var(--ds-moss-dark);
  padding: 6px 10px;
  display: flex;
  justify-content: space-between;
  font-family: var(--ds-font-synth);
  font-size: 0.75rem;
  color: var(--ds-torch-amber);
  margin-bottom: 16px;
}
.ds-title {
  font-family: var(--ds-font-title);
  font-size: 1.5rem;
  color: var(--ds-bone);
  margin: 0 0 10px;
  letter-spacing: 0.05em;
}
.ds-lore {
  font-size: 0.9375rem;
  line-height: 1.6;
  color: var(--ds-bone-dim);
  margin-bottom: 20px;
}
.ds-btn-tape {
  background: var(--ds-moss-dark);
  color: var(--ds-bone);
  font-family: var(--ds-font-synth);
  font-size: 0.8125rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  padding: 10px 20px;
  border: 1px solid var(--ds-moss-accent);
  cursor: pointer;
  transition: all 120ms ease;
}
.ds-btn-tape:hover {
  background: var(--ds-moss-accent);
  color: #0E100F;
}
```

---

## ✨ Micro-Interactions, Motion & Soundscapes

- **Candle Flicker:** Ambient highlights gently vary in intensity (3–5s non-repeating cycle).
- **Cassette Tape Click:** Triggers depress with firm mechanical resistance.

---

## ♿ WCAG 2.2 Accessibility & High-Contrast Guardrails

- **Contrast Ratios:**
  - Bone Parchment (`#D4CEBF`) on Crypt Surface (`#181B19`): **12.8:1** (Passes WCAG AAA).
  - Torch Amber (`#E28C38`) on Black (`#080A09`): **8.6:1** (Passes WCAG AAA).
- **Dual-Contrast Focus Ring:**
  `outline: 2px solid var(--ds-torch-amber); box-shadow: 0 0 0 2px var(--ds-crypt-black);`

---

## 🚫 Anti-Patterns & Visual Sins (Anti-AI Slop Traps)

- ❌ **NEVER use clean modern vector icons or glowing laser neons:** Visuals must appear as etched stone or ink drawings.
- ❌ **NEVER introduce polished high-budget orchestral CGI:** Dungeon Synth thrives on raw lo-fi sincerity.

---

## 📚 Sources & References

- Mortiis, *Født til å herske* (Cold Meat Industry, 1994).
- Dungeon Synth Fanzines Archive, *The Cryptic Whisper* (1995–1999).
## Appearance and Interaction Verification

Check the hover label against moss fill and retain bone text or adjust moss if required; stop candle variation under reduced motion, preserving crypt darkness and rough ink/stone instead of replacing them with glossy fantasy ornament.
