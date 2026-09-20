# 📚 Black-Box Testing Techniques Guide

This guide consolidates the formal techniques for designing functional (black-box) test cases, based on the works of **Paul C. Jorgensen** (*Software Testing: A Craftsman's Approach*), **Brian Hambling et al.** (*Software Testing: ISTQB Guide*), and **Ali Mili & Fairouz Tchier** (*Software Testing: Concepts and Operations*).

---

## 1. Boundary Value Analysis (BVA)

Boundary Value Analysis rests on the empirical observation that the highest defect density occurs at the extremes of input domains.

### 1.1. Canonical Test Values per Variable
For a variable $x$ defined on the interval $[a, b]$, we define the sampling points:
- **$a$**: Exact minimum ($min$)
- **$a^+$**: Immediately above the minimum ($min+$)
- **$nom$**: Nominal value (typical / average)
- **$b^-$**: Immediately below the maximum ($max-$)
- **$b$**: Exact maximum ($max$)
- **$a^-$**: Below the minimum ($min-$) [Invalid / Robust]
- **$b^+$**: Above the maximum ($max+$) [Invalid / Robust]

### 1.2. Taxonomy of BVA Techniques (Jorgensen)

| Technique | Fault Hypothesis | Points per Variable | Total Tests ($n$ variables) | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Traditional BVA** | Single Fault Assumption | $min, min+, nom, max-, max$ | $4n + 1$ | Varies 1 variable across the 4 boundaries while holding the others at $nom$, plus 1 fully nominal case. |
| **Robustness Testing** | Single Fault (with invalid values) | $min-, min, min+, nom, max-, max, max+$ | $6n + 1$ | Includes values outside the valid domain to test exception handling. |
| **Worst-Case Testing** | Multiple Fault Assumption | $min, min+, nom, max-, max$ | $5^n$ | Cartesian product of all 5 points for every variable. |
| **Robust Worst-Case** | Multiple Fault (with invalid values) | $min-, min, min+, nom, max-, max, max+$ | $7^n$ | Complete Cartesian product of the 7 points per variable. |

---

## 2. Equivalence Partitioning (EP)

Equivalence partitioning divides the input domain into classes where the program's behavior is assumed to be uniform.

### 2.1. Formal Classification of Partitions (Jorgensen)
- **Valid Classes ($V_i$)**: Subsets of data expected and accepted by the specification.
- **Invalid Classes ($I_j$)**: Subsets of data not accepted (out-of-range values, incorrect formats, invalid types).

### 2.2. Levels of Rigor in Equivalence Partitioning

1. **Weak Normal**:
   - Relies on the single-fault hypothesis.
   - Selects 1 value from each valid partition $V_i$.
   - Number of tests: $\max(|Classes(V_1)|, |Classes(V_2)|, \dots, |Classes(V_n)|)$.
2. **Strong Normal**:
   - Relies on the multiple-fault (interaction) hypothesis.
   - Covers the Cartesian product of all valid classes: $V_1 \times V_2 \times \dots \times V_n$.
3. **Weak Robust**:
   - Covers 1 value from each valid class and 1 value from each invalid class, testing invalid classes in isolation (one per test).
4. **Strong Robust**:
   - Covers the Cartesian product of all valid and invalid classes.

---

## 3. Decision Table-Based Testing

Ideal for complex business rules, intricate logical relationships, and conditional combinations.

### 3.1. Canonical Decision Table Structure

```
+------------------------------------+-------+-------+-------+-------+
| Condições / Entradas               | Regra 1| Regra 2| Regra 3| Regra 4|
+------------------------------------+-------+-------+-------+-------+
| C1: Saldo suficiente               |   T   |   T   |   F   |   F   |
| C2: Cartão ativo e desbloqueado    |   T   |   F   |   T   |   F   |
| C3: Limite diário não excedido     |   T   |   -   |   -   |   -   |
+------------------------------------+-------+-------+-------+-------+
| Ações / Saídas Esperadas           |       |       |       |       |
+------------------------------------+-------+-------+-------+-------+
| A1: Aprovar transação              |   X   |       |       |       |
| A2: Recusar por cartão bloqueado   |       |   X   |       |       |
| A3: Recusar por saldo insuficiente |       |       |   X   |   X   |
+------------------------------------+-------+-------+-------+-------+
```

### 3.2. Engineering Rules for Decision Tables
1. **Completeness**: For $k$ binary conditions, the complete table must represent $2^k$ elementary rules.
2. **Consistency**: No two identical columns of conditions may lead to divergent or contradictory actions.
3. **Simplification and Don't Care ($-$)**: If the value of a condition does not change the resulting action, combine the columns using the boolean absorption rule. A rule with $m$ "don't care" entries represents $2^m$ elementary rules.

---

## 4. State Transition Testing

Applied to reactive systems whose behavior depends on the event history and the current state (Finite State Machines - FSM).

### 4.1. Elements of an FSM
- **States ($S$)**: Finite set of possible states.
- **Events / Inputs ($E$)**: Stimuli that trigger transitions.
- **Actions / Outputs ($A$)**: Responses produced by the system.
- **Transitions ($T: S \times E \rightarrow S \times A$)**: State-change relation.

### 4.2. State Coverage Criteria (ISTQB & Jorgensen)
- **All States**: Every valid state $s \in S$ is visited at least once.
- **All Transitions (0-switch)**: Every valid transition $t \in T$ is executed at least once.
- **Transition Pairs (1-switch)**: Every sequence of two consecutive transitions ($S_1 \xrightarrow{E_1} S_2 \xrightarrow{E_2} S_3$) is exercised.
- **Invalid Transition Tests**: Send forbidden events to the current state and verify that the system rejects the transition without corrupting the state.

---

## 5. Combinatorial and All-Pairs (Pairwise) Testing

When the number of parameters and values creates a combinatorial explosion that makes the full Cartesian product unfeasible, the All-Pairs technique guarantees that every pair of values between any two parameters is tested in at least one test case.

### 5.1. Mathematical Foundation
- Based on **Orthogonal Arrays** $OA(N, k, v, t)$, where:
  - $N$: Number of test runs
  - $k$: Number of parameters
  - $v$: Number of levels/values per parameter
  - $t$: Interaction strength (usually $t=2$ for pairwise)
- **Practical Effectiveness**: Empirical studies (NIST) show that more than 70-85% of software defects are triggered by the interaction of at most 2 variables, and more than 95% by up to 3 variables.

---

## 6. Use Case Testing

Mapping of scenarios derived from business flows:
- **Basic Flow (Happy Path)**: Typical success sequence with no deviations.
- **Alternative Flows**: Valid variations for reaching the business goal.
- **Exception Flows**: Handling of errors, interruptions, and precondition failures.
- **Traceability Matrix**: Ensure 1:1 coverage between use case steps and executable test cases.
