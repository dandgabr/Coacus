---
name: "ai-model-evaluation"
description: "Provides AI model evaluation discipline based on production ML and LLM evaluation practice, covering offline evaluation anatomy (inputs, design, outputs), counterfactual evaluation with propensity logging, A/B testing with exit criteria and guardrail metrics, reward hacking and Goodhart defenses, LLM-as-a-judge design contracts and calibration, segment analysis and online-metric blind spots. Use when designing offline or online evaluations for models and LLM applications, building judge pipelines, or interpreting experiment results."
---

# AI Skill: AI Model Evaluation

This skill guides the AI to evaluate models and LLM applications as a two-stage discipline — offline rigor before online validation — with explicit defenses against metric gaming. It synthesizes evaluation practice from Nassery's AI model evaluation literature. Benchmark snapshots never predict messy real-world behavior; evaluation design does.

---

## 🧭 When to Activate

- Designing the evaluation plan for a model, recommender, LLM feature or agent.
- Deciding whether a model is ready for an online experiment.
- Building or calibrating LLM-as-a-judge pipelines.
- Diagnosing suspicious metric improvements (reward hacking).
- Setting up counterfactual or segment-level analysis.

---

## 🔁 Lifecycle Position

Define product requirements → develop → **offline evaluation** (fast loop on historical data) → **A/B test** (validates real-user impact) → conditional rollout gated on data. Offline rigor de-risks online tests; both stages are mandatory, not optional.

---

## 🧪 Offline Evaluation Anatomy

- **Inputs:** historical interactions, ground-truth labels, contextual metadata, structured action–outcome logs with propensity scores.
- **Design:** metric definitions (for example precision-at-k, NDCG-at-k), simulated scenarios (cold-start users, missing features), evaluation granularity (per session/per user), sampling strategy with confidence estimation.
- **Outputs:** performance metrics plus diagnostics — bias slices, coverage, robustness.
- For LLMs and agents the same frame applies: inputs become prompts, retrieved context, conversation history and tool results; design becomes rubrics, simulated user scenarios, tool-use constraints and judge setups; outputs become relevance, groundedness, tool-call accuracy, task-completion rates and failure categories.
- Engagement signals are proxies — clicks reflect placement as much as preference; interpret offline metrics with that bias.
- Use offline evaluation in **diagnostics mode** to explain behavior: slice by cohort, content type, geography, traffic pattern; findings feed online monitoring focus. Latency and load are first-class evaluation targets before user exposure.

---

## 🧮 Counterfactual Evaluation

- Grounded in causal inference; requires **counterfactual logging**: action taken, candidate set considered, propensity (ideally the full selection distribution), contextual metadata, policy/model version and observed outcome.
- Data-quality gates before trusting results: overlap (does the logged policy ever take the new policy's actions?), exploration (were alternatives tried?), effective sample size after weighting. Millions of rows can still carry near-zero usable evidence; large action spaces multiply data needs.

---

## 🚦 A/B Testing and Exit Criteria

Gate an online test behind explicit offline exit criteria:

- Beats the baseline on the primary offline metric.
- Guardrails (latency, cost, safety, fairness, calibration) within range.
- No unacceptable segment regressions; error analysis understood.
- Tested on realistic, recent, representative data.
- A clear hypothesis with pre-agreed acceptable trade-offs.

Match experiment strategy to model maturity: exploratory, dogfooding-flavored tests for prototypes; rigorous, guardrail-heavy tests for production models. Dogfooding is a qualitative prerequisite, never a substitute.

---

## 🎣 Reward Hacking and Goodhart Defenses

- Models optimize the measured lever, not the intent: verbosity inflating conversation length, clickbait chasing click-through, agents over-calling tools or over-escalating to close tasks. The risk is sharper for AI than static UX because models are trained optimizers in open-ended domains with feedback loops.
- Defense toolkit: **multi-metric contracts** (primary + guardrail metrics + non-inferiority margins), **adversarial offline stress tests** (verbosity bait, clickbait prompts), **game-resistant outcome metrics** (completion, repeat usage, downstream conversions), **segment analysis** to expose masked regressions, and **exploration traffic** to break feedback loops.
- Fairness, robustness and trust rarely appear in engagement metrics — carry offline bias and robustness findings into online monitoring plans.

---

## ⚖️ LLM-as-a-Judge

- Deterministic metrics collapse on open-ended generation; judges operationalize qualitative assessment as structured, repeatable proxies for human judgment.
- **Judge design contract — four questions:** what is being judged (answer, summary, pair, agent action); what criteria (accuracy, helpfulness, relevance, safety, coherence, completeness, policy compliance); what context the judge needs (query, source document, tool output, policy text); what output to produce (score, label, winner, ranking, structured JSON with reasons).
- Prompt pattern: impartial-evaluator role, explicit neutrality on length and style, ordered criteria, reason-before-verdict, strict structured output; ask whether the answer is factually supported by the provided source and free of unsupported claims.
- **Known failure modes to calibrate against:** length bias, first-position bias in pairwise comparison, polish-over-substance preference, missed factual errors under incomplete context, fluent justification of bad scores. Validate against human judgments and gold examples before trusting judge output.

---

## ⚠️ Pitfalls

- Trusting offline metrics stakeholders never reconciled with online outcomes — keep the correlation known and current.
- No agreed trade-off thresholds: co-define them cross-functionally, with safety, privacy and latency as non-tradable guardrails.
- Evaluation data diverging from production systems; multi-metric dashboards keep trade-offs transparent.
- Deploying a judge without calibration, or accepting its fluent explanations at face value.
- Single-metric optimization — the open door to reward hacking.

---

## 🔗 Integration with Other Skills

- For component-level RAG and LLM metrics, see [ai-llm-engineering-rag](../ai-llm-engineering-rag/SKILL.md).
- For explainability diagnostics that complement slice analysis, see [explainable-ai](../explainable-ai/SKILL.md).
- For annotation, golden sets and human evaluation workflows, see [human-in-the-loop-ml](../../../data/human-in-the-loop-ml/SKILL.md).
- For platform-level monitoring and drift, see [mlops-platform-engineering](../../../data/mlops-platform-engineering/SKILL.md).
- For adversarial evaluation of model security, see [ai-adversarial-ml-security](../../../security/ai/ai-adversarial-ml-security/SKILL.md).
