---
name: "ui-style-lunarpunk"
description: "Provides the canonical Lunarpunk & Nocturnal Cryptographic UI style (2022-present): solarpunk's nocturnal sibling combining bioluminescent forest flora, lunar phase cycles, midnight violet grounds, zero-knowledge privacy veils, and cryptographic defense. Use when designing privacy-first platforms, cryptographic tools, nighttime meditation apps, or nocturnal ecological worldbuilding experiences."
---

# UI Style: Lunarpunk & Nocturnal Cryptographic

**Lunarpunk** is the nocturnal, introspective, and privacy-centric counterpart to solarpunk. Where solarpunk flourishes in the daytime with radiant solar energy and civic transparency, Lunarpunk thrives in the restorative sanctuary of the night: bioluminescent forest flora, soft moonlit mist, mycelial networks, and zero-knowledge cryptography. In digital interfaces, Lunarpunk combines deep midnight violet backgrounds with gentle bioluminescent cyan glows, starlight silver typography, lunar phase indicators, and reveal-on-intent privacy veils.

---

## 🧭 When to Activate

- Designing privacy-first platforms, zero-knowledge cryptography tools, secure communication protocols, or decentralized identity wallets.
- Night-first applications for sleep health, guided meditation, celestial stargazing, astronomy tools, or ambient generative music.
- Ecological worldbuilding portals and narrative games focusing on nocturnal forest ecosystems, moonlit bioluminescence, and silent digital resilience.

---

## 🕰️ Definition, Lineage, and Timeline

- **Origins & Emergence:** Crystallized in early 2022 across ecological futurism and decentralized privacy communities (e.g. *Solarpunk Station*, Gitcoin, DarkFi). Positioned as the recognition that daytime transparency without nocturnal privacy leaves regenerative communities vulnerable to surveillance.
- **The Two Core Strands:**
  1. *The Ecological Nocturnal Sanctuary:* Restorative night nature, mycelial networks, bioluminescent fungi (*Panellus stipticus*), fireflies, and lunar phase rhythms.
  2. *The Cypherpunk Privacy Shield:* Digital privacy by default, zero-knowledge proofs (zk-SNARKs), obfuscated telemetry, and intentional data-shielding veils.
- **Distinctions from Neighboring Styles:**
  - Unlike **Solarpunk** (sunlit daytime, transparent civic infrastructure, sun gold and leaf green), Lunarpunk is nocturnal, introspective, violet, and starlit.
  - Unlike **Cyberpunk** (dystopian, hostile, rain-soaked neon alleys, weaponized corporate networks), Lunarpunk's darkness is restorative, organic, communal, and serene.
  - Unlike **Gothicpunk** (decadent aristocratic vampires, cathedral arches, blood red), Lunarpunk is ecological, botanical, and calm.
- **Absolute Veto:** Faux "privacy theater" consisting of superficial lock clipart without genuine cryptographic user agency. Any interface claiming privacy must implement honest default-private permissions and clear consent controls.

---

## 🎨 Visual DNA & Subgenre Taxonomy

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 LUNARPUNK VISUAL MATRIX                                │
├────────────────────────────┬────────────────────────────┬──────────────────────────────┤
│ 1. Bioluminescent Forest   │ 2. Zero-Knowledge Shield   │ 3. Celestial Starlight       │
│ • Deep midnight indigo     │ • Concealed private veils  │ • Moon silver typography     │
│ • Fungal spore cyan glow   │ • Intentional reveal click │ • Concentric phase rings     │
│ • Soft organic card curves │ • Lock-and-leaf indicators │ • Star chart coordinate axes │
└────────────────────────────┴────────────────────────────┴──────────────────────────────┘
```

- **Palette & Radiance:** Deep midnight ground (`#0E1224`), cosmic indigo (`#141A33`), radiant starlight violet (`#7C5CFF`), soft orchid (`#B57BEE`), bioluminescent cyan (`#2FE0C2`), moon silver (`#D9DEF2`), and firefly amber (`#F2D36B`).
- **Surfaces & Halos:** Translucent frosted containers (`rgba(20, 26, 51, 0.72)`), subtle 1px starlight borders, and soft cyan ambient drop glows (`box-shadow: 0 0 24px -6px rgba(47, 224, 194, 0.45)`).
- **Iconography:** Lunar phases (new, crescent, full), mycelial network nodes, moths, glowing flora, and cryptographic shields.

