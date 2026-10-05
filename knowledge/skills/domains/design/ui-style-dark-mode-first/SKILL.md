---
name: "ui-style-dark-mode-first"
description: "Provides the dark mode first UI style (2019-present): dark-native interface design with desaturated accents, tonal elevation and halation-aware typography, covering the platform timeline (Mojave, iOS 13, Android 10), prefers-color-scheme engineering, OLED economics and the NN/g research verdict on polarity. Use when designing dark-native products or implementing robust light/dark theming."
---

# UI Style: Dark Mode First

Dark-native interface design — products designed dark from the start rather than ported: dark-gray surfaces (never naive pure black), desaturated accents, elevation expressed as lightness, halation-aware typography. Platform dark modes 2016–2019 normalized it; "dark mode first" products followed 2019–present. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Designing dark-native products (developer tools, media, OLED-first apps).
- Implementing robust `prefers-color-scheme` theming with user override.
- Evaluating dark-mode claims (eye strain, battery) against the research.

---

## 🕰️ Definition and Timeline

- Windows 10 dark theme (2016) → **macOS Mojave** (announced WWDC Jun 4, 2018; released Sep 24, 2018 — first full-system macOS dark mode with public API) → **iOS 13** (Sep 19, 2019, system-wide with auto switching) → **Android 10** (Sep 2019). CSS `prefers-color-scheme` shipped 2019, Baseline-wide January 2020. Developer tools were dark-native long before.

---

## 🎨 Visual DNA

- **Surfaces:** dark grays (e.g. `#121212`-class), not pure black for non-OLED contexts; Material guidance: elevation communicated by progressively lighter surface tones.
- **Color:** desaturated/darkened brand accents to preserve contrast; error/success colors lightened.
- **Type:** light-on-dark with increased line-height; halation (bloom) makes light text glow — weights often reduced.
- **Icons:** filled ↔ outline swaps (iOS 13 behavior); monochrome symbol fonts adapt automatically.
- **Imagery:** dimmed photos (70–80% brightness layers); shadows invisible on dark — depth via tint.

---

## 🖱️ Interaction and Motion

- Theme-switch cross-fades; sunrise/sunset auto-toggling; dimmed night animations; OLED pure-black variants.

---

## 🛠️ Implementation Notes

```css
:root { color-scheme: light dark; }
@media (prefers-color-scheme: dark) {
  :root { --surface: #121212; --text: #e6e6e6; --accent: #8ab4f8; }
}
```

- `color-scheme: light dark` + `<meta name="color-scheme">` fixes UA widgets/scrollbars; `light-dark()` for inline dual values.
- JS: `matchMedia('(prefers-color-scheme: dark)')` + `change` listener; **persist user override over system default**.
- Avoid transparent black PNGs on tinted dark surfaces; swap assets via `<picture>`/`currentColor`.
- OLED economics: white at full brightness ≈ 6× the power of black (2016 Pixel measurement); Google confirmed dark-mode battery savings (Nov 2018).

---

## ♿ Accessibility

- NN/g verdict (Budiu, Feb 2020): for normal-vision users **light mode wins on visual acuity, proofreading and glanceable reading** (Piepenbrock 2013; Dobres 2017); dark mode helps mainly cloudy-ocular-media users (Legge 1985, cataract). Recommendation: **offer the toggle, never force dark**. Watch halation on thin weights; re-tune data-viz palettes per theme.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** developer/creator tools, media consumption, OLED-first mobile apps, long-session reading (with a light option).
- **Avoid:** forcing dark on everyone; marketing/print-heritage brands; colored data-viz without re-tuned palettes.

---

## ⚠️ Pitfalls

- Forced dark-mode extensions create artifacts; forgotten hardcoded colors; contrast math broken by desaturation; "flash of wrong theme" before hydration.

---

## 📚 Sources

- Raluca Budiu, "Dark Mode vs. Light Mode: Which Is Better?", NN/g, Feb 2, 2020 — https://www.nngroup.com/articles/dark-mode/
- MDN, "`prefers-color-scheme`" (Baseline Jan 2020) — https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-color-scheme
- "Dark mode", Wikipedia — https://en.wikipedia.org/wiki/Dark_mode
- "macOS Mojave", Wikipedia — https://en.wikipedia.org/wiki/MacOS_Mojave
- "iOS 13", Wikipedia — https://en.wikipedia.org/wiki/IOS_13
- Chris Welch, "Google confirms dark mode is a huge help for battery life on Android", The Verge, Nov 8, 2018 — https://www.theverge.com/2018/11/8/18076502/google-dark-mode-android-battery-life
- Material Design dark theme guidance — https://m3.material.io

---

## 🔗 Integration with Other Skills

- Sibling styles: [ui-style-material-you](../ui-style-material-you/SKILL.md), [ui-style-aurora-mesh-gradient](../ui-style-aurora-mesh-gradient/SKILL.md), [ui-style-cyberpunk-hud](../ui-style-cyberpunk-hud/SKILL.md).
- For theming tokens, see [frontend-developer](../../../roles/frontend-developer/SKILL.md).
- Newer sibling styles: [ui-style-tactile-brutalism](../ui-style-tactile-brutalism/SKILL.md), [ui-style-linear-saas](../ui-style-linear-saas/SKILL.md).
- Related -punk styles: [ui-style-cyberpunk](../ui-style-cyberpunk/SKILL.md), [ui-style-lunarpunk](../ui-style-lunarpunk/SKILL.md).
