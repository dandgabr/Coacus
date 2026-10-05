---
name: "ui-style-claymorphism"
description: "Provides the claymorphism and plasticine stop-motion UI style (2021-present): inflated 3D pastel shapes with dual inner shadows, handmade tactile fingerprint textures, stepped frame-rate animations, organic rounded contours and cozy warmth. Use when designing playful inflated UI, education apps, creative craft brands or clay-style marketing assets."
---

# UI Style: Claymorphism & Plasticine Stop-Motion

Puffy, tactile 3D UI — inflated shapes with curvature beyond plain rounded corners, dual inner shadows simulating soft clay, and artisanal plasticine textures with stepped stop-motion animation. Bridges digital 3D clay modeling (Michał Malewicz, 2021) and cinematic stop-motion animation (Aardman Animations, Will Vinton). Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Kid and family products, creative education platforms, animation studios, craft marketplaces, indie games, and whimsical brand portfolios.
- Radiating physical human warmth, approachable friendliness, and tactile comfort.
- Integrating 3D clay renders (Spline-class) or CSS-modeled plasticine volumes into web layouts.

---

## 🕰️ Definition and Timeline

- **Digital Claymorphism:** Named and defined by Michał Malewicz in 2021 (Hype4). Sparked by the 3D web tooling surge (Spline, Pitch's 3D key visuals) and illustrated avatar packs (Amrit Pal Singh's *Toy Faces*, Sam Briskar's *Avatarz*). Peaked in 2021–2022; evolved into soft elevation design systems.
- **Cinematic Stop-Motion Lineage:** Traced to Will Vinton (*Claymation*, 1974) and Nick Park (*Wallace & Gromit*, 1989). In digital interfaces, this strand introduces intentional human imperfections: subtle thumbprints, clay seams, matte earth pigments, and stepped 12fps animations.
- **Difference from neighbors:** Unlike [ui-style-neumorphism](../ui-style-neumorphism/SKILL.md), where elements extrude seamlessly from the background plane, Claymorphism floats on top of the canvas with high elevation, colorful inner highlights, and vibrant candy pastels.

---

## 🎨 Visual DNA

- **Shapes:** Generously inflated contours with corner rounding exceeding 50% (`border-radius: 32px` to `48px`, or pill `9999px`), with edge midpoints bowed outward like pressed dough.
- **Color:** Soft pastel bases (mint, cream `#FDFAF6`, marshmallow pink, baby blue) complemented by earthy plasticine accents (terracotta `#E76F51`, mustard `#E9C46A`, pine `#2A9D8F`).
- **Depth & Lighting:** Two opposing inner shadows create the dome volume (a light highlight at top-left, a darker tinted shade at bottom-right), anchored by a deep, soft ambient drop shadow.
- **Surface Texture:** Matte clay feel, subtle organic thumbprint contours, and soft inner bevels.
- **Typography:** Chunky, warm, friendly display typefaces (Baloo 2, Nunito, Quicksand) paired with clean geometric sans body text.

---

## 🖱️ Interaction and Motion

- **Squishy Affordance:** Buttons compress organically when pressed (`transform: scale(0.96)` with inner shadow contraction), giving an elastic, squishy feedback.
- **Stepped Stop-Motion Option:** Animation curves can adopt stepped keyframes (`animation-timing-function: steps(5)` at 10–12 fps) for playful stop-motion wiggles and artisanal charm.
- Under `prefers-reduced-motion: reduce`, disable all stepped wiggles and springy bounces, using subtle opacity transitions instead.

---

## 🛠️ Implementation Notes

```css
.clay {
  background: #fdfaf6;
  border-radius: 36px;
  box-shadow: 
    0 16px 32px rgba(61, 43, 31, 0.12),
    inset -6px -6px 12px rgba(61, 43, 31, 0.15),
    inset 6px 6px 16px #ffffff;
  transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.2s ease;
}
.clay:hover {
  transform: translateY(-4px) scale(1.01);
  box-shadow: 
    0 22px 40px rgba(61, 43, 31, 0.16),
    inset -6px -6px 12px rgba(61, 43, 31, 0.15),
    inset 6px 6px 18px #ffffff;
}
.clay:active {
  transform: translateY(2px) scale(0.97);
  box-shadow: 
    0 8px 16px rgba(61, 43, 31, 0.10),
    inset -8px -8px 16px rgba(61, 43, 31, 0.20),
    inset 4px 4px 10px #ffffff;
}
@media (prefers-reduced-motion: reduce) {
  .clay { transition: none; }
}
```

- The signature combination consists of a tinted outer shadow + opposing light/dark inner shadows.
- For bowed curved edges, pair CSS with SVG shape masks or 3D Spline assets.
- In dark themes, avoid pure black backgrounds so the inner clay shadows remain distinctly visible.

---

## ♿ Accessibility

- **Contrast Safety:** Pastel-on-pastel repeats the neumorphic contrast trap. Always use dark chocolate ink (`#3D2B1F`) or high-contrast white text exceeding WCAG 1.4.3 (4.5:1 ratio).
- **Control Boundaries:** Soft clay shadows alone may be insufficient for low-vision users; reinforce interactive boundaries with a crisp 1.5px semi-transparent outline or distinct color contrast (WCAG 1.4.11).
- **Motion Restraint:** Stepped frame animations and bouncy springs can trigger vestibular discomfort; strictly honor `prefers-reduced-motion: reduce`.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** Early childhood education, wellness onboarding, gamified productivity tools, creative studio showcases, and artisanal craft marketplaces.
- **Avoid:** High-density enterprise dashboards, regulatory compliance platforms, legal contracts, and financial trading terminals where whimsical volumes reduce information throughput.

---

## ⚠️ Pitfalls

- Overusing 3D inflated styles on every tiny UI element, causing severe visual clutter and reducing scan speed.
- Relying exclusively on white inner highlights on pale backgrounds, which disappear on low-contrast screens.
- Inflated asset weight: optimize 3D Spline scenes and WebP textures to prevent page load regressions.

---

## 📚 Sources

- Michał Malewicz, "Claymorphism in User Interfaces", *Hype4*, 2021 — https://hype4.academy/articles/design/claymorphism-in-user-interfaces
- Nick Park, *The Making of Wallace & Gromit*, Pavilion Books, 1997.
- Will Vinton, *Claymation: The Art of Dimensional Animation*, 1980.
- W3C, *Web Content Accessibility Guidelines 2.2* (1.4.3, 1.4.11, 2.3.3) — https://www.w3.org/TR/WCAG22/

---

## 🔗 Integration with Other Skills

- Sibling tactile and 3D styles: [ui-style-neumorphism](../ui-style-neumorphism/SKILL.md), [ui-style-glassmorphism](../ui-style-glassmorphism/SKILL.md), [ui-style-hand-drawn-sketch](../ui-style-hand-drawn-sketch/SKILL.md).
- 3D asset engineering: [ui-style-3d-immersive-webgl](../ui-style-3d-immersive-webgl/SKILL.md).
