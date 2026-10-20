# Motion Timing Engines

Canonical source for durations, easing, spring presets, interruption behaviour, the Web Animations API foundation and motion tokens. Other motion skills link here instead of restating values. Accessibility obligations live in the WCAG skill; this file covers timing only.

## 1. Duration-based easing or springs

Pick the engine by what the motion has to survive, not by taste.

| Question | Duration + easing | Spring |
| --- | --- | --- |
| Can the user interrupt or reverse it mid-flight? | Rarely | Often (drag, toggles, panels, cursor pull) |
| Does it need a fixed, predictable end time (choreography, sync with audio)? | Yes | No: settle time emerges from physics |
| Is it an effect (opacity, colour) rather than spatial movement? | Yes | Only with critical damping |
| Does the gesture hand over a velocity (fling, release)? | No | Yes |

Easing rules:

- **Enter: ease-out** (fast start, gentle landing), e.g. `cubic-bezier(0.2, 0, 0, 1)`. The element answers the user immediately and decelerates into place.
- **Exit: ease-in** (gentle start, fast leave), e.g. `cubic-bezier(0.3, 0, 1, 1)`. The element gets out of the way.
- **On-screen move: ease-in-out** or a spring.
- **Asymmetry:** exits are shorter than enters, about 70–80% of the matching enter. Users wait for arrivals; nobody waits for departures.
- **Distance-based duration:** a fixed duration over a long travel looks rushed, over a short one sluggish. Scale with distance and clamp to the band:

```js
// px → ms, clamped to the band for this motion class
const durationFor = (px, { min = 150, max = 400, msPerPx = 0.5 } = {}) =>
  Math.min(max, Math.max(min, min + px * msPerPx));
```

### Canonical duration bands (Coacus house defaults, not WCAG)

| Class | Examples | Duration |
| --- | --- | --- |
| Feedback | hover and press colour, focus ring fade | 100–150 ms |
| Component state | toggle, checkbox, tab indicator, chip | 150–250 ms |
| Overlay / layout | menu, drawer, modal, reflowing list | 250–400 ms |
| Route / page | page or view change | 300–500 ms |
| Exit | any of the above leaving | ≈ 70–80% of the matching enter |
| Scroll-linked | progress, parallax, reveal tied to scroll | no duration: progress-driven |

Effects (opacity, colour) never overshoot, whatever engine drives them.

## 2. `cubic-bezier()` versus `linear()`

`cubic-bezier(x1, y1, x2, y2)` describes one smooth curve with two control points. Y values outside [0, 1] give a single overshoot or anticipation; it cannot express oscillation.

`linear()` (Baseline widely available since December 2023: Chrome 113, Firefox 112, Safari 17.2) is a piecewise-linear easing through any number of points. Sampling a spring or bounce solver offline produces an easing that CSS transitions and keyframes can run off the main thread:

```css
:root {
  /* sampled from k=250, c=16, m=1 (spring.playful) over its ~0.5 s settle */
  --ease-playful: linear(0, 0.07 5%, 0.23 10%, 0.44 15%, 0.65 20%, 0.84 25%,
                         0.98 30%, 1.08 35%, 1.14 40%, 1.16 45%, 1.15 50%,
                         1.1 60%, 1.03 70%, 0.99 80%, 0.98 90%, 1);
}
.badge-in { transition: transform 500ms var(--ease-playful); }
```

Limits of a sampled `linear()` spring:

- **No velocity retargeting.** It is still a fixed-duration curve. When the target changes mid-flight, the new transition starts from the current value at zero velocity, so the motion kinks.
- **Faceting.** Too few points show visible straight segments and flattened peaks, especially at large travel or 120 Hz. Use enough points to keep the error below about 1% of travel; a generator plus a visual check beats hand-written stops.
- **Duration is baked in.** The duration must match the settle time the curve was sampled for, or the physics look wrong.

## 3. Spring model and canonical presets

A damped harmonic oscillator, displacement `x` from the target:

```text
F = −k·x − c·v        (k stiffness, c damping, v velocity, m mass)
ζ = c / (2·√(k·m))     damping ratio: 1 critical, < 1 underdamped
overshoot = exp(−ζπ / √(1 − ζ²))   for ζ < 1, as a fraction of travel
```

