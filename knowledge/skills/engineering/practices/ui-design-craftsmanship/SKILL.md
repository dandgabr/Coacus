---
name: "ui-design-craftsmanship"
description: "Provides interface design direction, heuristic critique and rendered verification when designing or refining visual, responsive and interaction quality."
---

# UI Design Craftsmanship

This skill equips coding agents with human-grade design discipline, ergonomic precision, and visual taste, eradicating generic "AI slop" and elevating frontend implementations into publication-grade, tactile, and accessible software.

---

## 🧭 Foundational Pillars

### 1. The Separation of Truth
- **`PRODUCT.md`**: Captures durable product truth (audience, core problem, operating constraints, voice, factual evidence). Never mix business requirements with visual styling choices.
- **`DESIGN.md`**: Captures visual system authority (tokens in `oklch()`, font scale ratios, surface treatments, spacing grids, elevation recipes).

### 2. The 4 Surface Modes
Every interface surface MUST declare its visitor mode:
- **`Persuade`**: (Landing pages, marketing, pricing). Design is the product. High contrast, sharp editorial typography, deliberate visual anchors.
- **`Operate`**: (Dashboards, editors, admin tools, data tables). Task completion outranks expression. High information density, predictable scannability, rock-solid keyboard navigation.
- **`Read`**: (Documentation, guides, long-form articles). Optimal measure (45-75 characters per line), typographic rhythm, distraction-free legibility.
- **`Experience`**: (Portfolios, interactive showcases, creative tools). The UI recedes; the user's focus is dedicated entirely to the central artifact.

---

## 🛠️ Intentional Design Directives

When directing or refining interfaces, apply these specific actions:

| Category | Action | Objective |
| :--- | :--- | :--- |
| **Build** | `shape` | Plan layout hierarchy, user flows, and state architecture before writing CSS/code. |
| **Build** | `init` | Inspect context and record durable product facts into `PRODUCT.md`. |
| **Build** | `document` | Extract and formalize existing CSS/Tailwind variables into `DESIGN.md`. |
| **Build** | `extract` | Pull repeated component patterns and tokens into reusable design system primitives. |
| **Evaluate** | `critique` | Conduct a UX design critique scoring visual hierarchy, alignment, rhythm, and clarity. |
| **Evaluate** | `audit` | Run technical verification: WCAG 2.2 AA contrast, responsive breakpoints, layout shifts. |
| **Refine** | `polish` | Final quality pass: alignment, micro-spacings, hover/focus rings, and border hairlines. |
| **Refine** | `bolder` | Inject character into timid, bland layouts: amplify scale contrast, tighten typography. |
| **Refine** | `quieter` | Tone down aggressive, over-saturated layouts: reduce competing visual noise. |
| **Refine** | `distill` | Strip away decorative fluff, redundant cards, and non-functional containers. |
| **Refine** | `harden` | Implement empty states, loading skeletons, error boundaries, and text overflows; skeleton and state-change mechanics in [ui-state-layout-transitions](../../../domains/design/ui-state-layout-transitions/SKILL.md). |
| **Refine** | `onboard` | Design guided first-run paths, progressive disclosure, and empty-state incentives. |
| **Enhance** | `animate` | Choose purposeful motion and timing for the task; preserve complete reduced-motion states. |
| **Enhance** | `colorize` | Introduce intentional, semantic color accents into sterile monochrome layouts. |
| **Enhance** | `typeset` | Establish a mathematical type scale (1.25 or 1.333) with calibrated line-heights. |
| **Enhance** | `layout` | Fix visual rhythm, enforce multi-tier spacing grids (4px/8px), and ensure section breathing. |
| **Enhance** | `delight` | Add subtle, memorable tactile micro-interactions (magnetic hovers, tactile clicks); recipes in [pointer-and-gesture](../../../domains/design/ui-motion-interaction/references/pointer-and-gesture.md). |
| **Enhance** | `overdrive` | Implement technically extraordinary effects (shaders, dynamic canvas, physics). |
| **Fix** | `clarify` | Rewrite ambiguous UX copy, microcopy, form field labels, and validation errors. |
| **Fix** | `adapt` | Adapt layout seamlessly for extreme screen sizes, mobile viewports, and touch targets. |
| **Fix** | `optimize` | Eliminate jank, layout recalculations, uncompressed visual assets, and CLS. |

---

## 🔬 The 5 Heuristic Self-Tests

Before completing any frontend delivery, run these 5 deterministic mental audits:

1. **The Squint Test (Focal Clarity)**:
   - Defocus your eyes. Is the primary call-to-action or focal point immediately unmistakable? If three elements compete for primary attention, demote two.
2. **The Border Strip Test (Typographic Hierarchy)**:
   - Mentally remove all borders, card backgrounds, and dividing lines. Does the layout still hold together logically solely through typography and whitespace? If not, the typography is too weak.
3. **The Color Budget Test (Chromatic Discipline)**:
   - Does each color have a purpose in this product and visual language? A restrained task interface and a deliberate multicolor composition need different budgets. Check legibility and state meaning before replacing the palette with neutrals.
