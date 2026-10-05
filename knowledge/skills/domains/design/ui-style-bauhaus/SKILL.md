---
name: "ui-style-bauhaus"
description: "Provides the Bauhaus UI style (1919-1933 lineage, revived for the web): form follows function, circle-square-triangle geometry, primary color with black, geometric sans typography and functional asymmetric layout, covering the school's timeline, tokens, grid and type rules, and how it differs from De Stijl and Swiss style. Use when designing geometric, educational, cultural or design-led brands that want modernist clarity with warmth."
---

# UI Style: Bauhaus

Modernist design from the German school (1919-1933): unify craft, art and industrial production; function over ornament; basic geometry; asymmetry with purposeful hierarchy. On screens it appears as bold shapes, primary accents and lowercase geometric type. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Designing for museums, schools, design studios, architecture or product brands that want geometric modernism.
- Building posters, landing pages and dashboards from circle, square and triangle primitives.
- Needing to separate Bauhaus from De Stijl and Swiss minimalism in an art-direction brief.

---

## 🕰️ Definition and Timeline

- Walter Gropius founded the Staatliches Bauhaus in Weimar on April 1, 1919; moved to Dessau (1925-1932) and Berlin (1932-1933); closed under Nazi pressure in 1933. Directors: Gropius, Hannes Meyer (1928-1930), Mies van der Rohe (1930-1933).
- Faculty included Klee, Kandinsky, Moholy-Nagy, Gunta Stolzl; Herbert Bayer led printing and advertising and drew the "Universal" lowercase sans proposal (1925-1930, never cast in metal).
- **Differences:** [ui-style-de-stijl](../ui-style-de-stijl/SKILL.md) restricts itself to orthogonal lines and flat planes in a rigorous neoplastic grid; Bauhaus embraces circles, triangles, diagonals and photomontage. [ui-style-swiss-web-minimalism](../ui-style-swiss-web-minimalism/SKILL.md) is postwar and grid-and-type driven, with little shape play. Bauhaus is a design-education philosophy first, a look second.

---

## 🎨 Visual DNA

- **Shapes:** circle, square, triangle as the base alphabet; overlapping, cropped and rotated for composition; diagonals allowed for energy.
- **Color:** primaries (red `#D62718`-ish, yellow `#F4B400`-ish, blue `#1D4E9E`-ish), black, white and warm paper tones; flat fills only, no gradients.
- **Type:** geometric sans (Futura, Jost, Josefin Sans, Poppins as a stand-in), lowercase headlines as a nod to Bayer, heavy weight contrast, text set in blocks and rotated vertical lines.
- **Layout:** asymmetry with strong alignment axes, thick rules, oversized numerals, photomontage with high-contrast cutouts.
- **Depth:** flat or stepped overlap; shadows avoided or hard-edged.

---

## 🖱️ Interaction and Motion

- Functional motion: shapes slide, rotate 90 degrees or scale in straight, mechanical easing (`ease-in-out`, 200-300ms).
- Hover swaps fills between primaries or rotates a shape quarter-turn; avoid blur and glow.
- Scroll compositions can reveal geometry in sequence; keep everything interruptible.

---

## 🛠️ Implementation Notes

```css
:root {
  --paper: #f3ede0; --ink: #111; --red: #d62718; --yellow: #f4b400; --blue: #1d4e9e;
}
body { background: var(--paper); color: var(--ink); font-family: "Jost", "Futura", sans-serif; }
h1 { font-weight: 800; text-transform: lowercase; letter-spacing: -.02em; }
.shape-circle { aspect-ratio: 1; border-radius: 50%; background: var(--red); }
.shape-tri { aspect-ratio: 1; background: var(--blue); clip-path: polygon(50% 0, 100% 100%, 0 100%); }
.btn { background: var(--ink); color: var(--paper); border: 0; padding: .75rem 1.25rem; }
.btn:hover { background: var(--red); transition: background .2s ease-in-out; }
.btn:focus-visible { outline: 3px solid var(--blue); outline-offset: 3px; }
```

- Compose on CSS Grid with explicit asymmetric tracks (e.g. `2fr 1fr 3fr`); let one shape bleed over a grid line.
- Decorative shapes are `aria-hidden` or CSS backgrounds; keep content order logical regardless of visual placement.

---

## ♿ Accessibility

- Yellow and red on paper often fail 4.5:1 for text (1.4.3): use black or white text on color fields after testing; use color fills as non-text elements needing 3:1 (1.4.11).
- Lowercase-only and rotated text harm readability and screen magnification: keep body copy in normal case, horizontal; reflow at 320px (1.4.10) and allow text spacing overrides (1.4.12).
- Meaning conveyed by shape or color alone fails 1.4.1; add labels or icons.
- Reading order must follow DOM order despite asymmetric visual layout (1.3.2); honor `prefers-reduced-motion`.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** cultural institutions, education, design and architecture studios, posters, product launches with a modernist angle.
- **Caution:** data-dense dashboards (use as accent system), e-commerce (brand pages only).
- **Avoid:** brands needing warmth through texture and handcraft, or high-ornament luxury (see Art Deco).

---

## ⚠️ Pitfalls

- "Bauhaus" used as a label for any primary-color-and-shapes page; without functional rationale it is pastiche.
- Using ITC Bauhaus display type (a 1970s commercial face, not a school typeface) as shorthand.
- Confusing with De Stijl (orthogonal only) or Swiss (no shapes).
- Cutout photomontage with unlicensed imagery.

---

## 📚 Sources

- Wikipedia, "Bauhaus" (Wikimedia Foundation), accessed 2026 — https://en.wikipedia.org/wiki/Bauhaus
- Wikipedia, "Herbert Bayer" (Wikimedia Foundation), accessed 2026 — https://en.wikipedia.org/wiki/Herbert_Bayer
- Tate, "De Stijl" (Tate), accessed 2026, used for the contrast with De Stijl — https://www.tate.org.uk/art/art-terms/d/de-stijl
- W3C, "Web Content Accessibility Guidelines (WCAG) 2.2" (W3C), 2023 — https://www.w3.org/TR/WCAG22/
- MDN, "prefers-reduced-motion" (Mozilla), accessed 2026 — https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
- Hex values and the Jost/Futura type mapping are practice suggestions, not from a cited source: `unverified`.

---

## 🔗 Integration with Other Skills

- For conformance discipline, see [web-accessibility-wcag](../../../engineering/practices/web-accessibility-wcag/SKILL.md).
- Sibling styles: [ui-style-de-stijl](../ui-style-de-stijl/SKILL.md), [ui-style-swiss-web-minimalism](../ui-style-swiss-web-minimalism/SKILL.md), [ui-style-flat-design](../ui-style-flat-design/SKILL.md), [ui-style-memphis](../ui-style-memphis/SKILL.md), [ui-style-mid-century-modern](../ui-style-mid-century-modern/SKILL.md).
