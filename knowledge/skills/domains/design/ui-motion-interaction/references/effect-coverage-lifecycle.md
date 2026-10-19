# Effect Coverage and Lifecycle

Use when decoration, reveal effects or progress indicators do not cover the expected region, or survive a change of context.

## Declare the coordinate space

| Owner | Expected coverage | Failure to test |
| --- | --- | --- |
| Viewport | Visible window or embedded viewport | Unexpected movement with document content |
| Scroll container | Its visible region, with the intended clipping | Overlay escaping the owner or hiding controls |
| Complete content | The full content extent as it grows | Scanlines or texture ending after one screen |
| Narrative scene | Its active/pinned interval | Hidden scene retaining work or blocking navigation |

Measure the actual owner and its containing block. Application chrome can reduce usable height even when the outer viewport size is correct. A percentage minimum height can exceed the space left by a sibling header. Check nested containers, orientation changes and content added after mounting.

## Layering and interaction

Inspect the stacking-context ancestry of the overlay and the element it overlaps. Transform, opacity and positioned layers can change which numeric order matters. Test the intersection point after scrolling; a header or progress bar can exist with correct dimensions and still be covered.

Decorative layers normally do not capture pointer interaction. Check keyboard focus and labels as well as pointer access. Do not raise every layer to an arbitrary large number: assign ordering relative to the intended owner and dialogs.

## Ownership contract

Record what mounting creates, how resize/content changes update it, what pauses offscreen or in an inactive view, and what teardown removes. Include observers, event handlers, timers, animation callbacks, drawing resources, nodes and temporary style changes. Teardown must be safe after partial initialization and a superseded asynchronous request.

Preserve complete static content when motion is reduced or the optional effect fails. An early return may skip decoration; it must not skip essential state or navigation. Test context changes while effects are still initializing, not only after a completed animation.

## Performance evidence

A callback interval includes scheduling and synchronization; it is not the processing cost of a rendered frame. Aggregate main-thread time, long-task observations, frame timing and retained-resource measurements answer different questions. Report the workload, environment, supported measurements and baseline. Software rendering or missing timing capability limits a hardware-performance claim.

Run representative idle, scroll and interruption workloads, then repeated mount/teardown cycles. Stable object counts and noisy heap totals are useful signals, not proof of zero retained resources. Attribute a regression before changing an effect to meet a budget.
