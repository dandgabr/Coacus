---
name: gnome-shell-extension-development
description: >-
  Provides practice for writing, checking and shipping a GNOME Shell extension in
  GJS: the layer split that keeps logic testable, the gates that catch what unit
  tests cannot import, verifying shell APIs against a live throwaway shell, the
  extension lifecycle (including the lock screen and suspend), notifications,
  settings and the preferences window. Use when building or reviewing a GNOME
  Shell extension, its preferences window or its notifications.
tags:
  - gnome-shell
  - gjs
  - extension
  - notifications
  - testing
---

# GNOME Shell extension development

An extension runs inside the desktop's own process, so a mistake costs more than
in an application: a module that fails to load disables the extension, a leaked
object survives it, and the platform decides things (the lock screen, Do Not
Disturb) that no setting of yours can override. This skill is the practice that
kept one extension honest through notifications, a preferences window and a
first-use flow. The facts it relies on were verified on a live shell; they are in
[the verified notes](references/gnome-shell-50-notes.md), with the version and the
date, and must be re-verified for another shell version.

## 1. Split by process and by layer

- **A pure core** holds every rule and every sentence the user reads: no GObject
  import, so it runs under the plain interpreter and the unit tests cover it.
- **Services** hold the I/O (timers, files, the keyring, the system bus). **The
  interface layer** only draws. **The preferences window is another process** (GTK
  and libadwaita); shell code never imports GTK, and the preferences never import
  the shell's toolkit.
- Enforce the split with a structure test that reads the imports: the core imports
  nothing outside itself, the shell toolkit stays in the interface layer, the
  notification API stays there too, and the system bus stays in the services.
- **Separate state from drawing.** A controller owns the state and the actions, and
  takes everything that touches the system as injected dependencies; each screen
  is a thin view over it. Two screens that sign in the same account then share one
  implementation, one sign-in at a time and one place to review, and the controller
  is testable with fakes: no keyring, no port, no browser.

## 2. Gates for what unit tests cannot import

The interface modules need the shell, so no unit test loads them. A name declared
twice, or not defined, is invisible until the extension is enabled, and then it
simply fails to load.

1. Check the **syntax of every module**.
2. **Enable the extension in a throwaway headless shell** and read its state and
   its error: the state must be enabled and the error empty. This is the gate that
   catches an undefined name.
3. **Look at it**: drive the interface in a throwaway shell and capture the screen.
   A passing gate does not say the icon is the right size.

A gate that has never failed is a hypothesis. Seed a defect (a name declared twice,
a name that does not exist), watch the gate fail, then restore the file and confirm
the diff is empty. Make the check script build its generated inputs first (the
compiled settings schema, the translation catalogs): a test that reads a stale
build fails for a setting it has never heard of.

## 3. Verify the shell API against a live shell

The shell's own scripts are compiled into its binary and cannot be listed or read.
An API recalled from an older version is a guess. In a throwaway shell with the
evaluation channel on, enumerate the prototypes, the GObject properties and the enum
values of what you are about to use, write against what you saw, and record the
version and the date. Confirm at least: the constructors and properties of the
notification classes, the urgency and privacy-scope values, how the session mode
reports a locked screen and where the notification settings live.

## 4. Lifecycle, the lock screen and suspend

- **Create after enabling, destroy when disabling**: sources, notifications, timers,
  signal handlers, bus subscriptions. A late event after disabling must create
  nothing, so the notifier keeps a destroyed flag.
- **Without the `unlock-dialog` session mode the shell disables the extension while
  the screen is locked.** Nothing of yours can then be on a lock screen, no alert is
  raised while locked, and a notification that was not read is gone after
  unlocking. Do not add a setting for what the platform already decides: a switch
  for details on the lock screen did nothing and was removed.
- The extension comes back on unlock, so what it needs to remember (what it already
  announced) lives on disk, and its memory must be longer than the longest lock:
  a quota that crossed its threshold during the lock is announced on the first look
  afterwards.
- **After suspend every timer is late at once** (they use the monotonic clock) and
  the data looks old. Subscribe to the login manager's sleep signal, hold connection
  alerts for a grace window, then refresh with jitter.

## 5. Notifications

- Use **a source of your own**; keep one notification per provider and kind and
  replace the old one rather than stacking.
- Urgency is **normal or high, never critical**: only critical bypasses Do Not
  Disturb. With it on, the banner is held for normal and high alike and the
  notification waits in the list. Actions do nothing while the screen is locked.
- **Text comes only from fixed, translated templates**, names from a registry and
  clamped numbers. Nothing a provider or a user typed reaches a notification or a
  tooltip: strip controls and bidirectional overrides, cap the length, turn markup
  off.
- **Quiet by construction.** Announce a crossing once and re-arm only after the
  value falls by a margin or the window resets; never announce the first reading;
  cap the number an hour and fold the rest into one summary; one connection alert
  per outage. A connection alert measured in time needs a clock, because a rejected
  sign-in is polled no more. Announce nothing until the set of providers is known.
- Offer a **test button** in the preferences that raises a counter the shell
  consumes. The assistant never sends a notification on its own.

## 6. Settings and the preferences window

- **Classify every settings key** as restored or kept by Restore defaults, in one
  list, with a test that fails for an unclassified key: a new setting must be
  decided about when it is added. Never reset what belongs to the user's accounts.
- **Reset in one batch** (delay then apply): the shell reacts to every key, and
  eighteen writes are eighteen rebuilds.
- A combo row must **not write back a value it only read**, or following a reset
  gives the key a user value again and the shell reacts twice.
- Read a setting once and refresh it on change, and **re-check it where it is used**:
  the user can edit it by hand.
- Dim a control when its master switch is off instead of blocking it, so the value
  stays visible. Show the current value in the row, not only inside it.
- A danger or terms confirmation has **one code path** used by every screen, with
  the safe response as the default.

## 7. Internationalization

- **Follow the session language.** Never change the locale of the process: it would
  translate the shell itself. A language without a catalog shows the source text.
- The extraction tool only sees **literal strings** inside the translation calls: a
  table of texts built outside them is invisible, so write the texts where they are
  translated. Keep the percent sign in the template (`%d%%`), because the language
  decides the spacing.
- A plain interpreter has no `String.format`: use a small printf, so the same code
  runs under the tests.

## 8. Checking a change

See [the verified notes](references/gnome-shell-50-notes.md) for the recipes: the
evaluation scope lacks the toolkit, a fresh shell opens a welcome dialog, a virtual
pointer that starts in the corner triggers the hot corner, an icon needs a size,
and one preferences page can be shown alone with a small harness and an in-memory
settings backend.
