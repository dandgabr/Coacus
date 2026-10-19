---
name: "ui-style-gothicpunk"
description: "Provides the canonical Gothicpunk & Modern Gothic UI style (1991 onward): decadent dark-fantasy noir originating from Vampire: The Masquerade, featuring pointed lancet arches, stained-glass chiaroscuro, tarnished gold leaf, blood crimson accents, aged bone typography, and urban post-punk nihilism. Use when designing tabletop RPG interfaces, dark fantasy games, goth music platforms, or horror narrative worlds."
---

# UI Style: Gothicpunk & Modern Gothic

**Gothicpunk** (frequently hyphenated as **Gothic-Punk**) is the aesthetic collision of High Gothic ecclesiastical grandeur (pointed lancet arches, ribbed vaults, stone gargoyles, stained-glass windows) with late-20th-century punk nihilism, urban decay, and dark supernatural noir. Originating in tabletop roleplaying (*Vampire: The Masquerade*), Gothicpunk envisions modern metropolises where towering neo-Gothic skyscrapers loom over rain-slicked asphalt, shadows conceal ancient decadent aristocracies, and tarnished gold leaf accents bleed into near-black obsidian.

---

## 🧭 When to Activate

- Designing components, navigation, and character sheets for tabletop RPGs, vampire lore wikis, horror video games, or dark-fantasy narrative experiences.
- Dark nightlife, goth and post-punk music hubs, occult literature archives, or high-fashion noir editorial platforms.
- Replacing sterile modern dark mode with rich historical chiaroscuro, pointed lancet framing, blood-crimson highlights, and tarnished gold metallic textures.

---

## 🕰️ Definition, Lineage, and Timeline

- **Origins & Coinage:** Formalized in 1991 by Mark Rein-Hagen and White Wolf Publishing in the foundational rulebook for *Vampire: The Masquerade* (the *World of Darkness* setting). Defined as a heightened reality where the Gothic architecture of Europe looms oppressive over modern crime, corruption, and countercultural punk defiance.
- **Architectural & Subcultural Heritage:** Grounded in High Gothic cathedrals (Abbey of Saint-Denis, Notre-Dame de Paris, Chartres) and the 18th-century Gothic Revival, cross-pollinated with 1980s post-punk, Bauhaus, Siouxsie and the Banshees, and Clive Barker's dark supernatural horror.
- **Distinctions from Neighboring Styles:**
  - Unlike **Cyberpunk** (electric neon cyan/magenta, Japanese megacorporation logos, holographic HUDs, cyberware cables), Gothicpunk rejects electronic neon in favor of candlelit chiaroscuro, tarnished gold, cathedral arches, and velvet.
  - Unlike **Dark Fantasy / Grimdark** (medieval mud, rusty swords, peasant plague, unpaved fantasy kingdoms), Gothicpunk is explicitly urban, decadent, tailored, and set against modern or Victorian metropolitan architecture.
  - Unlike **Dark Mode First** (neutral minimal dark grays designed for code editors), Gothicpunk is deeply atmospheric, textured, theatrical, and emotionally menacing.
- **Absolute Veto:** Illegible walls of German blackletter or dripping blood text that destroy reading comprehension are strictly forbidden. Blackletter must be restricted to primary display titles, while body paragraphs use pristine high-contrast classical serifs.

---

## 🎨 Visual DNA & Subgenre Taxonomy

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 GOTHICPUNK VISUAL MATRIX                               │
├────────────────────────────┬────────────────────────────┬──────────────────────────────┤
│ 1. Aristocratic Masquerade │ 2. High Gothic Cathedral   │ 3. Urban Alley Post-Punk     │
│ • Blood crimson velvet     │ • Pointed lancet windows   │ • Photocopy xerox grit       │
│ • Tarnished antique gold   │ • Rose-window radial grids │ • Distressed torn margins    │
│ • Ornate crests & seals    │ • Chiseled stone masonry   │ • Scratched vinyl & asphalt  │
└────────────────────────────┴────────────────────────────┴──────────────────────────────┘
```

- **Palette & Shadow:** Subterranean obsidian black (`#0B0A0C`), cold cathedral slate (`#151419`), aged parchment bone (`#E9E2D0`), deep blood crimson (`#8B0A1A`), rich oxblood (`#4A0D14`), and tarnished antique gold (`#B08D3C`).
- **Architectural Geometry:** 50-degree pointed lancet arches, radial rose-window coordinates, gothic tracery trefoils, and tall vertical proportions.
- **Surfaces & Light:** Dramatic chiaroscuro (deep deep shadows illuminated by singular flickering warm candle highlights), stained-glass chromatic refractions, and subtle 35mm film grain.

---

