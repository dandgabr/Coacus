# Rendered Interface Verification

Use these checks after changing a design system, a multi-view surface, a scroll-driven effect, or a published UI. Verify what the browser renders, not only whether the source parses or a state class appears.

## Trace structure before styling

- Read the rendered component tree and confirm that each CSS selector and observer target matches the real nesting. Count the matched scenes or controls against the intended content; wrappers and hidden tabs often invalidate direct-child selectors.
- Check spacing between sibling sections as well as gaps inside grids and cards. A component can have well-spaced children while touching the next section.

## Measure responsive boundaries

- Check a narrow phone, a wider phone, a tablet or breakpoint edge, and a desktop viewport. Include the smallest supported width when the layout claims to be responsive.
- Include orientation and available height: a wide, short window can fail while a tall window at another width works. Subtract application chrome, fixed headers and container insets from the usable area. In an embedded panel, the owner container can be more restrictive than the browser viewport.
- Measure each control against its owning visual surface and the visible stage or viewport. Check all four edges and horizontal overflow. If rotation or optical alignment intentionally crosses a boundary, document the element, expected offset, and why the overlap preserves readability and hit-target access; reject clipping, obscured labels, and unreachable hit targets.
- Check buttons, links, fields, charts, and decorative media in every active view and representative theme variants. Do not let hidden elements pass as valid visible controls.
- Compare related columns, sibling spacing, internal padding, baselines and reading measure. A form stranded below a short column or a header touching the edge can fit the viewport while still violating the intended composition. Let long words and translated headings wrap or resize within their real container; clipping is not a typography repair.

## Verify appearances and semantic state

Trace the winning paint declarations as well as tokens. Check the complete surface stack and important control states using [theme surfaces](../../../../domains/design/color-ui-systems/references/theme-surface-states.md) and [painted contrast](../../../../domains/design/color-contrast-accessibility/references/painted-contrast-audits.md). A brighter canvas does not establish readable cards, fields or tables.

Style rules must respect semantic visibility: switching a view should expose the intended view, not leave an inactive panel visible because an appearance forces its display mode. Check keyboard focus and effects in hidden views too.

Compare stacking contexts when a progress indicator, menu or overlay covers another element. A larger layer number in a nested context may still be below its sibling. Verify the visible overlap point in every supported appearance, not just each element's separate computed style.

## Preserve the subject while capturing it

Wait for the selected appearance, relevant stylesheet, fonts and intended animation state. Remove incidental hover before comparing rest states. A semantic hidden state and accessibility-hidden decoration require different filtering.

Record geometry before any screenshot-only adaptation. Expanding a scrolling container can change viewport-sized scenes and resize observers; making overflow visible can expose the page's unrelated background. Prefer viewport captures or a method preserving the relevant dimensions. State what any full-content capture changes and confirm representative unmodified viewport output.

Use an inventory-derived coverage matrix and identify sampled axes explicitly. Test the measurement itself with known bad cases such as zero-height bars, overridden hidden state or an unreadable inherited surface. A screenshot file or a successful event is not an acceptance oracle.

For a small product-independent control and known defects, use [interface fixture exercises](interface-fixture-exercises.md). Keep its browser-backed results separate from source checks and reasoning-only skill evaluations.

## Prove interactive output

- For scroll-driven scenes, scroll through the content and assert that the active scene changes and each scene produces its intended visible effect. For opacity-based reveals, check opacity; for progress indicators with defined endpoints, check both endpoints. Verify that animated content has nonzero rendered dimensions; a state class alone does not prove that a chart or illustration is visible. The scene mechanics and their acceptance checks live in [ui-scroll-driven-motion](../../../../domains/design/ui-scroll-driven-motion/SKILL.md).
- Verify effect cleanup when changing views or themes, and confirm that `prefers-reduced-motion` exposes the information without requiring animation.
- For dialogs with explicit **Accept** and **Cancel** choices, stage preference changes until acceptance. Cancel, Escape, and the close control should discard pending changes unless the product explicitly defines a different save model.
- Assert user-visible outcomes and dimensions, not only class names or event completion. When adding automated regression coverage, seed a failure such as zero-height chart bars or a hidden action row and confirm the check catches it.

## Verify published assets

When a CDN or edge cache serves the site, check the deployed preview or live HTML and the CSS, JavaScript, and dynamically loaded modules that it references. Confirm that the responses contain the intended revision for that deployment; propagate an asset version through dynamic imports when stale cached assets can mix old behavior with new markup. Run this check after the preview or deployment is available; a successful build or deployment status alone does not prove edge freshness.

## Bound verification to the change

Select representative surfaces, shared consumers and failure boundaries from the actual change. A clipped-label repair needs its owner container, relevant width and zoom, text expansion and affected shared controls; it does not require rediscovering the brand or testing every possible combination. A system-wide token change justifies broader consumer coverage.

For each selected case record the expected user-visible outcome, evidence and revision, then mark it observed, not run, or not applicable with a reason. State unavailable browsers/devices and residual uncertainty. Follow authorized local automation capabilities; do not claim cross-engine coverage from a single engine. Include reflow and zoom where the changed content can fail.

Keep source/schema checks, reasoning-only behavior evaluations and actual browser/media/network observations separate. None alone certifies general conformance. Operational tracker checks belong to [consent automation](../../../../security/grc/consent-dsr-automation/references/runtime-consent-and-erasure.md).

Sources reviewed 2026-10-27: [WAI reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html), [involving users](https://www.w3.org/WAI/test-evaluate/involving-users/), and [lab versus field evidence](https://web.dev/articles/lab-and-field-data-differences). Offline export cadence does not establish live input responsiveness; do not add telemetry automatically to obtain evidence.

## Component-library compatibility

Before comparing working and released output, validate the same fixture against the pinned baseline using [consumer contracts](consumer-contract-verification.md). An invalid baseline stops regression classification. Verify dynamic class families and the owning scope before treating an exception as obsolete.