---

## 📐 Lighting Physics, Specular Splits & Surfaces

1. **Bioluminescent Flora Glow:**
   - Soft, restorative cyan emission radiating from dark organic panels.
   ```css
   background-color: rgba(20, 26, 51, 0.75);
   border: 1px solid rgba(124, 92, 255, 0.45);
   box-shadow: 0 0 28px -6px rgba(47, 224, 194, 0.35), inset 0 0 12px rgba(47, 224, 194, 0.08);
   border-radius: 20px;
   ```
2. **Zero-Knowledge Privacy Blur Veil:**
   - Obfuscated private data that clears on deliberate user intent.
   ```css
   filter: blur(8px);
   transition: filter 0.3s ease-out;
   cursor: pointer;
   ```

---

## 🏷️ Complete Design Tokens

```css
:root {
  /* Midnight Grounds */
  --lunar-midnight-bg: #0E1224;
  --lunar-indigo-surface: #141A33;
  --lunar-card-surface: rgba(20, 26, 51, 0.75);

  /* Bioluminescent Emissions */
  --lunar-teal-glow: #2FE0C2;
  --lunar-teal-dim: rgba(47, 224, 194, 0.3);
  --lunar-violet-light: #7C5CFF;
  --lunar-orchid: #B57BEE;
  --lunar-firefly-amber: #F2D36B;

  /* Typography & Inks */
  --lunar-silver-moon: #D9DEF2;
  --lunar-silver-muted: #9BA4C8;

  /* Borders & Optical Geometry */
  --lunar-border: 1px solid rgba(124, 92, 255, 0.4);
  --lunar-border-active: 1px solid var(--lunar-teal-glow);
  --lunar-radius: 20px;

  /* Typography */
  --lunar-font-display: 'Fraunces', 'Cormorant Garamond', serif;
  --lunar-font-body: 'Plus Jakarta Sans', system-ui, sans-serif;
  --lunar-font-mono: 'Space Mono', monospace;
}
```

---

## 🔤 Typography & Lettering Architecture

- **Primary Display Headings:** Lyrical, organic display serifs (*Fraunces*, *Cormorant Garamond*, *Spectral*) with soft flared terminals and delicate weight modulation.
- **Body & Paragraphs:** High-contrast neutral sans (*Plus Jakarta Sans*, *Inter*) set in luminous moon silver (`#D9DEF2`) on midnight indigo with 1.7 line-height.
- **Cryptographic Identifiers:** Clean monospaced fonts (*Space Mono*) for public keys (`0x71a...`), zero-knowledge proof commitments, and phase timestamps.

---

## 🖱️ Interaction Dynamics, Sound Cues & Motion

- **Bioluminescent Bloom on Focus:** Cards and inputs intensify their cyan ambient glow smoothly when hovered or keyboard-focused (`transition: box-shadow 0.3s ease`).
- **Reveal-on-Intent for Private Fields:** Sensitive account balances or cryptographic secrets blur by default and un-blur only upon explicit user click (never on mere mouse hover).
- **Lunar Cycle Transition:** Tabs and progress stages advance with circular celestial phase sweeps.
- **Motion Reduction:** When `prefers-reduced-motion: reduce` is enabled, all background star drift and breathing glows freeze into static, soothing dark layouts.

---

## 🧩 Canonical Component Specifications

### 1. Bioluminescent Flora Card (`.lunar-card`)
A dark indigo container with starlight borders, soft cyan ambient glow, and moon silver typography.
```html
<article class="lunar-card">
  <div class="lunar-card-header">
    <span class="lunar-phase">WANING CRESCENT // 22%</span>
    <h3 class="lunar-title">Mycelial Canopy Mesh</h3>
  </div>
  <p class="lunar-text">Local sensor network reporting zero packet interception across dark peer-to-peer relay nodes.</p>
</article>
```
```css
.lunar-card {
  background: var(--lunar-card-surface);
  color: var(--lunar-silver-moon);
  border: var(--lunar-border);
  border-radius: var(--lunar-radius);
  box-shadow: 0 0 24px -6px var(--lunar-teal-dim);
  padding: 2rem;
  position: relative;
  transition: box-shadow 0.3s ease, border-color 0.3s ease;
}
.lunar-card:hover {
  border-color: var(--lunar-teal-glow);
  box-shadow: 0 0 32px -4px rgba(47, 224, 194, 0.45);
}
.lunar-phase {
  font-family: var(--lunar-font-mono);
  font-size: 0.75rem;
  color: var(--lunar-orchid);
  letter-spacing: 0.08em;
  display: block;
  margin-bottom: 0.5rem;
}
```

