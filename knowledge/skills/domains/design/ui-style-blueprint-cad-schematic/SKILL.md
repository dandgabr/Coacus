---
name: "ui-style-blueprint-cad-schematic"
description: "Provides the architectural blueprint and CAD schematic UI style: engineering cyan lines, coordinate crosshairs, dimension tick marks, monospaced drafting notes and technical grid backing. Use when building engineering tools, architecture portfolios or technical hardware docs."
---

# UI Style: Blueprint & CAD Technical Schematic

Derived from traditional cyanotype architectural blueprints and modern CAD (Computer-Aided Design) drafting software. Emphasizes mathematical precision, dimensioning arrows, coordinate systems, grid callouts, and technical drafting aesthetics.

---

## 🧭 When to Activate

- Developer tools, architectural portfolios, robotics hardware telemetry, infrastructure docs, and industrial manufacturing sites.
- Communicating rigorous precision, engineering authority, and transparent mechanics.

---

## 🎨 Visual DNA

- **Palette:** Blueprint cyan (`#00F0FF`), drafting deep navy (`#0A192F`), precision white (`#FFFFFF`), grid blue (`#1E3A5F`), and revision red (`#FF3B30`).
- **Type:** Architectural drafting fonts, monospaced consoles (Consolas, Space Mono, Technical Drafting Sans).
- **Details:** Orthogonal dimension ticks, angle callouts, coordinate crosshairs, millimeter grid paper backgrounds, and title block approval stamps.

---

## 🛠️ Implementation Notes

```css
.blueprint-canvas {
  background-color: #0b1d3a;
  background-image: linear-gradient(rgba(0, 240, 255, 0.15) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(0, 240, 255, 0.15) 1px, transparent 1px);
  background-size: 20px 20px;
  color: #00f0ff;
  border: 2px solid #00f0ff;
}
```

---

## ♿ Accessibility

- Glowing cyan against deep navy provides strong contrast, but fine 1px grid lines should remain at low opacity so they do not distract from reading primary text.
