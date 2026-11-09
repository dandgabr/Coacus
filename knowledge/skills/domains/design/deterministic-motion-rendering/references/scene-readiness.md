# Scene Readiness

Use this reference when scene preparation or frame evaluation depends on
asynchronous resources. Reviewed 2026-10-27. The readiness contract below is an
original Coacus convention; linked API documentation establishes the underlying
mechanisms.

## Required resources, explicit outcomes

Create a scene-specific inventory: font identities and weights, image files,
data snapshots, video segments, textures and other renderer resources. Give
each required item a ready condition, timeout and actionable failure message.
Capture only after required conditions succeed. Record optional substitutions
as creative decisions rather than silently accepting missing resources.

- Await `document.fonts.ready`, then verify the required font faces loaded and
  are actually used. Completion of the font set alone does not prove an intended
  font succeeded or that a fallback is acceptable.
- Await each image's `decode()` and handle rejection. Include CSS backgrounds
  and masks in the inventory; waiting only for document image elements misses
  them. Use explicit preload/decode paths where needed.
- Freeze external data into an identified input snapshot. A live request per
  frame can change the scene and make parallel workers disagree.
- Confirm video media timestamps and texture upload completion after seeking.
  A requested `currentTime` is not proof of the image actually presented.
- Wait for required scene compilation/resource preparation through the chosen
  renderer's supported mechanisms. Page load, network idleness and a fixed
  sleep do not prove GPU or media readiness.

The export controller may use a clock to enforce a preparation deadline; that
clock must not determine animation state. Timeouts fail the relevant operation
and identify the resource. They must not convert an incomplete scene into a
passing capture.

## Acceptance probes

Delay a required font and image independently, then make each unavailable.
Confirm that capture waits in the first case and reports the named failure in
the second. Seek video backward as well as forward and inspect the actual
presented timestamp/frame. Exercise these with the intended capture tool and
assets; a reasoning evaluation cannot establish that the barriers ran.

## Sources

- [FontFaceSet.ready](https://developer.mozilla.org/en-US/docs/Web/API/FontFaceSet/ready): font loading and layout completion.
- [Image decoding](https://developer.mozilla.org/en-US/docs/Web/API/HTMLImageElement/decode): decoding promise and failure handling.
- [Video frame callback](https://developer.mozilla.org/en-US/docs/Web/API/HTMLVideoElement/requestVideoFrameCallback): presented media timestamp evidence; callback timing alone does not guarantee frame-accurate extraction.
- [Remotion render barriers](https://www.remotion.dev/docs/delay-render): explicit labeled barriers and timeout handling as comparative evidence, without requiring Remotion.
