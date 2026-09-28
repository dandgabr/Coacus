---
name: "color-theory-foundations"
description: "Provides color science foundations for UI work based on perceptual color research: trichromacy and metamerism, additive vs subtractive models, why HSL lightness is perceptually broken, CIE Lab/LCh, the OKLab/OKLCH perceptual space, CAM16/HCT and wide-gamut P3, CSS Color 4/5 functions (oklch, color-mix, relative colors, color-scheme), gamut mapping and sRGB gamma. Use when choosing or converting color models, authoring ramps, or implementing modern CSS color."
---

# AI Skill: Color Theory Foundations

The science under color decisions: how humans perceive color, why the models we code in distort it, and which perceptual spaces and CSS features fix it. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Choosing a color model or space for a palette, token system or gradient.
- Authoring shade ramps or programmatic color transformations.
- Implementing `oklch()`, `color-mix()`, relative colors or wide-gamut output.
- Debugging "why did this hue shift / why is the ramp uneven".

---

## 👁️ Perception Basics

- **Trichromacy:** three cone classes — L (~560nm), M (~530nm), S (~420nm); ~6–7M cones vs ~92M rods, with S-cones only ~2% and nearly absent from the fovea. L:M ratios vary between "normal" observers, so colorimetry describes an average observer, not a person.
- **Opponent processing:** the brain derives color from cone differences (red-green, blue-yellow axes) — the basis of Lab/Oklab.
- **Metamerism:** different spectra can produce identical tristimulus responses, which is what makes RGB displays possible. Named failure modes: illuminant, observer, field-size, geometric and device metamerism. Consequence: a hex value specifies a *stimulus*, not an *appearance*.
- **Simultaneous contrast and color constancy:** perceived color shifts with its neighbors, and the visual system adapts to the illuminant. This is why Albers says color is the most relative medium in art — and why contrast must be measured, never eyeballed.

---

## 🎨 Color Models and Spaces

- **RGB (additive, screens) vs CMYK (subtractive, print):** sRGB's gamut mostly meets low-end printers but is too small for professional work, especially blue-green. CSS gamut volumes (Lab units): sRGB 0.820M, display-p3 1.233M, a98-rgb 1.310M, rec2020 2.042M, prophoto-rgb 2.896M.
- **HSL/HSV are geometric re-encodings of sRGB, not perceptual spaces.** At constant HSL L, yellow and blue "match" numerically while their perceived lightness differs by ~50 points (Oklab ≈ 0.97 vs ≈ 0.45); hue swaps silently change real lightness and can break text contrast; HSL cannot express P3. This is the `darken()` bug class.
- **CIE XYZ (1931):** device-independent tristimulus space; Y is luminance; XYZ is additive (light mixtures are predicted by sums), unlike gamma-encoded RGB.
- **CIE Lab/LCh:** the standard perceptual opponent space, but with poor hue prediction in blues — `lch()` values around hue 270–330° drift blue→purple when only lightness or chroma changes.
- **OKLab/OKLCH (Ottosson, 2020):** fixes hue linearity and lightness prediction — best-in-class lightness/chroma error, Munsell constant-chroma rings reproduce as circles, white→blue blends do not drift purple. Now Photoshop's default gradient interpolation, Unity/Godot pickers, and the CSS default for `color-mix()`. In `oklch()` 100% chroma = 0.4.
- **CAM16/HCT (Material 3):** HCT = CAM16 hue/chroma + CIELAB L* tone, viewing-condition aware; powers Material dynamic color, tonal palettes and contrast utilities.
- **Display P3 / wide gamut:** OKLCH coordinates are gamut-independent; only chroma ceilings differ per display. Spec a safe sRGB value, then raise chroma under `@media (color-gamut: p3)`.

---

## 🧮 Gamma and Luminance

