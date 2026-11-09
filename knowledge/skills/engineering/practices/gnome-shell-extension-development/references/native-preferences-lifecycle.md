# Native preferences lifecycle and observable actions

Use this reference when a GTK/libadwaita preferences page stops reacting to settings,
or when a green test does not match the person's experience of its controls.

## Navigation lifetime is not widget mapping

Widget mapping describes presentation, not ownership. A navigation page can unmap
during initial presentation, temporary window hiding or reparenting. Disposing its
subscriptions on every unmap can leave visible controls that still write settings
but never update their rows, labels or sensitivity. Instrument the active handler
identities before and after presentation, not only after the first button click.

For a terminal subpage, use the navigation page's semantic leaving signal and a
window-close path. The observed `Adw.NavigationPage` implementation uses `hiding`
instead of widget `unmap`; recheck these signals on the target runtime. If a page
can be covered and subsequently returned to, either retain subscriptions for that
navigation lifetime or recreate them when it becomes active. Make disposal
idempotent and disconnect only the handlers owned by that page.

Preserve focus on the logical connector while reordering retained widgets. When a
boundary disables the focused arrow, choose another enabled action in the same
row. Read the current registry and order for each action so an old callback does
not overwrite newly added sibling connectors. Keep Live and Demo presentation
settings independent; hidden popup cards still collect data unless separately
paused by the user.

## Test the action, persistence and displayed result

Trigger the actual control callback. Assert the written connector IDs and the
displayed row order after each up/down click, including repeated moves, boundary
sensitivity and focus. Assigning the expected setting directly before asserting
it proves the fixture, not the button. An unchanged view can be a lost subscription
even when the write succeeded; investigate the two boundaries separately.

Exercise adding a sibling after controls exist, external order/visibility changes,
temporary hide/restore, back/reopen and window close. Use synthetic scoped IDs in
Live as well as Demo. A registry test alone does not establish native GTK behavior.

Capture owned handler IDs before disposal. Verify that the runtime reports each
signal disconnected, for example with
[GObject.signal_handler_is_connected](https://docs.gtk.org/gobject/func.signal_handler_is_connected.html).
A tracking array returning to its initial length can pass while the actual
callbacks remain registered. In an isolated copy, omit the disconnect call and
require that test to fail; also revert the lifetime signal and omit the setting
write to prove the behavioral assertions catch their respective regressions.

## Evidence and limits

The [observed defect and fix](https://github.com/dandgabr/elfvision/blob/93b17f5192290e10de834125061735f3b9e3a270/docs/temp/popup-order-buttons-fix.md)
and [native GTK regression](https://github.com/dandgabr/elfvision/blob/93b17f5192290e10de834125061735f3b9e3a270/tests/prefsPopup.js)
record the tested navigation behavior on 2026-10-08. The original control test
passed while the rows remained stale; its strengthened form rejected that build.
Removing actual signal disconnection initially survived a handler-count check,
then failed the runtime connection assertion. Synthetic GTK and Shell probes do
not replace human accessibility acceptance or authorize real account changes.
