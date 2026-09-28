# EA Frameworks — Resolved Versions and Sources

Every pin below was resolved against the publisher's own page in the research
session of **2026-09-28** and MUST be re-resolved before it is cited as current
(see `version-freshness`). A pin that could not be resolved against a primary
source is marked **`unverified`** and MUST NOT be presented as current.

## Versioned standards

| Framework | Current version | Publisher | Date | Status |
|---|---|---|---|---|
| TOGAF | 10th Edition (product C220) + Technical Corrigendum 1 | The Open Group | 2025-05-19 (TC1 May 2025) | Verified |
| ArchiMate | 3.2 (product C226) | The Open Group | 2022-10-19 | Verified |
| ISO/IEC/IEEE 42010 | :2022, Edition 2 | ISO/IEC/IEEE (JTC 1/SC 7) | 2022-11 | Verified |
| FEAF / FEA | FEAF-II Version 2 + the Common Approach to Federal EA | OMB (CIO Council for the 1999/2001 originals) | 2013-01-29 / 2012-05-02 | Verified |
| DoDAF | 2.02 | US DoD CIO | 2010-08 | Verified |
| COBIT | 2019 | ISACA | 2019 | Verified |
| ITIL | ITIL Version 5 released; ITIL 4 still supported | PeopleCert / AXELOS | — | Verified (existence); exact 5.0 edition `unverified` |
| SAFe | 6.0 + AI-Native SAFe | Scaled Agile, Inc. | 2026 | Verified |

TOGAF 9.2 remains a supported certification basis; the 10th Edition splits into
TOGAF Fundamental Content plus TOGAF Series Guides.

## Non-versioned frameworks / ontologies

| Framework | Nature | Pin |
|---|---|---|
| Zachman | A 6×6 classification ontology; prescribes no method, notation or content | v3.0 reported by secondary sources only — **`unverified`** (publisher page unreachable) |
| Gartner EA | A discipline and operating model, not a numbered standard | Cite the definition, not a version |

## Books

| Book | Author(s) | Edition / year |
|---|---|---|
| Enterprise Architecture As Strategy | Ross, Weill, Robertson | 2006, Harvard Business School Press |
| Enterprise Architecture at Work (ArchiMate) | Lankhorst et al. | 2005 first edition resolved; current edition **`unverified`** |
| Patterns of Enterprise Application Architecture | Martin Fowler | 2002, Addison-Wesley — note: application-pattern catalogue, NOT an EA framework |
| Enterprise Architecture: Creating Value by Informed Governance | Proper, Lankhorst et al. | 2008 |
| An Introduction to Enterprise Architecture | Scott J. Bernard | AuthorHouse |

## Canonical domain placement (primary sources)

- **TOGAF four domains:** Business, Data, Application, Technology. A description
  covering fewer than all four is by definition not a complete enterprise
  architecture.
- **FEAF six sub-architectures:** strategy, business, data, applications,
  infrastructure, security — hierarchical **except security**, which is a
  cross-cutting thread that pervades every other domain.
- **Network:** a Technology-domain concern (topology, connectivity), not a peer
  domain.

## Governance vocabulary — precise attribution

- **ISO/IEC/IEEE 42010** governs the **architecture description**: stakeholder,
  concern, architecture viewpoint, view, model kind, correspondence,
  architecture rationale/decisions. It explicitly does not specify processes,
  methods, notations or tools.
- **TOGAF** governs the **method, the governance and the artefacts**, including
  the **architecture contract** (ADM Phase G) and the **dispensation/waiver**.
  The architecture contract is a TOGAF term, NOT an ISO 42010 term.
