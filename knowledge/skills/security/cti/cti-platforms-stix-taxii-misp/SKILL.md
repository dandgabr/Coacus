---
name: cti-platforms-stix-taxii-misp
description: Acts as a CTI Platform specialist covering the STIX 2.1 object model, TAXII 2.1 collections and channels, MISP taxonomies, galaxies and machine tags, OpenCTI data modeling, and the indicator taxonomy used to exchange threat intelligence.
metadata:
  type: defensive
  phase: recon
---

# CTI Platforms and Data Exchange (STIX, TAXII, MISP)

This skill guides the AI to exchange threat intelligence in standard, machine-readable form.

---

## 🧩 1. STIX 2.1

- **STIX Domain Objects** include Threat Actor, Intrusion Set, Campaign, Attack Pattern, Malware, Tool, Infrastructure, Indicator, Observed Data, Vulnerability, Identity, Location, Course of Action, Grouping, Note, Opinion and Report.
- **Relationship Objects** link them (Relationship, Sighting); STIX Cyber Observable Objects can be related directly.
- **Confidence** is a first-class property; use it rather than implying certainty in prose.
- An Indicator is "based-on" Observed Data; keep the chain so consumers can see the evidence.

---

## 📡 2. TAXII 2.1

- A RESTful HTTPS protocol for CTI exchange with **Collections** (request/response) and **Channels** (publish/subscribe, reserved).
- **API Roots** group collections; discovery happens at `/taxii2/` (and via a DNS SRV record).
- The **TAXII Envelope** replaced the STIX Bundle; content negotiation selects the serialization.
- STIX and TAXII are independent standards; you can use STIX without TAXII.

---

## 🏷️ 3. MISP Taxonomies and Galaxies

- **Machine tags** take the form `namespace:predicate=value`.
- Relevant namespaces: `admiralty-scale`, `diamond-model`, `kill-chain`, `unified-kill-chain`, `estimative-language`, `ioc`, `tlp`, `veris`, `osint`, `ransomware`, `malware_classification`, `detection-engineering`.
- **Galaxies** add structured, clustered knowledge (threat actors, tools, attack patterns).
- Use taxonomies to make sharing machine-consumable, not just human-readable.

---

## 🗄️ 4. OpenCTI and Indicator Hygiene

- OpenCTI models STIX 2.1 with containers, deduplication, reliability/confidence, feeds and decay rules.
- **Indicator decay**: indicators expire; a stale IOC is worse than none because it wastes analyst time and produces false positives.
- Feed operational indicators into detection (via the [detection-engineering](../../operations/detection-engineering/SKILL.md) skill) and strategic context into the threat model.

---

## 🔗 5. Integration with Other Skills

- For the analysis process, see the [cti-threat-intel-lifecycle](../cti-threat-intel-lifecycle/SKILL.md) skill.
- For ATT&CK mapping, see the [cti-mitre-attack](../cti-mitre-attack/SKILL.md) skill.
- For graph-based correlation, see the [graph-relationship-mapping](../../../mapping/graph-relationship-mapping/SKILL.md) skill.
