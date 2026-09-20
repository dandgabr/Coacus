---
name: data-mesh-governance
description: Specializes in Data Mesh Architecture, Data Products, and Federated Governance based on Implementing Data Mesh (Jean-Georges Perrin) and The Enterprise Data Catalog (Ole Olesen-Bagneux). Covers the 4 Data Mesh principles (Domain Ownership, Data as a Product, Self-Serve Data Platform, Federated Computational Governance), Data Contracts (OpenDataContract), data lineage, and enterprise catalogs.
---

# Data Mesh Architecture and Federated Data Governance

This skill establishes the architectural and operational principles for transitioning from centralized monolithic data lakes to a decentralized, domain-oriented approach (**Data Mesh**), with automated governance and formal data contracts.

---

## 🏛️ 1. The 4 Foundational Data Mesh Principles

1. **Domain Ownership**: Business/engineering teams that own the operational domain are responsible for its analytical data.
2. **Data as a Product (DaaP)**: Analytical data has identified consumers, quality SLAs/SLOs, documentation, and formal contracts.
3. **Self-Serve Data Platform**: Domain-agnostic infrastructure that abstracts away the complexity of provisioning pipelines, storage, and access.
4. **Federated Computational Governance**: Security, privacy (LGPD/GDPR), compliance, and audit policies applied automatically as code (*Policy as Code*).

---

## 📜 2. Structure of a Data Contract (OpenDataContract Specification)

```yaml
version: 1.0.0
dataset: orders_completed
domain: checkout_financial
owner: team-checkout@empresa.com
status: active
sla:
  freshness: 5m
  availability: 99.9%
schema:
  - name: order_id
    type: string
    description: "UUID da transação aprovada"
    required: true
    pii: false
  - name: customer_tax_id
    type: string
    description: "CPF/Tax ID do comprador"
    required: true
    pii: true
    classification: restricted
  - name: total_amount_cents
    type: integer
    description: "Valor em centavos de moeda corrente"
    required: true
```
