---
name: "data-science-workflow"
description: "Provides expert patterns for the end-to-end data science workflow and strategy based on Learning Data Science, Data Science at the Command Line, Data Science: The Hard Parts, and Data Science on AWS. Covers the lifecycle (ask/obtain/clean/explore/model/communicate) and OSEMN, Unix command-line data wrangling, data strategy and stakeholder communication, metrics design (funnels, stock-flow, P×Q), data leakage and drift, A/B testing, and MLOps lifecycle on AWS with SageMaker."
---

# AI Skill: Data Science Workflow, Strategy and Production

This skill guides the AI to run a data project end to end — from question to deployment — and to treat judgement, metrics and communication as first-class. It builds on *Learning Data Science* (Lau, Gonzalez & Nolan), *Data Science at the Command Line* (Janssens), *Data Science: The Hard Parts* (Vaughan), and *Data Science on AWS* (Fregly & Barth).

---

## 🧭 When to Activate

- Scoping a data project and defining success metrics.
- Wrangling data with Unix tools or in a notebook.
- Communicating findings to non-technical stakeholders.
- Diagnosing data leakage, drift, or a misleading metric.
- Designing an ML production pipeline and MLOps lifecycle.

---

## 🔄 The Lifecycle

**Ask a Question → Obtain Data → Understand the Data → Understand the World**, iterating (EDA sends you back). Question types: descriptive, exploratory, inferential, predictive. Define scope as **target population → access frame → sample**; diagnose selection and measurement bias.

The command-line framing uses **OSEMN**: **O**btain, **S**crub, **E**xplore, **M**odel, i**N**terpret — iterative and nonlinear ("80% of the work is cleaning the data").

---

## 🐚 Command-Line Data Science

Unix philosophy: small tools + pipes. Docker image `datasciencetoolbox/dsatcl2e`.

- **Obtain:** `curl`, `tar`, **`in2csv`** (Excel→CSV via csvkit), **`sql2csv --db 'sqlite:///...' --query 'SELECT …'`**, `jq` for APIs, secrets via `$(< file)`.
- **Scrub:** `grep`/`sed`/`awk`; **csvkit** (`csvlook`, `csvgrep`, `csvcut`, `csvsort`, `csvjoin`, `csvsql`, `csvstack`) and the faster **xsv**; `body`/`header`/`cols` helpers; `xml2json | jq` and `pup` for HTML. **Convert to CSV early** — classic tools cannot parse structure.
- **Explore/Model:** `csvstat`, `rush` (R one-liners), Tapkee (dimensionality reduction), Vowpal Wabbit, SciKit-Learn Laboratory.
- **Reproducibility:** a **`Makefile`** (make targets/recipes with input-output dependencies, tab-indented rules) reruns only stale steps; version-control everything.
- **Parallelism:** **GNU Parallel** (`seq 0 2 100 | parallel "echo {}^2 | bc"`, `--jobs`, `--results`, `--sshloginfile`, `--pipe`).

**Pitfalls:** `make` requires real tabs; headerless CSV needs explicit `-H`; greedy regex overmatches; `.apply()` is far slower than vectorized pandas; `pd.merge` is less flexible than SQL `WITH`.

---

## 📈 Metrics, Strategy and Communication (Vaughan)

