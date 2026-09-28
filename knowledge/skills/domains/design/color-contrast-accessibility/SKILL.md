---
name: "color-contrast-accessibility"
description: "Provides color contrast and accessibility engineering: WCAG 2.2 thresholds (4.5:1, 3:1, 7:1, non-text 3:1), the relative-luminance and contrast-ratio math, known WCAG limitations and APCA (Lc values, WCAG 3 status), color vision deficiency types and prevalence, colorblind-safe palettes (Okabe-Ito, viridis), testing tooling and the full state matrix, plus dark-mode halation pitfalls. Use when verifying contrast, choosing accessible palettes or implementing dark mode."
---

# AI Skill: Color Contrast and Accessibility

The measurable half of color work: thresholds, math, the APCA successor, color-vision deficiency, tooling and dark-mode pitfalls. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Verifying or fixing contrast on text, controls, borders, focus rings or charts.
- Choosing colorblind-safe palettes for UI or data visualization.
- Implementing dark mode and auditing its contrast.
- Choosing between WCAG 2 ratios and APCA as the checking method.

---

## 📏 WCAG 2.2 Requirements (Recommendation, 12 Dec 2024)

- **SC 1.4.3 AA:** text ≥ **4.5:1**; large text ≥ **3:1**. Large = ≥18pt (≈24px) regular or ≥14pt (≈18.66px) bold; delivered size, not user-resized.
- **Thresholds are hard:** 4.499:1 fails; values are never rounded. Maximum possible is 21:1.
- **SC 1.4.6 AAA:** 7:1 text / 4.5:1 large.
- **SC 1.4.11 AA (non-text):** UI-component boundaries/states and meaningful graphics ≥ **3:1** against adjacent colors — input borders, checkbox checks, toggle thumbs, gradient worst point, focus rings (an author-styled ring needs 3:1; hover treatments are supplemental but must not reduce component contrast).
- **SC 1.4.1 A (Use of Color):** color must never be the only means of conveying meaning; a lightness difference yielding ≥3:1 counts as a second cue — hue-only never does.
- **Exemptions:** inactive (disabled) controls, decoration, invisible text and logotypes. But **placeholder, hover-revealed and focus text are in scope**.

---

## 🧮 The Math

- Linearize each sRGB channel (÷12.92 below 0.04045, else `((v+0.055)/1.055)^2.4`), then `L = 0.2126R + 0.7152G + 0.0722B`; contrast ratio = `(L1 + 0.05)/(L2 + 0.05)`.
- The +0.05 flare term models ambient light; ratios (not absolute luminance) are used because screens emit relative to their own range.
- **Known criticisms:** not perceptually uniform (overstates contrast for dark colors), polarity-blind (symmetric ratio misjudges light-on-dark), and spatial-ignorant (ignores font size/weight — the dominant factor in perceived contrast). The 4.5:1/3:1 figures trace to 1980s print-era standards.

---

## 🧪 APCA — the WCAG 3 Candidate

- APCA (Somers/Myndex) outputs a polarity-aware **Lc** value from a color pair; it is the candidate method for **WCAG 3.0 (Working Draft, 10 Sep 2026 — not a standard)**; use it today as a *supplement* when contracts require WCAG 2.
- **Lc semantics:** 0 to ±106; **negative Lc = light text on dark** (reverse polarity); never swap foreground/background in tools.
- **Use-case levels (reference font, bronze mode):** Lc 90 preferred body; Lc 75 minimum body (≥18px); Lc 60 non-body content; Lc 45 large/heavy text (≥36px) and pictograms; Lc 30 placeholder/disabled and large non-text; Lc 15 absolute discernible minimum. AAA-equivalent ≈ +15.
- **Why it matters:** perceptual uniformity, explicit polarity asymmetry (fixes dark-mode over-prescription), and font size/weight awareness. Dark mode should use *less* effective contrast, not more.

---

## 👓 Color Vision Deficiency

- **Types:** red-green dominates — deuteranomaly is the most common single form (mild, greens redder), then protanomaly, deuteranopia, protanopia; blue-yellow (tritan) is rarer; complete CVD is rare.
- **Prevalence:** about **1 in 12 men** (NEI); ~8% of Caucasian males, 5% Asian, 4% African (red-green); ~5% of the world population has some CVD. The ~0.5% women figure was unverifiable this session [unverified].
- **Lightness is preserved** in common CVD — hue discrimination breaks, contrast does not. Exception: **red on black is near-invisible to protans** — avoid it.
- **Okabe-Ito palette** (8 colors, unambiguous to CVD and non-CVD): black, orange, sky blue, bluish green, yellow, blue, vermilion, reddish purple. Pair with redundant coding — shape, pattern, labels, position, line style.
- **Simulators show which colors are confusable, not what CVD users see** — never judge people by simulator output.

