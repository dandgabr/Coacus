# Stylus and Pen Input

## Context

Separate precision tasks such as handwriting or drawing from the surrounding navigation and file operations. Identify the pen capabilities actually available, including hover, pressure, tilt, eraser, and cancellation signals.

## Controls

Expose ink, select, pan, and erase through named mode controls where relevant. Use pen or touch shortcuts as accelerators and give their equivalent commands a visible path. Offer usable default ink when pressure or tilt is absent. Assign finger input to navigation or drawing according to the declared mode.

## States

Show the active mode near the work, give immediate stroke feedback, and commit each accepted stroke as an undoable operation. Keep provisional changes scoped to their pointer so cancellation can remove a rejected contact without undoing a valid stroke. Show a recoverable state if recognition is uncertain.

## Accessibility

Allow keyboard, touch, or assistive input to navigate surrounding UI, export, undo, organize, and enter text. Allow a non-gesture path for annotation operations that can be expressed through controls. Identify cases where producing a particular freehand mark is itself the task.

## Evidence

GO's PenPoint guide gives gestures and visible controls a dual command path. Apple's Newton guide covers pen-oriented input fields and text entry. See [archive editions](aresluna-source-map.md) and current [Android stylus input guidance](https://developer.android.com/develop/ui/compose/touch-input/input-compatibility-on-large-screens).

## Validation

Draw one stroke while resting the other hand on the display. Confirm the intended stroke remains after a rejected contact, then undo it and use the keyboard or touch to rename and save the document. Repeat without a pressure-capable pen.
