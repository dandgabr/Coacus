---
name: "ui-style-claymorphism"
description: "Provides the canonical Claymorphism & Stop-Motion 3D UI style (2021-present): inflated, tactile modeling clay surfaces, pillowy rounded containers, dual inner shadows simulating curved 3D volume, pastel-vibrant palettes, and playful plasticine charm. Covers inner shadow mathematics, tactile hover squish physics, design tokens, and WCAG 2.2 accessibility. Use when designing children's educational apps, gamified dashboards, crypto/NFT playful interfaces, or friendly mobile products."
---

# UI Style: Claymorphism & Stop-Motion 3D

**Claymorphism** is the design style of inflated, tactile 3D surfaces resembling soft modeling clay, plasticine, or marshmallow cushions. Coined in late 2021 by designer Michał Malewicz as a playful and accessible evolution of neumorphism, Claymorphism solves neumorphism's contrast failure by floating brightly colored, fully inflated objects above contrasting backgrounds. The signature physical illusion is achieved using **dual inner shadows** (one light highlight and one darker tone) that curve the interior face into a bulbous, puffy cushion.

---

## 🧭 When to Activate

- Designing friendly consumer mobile apps, gamified habit trackers, children's educational platforms, or onboarding wizards.
- Creative tools, toy brand showcases, casual video game user interfaces, or crypto/NFT platforms seeking approachable tactile warmth.
- Replacing sterile corporate flat boxes with friendly, voluminous 3D cushion cards that invite touch and playful interaction.

---

## 🕰️ Definition, Lineage, and Timeline

- **Origins & Emergence:** Coined in December 2021 by Michał Malewicz (UX Collective). Rose alongside the popularity of 3D illustration tools (Blender, Spline) and playful metaverse/NFT art aesthetics.
- **The Physical Metaphor:** Hand-sculpted plasticine or soft matte rubber. Objects appear plump, inflated with air, and soft to the touch, evoking Aardman stop-motion animation (*Wallace & Gromit*) and physical toy prototypes.
- **Distinctions from Neighboring Styles:**
  - Unlike **Neumorphism** (flat extruded monochrome background, weak contrast, zero inner color fills), Claymorphism uses distinct vibrant card fills that float above different background colors, completely passing contrast audits.
  - Unlike **Glassmorphism** (frosted translucent blur, 1px white specular hair rim), Claymorphism is 100% opaque, matte, bulbous, and pillowy.
  - Unlike **Skeuomorphism** (photorealistic wood, leather, brushed metal), Claymorphism represents stylized cartoon plasticine with matte lighting.
- **Absolute Veto:** Rigid 90-degree square corners or metallic chrome gradients. Claymorphic shapes must always be softly rounded (`border-radius: 20px` to `40px`) with velvety matte surfaces.

---

## 🎨 Visual DNA & Subgenre Taxonomy

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 CLAYMORPHISM MATRIX                                    │
├────────────────────────────┬────────────────────────────┬──────────────────────────────┤
│ 1. Pastel Marshmallow      │ 2. Saturated Plasticine    │ 3. Gamified Toy Prototype    │
│ • Soft butter & lavender   │ • Punchy coral, cyan & lime│ • Bold squishy action buttons│
│ • Deep inner volume shadow │ • High-contrast dark text  │ • Bouncy spring micro-actions│
│ • Pillowy rounded cards    │ • Floating drop elevation  │ • Playful badge badges       │
└────────────────────────────┴────────────────────────────┴──────────────────────────────┘
```

- **Palette & Vibrancy:** Butter cream ground (`#F8F5EE`), soft lilac (`#E0D7FF`), puffy sky blue (`#C8E7FF`), strawberry coral (`#FF9EAA`), mint clay (`#B4F8C8`), and deep charcoal text (`#1A1D20`).
- **The Dual Inner-Shadow Formula:** Two opposite inset shadows creating interior curvature:
  - Upper-left inner highlight: `inset 4px 4px 8px rgba(255, 255, 255, 0.7)` (reflecting overhead light).
  - Bottom-right inner shadow: `inset -6px -6px 12px rgba(0, 0, 0, 0.12)` (shading the bottom curve).
- **Floating Drop Shadow:** A soft, diffused outer drop shadow (`0 16px 32px rgba(0, 0, 0, 0.08)`) establishing that the clay cushion floats above the floor.

---

## 📐 Lighting Physics, Specular Splits & Surfaces

