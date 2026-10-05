---
name: "ui-style-hand-drawn-sketch"
description: "Provides the hand-drawn / sketch UI style (2010s-present): wobbly strokes, hachure fills, doodle icons and marker typography that signal drafts and humanity, covering Rough.js, SVG filter wobble, stroke-dash techniques, tool precedents like Excalidraw and legibility limits. Use when designing whiteboard-like tools, playful brand surfaces or low-fidelity-feeling interfaces."
---

# UI Style: Hand-Drawn Sketch

Interfaces that look drawn by a person: imperfect lines, scribbled fills, doodled icons and handwriting-like type. The roughness signals "work in progress" and warmth, which lowers perceived commitment and invites feedback. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Diagramming, whiteboard, brainstorming or wireframing tools where a rough look invites iteration.
- Playful brand, education or children's surfaces needing personality over polish.
- Illustration-led landing pages with doodle accents and annotations.

---

## 🕰️ Definition and Timeline

- Rough.js, created by Preet Shihn (MIT licence), renders shapes with a sketchy look on Canvas and SVG, with `roughness`, `bowing` and fill styles (hachure, cross-hatch, zigzag, dots, solid).
- Rough.js powers Excalidraw (a whiteboard app) and Diagrams.net's sketch mode; this normalized the look in developer tooling.
- Low-fidelity sketch styling is a long-standing wireframing practice (Balsamiq-style mockups; `unverified` dates not cited here).
- Distinct from [ui-style-flat-design](../ui-style-flat-design/SKILL.md): lines are intentionally irregular. Distinct from [ui-style-collage-scrapbook](../ui-style-collage-scrapbook/SKILL.md): one pen-like voice, not mixed cut-out media.

---

## 🎨 Visual DNA

- **Lines:** slightly wobbly, double-stroked, overshooting corners; round caps; 2-3px weight.
- **Fills:** hachure, cross-hatch, scribble or flat marker blocks that do not fully reach the outline.
- **Color:** pencil gray or ink on paper tones (off-white, kraft), with one or two highlighter accents.
- **Type:** handwriting or marker faces for headings (Caveat, Patrick Hand, Gochi Hand: `unverified` as exemplars); a plain sans for body.
- **Ornament:** arrows, underlines, circled words, margin annotations, tape and stars.

---

## 🖱️ Interaction and Motion

- "Draw-on" reveals: animate `stroke-dashoffset` so an outline traces itself (400-900ms), once on entry.
- Hover: slight rotation (1-2 degrees) or re-roughening with a new seed, 120-200ms.
- Avoid constant jitter; if a boil effect is used, step it at 6-8 fps on a single decorative element.
- Under `prefers-reduced-motion: reduce`, render final strokes immediately and stop all jitter.

---

## 🛠️ Implementation Notes

```html
<svg width="0" height="0" aria-hidden="true" focusable="false">
  <filter id="wobble">
    <feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="2" seed="3" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="3" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
</svg>
```

```css
.sketch { border: 2px solid #222; border-radius: 255px 15px 225px 15px / 15px 225px 15px 255px; }
.sketch-line { filter: url(#wobble); }
.draw path { stroke-dasharray: var(--len); stroke-dashoffset: var(--len); animation: draw .8s ease-out forwards; }
@keyframes draw { to { stroke-dashoffset: 0; } }
@media (prefers-reduced-motion: reduce) { .draw path { animation: none; stroke-dashoffset: 0; } }
```

- Apply wobble filters to decorative borders and icons, never to body text.
- Use Rough.js for generated diagrams; seed it for stable output across renders.
- Keep the control's real hit area and a solid focus outline independent of the rough decoration.

---

## ♿ Accessibility

- 1.4.3 Contrast (Minimum): thin, light pencil gray on cream often fails; hold text at 4.5:1 and strokes at 3:1 (1.4.11 Non-text Contrast).
- 1.4.12 Text Spacing and 1.4.4 Resize Text: handwriting fonts degrade at small sizes and with dyslexia; limit them to short headings.
- 2.4.7 Focus Visible and 2.4.11 Focus Not Obscured: use a crisp solid outline, not a wobbly one.
- 2.5.8 Target Size (Minimum): sketchy boundaries must not shrink actual clickable areas below 24px.
- SVG doodles: decorative ones get `aria-hidden="true"`; meaningful diagrams need text alternatives.
- Honor `prefers-reduced-motion` for draw-on and boil animations.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** whiteboards, brainstorming, education, indie products, creative portfolios, onboarding illustrations.
- **Caution:** SaaS marketing (accent doodles only), long-form text pages.
- **Avoid:** banking, legal, medical or enterprise surfaces where polish signals trust; dense data UIs.

---

## ⚠️ Pitfalls

- Roughness applied to everything reads as noise; keep body text and form chrome clean.
- Handwriting fonts for paragraphs hurt readability and localization coverage.
- Random jitter per render changes layout screenshots and causes visual regression noise; seed it.
- Fake-sketch icon packs mixed with crisp UI produce an inconsistent voice.
- Filter-heavy SVG on many elements costs paint time on mobile.

---

## 📚 Sources

- Preet Shihn, "Rough.js" — https://roughjs.com/
- MDN Web Docs, "<feTurbulence> SVG filter primitive" (Mozilla) — https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/feTurbulence
- MDN Web Docs, "prefers-reduced-motion" (Mozilla) — https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
- W3C, "Web Content Accessibility Guidelines (WCAG) 2.2", Recommendation 12 Dec 2024 — https://www.w3.org/TR/WCAG22/
- Excalidraw, GitHub README (MIT license) — https://github.com/excalidraw/excalidraw ("open source virtual hand-drawn style whiteboard")
- Preet Shihn, "Rough.js" — https://roughjs.com/ (sketchy hand-drawn-style graphics for Canvas and SVG; lists Excalidraw and Diagrams.net among users)

---

## 🔗 Integration with Other Skills

- For conformance discipline, see [web-accessibility-wcag](../../../engineering/practices/web-accessibility-wcag/SKILL.md).
- Sibling styles: [ui-style-collage-scrapbook](../ui-style-collage-scrapbook/SKILL.md), [ui-style-organic-biophilic](../ui-style-organic-biophilic/SKILL.md), [ui-style-flat-design](../ui-style-flat-design/SKILL.md), [ui-style-micro-interactions](../ui-style-micro-interactions/SKILL.md), [ui-style-risograph-zine](../ui-style-risograph-zine/SKILL.md).
