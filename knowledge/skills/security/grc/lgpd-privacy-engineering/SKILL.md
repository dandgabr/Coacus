---
name: lgpd-privacy-engineering
description: >-
  Guides Brazilian LGPD software assessments from evidence collection to a
  personal data map, processing records (ROPA), lawful basis review, legitimate
  interest assessment (LIA) and impact report (RIPD). Use for Brazilian privacy
  design, legacy audits, small processing agent eligibility, data subject
  rights, cross-border data flows or a suspected personal data incident.
tags: [privacy, brazil, governance]
---

# Brazilian Privacy Engineering

Use the [Brazilian LGPD sources](references/brazilian-lgpd-sources.md) to resolve
applicable text and effective dates. Link each proposed legal conclusion to the
specific rule and the facts that make it applicable. Flag inaccessible sources,
unknown facts and legal decisions awaiting review.

## Triage first

- For an active or suspected personal data incident, alert the project incident
  owner and use the [Brazilian incident procedure](references/lgpd-operations.md#security-incident).
  Start the timeline and identify authorized containment and evidence
  preservation steps before routine discovery. Keep affected people and
  regulatory communication decisions in scope.
- For a new feature, distinguish design plans from deployed behavior. For an
  existing product, inspect the implementation and prioritize findings by
  harm to people, urgency and confidence. For a mixed project, keep those
  evidence states visible for each activity.
- Assess LGPD territorial and material scope before proposing controls. Load
  `brazil-eca-digital` when children or adolescents in Brazil are the intended
  or likely audience, or relevant age-restricted features are present. Review
  the child's best interests for personal data processing independently of
  Digital ECA scope.

## Build the record

1. Map an activity per purpose and legal role. Trace collection, use,
   inference, storage, disclosures, remote access and disposal. Check schemas,
   routes, browser or mobile storage, SDK configuration, telemetry, jobs and
   infrastructure. Cite redacted evidence by path, revision or test record.
   Label findings as observed in source, observed in runtime, declared by the
   owner or supplier, planned, or unknown. Link each activity across artifacts
   with the same stable ID.
2. Record the proposed legal basis for each purpose. Use the rules for ordinary
   and sensitive data separately. For legitimate interest, document purpose,
   strict necessity, balancing and safeguards. Determine who makes processing
   decisions, who acts on instructions and who owns the privacy contact.
3. Consolidate the reviewed activities into a ROPA. Assess small processing
   agent eligibility before selecting a simplified record or deadline.
   Determine the reason for each RIPD and assess harm to people, control
   evidence and residual risk. Use the [decision and drafting procedure](references/lgpd-operations.md).
4. Record the responsible owner, evidence still needed, decisions pending
   review and when to reopen the work. Draft a notice from the reviewed ROPA
   when requested. Require authorized review before treating a basis, contract,
   public notice or filing as approved.

Read-only assessment produces findings and draft content. Write project
artifacts only within the requested scope. Use redacted or synthetic evidence
and approved restricted storage for sensitive material. Report the limits of
repository review, including unverified contracts and production settings.

## Handoffs

Use `security-privacy` for general privacy design and `consent-dsr-automation`
for implementation and verification of consent, rights and erasure. Use
`third-party-risk-management` for due diligence and
`incident-response-blue-team` for operational incident response. Apply the
[Brazilian procedures](references/lgpd-operations.md) to their respective
records, notices and deadline decisions.
