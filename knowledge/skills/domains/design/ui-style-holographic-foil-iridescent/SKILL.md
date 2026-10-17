---
name: "ui-style-holographic-foil-iridescent"
description: "Provides the canonical Holographic Foil & Iridescent Chrome UI style: optical thin-film interference simulation, dynamic rainbow diffraction angles, pearlescent shimmer, metallic specular flares, and shifting prismatic gradients. Use when designing exclusive membership tiers, collectible digital asset drops, luxury cosmetics platforms, or futuristic fintech card interfaces."
---

# UI Style: Holographic Foil & Iridescent Chrome

**Holographic Foil & Iridescent Chrome** is the optical simulation of light wave interference across microscopic thin-film layers—recreating the dynamic, angle-dependent rainbow shimmer of security holograms, collectible trading card foils (Pokémon, Magic: The Gathering), anodized titanium coatings, and mother-of-pearl surfaces. In digital user interfaces, Holographic Foil combines dark obsidian or crisp silver substrates with multi-spectral gradient shaders, cursor-tracking specular light flares, metallic border reflections, and tactile 3D perspective tilts.

---

## 🧭 When to Activate

- Exclusive membership tiers, VIP tier passes, or premium black-card fintech dashboards.
- Collectible digital assets, physical card game companion apps, limited-edition streetwear drops, or luxury cosmetic brand landing pages.
- Elevating cards, hero titles, or interactive badges with tangible physical foil shimmer and prismatic depth.

---

## 🕰️ Definition, Lineage, and Timeline

