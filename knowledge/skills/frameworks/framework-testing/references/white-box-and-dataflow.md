# 🔬 Structural (White-Box), Control Flow, and Data Flow Testing Guide

This guide covers the theoretical and mathematical foundations of structural (white-box) software testing, derived from the work of **Paul C. Jorgensen**, **Ali Mili & Fairouz Tchier**, and safety-critical reliability guidelines (RTCA DO-178C / ISO 26262).

---

## 1. Control Flow Graph (CFG) and DD-Paths

The Control Flow Graph $G = (V, E)$ models every possible execution path of a software unit, where $V$ are basic blocks of statements and $E$ are the directed arcs of control transfer.

### 1.1. Decision-to-Decision Paths (DD-Paths - Jorgensen)
A DD-Path is a chain of nodes in a CFG that:
1. Consists of a single node with in-degree $\ge 2$ (junction node), OR
2. Consists of a single node with out-degree $\ge 2$ (decision node), OR
3. Is a maximal path of nodes with in-degree $\le 1$ and out-degree $\le 1$ (a linear sequence with no branching).

Compressing a CFG into a DD-Path graph preserves all control-flow testing properties while simplifying structural analysis.

---

## 2. McCabe's Cyclomatic Complexity and Basis Path Testing

Cyclomatic Complexity $V(G)$ measures the number of linearly independent paths in a basis of the graph's vector space.

### 2.1. Calculation Formulas
For a graph with $e$ edges, $n$ nodes, and $p$ connected components (usually $p=1$ for a function):
$$V(G) = e - n + 2p$$

For planar graphs where all decisions are binary (simple predicates $d$):
$$V(G) = d + 1$$
$$V(G) = \text{Número de regiões fechadas no plano} + 1$$

### 2.2. Basis Path Testing Algorithm
1. **Draw the CFG** corresponding to the code.
2. **Compute $V(G)$** to determine the exact size of the basis of linearly independent paths.
3. **Select the Basis Path**: Choose a path representative of the system's typical execution.
4. **Generate the Derived Paths**: Systematically flip the outcome of each predicate along the basis path to derive $V(G)$ orthogonal paths.
5. **Formulate the Test Cases**: Define input values that force the program flow through each path in the basis.

---

## 3. Control Flow Coverage Hierarchy

```
         [ Multiple Condition Coverage (MCC) ]
                         │
                         ▼
        [ Modified Condition/Decision Coverage (MC/DC) ]
                         │
                         ▼
         [ Decision / Branch Coverage (C1) ]
                         │
                         ▼
         [ Statement Coverage (C0) ]
```

### 3.1. Statement Coverage ($C_0$)
- Requires that every executable statement be traversed at least once.
- **Formula**: $\text{Cobertura } C_0 = \frac{\text{Instruções Executadas}}{\text{Total de Instruções}} \times 100\%$.
- **Limitation**: Insensitive to empty branches (`if (cond) { ... }` without `else`), which can leave branches and conditions entirely untested.

### 3.2. Branch / Decision Coverage ($C_1$)
- Requires that every conditional decision be evaluated as True (T) and False (F) in distinct runs.
- Guarantees $100\%$ of $C_0$ coverage, but does not evaluate the atomic conditions inside compound expressions.

### 3.3. Modified Condition/Decision Coverage (MC/DC)
Required for software at the highest criticality level (e.g., avionics DO-178C Level A).

**MC/DC Requirements**:
1. Every decision reaches every possible outcome (T and F).
2. Every atomic condition within the decision reaches every possible outcome (T and F).
3. Each atomic condition is shown to affect the decision outcome **independently** (varying only that condition while the others remain fixed or have no short-circuit effect).

For a decision with $n$ atomic conditions:
- **Number of tests required**: $n + 1$ tests (in contrast to $2^n$ for full MCC).

#### Example MC/DC Independence Table for $(A \lor B) \land C$:

| Test | A | B | C | Decision Result | Test Pair for A | Test Pair for B | Test Pair for C |
| :---: | :-: | :-: | :-: | :---: | :---: | :---: | :---: |
| 1 | **T** | F | **T** | **T** | (1, 2) | | (1, 4) |
| 2 | **F** | F | **T** | **F** | (1, 2) | (3, 2) | |
| 3 | F | **T** | **T** | **T** | | (3, 2) | (3, 5) |
| 4 | T | F | **F** | **F** | | | (1, 4) |
| 5 | F | T | **F** | **F** | | | (3, 5) |

---

## 4. Data Flow Testing (Jorgensen & Mili)

Focuses on the life cycle of variables within the program: creation, modification, and use.

### 4.1. Fundamental Definitions
- **$\text{def}(v, n)$**: The value of variable $v$ is defined or modified at node $n$ (e.g., assignment `v = expr;`, input read).
- **$\text{use}(v, n)$**: The value of variable $v$ is referenced at node $n$.
  - **c-use (computational use)**: Use in an arithmetic computation or direct assignment.
  - **p-use (predicate use)**: Use in a conditional expression that decides control flow.
- **Def-Clear Path**: An underlying path between node $i$ and node $j$ for variable $v$ where no new definition of $v$ occurs in the intermediate nodes.
- **du-path (Definition-Use Path)**: A simple path from the definition node $\text{def}(v, i)$ to the use node $\text{use}(v, j)$ that is definition-clear for $v$.

### 4.2. Data Flow Coverage Criteria

| Criterion | Requirement |
| :--- | :--- |
| **All-Defs** | For every definition of $v$ at $n$, the test set must contain at least one def-clear path to some use ($\text{c-use}$ or $\text{p-use}$). |
| **All-P-Uses** | For every definition of $v$ and every reachable $\text{p-use}$, a def-clear path must be executed. |
| **All-C-Uses** | For every definition of $v$ and every reachable $\text{c-use}$, a def-clear path must be executed. |
| **All-Uses** | Covers at least one def-clear path from each definition to every possible use ($\text{c-use}$ and $\text{p-use}$). |
| **All-DU-Paths** | Covers **every** simple, definition-clear du-path between all definitions and all their uses. (The most rigorous data-flow criterion). |

---

## 5. Program Slicing (Mili)

Program slicing decomposes a program into the parts relevant to the value of a specific variable at a point of interest.

### 5.1. Slicing Criterion
A slice criterion is formally defined by:
$$C = (s, V)$$
where $s$ is a statement/line of the program and $V$ is a subset of the variables observed at $s$.

### 5.2. Slicing Modalities
- **Static Slice**: Contains every statement in the program that can influence the values of $V$ at $s$ for any possible input (computed via control and data dependency graphs).
- **Dynamic Slice**: Contains only the statements that actually influenced the values of $V$ at $s$ during a run with a specific input.
- **Applications in Testing**:
  - **Regression Isolation**: If a code change does not belong to the slice of a test's output variables, the test will be unaffected (regression suite reduction).
  - **Fault Localization**: The intersection of the slices of failing tests with the complement of the slices of passing tests points with high probability to the defect's exact location (Fault Localization).
