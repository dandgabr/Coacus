# Scroll Narrative Modes

Choose the interaction the product needs before choosing its implementation.

| Mode | What scroll controls | Native expectation |
| --- | --- | --- |
| Continuous reading | Position in a normal document | Content remains directly scrollable |
| Threshold reveal | Appearance or annotation at a boundary | Scrolling remains continuous |
| Pin and scrub | A scene's visual state through an interval | Input can continue through the interval |
| Stepped presentation | Movement between discrete scenes | Each scene has a clear reachable destination |

A long page is not necessarily a deck. A scene class changing is not proof that the requested transition is visible. Prefer native scrolling, anchoring and snap behavior when they meet the requirement.

## If a stepped presentation is explicitly requested

Define scene alignment against the available area below fixed controls. Keep the selected scene and progress coherent after resize, interruption and orientation changes. Check progress endpoints and visible ordering over the menu in every appearance.

If native snap alone does not provide the specified gesture behavior, keep any additional wheel/key handling local to the active narrative. Normalize input units where the platform distinguishes pixels, lines or pages; handle momentum without trapping the user or swallowing a new gesture after resize.

Preserve zoom gestures, horizontal input, editable fields, range controls, nested scrolling tables and default behavior outside the narrative. A scene taller than the usable viewport must remain scrollable to its final controls before advancing. Provide keyboard and touch access to every scene; do not make information depend on a wheel event.

## Static and reduced-motion paths

Expose the full information without requiring scrubbed animation, forced timing or a transition to finish. Use an appropriate static sequence or immediate navigation for the product. Verify that actions below the fold remain reachable. Leaving a snap rule in place is not by itself proof of an accessible static path.

## Acceptance

Exercise forward/back gestures, keyboard navigation, a scene larger than the screen, focus inside a field, resize mid-transition and switching away from the narrative. Assert scene placement, visible output, progress layering and cleanup. Preserve a continuous-reading control case so a rule does not turn every article into slides.
