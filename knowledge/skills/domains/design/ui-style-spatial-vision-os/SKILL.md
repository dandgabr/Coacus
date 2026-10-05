---
name: "ui-style-spatial-vision-os"
description: "Provides the visionOS and spatial computing UI style: multi-layered glass elevation, dynamic specular edge reflections, deep material refraction and eye/gesture-focused micro-states. Use when building spatial web, XR dashboards or next-gen glassmorphic interfaces."
---

# UI Style: Spatial UI & VisionOS Elevation

Pioneered by Apple visionOS and modern spatial computing paradigms. Moves beyond flat glassmorphism into true 3D spatial glass, characterized by dynamic specular border highlights, adaptive environmental luminescence, deep depth blur, and gaze/hover elevation.

---

## 🧭 When to Activate

- Spatial web applications, WebXR dashboards, high-end productivity suites, and luxury hardware interfaces.
- Imparting deep three-dimensional elevation, physical weightlessness, and responsive optic feedback.

---

## 🎨 Visual DNA

- **Palette:** Highly translucent neutral glass layers (`rgba(255, 255, 255, 0.12)` over dark; `rgba(255, 255, 255, 0.65)` over light), with crisp white specular rims (`rgba(255, 255, 255, 0.3)` to `0.8`).
- **Materials:** Deep multi-pass backdrop blur (`backdrop-filter: blur(40px) saturate(180%)`), inner glow highlights, and subtle shadow occlusion.
- **Hover/Interaction:** Interactive light follows pointer cursor, illuminating border bevels dynamically; soft 3D scale-up on hover (`transform: translateZ(12px)`).
- **Type:** Clean, ultra-legible system typography (SF Pro Display, Inter) with subtle embossed text shadows for optical legibility over variable backgrounds.

---

## 🛠️ Implementation Notes

```css
.spatial-glass-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(40px) saturate(190%);
  -webkit-backdrop-filter: blur(40px) saturate(190%);
  border: 1px solid rgba(255, 255, 255, 0.22);
  border-top-color: rgba(255, 255, 255, 0.45);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.25), inset 0 1px 0 rgba(255, 255, 255, 0.35);
  border-radius: 28px;
}
```

---

## ♿ Accessibility

- Translucent glass must maintain adequate contrast over dynamic or moving background imagery; utilize solid background fallbacks when contrast drops below 4.5:1.
