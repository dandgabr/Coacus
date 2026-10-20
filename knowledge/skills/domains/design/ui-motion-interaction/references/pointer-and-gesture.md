# Pointer and Gesture Recipes

Use when building pointer-reactive decoration (magnetic controls, tilt and glare, spotlight, cursor follower, ripple, image trail) or direct-manipulation gestures (drag, swipe, fling, rubber-band). Each recipe gives the minimal correct mechanism and the pitfalls that break it. Timing values, spring presets and interruption rules live in [motion-timing-engines.md](motion-timing-engines.md); accessibility obligations live in the `🎞️ Motion and Animation` section of [web-accessibility-wcag](../../../../engineering/practices/web-accessibility-wcag/SKILL.md). Link to them instead of restating values here.

## Global gating

Pointer-reactive effects assume a precise hovering pointer. Touch, pen-without-hover, keyboard and switch users never trigger them, so the effect must be pure enhancement: the control works, reads and shows state without it.

```css
/* Base: static, complete, every input. */
.fx-magnetic__inner, .fx-tilt__card { transform: none; }

@media (hover: hover) and (pointer: fine) and (prefers-reduced-motion: no-preference) {
  /* Pointer-reactive styles only here. */
}
```

```js
const fineHover = matchMedia(
  '(hover: hover) and (pointer: fine) and (prefers-reduced-motion: no-preference)'
);
let teardown = null;
function sync() {
  teardown?.();
  teardown = fineHover.matches ? mountPointerEffects() : null; // returns a cleanup function
}
fineHover.addEventListener('change', sync);
sync();

// Read a duration token (defined in motion-timing-engines.md) in milliseconds.
function motionMs(token) {
  const raw = getComputedStyle(document.documentElement).getPropertyValue(token).trim();
  const n = parseFloat(raw);
  return Number.isNaN(n) ? 0 : raw.endsWith('ms') ? n : n * 1000;
}
```

Durations below are the duration tokens (`--motion-feedback`, `--motion-state`, `--motion-layout`, `--motion-narrative`) and easing tokens (`--ease-enter`, `--ease-exit`) from [motion-timing-engines.md](motion-timing-engines.md); script reads them through `motionMs()` so CSS and JavaScript stay on one scale.

Rules for every recipe:

- Filter by `event.pointerType === 'mouse'` inside handlers as well; hybrid devices match `(pointer: fine)` while the user is touching.
- Animate only `transform` and `opacity` on the moving node. Write custom properties or transforms once per frame from a `requestAnimationFrame` callback, never directly from `pointermove` (it can fire several times per frame).
- Cache geometry (`getBoundingClientRect()`) on `pointerenter` and invalidate it on `scroll`/`resize`; reading layout on every move forces synchronous layout.
- Keep the hit area fixed. Move an inner wrapper or a pseudo-element, never the element that receives the pointer events.
- Every mount returns a cleanup that removes listeners, cancels the frame loop and resets inline styles.
- Reduced motion (Coacus house policy, WCAG technique C39): drop spatial movement and keep a static or colour/opacity state cue.

## Magnetic button

The label drifts toward the pointer by a fraction of the offset from the control centre, then springs back on exit.

```html
<button class="fx-magnetic" type="button">
  <span class="fx-magnetic__inner">Send</span>
</button>
```

```js
function magnetic(btn, strength = 0.3) {          // 0.2–0.4× of the offset
  const inner = btn.querySelector('.fx-magnetic__inner');
  const duration = motionMs('--motion-state') / 1000; // GSAP takes seconds
  const xTo = gsap.quickTo(inner, 'x', { duration, ease: 'power3' });
  const yTo = gsap.quickTo(inner, 'y', { duration, ease: 'power3' });
  let rect = null;
  const enter = (e) => { if (e.pointerType === 'mouse') rect = btn.getBoundingClientRect(); };
  const move = (e) => {
    if (!rect) return;
    xTo((e.clientX - (rect.left + rect.width / 2)) * strength);
    yTo((e.clientY - (rect.top + rect.height / 2)) * strength);
  };
  const leave = () => { rect = null; xTo(0); yTo(0); };
  const invalidate = () => { rect = null; };
  btn.addEventListener('pointerenter', enter);
  btn.addEventListener('pointermove', move);
  btn.addEventListener('pointerleave', leave);
  addEventListener('scroll', invalidate, { passive: true });
  return () => {
    btn.removeEventListener('pointerenter', enter);
    btn.removeEventListener('pointermove', move);
    btn.removeEventListener('pointerleave', leave);
    removeEventListener('scroll', invalidate);
    gsap.set(inner, { x: 0, y: 0 });
  };
}
```

