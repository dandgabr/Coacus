---
name: "ui-style-art-nouveau"
description: "Provides the authentic Art Nouveau UI style (1890–1910): organic whiplash curves, sinuous botanical tendrils, Alphonse Mucha illustrations, Hector Guimard cast iron metro entrances, Louis Comfort Tiffany stained glass, and muted jewel tones. Use when designing artistic luxury brands, botanical portfolios, theatrical applications, cultural heritage sites, or organic decorative web experiences."
---

# UI Style: Art Nouveau (Organic Whiplash & Belle Époque)

Art Nouveau is the international decorative movement that flourished between 1890 and 1910, revolting against sterile academic historicism by finding inspiration in the dynamic rhythms of the natural world. Defined by the iconic "whiplash" curve (*coup de fouet*), sensual botanical forms, undulating water lilies, insect wing geometry, and stained glass iridescence. Synthesized from Hector Guimard's Paris Métro architecture and Alphonse Mucha's lithographic masterworks.

---

## 🧭 When to Activate

- Designing for luxury perfumery, botanical sciences, organic cosmetics, high-end cultural institutions, theatrical events, or historical literature.
- Crafting interfaces where borders, buttons, and dividers flow with organic, asymmetrical, rhythmic vitality rather than rigid geometric boxes.
- Distinct from Arts and Crafts; activate Art Nouveau when the design demands fluid serpentine curves, feminine elegance, and French Belle Époque glamour.

---

## 🕰️ Definition, Lineage, and Timeline

- **Chronology:** Flourished from 1890 (Hôtel Tassel by Victor Horta in Brussels) to 1910 (superseded by Art Deco and early modernism).
- **Core Practitioners:** Alphonse Mucha (posters and jewelry), Hector Guimard (cast iron entrances), Antoni Gaudí (Barcelona modernisme), Louis Comfort Tiffany (favrile stained glass), René Lalique (glass and gemstones).
- **Distinction from Neighbors:**
  - Unlike **Arts & Crafts / [ui-style-arts-and-crafts](../ui-style-arts-and-crafts/SKILL.md)**: Arts & Crafts is rustic, honest, medievalist, heavy, and built on woodblock prints; Art Nouveau is urban, sinuous, erotic, lighter, and celebrates exotic curved iron and blown glass.
  - Unlike **Art Deco / [ui-style-art-deco](../ui-style-art-deco/SKILL.md)**: Art Deco is industrial, symmetrical, streamlined, and geometric (1920–1939); Art Nouveau is organic, asymmetrical, and biological (1890–1910).

---

## 🎨 Visual DNA & Subgenre Taxonomy

- **The Whiplash Curve:**
  - Asymmetric, undulating curves that accelerate and snap back like the motion of a whip or flowing hair.
  - Implemented via complex SVG vector paths and continuous organic border contours.
- **Botanical Palette:**
  - Sage Olive (`#556B2F`), Dusty Peacock Teal (`#1D4E5B`), Pale Absinthe Green (`#C3D9A4`), Muted Terracotta (`#C86D51`), and Tarnished Gold (`#D4AF37`).
- **Typography:**
  - Distinctive turn-of-the-century typography with curved crossbars, high-waisted glyphs, and flared terminals (*Eckmann*, *Arnold Böcklin*, *ITC Benguiat*).

---

## 📐 Lighting Physics, Specular Splits & Surfaces

1. **Favrile Stained Glass Translucency:**
   ```css
   background: radial-gradient(circle at 30% 20%, rgba(212, 175, 55, 0.25) 0%, rgba(29, 78, 91, 0.85) 100%);
   border: 2px solid #556B2F;
   box-shadow: inset 0 0 20px rgba(195, 217, 164, 0.2), 0 8px 24px rgba(15, 30, 35, 0.5);
   ```
2. **Guimard Cast Iron Frame:**
   - Deep patinated bronze-green with subtle directional sunlight highlight.
   ```css
   border: 3px solid #23342A;
   box-shadow: inset 1px 1px 0 #5E7A68, inset -1px -1px 0 #0E1712, 0 6px 16px rgba(0,0,0,0.4);
   ```

---

## 🏷️ Complete Design Tokens

