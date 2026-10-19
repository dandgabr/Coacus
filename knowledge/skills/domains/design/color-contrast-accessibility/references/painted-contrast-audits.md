# Painted Contrast Audits

Use this reference when a token-level contrast check disagrees with what someone can read, or when text sits on a layered surface. A calculation, a rendering sample and a conformance assessment have different scopes.

## Establish the actual foreground

Inspect the delivered font size and weight, color, text fill, opacity and relevant ancestor opacity. A separate text-fill declaration can override the visible ink while computed color appears correct. Consider selection, placeholder, focus, hover and visited states where the component exposes them. Wait for the intended font and appearance to be applied.

Inspect generated text and visible decorative glyphs as well as ordinary text nodes. An accessibility-hidden element can still paint pixels; exclude it from a visual audit only for an explicit visual reason. Conversely, content in a semantically hidden view is not evidence that the active view is readable.

## Reconstruct or sample the background

For solid layers, composite alpha in paint order and stop traversing when an opaque layer fully covers what lies behind it. Do not reject the whole measurement merely because a gradient exists behind an opaque card. Pseudo-elements, overlays, filters, blend modes and images can make a simple ancestor-color calculation insufficient.

For complex backgrounds, inspect the region actually behind the text in the relevant states and frames. Multiple samples help triage; a median can miss a small bad region and cannot establish the worst case. Preserve extreme or suspicious samples for investigation instead of discarding them as noise.

When making a background-only capture, hide the text's paint without changing dimensions, line breaks, layout or `currentColor`-driven surfaces. A broad color reset can erase the very background being measured. Compare at least one unmodified viewport rendering to confirm the measurement setup did not change the subject.

## Report the claim you measured

- Record the appearance, component/state, viewport or container, font readiness, revision, method and limitations.
- Distinguish a failing pair from an unsupported composition or skipped region. A skip never counts as a passing contrast pair.
- A source-pattern warning is not a measured ratio. A computed ratio on two tokens is not proof those tokens paint the component.
- Text over an image or moving layer needs examination of relevant worst regions/states; one attractive screenshot does not prove the full sequence.
- Apply the relevant text/non-text requirements and their exemptions accurately. Do not turn every decorative divider into an essential control boundary or treat placeholders as decoration.

## Repair without erasing the style

Choose the narrowest repair that makes the content readable: correct the applied ink, bind the intended surface, adjust translucency, add a local reading plate, change position or reduce competing decoration. A checkered or textured backdrop can remain if the reading surface works. Do not maximize every ratio indiscriminately or rely on glow alone to rescue unreadable body text.

## Test the auditor

Use controlled counterexamples: readable tokens with an overriding dark text fill; a gradient behind an opaque card; a tiny low-contrast region missed by a median; and a visible glyph marked accessibility-hidden. Verify the auditor detects the intended failure and preserves a known-readable control case. Structural tests of the auditor do not substitute for inspection of the delivered interface.
