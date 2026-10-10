---
name: "ui-presentation-slides"
description: "Provides design engineering patterns for high-impact presentation slides, technical pitch decks, and executive briefings. Covers 16:9 canvas geometry, the Assertion-Evidence framework (Alley, 2003), typographic scale budgets for distance legibility, visual storytelling layouts (split comparison, metric hero, timeline progressions, system architecture breakdowns), high-contrast data visualization, and cognitive load minimization. Use when designing presentation decks, slide decks, pitch decks, keynote visuals, or board summaries."
tags:
  - presentation-slides
  - slide-design
  - pitch-decks
  - visual-storytelling
  - ui-design
---

# UI Presentation Slides: High-Impact Visual Decks & Technical Briefings

Presentation slides are visual cognitive aids, not reading documents. Grounded in cognitive load theory (Sweller, 1988) and the **Assertion-Evidence Framework** (Alley, 2003), high-impact slides maximize audience comprehension by pairing a complete sentence assertion with visual evidence rather than bulleted lists of text fragments.

---

## 🧭 When to Activate

- Designing presentation decks, investor pitch decks, conference talks, or keynote slides.
- Translating technical architectures or roadmaps into executive slide formats.
- Structuring board meetings, sprint demos, or product launch briefings.
- Composing slide layouts in 16:9 canvas aspect ratios (1920×1080px).
- Establishing typographic scale budgets and color contrast for large displays and projectors.

---

## 📐 Geometry & Canvas Layout Budgeting

The standard modern canvas is **16:9 widescreen**:
- **Reference Dimensions**: `1920 × 1080 px` (or scalable vector base).
- **Safety Margins**: Minimum 80px to 120px padding on all sides. Projectors and external conference monitors frequently crop or display bezels over the perimeter.
- **Visual Grid**: 12-column layout with 24-32px gutters; or 4-quadrant modular grid.

```
+-----------------------------------------------------------+
|  [Category / Tracker]                           [Slide #]  |
|                                                           |
|  ASSERTION HEADLINE: Complete Takeaway Sentence           |
|                                                           |
|  +---------------------------+ +-----------------------+  |
|  |                           | |                       |  |
|  |   VISUAL EVIDENCE         | |   SUPPORTING DATA     |  |
|  |   (Diagram, Architecture, | |   (Key Metrics,       |  |
|  |    Screenshot, Flow)      | |    Proof Points)      |  |
|  |                           | |                       |  |
|  +---------------------------+ +-----------------------+  |
|                                                           |
+-----------------------------------------------------------+
```

---

## ✍️ Typographic Scale for Distance Legibility

Slide text must be readable from the back of an auditorium or on a compressed video conference window:

| Element | Size (px / pt) | Weight | Maximum Length |
| :--- | :--- | :--- | :--- |
| **Tracker / Eyebrow** | 16-18px | Semibold (600), Uppercase | 2-4 words |
| **Assertion Headline** | 40-52px | Bold (700) | 1-2 lines (max 15 words) |
| **Section Title Slide**| 64-80px | Heavy (800) | 3-6 words |
| **Metric Hero Number** | 80-120px | Black (900), Tabular | 1-4 characters + unit |
| **Supporting Body** | 20-24px | Regular/Medium (400-500) | Short annotations only |
| **Footnotes / Sources**| 12-14px | Light/Muted (400) | 1 line at slide footer |

---

## 🏛️ Canonical Slide Archetypes

### 1. The Assertion-Evidence Slide
- **Headline**: Replaces topic phrases ("Q3 Sales") with an explicit takeaway claim ("Q3 enterprise sales expanded 44%, driven by API tier upgrades").
- **Visual Body**: Replaces text bullet points with a single dominant visual (a high-resolution diagram, flow chart, or customer quote).

### 2. Metric Showcase (The Big Number)
- **Structure**:
  - 1 to 3 dominant metric callouts arranged horizontally.
  - Large tabular number (`120px`, bold).
  - Explicit metric label (`20px`) and comparative baseline below (`+38% YoY`).
- **Best For**: Traction slides, performance benchmark gains, financial achievements.

### 3. Split Comparison (Before vs After / Problem vs Solution)
- **Structure**:
  - Two contrasting columns (`1fr 1fr`).
  - Left Column (Problem / Legacy): Muted tones, red/amber subtle accents, friction points.
  - Right Column (Solution / Modern): Brighter contrast, brand accent, streamlined architecture.
- **Best For**: Product value pitches, architectural migrations, feature replacements.

### 4. Technical Architecture & Dataflow Slide
- **Structure**:
  - Left-to-right directional flow (`Input → Processing / Model → Output / Consumer`).
  - Clear container grouping (Client boundary, Cloud infrastructure, Datastore layer).
  - High-contrast nodes connected by directional arrows with concise protocol labels (REST, gRPC, WebSocket).

### 5. Multi-Column Progression (3-Step Roadmap or Value Pillars)
- **Structure**:
  - 3 or 4 equal-width vertical cards (`1fr 1fr 1fr`).
  - Large sequence step (`01`, `02`, `03`) or feature icon at card header.
  - Bold proposition followed by concise outcome statement.

---

## 🚫 Critical Anti-Patterns in Slide Design

1. **The Wall of Bullet Points**:
   - Never place 5+ bullet points of full sentences on a slide. The audience will read ahead and ignore the presenter.
2. **Low-Contrast Gray Text**:
   - Projectors wash out subtle contrast. Ensure body text has at least `7:1` contrast ratio against the background slide color.
3. **Competing Visual Anchors**:
   - Limit each slide to **one visual focal point** (one chart, one diagram, or one stat block). Multiple equal-weight diagrams create visual chaos.
4. **Uncropped Raw Screenshots**:
   - Never paste full raw desktop screens with browser toolbars and OS menus. Crop tightly to the relevant UI element and frame it with subtle elevation or border radius.
