---
name: desktop-app-distribution
description: >-
  Provides packaging, installation and login-start practice for a cross-platform
  desktop application. Use when choosing what to distribute, installing a build
  on a workstation, or wiring an app to start at login on Linux, Windows or
  macOS.
tags:
  - packaging
  - installation
  - autostart
  - desktop
---

# Desktop App Distribution

How a desktop application reaches a machine and starts itself there. The work
splits into three decisions made in this order: **what to ship**, **how to
install it**, and **how it comes back at login**. Each decision constrains the
next, so settling the delivery channel first is not optional.

## 1. Choose the artifact from the update channel, not the OS alone

The update mechanism picks the format. A bundle the app can replace in place and
a bundle the operating system's package manager owns follow different rules, and
mixing them produces an install that silently stops updating.

| Channel | Ships | Updater | Installs with |
|---|---|---|---|
| Self-contained image (AppImage, portable archive) | one executable file | the app replaces the file itself | no privilege, per user |
| Native package (`.deb`, `.rpm`, MSI, `.dmg`) | package manager metadata | the package manager | elevated, system-wide |

- **A self-contained image is the only form the app can update itself.** The
  updater must know which file to replace; an image run from a path it can
  rename can update itself, a package installed under a system prefix cannot.
  When a package-manager install would make an in-place update impossible,
  suppress the update affordance instead of offering one that fails.
- **A per-user install needs no elevation.** Prefer it when the app is a
  user-session program: it avoids `sudo`, keeps the uninstall local, and removes
  a class of permission failures. Reach for a system install only when policy
  requires it.
- **Name the moving file stably.** Install a versioned image under a stable
  name (for example `app.AppImage`, not `app-1.4.2-x86_64.AppImage`) so the
  login entry, the updater and the user's shell shortcuts do not need editing on
  every release.

### Before trusting a downloaded binary

A distributed artifact is a claim until its provenance is checked. Confirm the
binary was built from the source you have, then verify its signature where the
project publishes one.

- Compare the checkout against the release tag before downloading: the peeled
  tag commit and `HEAD` must be the same commit. A tag that points at a
  different commit is a different build.
- Prefer the platform's signed artifact and its detached signature; verify both.
- Record the version and the artifact path where the install is described, and
  prefer a stable name for the installed copy.

## 2. Install and verify the running surface

Installing a desktop app is not finished when the files land. A tray app in
particular depends on session services that a headless check never exercises.

