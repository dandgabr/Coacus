# 🧬 Mutation Testing, Fault Seeding, and Metamorphic Testing Guide

This guide synthesizes the advanced theory of test-suite evaluation, software reliability, and the treatment of the oracle problem, grounded in the work of **Ali Mili & Fairouz Tchier** (*Software Testing: Concepts and Operations*) and modern software engineering methodologies.

---

## 1. Fundamentals of Mutation Testing

Mutation testing evaluates the real effectiveness of a test suite by injecting deliberate syntactic changes (mutations) into the source code to check whether the existing tests can detect (kill) those anomalies.

### 1.1. Fundamental Theoretical Premises
1. **Competent Programmer Hypothesis**:
   Programmers develop programs that are close to correct. Real defects are predominantly small syntactic and semantic deviations (operator errors, inverted boundary conditions, swapped variables).
2. **Coupling Effect**:
   Test cases capable of detecting small, simple atomic defects (first-order mutants) are statistically coupled to the ability to detect complex, higher-order composite faults.

---

## 2. Mutation Operators and Mutant Taxonomy

A mutation operator is a grammatical code-transformation rule.

### 2.1. Main Classes of Mutation Operators

| Operator | Name | Description | Original Example | Mutated Code |
| :--- | :--- | :--- | :--- | :--- |
| **AOR** | Arithmetic Operator Replacement | Replaces arithmetic operators | `x = a + b;` | `x = a - b;` or `x = a * b;` |
| **ROR** | Relational Operator Replacement | Replaces relational operators | `if (x >= limit)` | `if (x > limit)` or `if (x == limit)` |
| **COR** | Conditional Operator Replacement | Changes boolean operators | `if (a && b)` | `if (a || b)` |
| **LCR** | Logical Connector Replacement | Inverts boolean values / bits | `flag = !ready;` | `flag = ready;` |
| **SDL** | Statement Deletion | Deletes an executable statement | `calculate_discount();` | `/* removido */` |
| **UOI** | Unary Operator Insertion | Inserts unary operators | `return value;` | `return -value;` or `return ++value;` |

### 2.2. Mutant Classification
- **Killed Mutant**: A test case in suite $T$ failed when running the mutant (behavior diverged from the original program).
- **Live/Surviving Mutant**: The entire test suite passed successfully on the mutant (indicates a gap or weakness in the test assertions).
- **Equivalent Mutant**: The mutant changed the syntax but preserves exactly the same functional semantics as the original (e.g., `i++` vs `++i` in an isolated loop). Determining equivalent mutants automatically is undecidable (Turing's halting problem).

### 2.3. Calculating the Mutation Score
The Mutation Score $MS(T, P)$ measures test sufficiency:

$$MS(T, P) = \frac{K}{M - E} \times 100\%$$

Where:
- $K$ = Number of killed mutants.
- $M$ = Total number of mutants generated.
- $E$ = Number of identified equivalent mutants.

---

## 3. Fault Seeding and the Mills Model

Fault seeding deliberately introduces a known number of artificial defects into the software to estimate the total number of real defects still hidden.

### 3.1. Capture-Recapture Approach (Mills Model)
Let:
- $S$: Number of artificial defects seeded into the code.
- $s$: Number of seeded defects discovered during test execution.
- $n$: Number of real (natural) defects found by the same tests.
- $N$: Estimated total number of real defects present in the code.

Assuming the tests have the same probability of finding real and seeded defects:
$$\frac{s}{S} \approx \frac{n}{N} \implies \hat{N} = \frac{n \times S}{s}$$

### 3.2. Estimating Residual Defects
The estimated number of real defects not yet discovered ($N_{residual}$) is:
$$N_{residual} = \hat{N} - n = n \left( \frac{S}{s} - 1 \right)$$

---

## 4. Metamorphic Testing and the Oracle Problem

The **Oracle Problem** arises when it is computationally prohibitive or theoretically impossible to know in advance the exact expected result of an input (e.g., stochastic algorithms, graphical rendering, natural language processing, machine learning).

### 4.1. Metamorphic Relations (MR)
Metamorphic testing bypasses the oracle by checking **necessary relational properties** across multiple executions of the program with related inputs.

If $f(x)$ computes a function under input $x$, we derive a transformed input $x'$ such that a mathematical relation between $f(x)$ and $f(x')$ must necessarily hold.

#### Examples of Metamorphic Relations in Real Domains:

1. **Shortest Path Algorithm ($ShortestPath(G, A, B)$)**:
   - *Base input*: Graph $G$, nodes $A$ and $B$. Computed distance $= d$.
   - *Metamorphic input*: Graph $G$ where every edge is multiplied by the constant factor $k > 0$.
   - *Relation*: $ShortestPath(k \cdot G, A, B) = k \cdot d$.
2. **Search Engine / Information Retrieval**:
   - *Base input*: Query $Q_1 = \text{"Software Testing"}$. Returns document set $D_1$.
   - *Metamorphic input*: Query $Q_2 = \text{"Software Testing AND Books"}$. Returns $D_2$.
   - *Relation*: $D_2 \subseteq D_1$.
3. **Cryptographic Functions / Hashes**:
   - *Base input*: Message $M_1$.
   - *Metamorphic input*: Message $M_2 = M_1 \text{ with 1 bit flipped}$.
   - *Relation (Avalanche Effect)*: $\text{HammingDistance}(Hash(M_1), Hash(M_2)) \approx \frac{\text{Tamanho do Hash}}{2}$.
