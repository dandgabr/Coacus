---
name: "color-data-visualization"
description: "Provides color for data visualization and charts: colormap taxonomy (sequential, diverging, cyclic, qualitative), perceptually uniform maps (viridis family) and why jet is banned, colorblind-safe categorical palettes (Okabe-Ito, tol), encoding rules (never color alone, limited categories, ordered lightness), gradient interpolation in oklab, chart contrast on light/dark, and data-viz token families. Use when choosing chart colors, building data-viz palettes or auditing dashboards for accessibility."
---

# AI Skill: Color for Data Visualization

Chart color is functional, not decorative: it encodes data, so it follows perceptual and accessibility rules rather than brand taste. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Choosing colors for charts, maps, heatmaps or dashboards.
- Building a categorical or sequential palette for a product's data viz.
- Auditing existing charts for color accessibility.
- Integrating chart colors into a design-token system.

---

## 🗺️ Colormap Taxonomy (Moreland's classification)

- **Sequential:** ordered data with a monotonic lightness ramp (low→high). Use for magnitude, density, counts.
- **Diverging:** two hues meeting at an unsaturated neutral midpoint; use only when there is a meaningful center (change, deviation, correlation).
- **Cyclic:** values that wrap (angles, phase, time-of-day); the two ends must match.
- **Qualitative:** unordered categories; hues chosen to be maximally distinguishable, no implied order.
- Mixing categories is the most common chart-color error: a rainbow across ordered data destroys the perceived order.

---

## 🌈 Perceptual Maps

- **viridis** (van der Walt & Smith, BIDS, 2015) and its kin — magma, inferno, plasma, cividis — are perceptually uniform in CAM02-UCS *and* in grayscale, robust under CVD simulation, and CC0-licensed; viridis became Matplotlib's default in 2.0.
- **jet is explicitly discouraged:** wildly non-monotonic lightness creates false boundaries and hides real ones.
- Uniform maps also survive grayscale printing and low-quality projectors — a good smoke test for any palette.
- Categorical alternative: **ColorBrewer**-style sets and Paul Tol's qualitative schemes are designed for maximum separation at small counts.

---

## 🎨 Categorical and CVD-Safe Palettes

- **Okabe-Ito (8 colors):** black, orange, sky blue, bluish green, yellow, blue, vermilion, reddish purple — unambiguous to colorblind and non-colorblind viewers; the default recommendation for categorical data. Available in Matplotlib as `okabe_ito`.
- **Red+green is the most dangerous pairing** (red-green CVD is the most common form, ~5–8% of male populations depending on ancestry) — avoid it in every chart, not just status indicators.
- **Limit categories:** beyond ~7–8 hues, discrimination collapses; group small categories into "other", facet, or switch to position/labels instead of more colors.
- **Ordered categories** (e.g., severity levels) should use an ordered ramp, not categorical hues.
- **Redundant coding:** pair color with shape, line style, direct labels, or position; put labels on the graphic rather than in a distant legend; use vermilion instead of pure red; thick lines and bold fonts help color-coded items.

---

## 🧮 Gradients and Interpolation

- Interpolate in a perceptual space: CSS `<gradient>` supports `in oklab` / `in oklch` (and hue methods `shorter/longer/increasing/decreasing`); legacy sRGB interpolation passes through muddy midpoints and unintended hues (blue→white via purple).
- Alpha is premultiplied in CSS gradients, avoiding gray fringing — but alpha compositing must be fully resolved before contrast checks.
- Heatmap legends must be readable: label the scale, state units, and ensure the ramp's endpoints are distinguishable under CVD simulation.

---

## 🌗 Charts in Light and Dark Themes

- Re-tune the palette per theme; do not invert it. Surface steps change the contrast budget, and a hue that passes on white often fails on dark gray.
- Charts on dark surfaces: avoid saturated colors at maximum luminance (halation); desaturate and let the mid-tones carry.
- Contrast rules still apply: graphical objects required to understand content need **3:1** against adjacent colors (WCAG 1.4.11); text in charts needs 4.5:1 / 3:1 (1.4.3).
- Gradient/area fills must be checked at the **worst point**, not the average.

---

## 🧱 Tokens for Data Viz

- Keep a **separate data-viz token family** from chrome tokens: Primer ships 16 data-viz hues, each with `emphasis` (fill/line) and `muted` (background/area) variants, tuned per theme. A brand palette is not a chart palette.
- Name by role and order (`data-viz-categorical-1..8`, `data-viz-sequential-*`), not by hue — then themes can remap without renaming.
- Ship the palette as constants consumable by charting libraries (themeable chart themes), and document the encoding order so downstream charts stay consistent.

---

## ⚠️ Pitfalls

- Rainbow/jet on sequential data; too many categorical colors; red+green pairs.
- Color-only encoding with no redundant cue; legends remote from series.
- Reusing brand or UI status colors as chart colors (and vice versa).
- Checking contrast on the average gradient color instead of the worst.

---

## 📚 Sources

- Matplotlib, "Choosing Colormaps" — https://matplotlib.org/stable/users/explain/colors/colormaps.html
- BIDS, "mpl colormaps" (viridis origin), 2015 — https://bids.github.io/colormap/
- Okabe & Ito, "Color Universal Design", 2002/2008 — https://jfly.uni-koeln.de/color/
- MDN, "`<gradient>` CSS type" — https://developer.mozilla.org/en-US/docs/Web/CSS/gradient
- Björn Ottosson, "A perceptual color space for image processing" — https://bottosson.github.io/posts/oklab/
- Primer, "Color primitives" (data-viz token family) — https://primer.style/product/primitives/color/
- W3C WAI, "Understanding SC 1.4.11 Non-text Contrast" — https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html

---

## 🔗 Integration with Other Skills

- For CVD prevalence and contrast math, see [color-contrast-accessibility](../color-contrast-accessibility/SKILL.md).
- For palette construction, see [color-harmony-palettes](../color-harmony-palettes/SKILL.md).
- For token architecture, see [color-ui-systems](../color-ui-systems/SKILL.md).
- For visualization design broadly, see [data-intensive-systems](../../../data/data-intensive-systems/SKILL.md).
