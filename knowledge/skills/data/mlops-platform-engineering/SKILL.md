---
name: "mlops-platform-engineering"
description: "Provides ML platform engineering based on internal developer platform practice for ML and AI systems, covering MLOps maturity levels, Kubeflow pipelines, MLflow tracking and registry, Feast feature stores with point-in-time correctness, BentoML serving, drift detection with statistical tests, monitoring and explainability integration, LLM observability, token cost economics and tiered model routing. Use when building or operating ML platforms, productionizing models, or adding LLMOps to an existing platform."
---

# AI Skill: ML Platform Engineering

This skill guides the AI to build ML platforms as closed-loop systems where the pipeline — not the model — is the durable asset. It synthesizes platform engineering practice from Tan and Padmanabhan's ML platform literature. Resolve current versions of Kubeflow, MLflow, Feast, BentoML and Evidently before pinning.

---

## 🧭 When to Activate

- Standing up or evolving an ML platform or internal developer platform for ML.
- Productionizing a trained model with tracking, registry, serving and monitoring.
- Designing feature stores or solving training-serving skew.
- Adding LLM workloads (RAG services, prompt observability) to an existing platform.
- Planning ML infrastructure cost and scale thresholds.

---

## 🔁 The Closed Loop and Maturity Ladder

- ML work is a loop: problem definition → data collection → exploration → training → evaluation → deployment → monitoring → maintenance. Models are ephemeral; the loop is the asset. Model weights and code are separate entities with explicit lineage.
- **Maturity levels:** manual script-driven builds (no monitoring) → retraining pipelines as the deployment unit with experimental-operational symmetry → CI/CD for the pipelines themselves, everything automated except data and model analysis.
- Level-one prerequisites: data and model validation gates, a feature store where justified, pipeline monitoring with lineage and metadata, and auto-triggered retraining on schedules, new data or drift.

---

## 🧱 Platform Backbone

- Containerization → orchestration → packaging → CI/CD with declarative delivery → metrics and alerting.
- **Pipelines:** a component is one container in one pod; components compose into DAGs; distinguish scalar values from file-path artifacts; share large datasets through persistent volumes instead of re-downloading.
- **Tracking and registry:** log parameters, metrics and artifacts per run; select best runs by metric queries; promote versions through staging to production with governance; run the registry on shared infrastructure, never on laptops.
- **Feature store:** offline store for training-time historical retrieval, online store for low-latency inference, materialization jobs pushing offline to online, and a registry of entities and features. The headline guarantee is point-in-time correctness — the most recent feature value at or before the event timestamp — eliminating hand-written leakage-prone joins. Feature stores decouple generation from modeling and make features reusable, attacking training-serving skew.

---

## 🚀 Serving

- Wrap models as services: an API server parses and validates input; runners execute inference in their own worker processes; scale API servers and runners independently.
- Version artifacts as tagged, deployable units; expose separate machine (JSON) and human (rendered) endpoints when debugging aids matter.
- Real-time endpoints need batching, rate limiting and streaming planned in; batch pipelines need schedules and backfills.

---

## 📉 Drift and Monitoring

- Drift taxonomy: label drift, prior-probability shift, covariate shift, sudden exogenous drift.
- Detect with statistical tests between reference and current data — CDP-based two-sample tests for numeric features, chi-square for categorical, distance-based measures for magnitude — letting the tooling auto-select or accepting custom tests.
- Compose reports from dataset-level and column-level metrics (missingness, summaries, regression quality); wire drift checks into pipeline components and API capture.
- Monitoring splits into basic metrics, custom metrics, logging and alerting; explainability is the "why" complement — attribution heatmaps over model activations verify what a detector attends to and inform retraining decisions.
- Regulated contexts make explanation mandatory (adverse-action reason codes in credit); product contexts use it for trust.

---

## 🧠 LLMOps Extension

- LLM applications differ in nondeterminism, prompts-as-code and new failure modes; RAG services are composed retrieval + augmentation + generation components, not a single API call.
- Use asymmetric embedding task types (document indexing vs query embedding) for measurable retrieval gains; wrap provider SDKs behind an interface so models are swappable; prefer cosine similarity for text embeddings.
- Retrieval quality levers: chunk size (precision versus context), embedding-domain fit, similarity metric choice.
- **Prompt observability:** trace every call, version and manage prompts, evaluate responses beyond traditional metrics — prompt engineering is treated as versioned, tested, logged infrastructure.
- Add LLM-specific safety and adversarial testing plus production guardrails as a governance layer.

---

## 💰 Cost Economics

- Token-metered pricing scales with user behavior; price queries before launch (worked examples span a 70x range between premium API and self-hosted open source per query).
- Self-hosting thresholds as planning heuristics: cloud APIs win below roughly 100k queries/month; break-even mid-range; self-hosted savings above roughly 500k/month; large self-hosted models demand multi-GPU fleets and dedicated DevOps capacity.
- **Tiered model routing** (cheap model for routing and classification, mid-tier for standard answers, premium for complex generation) cuts cost sharply but adds router-accuracy monitoring, threshold experimentation and multi-model versioning burden.
- Peak-load spikes either multiply token costs or force over-provisioned fleets idling most of the time — plan for both.

---

## ⚠️ Pitfalls

- Conflating model with code, or tracking runs only on local machines.
- Skipping established platform practice — duplication and debt erase the apparent speedup.
- One generic embedding configuration for both documents and queries.
- Asserting vague problem statements ("predict churn") without stakeholder alignment.
- Deploying without drift monitoring, or with logs nobody alerts on.

---

## 🔗 Integration with Other Skills

- For evaluation gates before promotion, see [ai-model-evaluation](../../domains/industry/ai-model-evaluation/SKILL.md).
- For annotation pipelines feeding the platform, see [human-in-the-loop-ml](../human-in-the-loop-ml/SKILL.md).
- For LLM application architecture, see [ai-application-engineering](../../domains/industry/ai-application-engineering/SKILL.md).
- For Kubernetes and delivery backbone, see [program-containers](../../infrastructure/program-containers/SKILL.md) and [devops-engineer](../../roles/devops-engineer/SKILL.md).
- For scale-out training, see [distributed-ml-scaling](../distributed-ml-scaling/SKILL.md).
