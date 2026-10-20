# View Transitions

The View Transition API captures a snapshot of the current state, lets you change the DOM, captures the new state, and animates between the two with CSS on a tree of pseudo-elements. The live DOM is final from the moment the update callback returns; only snapshots animate. The `--motion-*` duration tokens used below are defined in [motion-timing-engines.md](../../ui-motion-interaction/references/motion-timing-engines.md).

---

## Same-Document API

```js
function swapView(update) {
  // Base path: no API, or the user asked for less motion handled in CSS.
  if (!document.startViewTransition) {
    update();
    return;
  }
  // Callback form: Chrome 111, Firefox 144, Safari 18. The update may return a
  // promise; the new snapshot waits for it.
  const vt = document.startViewTransition(update);
  vt.updateCallbackDone.then(() => restoreFocus());   // DOM is final: move focus now
  vt.ready.catch(() => {});      // rejects when the transition is skipped or aborted
  // finished resolves once the animation completes or is skipped; it rejects only
  // when the update callback rejects, so clean up in finally().
  vt.finished.finally(() => cleanup());
}
```

The three promises:

| Promise | Settles when | Use it for |
|---|---|---|
| `updateCallbackDone` | The update callback resolves (or rejects) | Focus management, analytics, state that depends on the new DOM |
| `ready` | Pseudo-element tree is built and the animation is about to start | Driving custom WAAPI animations on the pseudo-elements |
| `finished` | Resolves when the animation ends or the transition is skipped; rejects if the update callback rejects | Removing temporary `view-transition-name` values, re-enabling input |

`vt.skipTransition()` jumps to the final state without animating; the update still runs. Starting a new transition while one is active skips the active one. Call `skipTransition()` when a second user action arrives mid-transition and the intermediate animation would mislead.

The options-object form `startViewTransition({ update, types })` arrived with transition types (Chrome 125, Firefox 147, Safari 18.2). Firefox 144 to 146 accepts only the callback form, so guard the object form (see Transition Types).

---

## Naming Participants

```css
.card[data-active] { view-transition-name: hero-card; }
.thumb { view-transition-name: match-element; } /* identity from the element itself */
.thumb { view-transition-class: thumb; }        /* one rule styles every thumb group */

::view-transition-group(.thumb) { animation-duration: var(--motion-layout); }
```

- `view-transition-name` must be **unique** among rendered elements at capture time. A duplicate name aborts the whole transition: `ready` rejects and the DOM updates without animation. Generate names from stable IDs (`view-transition-name: card-${id}` set inline) or use `match-element`.
- `match-element` (Chrome 137, Firefox 144, Safari 18.4) derives identity from the element object, so it pairs the same node across the swap. It does not pair two different nodes, such as a thumbnail and a detail image; use an explicit shared name for that.
- `view-transition-class` (Baseline newly 2025-10-14) groups styling without repeating selectors per name.
- Elements without a name are part of the `root` snapshot and cross-fade as one image.

---

## Transition Types

```js
function startTyped(update, types) {
  try {
    return document.startViewTransition({ update, types });
  } catch {
    // Engines without the options object reject it; fall back to an untyped transition.
    return document.startViewTransition(update);
  }
}
startTyped(update, ['nav-back']);
```

```css
html:active-view-transition-type(nav-back) {
  &::view-transition-old(main) { animation-name: slide-out-right; }
  &::view-transition-new(main) { animation-name: slide-in-left; }
}
```

Types and `:active-view-transition-type()` are Baseline newly available since 2026-01-13. `vt.types` is a mutable set, so a `pagereveal` handler can add types during cross-document navigation.

---

## Pseudo-Element Tree

```
::view-transition
└─ ::view-transition-group(name)
   └─ ::view-transition-image-pair(name)
      ├─ ::view-transition-old(name)
      └─ ::view-transition-new(name)
```

- The **group** animates size and position (`width`, `height`, `transform`) from old box to new box.
- The **image pair** isolates blending (`isolation: isolate`, `mix-blend-mode: plus-lighter` on the images) so the cross-fade does not dip in brightness.
- **old/new** are replaced elements showing the snapshots; they fade by default.

### Stretched Snapshots

When the aspect ratio changes (a square thumbnail becomes a wide hero), the default `object-fit: fill` stretches both images. Fix it per name:

```css
::view-transition-old(hero),
::view-transition-new(hero) {
  height: 100%;          /* follow the group's height while it animates */
  object-fit: cover;     /* crop instead of stretch */
  overflow: clip;
}
```

