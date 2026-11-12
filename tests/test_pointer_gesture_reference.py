import shutil
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / 'knowledge/skills/domains/design/ui-motion-interaction/references/pointer-and-gesture.md'


class PointerGestureReferenceTests(unittest.TestCase):
    def test_shimmer_is_static_by_default(self):
        text = REFERENCE.read_text(encoding='utf-8')
        section = text.split('## Pure CSS micro-interactions and shimmer text', 1)[1].split('## Version Sources', 1)[0]
        self.assertNotIn('animation: fx-shimmer', section)

    def test_shimmer_has_readable_fallback_and_guarded_transparency(self):
        text = REFERENCE.read_text(encoding='utf-8')
        section = text.split('## Pure CSS micro-interactions and shimmer text', 1)[1].split('## Version Sources', 1)[0]
        css = section.split('```css', 1)[1].split('```', 1)[0]
        base = css.split('@supports', 1)[0]
        self.assertIn('color: var(--fg)', base)
        self.assertNotIn('color: transparent', base)
        self.assertIn('@supports (background-clip: text)', css)
        self.assertIn('color: transparent', css.split('@supports (background-clip: text)', 1)[1])

    @unittest.skipUnless(shutil.which('node'), 'Coverage gap: Node unavailable; JavaScript gesture behavior not executed')
    def test_drag_release_and_cancellation(self):
        text = REFERENCE.read_text(encoding='utf-8')
        section = text.split('## Drag, swipe and fling', 1)[1]
        source = section.split('```js\n', 1)[1].split('\n```', 1)[0]
        source = source.replace('  const clampDisplay =', '  globalThis.testRubber = rubber;\n  const clampDisplay =')
        check = r'''
const assert = require('node:assert/strict');
const window = {listeners: {}, addEventListener(type, fn) { (this.listeners[type] ??= []).push(fn); }, removeEventListener(type, fn) { this.listeners[type] = (this.listeners[type] || []).filter(item => item !== fn); }};
class Element {
  constructor() { this.listeners = {}; this.style = {transform: ''}; this.clientWidth = 100; this.capture = null; }
  addEventListener(type, fn) { this.listeners[type] = fn; }
  removeEventListener(type, fn) { if (this.listeners[type] === fn) delete this.listeners[type]; }
  setPointerCapture(id) { this.capture = id; }
  hasPointerCapture(id) { return this.capture === id; }
  releasePointerCapture(id) { this.capture = null; this.emit('lostpointercapture', {pointerId: id}); }
  emit(type, props) {
    if (type === 'lostpointercapture' && (!props.target || props.target === this)) this.capture = null; // native capture has already ended
    const e = {button: 0, pointerId: 1, clientX: 0, clientY: 0, timeStamp: 0, detail: 1, target: this, preventDefault() { this.prevented = true; }, stopImmediatePropagation() { this.stopped = true; }, ...props};
    this.listeners[type]?.(e);
    for (const fn of window.listeners[type] || []) fn(e);
    return e;
  }
}
const el = new Element(), releases = [];
const sync = draggable(el, {min: -100, max: 100, onRelease: value => releases.push(value)});
const down = () => el.emit('pointerdown', {});
const move = x => el.emit('pointermove', {clientX: x, timeStamp: 20});
const position = () => el.style.transform;
down();
assert.equal(el.capture, null, 'pending press must not retarget a nested button click');
move(20);
assert.equal(el.capture, 1, 'capture starts once horizontal drag is established');
el.emit('lostpointercapture', {target: {}}); // implicit child capture was transferred
assert.equal(position(), 'translate3d(20px, 0, 0)', 'child capture transfer must not cancel the drag');
el.emit('pointercancel', {}); el.emit('lostpointercapture', {});
assert.equal(releases.length, 0, 'cancel must not commit');
assert.equal(position(), '', 'cancel restores the original inline transform');
down(); move(10);
assert.equal(position(), 'translate3d(10px, 0, 0)', 'next drag starts at the restored baseline');
el.emit('pointerup', {clientX: 10, timeStamp: 30});
assert.equal(releases.length, 1, 'release commits once even when capture is lost');
assert.equal(releases[0].x, 10);
const dragClick = el.emit('click', {detail: 1});
assert.equal(dragClick.prevented, true, 'drag-generated click must be cancelled');
assert.equal(dragClick.stopped, true, 'drag-generated click must not activate descendants');
assert.notEqual(el.emit('click', {detail: 0}).prevented, true, 'keyboard activation remains available');
assert.notEqual(el.emit('click', {detail: 1}).prevented, true, 'subsequent ordinary click remains available');
assert.equal(position(), 'translate3d(10px, 0, 0)', 'release preserves the committed position');
down(); move(30); el.emit('lostpointercapture', {});
assert.equal(releases.length, 1, 'lost capture must not commit');
assert.equal(position(), 'translate3d(10px, 0, 0)', 'lost capture restores last committed position');
down(); el.emit('pointermove', {clientX: 1, clientY: 30, timeStamp: 20}); el.emit('pointerup', {});
assert.equal(releases.length, 1, 'vertical intent must not commit');
const held = new Element(), heldReleases = [];
draggable(held, {min: -100, max: 100, onRelease: value => heldReleases.push(value)});
held.emit('pointerdown', {timeStamp: 0});
held.emit('pointermove', {clientX: 20, timeStamp: 20});
held.emit('pointerup', {clientX: 20, timeStamp: 500});
assert.equal(heldReleases[0].velocity, 0, 'holding before release must discard stale velocity');
const flick = new Element(), flickReleases = [];
draggable(flick, {min: -100, max: 100, onRelease: value => flickReleases.push(value)});
flick.emit('pointerdown', {timeStamp: 0});
flick.emit('pointermove', {clientX: 20, timeStamp: 20});
flick.emit('pointerup', {clientX: 20, timeStamp: 30});
assert.equal(flickReleases[0].velocity, 20 / 30 * 1000, 'recent flick includes release timing');
const reduced = new Element(), reducedReleases = [];
const reducedSync = draggable(reduced, {min: -100, max: 100, reducedMotion: true, onRelease: value => reducedReleases.push(value)});
reducedSync(120);
assert.equal(reduced.style.transform, 'translate3d(100px, 0, 0)', 'reduced sync clamps to bounds');
reducedSync(0);
reduced.emit('pointerdown', {timeStamp: 0});
reduced.emit('pointermove', {clientX: 50, timeStamp: 20});
assert.equal(reduced.style.transform, 'translate3d(50px, 0, 0)', 'reduced drag follows pointer within bounds');
reduced.emit('pointermove', {clientX: 150, timeStamp: 30});
assert.equal(reduced.style.transform, 'translate3d(100px, 0, 0)', 'reduced drag clamps without rubber band');
reduced.emit('pointerup', {clientX: 150, timeStamp: 40});
assert.deepEqual(reducedReleases[0], {x: 100, velocity: 0}, 'reduced release cannot fling');
reducedSync.dispose();
const overshoot = new Element(), overshootReleases = [];
draggable(overshoot, {min: -100, max: 100, onRelease: value => overshootReleases.push(value)});
overshoot.emit('pointerdown', {clientX: 0, timeStamp: 0});
overshoot.emit('pointermove', {clientX: 150, timeStamp: 20});
const edge = overshoot.style.transform;
overshoot.emit('pointerup', {clientX: 150, timeStamp: 30});
assert.equal(overshootReleases[0].x, parseFloat(edge.match(/translate3d\(([^p]+)/)[1]));
overshoot.emit('pointerdown', {clientX: 150, timeStamp: 40});
overshoot.emit('pointermove', {clientX: 158, timeStamp: 50});
assert.ok(parseFloat(overshoot.style.transform.match(/translate3d\(([^p]+)/)[1]) > overshootReleases[0].x, 'outward drag must not jump inward');
const lateFlick = new Element(), lateReleases = [];
draggable(lateFlick, {min: -100, max: 100, onRelease: value => lateReleases.push(value)});
lateFlick.emit('pointerdown', {timeStamp: 0});
lateFlick.emit('pointermove', {clientX: 20, timeStamp: 20});
lateFlick.emit('pointermove', {clientX: 20, timeStamp: 500});
lateFlick.emit('pointerup', {clientX: 40, timeStamp: 510});
assert.equal(lateReleases[0].velocity, 2000, 'release movement after a hold contributes to velocity');
assert.equal(lateReleases[0].x, 40, 'release includes final pointer position');
const sparse = new Element(), sparseReleases = [];
draggable(sparse, {min: -100, max: 100, onRelease: value => sparseReleases.push(value)});
sparse.emit('pointerdown', {timeStamp: 0});
sparse.emit('pointermove', {clientX: 20, timeStamp: 20});
sparse.emit('pointerup', {clientX: 40, timeStamp: 220});
assert.equal(sparseReleases[0].velocity, 100, 'sparse release displacement uses the last known sample');
sync(40);
assert.equal(position(), 'translate3d(40px, 0, 0)', 'sync updates the visual position');
down(); move(20);
assert.equal(position(), 'translate3d(60px, 0, 0)', 'drag uses the synchronized logical baseline');
el.emit('pointercancel', {});
down(); move(20); el.emit('pointercancel', {});
assert.equal(position(), 'translate3d(40px, 0, 0)', 'cancel restores the externally synchronized position');
assert.equal(releases.length, 1, 'cancel after synchronization must not commit');
sync(120);
assert.equal(position(), 'translate3d(120px, 0, 0)', 'sync preserves the exact out-of-bounds position');
down(); move(20); el.emit('pointercancel', {});
assert.equal(position(), 'translate3d(120px, 0, 0)', 'cancel restores exact out-of-bounds visual baseline');
down(); move(20); el.emit('lostpointercapture', {});
assert.equal(position(), 'translate3d(120px, 0, 0)', 'native capture loss restores exact out-of-bounds visual baseline');
down(); move(-20); el.emit('pointerup', {clientX: -20, timeStamp: 30});
assert.equal(releases.length, 2, 'ordinary release after lost capture commits');
assert.equal(releases[1].x, 100, 'inward drag from synchronized overshoot reaches the real bound');
sync(120); down(); move(-30);
assert.equal(position(), 'translate3d(90px, 0, 0)', 'inward movement continues within bounds');
el.emit('pointercancel', {});
sync(-120); down(); move(20);
assert.equal(position(), 'translate3d(-100px, 0, 0)', 'inward drag reaches the lower bound');
el.emit('pointerup', {clientX: 20, timeStamp: 30});
assert.equal(releases.at(-1).x, -100, 'release preserves the lower bound');
const bounded = new Element(), boundedReleases = [];
const boundedSync = draggable(bounded, {min: -100, max: 100, onRelease: value => boundedReleases.push(value)});
const displayed = () => parseFloat(bounded.style.transform.match(/translate3d\(([^p]+)/)[1]);
for (const sign of [1, -1]) {
  boundedSync(sign * 500);
  assert.equal(displayed(), sign * 200, 'sync limits overshoot to one width');
  boundedSync(sign * 120);
  for (let i = 0; i < 10; i++) {
    bounded.emit('pointerdown', {timeStamp: i * 100});
    bounded.emit('pointermove', {clientX: sign * 10000, timeStamp: i * 100 + 20});
    assert.ok(displayed() <= 200 && displayed() >= -200, 'drag display remains within one width of bounds');
    bounded.emit('pointerup', {clientX: sign * 10000, timeStamp: i * 100 + 30});
  }
}
boundedSync(0);
bounded.emit('pointerdown', {timeStamp: 2000});
bounded.emit('pointermove', {clientX: 150, timeStamp: 2020});
const visualMove = displayed();
bounded.emit('pointerup', {clientX: 150, timeStamp: 2030});
assert.ok(Math.abs(boundedReleases.at(-1).velocity - visualMove / 30 * 1000) < 1e-8, 'release velocity follows displayed displacement');
const zero = new Element(), zeroReleases = [];
zero.clientWidth = 0;
const zeroSync = draggable(zero, {min: -100, max: 100, onRelease: value => zeroReleases.push(value)});
zero.emit('pointerdown', {}); zero.emit('pointermove', {clientX: 150, timeStamp: 20});
zero.emit('pointerup', {clientX: 150, timeStamp: 30});
assert.equal(zeroReleases[0].x, 100, 'zero width clamps to bound rather than NaN');
assert.equal(globalThis.testRubber(0, 0), 0, 'zero width and zero overshoot stay finite');
zeroSync.dispose();
// Disposal inside onRelease must not expose the browser's subsequent click.
const nativeSetTimeout = globalThis.setTimeout, nativeClearTimeout = globalThis.clearTimeout;
const timers = new Map(); let timerId = 0;
globalThis.setTimeout = fn => { timers.set(++timerId, fn); return timerId; };
globalThis.clearTimeout = id => timers.delete(id);
const flushTimers = () => { for (const [id, fn] of [...timers]) { timers.delete(id); fn(); } };
const disposedOnRelease = new Element();
let releaseSync;
releaseSync = draggable(disposedOnRelease, {min: -100, max: 100, onRelease: () => releaseSync.dispose()});
const clicksBefore = window.listeners.click.length;
disposedOnRelease.emit('pointerdown', {pointerId: 987});
disposedOnRelease.emit('pointermove', {pointerId: 987, clientX: 20, timeStamp: 20});
disposedOnRelease.emit('pointerup', {pointerId: 987, clientX: 20, timeStamp: 30});
assert.notEqual(disposedOnRelease.emit('click', {detail: 0}).prevented, true, 'keyboard click survives synchronous disposal');
assert.equal(disposedOnRelease.emit('click', {detail: 1, pointerId: 987}).prevented, true, 'drag click is suppressed after synchronous disposal');
assert.equal(window.listeners.click.length, clicksBefore - 1, 'suppression listener removed after click');
assert.notEqual(disposedOnRelease.emit('click', {detail: 1, pointerId: 987}).prevented, true, 'later click survives');
const noClick = new Element(); let noClickSync;
noClickSync = draggable(noClick, {min: -100, max: 100, onRelease: () => noClickSync.dispose()});
const beforeTimeout = window.listeners.click.length;
noClick.emit('pointerdown', {pointerId: 988}); noClick.emit('pointermove', {pointerId: 988, clientX: 20, timeStamp: 20});
noClick.emit('pointerup', {pointerId: 988, clientX: 20, timeStamp: 30});
flushTimers();
assert.equal(window.listeners.click.length, beforeTimeout - 1, 'suppression listener removed when no click arrives');
assert.notEqual(noClick.emit('click', {detail: 1, pointerId: 988}).prevented, true, 'expired suppression does not affect later clicks');
globalThis.setTimeout = nativeSetTimeout; globalThis.clearTimeout = nativeClearTimeout;
const multi = new Element(), multiReleases = [];
const multiSync = draggable(multi, {min: -100, max: 100, onRelease: value => multiReleases.push(value)});
multi.emit('pointerdown', {pointerId: 1});
multi.emit('pointerdown', {pointerId: 2});
multi.emit('pointermove', {pointerId: 2, clientX: 50});
assert.equal(multi.style.transform, '', 'other pointer cannot drag');
multi.emit('pointermove', {pointerId: 1, clientX: 20});
multi.emit('pointerup', {pointerId: 2, clientX: 50});
assert.equal(multi.capture, 1, 'other pointer cannot release capture');
const beforeDispose = Object.fromEntries(Object.entries(window.listeners).map(([type, listeners]) => [type, listeners.length]));
multiSync.dispose(); multiSync.dispose();
for (const type of ['pointermove', 'pointerup', 'pointercancel', 'click']) {
  assert.equal(window.listeners[type].length, beforeDispose[type] - 1, `dispose removes ${type} listener`);
}
multiSync(50);
assert.equal(multi.capture, null, 'dispose releases capture');
assert.equal(multi.style.transform, '', 'dispose restores pre-drag transform');
multi.emit('pointerup', {pointerId: 1, clientX: 20});
multi.emit('pointerdown', {pointerId: 1}); multi.emit('pointermove', {pointerId: 1, clientX: 30});
assert.equal(multiReleases.length, 0, 'disposed gesture never commits');
assert.equal(multi.style.transform, '', 'disposed listeners are inactive');
console.log('pointer gesture checks passed');
'''
        result = subprocess.run(['node', '-e', source + '\n' + check], cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
