---
name: ai-governance-iso-42001
description: Acts as an AI Governance and Assurance specialist covering ISO/IEC 42001 (AI Management System), 42005 (impact assessment), 23894 (AI risk), 27090 (AI security threats), the NIST AI RMF and its Generative AI Profile, and the EU AI Act risk tiers and timelines.
metadata:
  type: defensive
  phase: report
---

# AI Governance and Assurance

This skill guides the AI to establish an auditable management system for AI, distinct from securing a specific model.

---

## 🏛️ 1. Management System (ISO/IEC 42001)

An **AI Management System (AIMS)** follows a Plan-Do-Check-Act structure like other ISO management systems: scope, leadership, planning, support, operation, performance evaluation and improvement. Use **ISO/IEC 42005** for AI system impact assessment and **ISO/IEC 23894** for AI risk management.

---

## ⚠️ 2. Risk Frameworks

- **NIST AI RMF 1.0**: the Govern, Map, Measure and Manage functions; the Generative AI Profile (NIST AI 600-1) extends it with GenAI-specific risks.
- **ISO/IEC 27090**: AI security threats, linking AI risk to the security program.
- **Google SAIF**: a 15-risk taxonomy that is practical for engineering teams.

---

## 🇪🇺 3. EU AI Act

- **Unacceptable-risk** practices are prohibited.
- **High-risk** systems carry the heaviest obligations: risk management, data governance, technical documentation, human oversight, accuracy and cybersecurity.
- **Limited-transparency** systems require disclosure (for example, that the user is interacting with an AI).
- **Minimal-risk** systems have no specific obligations.
- Timeline: prohibitions and AI literacy applied from February 2025; general-purpose AI obligations from August 2025; the remainder applied from August 2026; high-risk obligations phase in later. Verify dates against the official implementation timeline before asserting them.

---

## 📋 4. Assurance Artifacts

- **Model cards** and system documentation.
- **AI BOM**: training data provenance, model and dependency inventory.
- **Impact and risk assessments** with owners.
- **Incident response** for AI failures and misuse.

---

## 🔗 5. Integration with Other Skills

- For AI security specifics, see the [ai-llm-slm-security](../../ai/ai-llm-slm-security/SKILL.md) and [ai-adversarial-ml-security](../../ai/ai-adversarial-ml-security/SKILL.md) skills.
- For agentic risk, see the [ai-agentic-security](../../ai/ai-agentic-security/SKILL.md) skill.
- For the ISMS overlap, see the [iso-27000-series](../iso-27000-series/SKILL.md) skill.
- For the general GRC program, see the [security-grc-compliance](../security-grc-compliance/SKILL.md) skill.
