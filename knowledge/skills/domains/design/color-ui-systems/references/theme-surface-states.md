# Theme Surfaces and Component States

Use this procedure when an appearance changes but its cards, controls or typography retain paint from another appearance. The product decides which appearances exist; a second appearance does not inherently require a new layout or motion.

## Trace the complete surface

Start with the semantic role, find the declaration that wins, then inspect the painted result. A valid token can be unused, overridden or obscured.

Inventory canvas, header, hero, cards, dialogs, tables, fields, notifications and decorative layers. For each, record foreground, muted ink, surface, boundary and focus roles. Inspect images, gradients, pseudo-elements, inline styles, filters, opacity, blend modes, text shadows and text fill as well as background color. A background image can keep painting after background color changes.

Replace the complete background declaration when its old layers no longer belong to the appearance. Preserve a useful texture when a local reading surface, position change or ink treatment solves the actual problem. Reassess the composition after the repair rather than judging each token in isolation.

## Review native and custom controls

| Component | States and paint to inspect |
| --- | --- |
| Checkbox/radio | Checked, unchecked, mixed where supported, indicator, surrounding label, keyboard focus and disabled |
| Range | Filled/unfilled track, thumb, focus, endpoint values and disabled |
| Switch | Off/on track, thumb position, accessible state, focus and label |
| Field | Input, placeholder, selection, autofill where relevant, error, focus and disabled |
| Table | Header, alternating rows, selected/hovered rows, separators and status labels |

Set native accent and color-scheme behavior intentionally when the platform offers them. Custom paint must preserve semantics, keyboard operation and the platform's high-contrast behavior. A native color is a defect when it contradicts the intended roles, not because that hue is categorically forbidden.

Changing a control's state must produce an understandable outcome. Compare both states after transitions settle and after removing incidental hover. Combine color with position, shape, text or another appropriate cue; a small token difference does not establish a perceptible state difference.

## Example role relationships

```css
.setting-control { accent-color: var(--action); }
.setting-switch { background: var(--control-off); }
.setting-switch[aria-checked="true"] { background: var(--control-on); }
.setting-switch::before { background: var(--control-thumb); }
.data-table th { color: var(--table-heading-ink); background: var(--table-heading-surface); }
```

These selectors and role names illustrate relationships, not a required component API. The component implementation owns its accessible state and interaction.

## Acceptance

Verify a real component in each supported appearance and important state. Check that intended roles are applied, painted contrast is sufficient, transitions do not expose an unreadable intermediate state, and the existing visual language remains recognizable. Pair this procedure with [painted contrast audits](../../color-contrast-accessibility/references/painted-contrast-audits.md).