- **Physical Heritage:** Grounded in the optical physics of holography (invented by Dennis Gabor, Nobel Prize in Physics 1971) and security embossing pioneered by the American Bank Note Company in 1983 (credit card dove holograms). Exploded in youth culture through 1990s foil-stamped trading cards.
- **Digital Resurgence (2020s):** Re-imagined in modern web architecture via CSS conical gradients, WebGL thin-film interference shaders, and gyroscope-driven mobile card simulators (notably Simon Goellner's Pokémon foil CSS experiments).
- **Distinctions from Neighboring Styles:**
  - Unlike **Glassmorphism** (frosted translucent blur, passive light transmission), Holographic Foil is opaque, reflective, metallic, and actively generates spectral color shifts.
  - Unlike **Gradient & Duotone** (static pairing of two fixed colors), Holographic Foil dynamically sweeps through the full 360-degree rainbow spectrum based on pointer movement.
  - Unlike **Aurora / Mesh Gradient** (soft ambient blurred background fields), Holographic Foil is sharp, reflective, and contained within tangible cards and badges.
- **Absolute Veto:** Illegible thin text filled with high-frequency rainbow gradients floating directly over busy foil backgrounds. Gradient text is strictly reserved for large display titles with solid contrast backing; body copy must always use solid high-contrast monochrome ink.

---

## 🎨 Visual DNA & Subgenre Taxonomy

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              HOLOGRAPHIC FOIL MATRIX                                   │
├────────────────────────────┬────────────────────────────┬──────────────────────────────┤
│ 1. Collectible Card Foil   │ 2. Pearlescent Iridescent  │ 3. Rainbow Titanium Chrome   │
│ • Prismatic diagonal flare │ • Subtle pastel pearl glow │ • Saturated neon spectrum    │
│ • Pointer tracking sheen   │ • Soft lavender & mint     │ • High-specular mirror edge  │
│ • Holographic starbursts   │ • Clean luxury beauty mood │ • Dark obsidian chassis      │
└────────────────────────────┴────────────────────────────┴──────────────────────────────┘
```

- **Palette & Spectral Rays:** Deep obsidian canvas (`#0B0C10`), pearlescent violet (`#E0C3FC`), electric mint (`#8EC5FC`), radiant magenta (`#FBC2EB`), solar gold (`#FFE082`), and holographic platinum silver (`#F3F4F6`).
- **Prismatic Optics:** Thin-film interference simulation created through multi-stop linear and conic gradients tilted at dynamic angles.
- **Surface Lighting:** Directional specular sweep traversing the surface on hover (`transform: translateX(-100%)` to `translateX(100%)`).

---

## 📐 Lighting Physics, Specular Splits & Surfaces

1. **Thin-Film Prismatic Interference Surface:**
   - Multi-chromatic specular gradient layered over an obsidian core.
   ```css
   background: linear-gradient(
     135deg,
     #ff9a9e 0%,
     #fecfef 15%,
     #a1c4fd 35%,
     #c2e9fb 50%,
     #d4fc79 70%,
     #96e6a1 85%,
     #ff9a9e 100%
   );
   background-size: 300% 300%;
   box-shadow: 0 10px 30px rgba(161, 196, 253, 0.25);
   ```
2. **Metallic Hologram Card with Specular Flare:**
   - Dark core with a sweeping rainbow holographic border and sheen overlay.
   ```css
   border: 1.5px solid transparent;
   background:
     linear-gradient(#0f1016, #0f1016) padding-box,
     linear-gradient(135deg, #ff007f, #00f0ff, #ffe600, #ff007f) border-box;
   box-shadow: 0 12px 36px rgba(0, 0, 0, 0.6), inset 0 0 20px rgba(255, 255, 255, 0.05);
   ```

---

## 🏷️ Complete Design Tokens

```css
:root {
  /* Substrates & Obsidian Grounds */
  --holo-obsidian-bg: #0B0C10;
  --holo-card-surface: #12141D;
  --holo-card-surface-light: #1A1D2B;

  /* Prismatic Foil Hues */
  --holo-prism-pink: #FF69B4;
  --holo-prism-cyan: #00F0FF;
  --holo-prism-gold: #FFE082;
  --holo-prism-purple: #9D4EDD;
  --holo-pearl-silver: #F3F4F6;

  /* Specular Sheen & Border */
  --holo-sheen-glow: rgba(0, 240, 255, 0.35);
  --holo-border: 1.5px solid rgba(255, 255, 255, 0.3);
  --holo-radius: 20px;

  /* Typography */
  --holo-font-display: 'Syne', 'Clash Display', sans-serif;
  --holo-font-body: 'Inter', system-ui, sans-serif;
  --holo-text-primary: #FFFFFF;
  --holo-text-secondary: #CBD5E1;
}
```

---

## 🔤 Typography & Lettering Architecture

- **Primary Display Headings:** Sculptural, wide geometric display sans-serifs (*Syne*, *Clash Display*, *Space Grotesk*) featuring bold, expressive proportions. Display titles can feature clipped holographic gradient fills (`-webkit-background-clip: text`).
- **Body & Paragraphs:** High-contrast, clean neutral sans (*Inter*) set in crisp snow white (`#FFFFFF`) or soft silver (`#CBD5E1`), ensuring effortless legibility over dark card substrates.
- **Badge & Certification Metrics:** Sleek uppercase small-caps with generous letter-spacing (0.08em to 0.15em).

---

## 🖱️ Interaction Dynamics, Sound Cues & Motion

- **Pointer-Tracking Specular Sweep:** As the cursor traverses a holographic card, the specular reflection gradient translates smoothly across the surface.
- **3D Card Perspective Tilt:** Moving the mouse tilts the card along the X and Y axes (`transform: perspective(1000px) rotateX(...) rotateY(...)`), simulating inspecting a physical foil card under a gallery spotlight.
- **Prismatic Wave Animation:** Status badges and border trims cycle through a subtle 8-second continuous rainbow rotation.
- **Motion Gating:** When `prefers-reduced-motion: reduce` is detected, 3D perspective tilts and continuous gradient cycles are disabled, presenting a static, elegant pearlescent gradient.

---

## 🧩 Canonical Component Specifications

### 1. Collector Hologram Card (`.holo-card`)
A dark obsidian card framed by a 1.5px rainbow diffraction border and sweeping sheen reflection.
```html
<article class="holo-card">
  <div class="holo-card-inner">
    <span class="holo-tier-badge">EDITION // 001 OF 100</span>
    <h3 class="holo-title">Cosmic Prism Key</h3>
    <p class="holo-desc">Cryptographic ownership token verified on optical quantum ledger.</p>
  </div>
</article>
```
```css
.holo-card {
  position: relative;
  background:
    linear-gradient(var(--holo-card-surface), var(--holo-card-surface)) padding-box,
    linear-gradient(135deg, #ff007f 0%, #00f0ff 50%, #ffe600 100%) border-box;
  border: 1.5px solid transparent;
  border-radius: var(--holo-radius);
  box-shadow: 0 12px 36px rgba(0, 0, 0, 0.6);
  padding: 2rem;
  color: var(--holo-text-primary);
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.holo-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 44px rgba(0, 240, 255, 0.25);
}
```

### 2. Prismatic Foil Action Button (`.holo-btn`)
An interactive button with shifting rainbow specular gradient fill and obsidian text.
```css
.holo-btn {
  background: linear-gradient(135deg, #FF69B4 0%, #00F0FF 50%, #FFE082 100%);
  color: #0B0C10;
  font-family: var(--holo-font-display);
  font-size: 1.05rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: 0.75rem 1.8rem;
  border: none;
  border-radius: 9999px;
  cursor: pointer;
  box-shadow: 0 4px 20px rgba(0, 240, 255, 0.35);
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.holo-btn:hover {
  box-shadow: 0 6px 28px rgba(255, 105, 180, 0.5);
  transform: translateY(-2px);
}
```

### 3. Holographic VIP Pass Pill (`.holo-pill`)
A small metallic badge with iridescent perimeter lighting.

### 4. Thin-Film Specular Shimmer Banner (`.holo-shimmer-banner`)
A horizontal ribbon reflecting dynamic rainbow light flares on cursor movement.

---

## ♿ Accessibility & Environmental Contrast (WCAG 2.2)

- **Contrast Protection:** Prismatic foil backgrounds must never sit directly beneath delicate body text. Body copy must always reside over a solid dark core (`#12141D`), ensuring a contrast ratio of 16.5:1 against pure white text.
- **Photosensitivity Safeguards (WCAG 2.3.1):** Shimmer loops and rainbow cycles must be smooth, continuous, and never flash or strobe above 2.0 Hz.
- **Focus Indicators:** Pure electric cyan outline with 3px offset (`outline: 3px solid #00F0FF; outline-offset: 3px;`).

---

## ✅ When to Use / ❌ When to Avoid

### Ideal Use Cases
- Limited-edition collectible card drops, NFT token showcases, and web3 pass holders.
- High-end beauty, luxury perfume, and avant-garde cosmetics e-commerce platforms.
- VIP fintech debit card tier selectors and futuristic credit products.

### Anti-Patterns & Prohibitions
- Text-heavy technical manuals, legal disclosures, or billing history logs.
- Low-contrast light backgrounds where iridescent foil becomes invisible.
- High-frequency rapid flashing effects that trigger migraine or photosensitive seizures.

---

## 📚 Authoritative Sources & Historical Artifacts

- Dennis Gabor, *Holography, 1948-1971*, Nobel Lecture in Physics, 1971.
- Simon Goellner, *Interactive CSS Holographic Card Shaders*, 2022.
- American Bank Note Company, *The History of Credit Card Security Holograms*, 1983.
- W3C, *Web Content Accessibility Guidelines 2.2* (1.4.3, 2.3.1).

---

## 🔗 Cross-Skill Integration & Dialect Relations

- **Sibling Optical Styles:** [ui-style-glassmorphism](../ui-style-glassmorphism/SKILL.md), [ui-style-aurora-mesh-gradient](../ui-style-aurora-mesh-gradient/SKILL.md), [ui-style-gradient-duotone](../ui-style-gradient-duotone/SKILL.md).
- **Surface & 3D Peers:** [ui-style-claymorphism](../ui-style-claymorphism/SKILL.md), [ui-style-3d-immersive-webgl](../ui-style-3d-immersive-webgl/SKILL.md), [ui-style-y2k-revival](../ui-style-y2k-revival/SKILL.md).