`gsap.quickTo()` reuses one tween per property and retargets it on each call, so it is cheap inside `pointermove`. With Motion, drive the same offset through a spring (`spring.snap` from [motion-timing-engines.md](motion-timing-engines.md)) so the return carries velocity.

Pitfalls:

- Translating the `<button>` itself moves its hit area under the pointer, which fires `pointerleave`, which snaps it back, which fires `pointerenter`: a jitter loop. Only the inner wrapper moves.
- A proximity field larger than the control needs a padded, invisible wrapper as the listener, not a document-wide `pointermove` that measures every magnet each frame.
- Keep the offset small enough that the label never leaves the visible background or the focus ring; offsets above roughly 0.4× read as the control fleeing the pointer.
- Never move the control on focus; keyboard users get the normal focus indicator only.

## 3D tilt with glare

Register the rotation as typed custom properties so CSS can transition them; script only writes target angles. The outer wrapper is the fixed, unrotated hit area that receives pointer events; only the inner card rotates.

```html
<div class="fx-tilt">                      <!-- listener: fixed hit area, carries perspective -->
  <article class="fx-tilt__card">…</article> <!-- rotates; never receives the geometry reads -->
</div>
```

```css
@property --rx { syntax: '<angle>'; inherits: false; initial-value: 0deg; }
@property --ry { syntax: '<angle>'; inherits: false; initial-value: 0deg; }
@property --gx { syntax: '<percentage>'; inherits: false; initial-value: 50%; }
@property --gy { syntax: '<percentage>'; inherits: false; initial-value: 50%; }

.fx-tilt { perspective: 900px; }
.fx-tilt__card { position: relative; isolation: isolate; border-radius: 16px; overflow: clip; }

@media (hover: hover) and (pointer: fine) and (prefers-reduced-motion: no-preference) {
  .fx-tilt__card {
    transform: rotateX(var(--rx)) rotateY(var(--ry));
    transition: --rx var(--motion-state) var(--ease-enter), --ry var(--motion-state) var(--ease-enter);
  }
  .fx-tilt__card::after {         /* glare layer */
    content: '';
    position: absolute; inset: 0;
    pointer-events: none;
    background: radial-gradient(circle at var(--gx) var(--gy),
      rgb(255 255 255 / 0.35), transparent 55%);
    mix-blend-mode: soft-light;
    opacity: 0;
    transition: opacity var(--motion-feedback) var(--ease-enter);
  }
  .fx-tilt.is-tilting .fx-tilt__card::after { opacity: 1; }
  .fx-tilt.is-tilting .fx-tilt__card { will-change: transform; }
}
```

```js
function tilt(wrapper, maxDeg = 6) {              // cap 4–8°
  const card = wrapper.querySelector('.fx-tilt__card'); // typed properties do not inherit: write on the card
  let rect = null, frame = 0, px = 0.5, py = 0.5;
  const paint = () => {
    frame = 0;
    card.style.setProperty('--ry', `${(px - 0.5) * 2 * maxDeg}deg`);
    card.style.setProperty('--rx', `${(0.5 - py) * 2 * maxDeg}deg`);
    card.style.setProperty('--gx', `${px * 100}%`);
    card.style.setProperty('--gy', `${py * 100}%`);
  };
  const enter = (e) => {
    if (e.pointerType !== 'mouse') return;
    rect = wrapper.getBoundingClientRect();     // unrotated box: stable while the card tilts
    wrapper.classList.add('is-tilting');        // will-change only while hovering
  };
  const move = (e) => {
    if (!rect) return;
    px = (e.clientX - rect.left) / rect.width;
    py = (e.clientY - rect.top) / rect.height;
    frame ||= requestAnimationFrame(paint);
  };
  const leave = () => {
    rect = null; px = py = 0.5; paint();
    wrapper.classList.remove('is-tilting');
  };
  const invalidate = () => { if (rect) rect = wrapper.getBoundingClientRect(); };
  wrapper.addEventListener('pointerenter', enter);
  wrapper.addEventListener('pointermove', move);
  wrapper.addEventListener('pointerleave', leave);
  addEventListener('scroll', invalidate, { passive: true, capture: true });
  addEventListener('resize', invalidate);
  return () => { /* remove listeners, cancelAnimationFrame(frame), clear properties */ };
}
```