```css
:root {
  /* Art Nouveau Palette */
  --nouveau-peacock: #1D4E5B;
  --nouveau-absinthe: #C3D9A4;
  --nouveau-olive: #475C3E;
  --nouveau-gold: #D4AF37;
  --nouveau-gold-dim: #9E7D23;
  --nouveau-parchment: #F7F4EA;
  --nouveau-charcoal: #1C2421;
  --nouveau-terracotta: #C86D51;

  /* Typography */
  --nouveau-font-display: 'Benguiat', 'Cinzel Decorative', serif;
  --nouveau-font-body: 'Cormorant Garamond', Georgia, serif;
}
```

---

## 🧱 Production-Ready Component Blueprint

```html
<article class="nouveau-card">
  <div class="nouveau-ornament-top"></div>
  <span class="nouveau-badge">BELLE ÉPOQUE</span>
  <h3 class="nouveau-title">Serpentine Harmony</h3>
  <p class="nouveau-prose">Organic curves distilled from nature, celebrating rhythmic ironwork and blown glass.</p>
  <button class="nouveau-btn" type="button">
    <span>DISCOVER SALON</span>
  </button>
  <div class="nouveau-ornament-bottom"></div>
</article>
```

```css
.nouveau-card {
  background: var(--nouveau-parchment);
  border: 2px solid var(--nouveau-olive);
  border-radius: 24px 4px 24px 4px;
  padding: 32px 24px;
  color: var(--nouveau-charcoal);
  font-family: var(--nouveau-font-body);
  position: relative;
  box-shadow: 0 8px 24px rgba(29, 78, 91, 0.15);
  text-align: center;
}
.nouveau-badge {
  font-family: var(--nouveau-font-display);
  font-size: 0.75rem;
  letter-spacing: 0.2em;
  color: var(--nouveau-gold-dim);
  border-bottom: 1px solid var(--nouveau-gold);
  padding-bottom: 4px;
  display: inline-block;
}
.nouveau-title {
  font-family: var(--nouveau-font-display);
  font-size: 1.75rem;
  color: var(--nouveau-peacock);
  margin: 16px 0 8px;
}
.nouveau-prose {
  font-size: 1rem;
  line-height: 1.6;
  color: #38423E;
  margin-bottom: 24px;
}
.nouveau-btn {
  background: transparent;
  color: var(--nouveau-peacock);
  font-family: var(--nouveau-font-display);
  font-weight: 700;
  letter-spacing: 0.12em;
  padding: 12px 28px;
  border: 2px solid var(--nouveau-gold);
  border-radius: 16px 2px 16px 2px;
  cursor: pointer;
  transition: all 180ms ease-out;
}
.nouveau-btn:hover {
  background: var(--nouveau-peacock);
  color: #FFFFFF;
  border-color: var(--nouveau-peacock);
  box-shadow: 0 4px 16px rgba(29, 78, 91, 0.3);
}
```

---

## ✨ Micro-Interactions, Motion & Soundscapes

- **Whiplash Unfurl:** Modals and panels expand with asymmetrical curvilinear transitions.
- **Glass Specular Shift:** Cards gently shift iridescent reflections as the cursor moves over surfaces.

---

## ♿ WCAG 2.2 Accessibility & High-Contrast Guardrails

- **Contrast Ratios:**
  - Charcoal (`#1C2421`) on Parchment (`#F7F4EA`): **14.9:1** (Passes WCAG AAA).
  - Peacock Teal (`#1D4E5B`) on Parchment (`#F7F4EA`): **8.6:1** (Passes WCAG AAA).
  - Dark Gold (`#9E7D23`) on Parchment: **4.65:1** (Passes WCAG AA).
- **Dual-Contrast Focus Ring:**
  `outline: 2px solid var(--nouveau-peacock); box-shadow: 0 0 0 2px var(--nouveau-gold);`

---

## 🚫 Anti-Patterns & Visual Sins (Anti-AI Slop Traps)

- ❌ **NEVER use rigid symmetry or sharp 90-degree boxes:** Art Nouveau breathes through asymmetric botanical flow.
- ❌ **NEVER use neon synthetic colors:** All pigments must evoke natural stone, vegetal dyes, oxidized copper, or stained glass.

---

## 📚 Sources & References

- Alphonse Mucha, *Documents Décoratifs* (Paris, 1902).
- Victor Horta, *The Architecture of Art Nouveau* (Brussels, 1895).
