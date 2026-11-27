---
name: brazil-eca-digital
description: >-
  Assesses products under Brazil's Digital ECA when children or adolescents are
  intended or likely users, or age-restricted features are in scope. Use for
  age assurance, protective defaults, parental supervision, child safety
  impact assessment or CNCA and NIDUS reporting readiness.
tags: [privacy, brazil, child-safety]
---

# Brazilian Digital ECA

Start with the [Brazilian Digital ECA source register](references/brazilian-digital-eca-sources.md).
Verify the current law, implementing rules and reporting phase before giving a
compliance recommendation. Use `lgpd-privacy-engineering` for the separate
purpose, legal basis and safeguards of personal data processing.

1. **Classify the product and its audience.** Identify the product or service,
   provider role, Brazil availability and intended users. If children or
   adolescents are the intended audience, record the supporting facts. For
   likely access, assess attractiveness and probability of use, ease of access
   and relevant risk together. Evaluate the ANPD guide's rebuttable product
   categories and any applicable scope exception. Document actual product
   features rather than relying on an age label or a contractual restriction.
2. **Evaluate by feature and provider role.** Consider age assurance, access
   restrictions, protective defaults, supervision, messaging, games,
   advertising, spending, recommendation and reporting where applicable.
   Distinguish the duties of the application provider, app store and operating
   system. Check the role and age conditions for linking a guardian account.
3. **Design and verify controls.** Minimize age data and restrict its use to
   the authorized purpose. Provide age-classification challenge and correction
   handling. For the restricted access covered by Article 9(1), require
   reliable verification at every covered access and exclude self-declaration
   as the method. Require the covered provider's own access protection
   independently of store or operating-system signals. Use the more protective
   result when the Decree applies to conflicting sources. Use synthetic accounts and
   redacted evidence for pass, block, uncertainty and correction cases.
4. **Record impact and response.** For a covered product, document the
   child safety and health impact assessment and prepare its public summary
   for authorized review. Assess the separate Article 31 transparency
   threshold. Identify the protection owner and approved reporting and
   removal channels. Read the [NIDUS transition](references/brazilian-digital-eca-sources.md#nidus-registration-and-reporting)
   before deciding whether registration or a filing applies.

## Review record

Use one row per feature or product boundary. Record evidence and an owner even
when a conclusion remains open.

| Product or feature | Audience and risk evidence | Role and applicable source | Control and observed result | Open decision, owner and review date |
| --- | --- | --- | --- | --- |
| [Scope] | [Audience, access, attractiveness, risks] | [Role, article, version and applicability] | [Planned or observed evidence] | [Decision and next check] |

Record findings, restricted evidence references and draft artifacts within the
requested scope. Route real incidents promptly to authorized safety and
response teams. Keep sensitive content, credentials and personal identifiers
out of routine review artifacts.
