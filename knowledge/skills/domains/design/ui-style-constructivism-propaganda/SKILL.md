---
name: "ui-style-constructivism-propaganda"
description: "Provides the constructivist and agitprop poster UI style (1919-1930s): aggressive 45-degree diagonal axes, heavy black-and-scarlet geometric primitives, photomontage frames, industrial baseline typography and dynamic structural tension. Use when designing high-impact editorial, cultural manifesto or avant-garde campaign web interfaces."
---

# UI Style: Constructivism & Agitprop Graphic

Graphic radicalism derived from early 20th-century avant-garde constructivism and political poster design (Aleksandr Rodchenko, El Lissitzky, Varvara Stepanova, Gustav Klutsis). Replaces conventional symmetrical grids with engineered dynamic tension, 45-degree diagonal baselines, raw photographic montage, and industrial typography acting as architectural load-bearing structures. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Designing bold editorial features, cultural manifesto pages, exhibition hubs, or statement brand interfaces.
- Replacing conventional symmetrical grids with engineered dynamic tension and industrial rhythm.
- Creating high-contrast activist, publishing, or avant-garde visual campaigns.

---

## 🕰️ Definition and Timeline

- **Lineage:** Born in post-revolutionary Russia (1919–1934) via INKhUK and Vkhutemas. Key foundational works include El Lissitzky's poster *Beat the Whites with the Red Wedge* (1919) and Rodchenko and Mayakovsky's advertising agitations (1923–1925).
- **Philosophical core:** Rejection of "art for art's sake" in favor of utilitarian visual engineering (*konstruktsiya*). The graphic designer acts not as an artist, but as a visual constructor assembling prefabricated industrial elements (lines, geometric solids, press type, and photographs).
- **Difference from neighbors:** Unlike [ui-style-bauhaus](../ui-style-bauhaus/SKILL.md), which emphasizes calm, orthogonal, primary-color functionalism and balanced grids, Constructivism uses aggressive diagonal shear (typically -12° to -45°), asymmetric kinetic thrust, and dominant scarlet-and-black contrast. Unlike [ui-style-neo-brutalism](../ui-style-neo-brutalism/SKILL.md), which is playful, pastel-accented, and Gumroad-inspired, Constructivism is serious, mechanical, and ideological.

---

## 🎨 Visual DNA

- **Palette:** Stark tri-color base: Soviet scarlet red (`#D90429` or `#E63946`), pitch black (`#111111`), and warm aged newsprint cream (`#F4EBD9` or `#EFE6D5`). Accents occasionally incorporate industrial steel gray (`#4A4E69`) or warning ochre (`#E09F3E`).
- **Type:** Heavy condensed grotesques, geometric sans-serif caps, and industrial display faces (Bebas Neue, Anton, Oswald, Archivo Black, Rodchenko-class woodblock grotesques). Headings run along diagonal axes, with dynamic baseline shifts and extreme weight contrast against monospaced caption indices.
- **Shapes & Structural Lines:** Dynamic 45° and 135° diagonal rules, solid triangles, red wedges, circular target concentric bands, heavy black framing bars (4px to 14px), and visible structural rivets.
- **Photomontage:** High-contrast duotone or 1-bit dithered black-and-white photography sliced along sharp geometric angles, with bold scarlet overlays and mechanical framing elements.
- **Depth:** Zero drop shadows or soft gradients. Depth is achieved purely through layered, overlapping geometric cutouts, stark diagonal planes, and hard opaque color blocks.

---

## 🖱️ Interaction and Motion

- Dynamic angular snap: hover states rotate elements back toward horizontal alignment (e.g. from `-2deg` to `0deg`) or thrust outward along a 45-degree vector.
- Mechanical transitions: instantaneous or brisk easing (`0.12s` to `0.18s` linear or `cubic-bezier(0.2, 0, 0, 1)`), avoiding soft organic squashes.
- Scroll choreography: geometric panels slide in along diagonal shear axes rather than simple vertical fades.
- Under `prefers-reduced-motion: reduce`, disable all diagonal baseline shifts and rotational transitions, maintaining fixed, static high-contrast layouts.

---

## 🛠️ Implementation Notes

```css
:root {
  --bg: #f4ebd9;
  --fg: #111111;
  --accent-red: #d90429;
  --font-display: 'Oswald', 'Bebas Neue', sans-serif;
  --font-body: 'Space Grotesk', sans-serif;
}

.constructivist-banner {
  background: var(--bg);
  color: var(--fg);
  border: 4px solid #111111;
  border-left: 14px solid var(--accent-red);
  transform: rotate(-1deg);
}

.diagonal-wedge {
  clip-path: polygon(0 0, 100% 15%, 100% 100%, 0 85%);
  background: var(--accent-red);
  color: #ffffff;
  font-family: var(--font-display);
  text-transform: uppercase;
}
```

- Tailwind idiom: `border-4 border-black border-l-[14px] border-l-red-600 -rotate-1 font-black uppercase`.
- Layout rule: keep micro-typography perfectly aligned and legible, concentrating dynamic diagonal shear on macro containers and display titles.

---

## ♿ Accessibility

- **Contrast compliance:** While scarlet (`#D90429`) against black (`#111111`) fails WCAG AA (ratio ~3.2:1), scarlet against newsprint cream (`#F4EBD9`) easily exceeds 4.8:1, and pure black on cream exceeds 14:1. Never place critical running text in red directly over black.
- **Heading semantics:** Headings rotated via CSS `transform` must remain native HTML heading tags (`<h1>`–`<h6>`) so screen readers parse document outline properly.
- **Cognitive load:** Extreme diagonal tilts can impair reading comprehension for users with cognitive or visual impairments; keep body copy strictly horizontal with generous line-height (`1.6`).

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** Cultural institutions, documentary features, architectural exhibitions, political science journals, indie record releases, and statement manifestos.
- **Caution:** Media platforms requiring high content neutrality; e-commerce checkouts.
- **Avoid:** Corporate banking, healthcare patient portals, SaaS dashboards requiring calm daily use, and long-form technical documentation.

---

## ⚠️ Pitfalls

- Overusing diagonal rotation across every container, turning an intentional avant-garde grid into an illegible, chaotic amusement park.
- Using modern soft rounded corners (`border-radius > 0`), which immediately destroys the sharp industrial rigor of the style.
- Relying on red text for important microcopy without verifying background luminance.

---

## 📚 Sources

- El Lissitzky, *About Two Squares: A Suprematist Tale in 6 Constructions*, 1922.
- Aleksandr Rodchenko, *The Constructivists: The Art of Graphic Design*, 1928.
- Camilla Gray, *The Russian Experiment in Art 1863-1922*, Thames & Hudson, 1986.
- MoMA Exhibition Archives, "Rodchenko and Popova: Defining Constructivism", 2009.

---

## 🔗 Integration with Other Skills

- Sibling historical avant-garde styles: [ui-style-bauhaus](../ui-style-bauhaus/SKILL.md), [ui-style-de-stijl](../ui-style-de-stijl/SKILL.md), [ui-style-swiss-web-minimalism](../ui-style-swiss-web-minimalism/SKILL.md).
- High-contrast relatives: [ui-style-brutalist-monochrome](../ui-style-brutalist-monochrome/SKILL.md), [ui-style-neo-brutalism](../ui-style-neo-brutalism/SKILL.md).
