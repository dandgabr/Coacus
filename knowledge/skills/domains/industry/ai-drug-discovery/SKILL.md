---
name: "ai-drug-discovery"
description: "Provides AI drug discovery pipeline engineering based on computational drug discovery practice, covering molecular representations (SMILES, descriptors, fingerprints, graphs), virtual screening and Ro5/PAINS filters, QSAR modeling discipline, docking and active learning at billion-compound scale, VAE-based de novo design, graph neural networks for drug-target affinity, protein structure prediction platforms and honest clinical translation metrics. Use when building ML pipelines for molecular property prediction, virtual screening, de novo molecular generation or drug-target interaction modeling."
---

# AI Skill: AI Drug Discovery Pipelines

This skill guides the AI to build machine-learning pipelines for small-molecule discovery with the domain discipline the field demands: representation choice first, honest validation always, and experimental confirmation as the only ground truth. It synthesizes computational drug discovery engineering practice from Flynn's pipeline literature. Resolve current versions of RDKit, scikit-learn and PyTorch before pinning.

---

## 🧭 When to Activate

- Predicting molecular properties or bioactivity with ML.
- Designing virtual screening or hit-triage funnels.
- Building QSAR models under small-data constraints.
- Docking at scale, or combining ML predictors with physics-based scoring.
- Generative molecular design or drug-target affinity modeling.

---

## 🌍 Problem Frame

- Chemical space is on the order of 10^63 drug-like molecules against roughly 10^5 proteoform targets; assays convert biological questions into the labeled numbers models learn from — assay quality caps model quality.
- Candidates die from lack of efficacy, toxicity or off-targets, poor pharmacokinetics, or manufacturability; clinical attrition is dominated by Phase 2, where target validation — not molecular properties — decides outcomes. Position AI value honestly: property optimization and hit-to-lead compression are proven; target discovery is emerging.

---

## 🧬 Molecular Representations

Choose the representation before the model; it bounds everything downstream:

- **SMILES** strings — compact, order-semantic (atom order carries chemistry).
- **Physicochemical descriptors** — molecular weight, lipophilicity, hydrogen-bond donor/acceptor counts and kin.
- **Fingerprints** — structural keys from a fixed fragment dictionary (for example MACCS) versus hashed path- or circular-based fingerprints that need no dictionary but admit bit collisions.
- **2D molecular graphs** — atoms and bonds as nodes and edges for graph neural networks.
- **Learned latents** — embeddings from autoencoders or pretrained molecular models.

---

## 🔬 Virtual Screening Funnel

Stage expensive evaluation last:

1. Load the compound library.
2. Property filters — the Rule-of-5 profile (molecular weight, lipophilicity, H-bond counts, at most one violation) flags oral-bioavailability risk rather than disqualifying; measure distribution shifts around filters, not just counts.
3. Substructure filters remove reactive or frequent-hitter toxicophores.
4. Fingerprint similarity search against known actives — prefer Tanimoto over Dice when hunting close analogs (Dice inflates scores); similarity one is not identity.
5. Triage and assay.

---

## 📐 QSAR Discipline (Small Data)

- Log-transform binding parameters to stabilize variance and enable valid statistics.
- Drop descriptors constant across most compounds; drop descriptor pairs with near-unity correlation, iterating on the most-correlated first — and beware leakage when selecting on the full dataset.
- Lasso-style grid search doubles as feature selection; cap model breadth near five training compounds per descriptor.
- Accept candidates only with strong fit and predictive scores, significant descriptor coefficients, and a simplicity tie-breaker.
- With tens of ligands, every split is fragile: use repeated or nested cross-validation and report score distributions, never a single split.
- Gradient boosting is the frequent tabular winner; split by chemical scaffold (project chemistry, then split so train and test cover the same space) to fight scaffold leakage.

---

## 🎯 Docking and Active Learning

- Frame: prepared receptor structure (itself an uncertain model) + ligand conformers + binding box → pose ranking by a scoring estimate, never a measured free energy.
- Failure modes: preparation sensitivity (protonation, tautomers, waters, metals), rigid-receptor assumptions, scoring degradation on unfamiliar chemistry. Validate top poses against crystallographic poses, seek consensus via rescoring or short simulation, and confirm experimentally — good scores with bad poses are a known trap.
- Billion-compound catalogs make exhaustive docking infeasible: an ML affinity predictor screens the pool and docking is spent only on informative candidates each round (explore/exploit over the pool); the same active-learning loop schedules expensive free-energy calculations during lead optimization.

---

## 🧠 Generative and Affinity Models

- **VAEs** encode molecules as Gaussian clouds with a reconstruction-plus-divergence objective and the reparameterization trick; tuning pathologies: divergence weight too low yields unregularized islands, too high collapses latent information; autoregressive decoders risk posterior collapse — watch the divergence term and perturb the latent to diagnose; cyclical annealing is the practical fix.
- **Sequence models** respect SMILES order semantics (ring-closure syntax included) where feedforward baselines fail.
- **Graph neural networks** for drug-target affinity: parallel encoders over drug graphs and protein residue graphs, pooled and fused into affinity regression; report concordance-index alongside error metrics (ranking is what prioritization needs; error metrics are the differentiable surrogate).
- **Transformers** and protein language models handle global residue–residue contacts that local graph attention and single-vector encodings cannot; platform pattern: foundation-model services plus inference microservices plus reference generative screening loops (fold the target → generate under property oracles → dock → refine → iterate).

---

## ⚠️ Pitfalls

- Choosing a model before fixing the representation and the assay question.
- Trusting a single train/test split on small molecular datasets.
- Treating docking scores as energies, or similarity one as identity.
- Reading filter pass-counts without checking distribution shifts.
- Overselling AI-discovered targets when the demonstrated value is property optimization and cycle-time compression.

---

## 🔗 Integration with Other Skills

- For the underlying ML workflow, see [python-data-science](../../../data/python-data-science/SKILL.md).
- For model interpretation in regulated settings, see [explainable-ai](../explainable-ai/SKILL.md).
- For evaluation discipline and data splits, see [ai-model-evaluation](../ai-model-evaluation/SKILL.md).
- For health-data interoperability and compliance, see [healthtech-standards-security](../healthtech-standards-security/SKILL.md).
- For GPU-scale training, see [distributed-ml-scaling](../../../data/distributed-ml-scaling/SKILL.md).
