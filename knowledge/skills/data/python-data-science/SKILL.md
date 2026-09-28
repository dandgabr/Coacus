---
name: "python-data-science"
description: "Provides expert patterns for Python data science and applied machine learning based on Data Science from Scratch, Introduction to Machine Learning with Python, the Python Data Science Handbook, Python Machine Learning Cookbook, and Practical Statistics for Data Scientists. Covers NumPy vectorization and broadcasting, pandas wrangling, matplotlib/seaborn, the scikit-learn estimator API with pipelines and model selection, supervised and unsupervised algorithms, feature engineering, and the statistics (bootstrap, A/B testing, regression) behind applied data science."
---

# AI Skill: Python Data Science and Applied Machine Learning

This skill guides the AI to act as a data scientist who reasons about data before reaching for a model: understand the distribution, choose the simplest adequate estimator, and validate with the right metric. It builds on *Data Science from Scratch* (Grus), *Introduction to Machine Learning with Python* (Müller & Guido), the *Python Data Science Handbook* (VanderPlas), the *Python Machine Learning Cookbook* (Albon), and *Practical Statistics for Data Scientists* (Bruce, Bruce & Gedeck).

Resolve current versions of NumPy, pandas, scikit-learn and the plotting libraries from their publishers before pinning them; the APIs below name the stable interfaces.

---

## 🧭 When to Activate

- Loading, cleaning, joining, aggregating or reshaping tabular data.
- Choosing, training, tuning or evaluating a supervised/unsupervised model.
- Designing a leakage-free preprocessing + model pipeline.
- Interpreting results statistically (confidence intervals, A/B tests, regression diagnostics).
- Diagnosing overfitting, class imbalance, or a metric that misleads.

---

## 🔢 NumPy: Vectorization and Broadcasting

`ndarray` is a fixed-type contiguous buffer (`dtype`, `shape`, `ndim`, `size`, `itemsize`). Operations run in compiled C, not the interpreter loop — vectorize instead of looping.

- Creation: `np.array(list, dtype='float32')`, `np.zeros/ones/empty`, `np.arange`, `np.linspace`, `np.random.default_rng(seed)`.
- **Slicing returns views, not copies** (`x[::2]`, `grid[:2,:3]`); reshaping is `x.reshape(...)`; add axes with `np.newaxis`:
```python
x = np.arange(10)
x[:, np.newaxis].shape   # (10, 1)
```
- **Universal functions** (`np.add`, `np.exp`, `np.sqrt`, `np.log1p`) with `out=`, `reduce`, `accumulate`, `outer`, `np.at`.
- **Broadcasting** pads the shorter shape with leading 1s; each dimension must be equal or 1. `a + b[:, np.newaxis]` produces the outer sum.
- Aggregations with `axis=`, boolean masks (`x[x > 5]`), **fancy indexing** (`x[[3,5,8]]`, mutable), sorting (`np.sort`, `np.argsort`, `np.partition`).
- **Structured arrays** (compound dtypes with named fields) bridge to pandas.

---

## 🐼 pandas: Wrangling

`Series` is an index-labeled 1-D array; `DataFrame` is a dict of aligned Series sharing an index.

- **Indexing:** explicit indexers remove ambiguity — `.loc[label]` (inclusive) and `.iloc[position]`. Never set values with chained indexing (`df[mask]['col']=…` triggers `SettingWithCopyWarning`); use `.loc`.
- **Missing data:** `isnull`, `dropna(how='all')`, `fillna`, `ffill`/`bfill`, `interpolate`. Distinguish MCAR/MAR/MNAR — dropping MNAR rows injects bias.
- **Combining:** `pd.concat([df1,df2])`; `df1.merge(df2, on='k', how='inner'|'left'|'right'|'outer')`.
- **GroupBy** is split-apply-combine: `.groupby('k').agg([...])`, `.transform`, `.apply` (much slower than vectorized ops). `pivot_table`.
- **Time series:** `pd.to_datetime`, `date_range`, `resample('M').mean()`, `rolling(window=30).mean()`, `shift()` for lags.
- **Vectorized strings:** `ser.str.lower()`, `.str.contains(r'\d+')`, `.str.extract`.
- **Performance:** `df.query(...)` and `df.eval(...)` avoid temporaries (`numexpr`).

**Visualization:** prefer the object-oriented `fig, ax = plt.subplots()` API over the state-machine; seaborn (`sns.pairplot`, `kdeplot`, `lmplot`) for statistical plots over a DataFrame. Use `%matplotlib inline` and `rcParams` for defaults.

---

## 🤖 scikit-learn: API, Pipelines, Model Selection

