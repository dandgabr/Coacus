---
name: "explainable-ai"
description: "Provides expert patterns for explainable and responsible AI with Python based on Practical Explainable AI Using Python, covering model-agnostic explanations (LIME, SHAP, anchors, counterfactuals), the SHAP additivity property, global vs local explanation, SP-LIME for global surrogates, image attribution (Integrated Gradients), feature importance, and fairness auditing with the What-If Tool."
---

# AI Skill: Explainable and Responsible AI

This skill guides the AI to make model decisions inspectable and auditable, and to reason about fairness, rather than shipping a black box. It builds on *Practical Explainable AI Using Python* (Mishra).

Resolve current versions of `shap`, `lime`, `alibi`, `eli5` and the What-If Tool from their publishers before pinning them.

---

## 🧭 When to Activate

- A stakeholder asks *why* a model produced a prediction.
- Debugging a suspicious model (leakage, spurious feature, bias).
- Producing local (per-instance) vs global (dataset-level) explanations.
- Auditing fairness across population slices before deployment.
- Choosing between inherently interpretable models and post-hoc explanation.

---

## 🧠 Interpretability vs Explainability

- **Interpretable** models (linear/logistic regression, shallow decision trees, rule lists) expose their reasoning by construction.
- **Explainable** methods are *post-hoc*: they explain an otherwise opaque model.

Prefer an interpretable model when it reaches the required performance; use post-hoc methods when it does not. Every explanation is an approximation of the model, not ground truth.

---

## 📊 SHAP (Shapley Additive exPlanations)

SHAP assigns each feature a contribution such that **the attributions are additive and sum to (model output − base value)** — a game-theoretic guarantee that other methods lack.

```python
import shap
explainer = shap.TreeExplainer(model)          # trees/boosting: XGBoost, LightGBM, CatBoost
shap.force_plot(explainer.expected_value, shap_values[0, :], X.iloc[0, :])
shap.waterfall_plot(...); shap.partial_dependence_plot(...)
```

- `TreeExplainer` (fast, exact for trees), `DeepExplainer`/`GradientExplainer` (deep-learning image classifiers), `KernelExplainer` (model-agnostic, slower).
- The **masker/background** dataset sets the baseline. Runtime scales with its size — a few hundred to a few thousand representative samples is the usual guide; pick the smallest defensible masker (`shap.maskers.Independent(xtrain, max_samples=2000)`).
- Multiclass uses `explainer.expected_value[k]`.

---

## 🍋 LIME and Anchors

**LIME** fits a local interpretable surrogate around one prediction by perturbing samples and weighting by locality:

```python
exp = explainer.explain_instance(np.array(xtest)[60], model.predict, num_features=14)
exp.as_list()   # local prediction + intercept + signed per-feature weights
```

- LIME explanations are **local approximations** and can be unstable across runs; use **SP-LIME** (`lime.submodular_pick.SubmodularPick`) to select a non-redundant set that approximates the global boundary.
- **Anchors** (`alibi`, `AnchorTabular`/`AnchorText`/`AnchorImage`) return model-agnostic *sufficient conditions* for a prediction: `explain(X, threshold=0.95)`.

**Counterfactuals / contrastive explanations** answer "the smallest change that flips the prediction" (`alibi` `CounterfactualProto`, `CEM`); **Integrated Gradients** attributes pixel importance by integrating gradients along a path from baseline to input.

---

## ⚖️ Fairness and Responsible AI

- Probe behavior across **population slices** and simulate what-if scenarios with Google's **What-If Tool** (`witwidget`, `WitConfigBuilder`) — inspect per-slice performance, confusion, and thresholds.
- Frame fairness through **data bias**, **algorithmic bias**, **interpretation/training bias**, and bias **mitigation**; tie findings to Responsible AI commitments.
- For rule extraction from expert systems, backward/forward chaining reconstructs decision logic.

---

## ⚠️ Pitfalls

- **Explaining a proxy, not the truth**: SHAP/LIME approximate the model, so a plausible explanation can be wrong.
- **Background/segmentation choice drives the result** — document it.
- **LIME instability** — never present a single local explanation as definitive global behavior.
- **Attribution ≠ causation**; a high SHAP value does not prove the feature caused the outcome.
- Do not use a post-hoc explanation to *replace* fairness testing, leakage checks, or validation.

---

## 🔗 Integration with Other Skills

- For the modeling workflow, see [python-data-science](../../../data/python-data-science/SKILL.md).
- For adversarial-ML attacks and defenses, see [ai-adversarial-ml-security](../../../security/ai/ai-adversarial-ml-security/SKILL.md).
- For AI governance and assurance, see [ai-governance-assurance](../../../security/ai/ai-governance-assurance/SKILL.md).
- For privacy-preserving data handling, see [security-privacy](../../../security/grc/security-privacy/SKILL.md).
