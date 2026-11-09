# Theming and Accessibility

Map the selected release's theme API to the project's existing semantic tokens. Preserve intentional brand and density decisions. Check the complete surface stack rather than replacing only a background token.

Distinguish explicit light/dark selection from automatic system preference. Verify how the installed release resolves automatic mode, stores an explicit preference and applies the initial appearance before paint. Do not assume an attribute alone implements preference resolution.

For RTL, select the release's matching directional assets and confirm direction-aware utility behavior. Review navigation placement, table overflow, icon meaning and keyboard reachability using representative translated content. Do not require a direction the product does not support.

Reuse:
- [Theme surface states](../../../domains/design/color-ui-systems/references/theme-surface-states.md).
- [Accessibility practice](../../../engineering/practices/web-accessibility-wcag/SKILL.md).
- [Forced-colors and motion exercises](../../../engineering/practices/ui-design-craftsmanship/references/forced-colors-motion-exercises.md).

A built-in dark theme, contrast helper or motion media query does not establish accessibility conformance. Check rendered foreground/background pairs, focus, names, keyboard operation and retained information in the actual supported states.

Sources reviewed 2026-10-28:
- [Color modes](https://github.com/tabler/tabler/blob/7ec9589ba63da56be273a12d9da9b9dfce59f5ee/docs/content/ui/getting-started/color-modes.mdx).
- [Accessibility source cases](https://github.com/tabler/tabler/blob/7ec9589ba63da56be273a12d9da9b9dfce59f5ee/core/scss/layout/_accessibility.scss).
