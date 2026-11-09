# Canvas Image Sequences Keyed to Scroll

Frame-by-frame sequences (a product rotating, an object assembling) scrubbed by scroll position. Gate the technique first: see the "Default: No" box in [the skill](../SKILL.md). Shader effects, 3D scenes and WebGL texture streaming belong to [ui-gpu-graphics-web](../../../../engineering/practices/ui-gpu-graphics-web/SKILL.md).

---

## 1. Architecture

- One `<canvas>` inside a sticky stage; a poster `<img>` underneath it in the HTML so the first paint and the no-JS path show a real image.
- Scroll only marks the sequence dirty. One `requestAnimationFrame` callback reads progress and draws at most once per frame.
- **Never set `img.src` per scroll event.** Each change can start a network request and a synchronous decode on the main thread, and the image flickers while the next frame loads.
- Decode ahead of need with `createImageBitmap`, draw the decoded bitmap, and release bitmaps outside a sliding window with `close()`.

```html
<section class="sequence" aria-labelledby="sequence-title">
  <h2 id="sequence-title">How the hinge folds</h2>
  <div class="sequence__stage">
    <img class="sequence__poster" src="/seq/frame-000.avif" width="1280" height="720"
         alt="The laptop hinge folding from open to closed in three positions">
    <canvas class="sequence__canvas" aria-hidden="true" hidden></canvas>
  </div>
  <p class="sequence__caption">The hinge rotates 180° on a single axis and locks flat at both ends.</p>
</section>
```

The poster's `alt` and the visible caption carry the information; the canvas is marked `aria-hidden` because it repeats them. If the canvas is the only visual, give it `role="img"` and an `aria-label` that states what the sequence shows (1.1.1).

## 2. Frame loop with a sliding window

```js
const FRAME_COUNT = 120;
const WINDOW = 12;                                  // decoded frames kept on each side
const url = (i) => `/seq/frame-${String(i).padStart(3, '0')}.avif`;

const section = document.querySelector('.sequence');
const canvas = section.querySelector('canvas');
const ctx = canvas.getContext('2d');
const encoded = new Map();                          // index -> Blob (compressed, small)
const decoded = new Map();                          // index -> ImageBitmap (w × h × 4 bytes)
const controller = new AbortController();
let current = -1;
let queued = false;

function sizeCanvas() {
  const dpr = Math.min(devicePixelRatio, 2);        // cap DPR: memory grows with its square
  const { width, height } = canvas.getBoundingClientRect();
  canvas.width = Math.round(width * dpr);
  canvas.height = Math.round(height * dpr);
  current = -1;                                     // force a redraw
}

function progress() {
  const rect = section.getBoundingClientRect();
  const distance = section.offsetHeight - innerHeight;
  return Math.min(1, Math.max(0, -rect.top / distance));
}

const pending = new Set();

async function decode(i) {
  if (decoded.has(i) || pending.has(i) || !encoded.has(i)) return false;
  pending.add(i);
  try {
    decoded.set(i, await createImageBitmap(encoded.get(i)));
    return true;
  } finally {
    pending.delete(i);
  }
}

function nearestAvailable(i) {
  for (let d = 0; d < FRAME_COUNT; d += 1) {
    if (decoded.has(i - d)) return i - d;
    if (decoded.has(i + d)) return i + d;
  }
  return -1;
}

function draw() {
  queued = false;
  const target = Math.round(progress() * (FRAME_COUNT - 1));

  for (const [i, bitmap] of decoded) {               // release outside the window
    if (Math.abs(i - target) > WINDOW) { bitmap.close(); decoded.delete(i); }
  }
  for (let i = target - WINDOW; i <= target + WINDOW; i += 1) {
    if (i >= 0 && i < FRAME_COUNT) decode(i).then((added) => added && request());
  }

  const frame = nearestAvailable(target);
  if (frame === -1 || frame === current) return;
  ctx.drawImage(decoded.get(frame), 0, 0, canvas.width, canvas.height);
  current = frame;
  canvas.hidden = false;                             // poster stays until a frame is drawn
}

function request() {
  if (!queued) { queued = true; requestAnimationFrame(draw); }
}
```

Scroll and resize listeners call `request()` (passive), an IntersectionObserver stops requesting while the section is off screen, and teardown closes every bitmap, aborts pending fetches with `controller.abort()` and disconnects observers.

## 3. Memory budget

A decoded frame costs `width × height × 4` bytes, whatever the file size.

| Frame size | One decoded frame | 120 frames | Window of 25 |
| --- | --- | --- | --- |
| 1920 × 1080 | ≈ 8.3 MB | ≈ 1.0 GB | ≈ 207 MB |
| 1280 × 720 | ≈ 3.7 MB | ≈ 442 MB | ≈ 92 MB |
| 960 × 540 | ≈ 2.1 MB | ≈ 249 MB | ≈ 52 MB |