ζ, not stiffness alone, decides whether something bounces. Stiffness sets speed; damping ratio sets character.

### Canonical spring tokens (m = 1)

| token | use | stiffness k | damping c | ζ | overshoot | ~settle (2%) |
|---|---|---|---|---|---|---|
| `spring.snap` | press feedback, toggles, small controls | 500 | 45 | ≈1.0 | 0% | ≈0.26 s |
| `spring.smooth` | menus, drawers, modals, layout moves | 300 | 31 | ≈0.89 | ≈0.2% | ≈0.26 s |
| `spring.playful` | celebratory badges, rare delight | 250 | 16 | ≈0.51 | ≈16% | ≈0.5 s |

Common mistake: k = 400, c = 30 gives ζ ≈ 0.75 and about 3% overshoot, so it is not "zero bounce". Effects tokens (opacity, colour, blur) use critical damping or a duration curve and never overshoot.

### Mapping to Motion

Motion's `spring` transition accepts physics options (`stiffness`, `damping`, `mass`) or time options (`visualDuration` in seconds, `bounce` from −1 to 1 where 0 is critically damped). When both are present, the physics options win and the time options are ignored.

```js
import { animate } from "motion";
// exact canonical token
animate(el, { x: 240 }, { type: "spring", stiffness: 300, damping: 31, mass: 1 });
// approximate equivalent when designers think in time
animate(el, { x: 240 }, { type: "spring", visualDuration: 0.26, bounce: 0.05 });
```

Store tokens as physics values; treat `visualDuration`/`bounce` as an authoring approximation, not the source of truth.

### Material 3 Expressive motion scheme

Material 3 Expressive replaces duration/easing pairs with springs, split into **spatial** tokens (position, size, rotation: may overshoot in the expressive scheme) and **effects** tokens (colour, opacity: never overshoot), each in fast / default / slow speeds, under a *standard* or *expressive* scheme. Compose values (androidx-main `MotionScheme.kt`, resolved 2026-10-20), as stiffness / damping ratio:

| Token | Stiffness | Damping ratio |
| --- | --- | --- |
| Expressive spatial default | 380 | 0.8 |
| Expressive fast spatial | 800 | 0.6 |
| Standard spatial default | 700 | 0.9 |
| Effects default | 1600 | 1.0 |

Compose uses a damping ratio directly; convert to `c = 2ζ·√(k·m)` for web solvers.

## 4. Interruption and retargeting by path

| Path | What happens when the target changes mid-flight |
| --- | --- |
| CSS transition | Reverses from the current value. A reversal back to the start uses a shortened duration proportional to progress already made (reversing shortening factor). Velocity is not preserved. |
| CSS `@keyframes` animation | No retargeting. Changing the animation restarts it, so the element jumps to the first keyframe unless you capture the current state. |
| Sampled `linear()` spring | Behaves as a CSS transition: restarts at zero velocity, visible kink. |
| View Transition | Not interruptible. A new `startViewTransition()` skips the running one; call `transition.skipTransition()` to abandon it explicitly. Keep durations short. |
| Web Animations API | Scriptable control: `animation.reverse()`, `playbackRate`, `updatePlaybackRate()` (smooth rate change without a jump), `currentTime` seeking. Still no physical velocity. |
| JS spring solver (Motion, react-spring, custom) | Carries position and velocity into the new target. The only path that is truly continuous under interruption. |

Use a JS spring for anything the user can grab, fling or toggle rapidly. Use CSS for fire-and-forget transitions.

## 5. Web Animations API foundation

CSS animations, CSS transitions and `element.animate()` all surface as `Animation` objects.

```js
const anim = el.animate(
  [{ transform: "translateY(8px)", opacity: 0 }, { transform: "none", opacity: 1 }],
  { duration: 220, easing: "cubic-bezier(0.2, 0, 0, 1)", fill: "both" }
);
await anim.finished;          // promise; rejects with AbortError on cancel()
anim.commitStyles();          // write the end state to inline style
anim.cancel();                // drop the fill so it does not pin computed style

el.getAnimations();           // running CSS + WAAPI animations on el
document.getAnimations();     // every animation in the document
```

Avoid leaving `fill: "forwards"` animations piling up; commit and cancel instead.

