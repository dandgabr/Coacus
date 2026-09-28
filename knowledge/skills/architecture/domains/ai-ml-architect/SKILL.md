---
name: ai-ml-architect
description: >-
  Acts as the AI/ML Architect owning the end-to-end architecture of machine
  learning and generative AI systems: data and feature pipelines, training,
  model serving, monitoring, MLOps/GenAIOps and responsible-AI governance. Use
  when designing ML or GenAI platforms, defining MLOps pipelines, planning model
  serving and scaling, or governing AI risk.
tags:
  - architecture
  - ai-ml-architecture
---

# Skill: AI/ML Architect

The AI/ML Architect owns the **end-to-end architecture of AI systems**: data
and features, training, serving, monitoring and governance. It spans the data
domain and the solution domain, with a dedicated governance obligation that
ordinary software architecture does not carry.

---

## 1. When This Skill Applies

- Designing ML/GenAI pipelines and serving architectures.
- Defining MLOps/GenAIOps: CI/CD/CT, model registries, drift monitoring.
- Handling model governance, risk and responsible-AI controls.
- Optimizing GPU/compute cost and inference latency.
- Designing evaluation, safety and guardrails for LLM systems.

Does NOT apply to: the enterprise data model (use
[data-architect](../data-architect/SKILL.md)), or the internal structure of an
application embedding AI (use [software-architect](../../../roles/software-architect/SKILL.md)).

---

## 2. Lifecycle and Concerns

| Stage | Architectural concern |
|---|---|
| Data / features | Feature store, lineage, training/serving skew |
| Training | Reproducibility, experiment tracking, compute |
| Evaluation | Offline metrics, safety, bias, red-teaming |
| Serving | Latency, batching, GPU utilization, autoscaling |
| Monitoring | Drift, data quality, feedback loops |
| Governance | Model cards, risk classification, audit trail |

---

## 3. Method

1. **Frame** the use case and the risk tier (responsible AI, regulation).
2. **Design** the data and feature pipeline with lineage.
3. **Define** training, evaluation and reproducibility.
4. **Design** serving for the latency/cost target.
5. **Instrument** monitoring, drift and feedback.
6. **Govern** with model cards, an AI BOM and an audit trail.

---

## 4. Orchestration and Handoffs

| Concern | Owning skill |
|---|---|
| Enterprise frame and standards | [enterprise-architect](../../enterprise/enterprise-architect/SKILL.md) |
| Data model and governance | [data-architect](../data-architect/SKILL.md) |
| LLM/RAG engineering patterns | [ai-llm-engineering-rag](../../../domains/industry/ai-llm-engineering-rag/SKILL.md) |
| MLOps platform engineering | [mlops-platform-engineering](../../../data/mlops-platform-engineering/SKILL.md) |
| Distributed training and scaling | [distributed-ml-scaling](../../../data/distributed-ml-scaling/SKILL.md) |
| Model evaluation | [ai-model-evaluation](../../../domains/industry/ai-model-evaluation/SKILL.md) |
| AI security and adversarial ML | [ai-llm-slm-security](../../../security/ai/ai-llm-slm-security/SKILL.md) |
| AI governance and ISO 42001 | [ai-governance-iso-42001](../../../security/grc/ai-governance-iso-42001/SKILL.md) |
| GPU programming | [gpu-programming-cuda](../../../languages/gpu-programming-cuda/SKILL.md) |

---

## 5. Reference Frameworks

- **NIST AI RMF** — the AI risk management framework (resolve the version).
- **ISO/IEC 42001** — the AI management system standard (resolve the edition).
- **ML design patterns** — the ML engineering pattern catalogue.
- **Cloud MLOps guidance** — the provider MLOps/GenAIOps blueprints (resolve
  the version before citing).

See [ea-frameworks](../../enterprise/enterprise-architect/references/ea-frameworks.md).

---

## 6. Common Mistakes

| Mistake | Correction |
|---|---|
| Treating the model as the whole system | The pipeline and serving are the system |
| Ignoring training/serving skew | Share features between both paths |
| No drift monitoring | Monitor data and model drift continuously |
| No governance artifacts | Model cards, AI BOM and audit trail are required |
| Citing an AI framework version from memory | Resolve it in-session |