Decoding the whole sequence up front is the most common cause of crashes. Keep compressed blobs in memory, decode a window, and size frames to the displayed CSS size times the capped DPR.

**iOS:** WebKit caps total canvas memory and the system terminates a content process under memory pressure; the page then reloads, often mid-scroll. Test on a real mid-range iPhone, not only in a desktop simulator.

## 4. Loading strategy

- **Progressive preload:** fetch keyframes first (every 8th frame, then every 4th, then every 2nd, then the rest). Draw the nearest decoded frame, so scrubbing works coarsely at once and sharpens as data arrives.

  ```js
  const order = [8, 4, 2, 1].flatMap((step) =>
    Array.from({ length: FRAME_COUNT }, (_, i) => i).filter((i) => i % step === 0)
  ).filter((i, n, all) => all.indexOf(i) === n);

  async function load() {
    for (const i of order) {
      const response = await fetch(url(i), { signal: controller.signal });
      encoded.set(i, await response.blob());
      request();
    }
  }
  ```
- **Poster:** the first frame as a real `<img>` with dimensions, so layout is stable and the largest paint is not blocked on the sequence.
- **Formats:** AVIF or WebP cut transfer size; AVIF decodes more slowly, so measure decode time per frame on the target device. Pick the format once by feature test, not per frame.
- **Start late:** begin fetching when the section approaches the viewport (IntersectionObserver with a generous `rootMargin`), and skip the sequence entirely on `navigator.connection.saveData` where available.
- **Worker option:** `canvas.transferControlToOffscreen()` moves decoding and drawing into a worker; the main thread only posts progress values.

## 5. Video scrubbing instead of frames

A muted, inline `<video>` with `currentTime = progress × duration` set from the rAF loop is far smaller to download.

- Seeking lands on a keyframe and decodes forward, so long GOPs make scrubbing stutter. Encode all-intra or with a short GOP:

  ```bash
  ffmpeg -i source.mov -an -c:v libx264 -g 1 -crf 22 -pix_fmt yuv420p -movflags +faststart scrub.mp4
  ```

  `-g 1` makes every frame a keyframe (largest file, smoothest seek); `-g 5` to `-g 10` trades size for smoothness.
- Do not issue a new seek while one is pending: remember the latest target and apply it on `seeked`.
- `video.requestVideoFrameCallback()` reports when a frame is actually presented, which helps verify sync.
- Use `muted playsinline preload="auto"` and never autoplay it as a substitute for the scrub.

### Frame-exact decoding with WebCodecs

When every frame must be exact, demux the file (for example with mp4box.js), feed `EncodedVideoChunk`s to a `VideoDecoder`, draw each `VideoFrame` to the canvas and call `frame.close()` immediately; holding frames stalls the decoder's pool. Seek by resetting the decoder and decoding from the preceding keyframe. Keep the `<video>` or image path as fallback where `VideoDecoder` is missing.

| API | Support |
| --- | --- |
| `createImageBitmap` (full options) | Baseline widely available 2026-06-11 |
| `ImageBitmap.close()` | Chrome 52, Firefox 46, Safari 15 |
| `OffscreenCanvas` | Chrome 69, Firefox 105, Safari 16.4 |
| `VideoDecoder` | Chrome 94, Firefox 130, Safari 16.4 |
| `requestVideoFrameCallback` | Chrome 83, Firefox 132, Safari 15.4 |

## 6. Reduced motion and static path

Under `prefers-reduced-motion: reduce`, do not attach the frame loop. Show the poster, or two or three key stills in normal flow with captions, and collapse the tall scroll section to its natural height. The same static path serves no-JS and decode failures.

---

## Version Sources

Moving release pins in this file were resolved 2026-10-20 against web-features 3.43.0 (https://registry.npmjs.org/web-features) and MDN browser-compat-data 8.1.6 (https://registry.npmjs.org/@mdn/browser-compat-data):

- **`createImageBitmap`** (verified) — Baseline widely available 2026-06-11
- **`ImageBitmap.close()`** (verified) — Chrome 52, Firefox 46, Safari 15
- **`OffscreenCanvas`** (verified) — Chrome 69, Firefox 105, Safari 16.4
- **`VideoDecoder`** (verified) — Chrome 94, Firefox 130, Safari 16.4
- **`requestVideoFrameCallback`** (verified) — Chrome 83, Firefox 132, Safari 15.4
- **iOS canvas memory cap value** (unverified) — WebKit does not publish a stable limit; the file states the behavior, not a number
