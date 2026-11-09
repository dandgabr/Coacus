# Rendered Interface Oracles and Fixtures

Use when source-level checks pass while users still encounter unreadable, clipped, obscured or unreachable interface content. Choose assertions for observable requirements, not for the current implementation's markers.

## Define the claim and matrix

Derive the inventory from authoritative product data. Select relevant appearances, states, routes, views, dimensions, orientation, zoom, language and movement settings. Say which axes are exhaustive, sampled or not exercised. Fixed inventory counts belong only to a deliberately frozen contract or synthetic fixture.

Test dimensions around breakpoints and a wide/short case as well as tall/narrow. Measure the visible content owner after application chrome and insets. Fitting the outer document width is weaker than fitting a card's content, preserving sibling separation or aligning the intended columns.

Different checks establish different things:

| Oracle | Establishes | Does not establish |
| --- | --- | --- |
| Token/schema check | Defined values and shape agree | Values actually paint a component |
| Computed styles | Winning declarations at the sampled state | Complete composed pixels or legibility |
| Geometry/visibility | Bounds, intersections and reachable regions | Historical authenticity or complete contrast |
| Painted sampling | Measured regions at the sampled rendering | Every gradient region, frame or conformance criterion |
| Interaction replay | Outcome under the exercised input | Other input methods or all runtime races |
| Human visual review | Judgment for the inspected cases | Exhaustive inspection of unreviewed cases |

## Keep the measurement subject intact

Wait for the requested stylesheet/appearance, font readiness and intended state. Reset incidental hover for rest-state comparisons. A fixed delay alone does not demonstrate readiness.

Measure geometry before adapting the page for screenshots. Expanding a scroll container can change scene height, resize observers, sticky positioning and the painted background. Use unmodified viewport captures when those conditions matter; disclose changes made for a full-content image. Hiding text for background sampling must not change its dimensions or erase `currentColor` surfaces.

Semantic hidden views are different from visible decoration excluded from the accessibility tree. Audit filters must follow the claim: an accessibility-hidden glyph can still have a visual contrast defect.

## Assert relationships and output

Check the child against its owning surface and the available visible region. Check all relevant edges, sibling spacing, column relationships and whether the final control in tall content can be reached. Document bounded intentional overlap instead of allowing all overflow for an expressive style.

For reveal/progress effects, test actual dimensions, paint and the overlap point with fixed controls. State classes and event delivery alone can pass when a chart has zero height or a menu covers its progress indicator. Check effect teardown when its owner changes.

For async state, replay out-of-order completions and preserve a valid positive control. A guard that always refuses an update can pass a rejection-only test. Test the success path as well as the blocked stale response.

## Test the oracle with controlled defects

Use single changes whose failure is known: zero-height bars, a semantic hidden override, old dark text fill on a new dark surface, identical switch-state paint, a covered progress indicator or an invalid evidence root. Restore each change before the next run.

Record which assertion detects each defect and which mutants survive. Do not report a prose hypothesis as an executed mutation. A source-matching assertion does not prove the same behavior as a rendered fixture.

## Fixtures and evidence lifecycle

Keep fixtures small and explicit. Candidate and approved states should be synthetic inputs where both matter, not assumptions that the real repository stays in an early pilot stage. Resolve evidence paths against the correct fixture root and preserve required evidence when copying.

Exclude unrelated screenshots, videos, dependency trees and tool state from repeated snapshots. Make scratch location configurable; distinguish quota, capacity and permission failures before changing product code. Do not inspect or delete unrelated credential-bearing tool state.

Record revision, input, method, capability, result and limitations per case. Preserve historical reports and point corrected cases at their reexecution; do not rewrite an old result to match a later approval. A skipped, unknown or unsupported case never aggregates to a pass. A clean sample is not a certification.