Every estimator is `fit(X, y)` → `predict(X)`; transformers add `transform`/`fit_transform`; learned state lives in trailing-underscore attributes (`coef_`, `classes_`, `feature_importances_`).

```python
model = GaussianNB()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
```

- **Fit preprocessing on train only.** Wrap scalers/encoders in a `Pipeline`/`make_pipeline` so scaling happens inside each CV fold; `ColumnTransformer` handles mixed numeric/categorical columns.
- **Cross-validation:** `cross_val_score(model, X, y, cv=5)`; `KFold`, `StratifiedKFold` (default for classification), `GroupKFold`. `GridSearchCV`/`RandomizedSearchCV` tune `best_params_`; nested CV gives an unbiased estimate at high cost.
- **Metrics** (`sklearn.metrics`): `accuracy_score` (misleads on imbalance), `precision/recall/f1`, `classification_report`, `roc_auc_score`, `average_precision_score`; regression `mean_absolute_error`, `mean_squared_error`, `r2_score`. Pass via `scoring=`.
- `validation_curve`/`learning_curve` diagnose variance vs bias.

**Supervised:** k-NN (scaling-sensitive, slow prediction), linear models (`Ridge` L2, `Lasso` L1 sparse, `ElasticNet`, `LogisticRegression`), Naive Bayes, trees and ensembles (`RandomForest`, gradient boosting, XGBoost), SVM (`C`/`gamma` interact, requires scaling). Expose confidence with `decision_function`/`predict_proba`.

**Unsupervised:** scaling (`StandardScaler`, `RobustScaler`, `MinMaxScaler`) is mandatory for k-NN/SVM/PCA/k-means and unnecessary for trees. `PCA(n_components=0.99)`, `KernelPCA`, t-SNE/UMAP (visualization only). Clustering: `KMeans` (elbow/`silhouette_score`), `AgglomerativeClustering`, `DBSCAN` (no k, noise −1), `GaussianMixture` (BIC/AIC).

---

## 🧪 Statistics for Data Science

- **EDA:** location (mean, trimmed mean, median, mode), variability (variance, std, IQR, MAD), percentiles, distributions, correlation matrices.
- **Bootstrap:** resample with replacement `R` times to obtain confidence intervals and standard errors for *any* statistic.
```python
def bootstrap_sample(data):
    return [random.choice(data) for _ in data]
```
- **Inference:** Central Limit Theorem, standard error, permutation tests, t-tests (`scipy.stats.ttest_ind`), ANOVA (`statsmodels`), chi-square (`chi2_contingency`), power and sample size, multiple-testing correction.
- **Regression:** from-scratch least squares; `statsmodels` `smf.ols` for standard errors/t-stats/p-values vs `sklearn` for prediction. Diagnose outliers, influence, heteroskedasticity, multicollinearity (VIF); logistic regression coefficients are **odds ratios**.

Implementing the primitives once (Grus) exposes why scaling, learning rates and loss gradients matter.

---

## ⚖️ Best Practices and Pitfalls

1. **Fit on train only** — every scaler/encoder/imputer/selector is a model; leakage inflates scores.
2. **Split before exploring**; reserve the hold-out for the final number.
3. **Match the metric to the cost** — prefer F1/ROC-AUC/PR-AUC on imbalanced data; `class_weight='balanced'`, resampling (SMOTE).
4. **Start from the simplest baseline** (dummy → logistic → complexity justified by the learning curve).
5. **Handle missing data deliberately**; impute rather than blunt `dropna`.
6. **Encode categories correctly** — `OneHotEncoder(handle_unknown='ignore')` for nominal (never `LabelEncoder` on features, which invents order).
7. **Seed everything** (`random_state`, `np.random.default_rng`) and pin library versions.
8. **Reduce dimensionality** before distance-based work — the curse of dimensionality degrades k-NN/clustering.
9. **Interpret before shipping** — feature importances, coefficients with standard errors; correlation ≠ causation.
10. **Persist the model with its exact preprocessing pipeline** (`joblib`/`pickle`).

---

## 🔗 Integration with Other Skills

- For the mathematical foundations (linear algebra, optimization), see [data-science-advanced-math](../../domains/academic/data-science-advanced-math/SKILL.md).
- For scaling across machines, see [distributed-ml-scaling](../distributed-ml-scaling/SKILL.md).
- For deep learning and LLM pipelines, see [ai-llm-engineering-rag](../../domains/industry/ai-llm-engineering-rag/SKILL.md).
- For model explainability, see [explainable-ai](../../domains/industry/explainable-ai/SKILL.md).