Scroll timelines in script: `new ScrollTimeline({ source, axis })` and `new ViewTimeline({ subject, axis, inset })`, passed as `timeline` to `element.animate()`. Scroll-driven animations are **Limited availability** (Chrome 115, Safari 26, Firefox preview only): feature-detect with `"ScrollTimeline" in window` and keep a static or IntersectionObserver fallback. Depth on scroll-linked motion belongs to the planned ui-scroll-driven-motion skill.

## 6. Motion tokens and choreography

Name tokens by role, not by value: `motion.duration.feedback`, `motion.duration.overlay-enter`, `motion.easing.enter`, `motion.easing.exit`, `motion.spring.snap`. Values can change; roles stay.

DTCG Format Module 2025.10 (Stable, published 2025-10-28; https://www.designtokens.org/TR/2025.10/format/, resolved 2026-10-20) defines `duration` (object with `value` and `unit` `"ms"` or `"s"`), `cubicBezier` (`[P1x, P1y, P2x, P2y]`, x in [0, 1]) and the composite `transition`. It has no spring type: store springs as a group of `number` tokens with a documented convention.

```json
{
  "motion": {
    "duration": { "overlay-enter": { "$type": "duration", "$value": { "value": 300, "unit": "ms" } } },
    "easing": { "enter": { "$type": "cubicBezier", "$value": [0.2, 0, 0, 1] } },
    "spring": {
      "smooth": {
        "stiffness": { "$type": "number", "$value": 300 },
        "damping": { "$type": "number", "$value": 31 },
        "mass": { "$type": "number", "$value": 1 }
      }
    }
  }
}
```

Choreography:

- **Stagger budget:** cap the total of all offsets at 300–500 ms. With a fixed budget, the per-item delay is `budget / count`; past about 8–10 items, animate the group or only the first visible ones.
- **Order by meaning:** lead with the element the user acted on, then its consequences; read order for lists.
- **One focal motion at a time.** Parallel motions of equal weight compete for attention.

## 7. Squash and stretch

The first of Disney's twelve principles (Thomas and Johnston, *The Illusion of Life*, 1981). An object deforms on impact or acceleration to convey mass and elasticity.

- **Preserve volume:** `scaleX · scaleY ≈ 1` (squash to `scaleY(0.9)` → `scaleX(1.11)`).
- **Origin at the contact point:** `transform-origin: bottom center` for a landing.
- **Small and short:** at most 10–15% deformation, held for one feedback-band beat, then a `spring.snap` back.

```css
@keyframes land { 40% { transform: scale(1.1, 0.9); } 100% { transform: none; } }
.ball { transform-origin: 50% 100%; }
```

> **Default: No** for operational and dense interfaces, text, data visualisation and brand marks.
> **Allowed when:** a playful, low-density surface (game UI, onboarding illustration, celebratory badge) and the deformation reinforces a physical metaphor.
> **Evidence required:** text and numbers stay undistorted; the reduced-motion path removes it.
> **Fallback:** a plain opacity or scale-only transition.

For character and sprite motion review, use [game-animation-qa-motion](../../../industry/game-animation-qa-motion/SKILL.md).

## Version Sources

Moving release pins in this file were resolved 2026-10-20:

- **CSS `linear()` easing** (verified) — Baseline widely available December 2023 (Chrome 113, Firefox 112, Safari 17.2) — web-features 3.43.0 and MDN BCD 8.1.6, https://developer.mozilla.org/en-US/docs/Web/CSS/easing-function/linear
- **Scroll-driven animations / `ScrollTimeline` / `ViewTimeline`** (verified) — Limited availability: Chrome 115, Safari 26, Firefox preview only — MDN BCD 8.1.6, https://developer.mozilla.org/en-US/docs/Web/API/ScrollTimeline
- **Motion `spring` options** (verified) — motion 14.4.0 (2026-10-19), https://motion.dev/docs/spring and https://motion.dev/changelog
- **Material 3 Expressive Compose motion scheme values** (verified) — androidx-main `MotionScheme.kt`, https://android.googlesource.com/platform/frameworks/support/+/androidx-main/compose/material3/material3/src/commonMain/kotlin/androidx/compose/material3/MotionScheme.kt
- **DTCG Format Module 2025.10** (verified) — Stable, published 2025-10-28, https://www.designtokens.org/technical-reports/
