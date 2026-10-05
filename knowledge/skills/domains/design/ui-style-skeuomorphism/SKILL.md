---
name: "ui-style-skeuomorphism"
description: "Provides the complete skeuomorphism UI style (2007-present): real-world tactile physical metaphors, stitched leather, brushed aluminum, milled metal dials, Y2K cyber aqua gloss and tactile affordances. Covers historical iOS 1-6 lineage, modern skeu-neomorphic hybrids, translucent iMac optimism and contrast accessibility. Use when designing tactile audio plugins, metaphor-first onboarding or physical device emulations."
---

# UI Style: Skeuomorphism (Classic, Modern Hybrid & Cyber Aqua)

Interfaces retaining tactile metaphors and ornamental cues from real-world physical objects. Derived from Greek *skeuos* (container/tool) + *morphē* (form). Spans the full historical arc: from classic iOS 1–6 stitched leather and mahogany shelves, to early-2000s translucent Aqua candy gloss, to contemporary skeuomorphic-neomorphic hybrids (milled aluminum dials, realistic mechanical switches, and precision audio plugins). Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Audio production software, synthesizer plugins, virtual mixing consoles, and physical hardware simulators.
- Metaphor-led onboarding for audiences where real-world physical parallels dramatically reduce learning curves.
- Specialized luxury watch showcases, craft tools, and retro computing celebrations.
- Modern tactile interfaces seeking tangible physical weight without flat sterility.

---

## 🕰️ Definition and Timeline

- **Classic Era (2007–2012):** Apple iOS 1 through 6 under Scott Forstall. Real-world physical simulations (green casino felt in Game Center, stitched leather in Calendar, yellow legal pad in Notes). Ended at Apple with iOS 7 (WWDC 2013) led by Jony Ive.
- **Y2K Cyber Aqua Strand (1998–2003):** Mac OS X Aqua interface (Steve Jobs: "liquid, you'd want to lick it") paired with Bondi Blue iMac G3 hardware. Characterized by pulsing blue jelly buttons, brushed metal, pinstripe textures, and candy drop reflections.
- **Modern Hybrid / Soft Tactile Strand (2020s):** The synthesis of skeuomorphism and subtle depth: precision-milled aluminum knurling, rotary dials with optical specular reflection, tactile toggle physics, and instrument-grade affordance.
- **Difference from neighbors:** Unlike [ui-style-neumorphism](../ui-style-neumorphism/SKILL.md), which is sculpted entirely out of the background plane with uniform soft shadows, Skeuomorphism incorporates multi-material diversity (wood, glass, chrome, plastic, leather) and authentic specular highlights.

---

## 🎨 Visual DNA

- **Surfaces & Materials:**
  - *Classic:* Stitched leather, mahogany wood, green billiard felt, brushed metal.
  - *Aqua Cyber:* Translucent colored plastic (Bondi blue, ruby, lime), liquid glass bubbles, horizontal gloss highlights.
  - *Modern Hybrid:* Milled aluminum knobs with radial knurling, anodized dark metal, precision instrument bezels.
- **Depth & Lighting:** Consistent top-down lighting (90° or 120° light angle); multi-layered drop shadows, sharp inner specular highlights, and calibrated bevels (`box-shadow: inset 0 1px 0 rgba(255,255,255,0.7), inset 0 -1px 0 rgba(0,0,0,0.3)`).
- **Typography:** Crisp humanist sans-serifs or robust technical grotesques (Helvetica Neue, SF Pro, Inter) featuring subtle debossed letterpress text shadows (`text-shadow: 0 1px 0 rgba(255,255,255,0.8)` on light surfaces; `0 -1px 0 rgba(0,0,0,0.9)` on dark).

---

## 🖱️ Interaction and Motion

