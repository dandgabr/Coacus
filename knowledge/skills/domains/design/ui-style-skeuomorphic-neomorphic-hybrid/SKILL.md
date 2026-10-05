---
name: "ui-style-skeuomorphic-neomorphic-hybrid"
description: "Provides the hybrid skeu-morphic and neomorphic UI style: calibrated tactile bevels, inner glass refraction, physical depth without clutter and refined haptic affordance. Use when designing premium audio plugins, smart home controllers or luxury digital hardware."
---

# UI Style: Skeuomorphic-Neomorphic Hybrid (Soft Depth)

Synthesizes the tactile familiarity of classic skeuomorphism (dials, toggles, beveled edges) with the clean elegance of modern neumorphism and glassmorphism. Creates rich, touchable interfaces without the heavy ornamentation of early skeuomorphic software.

---

## 🧭 When to Activate

- Digital audio workstations (DAW), audio plugins, smart home hardware controls, and luxury automotive consoles.
- When clear physical affordance and tactile depth are required for precise interactive manipulation.

---

## 🎨 Visual DNA

- **Palette:** Polished aluminum silver (`#E3E6EB`), deep tactile dark slate (`#1E222B`), illuminated blue/amber indicator LEDs (`#38BDF8`).
- **Shading:** Precision dual-shadows (diffuse ambient shadow combined with razor-sharp specular rim light), milled metal concentric rings, and soft convex pill shapes.
- **Controls:** Rotary encoders, knurled metal knobs, recessed toggle switches, and back-lit silicone buttons.

---

## 🛠️ Implementation Notes

```css
.tactile-knob {
  background: linear-gradient(145deg, #f0f3f8, #d8dbe0);
  box-shadow: 6px 6px 12px #c2c5ca, -6px -6px 12px #ffffff, inset 1px 1px 2px rgba(255, 255, 255, 0.8);
  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.6);
}
```

---

## ♿ Accessibility

- Low-contrast neumorphic edges frequently fail WCAG non-text contrast; this hybrid style solves this by introducing defined 1px boundary lines and crisp status indicators.
