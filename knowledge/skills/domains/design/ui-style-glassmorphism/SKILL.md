---
name: "ui-style-glassmorphism"
description: "Provides the glassmorphism UI style (2020-2023): frosted translucent panels with backdrop blur, hairline light borders and vivid blurred backgrounds, covering visual DNA, CSS techniques (backdrop-filter, rgba layers, @supports fallbacks), backdrop-root pitfalls, contrast strategy and OS lineage from Aero and iOS 7 to Big Sur, Mica and visionOS. Use when designing or building frosted-glass interfaces or evaluating the style for a product."
---

# UI Style: Glassmorphism

Frosted-glass surfaces — translucent panels blurring the content behind them, edge-lit with hairline borders — named by Michał Malewicz (December 2020), institutionalized by macOS Big Sur (November 2020), Windows 11 Mica (2021) and visionOS (2023). Synthesized from verified design-history research; see Sources.

---

## 🧭 When to Activate

- Building overlays, players, sidebars or modals that float over rich backgrounds.
- Evaluating whether glass surfaces fit a product's brand and accessibility bar.
- Debugging `backdrop-filter` behavior or contrast failures on glass.

---

## 🕰️ Definition and Timeline

- Lineage: Windows Vista/7 Aero Glass (2006–2009), iOS 7 frosted translucency (2013).
- Named as a web trend by Malewicz (Dec 2020); hype accelerated by macOS Big Sur (Nov 12, 2020) and seeded by Alexander Plyuto's 2020 Dribbble glass shots.
- Peaked 2021–2022 as a web fad; institutionalized as an OS material (Mica, visionOS) rather than dying.

---

## 🎨 Visual DNA

- **Surfaces:** 5–20% white (or dark) rgba panels over vivid blurred background blobs.
- **Depth:** one soft ambient drop shadow + 1px light inner border (white at 20–40%).
- **Blur:** 10–30px backdrop blur, often plus `saturate(150–180%)`.
- **Shapes:** large continuous corner radii (~12–32px); floating layered cards.
- **Typography:** neutral grotesques (SF Pro/Helvetica class) — decoration lives in the surface, not the type.
- **Iconography:** thin-line icons; **layout:** floating panels over gradient or photo backdrops.

---

## 🖱️ Interaction and Motion

- Subtle scale/translate on hover; springy Apple-class easing; parallax background blobs; glass panes for modals and sheets. Keep blur static — animating `backdrop-filter` is expensive.

---

## 🛠️ Implementation Notes

```css
.glass {
  background: rgb(255 255 255 / 0.15);
  backdrop-filter: blur(20px) saturate(180%); /* + -webkit- prefix for Safari */
  border: 1px solid rgb(255 255 255 / 0.25);
  box-shadow: 0 8px 32px rgb(0 0 0 / 0.35);
  border-radius: 20px;
}
```

- Gate with `@supports (backdrop-filter: blur(1px))`; fall back to a near-opaque background.
- `backdrop-filter` is Baseline 2024; Safari historically needed the prefix.
- **Backdrop roots:** any ancestor with `filter`, `opacity < 1`, `mask`, `mix-blend-mode` or `will-change` on those properties stops the blur — the classic "why doesn't it blur" bug (MDN).
- `prefers-reduced-transparency` exists but is experimental — do not rely on it as the only fallback.

---

## ♿ Accessibility

- Text contrast over glass is **unpredictable** — the backdrop is whatever scrolls underneath; WCAG 1.4.3 (4.5:1 / 3:1) cannot be guaranteed on a variable background. Raise pane opacity under text areas, keep body copy off glass, and test against the lightest and darkest backdrop states.
- Large blur areas cost GPU on low-end devices; Windows Mica falls back to solid color under High Contrast, transparency-off and Battery Saver — copy that honesty.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** ephemeral layers (modals, nav bars, mini-players) over controlled backgrounds; brand moments.
- **Avoid:** body-text containers, data-dense UI, user-controlled backgrounds, light-mode enterprise tools.

---

## ⚠️ Pitfalls

- "Gray mush" when opacity is raised to fix contrast — the effect dies; decide which you are optimizing for.
- Legibility drifts across scroll positions; 2021's web became interchangeable glass cards.

---

## 📚 Sources

- Michał Malewicz, "Glassmorphism in User Interfaces" (Hype4/UX Collective), 2020 — https://hype4.academy/articles/design/glassmorphism-in-user-interfaces
- Apple, "macOS Big Sur is here", Nov 12, 2020 — https://www.apple.com/newsroom/2020/11/macos-big-sur-is-here/
- Microsoft, "Mica material — Windows apps", Microsoft Learn — https://learn.microsoft.com/en-us/windows/apps/design/style/mica
- MDN, "`backdrop-filter`" (Baseline 2024; backdrop roots) — https://developer.mozilla.org/en-US/docs/Web/CSS/backdrop-filter
- MDN, "`prefers-reduced-transparency`" — https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-transparency
- W3C, "Understanding SC 1.4.3 Contrast (Minimum)", WCAG 2.1 — https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html

---

## 🔗 Integration with Other Skills

- For the underlying UX craft, see [ui-ux-principles](../../../engineering/practices/ui-ux-principles/SKILL.md).
- For conformance discipline, see [web-accessibility-wcag](../../../engineering/practices/web-accessibility-wcag/SKILL.md).
- Sibling styles: [ui-style-neumorphism](../ui-style-neumorphism/SKILL.md), [ui-style-claymorphism](../ui-style-claymorphism/SKILL.md), [ui-style-aurora-mesh-gradient](../ui-style-aurora-mesh-gradient/SKILL.md), [ui-style-frutiger-aero](../ui-style-frutiger-aero/SKILL.md).