Pitfalls:

- Listening on the rotating element itself moves its edges under a stationary pointer: near a corner the pointer falls off the rotated box, `pointerleave` resets the tilt, the box swings back under the pointer and `pointerenter` fires again. The unrotated wrapper keeps the hit area and the measured rect fixed.
- `inherits: false` keeps descendants from recomputing styles when the angle changes; it also stops a nested tilt card from inheriting the parent's rotation.
- Without `@property`, `--rx` is an untyped token: the transition snaps instead of interpolating.
- Put `perspective()` inside the transform (or `perspective` on the parent); without it rotation looks like a flat skew.
- Rotated text is resampled and blurs; keep the cap at 4–8° and test small text at 1× device pixel ratio.
- `will-change` held permanently on a grid of cards promotes every card to a layer; add it on `pointerenter`, remove it on `pointerleave`.
- `overflow: clip` on the card plus a rounded corner keeps the glare inside the shape; the glare layer needs `pointer-events: none` so it never steals clicks from links in the card.
- Check contrast of text under the brightest glare position, not only at rest.

## Spotlight and torch

A radial highlight follows the pointer: as a border glow, a surface tint, or a torch that reveals a hidden layer through `mask-image`.

```css
.fx-spot { position: relative; --x: 50%; --y: 50%; }
.fx-spot__reveal {
  position: absolute; inset: 0;
  pointer-events: none;
  opacity: 0;
  mask-image: radial-gradient(circle 160px at var(--x) var(--y), #000 30%, transparent 100%);
  transition: opacity var(--motion-feedback) var(--ease-enter);
}
@media (hover: hover) and (pointer: fine) {
  .fx-spot:hover .fx-spot__reveal { opacity: 1; }
}
/* Keyboard parity: centre the highlight on focus. */
.fx-spot:focus-within { --x: 50%; --y: 50%; }
.fx-spot:focus-within .fx-spot__reveal { opacity: 1; }
```

```js
function spotlight(host) {
  let frame = 0, x = 0, y = 0, rect = null;
  const paint = () => {
    frame = 0;
    host.style.setProperty('--x', `${x}px`);
    host.style.setProperty('--y', `${y}px`);
  };
  const move = (e) => {
    if (e.pointerType !== 'mouse') return;
    rect ??= host.getBoundingClientRect();
    x = e.clientX - rect.left; y = e.clientY - rect.top;
    frame ||= requestAnimationFrame(paint);      // at most one write per frame
  };
  // Hand the position back to CSS: inline --x/--y would override the stylesheet
  // centre and the :focus-within rule, so remove them instead of leaving stale values.
  const clear = () => {
    cancelAnimationFrame(frame); frame = 0; rect = null;
    host.style.removeProperty('--x');
    host.style.removeProperty('--y');
  };
  const invalidate = () => { rect = null; };      // re-measure on the next move
  host.addEventListener('pointermove', move);
  host.addEventListener('pointerleave', clear);
  host.addEventListener('focusin', clear);       // keyboard focus re-centres the highlight
  addEventListener('scroll', invalidate, { passive: true, capture: true }); // any scroller
  addEventListener('resize', invalidate);
  return () => { /* remove every listener added above */ clear(); };
}
```

Pitfalls:

- Changing a gradient or mask position is a repaint of the masked layer every frame, not a compositor-only update. Keep the masked layer small, avoid stacking it under `backdrop-filter`, and measure paint time on a low-end device before shipping a page-wide torch.
- One listener on a grid container that writes `--x/--y` per card (relative to each card) is cheaper than one listener per card.
- Content revealed only under the torch is invisible to touch, keyboard and screen-magnifier users: the torch layer must be decorative, or the same content must be reachable another way. `:focus-within` parity is the minimum.
- Border-glow variants must not reduce the resting border below the non-text contrast needed to identify the control.

## Custom cursor follower

> **Default: No**
> - **Allowed when:** the follower is a decorative, additive layer on a brand or portfolio surface, the native cursor stays visible, and no task depends on it.
> - **Evidence required:** native cursor visible in every state; the focused control never entirely hidden by the follower (SC 2.4.11) and its focus indicator still visible (SC 2.4.7); follower hidden under coarse pointers, reduced motion and forced colours; frame loop stops when idle.
> - **Fallback:** the native cursor alone. Never set `cursor: none` on the page or a control: it removes the system cursor that users have sized, coloured or magnified.

