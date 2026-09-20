# 📋 Test Management, Static Reviews, and ISTQB Guide

This guide synthesizes the management practices, static reviews, risk-based testing, and quality metrics consolidated in the ISTQB/ISEB body of knowledge, based on **Brian Hambling et al.** (*Software Testing: An ISEB/ISTQB Foundation Guide*).

---

## 1. The 7 Fundamental Principles of Software Testing (ISTQB)

1. **Testing shows the presence of defects, not their absence**: Testing reduces the probability of remaining defects, but does not prove the software's absolute mathematical correctness.
2. **Exhaustive testing is impossible**: Testing every combination of inputs and preconditions is unfeasible; you must apply risk analysis, boundary values, and equivalence partitions.
3. **Early Testing / Shift-Left**: Test activities should begin in the early phases of the life cycle (requirements, architecture) to avoid the exponential spread of correction cost.
4. **Defect Clustering**: A small fraction of modules contains most of the discovered defects (Pareto Principle: ~80% of defects concentrated in ~20% of the code).
5. **Pesticide Paradox**: Running the same test suite repeatedly without changes makes it lose the ability to find new defects; test cases must be continuously reviewed and evolved.
6. **Testing depends on context**: Testing a financial system or an air traffic control system requires substantially more rigorous approaches than a blog or a static e-commerce site.
7. **The Absence-of-Errors Fallacy**: Finding and fixing defects does not guarantee success if the system built does not meet the real needs and expectations of end users.

---

## 2. Static Testing Techniques

Static testing examines software artifacts (requirements, diagrams, source code) **without executing the code**.

### 2.1. Levels of Formality in Human Reviews

```
[ Informal ] ────► [ Walkthrough ] ────► [ Revisão Técnica ] ────► [ Inspeção Formal ]
  (Sem atas)      (Conduzido pelo autor)    (Especialistas/Pares)     (Fagan - Papéis e métricas)
```

| Review Type | Formality | Conducted By | Main Focus | Metrics Collected |
| :--- | :--- | :--- | :--- | :--- |
| **Informal Review** | Low | Any peer | Quick two-way check (pair review) | No |
| **Walkthrough** | Medium | Artifact author | Training, alignment of understanding, and idea gathering | Optional |
| **Technical Review** | High | Lead Reviewer / Moderator | Compliance with technical standards and architecture | Yes |
| **Inspection (Fagan)** | Very High | Trained independent moderator | Systematic defect detection using strict checklists | Yes (reading rate, defects per page) |

### 2.2. Roles in a Formal Inspection
- **Author**: Creator of the artifact under review.
- **Moderator (Facilitator)**: Leads the inspection, manages time, and ensures the process is followed.
- **Scribe (Recorder)**: Records each identified defect and the agreed actions.
- **Reviewers (Inspectors)**: Specialists who examine the document in detail before the meeting.
- **Manager**: Ensures time and resources are allocated, but does not interfere technically in the decisions.

---

## 3. Risk-Based Testing (RBT)

RBT directs test effort, time, and budget toward the areas of the system with the highest probability of failure and the greatest business impact.

### 3.1. Risk Assessment Matrix

$$Nível\ de\ Risco = Probabilidade\ (Likelihood) \times Impacto\ no\ Negócio\ (Impact)$$

```
Alto     │   MÉDIO    │    ALTO    │  CRÍTICO   │
         │  (Testar)  │ (Prioridade)│(Extensivo) │
Impacto  ├────────────┼────────────┼────────────┤
Médio    │   BAIXO    │   MÉDIO    │    ALTO    │
         │(Amostragem)│  (Testar)  │ (Prioridade)│
         ├────────────┼────────────┼────────────┤
Baixo    │   MÍNIMO   │   BAIXO    │   MÉDIO    │
         │(Se houver  │(Amostragem)│  (Testar)  │
         │  tempo)    │            │            │
         └────────────┴────────────┴────────────┘
             Baixa        Média        Alta
                     Probabilidade
```

### 3.2. Practical Application of RBT
1. **Execution Prioritization**: Critical and High-risk test cases are executed first and with multiple methods (BVA Worst-case, MC/DC).
2. **Exit Criteria**: The release is authorized only when $100\%$ of the High/Critical-risk tests pass and the residual risk is acceptable.

---

## 4. Quality Metrics and Test Effectiveness

### 4.1. Defect Removal Efficiency (DRE)
Measures the percentage of defects eliminated before the release to production:

$$DRE = \frac{D_{interno}}{D_{interno} + D_{producao}} \times 100\%$$

Where:
- $D_{interno}$: Defects found and fixed during the development and testing phases.
- $D_{producao}$: Defects reported by users after the release.
- *Excellence Target*: $DRE \ge 95\%$.

### 4.2. Defect Density
$$Densidade = \frac{\text{Total de Defeitos}}{\text{Tamanho do Software (KLOC ou Pontos de Função)}}$$

It reveals components in the repository that are abnormally prone to failure.
