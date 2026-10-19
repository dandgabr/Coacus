# Independent Interface Fixture Exercises

Use [the standalone HTML fixture](../examples/interface-verification.html) when testing a rendered-interface checker or exercising guidance outside the originating product. It has no remote assets or application backend. It is an example, not a framework runner or a conformance certificate.

Set the owner element's appearance attribute to light or dark and its kind to operate, read or experience. Exercise a narrow window, a wide/short window and a tall/narrow window. Measure the owner after the explanatory chrome, not an assumed full-window height. Check that fields fit their cards and the final action in the tall form is reachable.

Inspect full-surface texture coverage, progress over the fixed menu, the visible chart bars, supported control states and the local reading plate over the checker pattern. Keep an unmodified viewport rendering as a control before any full-content capture.

## Controlled defects

Inject each defect separately in the test context, observe the discriminating assertion fail and restore the original before continuing:

| Defect | Expected oracle |
| --- | --- |
| Set chart bar heights to zero | Positive rendered dimensions fail |
| Give the reading title a dark text fill in the dark appearance | Effective foreground/background contrast fails while nominal color still passes |
| Override the inactive view's hidden display | Active-view visibility assertion fails |
| Lower progress beneath the fixed menu | The overlap point is covered despite both elements having dimensions |
| Limit the texture to one viewport | Mid/end content coverage fails |
| Make off/on switch tracks and thumb paint identical and remove thumb displacement | Distinguishable state output fails |

The examples can establish that a particular oracle detects a controlled defect. They do not render every visual style, prove a skill caused an agent's improvement, or cover every writing system, browser, assistive technology or moving gradient frame.
