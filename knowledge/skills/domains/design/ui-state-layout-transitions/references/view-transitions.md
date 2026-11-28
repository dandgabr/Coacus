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

Both documents opt in with `@view-transition { navigation: auto; }`. Keep ordinary same-origin links and let the browser commit navigation even if snapshots are skipped, including on a reload or a direct URL. For slow documents, `<link rel="expect" href="#main-content" blocking="render">` can hold the first render until a small, early target has been parsed. It can delay first paint.

### Compatibility by capability

Review date 2026-11-27. The Firefox numbers in the Beta column describe the Beta channel available on that date. Gate each capability used.

| Capability | Stable support at review | Firefox Beta |
|---|---|---|
| Cross-document opt-in with `@view-transition` | Chrome 126, Safari 18.2 | Firefox 162 |
| `pageswap` / `PageSwapEvent.activation` | Chrome 124, Safari 18.2 for same-origin navigation | Firefox 162 |
| `pagereveal` | Chrome 123, Safari 18.2 | Firefox 162 |
| `event.viewTransition` on both events | Chrome 126, Safari 18.2 | Firefox 162 |
| `navigation.activation` on the incoming document | Chrome 123, Firefox 147, Safari 26.2 | Available in stable Firefox |
| `rel="expect"` | Chrome 124, Safari 18.2 | Firefox 162 |
| Element-scoped `Element.startViewTransition()` | Chrome 147 | No support recorded |