```css
.fx-cursor {
  position: fixed; inset: 0 auto auto 0;
  width: 32px; height: 32px; margin: -16px 0 0 -16px;
  border-radius: 50%;
  background: #fff;
  mix-blend-mode: difference;                    /* readable over light and dark */
  pointer-events: none;                          /* never intercepts clicks */
  z-index: 2147483000;
  display: none;
}
@media (hover: hover) and (pointer: fine) and (prefers-reduced-motion: no-preference) {
  .fx-cursor { display: block; }
}
@media (forced-colors: active) { .fx-cursor { display: none; } }
```

```js
function follower(el, k = 14) {                  // k in 1/s: higher = tighter
  let x = innerWidth / 2, y = innerHeight / 2, tx = x, ty = y;
  let last = 0, frame = 0;
  const step = (now) => {
    const dt = Math.min((now - (last || now)) / 1000, 0.1);
    last = now;
    const a = 1 - Math.exp(-k * dt);             // frame-rate-independent LERP
    x += (tx - x) * a; y += (ty - y) * a;
    el.style.transform = `translate3d(${x}px, ${y}px, 0)`;
    if (Math.abs(tx - x) + Math.abs(ty - y) > 0.1) frame = requestAnimationFrame(step);
    else { frame = 0; last = 0; }                // idle: stop the loop
  };
  const move = (e) => {
    if (e.pointerType !== 'mouse') return;
    tx = e.clientX; ty = e.clientY;
    frame ||= requestAnimationFrame(step);
  };
  addEventListener('pointermove', move, { passive: true });
  return () => { removeEventListener('pointermove', move); cancelAnimationFrame(frame); };
}
```

`x += (tx - x) * 0.1` per frame is frame-rate dependent: the follower is twice as tight at 120 Hz as at 60 Hz. The exponential form `1 - exp(-k·dt)` gives the same feel at any refresh rate.

Pitfalls: a large follower over a focused control hides the focus ring (keep it small or shrink it over interactive elements); `mix-blend-mode: difference` on a layer above the whole page can flatten into an expensive full-page composite, so keep the element small; hide it when the pointer leaves the window (`pointerout` with `relatedTarget === null`).

## Ripple

A press ripple confirms the press location on a surface. It must be optional feedback; the control's state change carries the meaning.

```css
.fx-ripple-host { position: relative; overflow: hidden; isolation: isolate; }
.fx-ripple {
  position: absolute; border-radius: 50%;
  background: currentColor; opacity: 0.24;
  pointer-events: none;
  transform: scale(0);
  animation: fx-ripple var(--motion-layout) var(--ease-enter) forwards;
}
@keyframes fx-ripple { to { transform: scale(1); opacity: 0; } }
@media (prefers-reduced-motion: reduce) {
  .fx-ripple { animation: fx-ripple-fade var(--motion-feedback) linear forwards; transform: none; inset: 0; border-radius: 0; }
  @keyframes fx-ripple-fade { from { opacity: 0.16; } to { opacity: 0; } }
}
```

```js
function spawnRipple(host, x, y) {
  const r = host.getBoundingClientRect();
  const size = 2 * Math.hypot(Math.max(x, r.width - x), Math.max(y, r.height - y));
  const dot = document.createElement('span');
  dot.className = 'fx-ripple';
  dot.setAttribute('aria-hidden', 'true');
  Object.assign(dot.style, {
    width: `${size}px`, height: `${size}px`,
    left: `${x - size / 2}px`, top: `${y - size / 2}px`,
  });
  dot.addEventListener('animationend', () => dot.remove(), { once: true });
  host.append(dot);
}
host.addEventListener('pointerdown', (e) => {
  const r = host.getBoundingClientRect();
  spawnRipple(host, e.clientX - r.left, e.clientY - r.top);
});
host.addEventListener('click', (e) => {          // keyboard activation: detail === 0
  if (e.detail === 0) spawnRipple(host, host.clientWidth / 2, host.clientHeight / 2);
});
```

The ripple uses `--motion-layout`, not `--motion-feedback`: it is a spatial expansion across the whole surface, so it sits in the layout band, while the control's own state change (colour, pressed state) still lands within the feedback band and carries the meaning.

