# GNOME Shell 50 notes

**Verified on:** GNOME Shell 50.5 (Fedora 44), in a throwaway headless shell started
with the unsafe mode, on 2026-10-07. Source of each fact: introspection of the live
shell through its evaluation channel, or a scripted run. Re-verify for another shell
version before relying on a name.

## Notifications (the message tray module)

- Exports: `ANIMATION_TIME`, `Action`, `MessageTray`, `Notification`,
  `NotificationApplicationPolicy`, `NotificationDestroyedReason`,
  `NotificationGenericPolicy`, `NotificationPolicy`, `PrivacyScope`, `Sound`, `Source`,
  `State`, `Urgency`, `getSystemSource`.
- `Urgency`: LOW 0, NORMAL 1, HIGH 2, CRITICAL 3. `PrivacyScope`: USER 0 (the default),
  SYSTEM 1.
- `Source` properties: `title`, `icon`, `icon-name`, `count`, `policy`. Create it with
  a title and an icon, then add it to the tray.
- `Notification` properties: `source`, `title`, `body`, `use-body-markup`, `gicon`,
  `icon-name`, `sound`, `datetime`, `privacy-scope`, `urgency`, `acknowledged`,
  `resident`, `for-feedback`, `is-transient`. Methods: `addAction`, `clearActions`,
  `activate`, `destroy`.
- A source's notifications are added with `source.addNotification(notification)`.
- Do Not Disturb is the `show-banners` key of `org.gnome.desktop.notifications`. With it
  off, neither a normal nor a high urgency notification shows a banner (the tray state
  stays hidden) and both stay in the source's list.

## Lock screen and session

- The session mode reports a locked screen through `isLocked`.
- An extension without the `unlock-dialog` session mode is disabled when the screen
  locks: after the lock call, the extension object has no notifier and its panel item is
  gone. The lock-screen capture of a headless shell is black.

## Evaluation scope and test recipes

- The scope has `Main`, `Gio`, `GLib` and `Shell`, but not `Clutter`: import it with
  `imports.gi.Clutter`.
- A fresh shell opens the welcome dialog and the overview. Close the dialogs found in
  `Main.layoutManager.modalDialogGroup` and hide the overview before driving it.
- A virtual pointer device starts at the top-left corner and that triggers the hot
  corner: move it to the middle of the screen first, then to the target.
- An icon without an explicit size renders huge in a row: give it one.
- One preferences page alone: a small program that builds the page with the settings
  schema and an in-memory settings backend and presents it in a preferences window inside
  the headless shell. Open the dialogs from the program, then capture the screen.
- The throwaway shells have their own empty keyring, so no account is connected: start
  them with made-up data to see the interface working.
- `String.prototype.format` exists in the shell and in the preferences process but not in
  a plain interpreter.
