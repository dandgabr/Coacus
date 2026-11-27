---
name: ui-device-interface-patterns
description: "Designs interfaces for desktop, phones, tablets, foldables, stylus devices, smartwatches, smart TVs, interactive tabletops, AR, VR, and motion-controlled systems. Use when a UI must adapt to device posture, viewing distance, touch, pen, keyboard, remote or D-pad, rotating bezel, multi-user touch, gaze, or tracked motion."
---

# UI Device Interface Patterns

Identify the task, its physical setting, the user's position, the available controls and assistive technologies, and the input changes that can happen mid-task. Select the profile that governs the essential interaction. Combine profiles when two constraints apply, such as a pen tool within an adaptive tablet shell.

| Interaction or constraint | Profile |
| --- | --- |
| Windowed work with keyboard, trackpad, or mouse | [Desktop](references/desktop.md) |
| Handheld touch, hardware keys, or an adaptive pane layout | [Mobile and tablet](references/mobile-tablet.md) |
| Handwriting, drawing, or precise annotation | [Stylus](references/stylus.md) |
| A short task or glance from the wrist | [Wearables](references/wearables.md) |
| Viewing from a distance with a remote or directional pad | [TV](references/tv.md) |
| Multiple people gathered around a shared surface | [Tabletop](references/tabletop.md) |
| Gaze, tracked hands, head movement, or body gestures | [Spatial and motion](references/spatial-motion.md) |

## Specify the task across inputs

1. Name the critical task and its starting point. Describe what remains possible when the usual input is unavailable. Apply the applicable native or web accessibility requirements.
2. Specify activation, focus, selection, progress, cancellation, and recovery. Give critical actions visible names or platform semantics. Make focus discernible from selection and preserve it across temporary UI where practical.
3. Preserve content, drafts, and task position across window changes, external keyboard attachment, orientation changes, and suspension. Before replacing a control, specify where focus will land.
4. Choose a visual style once the interaction requirements are clear. In a retro-styled TV application, use the TV profile to define focus and remote behavior, then apply lineage cues from the requested visual style to readable surfaces.
5. Record the device, environment, input sequence, and observed outcome for each check. Verify essential paths on representative hardware and with supported assistive input. Record emulator and documentation evidence with their scope.

## Adapt the visual hierarchy

| Surface | Visual emphasis |
| --- | --- |
| Desktop | Give the active workspace clear boundaries. Keep document content, command groups, and selection visually distinct. |
| Phone and tablet | Give the primary task the first reading position. Preserve selected-item cues when a detail pane joins the layout. |
| Stylus | Give ink a quiet canvas. Mark the active tool and mode where the writing hand is unlikely to cover them. |
| Wearable | Give the primary value or action the strongest contrast and largest readable type. Keep secondary labels inside the usable shape. |
| TV | Use distance-readable labels and a focus treatment that survives bright or dark imagery. Reserve room around the focus ring. |
| Tabletop | Orient local labels to their participant and give shared state a consistent visual anchor. |
| Spatial or motion | Use stable text backing and readable depth separation. Give tracked targets and confirmed selections distinct cues. |

Use [app layout architectures](../ui-app-layout-architectures/SKILL.md) for navigation and shell composition. Use [UI motion interaction](../ui-motion-interaction/SKILL.md) for motion feedback. Use the [Aresluna source map](references/aresluna-source-map.md) to research a platform or edition. Treat historical evidence as context and verify present platform requirements with its publisher.

For web interfaces, check the applicable requirements for keyboard access, focus order and visibility, pointer gestures, alternatives to dragging, and target size. For native interfaces, check the current platform guidance and requirements that apply to its runtime. [W3C Web Content Accessibility Guidelines](https://www.w3.org/TR/wcag/).