4. **The Target Ergonomics Test (Hit Areas & Thumb Zones)**:
   - Does every interactive target measure at least 24×24 CSS px (WCAG 2.5.8, AA), with primary touch controls at the 44×44 enhanced target (2.5.5, AAA) where the layout allows? Is critical action density calibrated to prevent accidental clicks?
5. **The Motion Budget Test (Accessibility & Restraint)**:
   - Are duration, interruption and movement appropriate to the task? Brief feedback and a narrative sequence need different timing; check each duration against the canonical bands in [motion-timing-engines](../../../domains/design/ui-motion-interaction/references/motion-timing-engines.md). Reduced motion must retain complete content and usable controls; decorative motion is optional.

## 🧪 Rendered Interface Verification

When a UI has multiple themes, responsive layouts, scroll reveals, or dialogs with explicit choices, verify the rendered behavior against the actual DOM. Use [rendered-interface verification](references/rendered-interface-verification.md) for the checks and release evidence. To exercise a checker outside the product, use the [interface fixture exercises](references/interface-fixture-exercises.md).

---

## 🚫 AI Slop Blacklist & Prescribed Antidotes

| Generic AI Tell ("Slop") | Root Cause | Prescribed Craft Antidote |
| :--- | :--- | :--- |
| **Icon in a rounded pastel box** | Habit of placing an icon tile above every card title | Place the icon inline with text or eliminate it. Rely on strong typographic titles. |
| **Single italic serif word** | Inserting an italic serif word in a sans-serif headline | Commit to a single typeface family or establish a coherent editorial contrast across the entire header. |
| **Hero eyebrow pill badge** | Formulaic pill with sparkles/emojis above hero | Replace with a crisp, uppercase tracking kicker or eliminate the redundant badge entirely. |
| **Gray text on colored fill** | `text-gray-400` on `bg-blue-600` or `bg-slate-900` | Choose verified foreground/background pairs; light or dark ink can be appropriate depending on the actual fill. |
| **Nested card syndrome** | Card inside card inside card with heavy borders | Eliminate internal cards. Differentiate groupings using subtle background tint shifts or spacing. |
| **Vague, oversized shadows** | `shadow-2xl` spreading artificial black smudge | Use layered multi-stop shadows (`0 1px 2px rgba(...)`, `0 4px 12px rgba(...)`) with low opacity. |
| **Monotonous spacing** | `p-6` and `gap-4` used across every container | Use differentiated spacing scale: 8px tight, 16px medium, 32px-48px between major visual zones. |
| **Default font inertia** | Using Inter/Arial/Roboto for every brief | Select typefaces matching the brand voice (e.g. Plus Jakarta Sans, Geist, Instrument Serif, Outfit). |

---

## 🎨 Surface & Token Craft Recipes

### 1. Tinted Neutrals for Surfaces That Need Them

This recipe suits many reading and task surfaces. It is not a ban on intentional black-and-white, phosphor, neon or other style-specific palettes. Preserve the chosen language while verifying painted contrast and state meaning.
```css
/* Bad */
background-color: #000000;
color: #888888;

/* Good: OKLCH Warm Dark Lacquer */
--surface-ground: oklch(12% 0.008 95);
--surface-panel:  oklch(16% 0.010 95);
--text-primary:   oklch(94% 0.004 95);
--text-muted:     oklch(70% 0.008 95);
```

### 2. Discrete Hairline Borders
```css
/* Tactile 1px border with subtle transparency */
border: 1px solid oklch(94% 0.004 95 / 0.08);
```

### 3. Layered Multi-Stop Shadows
```css
/* Refined depth rather than blurry smudges */
box-shadow: 
  0 1px 2px oklch(0% 0 0 / 0.12),
  0 4px 12px oklch(0% 0 0 / 0.08);
```

## 🧱 Icon and Asset Sets: Constraints Live in a Test

When a set of icons or other small assets is drawn by hand or generated by a model,
the constraints are encoded in a structural test, not only in the prompt that asked
for them:

- State them as checkable facts: viewBox size, one filled path, no background shape,
  no stroke, gradient, opacity or transform, the single paint value that lets the host
  recolor it. A background rectangle slips past a visual glance on one theme and shows
  on the next.
- Generate several candidates, keep the simplest, then review at the real size and on
  both a light and a dark theme. Generated paths are valid XML more often than they
  are consistent: weight, corner and margin are judged side by side.
- Draw inspired glyphs rather than trace a trademarked logo when the set is not the
  owner's.

## Reference and Commercial Evidence

When adopting screenshots, URLs or recordings, use [reference evidence and adoption](references/reference-evidence-and-adoption.md) to separate observations, inferences and unknowns, preserve semantic tokens and document claim and asset evidence. Keep legal interpretation with the compliance owner.

## Consumer Contracts and Accessibility Exercises

For component-library changes, use [consumer contract verification](references/consumer-contract-verification.md) to resolve unknown classes, obsolete exceptions and invalid compatibility baselines. For high-contrast controls and retained loading information, use [forced-colors and motion exercises](references/forced-colors-motion-exercises.md). These are verification procedures, not new automatic framework gates.
