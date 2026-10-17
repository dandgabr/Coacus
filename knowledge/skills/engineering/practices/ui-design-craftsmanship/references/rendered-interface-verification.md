# Rendered Interface Verification

Use these checks after changing a design system, a multi-view surface, a scroll-driven effect, or a published UI. Verify what the browser renders, not only whether the source parses or a state class appears.

## Trace structure before styling

- Read the rendered component tree and confirm that each CSS selector and observer target matches the real nesting. Count the matched scenes or controls against the intended content; wrappers and hidden tabs often invalidate direct-child selectors.
- Check spacing between sibling sections as well as gaps inside grids and cards. A component can have well-spaced children while touching the next section.

## Measure responsive boundaries

- Check a narrow phone, a wider phone, a tablet or breakpoint edge, and a desktop viewport. Include the smallest supported width when the layout claims to be responsive.
- Measure each control against its owning visual surface and the visible stage or viewport. Check all four edges and horizontal overflow. If rotation or optical alignment intentionally crosses a boundary, document the element, expected offset, and why the overlap preserves readability and hit-target access; reject clipping, obscured labels, and unreachable hit targets.
- Check buttons, links, fields, charts, and decorative media in every active view and representative theme variants. Do not let hidden elements pass as valid visible controls.

## Prove interactive output

- For scroll-driven scenes, scroll through the content and assert that the active scene changes and each scene produces its intended visible effect. For opacity-based reveals, check opacity; for progress indicators with defined endpoints, check both endpoints. Verify that animated content has nonzero rendered dimensions; a state class alone does not prove that a chart or illustration is visible.
- Verify effect cleanup when changing views or themes, and confirm that `prefers-reduced-motion` exposes the information without requiring animation.
- For dialogs with explicit **Accept** and **Cancel** choices, stage preference changes until acceptance. Cancel, Escape, and the close control should discard pending changes unless the product explicitly defines a different save model.
- Assert user-visible outcomes and dimensions, not only class names or event completion. When adding automated regression coverage, seed a failure such as zero-height chart bars or a hidden action row and confirm the check catches it.

## Verify published assets

When a CDN or edge cache serves the site, check the deployed preview or live HTML and the CSS, JavaScript, and dynamically loaded modules that it references. Confirm that the responses contain the intended revision for that deployment; propagate an asset version through dynamic imports when stale cached assets can mix old behavior with new markup. Run this check after the preview or deployment is available; a successful build or deployment status alone does not prove edge freshness.
