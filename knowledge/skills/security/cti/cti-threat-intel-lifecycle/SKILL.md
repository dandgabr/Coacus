---
name: cti-threat-intel-lifecycle
description: Acts as a Cyber Threat Intelligence lifecycle specialist covering intelligence requirements (PIR), collection, processing, analysis with structured analytic techniques, dissemination, the Admiralty source-reliability scale, estimative language and TLP 2.0 handling.
metadata:
  type: defensive
  phase: recon
---

# Cyber Threat Intelligence Lifecycle

This skill guides the AI to run the intelligence cycle end to end, from a question the business needs answered to a product the decision maker can act on.

---

## 🔄 1. The Cycle

1. **Requirements (PIR)**: state the priority intelligence requirements; intelligence without a question is trivia.
2. **Collection**: plan sources (OSINT, vendor, ISAC, internal telemetry) against the requirements.
3. **Processing**: normalize, deduplicate and store; this is where STIX/MISP data models matter.
4. **Analysis**: turn data into judgment using structured analytic techniques.
5. **Dissemination**: deliver BLUF-style products to the right audience with handling markings.
6. **Feedback**: did it change a decision? If not, the requirement or the product was wrong.

---

## 🔬 2. Analysis Discipline

- **Admiralty/NID source grading**: rate the source (A-F reliability) and the information (1-6 credibility), for example `B2`.
- **Structured analytic techniques**: Analysis of Competing Hypotheses, key-assumptions check, indicators and signposts; these counter confirmation bias, anchoring and mirror-imaging.
- **Estimative language**: express likelihood and confidence separately; "likely" and "we are confident" are different claims.

---

## 🛡️ 3. Handling and Sharing

- **TLP 2.0**: `TLP:RED`, `TLP:AMBER` (and `TLP:AMBER+STRICT`), `TLP:GREEN`, `TLP:CLEAR`; mark in the header and footer and never reclassify without the owner's consent.
- Share through ISACs/CERTs and platforms; the value of intelligence grows with legitimate sharing.
- Protect sources and methods; a leaked source ends collection.

---

## 📝 4. Product Forms

- **Strategic**: trends and risk for leadership.
- **Operational**: campaigns and actors for defenders.
- **Tactical**: TTPs and indicators for detection and hunting.
Match the product to the audience and the decision it informs.

---

## 🔗 5. Integration with Other Skills

- For ATT&CK mapping, see the [cti-mitre-attack](../cti-mitre-attack/SKILL.md) skill.
- For formats and platforms, see the [cti-platforms-stix-taxii-misp](../cti-platforms-stix-taxii-misp/SKILL.md) skill.
- For hunting from intelligence, see the [threat-hunting](../../operations/threat-hunting/SKILL.md) skill.
- For the analysis methods in depth, see the [academic-scientific-research](../../../domains/academic/academic-scientific-research/SKILL.md) skill.