Pitfalls: size the circle to the farthest corner, or it clips short of the edges; spawn on `pointerdown`, not `click`, so the feedback is immediate; remove on `animationend` (also on `animationcancel` if the host can be hidden mid-animation) so nodes do not accumulate; `overflow: hidden` on a host that also shows an outside focus ring clips the ring, so use `outline` (not clipped) or an inner wrapper.

## Hover image trail

> **Default: No**
> - **Allowed when:** a portfolio or campaign surface uses images as pure decoration behind or beside content that stands on its own.
> - **Evidence required:** no required content carried by the trail; images decorative (`alt=""`) and `aria-hidden`; flash check against SC 2.3.1; trail never covers hover/focus content in a way that violates SC 1.4.13; constant node count under fast pointer movement.
> - **Fallback:** a static image or a single hover preview.

```js
function imageTrail(host, sources, { gap = 80, pool = 8 } = {}) {
  const imgs = sources.slice(0, pool).map((src) => {
    const img = new Image();
    img.src = src; img.alt = ''; img.decoding = 'async';
    img.className = 'fx-trail'; img.setAttribute('aria-hidden', 'true');
    img.decode().catch(() => {});                // preload: no decode jank on first show
    host.append(img);
    return img;
  });
  let i = 0, lastX = null, lastY = null, lastT = 0;
  const move = (e) => {
    if (e.pointerType !== 'mouse') return;
    const r = host.getBoundingClientRect();
    const x = e.clientX - r.left, y = e.clientY - r.top;
    if (lastX !== null && Math.hypot(x - lastX, y - lastY) < gap) return; // distance gate
    if (e.timeStamp - lastT < 120) return;       // time gate for flash safety
    lastX = x; lastY = y; lastT = e.timeStamp;
    const img = imgs[i++ % imgs.length];         // fixed pool, round-robin
    img.getAnimations().forEach((a) => a.cancel());
    img.animate(
      [
        { transform: `translate(${x}px, ${y}px) translate(-50%, -50%) scale(0.9)`, opacity: 1 },
        { transform: `translate(${x}px, ${y}px) translate(-50%, -50%) scale(1)`, opacity: 0 },
      ],
      { duration: motionMs('--motion-narrative'), easing: 'ease-out', fill: 'forwards' } // decorative, non-blocking
    );
  };
  host.addEventListener('pointermove', move);
  return () => host.removeEventListener('pointermove', move);
}
```

```css
.fx-trail { position: absolute; left: 0; top: 0; width: 180px; pointer-events: none; opacity: 0; }
```

Pitfalls: creating an `<img>` per move leaks nodes and decode work, so reuse a fixed pool; gate by distance (~80 px) and by time, because a fast flick at a short distance gate spawns many images per second; high-contrast images popping in quick succession can count as flashes, so keep each image small and test with a flash analyser. Under WCAG's general flash threshold, flashing fails only when the combined flashing area exceeds 25% of any 10° visual field (0.006 sr) at typical viewing distance; WCAG estimates a 10° field as a 341 × 256 px rectangle on a 1024 × 768 screen, so the limit is about a quarter of that rectangle (≈ 21,800 px², for example 170 × 128 px); animate `transform`/`opacity` only, never `left`/`top`.

## Drag, swipe and fling

Direct manipulation needs capture, intent detection, velocity, and a release that hands velocity to a spring or decay.

```css
.fx-drag-x { touch-action: pan-y; user-select: none; } /* horizontal drag; vertical scroll stays native */
```