## 📐 Lighting Physics, Specular Splits & Surfaces

1. **Cathedral Lancet Arch & Chiaroscuro Shadow:**
   - Deep subterranean dark background cut by a pointed arch with a warm golden top edge.
   ```css
   background-color: #0b0a0c;
   background-image: radial-gradient(circle at 50% 0%, rgba(176, 141, 60, 0.12) 0%, rgba(11, 10, 12, 0.98) 85%);
   box-shadow: inset 0 0 50px rgba(0, 0, 0, 0.95), 0 8px 30px rgba(0, 0, 0, 0.8);
   ```
2. **Tarnished Gold Foil Bezel:**
   - Burnished, weathered antique gold frame with dark crevices.
   ```css
   border: 1.5px solid #b08d3c;
   box-shadow: inset 0 0 8px rgba(176, 141, 60, 0.3), 0 0 15px rgba(139, 10, 26, 0.2);
   ```

---

## 🏷️ Complete Design Tokens

```css
:root {
  /* Subterranean Obsidian Grounds */
  --gothic-obsidian-bg: #0B0A0C;
  --gothic-crypt-surface: #151419;
  --gothic-crypt-card: #1C1A21;
  --gothic-cathedral-border: #2D2A35;

  /* Blood & Pigments */
  --gothic-blood-crimson: #8B0A1A;
  --gothic-blood-bright: #C1121F;
  --gothic-blood-glow: rgba(193, 18, 31, 0.35);
  --gothic-oxblood: #4A0D14;
  --gothic-bone-text: #E9E2D0;
  --gothic-bone-dim: #9E9788;

  /* Antique Metals */
  --gothic-tarnished-gold: #B08D3C;
  --gothic-gold-highlight: #D8B462;
  --gothic-cold-steel: #7A8089;

  /* Typography */
  --gothic-font-display: 'UnifrakturCook', 'Cinzel Decorative', serif;
  --gothic-font-title: 'Cormorant Garamond', 'Playfair Display', serif;
  --gothic-font-body: 'Cormorant', Georgia, serif;
  --gothic-font-punk: 'League Gothic', 'Oswald', sans-serif;

  /* Geometry */
  --gothic-border-radius: 2px;
}
```

---

## 🔤 Typography & Lettering Architecture

- **Primary Display Titles:** Historic blackletter or ornate inscriptional serifs (*UnifrakturCook*, *Cinzel Decorative*) used sparingly for short, imposing headers and chapter markers.
- **Editorial Sub-headings & Prose:** Elegant high-contrast didone and old-style serifs (*Cormorant Garamond*, *Playfair Display*) set with generous tracking and 1.65 line-height, delivering aristocratic literary cadence.
- **Body Text:** High-contrast, easily readable book serifs (*Cormorant*, *EB Garamond*) set in aged bone (`#E9E2D0`) on obsidian. Never set multi-sentence body text in blackletter.
- **Punk Faction Stamps:** Heavy condensed grotesque caps (*League Gothic*, *Oswald*) for clandestine faction tags and counterculture zine inserts.

---

## 🖱️ Interaction Dynamics, Sound Cues & Motion

- **Fade-Up from Darkness:** Modals and dialogue panels emerge slowly from absolute black with long, cinematic opacity ramps (400ms–700ms).
- **Candle Ember Shimmer:** Status seals and active indicators possess a subtle, non-flashing ember warmth breathing between gold and crimson.
- **Hover Blood-Draw Underline:** Interactive links draw an ember-red underline outward from the center upon cursor hover.
- **Motion Reduction:** When `prefers-reduced-motion: reduce` is enabled, all candle flicker and cinematic fade-ups collapse into clean, instant state transitions.

---

## 🧩 Canonical Component Specifications

### 1. Lancet Arch Crypt Container (`.gothic-crypt-card`)
A pointed gothic container finished with tarnished gold borders and bone typography.
```html
<article class="gothic-crypt-card">
  <div class="gothic-card-header">
    <span class="gothic-sect-tag">CAMARILLA ARCHIVE // COVENANT</span>
    <h3 class="gothic-title">The Masquerade Concordat</h3>
  </div>
  <p class="gothic-prose">Preserve the silence across all metropolitan havens under pain of blood hunt.</p>
</article>
```
```css
.gothic-crypt-card {
  background: var(--gothic-crypt-card);
  color: var(--gothic-bone-text);
  border: 1.5px solid var(--gothic-tarnished-gold);
  border-radius: var(--gothic-border-radius);
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.8), inset 0 0 20px rgba(176, 141, 60, 0.08);
  padding: 1.75rem;
  position: relative;
}
.gothic-sect-tag {
  font-family: var(--gothic-font-punk);
  font-size: 0.8rem;
  color: var(--gothic-blood-bright);
  letter-spacing: 0.12em;
  display: block;
  margin-bottom: 0.5rem;
}
.gothic-title {
  font-family: var(--gothic-font-title);
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0 0 0.75rem 0;
  color: var(--gothic-gold-highlight);
}
```

