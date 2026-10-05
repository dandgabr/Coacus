---
name: "ui-style-glassmorphism"
description: "Provides the complete glassmorphism and visionOS spatial computing UI style (2020-present): frosted translucent panels with backdrop blur, hairline specular borders, 3D z-axis elevation, gaze/hover illumination and depth refraction. Covers OS lineage from Windows Aero and iOS 7 to macOS Big Sur and Apple visionOS, backdrop-root pitfalls and contrast strategy. Use when designing overlays, spatial web, XR dashboards or next-generation glassmorphic interfaces."
---

# UI Style: Glassmorphism & VisionOS Spatial Elevation

Frosted translucent glass surfaces — translucent panels blurring content beneath them, edge-lit with hairline specular highlights, and elevated into three-dimensional spatial computing. Named by Michał Malewicz (December 2020), institutionalized by macOS Big Sur and Windows 11 Mica, and elevated to true spatial computing by Apple visionOS (2024). Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Spatial web applications, WebXR experiences, floating modal overlays, audio/video players, and navigation bars.
- High-end productivity suites, modern dashboard cards, and luxury hardware interfaces.
- Upgrading flat 2D glassmorphic mockups into physically plausible, specular-lit optical materials.

---

## 🕰️ Definition and Timeline

- **2D Web Glassmorphism (2020–2022):** Lineage traces to Windows Vista/7 Aero Glass (2006) and iOS 7 translucency (2013). Named by Michał Malewicz in December 2020, accelerated by macOS Big Sur (Nov 2020) and Alexander Plyuto's Dribbble concepts.
- **VisionOS Spatial Computing Strand (2023–present):** Unveiled by Apple at WWDC 2023 and shipped commercially in 2024. In spatial computing, interfaces exist within real physical rooms: opaque slabs feel claustrophobic, while unlit sheets lack legibility. VisionOS solves this via multi-pass Gaussian blur combined with dynamic specular edge lighting and eye/cursor hover flares.
- **Difference from neighbors:** Unlike [ui-style-neumorphism](../ui-style-neumorphism/SKILL.md), which is opaque and sculpted from the background plane, Glassmorphism is transparent, optical, and reveals the layered depths below.

---

## 🎨 Visual DNA

- **Surfaces & Opacity:** 10%–20% translucent white or obsidian layers (`rgba(255, 255, 255, 0.12)`) over rich ambient gradient blobs (`#0E1017` to `#202738`).
- **Depth & Multi-Pass Blur:** `backdrop-filter: blur(24px) saturate(180%)` to `blur(40px)`, combined with soft ambient drop shadows (`0 20px 40px rgba(0, 0, 0, 0.35)`).
- **Specular Edge Highlights:** Calibrated 1px border where the top edge is brighter (`rgba(255, 255, 255, 0.45)`), simulating environmental ceiling light reflection, while side and bottom borders fade to `rgba(255, 255, 255, 0.12)`.
- **Shapes:** Generously rounded corners (`border-radius: 20px` to `32px` on cards, pill `9999px` on buttons).
- **Typography:** Ultra-crisp modern grotesques (SF Pro, Inter, Plus Jakarta Sans) paired with subtle text drop shadows for legibility over variable backgrounds.

---

## 🖱️ Interaction and Motion

- **Gaze & Hover Flare:** Hovering a glass card raises its z-axis elevation (`transform: translateY(-3px) scale(1.01)`) and intensifies its top specular highlight.
- **Spring-Loaded Physics:** Transitions employ Apple-style fluid damping curves (`cubic-bezier(0.25, 1, 0.5, 1)` over 300ms).
- Keep blur static during animations: animating `backdrop-filter` radius causes severe GPU frame drops.
- Under `prefers-reduced-motion: reduce`, disable all z-axis scaling and specular cursor tracking, maintaining static translucent panels.

---

## 🛠️ Implementation Notes

```css
:root {
  --glass-bg: #0e1017;
  --glass-surface: rgba(255, 255, 255, 0.10);
  --glass-border: rgba(255, 255, 255, 0.20);
  --glass-top-light: rgba(255, 255, 255, 0.45);
}
body {
  background: radial-gradient(circle at 50% 20%, #202738, #0e1017);
  color: #f5f5f7;
  font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif;
}
.glass-panel {
  background: var(--glass-surface);
  backdrop-filter: blur(30px) saturate(180%);
  -webkit-backdrop-filter: blur(30px) saturate(180%);
  border: 1px solid var(--glass-border);
  border-top-color: var(--glass-top-light);
  border-radius: 24px;
  box-shadow: 0 16px 36px rgba(0, 0, 0, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.3);
  transition: transform 0.3s cubic-bezier(0.25, 1, 0.5, 1), box-shadow 0.3s ease;
}
.glass-panel:hover {
  transform: translateY(-3px);
  box-shadow: 0 24px 48px rgba(0, 0, 0, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.5);
}
@media (prefers-reduced-motion: reduce) {
  .glass-panel { transition: none; }
}
```

- **Backdrop-Root Bug:** Any ancestor with `filter`, `opacity < 1`, `mask`, or `mix-blend-mode` creates a new stacking context that stops backdrop blur on child elements.
- Always provide an opaque solid fallback (`#141721`) for browsers without `backdrop-filter` support.

---

## ♿ Accessibility

- **Variable Contrast Hazard:** Text contrast over glass varies depending on what scrolls underneath. Never place small body copy over unpredictable backgrounds; increase glass surface opacity under text containers to guarantee WCAG 1.4.3 (4.5:1 ratio).
- **Focus Indicators:** Specular edge glints do not qualify as accessible focus indicators. Interactive elements must display a distinct 2px or 3px solid focus ring with high contrast (WCAG 2.4.7).
- **Reduced Transparency:** Respect `prefers-reduced-transparency` by falling back to solid background panels.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** Floating navigation bars, modal dialogs, audio/video players, WebXR portals, and luxury tech showcase heroes.
- **Avoid:** Dense data spreadsheets, high-contrast reading apps, and government document filings.

---

## 📚 Sources

- Apple Inc., "Principles of Spatial Design", WWDC 2023 Session 10072.
- Apple Inc., "Design for visionOS: Human Interface Guidelines", 2024.
- Michał Malewicz, "Glassmorphism in User Interfaces", *Hype4*, 2020.
- Microsoft Learn, "Mica material for Windows apps", 2021.
- W3C, *Web Content Accessibility Guidelines 2.2* (1.4.3, 2.4.7) — https://www.w3.org/TR/WCAG22/

---

## 🔗 Integration with Other Skills

- Sibling depth styles: [ui-style-neumorphism](../ui-style-neumorphism/SKILL.md), [ui-style-claymorphism](../ui-style-claymorphism/SKILL.md), [ui-style-aurora-mesh-gradient](../ui-style-aurora-mesh-gradient/SKILL.md).