1. **Inflated Cushion (Convex Clay Surface):**
   - Combining outer drop shadow with dual opposing inner volume shadows.
   ```css
   background-color: #e0d7ff;
   border-radius: 28px;
   box-shadow:
     0 14px 28px rgba(100, 80, 160, 0.15),
     inset 4px 4px 8px rgba(255, 255, 255, 0.75),
     inset -6px -6px 12px rgba(80, 60, 140, 0.25);
   ```
2. **Squished Active Press State:**
   - On click, inner shadow deepens and element scales down slightly, simulating pliable clay compression.
   ```css
   transform: scale(0.97);
   box-shadow:
     0 6px 14px rgba(100, 80, 160, 0.18),
     inset 6px 6px 10px rgba(80, 60, 140, 0.3),
     inset -3px -3px 6px rgba(255, 255, 255, 0.6);
   ```

---

## 🏷️ Complete Design Tokens

```css
:root {
  /* Substrates & Clay Volumes */
  --clay-bg: #F8F5EE;
  --clay-card-lavender: #E4DCFF;
  --clay-card-sky: #CDE8FF;
  --clay-card-coral: #FFB5BC;
  --clay-card-mint: #C4F5D5;
  --clay-surface-white: #FFFFFF;

  /* Shadow Physics */
  --clay-drop-shadow: 0 16px 32px rgba(45, 35, 65, 0.08);
  --clay-drop-shadow-sm: 0 8px 18px rgba(45, 35, 65, 0.1);
  --clay-inner-light: inset 4px 4px 8px rgba(255, 255, 255, 0.8);
  --clay-inner-dark: inset -6px -6px 12px rgba(45, 35, 65, 0.15);

  /* Typography & Signals */
  --clay-text-primary: #1F242D;
  --clay-text-muted: #565F71;
  --clay-accent: #6366F1;

  /* Typography */
  --clay-font-display: 'Fredoka', 'Quicksand', 'Nunito', sans-serif;
  --clay-font-body: 'Nunito', system-ui, sans-serif;
  --clay-radius: 28px;
  --clay-radius-pill: 9999px;
}
```

---

## 🔤 Typography & Lettering Architecture

- **Primary Display Headings:** Friendly, rounded sans-serifs (*Fredoka*, *Quicksand*, *Nunito*) with plump stroke terminals, generous letter-spacing, and warm approachable cadence.
- **Body & Paragraphs:** High-legibility rounded sans (*Nunito*, *Comfortaa*) set in deep charcoal (`#1F242D`) ensuring high-contrast readability against pastel clay surfaces.
- **Button Microcopy:** Clear, encouraging action text ("Squish Here", "Let's Play", "Claim Badge") set in bold weights.

---

## 🖱️ Interaction Dynamics, Sound Cues & Motion

- **Pliable Squish Feedback:** On `:active`, clay buttons compress slightly along the vertical axis (`transform: scale(0.97, 0.94)`), simulating soft rubber or modeling dough being pressed down.
- **Natural Spring Rebound:** On release, elements bounce back with a natural spring curve (`cubic-bezier(0.34, 1.56, 0.64, 1)`).
- **Floating Hover Bob:** Interactive cards float upward slightly on cursor hover (`transform: translateY(-4px)`).
- **Motion Reduction:** When `prefers-reduced-motion: reduce` is enabled, bouncy spring transforms are disabled in favor of instantaneous shadow adjustments.

---

## 🧩 Canonical Component Specifications

### 1. Inflated Marshmallow Card (`.clay-card`)
A bulbous container with curved inner volume shadows and warm charcoal typography.
```html
<article class="clay-card">
  <div class="clay-badge">Level 4 Completed!</div>
  <h3 class="clay-title">Creative Workshop</h3>
  <p class="clay-text">Your stop-motion animation frames are rendered and ready for playback.</p>
</article>
```
```css
.clay-card {
  background: var(--clay-card-lavender);
  color: var(--clay-text-primary);
  border-radius: var(--clay-radius);
  box-shadow: var(--clay-drop-shadow), var(--clay-inner-light), var(--clay-inner-dark);
  padding: 2rem;
  position: relative;
  transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.clay-card:hover {
  transform: translateY(-4px);
}
.clay-badge {
  display: inline-block;
  background: #FFFFFF;
  color: var(--clay-accent);
  font-family: var(--clay-font-display);
  font-weight: 700;
  font-size: 0.85rem;
  padding: 0.35rem 0.85rem;
  border-radius: var(--clay-radius-pill);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.06), inset 2px 2px 4px #FFFFFF, inset -2px -2px 4px rgba(0, 0, 0, 0.08);
  margin-bottom: 0.75rem;
}
```

