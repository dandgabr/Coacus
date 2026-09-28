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

## 🔬 Explanation Method Atlas (Thampi)

- **Inherently interpretable models:** linear/logistic coefficients as effect sizes (unstable under correlated features), traceable decision trees (overfit-prone), and **GAMs** as the sweet spot — the target as a sum of per-feature smooth splines; per-feature effect curves are the explanation artifact.
- **Partial dependence plots:** average model output while sweeping one feature; **untrustworthy when the swept feature correlates with marginalized features** — forcing values creates impossible synthetic records and extrapolated junk. Feature-interaction PDPs extend this to pairs.
- **LIME internals:** perturbed dataset sampled from feature statistics → black-box predictions → locality-weighted linear surrogate; kernel width is a sensitivity knob; image variants perturb superpixels.
- **SHAP internals:** cooperative-game framing; coalitions are keep/resample masks; the weighting kernel emphasizes extreme coalitions; Shapley attributions carry stronger guarantees and unify additive methods. **Anchors** return high-precision if-then sufficiency rules.
- **Saliency for CNNs:** vanilla/guided backpropagation, SmoothGrad, integrated gradients; **Grad-CAM** gradient-weights the final convolutional feature map for a class-discriminative heatmap (guided Grad-CAM adds resolution). Choose gradient methods for fine localization, Grad-CAM for discriminative regions, LIME for model-agnostic image explanations.
- **Network dissection:** probe hidden units against an independently labeled concept dataset and quantify alignment by intersection-over-union — compares learned concept detectors across training tasks; needs dense concept labels.
- **Embedding inspection:** similarity search, PCA and t-SNE over embedding spaces — validate that a 2-D projection preserves high-dimensional structure before narrating clusters.
- **Fairness formalization:** per-group confusion-matrix quantities under competing definitions — demographic parity (equal positive rates), equality of opportunity (equal true-positive rates), equalized odds (equal TPR and FPR); no single definition suffices. Bias enters via proxy features and via learned representations; dropping protected attributes is insufficient.
- **Counterfactual explanations:** minimal feasible feature changes that flip the decision, framed as bi-objective optimization (reach the desired outcome while staying close to the input); diverse counterfactual sets aid recourse.
- **Datasheets for datasets:** standardized documentation of provenance, composition, collection process and intended uses — the transparency artifact handed to stakeholders.

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
