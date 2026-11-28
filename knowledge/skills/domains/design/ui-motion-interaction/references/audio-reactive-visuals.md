# Live audio-reactive visuals and interface sounds

Use this reference when a browser effect reads live audio, or a committed
interface action adds an optional sound. Use
[scroll-driven playback](../../ui-scroll-driven-motion/references/canvas-image-sequence.md)
for silent visual scrubbing and
[deterministic motion rendering](../../deterministic-motion-rendering/SKILL.md)
for fixed-timeline audio and video export.

## Choose the input and clock

- Use `getByteFrequencyData()` or `getFloatFrequencyData()` for spectrum
  magnitude. Each bin is spaced at `sampleRate / fftSize` Hz. Group bins for
  a small display instead of drawing every bin. Specify the range and whether
  each band shows its peak or average.
- Use `getFloatTimeDomainData()` for a waveform or an RMS envelope. An
  `AnalyserNode` does not detect beats. For beat-like pulses, define an
  onset rule on calibrated energy or spectral change, add a minimum interval
  between detections, and check silence, noise and changing tempo. Use source
  timestamps for known, authored beats.
- Schedule audio with `AudioContext.currentTime`. Use display timestamps only
  to throttle drawing. Allocate analysis arrays once, choose an FFT size based
  on the frequency/time trade-off, and tune smoothing for the signal. Verify
  a known signal and the return to silence with the configured smoothing.
- For an existing media element, call `createMediaElementSource()` once per
  element. Test source loading and CORS on the deployed origin. Keep a viable
  native playback route if graph setup fails. Once a media element feeds the
  graph, native controls alone cannot restore output from a suspended
  context. Restore an independently playable element if necessary.

## Own activation, fallbacks and teardown

Keep first load silent. Use a labeled playback control and call
`AudioContext.resume()` and, for a media element, `play()` from the user
gesture before waiting on unrelated work. Reuse a context for the mounted
owner. Handle constructor, resume and playback failures. Publish playing state
and schedule drawing only after playback has started. Keep controls usable,
offer retry, and retain either independently playable native controls or a
static textual equivalent when enhancement is unavailable.

Make pause and stop control playback and drawing together. On pause, retain
the current position when resume is offered. On stop, reset position. Cancel
scheduled draw work and pending starts using an ownership check or request
revision after each asynchronous boundary. On unmount, cancel callbacks and
cues, dispose listeners, disconnect the graph, and close the context if the
component owns it. A stale promise must never restart the disposed effect.

Reduced motion and sound preference are separate. Keep a static equivalent
visible and stop drawing when the preference changes to reduce, while leaving
explicitly started audio under the listener's control. Skip draws when hidden;
decide audio continuation separately for the product. Keep keyboard-operable
controls and convey meaningful results in text without announcing each frame.
See [web accessibility](../../../../engineering/practices/web-accessibility-wcag/SKILL.md#-captions-transcripts-and-audio).

## Attach an optional interface cue to the committed action

Keep sound off until opt-in. Attach one cue at the semantic commit point, not
to a pointer event or a speculative state change. Publish visible and
programmatic confirmation even when muted or playback fails. Give cues their
own gain and a short envelope, and choose a bounded concurrency policy. Stop
active cues on mute, stop, and teardown. The example replaces a currently
playing cue with the newest one and routes cues around the sample analyser.

## Run the example

Open [frequency-visualizer.html](../examples/frequency-visualizer.html) in a
browser with a local web server. The original signal consists of a one-second
440 Hz sine tone followed by 0.75 seconds of silence, with a short fade at the
tone endpoints. The fixture caps paint work at 30 updates per second and
aggregates only the lower 4 kHz into 24 bars. The fixture uses a fixed-size
canvas and leaves the sample description available in every state.

Check these observable outcomes:

1. On first load, no context, source, or cue starts. Start produces a band near
   440 Hz, followed by silence. Pause freezes playback position and hides the
   graph. Resume continues from that position. Stop resets it.
2. Add a marker before opt-in, during sound-enabled playback, and after
   muting. Each action increments the count once. Only the sound-enabled
   playback action starts a cue. Repeat closely to check the one-voice limit.
3. Force a resume or playback rejection and retry successfully. Delay a start,
   stop or detach the owner before resolving it, and check that no stale
   source or callback starts. Teardown while a cue is active stops it.
4. Change the reduced-motion preference during playback in both directions.
   Verify drawing stops and returns, audio remains controllable, and the
   description remains visible. Disable enhancement and verify the static
   path. For a real media input, also check native playback recovery if used.

## Compatibility sources

Check the target browser with a fresh session because permission, activation
history, embedding policy and platform behavior can affect playback. Feature
detection establishes that an API exists. A successful play or resume and
observed output establish that it works for the current session. Review date
2026-11-27. [Web Audio analyser and context model](https://webaudio.github.io/web-audio-api/#AnalyserNode),
[Chrome autoplay policy](https://developer.chrome.com/blog/autoplay),
[WebKit media autoplay policy](https://webkit.org/blog/7734/auto-play-policy-changes-for-macos/).

When the controls are separate, keep Play focusable with `aria-disabled="true"` during the pending promise and guard repeat activation in the handler. Transfer focus only when the currently focused control becomes disabled after a committed state change. On a rejected start, keep Play available for retry. Verify with Tab, Enter and Space from a fresh page.

Listen for audio context state changes during playback. If the browser suspends or interrupts the audio clock, pause the visualizer, retain the playback offset, and show an explicit Resume action. Treat a closed graph as unavailable and recreate it only on a new user action.
