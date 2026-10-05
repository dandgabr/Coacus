---
name: "ui-style-isometric"
description: "Provides the isometric illustration and UI technique (engineering drawing origins, video games from 1981, web revival 2010s-present): equal-foreshortening 30-degree axes, 2:1 dimetric pixel art, CSS transform and SVG construction, covering geometry, shading, layout, motion and WCAG handling. Use when designing explainer illustrations, product diagrams, isometric dashboards or game-like scenes without needing a WebGL renderer."
---

# UI Style: Isometric

An illustration and UI technique, not a mood: a parallel projection where three axes are equally foreshortened, giving pseudo-3D without perspective. For true real-time 3D scenes use [ui-style-3d-immersive-webgl](../ui-style-3d-immersive-webgl/SKILL.md). Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Explainer diagrams, architecture maps, onboarding illustrations, hero scenes, city or office cutaways.
- Game-like or tactical-RPG interfaces built in 2D art.
- Teams that want depth cues without WebGL cost or complexity.

---

## 🕰️ Definition and Timeline

- Isometric projection: a method for representing 3D objects in 2D in technical and engineering drawings; axonometric, three axes equally foreshortened, 120 degrees between axes; from Greek "equal measure". Derivation: rotate 45 degrees about the vertical axis and about 35.264 degrees about the horizontal (arcsin 1/sqrt 3). Measurements can be taken directly; no perspective, so depth can be ambiguous.
- Video games: most "isometric" games are dimetric with a 2:1 pixel ratio (axes about 26.565 degrees), because 30 degrees gives messy pixel lines. Early titles: Treasure Island (1981), Zaxxon (1982), Q*bert (1982), Ant Attack and Knight Lore (1983); resurgence in indie games and pixel art.
- Distinction from [ui-style-3d-immersive-webgl](../ui-style-3d-immersive-webgl/SKILL.md): this is a flat, authored projection with no camera or lighting engine. Distinction from [ui-style-claymorphism](../ui-style-claymorphism/SKILL.md): claymorphism is soft UI-component depth; isometric is a spatial drawing system. Distinction from [ui-style-bento-grid](../ui-style-bento-grid/SKILL.md): bento is a layout, isometric is a projection.

---

## 🎨 Visual DNA

- **Geometry:** all verticals stay vertical; horizontal edges run at 30 degrees (true) or 26.565 degrees (2:1 pixel); no vanishing points.
- **Shading:** three face tones per object (top lightest, left mid, right darkest) from one fixed light direction.
- **Color:** limited palette of 4-8 hues with tints for faces; flat fills, thin or no outlines.
- **Grid:** objects snap to a diamond tile grid; consistent unit height; shadows as flat skewed shapes.
- **Type:** keep labels flat and upright in HTML, linked to objects by leader lines; do not skew text.

---

## 🖱️ Interaction and Motion

- Hover raises a tile or object along the vertical axis (`translateY(-4px)`), 150-250ms; click expands a callout.
- Depth sorting by z-index (x+y order); animated parts move along axes only, keeping the projection consistent.

---

## 🛠️ Implementation Notes

```css
/* CSS isometric plane: rotate then skew/scale (MDN matrix()/transform functions) */
.iso { transform: rotateX(60deg) rotateZ(-45deg); transform-style: preserve-3d; }
/* Flat 2D alternative */
.iso-2d { transform: rotate(-30deg) skewX(30deg) scaleY(.864); }
.tile:hover { transform: translateY(-4px); transition: transform 200ms ease-out; }
.top { filter: brightness(1.15); } .right { filter: brightness(.8); }
@media (prefers-reduced-motion: reduce) { .tile:hover { transition: none; } }
```

- Author in SVG with a shared symbol set so faces and tiles reuse geometry; MDN documents `matrix()` and related transforms (Baseline widely available since July 2015).
- Prefer pre-drawn SVG or pixel sprites for crispness; use CSS 3D only for simple planes.
- True isometric (30 degrees) for vector art; 2:1 for pixel art.

---

## ♿ Accessibility

- Informative illustrations need text alternatives or an adjacent text description (1.1.1); complex diagrams need a long description or table alternative.
- Do not encode category only by hue or face tone (1.4.1); meet 3:1 for meaningful graphic parts (1.4.11).
- Interactive objects need keyboard access and focus order that matches the visual story, not the z-order (2.1.1, 2.4.3, 2.4.7, 1.3.2); targets at least 24px (2.5.8).
- Tiny labels in dense scenes must still reflow and zoom (1.4.4, 1.4.10); keep labels as real HTML text.
- Honor `prefers-reduced-motion`; no auto-playing scene loops without pause (2.2.2).

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** product explainers, infrastructure and workflow diagrams, game UI, empty-state art, marketing heroes.
- **Caution:** data dashboards (isometric charts distort comparison).
- **Avoid:** precision data reading, dense tables, small-screen primary navigation.

---

## ⚠️ Pitfalls

- Inconsistent angles or light direction between assets; mixing 30-degree and 2:1 art.
- Skewing text; hiding meaning in scene details with no text equivalent.
- Using CSS 3D for large scenes, causing blur and performance cost.
- Isometric charts: the projection hides true bar heights and misleads.

---

## 📚 Sources

- Wikipedia contributors, "Isometric projection" (Wikipedia), accessed 2026-10-05 — https://en.wikipedia.org/wiki/Isometric_projection
- Wikipedia contributors, "Isometric video game graphics" (Wikipedia), accessed 2026-10-05 — https://en.wikipedia.org/wiki/Isometric_video_game_graphics
- MDN Web Docs, "matrix()" CSS transform function (Mozilla), accessed 2026-10-05 — https://developer.mozilla.org/en-US/docs/Web/CSS/transform-function/matrix
- W3C, "Web Content Accessibility Guidelines (WCAG) 2.2" (W3C Recommendation), 12 Dec 2024 — https://www.w3.org/TR/WCAG22/
- The CSS rotate/skew/scale recipes above are author suggestions to be verified in a browser; not taken from a cited page.

---

## 🔗 Integration with Other Skills

- For conformance discipline, see [web-accessibility-wcag](../../../engineering/practices/web-accessibility-wcag/SKILL.md).
- Neighbors: [ui-style-3d-immersive-webgl](../ui-style-3d-immersive-webgl/SKILL.md), [ui-style-retro-computing-pixel](../ui-style-retro-computing-pixel/SKILL.md), [ui-style-claymorphism](../ui-style-claymorphism/SKILL.md), [ui-style-bento-grid](../ui-style-bento-grid/SKILL.md), [ui-style-flat-design](../ui-style-flat-design/SKILL.md).