### 2. Zero-Knowledge Shield Action Button (`.lunar-btn`)
An action trigger glowing with bioluminescent cyan luminescence and moonlit border.
```css
.lunar-btn {
  background: rgba(47, 224, 194, 0.12);
  color: var(--lunar-teal-glow);
  font-family: var(--lunar-font-body);
  font-size: 1rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  padding: 0.75rem 1.8rem;
  border: 1px solid var(--lunar-teal-glow);
  border-radius: 9999px;
  box-shadow: 0 0 14px rgba(47, 224, 194, 0.25);
  cursor: pointer;
  transition: background 0.2s ease, box-shadow 0.2s ease, transform 0.15s ease;
}
.lunar-btn:hover {
  background: var(--lunar-teal-glow);
  color: #0E1224;
  box-shadow: 0 0 24px rgba(47, 224, 194, 0.5);
  transform: translateY(-2px);
}
```

### 3. Reveal-on-Intent Privacy Shield (`.lunar-privacy-veil`)
A blurred data box that decrypts and un-blurs only upon deliberate user click.

### 4. Lunar Phase Progress Dial (`.lunar-dial`)
A circular progress indicator rendering the eight classical astronomical moon phases.

---

## ♿ Accessibility & Environmental Contrast (WCAG 2.2)

- **Contrast Mathematics:** Moon silver text (`#D9DEF2`) on midnight indigo (`#0E1224`) achieves an exceptional 12.8:1 contrast ratio (exceeding WCAG AAA 7:1).
- **Secondary Elements:** Bioluminescent cyan (`#2FE0C2`) achieves 11.2:1 against the background, ensuring high-contrast indicators. Saturated violet must be lightened to `#A794FF` for body text to satisfy 4.5:1.
- **Privacy Obfuscation (WCAG 4.1.2):** Blurred private data must be accompanied by an explicit accessible button with `aria-expanded` and an informative accessible label (e.g. "Reveal private wallet balance").
- **Focus Rings:** Unmistakable cyan outline with 3px offset (`outline: 2px solid var(--lunar-teal-glow); outline-offset: 3px;`).

---

## ✅ When to Use / ❌ When to Avoid

### Ideal Use Cases
- Cryptographic privacy tools, zero-knowledge wallets, and decentralized communication protocols.
- Restorative sleep trackers, nighttime wellness journals, and astronomy observation suites.
- Dark-mode ecological fiction, botanical narrative games, and ambient music portals.

### Anti-Patterns & Prohibitions
- High-intensity daytime sales dashboards or high-frequency stock exchange desks.
- Applying un-scrimmed dark UI to outdoor bright-sunlight mobile contexts where glare washes out dark indigo.
- Hiding critical navigation controls under a veil of "mystery" that confuses screen readers.

---

## 📚 Authoritative Sources & Historical Artifacts

- Solarpunk Station, "What is Lunarpunk?", March 2022.
- DarkFi Community, *Manifesto of Lunarpunk & Anonymity*, 2022.
- W3C, *Web Content Accessibility Guidelines 2.2* (1.4.3, 4.1.2).
- Jakob Nielsen, *10 Usability Heuristics for User Interface Design*, Nielsen Norman Group, 1994.

---

## 🔗 Cross-Skill Integration & Dialect Relations

- **Sibling Ecological Styles:** [ui-style-solarpunk](../ui-style-solarpunk/SKILL.md), [ui-style-organic-biophilic](../ui-style-organic-biophilic/SKILL.md).
- **Dark Mode & Speculative Peers:** [ui-style-dark-mode-first](../ui-style-dark-mode-first/SKILL.md), [ui-style-aurora-mesh-gradient](../ui-style-aurora-mesh-gradient/SKILL.md), [ui-style-cyberpunk](../ui-style-cyberpunk/SKILL.md).
## Appearance and Interaction Verification

Distinguish decorative blur from confidentiality/decryption; keep reveal-on-intent operable through keyboard and assistive state, clear revealed content on owner change, and verify silver/orchid text against translucent moonlit surfaces.

