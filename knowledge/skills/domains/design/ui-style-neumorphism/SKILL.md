---
name: "ui-style-neumorphism"
description: "Provides the canonical Neumorphism & Soft UI design style (2019-2020): monochromatic extruded and indented surfaces created from paired light-and-dark soft drop shadows, simulating plastic tactile relief. Covers shadow mathematics, directional lighting models, accessibility remediation, contrast border overlays, and hybrid design-system integration. Use when designing tactile smart-home remotes, audio equipment dials, or soft embossed card containers."
---

# UI Style: Neumorphism (Soft UI)

**Neumorphism** (a portmanteau of *neo* and *skeuomorphism*, also known as **Soft UI**) is the visual illusion of shapes extruded seamlessly from, or pressed indented into, a monochromatic background substrate. Rather than using contrasting surface colors or elevated drop shadows, Neumorphic elements share the exact hue of their parent background and rely on paired directional shadows—one bright white highlight offset towards the light source, and one soft dark shadow offset away—to simulate continuous embossed plastic or rubber skin.

---

## 🧭 When to Activate

- Designing tactile control remotes (smart-home thermostats, audio mixing dials, synthesizer knobs, lighting switches) where users expect physical mechanical relief.
- Evaluating Soft UI prototypes and applying essential accessibility remediation (adding high-contrast boundaries to prevent affordance collapse).
- Creating soft, tactile brand experiences, meditation tools, or embossed hardware telemetry cards in controlled single-theme interfaces.

---

## 🕰️ Definition, Lineage, and Timeline

- **Origins & Chronology:** Seeded in November 2019 by designer Alexander Plyuto on Dribbble with his *"Skeuomorph Mobile Banking"* shots. Formally named *"Neumorphism"* by Michał Malewicz in December 2019. Peaked rapidly in early 2020 before facing severe usability critiques for accessibility failures, ultimately settling into a specialized decorative and control-hardware accent.
- **The Core Illusion:** A single light source (typically upper-left, 135 degrees) shines across a continuous flat sheet. Elements do not float; they are vacuum-formed, pushed up (*extruded*) or stamped down (*concave / inset*).
- **Distinctions from Neighboring Styles:**
  - Unlike **Skeuomorphism** (rich realistic photographic textures: stitched leather, wood grain, brushed aluminum, glass gloss), Neumorphism is strictly flat, monochromatic, plastic, and textureless.
  - Unlike **Claymorphism** (inflated, colorful 3D marshmallow shapes with inner shadows and high chroma), Neumorphism is strictly monochromatic and subdued.
  - Unlike **Flat Design** (zero shadows, high-contrast solid color fills), Neumorphism relies entirely on diffuse shadows for shape definition.
- **Absolute Veto:** Borderless monochrome form fields where placeholder text and inputs share the background color (rendering them invisible to low-vision users) are strictly forbidden. All interactive inputs must feature explicit high-contrast boundaries meeting WCAG 1.4.11 (3:1).

---

## 🎨 Visual DNA & Subgenre Taxonomy

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 NEUMORPHISM MATRIX                                     │
├────────────────────────────┬────────────────────────────┬──────────────────────────────┤
│ 1. Extruded Surface (Out)  │ 2. Concave Well (Inset)    │ 3. Remediated Hybrid         │
│ • Paired light/dark drop   │ • Paired light/dark inset  │ • High-contrast 1.5px border │
│ • Appears pushed upwards   │ • Appears pressed or carved│ • High-contrast iconography  │
│ • Rounded pill/card corners│ • Used for active states   │ • Full WCAG 2.2 AA compliance│
└────────────────────────────┴────────────────────────────┴──────────────────────────────┘
```

- **Monochromatic Substrates:** Background, card, and button share an identical soft neutral base: warm gray (`#E0E5EC`), soft slate (`#DEE4ED`), or dark graphite (`#24272C`).
- **The Dual-Shadow Formula:** Two opposite shadows offset at 45 degrees:
  - Top-left highlight: negative X, negative Y, pure white or high luminance.
  - Bottom-right shadow: positive X, positive Y, low-opacity ambient darkness.
- **Curved Radii:** Generous corner rounding (12px to 28px) is mandatory; sharp 90-degree corners destroy the optical illusion of vacuum-formed plastic.

---

