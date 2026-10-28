# Forced Colors and Motion Exercises

Use the [independent fixture](../examples/interface-verification.html) to examine a masked dismiss control and a loading status. Keep existing geometry and appearance exercises available. No package or remote asset is needed.

## Positive cases

1. In ordinary and forced-colors appearances, navigate by keyboard to the dismissal trigger and close control. Verify a distinguishable focus indicator, a visible close shape or fallback, and the accessible name "Dismiss example notice".
2. Activate dismissal by keyboard. Verify the notice becomes hidden and focus returns to the trigger. Reopen it and repeat without losing keyboard reachability.
3. Under reduced motion, verify the loading text remains visible and exposed as status information. The decorative spinner may stop; the operation's meaning must remain.
4. Inspect the actual rendered control and accessibility information. Computed token values and a screenshot file alone are insufficient evidence of operability.

Use the authorized browser workflow. Record revision, appearance, viewport, forced-colors/reduced-motion settings and observed outcomes. Record unavailable emulation or assistive technology explicitly; do not claim a broader conformance result.

## Controlled defects

Inject each mutation only in the test context, confirm the relevant oracle rejects it, and restore before the next mutation.

| Defect | Discriminating observation |
| --- | --- |
| Remove both ordinary and forced-colors focus indicators from the focused close control | The rendered focus distinction is lost |
| Hide the close shape and its forced-colors fallback | The visible control loses its close affordance even though its accessible name remains |
| Hide the loading status when reduced motion is enabled | Loading information becomes unavailable rather than merely static |
| Remove the focus restoration after dismissal | Keyboard focus does not return to the trigger |

Pair every rejection with the restored positive case. Keep original dimensions when capturing evidence. These cases test a particular oracle; they do not certify the whole fixture, all forced-color palettes, assistive technologies or component libraries.

Source inspiration reviewed 2026-10-28: [Tabler accessibility cases](https://github.com/tabler/tabler/blob/7ec9589ba63da56be273a12d9da9b9dfce59f5ee/core/scss/layout/_accessibility.scss). This protocol and fixture behavior are original Coacus examples.
