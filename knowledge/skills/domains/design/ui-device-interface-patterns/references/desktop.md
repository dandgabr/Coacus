# Desktop and Workstation

## Context

Design for sustained work with a window that can shrink or move between monitors. Identify the command, its target document or selection, and whether a companion pane must remain visible while editing.

## Controls

Provide a discoverable path from menu, toolbar, or command chooser to each essential operation. Follow the target platform's standard key bindings and expose shortcuts alongside the named commands. For dense editable lists, define tab stops between regions and use the platform's internal navigation pattern inside a region. For ordinary move and reorder operations, give users a click or tap path, such as selecting an item and choosing a destination.

## States

Distinguish active window, focused control, and selected item through separate cues. When a dialog closes, return focus to its invoker if still available. When a row disappears, focus an available neighboring row or the list heading. Keep long-running actions and errors associated with the affected document.

## Accessibility

Verify keyboard and pointer operation separately. Use semantics for menu items, shortcuts, and dialog names. Check focus against high-contrast and dark appearances, including inactive windows, clipped scroll areas, and sticky toolbars.

## Evidence

The Commodore Amiga guide treats attention and feedback as part of interaction design. Apple describes per-window ordering in the early Aqua guide. Mac OS 8 documents focused controls for keyboard navigation. Use the [archive map](aresluna-source-map.md) to locate the relevant period editions. For a Workbench-inspired desktop, consult the [period GUI adaptation](../../ui-style-retro-computing/references/period-gui-appearance.md). For current keyboard patterns consult [GNOME Keyboard](https://developer.gnome.org/hig/guidelines/keyboard.html) and the applicable platform documentation.

## Validation

With keyboard alone, open a document, select an item, run a named command, dismiss its dialog, and confirm focus returns. Repeat after deleting the invoking item and after shrinking the window. Verify the indicated focus and the actual command target. Move another item using clicks or taps alone and confirm the destination without dragging.
