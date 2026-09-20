---
name: consent-dsr-automation
description: Acts as a Consent and Data Subject Request automation specialist covering consent capture and lifecycle, Global Privacy Control, DSR/DSAR orchestration, identity verification, cascading erasure and the audit evidence required by LGPD and GDPR.
metadata:
  type: defensive
  phase: report
---

# Consent and Data Subject Request Automation

This skill guides the AI to operationalize the rights that privacy law grants to individuals.

---

## ✅ 1. Consent Management

- Capture consent **granularly** (per purpose, per data category) with proof: what was shown, what was agreed, when, from where.
- Make withdrawal as easy as giving consent, and propagate the withdrawal to processors and downstream systems.
- Honor **Global Privacy Control** (GPC) signals as an opt-out of sale/sharing where the law requires it.
- Never infer consent from silence or from a pre-ticked box.

---

## 📨 2. DSR/DSAR Automation

1. **Intake**: a single channel that logs every request with a timestamp.
2. **Verification**: confirm the requester's identity without collecting more data than necessary.
3. **Discovery**: find all data for the subject across systems, including backups and processors.
4. **Fulfilment**: export (portability), correct, delete, or restrict, per the applicable right.
5. **Deadline tracking**: GDPR generally one month (extendable); LGPD has its own clocks.
6. **Evidence**: record what was returned, the legal basis for any refusal, and the completion.

---

## 🗑️ 3. Cascading Erasure

Deletion must reach transactional databases, logs, analytics replicas, caches and processors, while preserving only what the law requires (for example, immutable audit hashes or financial records under a retention obligation). Document the exceptions and their legal basis.

---

## 🔗 4. Integration with Other Skills

- For the privacy program, see the [security-privacy](../../grc/security-privacy/SKILL.md) skill.
- For data discovery across systems, see the [data-classification-dspm](../../data/data-classification-dspm/SKILL.md) skill.
- For the retention and disposal schedule, see the [data-mesh-governance](../../../data/data-mesh-governance/SKILL.md) skill.
- For the audit evidence, see the [grc-automation-oscal](../grc-automation-oscal/SKILL.md) skill.