### 2. Squishy Action Button (`.clay-btn`)
An action button finished in coral clay with tactile spring compression on click.
```css
.clay-btn {
  background: var(--clay-card-coral);
  color: #1F242D;
  font-family: var(--clay-font-display);
  font-size: 1.1rem;
  font-weight: 700;
  padding: 0.85rem 2rem;
  border: none;
  border-radius: var(--clay-radius-pill);
  box-shadow: 0 8px 18px rgba(255, 158, 170, 0.4), inset 3px 3px 6px rgba(255, 255, 255, 0.8), inset -4px -4px 8px rgba(180, 80, 95, 0.3);
  cursor: pointer;
  transition: transform 0.15s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.15s ease;
}
.clay-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 24px rgba(255, 158, 170, 0.5), inset 3px 3px 6px rgba(255, 255, 255, 0.9), inset -4px -4px 8px rgba(180, 80, 95, 0.35);
}
.clay-btn:active {
  transform: scale(0.96);
  box-shadow: 0 4px 10px rgba(255, 158, 170, 0.3), inset 5px 5px 8px rgba(180, 80, 95, 0.35), inset -2px -2px 4px rgba(255, 255, 255, 0.6);
}
.clay-btn:focus-visible {
  outline: 3px solid #6366F1;
  outline-offset: 4px;
}
```

### 3. Puffy Counter Pill (`.clay-pill-counter`)
An inflated metric pill with internal 3D depth and bold numeric values.

### 4. Floating Clay Tab Rail (`.clay-tab-rail`)
A rounded container housing floating clay button tabs with spring indicator pill transitions.

---

## ♿ Accessibility & Environmental Contrast (WCAG 2.2)

- **The Contrast Advantage Over Neumorphism:** Because claymorphic elements float with distinct colored card surfaces (`#E4DCFF`, `#FFB5BC`) over background substrates (`#F8F5EE`), card perimeter boundaries achieve clear visual separation.
- **Text Legibility (WCAG 1.4.3):** Charcoal text (`#1F242D`) on pastel lavender and coral achieves contrast ratios exceeding 9.5:1, easily surpassing WCAG AAA (7:1).
- **Non-Text Boundary Contrast (WCAG 1.4.11):** Soft shadows do not guarantee a 3:1 boundary. Verify the actual perimeter or required state indicator against its surrounding floor, and strengthen a contour when necessary while retaining matte volume.
- **Focus Rings:** High-visibility indigo outline with 4px offset (`outline: 3px solid #6366F1; outline-offset: 4px;`).

---

## ✅ When to Use / ❌ When to Avoid

### Ideal Use Cases
- Children's educational apps, coding toys, and playful learning management platforms.
- Gamified fitness, language learning apps (Duolingo-inspired friendliness), and digital habit trackers.
- Creative showcases, toy store catalogs, and friendly indie game interfaces.

### Anti-Patterns & Prohibitions
- Formal legal, banking compliance, or medical emergency software where playful toy aesthetics undermine authority.
- High-density data tables and administrative enterprise software with space constraints.
- Dark mode environments where pastel clay colors look muddy or unnatural.

---

## 📚 Authoritative Sources & Historical Artifacts

- Michał Malewicz, "Claymorphism in user interfaces", *UX Collective*, Dec 2021.
- CodyHouse, "CSS Claymorphism and 3D UI", 2022.
- Aardman Animations, *The Art of Stop-Motion Animation*, 2018.
- Jakob Nielsen, *10 Usability Heuristics for User Interface Design*, Nielsen Norman Group, 1994.

---

## 🔗 Cross-Skill Integration & Dialect Relations

- **Sibling 3D & Material Styles:** [ui-style-neumorphism](../ui-style-neumorphism/SKILL.md), [ui-style-glassmorphism](../ui-style-glassmorphism/SKILL.md), [ui-style-skeuomorphism](../ui-style-skeuomorphism/SKILL.md).
- **Playful & Friendly Peers:** [ui-style-kawaii-pastel-soft](../ui-style-kawaii-pastel-soft/SKILL.md), [ui-style-card-based-ui](../ui-style-card-based-ui/SKILL.md), [ui-style-3d-immersive-webgl](../ui-style-3d-immersive-webgl/SKILL.md).
## Appearance and Interaction Verification

Replace automatic clay contrast guarantees with checking inset edges, perimeter and pressed state against the real floor; strengthen a contour where needed while preserving inflated matte volume, pastel fills and instantaneous shadow feedback under reduced motion.
