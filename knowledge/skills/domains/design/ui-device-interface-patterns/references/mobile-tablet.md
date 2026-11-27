# Phones, Tablets, and Foldables

## Context

Design for interruption, available window space, and device posture. Consider touch, external keyboards, trackpads, and legacy hardware keys when the specified device offers them. Use the app window and hinge or inset information as layout inputs.

## Controls

Use one pane where two panes would make the primary work unreadable. When space permits, show the list and selected detail together. Reserve visible affordances for core operations that also have swipe or long-press shortcuts. Let system navigation and the on-screen keyboard retain their normal behavior.

## States

Keep selection, scroll position, unsaved input, and validation messages as the shell changes. When a split view collapses while someone is editing, preserve the detail and expose a return to its parent list. If selection is empty, show the relevant list or an empty detail with a clear next action.

## Accessibility

Test text enlargement and the software keyboard together. Check controls inside safe areas, beside fold regions, and above transient panels. Preserve semantic order and tab or switch navigation when the user changes input in an unchanged window.

## Evidence

Apple's 2008 iPhone guide addresses the primary task, touch gestures, and rotation. Its 2010 iPad guidance illustrates different arrangements of the same mail content across orientations. Nokia's Touch and Type guide covers combined keys and touch. See the [archive map](aresluna-source-map.md) and [Android adaptive guidance](https://developer.android.com/develop/adaptive-apps/guides/adaptive-dos-and-donts) for current window and input handling.

## Validation

Start an edit on a compact screen, expand into a two-pane view, attach a keyboard, rotate or resize, and collapse back while editing. Verify the same record and draft, reachable actions, and sensible focus and back behavior after each transition.
