---
name: "ui-style-spatial-vision-os"
description: "Provides the visionOS and spatial computing UI style: multi-layered glass elevation, dynamic specular edge reflections, deep material refraction, eye-and-gesture-focused micro-states and volumetric lighting. Use when building spatial web, XR dashboards or next-generation glassmorphic interfaces."
---

# UI Style: Spatial UI & VisionOS Elevation

Pioneered by Apple visionOS and modern spatial computing paradigms. Moves beyond flat 2D glassmorphism into true 3D spatial glass, characterized by dynamic specular border highlights, adaptive environmental luminescence, deep depth blur, and gaze/hover elevation. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Designing spatial web applications, WebXR dashboards, high-end productivity suites, and luxury hardware interfaces.
- Imparting deep three-dimensional elevation, physical weightlessness, and responsive optical feedback.
- Upgrading conventional flat glassmorphic UIs to physically-modeled optical materials.

---

## 🕰️ Definition and Timeline

- **Origins:** Unveiled by Apple with visionOS at WWDC 2023, shipping commercially in February 2024. Represents the culmination of macOS Big Sur's translucent materials and iOS blur sheets, matured into volumetric spatial computing.
- **Material philosophy:** In spatial computing, interfaces live inside real human physical spaces. Opaque backgrounds feel heavy and disconnect the user from reality; flat transparent cards lack legibility. VisionOS glass solves this through multi-pass Gaussian blur combined with specular light physics that respond dynamically to ambient lighting.
- **Difference from neighbors:** Unlike classic [ui-style-glassmorphism](../ui-style-glassmorphism/SKILL.md), which relies on simple static `backdrop-filter: blur(10px)` and white borders, Spatial UI incorporates specular light tracking, layered z-axis elevation cards (`translateZ`), adaptive luminance compensation, and subtle inner occlusion shadows.

---

## 🎨 Visual DNA

- **Palette:** Highly translucent neutral glass layers (`rgba(255, 255, 255, 0.10)` to `rgba(255, 255, 255, 0.18)` over dark canvases; `rgba(255, 255, 255, 0.65)` over light). Background ambient glow combines deep obsidian navy (`#0E1017` to `#1A1F2C`) with subtle cosmic gradients.
- **Specular Highlights:** Top border highlight carries higher opacity (`rgba(255, 255, 255, 0.45)`), while side and bottom borders fade to `rgba(255, 255, 255, 0.12)`, simulating ceiling light reflection.
- **Depth & Refraction:** Deep multi-pass backdrop blur (`backdrop-filter: blur(40px) saturate(190%)`), paired with dual-layer soft elevation shadows (`0 20px 50px rgba(0, 0, 0, 0.35)`).
- **Type:** Clean, ultra-legible human-interface typography (SF Pro Display, Inter, Plus Jakarta Sans), accompanied by subtle embossed text shadows for optical legibility over variable backgrounds.
- **Shapes:** Generously rounded corners (`border-radius: 24px` to `32px` on cards; pill-shaped `9999px` on buttons and tab bars).

---

## 🖱️ Interaction and Motion

- Gaze and hover elevation: hovering over an element triggers a luminous specular flare following the cursor coordinates and raises the card smoothly along the z-axis (`transform: translateY(-3px) scale(1.01)`).
- Spring-loaded physics: transitions use natural Apple-style spring curves (`cubic-bezier(0.25, 1, 0.5, 1)`, duration `0.3s`).
- Inner glow intensification: interactive buttons illuminate their internal gradient when hovered, communicating touchable depth.
- Under `prefers-reduced-motion: reduce`, disable all z-axis scaling and specular cursor tracking, maintaining static translucent glass cards.

---

## 🛠️ Implementation Notes

```css
#stage[data-style="spatial-vision-os"] {
  --bg: #0e1017;
  --surface: rgba(255, 255, 255, 0.10);
  --surface-2: rgba(255, 255, 255, 0.18);
  --fg: #f5f5f7;
  --muted: #a1a1a6;
  --accent: #2997ff;
  --accent-fg: #ffffff;
  --border: rgba(255, 255, 255, 0.22);
  --radius: 24px;
  --radius-sm: 14px;
  --shadow: 0 20px 40px rgba(0, 0, 0, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.4);
  --font-body: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
  background: radial-gradient(circle at 50% 20%, #202738, #0e1017);
  color: var(--fg);
}

#stage[data-style="spatial-vision-os"] .card {
  background: var(--surface);
  backdrop-filter: blur(35px) saturate(190%);
  -webkit-backdrop-filter: blur(35px) saturate(190%);
  border: 1px solid var(--border);
  border-top-color: rgba(255, 255, 255, 0.45);
  box-shadow: var(--shadow);
  border-radius: var(--radius);
}
```

---

## ♿ Accessibility

- **Variable background contrast:** Translucent glass cards over dynamic backgrounds can suffer severe contrast degradation. Always implement a solid fallback backing (`#141721`) when contrast falls below WCAG AA 4.5:1.
- **Focus state affordance:** Do not rely solely on specular border glimmers for focus states. Provide a distinct 3px high-contrast outline (`#2997FF`) with a 3px offset.
- **GPU performance:** Layered `backdrop-filter: blur()` can trigger severe frame drops on lower-end devices; use `@supports (backdrop-filter: blur(1px))` with solid fallback backgrounds.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** Spatial computing apps, WebXR tools, high-end creative software, luxury fintech portals, and futuristic operating dashboards.
- **Caution:** High-density financial spreadsheets where ultra-thin text requires absolute opacity.
- **Avoid:** Low-spec mobile web contexts with constrained GPU resources, or sites prioritizing raw minimalism.

---

## 📚 Sources

- Apple Inc., "Principles of Spatial Design", WWDC 2023 Session 10072.
- Apple Inc., "Design for visionOS: Human Interface Guidelines", Apple Developer Documentation, 2023–2024.
- Nielsen Norman Group, "Spatial Computing and Usability in XR", 2024.

---

## 🔗 Integration with Other Skills

- Ancestor styles: [ui-style-glassmorphism](../ui-style-glassmorphism/SKILL.md), [ui-style-neumorphism](../ui-style-neumorphism/SKILL.md).
- Interactive craft: [ui-motion-specialist](../ui-motion-interaction/SKILL.md).
