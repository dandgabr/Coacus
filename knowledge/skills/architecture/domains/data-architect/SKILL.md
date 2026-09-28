---
name: data-architect
description: >-
  Acts as the Data Architect owning the enterprise data asset: conceptual and
  logical models, data governance, lineage, data quality, master and reference
  data, and the data lifecycle. Use when defining enterprise data models,
  setting data governance and quality standards, planning master data, or
  aligning data architecture with business and application architecture.
tags:
  - architecture
  - data-architecture
---

# Skill: Data Architect

The Data Architect owns the **information domain** of the enterprise
architecture (TOGAF ADM Phase C, Data Architecture). It governs the data asset:
models, governance, lineage, quality and lifecycle — distinct from the database
engine (a DBA concern) and from analytics modelling (a BI/warehouse concern).

---

## 1. When This Skill Applies

- Defining conceptual, logical and enterprise data models.
- Setting data governance, stewardship and data-quality standards.
- Defining master data and reference data strategy.
- Ensuring regulatory compliance (privacy, retention) in data design.
- Guiding data integration and interoperability.
- Aligning data architecture with business capabilities and applications.

Does NOT apply to: database engine tuning and replication (use
[dba-database-administrator](../../../roles/dba-database-administrator/SKILL.md)),
or analytical pipeline implementation (use the data-engineering skills under
`knowledge/skills/data/`).

---

## 2. The Data Architect vs. the DBA vs. the Analytics Engineer

| Role | Owns |
|---|---|
| Data Architect | Logical/enterprise data model, governance, lineage, MDM |
| Database Administrator | Physical engine, indexing, tuning, replication, HA |
| Analytics / BI Architect | Warehouse/lakehouse modelling, semantic layer, metrics |

Keep the boundary: the Data Architect decides *what data means and how it is
governed*; the DBA decides *how the engine stores it*.

---

## 3. Method (TOGAF ADM Phase C, Data Architecture)

1. **Baseline** the current data architecture: entities, sources, flows,
   governance state.
2. **Target** the data architecture: canonical entities, ownership, quality
   targets, lifecycle and retention.
3. **Gap analysis** and a data migration strategy.
4. **Govern**: data standards, stewardship, lineage and quality metrics.
5. **Align** with application and business architecture, and with privacy
   obligations.

---

## 4. Orchestration and Handoffs

| Concern | Owning skill |
|---|---|
| Enterprise frame and target state | [enterprise-architect](../../enterprise/enterprise-architect/SKILL.md) |
| Physical engine, tuning, replication | [dba-database-administrator](../../../roles/dba-database-administrator/SKILL.md) |
| PostgreSQL / MariaDB / SQLite / MongoDB specifics | [db-postgresql](../../../data/db-postgresql/SKILL.md), [db-mariadb](../../../data/db-mariadb/SKILL.md), [db-sqlite](../../../data/db-sqlite/SKILL.md), [db-mongodb](../../../data/db-mongodb/SKILL.md) |
| Data mesh, data products, federated governance | [data-mesh-governance](../../../data/data-mesh-governance/SKILL.md) |
| Streaming and event-driven data | [realtime-streaming-event-driven](../../../data/realtime-streaming-event-driven/SKILL.md) |
| Privacy, de-identification, LGPD/GDPR | [security-privacy](../../../security/grc/security-privacy/SKILL.md) |
| Classification and DSPM | [data-classification-dspm](../../../security/data/data-classification-dspm/SKILL.md) |

---

## 5. Reference Frameworks

- **TOGAF** — ADM Phase C, Data Architecture.
- **DAMA-DMBOK** — the data management body of knowledge (pin the edition; see
  `version-freshness`).
- **ArchiMate** — Data/Information elements in the Application and Technology
  layers.
- **Metadata and data-quality standards** — ISO/IEC 11179 (metadata registries)
  and ISO 8000 (data quality); resolve each before citing.

See [ea-frameworks](../../enterprise/enterprise-architect/references/ea-frameworks.md)
for the resolved EA framework versions.

---

## 6. Common Mistakes

| Mistake | Correction |
|---|---|
| Confusing the logical model with the physical schema | The model is the architect's; the schema is the DBA's |
| Treating MDM as a tool purchase | It is a governance decision over entities |
| Ignoring lineage | Lineage is a first-class governance artefact |
| Skipping privacy in data design | Classify and de-identify at design time |
| Citing DMBOK edition from memory | Resolve the edition in-session |
