---
name: "ui-style-psychedelic-60s"
description: "Provides the 1960s psychedelic rock poster UI style: melting liquid typography, vibrating complementary optical palettes, kaleidoscopic symmetry, and fluid Art Nouveau revival vectors. Use when designing music festival, creative studio, counterculture or experimental web interfaces."
---

# UI Style: 1960s Psychedelic & Liquid Light

Visual language born in the mid-1960s San Francisco counterculture rock scene (Wes Wilson, Victor Moscoso, Bonnie MacLean, Rick Griffin, Alton Kelley). Defined by organic, melting hand-lettering that fills negative space, kaleidoscopic radial symmetry, vibrating optical color collisions, and liquid light projection textures. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Designing music festival hubs, creative agency portfolios, psychedelic rock/indie band landing pages, and podcast platforms.
- Creating expressive, fluid, and emotive user journeys that break digital rigidity.
- Crafting visual identities celebrating counterculture freedom, retro-nostalgia, and artistic spontaneity.

---

## 🕰️ Definition and Timeline

- **Origins:** Flourished 1965–1970 around the Fillmore Auditorium and Avalon Ballroom in San Francisco. Wes Wilson invented the characteristic "melting" lettering by swelling and squeezing glyphs into bulbous shapes that filled poster frames without margins.
- **Influences:** A radical revival and distortion of [ui-style-art-nouveau-arts-crafts](../ui-style-art-nouveau-arts-crafts/SKILL.md) whiplash curves, combined with Op Art color theory (Josef Albers's simultaneous contrast) and wet-plate liquid light show projections (Brotherhood of Light).
- **Difference from neighbors:** Unlike [ui-style-vaporwave-synthwave](../ui-style-vaporwave-synthwave/SKILL.md), which is digital, 1980s-mall nostalgic, and scanline-heavy, Psychedelic is organic, 1960s analog, hand-drawn, and fluid. Unlike [ui-style-acid-anti-design](../ui-style-acid-anti-design/SKILL.md), which is sharp, deconstructed, and rave-techno, Psychedelic celebrates harmonious natural flow, floral symmetry, and curved warmth.

---

## 🎨 Visual DNA

- **Palette:** High-chroma complementary pairs creating optical vibration: electric purple (`#7209B7`), acid magenta (`#F72585`), sunshine yellow (`#FFD166`), vivid orange (`#FF6B35`), and turquoise green (`#06D6A0`). Deep cosmic plum (`#19052B`) serves as the shadow canvas.
- **Type:** Liquid distorted display fonts (Cooper Black with swollen curves, Alhambra, Dreamland, Wes Wilson-inspired custom display types). High weight, convex swollen stems, and interlocking letterforms.
- **Shapes & Silhouettes:** Undulating contour lines, concentric wave rings, amoeba and teardrop badges, paisley motifs, and bilateral kaleidoscopic mirror layouts.
- **Lighting & Texture:** Soft radial glows, iridescent color bleeds, posterized high-contrast solarized photographic cutouts, and swirling marbling oil textures.
- **Depth:** Luminous layered glows (`box-shadow: 0 0 25px rgba(247, 37, 133, 0.4)`), soft translucent colored card backings, and multi-layered wave contours.

---

## 🖱️ Interaction and Motion

- Liquid morphing: hover interactions cause buttons and card boundaries to pulse gently with fluid bezier curves (`border-radius: 40px 10px 40px 10px` morphing to `10px 40px 10px 40px`).
- Ambient liquid flow: slow, rhythmic background color drift reminiscent of overhead projector oil-and-water light shows (15s to 25s loop).
- Springy physics: buttons scale with elastic overshoot on hover (`transform: scale(1.06) rotate(2deg)`).
- Under `prefers-reduced-motion: reduce`, disable continuous wave animations and fluid morphs, presenting static kaleidoscopic frames with high-contrast clarity.

---

## 🛠️ Implementation Notes

```css
#stage[data-style="psychedelic-60s"] {
  --bg: #19052b;
  --surface: rgba(114, 9, 183, 0.2);
  --fg: #ffd166;
  --accent: #f72585;
  --font-display: 'Cooper Black', 'Cinzel', cursive, sans-serif;
  --font-body: 'Quicksand', sans-serif;
  background: radial-gradient(circle at 50% 50%, #2e0854, #120324);
}

#stage[data-style="psychedelic-60s"] .card {
  background: linear-gradient(135deg, rgba(247, 37, 133, 0.15), rgba(114, 9, 183, 0.25));
  border: 2px solid #f72585;
  border-radius: 36px 12px 36px 12px;
  box-shadow: 0 0 25px rgba(247, 37, 133, 0.35);
  backdrop-filter: blur(8px);
}
```

---

## ♿ Accessibility

- **Optical vibration warning:** Simultaneous contrast between saturated pure red and pure cyan can cause visual strain and nausea. Always buffer text with solid background backings or deep plum drop shadows to guarantee stable reading edges.
- **Typography hierarchy:** Swollen liquid type must be strictly restricted to `h1` and display titles; body copy, form inputs, and system navigation links must use clean, highly legible grotesques with high luminance contrast.
- **Focus visibility:** Provide prominent, non-color-dependent focus rings (e.g. 3px solid white outline with 3px offset) on interactive elements.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** Music festivals, creative audio platforms, cannabis/botanical branding, independent record stores, and artistic culture showcases.
- **Caution:** Commercial e-commerce landing pages (keep shopping bag and checkout flows clean and conventional).
- **Avoid:** Corporate B2B SaaS, enterprise cloud management, healthcare applications, and legal software.

---

## ⚠️ Pitfalls

- Using low-contrast vibrating text for body paragraphs, rendering long-form reading impossible.
- Over-animating the canvas with rapid flashing colors, which can trigger vestibular issues or seizures.
- Flattening the style into a generic rainbow gradient without the characteristic swollen lettering and organic curves.

---

## 📚 Sources

- Paul Grushkin, *The Art of Rock: Posters from Presley to Punk*, Abbeville Press, 1987.
- Walter Medeiros, *San Francisco Rock Posters of the Sixties*, 1976.
- Josef Albers, *Interaction of Color*, Yale University Press, 1963.
- San Francisco Museum of Modern Art, "The Summer of Love Experience: Art, Fashion, and Rock & Roll", 2017.

---

## 🔗 Integration with Other Skills

- Ancestor styles: [ui-style-art-nouveau-arts-crafts](../ui-style-art-nouveau-arts-crafts/SKILL.md).
- Digital descendants: [ui-style-vaporwave-synthwave](../ui-style-vaporwave-synthwave/SKILL.md), [ui-style-acid-anti-design](../ui-style-acid-anti-design/SKILL.md).
- Motion craft: [ui-motion-specialist](../ui-motion-interaction/SKILL.md).