- **Physical Tactile Affordance:** Buttons visibly depress into the surface when clicked (`transform: translateY(2px)` with contracted bottom shadow).
- **Rotary & Slider Mechanics:** Volume knobs and rotary switches rotate along an axis, with subtle optical glint shifts simulating physical light reflection.
- **Tactile Transitions:** Mechanical toggle switches flip with snappy, weighted damping.
- Under `prefers-reduced-motion: reduce`, disable continuous rotation and spring damping while preserving static tactile button states.

---

## 🛠️ Implementation Notes

```css
.tactile-dial {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: conic-gradient(from 180deg, #d8d8d8, #f5f5f5, #b8b8b8, #f5f5f5, #d8d8d8);
  box-shadow: 
    0 10px 20px rgba(0, 0, 0, 0.25),
    inset 0 2px 3px rgba(255, 255, 255, 0.9),
    inset 0 -2px 3px rgba(0, 0, 0, 0.4);
  border: 1px solid #a0a0a0;
  cursor: grab;
}
.aqua-btn {
  background: linear-gradient(180deg, #6bb6ff 0%, #1e88e5 50%, #1565c0 51%, #1976d2 100%);
  border: 1px solid #0d47a1;
  border-radius: 9999px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2), inset 0 1px 2px rgba(255, 255, 255, 0.8);
  color: #ffffff;
  text-shadow: 0 -1px 1px rgba(0, 0, 0, 0.5);
}
.aqua-btn:active {
  background: linear-gradient(180deg, #1565c0 0%, #1976d2 50%, #0d47a1 51%, #1565c0 100%);
  transform: translateY(1px);
}
```

---

## ♿ Accessibility

- **Affordance Advantage:** As proven in usability research (Don Norman; Spiliotopoulos et al., 2018), physical tactile cues provide clear affordance and faster recognition for first-time or cognitive-assist users.
- **Contrast Rigor:** Beveled buttons and embossed letterpress text must maintain strict 4.5:1 text contrast and 3:1 control edge contrast (WCAG 1.4.3 & 1.4.11).
- **Touch Targets:** Complex mechanical dials and switches must provide adequate hit areas (minimum 44×44px or 24×24px per WCAG 2.5.8).

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** Digital audio workstations (DAWs), musical instrument interfaces, audio plugin effect units, retro hardware emulation, interactive onboarding, and luxury product configuration.
- **Avoid:** High-speed data-entry screens, mobile banking lists, text-heavy reading platforms, and minimalist enterprise workflows where decorative textures cause visual fatigue.

---

## ⚠️ Pitfalls

- Overloading screens with excessive contrasting textures (leather next to wood next to chrome), creating cacophony.
- Recreating obsolete physical constraints (such as pagination limited to physical book-page dimensions) that degrade digital usability.
- Heavy raster image assets: implement metallic reflections with CSS gradients and SVG rather than giant bitmap sprite sheets.

---

## 📚 Sources

- Don Norman, "Affordances and Design", 2004 — http://www.jnd.org/dn.mss/affordances_and.html
- Spiliotopoulos, Rigou & Sirmakessis, "A Comparative Study of Skeuomorphic and Flat Design from a UX Perspective", *Multimodal Technologies and Interaction*, 2018.
- Nick Wingfield & Nick Bilton, "Apple Shake-Up Could Lead to Design Shift", *The New York Times*, 2012.
- Steve Jobs, *Mac OS X Aqua Unveiling*, Macworld San Francisco, 2000.
- W3C, *Web Content Accessibility Guidelines 2.2* (1.4.3, 1.4.11, 2.5.8) — https://www.w3.org/TR/WCAG22/

---

## 🔗 Integration with Other Skills

- Ancestor and sibling styles: [ui-style-flat-design](../ui-style-flat-design/SKILL.md), [ui-style-neumorphism](../ui-style-neumorphism/SKILL.md), [ui-style-frutiger-aero](../ui-style-frutiger-aero/SKILL.md), [ui-style-steampunk](../ui-style-steampunk/SKILL.md).