- **Confirm the runtime it needs, per family, before installing.** A graphical
  session (Wayland or X11), a notification service, and a secret store are
  common requirements; a missing one shows as a silent failure, not an error.
  Probe the distribution family first (see the process conventions' "Measure the
  environment before a command") rather than assuming a package manager.
- **Verify the tray/panel surface on the running session.** On Linux a tray icon
  is a StatusNotifierItem, which needs a StatusNotifier host (GNOME needs the
  AppIndicator extension; KDE, LXQt, MATE, Cinnamon and waybar host it natively;
  XFCE needs a plugin). Query the session bus for the watcher and for the app's
  own item instead of assuming the icon appeared.
- **Verify single-instance behavior.** A login start plus a manual start must
  join the running instance, not build a second tray. Launch twice and confirm
  one process remains.

## 3. Start at login: a per-user login item, never a service

A tray GUI needs a graphical session, a notification bus and a secret store. A
system service runs with none of those, so the correct mechanism is always a
**per-user login item**. The user's own switch outranks the app's.

### The three formats

| OS | Entry | Notes |
|---|---|---|
| Linux | `~/.config/autostart/<app>.desktop` | honours `$XDG_CONFIG_HOME`; `Exec=` is shell-style |
| Windows | a value under `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` | per-user, no elevation |
| macOS | `~/Library/LaunchAgents/<app>.plist` | `ProgramArguments` is an array; `RunAtLoad` starts it once |

### The file is the intent; the OS entry is derived from it

On every launch, reconcile the OS entry to the configured intent. Reconcile
idempotently, and reconcile **without holding a shared lock across the OS
probe** — read the intended value, release the lock, then probe the OS.

### Distinguish four states, not a boolean

"Absent" and "the user turned it off" need different answers:

- **installed** — present, points at this executable, and the OS will run it;
- **absent** — nothing of ours is installed;
- **disabled** — present but the user (or the desktop) disabled it;
- **moved** — present but points at a different executable (a relocated image).

Then: enabled + absent/moved → write or repair; disabled in the file + present →
remove; **enabled in the file + disabled in the OS → leave it alone**. The
machine's own control outranks the file; re-enabling every launch is the app
fighting the user.

- Linux: a disable is `Hidden=true` or `X-GNOME-Autostart-enabled=false` in the
  entry.
- Windows: the `Run` value stays in place while the user's choice is recorded as
  a `StartupApproved\Run` value — read it, or the switch reports ON while Windows
  will not start the app.
- Reconcile must be **non-fatal**: a host that refuses the write (a read-only
  home, a locked registry) must not stop the app from running. Log, do not abort.

### Write the entries correctly

- **Quote and escape the executable path.** In an `Exec=` line and a Windows
  `Run` value, an unquoted path with a space is parsed as a truncated command
  (`C:\Program Files\...` runs `C:\Program`). Wrap the path, escape backslash,
  double-quote and `%` for `Exec`, and escape `&`, `<`, `>` for the plist XML —
  an unescaped ampersand makes the plist unparseable and the agent silently
  never loads.
- **Point at the real launch target.** An image that runs from a temporary mount
  has a binary path that disappears after exit; the entry must name the image
  variable (`$APPIMAGE`) rather than the extracted executable. Everywhere else,
  the running executable is right — and a set-but-empty variable must not win
  over a valid path and leave an `Exec=""`.
- **Pass a "started at login" argument** so the app knows it was launched
  unattended: with no tray it should stay in the background instead of popping a
  window at login.
- **Keep the entry name in one place.** The Windows value name, the Linux file
  stem and the macOS plist label must be a single literal, or the read finds
  what the write did not produce.

### Apply the OS effect after the durable state

Write the configuration, redraw the UI, **then** apply the OS effect. If the OS
step fails, the value the user chose is already saved and visible, and the error
is reported afterwards — not a half-applied toggle that looks broken.

## 4. Do not use a library that gets these wrong

A convenience dependency for autostart is worth auditing before adopting. Two
defects are common and both are correctness bugs a monitor must not inherit:
paths written **unquoted** (broken on any install location with a space), and
the Windows startup switch rewritten after the user cleared it in Task Manager.
The three entry formats are small; owning them keeps the quoting and the escapes
provable. Prefer a tested, pure entry builder over an opaque dependency.

## Verification checklist

Before calling an install done:

- The installed binary names a stable path, and its provenance was checked.
- The app runs on the target session, and its tray/panel item is registered.
- A second launch joins the first (single instance).
- The login entry exists, is valid, names the current executable, and carries the
  login-start argument.
- The settings switch reads the **OS** state, so it tells the truth even when the
  entry was changed outside the app.
- Disabling it in the OS leaves it disabled; moving the executable is repaired on
  the next launch.

## Related Skills

- [vcs-repository-management](../vcs-repository-management/SKILL.md): provenance
  and release-tag discipline the download check relies on.
- [documentation-designer](../documentation-designer/SKILL.md): writing the
  install and startup steps as durable how-to documentation.
- [linux-kernel-systemd-internals](../../../infrastructure/linux-kernel-systemd-internals/SKILL.md):
  why a login item and not a system service, and the systemd user context.
- [framework-qt6](../../../frameworks/framework-qt6/SKILL.md): a desktop toolkit
  whose deployment and platform integration this skill complements.
