# Interface State and Resource Ownership

Use when visual overrides, asynchronous loading or effects interfere with navigation and controls.

## Semantic state precedes decoration

Check the actual component tree before selecting nodes or defining layout. Theme selectors must not expose an inactive view by overriding its hidden state. Verify the expected active panel count, reachable controls, focus and absence of active work owned by inactive views.

Distinguish an inaccessible label, a visually hidden label and a visible element excluded from the accessibility tree. These are different states, not interchangeable audit filters.

## Transactions and failures

For a replaceable stylesheet, catalog or data request, identify the requesting context and invalidate stale results. Apply a coherent result or restore the previous/default state through the product's explicit fallback policy. Do not persist success before the required content is ready.

A decorative effect failure can preserve a complete static composition. A failure of essential content needs an appropriate error or fallback. Clean up resources belonging to the failed or superseded request even when its promise resolves later.

## Controls, tours and preferences

Test pointer and keyboard activation, accessible state and visible feedback together. State represented only by a class, or by two almost identical colors, is not a complete interaction contract. Review [theme surface states](../../../domains/design/color-ui-systems/references/theme-surface-states.md) for native and custom control paint.

Separate context help about the current item from whole-product onboarding. Both need accurate links and text after selection changes; a contextual tour need not repeat the entire onboarding sequence.

When a preferences dialog has Accept/Cancel semantics, distinguish pending from committed values. Cancel, Escape and close discard pending changes unless the product explicitly uses another save model. Preserve focus restoration. Do not add confirmation dialogs to actions already authorized outside that product flow.

## Ownership and geometry

Define which context owns listeners, observers, timers, animation callbacks, canvas, injected nodes and temporary styles. Mount only what the context needs and release those resources when it changes. Restore inline styles only if the effect owned the change.

Choose whether decoration covers the visible viewport, a scroll container or complete content. Check start, middle and end, resize and nested stacking contexts. Numeric layer order alone does not prove visible overlap. Use [rendered verification](../../../engineering/practices/ui-design-craftsmanship/references/rendered-interface-verification.md) and [effect lifecycle](../../../domains/design/ui-motion-interaction/references/effect-coverage-lifecycle.md).