## 📐 Lighting Physics, Specular Splits & Surfaces

1. **Extruded Relief (Convex Button / Card):**
   - Light source positioned at 135 degrees (top-left).
   ```css
   background: #e0e5ec;
   border-radius: 16px;
   box-shadow: -8px -8px 16px #ffffff, 8px 8px 16px rgba(163, 177, 198, 0.6);
   ```
2. **Pressed Inset Well (Concave / Active State):**
   - Reversing the shadow direction to internal creates an indented carved trough.
   ```css
   background: #e0e5ec;
   border-radius: 16px;
   box-shadow: inset -6px -6px 12px #ffffff, inset 6px 6px 12px rgba(163, 177, 198, 0.65);
   ```

---

## 🏷️ Complete Design Tokens

```css
:root {
  /* Substrate Color (Must match element backgrounds) */
  --neu-base: #E0E5EC;
  --neu-base-dark: #24272C;

  /* Paired Light/Dark Shadow Offsets */
  --neu-shadow-light: -8px -8px 16px #FFFFFF;
  --neu-shadow-dark: 8px 8px 16px rgba(163, 177, 198, 0.6);
  --neu-shadow-light-sm: -4px -4px 8px #FFFFFF;
  --neu-shadow-dark-sm: 4px 4px 8px rgba(163, 177, 198, 0.5);

  /* Inset Shadows for Pressed States */
  --neu-inset-light: inset -6px -6px 12px #FFFFFF;
  --neu-inset-dark: inset 6px 6px 12px rgba(163, 177, 198, 0.65);

  /* Remediated Contrast Signals */
  --neu-text-primary: #1E293B;
  --neu-text-secondary: #475569;
  --neu-accent-primary: #2563EB;
  --neu-border-remedy: 1.5px solid #64748B;

  /* Typography */
  --neu-font-family: 'Plus Jakarta Sans', 'Inter', system-ui, sans-serif;
  --neu-radius: 16px;
  --neu-radius-pill: 9999px;
}
```

---

## 🔤 Typography & Lettering Architecture

- **Primary Display Headings:** Modern geometric grotesque (*Plus Jakarta Sans*, *Inter*) with medium to bold weights, providing clear hierarchy against the soft plastic background.
- **Body & Paragraphs:** High-contrast neutral sans (*Inter*) set in dark slate (`#1E293B`), ensuring 10.5:1 contrast against `#E0E5EC`.
- **The Contrast Rule:** Never use light gray or low-contrast text. Because the background is monochromatic gray, typography must carry the entire semantic readability weight.

---

## 🖱️ Interaction Dynamics, Sound Cues & Motion

- **State Transition (Extrude to Inset):** On `:active` or checked state, buttons seamlessly swap external drop shadows for internal inset shadows (`transition: box-shadow 0.15s ease-out`).
- **Tactile Depress Feel:** A micro-scale compression (`transform: scale(0.98)`) reinforces the sensation of physical plastic depression.
- **Dial & Knob Rotation:** Knurled rotary dials rotate smoothly with radial pointer tracking.
- **Motion Reduction:** When `prefers-reduced-motion: reduce` is enabled, scale transformations are disabled, relying purely on instantaneous shadow swaps.

---

## 🧩 Canonical Component Specifications

### 1. Remediated Soft Card (`.neu-card`)
An extruded container equipped with subtle boundary definition to ensure accessible perception.
```html
<article class="neu-card">
  <div class="neu-card-header">
    <span class="neu-tag">Smart Thermostat</span>
    <h3 class="neu-title">Living Room Climate</h3>
  </div>
  <p class="neu-text">Target temperature set to 21.5°C. Heat pump operating at steady state.</p>
</article>
```
```css
.neu-card {
  background: var(--neu-base);
  border-radius: var(--neu-radius);
  border: var(--neu-border-remedy);
  box-shadow: var(--neu-shadow-light), var(--neu-shadow-dark);
  padding: 1.75rem;
  color: var(--neu-text-primary);
  position: relative;
}
```