- **Metrics properties:** Measurable, Actionable, Relevance, Timeliness. Decompose with **funnel analytics** `M = (M/m3)(m3/m2)(m2/m1)(m1/E)·E`, **stock-flow** `MAU_t = MAU_{t-1} + Incoming_t − Churned_t`, and **P×Q** `Revenue = Unit Price × Sales = ARPU × MAU`; marketplace `P = (P/V)(V/B)(L/S)(1/L)·B·S`.
- **Business cases** for retention, fraud, external data, and project valuation; watch self-selection and survivorship bias.
- **Narratives:** Clear, **Credible** (check order of magnitude, sanity, assumptions), **Memorable**, **Actionable**. Structure by **What / So What / Now What**; lead with a TL;DR; "long-term success is 75% soft skills."
- **ML rigor:** **data leakage** (outcome as feature, function of outcome, bad controls, mislabeled timestamps, complete/quasi-complete separation inflating AUC) and the **windowing methodology** (the training stage must mirror the scoring stage). **Incrementality:** confounders vs colliders, unconfoundedness, randomization, matching, **Double Machine Learning**.
- Fit imputation, scaling, feature selection and other learned preprocessing only on each training fold; apply the fitted transformation to that fold's held-out data. Choose splits that respect the deployment setting, including group, spatial or temporal dependence where applicable.
- For temporal data, prevent overlapping windows or future observations from leaking across splits. Compare forecasts with suitable simple baselines and document whether normalization removes amplitude or other signal relevant to the question.
- For exploratory analysis, state whether results cover the full dataset or a sample, preserve the data hierarchy and avoid treating inspected rows as proof of whole-dataset quality.
- **A/B tests:** decision criterion, **minimum detectable effect**, power/level/p, variance estimation, simulation, experiment governance and a hypotheses backlog.
- **Experimental units:** distinguish the unit randomized from repeated observations and measurement units; account for clustering and avoid treating repeated measurements as independent replicates. Record allocation, missing data, deviations and assumptions before interpreting a causal effect.
- **Design before observation:** specify outcomes, contrasts, allocation and analysis plans; use restricted randomization or blocking when appropriate and protect allocation concealment where feasible. Check design rank and aliasing, plan interim looks and stopping rules, and record departures. Randomization alone does not eliminate all sources of bias or establish a causal conclusion.
- **Statistical inference:** define the estimand, sampling unit, dependence and family of comparisons before selecting a model. Report effect estimates with uncertainty, missing-data treatment and sensitivity analyses; a non-significant diagnostic test does not establish that model assumptions hold.
- **Power and simulation:** justify effect sizes, variability, independent sample units and the data-generating assumptions; examine sensitivity to plausible alternatives and report failed simulations rather than silently excluding them.
- **Scientific networks:** define nodes, edges, direction, time, isolates and missingness before applying graph metrics. Specify whether weights represent strength or distance and whether an algorithm's interpretation matches that meaning. Assess community or centrality conclusions against parameter choices and suitable null models; a graph association alone is not a causal link.

Research-design guidance was informed by the upstream [experimental design](https://github.com/K-Dense-AI/scientific-agent-skills/blob/5f2bc0341354fd5590aef76a533ada1e1e5b4e62/skills/experimental-design/SKILL.md) and [statistical power](https://github.com/K-Dense-AI/scientific-agent-skills/blob/5f2bc0341354fd5590aef76a533ada1e1e5b4e62/skills/statistical-power/SKILL.md) skills.

---

## ☁️ MLOps on AWS (Fregly & Barth)

Follow the **Model Development Life Cycle** around Amazon **SageMaker**:

- **AutoML:** SageMaker **Autopilot** (`create_auto_ml_job`) and Comprehend.
- **Ingest/explore:** S3 **data lake**, **Glue Crawler** + Data Catalog, **Athena** (serverless SQL on S3), Redshift Spectrum, QuickSight, **Glue DataBrew**, **Deequ** (data unit tests), `awswrangler` (`wr.s3.read_parquet`).
- **Prepare:** **Processing Jobs** (`SKLearnProcessor`, `PySparkProcessor`), **Feature Store** (`FeatureGroup.create(enable_online_store=True)`, offline via Athena), Data Wrangler, **Lineage Tracking** and **Experiments**.
- **Train:** **JumpStart** pretrained models, `Estimator.fit(...)`, **Hyper-Parameter Tuning** (warm start), **Distributed Training**, Debugger + profiler (Spot interruption recovery), **Clarify** for bias/explainability.
- **Deploy/monitor:** real-time **Endpoints** vs **Batch Transform**, auto-scaling, A/B strategies, **Model Monitor** (data quality, model quality, **bias drift**, feature-attribution drift), Lambda + API Gateway, edge (TorchServe, DJL).
- **Pipelines/MLOps:** **SageMaker Pipelines** (`Pipeline(name=…, steps=[Step(...)])`), alternatives Step Functions / Kubeflow / MWAA / MLflow / TFX; **A2I** for human-in-the-loop. Maturity: manual → orchestrated pipelines → auto-triggered on new data/drift (GitOps).
- **Streaming/security:** Kinesis Firehose + Analytics, MSK/Kafka; IAM, network isolation, encryption at rest/in transit, Secrets Manager, Lake Formation.

**Cost control:** Spot/Savings Plans, checkpoints, early stopping.

---

## ⚠️ Pitfalls

- Peeking at the test set or over-tuning one validation split.
- Leakage from complete separation, timestamp mislabels, or features that encode the outcome.
- Confusing correlation with causation; ignoring confounders/colliders.
- Monitoring only system metrics and missing model/data drift.

---

## 🔗 Integration with Other Skills

- For the modeling toolkit, see [python-data-science](../python-data-science/SKILL.md).
- For scaling pipelines, see [distributed-ml-scaling](../distributed-ml-scaling/SKILL.md).
- For data governance and contracts, see [data-mesh-governance](../data-mesh-governance/SKILL.md).
- For cloud platform specifics, see [cloud-aws](../../infrastructure/cloud-aws/SKILL.md).