- **sRGB gamma is piecewise,** not a pure power law: linearize below 0.04045 by ÷12.92, else `((v+0.055)/1.055)^2.4`.
- **Naive RGB averaging is wrong** because channels are gamma-encoded: 50% blends and opacity math operate on encoded values, which is why legacy sRGB gradients produce muddy midpoints. Mix in `oklab` (perceptual) or `xyz`/`srgb-linear` (physically additive light).
- **Luminance vs luma:** the 0.2126/0.7152/0.0722 weights apply to *linearized* channels to yield relative luminance Y; applied to encoded values they yield luma (video approximation). WCAG contrast linearizes first.

---

## 🧩 CSS Color 4/5 Features (resolved)

- **CSS Color 4** is a W3C Candidate Recommendation Draft (26 Sep 2026); it adds `lab()`, `lch()`, `oklab()`, `oklch()` and `color()` with predefined spaces (`srgb`, `display-p3`, `a98-rgb`, `prophoto-rgb`, `rec2020`, `xyz`, …).
- **Baseline status (MDN):** `oklch()` and `color-mix()` widely available since May 2023; `color-scheme` since January 2022; relative color syntax in all evergreen browsers; `light-dark()` since May 2024.
- **`color-mix(in oklab, var(--c), transparent)`** — mixing default is `oklab` with shorter hue; MDN's guidance: `xyz`/`srgb-linear` for physical light, `oklab` for even perceptual spacing, `oklch` to avoid graying out, `srgb` only for legacy parity.
- **Relative color syntax:** `oklch(from var(--accent) calc(l - 0.1) c h)` derives state variants declaratively; alpha defaults to the origin's alpha; percentages cannot be added inside `calc()` (use `@supports` compat patterns for older Safari).
- **`color-scheme: light dark`** + `<meta name="color-scheme">` opts form controls, scrollbars and system colors into the scheme — the fix for dark-mode scrollbars and load-time flashes.
- **Gamut mapping:** CSS specifies an OkLCh chroma-reduction search preserving hue and lightness; engines have historically clipped, so lint out-of-gamut values and provide P3 overrides.

---

## ⚠️ Pitfalls

- Picking colors in hex/HSL and expecting perceptual behavior; "add 10% lightness" is not a perceptual operation.
- Assuming identical `L` values are equally light across hues; assuming `lch()` hue is stable across chroma/lightness.
- Averaging or interpolating gamma-encoded colors.
- Treating hex as an appearance rather than a stimulus (metamerism: it will not match across devices/lighting).

---

## 📚 Sources

- Björn Ottosson, "A perceptual color space for image processing" (OKLab), 2020/2025 — https://bottosson.github.io/posts/oklab/
- W3C, "CSS Color Module Level 4" (CRD, 26 Sep 2026) — https://www.w3.org/TR/css-color-4/
- MDN, "`oklch()`" — https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/oklch
- MDN, "`color-mix()`" — https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/color-mix
- MDN, "Using relative colors" — https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Colors/Using_relative_colors
- MDN, "`color-scheme`" — https://developer.mozilla.org/en-US/docs/Web/CSS/color-scheme
- Sitnik & Turner (Evil Martians), "OKLCH in CSS: why we moved from RGB and HSL", 2024/2025 — https://evilmartians.com/chronicles/oklch-in-css-why-quit-rgb-hsl
- Adam Wathan, "Tailwind CSS v4.0", Jan 2025 — https://tailwindcss.com/blog/tailwindcss-v4
- Material Foundation, "Material Color Utilities" (HCT/CAM16) — https://github.com/material-foundation/material-color-utilities
- Wikipedia, "Cone cell" — https://en.wikipedia.org/wiki/Cone_cell
- Wikipedia, "Metamerism (color)" — https://en.wikipedia.org/wiki/Metamerism_(color)
- Wikipedia, "sRGB" — https://en.wikipedia.org/wiki/SRGB

---

## 🔗 Integration with Other Skills

- For palette building on these foundations, see [color-harmony-palettes](../color-harmony-palettes/SKILL.md).
- For the accessibility math, see [color-contrast-accessibility](../color-contrast-accessibility/SKILL.md).
- For token and theming architecture, see [color-ui-systems](../color-ui-systems/SKILL.md).
