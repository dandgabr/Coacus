---
name: "ui-style-linear-saas"
description: "Provides the Linear-style SaaS UI style (2019-present): dark-first, low-chroma neutrals, perceptually uniform theming, tight Inter typography, subtle borders and keyboard-driven density, covering LCH-based theme generation, three-variable theming, soft glow accents and speed as aesthetic. Use when designing modern B2B SaaS product UI and marketing pages that signal craft, focus and performance."
---

# UI Style: Linear SaaS

The dominant look of 2020s product-led SaaS: calm, dark-first, neutral surfaces, Inter-family type, hairline borders, a single restrained accent and an interface that feels fast. Named for Linear, whose redesign write-ups are the primary documentation. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Designing issue trackers, analytics, CRM, dev and productivity SaaS with dense, keyboard-driven workflows.
- Building theme systems generated from few inputs (base, accent, contrast).
- Auditing a product that looks generic after copying this aesthetic.

---

## 🕰️ Definition and Timeline

- Linear published its UI redesign (part II) on March 28, 2024: LCH color space for theme generation, themes reduced from 98 variables to three (base, accent, contrast), Inter Display for headings with Inter for body, more contrast, less chroma for a "more neutral and timeless appearance"; a six-week project.
- The look then spread across startup sites (dark hero, soft radial glow, bento cards).
- Difference from [ui-style-dark-mode-first](../ui-style-dark-mode-first/SKILL.md): that skill is theming strategy; this is a full visual language. Versus [ui-style-glassmorphism](../ui-style-glassmorphism/SKILL.md) and [ui-style-aurora-mesh-gradient](../ui-style-aurora-mesh-gradient/SKILL.md): glow here is subtle and structural, not decorative spectacle. Versus [ui-style-brutalist-monochrome](../ui-style-brutalist-monochrome/SKILL.md): softer radii, atmospheric light, less exposed scaffolding.

---

## 🎨 Visual DNA

- **Type:** Inter (variable) with a display cut for headings; 12-14px UI sizes, tight tracking at large sizes, medium weights (450-600); tabular numerals.
- **Color:** near-black or off-white neutrals with a very slight hue; one accent (indigo/violet typical); semantic status colors desaturated; surfaces stepped by lightness, not shadow.
- **Edges:** 1px low-alpha borders (`rgba(255,255,255,.08)` on dark), radii 6-12px.
- **Light:** faint top gradient, radial glow behind hero, inner highlight on cards; no heavy drop shadows.
- **Layout:** sidebar plus list/detail panes, command palette, compact rows, icon at one stroke weight.
- **Marketing:** large product screenshots, bento grids, product-as-hero.

---

## 🖱️ Interaction and Motion

- Speed as aesthetic: optimistic updates, instant navigation, 100-200ms ease-out transitions.
- Keyboard everywhere: `Cmd/Ctrl+K` palette, single-letter shortcuts with visible hints, hover reveals row actions.
- Motion is purposeful and small (fade, 4-8px slide, layout transitions); no parallax or bounce.

---

## 🛠️ Implementation Notes

```css
:root {
  --bg: oklch(0.99 0.002 270); --surface: oklch(0.97 0.003 270);
  --text: oklch(0.2 0.01 270); --muted: oklch(0.45 0.01 270);
  --border: oklch(0.2 0.01 270 / .1); --accent: oklch(0.55 0.2 275);
}
[data-theme="dark"] {
  --bg: oklch(0.16 0.004 270); --surface: oklch(0.2 0.005 270);
  --text: oklch(0.96 0.003 270); --muted: oklch(0.7 0.01 270);
  --border: oklch(1 0 0 / .08); --accent: oklch(0.7 0.16 275);
}
.card { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; }
.btn-primary { background: var(--accent); color: oklch(0.99 0 0); transition: filter .15s ease-out; }
.btn-primary:hover { filter: brightness(1.08); }
:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
@media (prefers-contrast: more) { :root { --border: oklch(0.2 0.01 270 / .5); } }
```

- Derive themes from three inputs (base, accent, contrast); a perceptually uniform space such as LCH or OKLCH keeps lightness steps equal across hues. Linear used LCH; OKLCH here is a substitute for CSS support.
- Verify accent-on-surface and white-on-accent in both themes; recompute with the contrast variable for a high-contrast theme.

---

## ♿ Accessibility

- 1.4.3: muted gray text on dark surfaces is the usual failure; 4.5:1 for body, including placeholders and disabled-looking secondary text.
- 1.4.11: low-alpha borders (8% white) fail 3:1 for input and button edges; strengthen control borders, keep decorative dividers faint.
- 2.4.7 and 2.4.11: visible focus, not hidden by sticky headers; command palette needs focus management and `aria-activedescendant` or equivalent (4.1.2).
- 2.1.1 and 2.1.4: single-key shortcuts must be remappable or disableable.
- 1.4.4/1.4.10: 12px dense UI must zoom and reflow.
- Honor `prefers-color-scheme`, `prefers-contrast` and `prefers-reduced-motion`; glow and layout animations stop when reduced.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** B2B SaaS, developer products, project management, analytics, fintech tooling.
- **Caution:** consumer apps needing warmth; low-end devices (blur/glow cost).
- **Avoid:** brands that must differentiate (this look is now the default), audiences with low vision needs.

---

## ⚠️ Pitfalls

- Cargo-cult clones: dark hero, purple glow, bento, Inter; indistinguishable from competitors.
- Contrast loss from "subtle everything"; glow overuse hurting performance.
- Keyboard shortcuts with no discoverability or conflicts with assistive technology.
- Copying marketing polish without the actual speed that justifies it.

---

## 📚 Sources

- Karri Saarinen et al., "How we redesigned the Linear UI (part II)" (Linear), Mar 28, 2024 — https://linear.app/now/how-we-redesigned-the-linear-ui
- Vercel, "Geist: Colors" (role-based color scales; comparable system) — https://vercel.com/geist/colors
- W3C, "Understanding SC 1.4.11: Non-text Contrast" — https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
- MDN, "prefers-reduced-motion" (Mozilla) — https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
- Linear's earlier 2019-2022 redesign dates and the "Linear look" spread across startup sites: `unverified`.

---

## 🔗 Integration with Other Skills

- For conformance discipline, see [web-accessibility-wcag](../../../engineering/practices/web-accessibility-wcag/SKILL.md).
- Sibling styles: [ui-style-dark-mode-first](../ui-style-dark-mode-first/SKILL.md), [ui-style-bento-grid](../ui-style-bento-grid/SKILL.md), [ui-style-micro-interactions](../ui-style-micro-interactions/SKILL.md), [ui-style-calm-quiet-ui](../ui-style-calm-quiet-ui/SKILL.md), [ui-style-brutalist-monochrome](../ui-style-brutalist-monochrome/SKILL.md).
