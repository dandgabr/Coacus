# Runtime Consent and Erasure Evidence

Use when verifying an implementation of an agreed privacy policy. Legal applicability belongs to [security privacy](../../security-privacy/SKILL.md); this reference owns operational evidence.

## Purpose by state

For each purpose, state its allowed behavior and compare it with observed requests, payloads and stored identifiers. Exercise first visit, rejection, granular acceptance, reload, return visit and withdrawal. Include delayed tags, client-side navigation and stale stored preferences where the product uses them. Withdrawal must propagate to affected processors and must not be undone by subsequent navigation.

Separate storage consent from transmission: denied storage can coexist with cookieless requests. Compare those requests with the intended policy rather than treating them as an automatic pass or violation. Record viewport/session setup, state transition, relevant observations and untested server boundaries. Do not collect real user payloads into review artifacts; use synthetic data and redacted evidence.

## Erasure and restoration

Map live stores, caches, logs, processors and backups. For each, record deletion, justified retention, pending work, restricted use and expected expiry. A subject-linked audit hash may remain personal data; hashing alone is not a universal retention justification.

Define restoration handling so a backup does not silently reactivate previously erased processing. Reapply applicable deletion or restriction before exposing restored data. Explain remaining retention and processor limitations to the requester. Keep evidence minimal and tied to a justified purpose rather than assuming that immutable audit records are always safe.

## Acceptance examples

- Reject optional analytics, navigate and reload: observe whether delayed tags or saved preferences reactivate the purpose.
- Withdraw a previously accepted purpose: verify storage and downstream consequences, not only the switch label.
- Restore a backup containing an erased account: confirm the deletion/restriction is reapplied and report pending processor work honestly.

These checks require actual project resources to prove runtime behavior. A reasoning-only evaluation can assess the proposed checks, not claim their execution.

## Sources

Reviewed 2026-10-27; this procedure is Coacus synthesis.

- [Google consent behavior](https://developers.google.com/tag-platform/security/concepts/consent-mode).
- [LGPD retention and rights](https://www2.camara.leg.br/legin/fed/lei/2018/lei-13709-14-agosto-2018-787077-normaatualizada-pl.html).
- [ICO erasure guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/individual-rights/right-to-erasure/): UK-specific backup guidance, not an automatic interpretation of Brazilian law.
