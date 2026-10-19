---
name: "ui-style-dark-fantasy"
description: "Provides the authentic Dark Fantasy & Grimdark UI style: gothic cathedral architecture, Albrecht Dürer copperplate engravings, rusted wrought iron, damp castle stone, charred illuminated manuscripts, antique gold gilding, and blood-tinted glass. Use when designing epic dark RPG interfaces, grimdark gaming websites, dark fantasy lore archives, or gothic literary experiences."
---

# UI Style: Dark Fantasy (Gothic Grimdark & Antique Gold)

Dark Fantasy is an epic, visceral subgenre of fantasy that emphasizes dread, mortal peril, moral decay, and ancient fallen empires. Drawing visual authority from northern renaissance copperplate engravings (Albrecht Dürer), gothic cathedrals, wrought iron relic caskets, charred parchment scrolls, and antique gilded gold leaf tarnished by soot and blood. Synthesized from canonical grimdark literature (*The Witcher*, *Dark Souls*, *A Song of Ice and Fire*).

---

## 🧭 When to Activate

- Designing epic fantasy RPG interfaces, inventory screens, grimdark gaming companion apps, or dark lore encyclopedias.
- Crafting rich, tactile dark-mode applications where components must feel like heavy, forged physical relics.
- Distinct from humble lo-fi dungeon synth; activate Dark Fantasy when the aesthetic demands monumentality, gothic drama, and gilded craftsmanship.

---

## 🕰️ Definition, Lineage, and Timeline

- **Literary & Art Lineage:** Grounded in gothic literature (Mary Shelley, Bram Stoker), dark romanticism (Caspar David Friedrich), and renaissance master printmakers (Dürer, Goya).
- **Modern Incarnations:** High-budget grimdark media, from FromSoftware's *Elden Ring* and *Dark Souls* to *Diablo* and modern dark fantasy cinema.
- **Distinction from Neighbors:**
  - Unlike **Dungeon Synth / [ui-style-dungeon-synth](../ui-style-dungeon-synth/SKILL.md)**: Dungeon Synth is humble, lo-fi, tape-recorded, and unadorned; Dark Fantasy is cinematic, ornate, gilded, and heavily structured.
  - Unlike **[ui-style-gothicpunk](../ui-style-gothicpunk/SKILL.md)**: Gothicpunk fuses gothic architecture with modern urban leather and nightlife; Dark Fantasy remains archaic, medieval, and mythic.

---

## 🎨 Visual DNA & Subgenre Taxonomy

- **Ancient Materials:**
  - Carved Granite (`#15161A`), Wrought Iron (`#25272E`), Weathered Gilt (`#C5A059`), Deep Claret Blood (`#7A1C1C`), and Burnished Bronze (`#8C6239`).
- **Gothic Structural Form:**
  - Pointed lancet arches, trefoil tracery, chamfered corner frames, and ornate medieval scrollwork borders.
- **Typography:**
  - Monumental roman capitals and gothic blackletter display (*Cinzel*, *UnifrakturMaguntia*, *MedievalSharp*), accompanied by classical serif body text (*IM Fell English*, *EB Garamond*).

---

## 📐 Lighting Physics, Specular Splits & Surfaces

1. **Tarnished Gilded Gold Bevel:**
   - Multi-layered metallic gradient reflecting low ambient firelight.
   ```css
   background: linear-gradient(180deg, #E5C378 0%, #C5A059 40%, #8C6239 85%, #593D22 100%);
   -webkit-background-clip: text;
   -webkit-text-fill-color: transparent;
   filter: drop-shadow(0 2px 4px rgba(0,0,0,0.9));
   ```
2. **Heavy Forged Iron Panel:**
   ```css
   background: #181A20;
   border: 2px solid #363A45;
   box-shadow: inset 1px 1px 0 #525868, inset -1px -1px 0 #0D0E12, 0 12px 32px rgba(0, 0, 0, 0.9);
   ```

---

## 🏷️ Complete Design Tokens

```css
:root {
  /* Dark Fantasy Palette */
  --df-abyss: #0B0C0E;
  --df-stone-base: #14161A;
  --df-stone-panel: #1D2026;
  --df-iron-border: #3A3F4D;
  --df-gold-bright: #E5C378;
  --df-gold-tarnished: #C5A059;
  --df-gold-dark: #7A5C2B;
  --df-blood: #8A1C1C;
  --df-parchment-text: #E6E1D3;

  /* Typography */
  --df-font-display: 'Cinzel Decorative', 'Cinzel', serif;
  --df-font-body: 'IM Fell English', Georgia, serif;
}
```