### 2. Blood Crimson Action Button (`.gothic-btn-blood`)
A primary action button finished in deep blood crimson with tarnished gold borders.
```css
.gothic-btn-blood {
  background: linear-gradient(180deg, #8B0A1A 0%, #4A0D14 100%);
  color: #FFFFFF;
  font-family: var(--gothic-font-title);
  font-size: 1.05rem;
  font-weight: 600;
  letter-spacing: 0.08em;
  padding: 0.75rem 1.8rem;
  border: 1.5px solid var(--gothic-tarnished-gold);
  border-radius: 2px;
  box-shadow: 0 3px 12px rgba(139, 10, 26, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.2);
  cursor: pointer;
  transition: box-shadow 0.2s ease, transform 0.15s ease;
}
.gothic-btn-blood:hover {
  background: linear-gradient(180deg, #A80E22 0%, #5E111A 100%);
  box-shadow: 0 4px 18px rgba(193, 18, 31, 0.7), inset 0 1px 0 rgba(255, 255, 255, 0.3);
  transform: translateY(-1px);
}
.gothic-btn-blood:active {
  transform: translateY(1px);
}
```

### 3. Pointed Lancet Window Divider (`.gothic-lancet-frame`)
A decorative border framing headers with a 50-degree pointed gothic arch profile.

### 4. Wax Seal Indicator (`.gothic-seal`)
A circular status badge stamped in antique crimson wax with golden sigil embroidery.

---

## ♿ Accessibility & Environmental Contrast (WCAG 2.2)

- **Contrast Mathematics:** Aged bone text (`#E9E2D0`) on obsidian black (`#0B0A0C`) delivers a 14.8:1 contrast ratio (exceeding WCAG AAA 7:1).
- **Red Text Contrast Guard:** Never set multi-sentence body text in blood red (`#8B0A1A`) against dark backgrounds (fails 4.5:1). Reserve bright crimson (`#C1121F`) strictly for large headers (at least 24px) or bold badges, where it meets 3.2:1 against slate surfaces.
- **Photosensitivity Protections (WCAG 2.3.1):** Never use rapid flashing or lightning effects. All ambient candle glows must be slow, subtle, and stay under 1.5 Hz.
- **Focus Rings:** High-visibility gold outline (`outline: 2px solid var(--gothic-gold-highlight); outline-offset: 3px;`).

---

## ✅ When to Use / ❌ When to Avoid

### Ideal Use Cases
- Vampire and horror tabletop RPG digital companions, character sheet tools, and rule compendiums.
- Gothic literature portals, dark-fantasy book promotion, and atmospheric music label storefronts.
- Narrative Halloween microsites and historical medieval horror experiences.

### Anti-Patterns & Prohibitions
- Healthcare, mental wellness, or medical software where dark horror induces distress.
- Banking or enterprise B2B SaaS where excessive dark ornament obscures financial data.
- Any real-world sectarian hate symbols or extremist neo-Nazi misappropriations of blackletter typography.

---

## 📚 Authoritative Sources & Historical Artifacts

- Mark Rein-Hagen, *Vampire: The Masquerade*, White Wolf Publishing, 1st ed. 1991.
- Erwin Panofsky, *Gothic Architecture and Scholasticism*, Meridian Books, 1957.
- Clive Barker, *The Books of Blood*, Sphere Books, 1984.
- Jakob Nielsen, *10 Usability Heuristics for User Interface Design*, Nielsen Norman Group, 1994.

---

## 🔗 Cross-Skill Integration & Dialect Relations

- **Sibling Dark Speculative Styles:** [ui-style-dark-fantasy](../ui-style-dark-fantasy/SKILL.md), [ui-style-dungeon-synth](../ui-style-dungeon-synth/SKILL.md), [ui-style-cyberpunk](../ui-style-cyberpunk/SKILL.md).
- **Atmospheric & Noir Peers:** [ui-style-dark-mode-first](../ui-style-dark-mode-first/SKILL.md), [ui-style-grain-noise-texture](../ui-style-grain-noise-texture/SKILL.md), [ui-style-editorial-archive-luxury](../ui-style-editorial-archive-luxury/SKILL.md).
## Appearance and Interaction Verification

Give small faction metadata a readable bone/gold ink or a contrasting wax/paper field; keep crimson as gothic material and reserve large crimson lettering only when its actual size/weight and composite pass, preserving lancet architecture and urban punk identity.

