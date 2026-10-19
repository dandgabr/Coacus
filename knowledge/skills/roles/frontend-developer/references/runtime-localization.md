# Runtime Localization and Reversible State

Use when a running interface changes language without reloading. Translation quality and runtime state are different responsibilities; language specialists can review wording while the interface preserves behavior.

## Preference, negotiation and presentation

Keep the user's stored choice distinct from the resolved language. An automatic choice can follow an ordered device-language list without becoming a manual preference for the first resolved locale. Use the product's supported aliases and fallback policy; do not hard-code the author's language as a universal fallback.

Keep stable identifiers, route keys and appearance identifiers separate from localized display names. A default appearance can be light or dark; pressed state should describe the selected alternative, not assume one fixed polarity. Preserve route, selected view, data and focus when language or appearance changes.

## Reversible translation

For each source text or attribute, retain a reliable original or stable translation key. On every change, apply the selected translation or restore the defined source/fallback. Skipping a missing translation can leave text from the previously selected language in place.

Cover visible and inactive views, placeholders, accessible names, titles, dialogs, generated labels and effect-injected text. Localize numbers and units through the appropriate locale facilities. Refresh context-dependent tour text and links so they refer to the current item.

Test a cycle through source language, a different writing system and back, followed by reload and a change while another view is selected. Test missing keys explicitly. Key-set equality alone does not prove the DOM was restored.

## Direction, fonts and storage

Update language and direction metadata; isolate addresses, codes and other embedded directional text as appropriate. Check long words, font fallback and loading, and the actual component widths in left-to-right and right-to-left compositions.

Normalize unsupported or obsolete persisted values through the product's migration policy. If storage is unavailable, keep the interaction usable with the appropriate session state. Do not delete unrelated preferences to make one selector work.

## Async updates and failure

Bind an asynchronous load to the selection that requested it. Discard a late response when a newer route, language or appearance owns the view. A fallback should restore a coherent state, announce the outcome where useful and normalize persistence consistently; it should not leave half the interface in another appearance.

Inspect the dependency graph when a correct local implementation behaves differently after publication. A fresh document importing a cached catalog or registry can imitate a localization defect. See [published artifact verification](../../devops-engineer/references/published-artifact-verification.md).