---

## 🧱 Production-Ready Component Blueprint

```html
<div class="df-relic-card">
  <div class="df-card-accent"></div>
  <header class="df-header">
    <span class="df-tier-badge">LEGENDARY ARTIFACT</span>
    <h3 class="df-title">Blade of the Eclipse</h3>
  </header>
  <p class="df-lore">Forged within the ash of a fallen cathedral, its edge drinks the fading light of dying stars.</p>
  <div class="df-stats-row">
    <span>ATTACK: 640</span>
    <span class="df-stat-blood">BLOOD LOSS: +85</span>
  </div>
  <button class="df-btn-gilt" type="button">COMMUNE WITH RELIC</button>
</div>
```

```css
.df-relic-card {
  background: var(--df-stone-panel);
  border: 2px solid var(--df-iron-border);
  border-radius: 4px;
  padding: 28px;
  max-width: 440px;
  box-shadow: 0 12px 36px rgba(0, 0, 0, 0.95);
  font-family: var(--df-font-body);
  color: var(--df-parchment-text);
  position: relative;
}
.df-tier-badge {
  font-family: var(--df-font-display);
  font-size: 0.75rem;
  letter-spacing: 0.2em;
  color: var(--df-gold-tarnished);
  border-bottom: 1px solid var(--df-gold-dark);
  padding-bottom: 4px;
}
.df-title {
  font-family: var(--df-font-display);
  font-size: 1.625rem;
  color: var(--df-gold-bright);
  margin: 12px 0 8px;
  text-shadow: 0 2px 8px rgba(0,0,0,0.8);
}
.df-lore {
  font-size: 1rem;
  font-style: italic;
  line-height: 1.6;
  color: #B5B0A2;
  margin-bottom: 20px;
}
.df-stats-row {
  display: flex;
  justify-content: space-between;
  background: var(--df-stone-base);
  border: 1px solid #2B2F3A;
  padding: 8px 14px;
  font-family: var(--df-font-display);
  font-size: 0.8125rem;
  margin-bottom: 24px;
}
.df-stat-blood {
  color: #D34B4B;
}
.df-btn-gilt {
  width: 100%;
  background: linear-gradient(180deg, #2D323E 0%, #1A1D24 100%);
  color: var(--df-gold-bright);
  font-family: var(--df-font-display);
  font-size: 0.875rem;
  font-weight: 700;
  letter-spacing: 0.15em;
  padding: 12px;
  border: 1px solid var(--df-gold-dark);
  cursor: pointer;
  box-shadow: inset 0 1px 0 rgba(229, 195, 120, 0.3), 0 4px 12px rgba(0,0,0,0.6);
  transition: all 150ms ease;
}
.df-btn-gilt:hover {
  background: linear-gradient(180deg, #3D4454 0%, #222630 100%);
  border-color: var(--df-gold-bright);
  box-shadow: 0 0 16px rgba(229, 195, 120, 0.4);
}
```

---

## ✨ Micro-Interactions, Motion & Soundscapes

- **Ember Drift:** Faint orange embers slowly rise through the background atmosphere.
- **Relic Impact:** Triggers lock in place with heavy gothic stone/iron weight.

---

## ♿ WCAG 2.2 Accessibility & High-Contrast Guardrails

- **Contrast Ratios:**
  - Parchment Text (`#E6E1D3`) on Stone Surface (`#1D2026`): **13.9:1** (Passes WCAG AAA).
  - Bright Gold (`#E5C378`) on Dark Stone (`#14161A`): **11.2:1** (Passes WCAG AAA).
- **Dual-Contrast Focus Ring:**
  `outline: 2px solid var(--df-gold-bright); box-shadow: 0 0 0 2px #000;`

---

## 🚫 Anti-Patterns & Visual Sins (Anti-AI Slop Traps)

- ❌ **NEVER use rounded friendly bubble buttons:** Frames must be forged with sharp bevels and gothic geometry.
- ❌ **NEVER use modern tech sans-serifs:** Use high-contrast classical serifs and monumental lettering.

---

## 📚 Sources & References

- Albrecht Dürer, *The Apocalypse & Knight, Death and the Devil* (Nuremberg, 1498–1513).
- H.P. Lovecraft, *Supernatural Horror in Literature* (The Recluse, 1927).
## Appearance and Interaction Verification

Check the darkest tarnished gradient stop against the actual iron/stone backdrop and supply solid gilt ink for functional titles when needed; make ember drift decorative, scoped and static/off under reduced motion without brightening the grimdark substrate.