```js
const SLOP = 8;                                   // px before deciding intent (house default)
function draggable(el, { min, max, onRelease }) {
  let id = null, state = 'idle', startX = 0, startY = 0, base = 0, x = 0, samples = [];
  const rubber = (over, d, c = 0.55) => (1 - 1 / ((Math.abs(over) * c) / d + 1)) * d * Math.sign(over);
  const clampDisplay = (v) =>
    v < min ? min + rubber(v - min, el.clientWidth) :
    v > max ? max + rubber(v - max, el.clientWidth) : v;

  el.addEventListener('pointerdown', (e) => {
    if (e.button !== 0 || id !== null) return;
    id = e.pointerId; state = 'pending';
    startX = e.clientX; startY = e.clientY; base = x;
    samples = [{ t: e.timeStamp, x: e.clientX }];
    el.setPointerCapture(id);                    // keep receiving moves outside the element
  });
  el.addEventListener('pointermove', (e) => {
    if (e.pointerId !== id) return;
    const dx = e.clientX - startX, dy = e.clientY - startY;
    if (state === 'pending') {
      if (Math.hypot(dx, dy) < SLOP) return;
      if (Math.abs(dy) > Math.abs(dx)) { end(e); return; } // vertical intent: let it scroll
      state = 'dragging';
    }
    samples.push({ t: e.timeStamp, x: e.clientX });
    samples = samples.filter((s) => e.timeStamp - s.t <= 100); // recent window only
    x = base + dx;
    el.style.transform = `translate3d(${clampDisplay(x)}px, 0, 0)`;
  });
  const end = (e) => {
    if (e.pointerId !== id) return;
    const a = samples[0], b = samples.at(-1);
    const v = b && a && b.t > a.t ? (b.x - a.x) / (b.t - a.t) * 1000 : 0; // px/s
    if (state === 'dragging') onRelease({ x: clampDisplay(x), velocity: v });
    if (el.hasPointerCapture(id)) el.releasePointerCapture(id);
    id = null; state = 'idle';
  };
  el.addEventListener('pointerup', end);
  el.addEventListener('pointercancel', end);     // browser took over (e.g. native pan)
}
```

Mechanics:

- **Capture:** `setPointerCapture()` routes every subsequent event for that pointer to the element, so a fast drag cannot escape it. Handle `pointercancel` and `lostpointercapture`; touch scrolling or a system gesture can end the drag without `pointerup`.
- **`touch-action`:** declare what the browser keeps. `pan-y` on a horizontal carousel keeps vertical page scroll native; `none` takes everything and must be limited to the draggable surface. Calling `preventDefault()` in `pointermove` does not stop touch panning; only `touch-action` does.
- **Intent and slop:** wait for a small movement (house default 8 px) before deciding the axis; a press that never exceeds the slop is a tap and must still activate.
- **Velocity:** compute from samples in the last ~100 ms, not from the last two events, which are noisy and often zero at release.
- **Momentum and decay:** for free scrolling, decay velocity exponentially, `v(t) = v0·e^(−t/τ)`, which lands at `x0 + v0·τ`. Use the projected landing point to choose a snap target.
- **Rubber-band:** past a bound, display `f(x) = (1 − 1/((x·c/d) + 1))·d` where `x` is the overshoot, `d` the dimension and `c ≈ 0.55`; resistance grows smoothly and never exceeds `d`.
- **Release into a spring carrying velocity:** pass the measured velocity as the spring's initial velocity so motion is continuous, for example Motion `animate(el, { x: target }, { type: 'spring', velocity, stiffness, damping })`. Take presets and interruption rules from [motion-timing-engines.md](motion-timing-engines.md); a grabbed element that is mid-spring must stop where it is and follow the pointer.
- **Reduced motion:** keep the drag 1:1 (it is user-driven), but replace the fling and rubber-band settle with a short opacity or instant snap.
- **Single-pointer alternative (SC 2.5.7):** every drag outcome needs a non-drag path: previous/next buttons, a select control, or arrow keys on the focused item. Swipe-to-dismiss needs a visible dismiss button.

## Version Sources

Moving release pins in this file were resolved 2026-10-20 (Baseline from web-features 3.43.0, browser support from MDN BCD 8.1.6):

- **gsap 3.15.0** (verified) — https://registry.npmjs.org/gsap ; `gsap.quickTo()` API from https://gsap.com/docs/v3/GSAP/gsap.quickTo()
- **motion 14.4.0** (verified) — https://motion.dev/changelog
- **Pointer Events and interaction media queries (`hover`, `pointer`)** — Baseline widely available (verified) — https://web-platform-dx.github.io/web-features-explorer/
- **Registered custom properties (`@property`)** — Baseline 2024-07-09; Chrome 85, Firefox 128, Safari 16.4 (verified) — https://github.com/mdn/browser-compat-data
- **Unprefixed `mask-image`** — Baseline widely available 2026-06-07 (verified) — https://web-platform-dx.github.io/web-features-explorer/
- **Rubber-band formula and `c ≈ 0.55`** (unverified) — Apple does not publish the UIScrollView constant; the formula circulates only through secondary developer write-ups
- **Slop 8 px, 100 ms velocity window, 120 ms trail time gate** (unverified) — house defaults, not platform specifications; tune per product
