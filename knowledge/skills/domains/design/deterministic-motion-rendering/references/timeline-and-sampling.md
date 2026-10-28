# Timeline and Sampling

Reviewed 2026-10-27. The frame-domain and evaluation contracts are original
Coacus conventions. API examples illustrate adapters, not a maintained rendering
implementation or a required library stack.

## Frame-domain convention

Declare the exact rate as numerator `p` and denominator `q`, both positive, and
an integer frame count `N`. Capture indices `0` through `N - 1`; frame start time
is `i * q / p` seconds and media duration is `N * q / p` seconds. Keep the
rational rate through export rather than substituting a rounded decimal. If
duration is the input, declare the rounding rule used to derive `N` and report
the resulting duration.

For example, `p=30000`, `q=1001`, `N=300` means indices `0..299` and a duration
of `10.01` seconds. Capturing index `300` adds an unwanted endpoint frame.
Hold the final pose intentionally within the declared frame domain when the
story needs it.

## Evaluation independent of request order

Prefer immutable scene inputs plus a function of the requested frame/time.
For a simulation, reset and replay fixed steps from a known origin or a verified
checkpoint before sampling. Checkpoints must identify their input revision and
simulation state; they cannot depend on which capture worker ran first.

A seeded mutable random stream advanced once per capture still depends on call
order. Derive stable random values from a key such as scene seed, element ID and
authored sample/event ID. Use an element key for a persistent particle position;
include a sample key only when the intended signal changes over time. A new
unrelated random value every frame can cause flicker even if it is reproducible.

Compare repeated requests `90, 0, 90` and sequential versus shuffled schedules
in the same controlled environment. Include both a changing region and a known
static region so a renderer that ignores frame input cannot pass unnoticed.

## Adapter choices

| Scene technology | Positioning recipe | Important limit |
|---|---|---|
| CSS / Web Animations | Pause controlled animations and set `currentTime = seconds * 1000` | Wait for preparation and completed paint; disable unrelated autonomous animation. |
| GSAP | Pause the timeline and call `seek(seconds, true)` | Numeric positions use seconds; event suppression defaults to true. Do not rely on skipped callbacks to initialize scene state. |
| Lottie | Pause autoplay and call `goToAndStop(sourceFrame, true)` | Map export time to authored source fps and declare subframe behavior. |
| Three.js / canvas | Assign scene/camera state from the requested time and render explicitly | Keep shader uniforms and simulation state under the same time contract; use the existing GPU skill for engine implementation. |
| Video texture | Seek to the selected source timestamp and confirm the resulting decoded/presented image | Source fps may differ; variable-frame-rate media requires timestamp-aware selection, not integer frame multiplication. |

For example, a paused WAAPI animation uses milliseconds, while a Lottie source
frame is derived from its own authored rate:

```javascript
const seconds = frame * rate.denominator / rate.numerator;
animation.pause();
animation.currentTime = seconds * 1000;
lottieAnimation.goToAndStop(seconds * sourceFps, true);
```

This snippet demonstrates units only. The project's controller must implement
readiness and capture completion, identify all active animations and validate
backward seeking. Playback clocks and autonomous callbacks must not advance the
scene while a frame is paused.

## Optional subframe sampling

Declare shutter interval, sample count and blend/color policy if motion blur is
requested. Evaluate each sample independently. Separate discrete text/cut state
from continuous motion so temporal averaging does not accidentally blend two
headlines. Review adjacent frames at cut boundaries. Subframe sampling is an
optional creative/export choice, not evidence of quality by itself.

## Sources and verification limits

- [Remotion flickering](https://www.remotion.dev/docs/flickering): repeatable images, paused output and order-independent evaluation.
- [Remotion random](https://www.remotion.dev/docs/random): a stable key produces a stable pseudorandom value.
- [WAAPI currentTime](https://developer.mozilla.org/en-US/docs/Web/API/Animation/currentTime): milliseconds, including paused animations.
- [Lottie controls](https://github.com/airbnb/lottie-web#usage): frame/time selection and subframe control.
- [FFmpeg image sequences](https://ffmpeg.org/ffmpeg-formats.html#image2): explicit input framerate.
- [GSAP seek documentation](https://gsap.com/docs/v3/GSAP/Timeline/seek%28%29/): verified during source review on 2026-10-27; numeric positions use seconds, seeking preserves paused/reversed state, and `suppressEvents` defaults to true. Verify the installed package before adopting an adapter; this is not a release pin.