### 2. Tactile Push Button (`.neu-btn`)
An interactive action button that depresses mechanically from extruded to inset on click.
```css
.neu-btn {
  background: var(--neu-base);
  color: var(--neu-text-primary);
  border: var(--neu-border-remedy);
  border-radius: var(--neu-radius-pill);
  padding: 0.75rem 1.8rem;
  font-family: var(--neu-font-family);
  font-weight: 600;
  cursor: pointer;
  box-shadow: var(--neu-shadow-light-sm), var(--neu-shadow-dark-sm);
  transition: box-shadow 0.15s ease-out, transform 0.1s ease-out;
}
.neu-btn:hover {
  box-shadow: -6px -6px 12px #FFFFFF, 6px 6px 12px rgba(163, 177, 198, 0.7);
  transform: translateY(-1px);
}
.neu-btn:active, .neu-btn[aria-pressed="true"] {
  box-shadow: var(--neu-inset-light), var(--neu-inset-dark);
  transform: translateY(1px);
}
.neu-btn:focus-visible {
  outline: 3px solid var(--neu-accent-primary);
  outline-offset: 3px;
}
```

### 3. Slotted Track Slider (`.neu-slider`)
An indented horizontal groove housing a raised extruded slider thumb.

### 4. Rotary Embossed Dial (`.neu-dial`)
A circular extruded wheel featuring an engraved indicator notch and subtle radial gradients.

---

## ♿ Accessibility & Environmental Contrast (WCAG 2.2)

- **The Fundamental Failure of Pure Neumorphism:** Because pure neumorphism relies solely on subtle gray shadows on a gray background, borders between elements and the background achieve contrast ratios under 1.5:1—completely failing WCAG 1.4.11 (Non-text Contrast, requiring 3:1). Low-vision users and users in bright sunlight cannot perceive buttons or inputs.
- **The Remediation Protocol:**
  1. **Add Boundary Definition:** Use a boundary or state indicator whose contrast is verified against the actual substrate; a translucent gray stroke is not automatically remediation. The example uses solid `#64748B` on `#E0E5EC`, retaining paired soft shadows around it.
  2. **High-Contrast Text:** Set all body and title text in dark slate (`#1E293B`), ensuring 10.5:1 against the `#E0E5EC` ground (exceeding WCAG AAA 7:1).
  3. **High-Chroma Active States:** When a button is pressed or active, do not rely on shadow alone; introduce a distinct chromatic indicator (e.g. blue LED dot or colored text).
- **Focus Rings:** Unambiguous 3px solid accent outline (`outline: 3px solid #2563EB; outline-offset: 3px;`).

---

## ✅ When to Use / ❌ When to Avoid

### Ideal Use Cases
- Smart-home physical appliance interfaces, thermostat controllers, and IoT remote control panels.
- Digital music synthesizers, guitar pedal simulators, and audio mastering consoles.
- Tactile concept showcases and design exhibitions where physical skeuomorphic relief is the focus.

### Anti-Patterns & Prohibitions
- Critical high-volume consumer e-commerce checkout forms.
- Data-dense administrative dashboards requiring hundreds of table rows and inputs.
- Multi-theme applications where dynamic background shifts break the fragile monochromatic shadow formula.

---

## 📚 Authoritative Sources & Historical Artifacts

- Alexander Plyuto, *Skeuomorph Mobile Banking Continuation*, Dribbble, Dec 2019.
- Michał Malewicz, "Neumorphism in user interfaces", *UX Collective*, Dec 2019.
- Adrian Bece, "Neumorphism and CSS", *CSS-Tricks*, Mar 2020.
- Nick Babich, "Why Neumorphism is a Bad Idea for User Experience", *UX Planet*, 2020.

---

## 🔗 Cross-Skill Integration & Dialect Relations

- **Sibling Material Styles:** [ui-style-claymorphism](../ui-style-claymorphism/SKILL.md), [ui-style-glassmorphism](../ui-style-glassmorphism/SKILL.md), [ui-style-skeuomorphism](../ui-style-skeuomorphism/SKILL.md).
- **Tactile & Hardware Peers:** [ui-style-flat-design](../ui-style-flat-design/SKILL.md), [ui-style-card-based-ui](../ui-style-card-based-ui/SKILL.md), [ui-style-cassette-futurism](../ui-style-cassette-futurism/SKILL.md).
## Appearance and Interaction Verification

Replace subtle-border-as-remediation assurance with a verified boundary/indicator pair at rest, checked, focus and disabled states; update push-button example to follow it and recalculate both paired shadows and ink if an alternate substrate is requested.