For text blocks that change width, animate only the group and set `animation: none` on old and new so the text does not distort, or use `object-fit: none` with `object-position: left top`.

---

## Cross-Document View Transitions

```css
/* On BOTH the outgoing and the incoming page */
@view-transition { navigation: auto; }
```

- Not Baseline: Chrome 126 and Safari 18.2, no Firefox. Firefox navigates normally, which is the fallback.
- Same-origin navigations only, and both pages must opt in.
- `pageswap` fires on the old page before its snapshot (Chrome 124; Safari 18.2 partial) and `pagereveal` fires on the new page before its first render (Chrome 123, Safari 18.2). Both expose `event.viewTransition` (null when none runs); use them to set names or types that depend on the navigation (`event.activation` / `navigation.activation`).
- Render blocking: `<link rel="expect" href="#main-content" blocking="render">` (in the incoming page's `<head>`) holds the first render of the new page until that element is parsed, so the new snapshot is not empty. `rel="expect"` ships in Chrome 124 and Safari 18.2, not Firefox; it delays first paint, so point it at an element near the top of the document.
- Without render blocking, a slow page can snapshot before its content arrives and the transition animates to an empty frame.

---

## Chromium-Only Enhancements

Treat these as enhancements behind feature checks; the flat, document-scoped transition remains the base path.

| Feature | Chrome | Purpose |
|---|---|---|
| Nested groups (`view-transition-group: contain / nearest / <name>`) | 140 | Keep child groups clipped inside a parent group |
| Element-scoped transitions (`element.startViewTransition()`) | 147 | Run independent transitions in separate subtrees; the rest of the page stays interactive |
| `ViewTransition.waitUntil(promise)` | 144 | Extend the transition's lifetime until custom work settles |

```js
if ('startViewTransition' in Element.prototype) {
  panel.startViewTransition(() => updatePanel());
} else if (document.startViewTransition) {
  document.startViewTransition(() => updatePanel());
} else {
  updatePanel();
}
```

---

## Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  ::view-transition-group(*) { animation: none; }               /* no travel */
  ::view-transition-old(*),
  ::view-transition-new(*) { animation-duration: var(--motion-feedback); }  /* keep a short fade */
}
```

Prefer a short cross-fade over `animation: none` on everything: an instant swap of a whole region can be as disorienting as motion. Directional slides are the highest-risk pattern; remove them first.

---

## Interaction During the Snapshot

While the pseudo-element tree is on screen, `::view-transition` sits over the page and receives pointer events, so clicks are lost. Either keep transitions short (overlay/layout band), or let input through to unnamed content:

```css
::view-transition { pointer-events: none; }
```

Named participants are still not hit-testable for the duration, so avoid naming controls the user clicks rapidly. Rendering of the live DOM is paused between the old snapshot and `updateCallbackDone`; a slow async update freezes the screen, so keep the update fast or show progress before starting the transition.

---

## Framework Integration Snippets

React on lines without `<ViewTransition>`:

```js
import { flushSync } from 'react-dom';
document.startViewTransition(() => flushSync(() => setTab(next)));
```

Vue Router guard covering every navigation, including back and forward:

```js
import { nextTick } from 'vue';

let finishTransition;
router.beforeResolve(() => {
  if (!document.startViewTransition) return;
  return new Promise((resolveGuard) => {
    document.startViewTransition(
      () => new Promise((done) => { finishTransition = done; resolveGuard(); })
    );
  });
});
router.afterEach(async () => {          // also runs for failed navigations
  await nextTick();                    // wait for the new route's DOM
  finishTransition?.();
  finishTransition = undefined;
});
```

For link clicks only, `<RouterLink view-transition>` passes the `router.push()` promise to `startViewTransition`.

---

## Version Sources

Moving release pins in this file were resolved 2026-10-20:

- **View Transitions, classes, types, cross-document Baseline** (verified) — web-features 3.43.0, https://www.npmjs.com/package/web-features
- **Browser versions incl. `match-element`, `pageswap`, `pagereveal`, `rel="expect"`, nested groups, element-scoped, `waitUntil`** (verified) — @mdn/browser-compat-data 8.1.6, https://www.npmjs.com/package/@mdn/browser-compat-data
- **vue-router 5.4.0 `viewTransition` prop** (verified) — https://router.vuejs.org/api/interfaces/RouterLinkProps.html
