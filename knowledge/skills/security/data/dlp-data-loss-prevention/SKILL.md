---
name: dlp-data-loss-prevention
description: Acts as a Data Loss Prevention specialist covering endpoint, network and cloud DLP, infoType detection, inline redaction, CASB integration, LLM prompt scrubbing and the tuning of DLP to avoid both leaks and alert fatigue.
metadata:
  type: defensive
  phase: actions
---

# Data Loss Prevention (DLP)

This skill guides the AI to detect and prevent sensitive data leaving the places it is allowed to be.

---

## 🧭 1. DLP Surfaces

| Surface | Scope | Notes |
| :--- | :--- | :--- |
| **Endpoint** | Data copied to USB, printed, or pasted into personal apps | Highest fidelity, highest friction |
| **Network** | Data leaving through web, email or proxies | Sees egress; struggles with encrypted traffic |
| **Cloud / CASB** | SaaS sharing, cloud storage, API payloads | Where modern data actually moves |
| **LLM prompts** | Data pasted into AI tools | A new egress channel; inline redaction matters |

---

## 🔬 2. Detection Primitive

An **infoType** combines a pattern (regex, checksum, dictionary) with **context** (surrounding words, proximity) and a **likelihood** score. A bare regex produces noise; context is what makes DLP usable.

---

## ⚖️ 3. Action Ladder

1. **Log** - observe without interfering; use during tuning.
2. **Alert** - notify the security team.
3. **Warn** - notify the user and ask them to confirm.
4. **Block** - prevent the action.
5. **Quarantine** - hold the data for review.
6. **Auto-tag** - classify the data for downstream controls.

Move down the ladder deliberately per data class; blocking everything on day one guarantees the program loses user trust.

---

## 🎯 4. Tuning

- Establish a baseline and measure false positives per rule before enforcing.
- Use allowlists for legitimate business flows rather than loosening the detection.
- Review top triggers weekly; DLP decays without tuning.
- Redact rather than block where the business need is legitimate (for example, scrubbing PII from an LLM prompt).

---

## 🔗 5. Integration with Other Skills

- For discovery and classification, see the [data-classification-dspm](../data-classification-dspm/SKILL.md) skill.
- For privacy governance, see the [security-privacy](../../grc/security-privacy/SKILL.md) skill.
- For cloud data movement, see the [cloud-security-posture-cnapp](../../cloud/cloud-security-posture-cnapp/SKILL.md) skill.
- For AI prompt handling, see the [ai-llm-slm-security](../../ai/ai-llm-slm-security/SKILL.md) skill.