---

## 🔬 Tooling and Workflow

- **WebAIM Contrast Checker** for quick ratios; **TPGi Colour Contrast Analyser** for on-screen eyedropper sampling, alpha support and a built-in CVD simulator.
- **DevTools:** Chrome's color picker shows the ratio with AA/AAA badge lines and suggests a passing color; CSS Overview and the Issues panel find contrast problems; the Rendering panel emulates vision deficiencies. Firefox Accessibility Inspector simulates protanopia/deuteranopia/tritanopia/achromatopsia and contrast loss.
- **Automated scans catch static pairs only.** Low contrast is the most common web accessibility failure — **83.9% of the top million home pages** (avg 34 instances/page) per the WebAIM Million 2026. Manual work is mandatory for text over images/gradients, alpha compositing, dynamic states and non-text contrast.
- **Sampling discipline:** prefer computed CSS values; fully composite alpha before judging; test on a standard sRGB display (retina/P3 previews hide anti-aliasing damage).
- **Test the whole state matrix:** default, hover, focus, active, disabled, error, visited — plus placeholder.

---

## 🌙 Dark-Mode Pitfalls

- **Halation:** pure white on pure black overshoots for large/bold text; darken the light element (e.g., #eee–#ddd) instead of maximizing contrast.
- **WCAG 2 misleads in dark mode** (overstates near-black contrast) — verify with a perceptually-aware tool and test rendered anti-aliased values; gray-on-gray is the classic false pass.
- Elevation via lightness, not shadow; honor `prefers-color-scheme` and `prefers-contrast`.
- Avoid red on dark for text and semantic non-text (protanopia).

---

## ⚠️ Pitfalls

- Checking only the default state; ignoring focus-ring and border contrast.
- Using pure-red/pure-green data encodings; color-only status dots.
- Treating an automated scan pass as conformance; testing only the average of a gradient.

---

## 📚 Sources

- W3C WAI, "Understanding SC 1.4.3 Contrast (Minimum)" — https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
- W3C WAI, "Understanding SC 1.4.11 Non-text Contrast" — https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
- W3C WAI, "Understanding SC 1.4.6 Contrast (Enhanced)" — https://www.w3.org/WAI/WCAG22/Understanding/contrast-enhanced.html
- W3C WAI, "Understanding SC 1.4.1 Use of Color" — https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html
- W3C, "WCAG 3.0", Working Draft, 10 Sep 2026 — https://www.w3.org/TR/wcag-3.0/
- Andrew Somers, "The Easy Intro to the APCA Contrast Method", 2022 — https://git.apcacontrast.com/documentation/APCAeasyIntro
- Inclusive Reading Technologies, "ARC: Bronze Simple Mode" — https://readtech.org/ARC/tests/bronze-simple-mode/
- Andrew Somers, "The Realities and Myths of Contrast and Color", Smashing Magazine, Sep 2022 — https://www.smashingmagazine.com/2022/09/realities-myths-contrast-color/
- WebAIM, "The WebAIM Million", 2026 — https://webaim.org/projects/million/
- WebAIM, "Color Contrast Checker" — https://webaim.org/resources/contrastchecker
- TPGi, "Colour Contrast Analyser (CCA)" — https://www.tpgi.com/color-contrast-checker/
- National Eye Institute, "Types of Color Vision Deficiency", 2023/2025 — https://www.nei.nih.gov/learn-about-eye-health/eye-conditions-and-diseases/color-blindness/types-color-vision-deficiency
- Okabe & Ito, "Color Universal Design", 2002/2008 — https://jfly.uni-koeln.de/color/
- MDN, "Web Accessibility: Understanding Colors and Luminance" — https://developer.mozilla.org/en-US/docs/Web/Accessibility/Guides/Colors_and_Luminance
- Chrome for Developers, "Make your website more readable" — https://developer.chrome.com/docs/devtools/accessibility/contrast

---

## 🔗 Integration with Other Skills

- For the color science behind luminance, see [color-theory-foundations](../color-theory-foundations/SKILL.md).
- For conformance practice, see [web-accessibility-wcag](../../../engineering/practices/web-accessibility-wcag/SKILL.md).
- For chart and data-viz palettes, see [color-ui-systems](../color-ui-systems/SKILL.md).