Optional rendering and navigation APIs can arrive independently. An event may fire with a null `viewTransition`. A navigation may have no source entry. Leave the base navigation or an untyped cross-fade in place in those cases. [MDN browser-compat-data 8.1.11](https://www.npmjs.com/package/@mdn/browser-compat-data/v/8.1.11), [web-features 3.48.0](https://www.npmjs.com/package/web-features/v/3.48.0), [Firefox 162 Beta release notes](https://www.firefox.com/en-US/firefox/162.0beta/releasenotes/), [Firefox 162 developer notes](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox/Releases/162), [Chrome cross-document guide](https://developer.chrome.com/docs/web-platform/view-transitions/cross-document).

### Directional list-to-detail navigation

Serve the next four blocks together over one HTTP origin. Use direction from the actual source and destination entries on both sides of a navigation. Going from the list to the detail goes inward whether the user clicked the link or traversed history forward. Returning to the list goes outward, including with the browser Back button. The script leaves the history stack, viewport and focus restoration to the browser.

Save as `transition-list.html`. The list markup is in the scoped reorder example below.

```html
<!doctype html>
<html lang="en">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Field register</title>
<link rel="stylesheet" href="transition-navigation.css">
<script src="transition-navigation.js"></script>
<main>
  <h1>Field register</h1>
  <p><a id="detail-link" href="transition-detail.html#specimen">Open the reed specimen</a></p>
  <!-- Insert the isolated reorder block here to exercise both examples together. -->
</main>
</html>
```

Save as `transition-detail.html`.

```html
<!doctype html>
<html lang="en">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Reed specimen</title>
<link rel="stylesheet" href="transition-navigation.css">
<script src="transition-navigation.js"></script>
<main>
  <h1 id="specimen" tabindex="-1">Reed specimen</h1>
  <p>Collected along the boardwalk after the morning tide.</p>
  <p><a id="back-link" href="transition-list.html">Return to the field register</a></p>
</main>
</html>
```

Save as `transition-navigation.css`.

```css
:root {
  --motion-route: 400ms;
  --ease-enter: cubic-bezier(.2, 0, 0, 1);
}
@media (prefers-reduced-motion: no-preference) {
  @view-transition { navigation: auto; }
  :root:active-view-transition-type(into-detail)::view-transition-new(root) {
    animation: arrive var(--motion-route) var(--ease-enter) both;
  }
  :root:active-view-transition-type(back-to-list)::view-transition-new(root) {
    animation: return var(--motion-route) var(--ease-enter) both;
  }
}
@keyframes arrive { from { transform: translateX(1rem); opacity: 0; } }
@keyframes return { from { transform: translateX(-1rem); opacity: 0; } }
@media (prefers-reduced-motion: reduce) {
  ::view-transition-group(*) { animation-duration: 0s !important; }
}
```

Save as `transition-navigation.js`. Resolve a file's pathname and ignore its fragment, so fragment destinations keep their native focus behavior. In a deployed app use the app's known route patterns.

```js
const reduce = matchMedia('(prefers-reduced-motion: reduce)');
const list = new URL('transition-list.html', location.href).pathname;
const detail = new URL('transition-detail.html', location.href).pathname;

function labelTransition(transition, activation) {
  if (!transition) return;
  // Skip and duplicate-name failures can reject this promise.
  void transition.ready.catch(() => {});
  if (reduce.matches || new URLSearchParams(location.search).has('plain')) {
    transition.skipTransition();
    return;
  }
  const fromURL = activation?.from?.url;
  const toURL = activation?.entry?.url;
  if (!transition.types || !fromURL || !toURL || activation.navigationType === 'reload') return;

  const from = new URL(fromURL).pathname;
  const to = new URL(toURL).pathname;
  if (from === list && to === detail) transition.types.add('into-detail');
  if (from === detail && to === list) transition.types.add('back-to-list');
}

window.addEventListener('pageswap', event => {
  labelTransition(event.viewTransition, event.activation);
});
window.addEventListener('pagereveal', event => {
  labelTransition(event.viewTransition, window.navigation?.activation);
});
```

Open each document directly, follow the link in both directions, use browser Back and Forward, then repeat with reduced motion and with `?plain` on the starting page. Test scrolling the list before navigating so that Back can demonstrate restoration. A skipped snapshot must still show the destination at the correct URL. Use a document transition only for this page-level change. Keep independent controls outside the snapshot scope for local updates.

## Isolated Reorders

Use a scope per list to preserve surrounding pointer interaction and popover layering. Match nodes by identity with `view-transition-name: match-element`. Give every active scope its own update state. Scoped support absent or reduced motion enabled means the same reorder runs immediately. Use [FLIP](flip-layout-animation.md) if the product still needs local motion on an older engine.

Insert this block into the example beneath the detail link. Focus stays on the reorder controls above the lists. The notes panel sits at the foot of the viewport, and the page provides space to scroll content clear of it. The original list items are moved, so their identity survives each action.

```html
<style>
  :root { --motion-layout: 320ms; --notes-space: min(8rem, 40dvh); }
  .reorder-controls { display: flex; flex-wrap: wrap; gap: .5rem; }
  #reorder-note {
    position: fixed;
    inset: auto .5rem .5rem auto;
    margin: 0;
    box-sizing: border-box;
    inline-size: min(20rem, calc(100% - 1rem));
    max-block-size: var(--notes-space);
    overflow: auto;
  }
  :root:has(#reorder-note:popover-open) { scroll-padding-block-end: calc(var(--notes-space) + 1rem); }
  main:has(#reorder-note:popover-open) { padding-block-end: calc(var(--notes-space) + 1rem); }
  .reorder-list {
    padding: .5rem 2rem;
    background: #eef3e8;
    color: #193928;
  }
  .reorder-list::view-transition-group(*) { animation-duration: var(--motion-layout); }
  .reorder-list::view-transition { pointer-events: none; }
  @media (prefers-reduced-motion: no-preference) {
    .reorder-list li { view-transition-name: match-element; }
  }
</style>
<div class="reorder-controls">
  <button type="button" popovertarget="reorder-note">Open notes</button>
  <button class="reorder" type="button" aria-controls="north" hidden>Rotate north entries</button>
  <button class="reorder" type="button" aria-controls="south" hidden>Rotate south entries</button>
</div>
<div id="reorder-note" popover="manual">
  <p>Both groups remain available while these notes are open.</p>
  <button type="button" popovertarget="reorder-note" popovertargetaction="hide">Close notes</button>
</div>
<ul class="reorder-list" id="north" aria-label="North entries">
  <li>Headland</li>
  <li>Salt pool</li>
  <li data-last>Boardwalk</li>
</ul>
<ul class="reorder-list" id="south" aria-label="South entries">
  <li>Reed bank</li>
  <li>High tide line</li>
  <li data-last>Sand fence</li>
</ul>
<script>
  for (const button of document.querySelectorAll('.reorder')) {
    const list = document.getElementById(button.getAttribute('aria-controls'));
    let active;
    let pending = Promise.resolve();
    const rotate = () => list.insertBefore(list.lastElementChild, list.firstElementChild);

    function reorder() {
      if (reduce.matches || typeof list.startViewTransition !== 'function') {
        rotate();
        return;
      }

      const transition = list.startViewTransition(rotate);
      active = transition;
      void transition.ready.catch(() => {});
      void transition.finished.then(
        () => { if (active === transition) active = undefined; },
        () => { if (active === transition) active = undefined; }
      );
      return transition.updateCallbackDone;
    }

    button.hidden = false;
    button.addEventListener('click', () => {
      active?.skipTransition();
      pending = pending.then(reorder).catch(console.error);
    });
    reduce.addEventListener('change', () => {
      if (reduce.matches) active?.skipTransition();
    });
  }
</script>
```

At 320 CSS pixels wide, open the notes and activate each reorder while the other list is animating. Check that the pointer reaches both controls, then focus and activate Close notes during a snapshot. Repeat on a reduced-motion path and with the element method unavailable. When there are focusable nodes inside a moving item, use `moveBefore()` where available to preserve move-related state, or restore focus to the same connected node after moving it. Keep a control used repeatedly outside a captured region.

### Other Snapshot Capabilities

| Capability | Chrome | Purpose |
|---|---|---|
| Nested groups (`view-transition-group: contain / nearest / <name>`) | 140 | Keep child groups clipped inside a parent group |
| `ViewTransition.waitUntil(promise)` | 144 | Extend the transition's lifetime until custom work settles |

Disable optional capabilities independently when unsupported. [Chrome scoped transitions guide](https://developer.chrome.com/docs/css-ui/view-transitions/element-scoped-view-transitions).

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

Cross-document and scoped rows in the compatibility table were reviewed 2026-11-27. Other release pins were resolved 2026-10-20:

- **Same-document View Transitions, classes and types** (verified) — web-features 3.43.0, https://www.npmjs.com/package/web-features
- **Browser versions for `match-element`, nested groups and `waitUntil`** (verified) — @mdn/browser-compat-data 8.1.6, https://www.npmjs.com/package/@mdn/browser-compat-data
- **vue-router 5.4.0 `viewTransition` prop** (verified) — https://router.vuejs.org/api/interfaces/RouterLinkProps.html
