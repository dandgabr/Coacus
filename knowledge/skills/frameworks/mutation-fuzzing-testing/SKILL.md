---
name: mutation-fuzzing-testing
description: "Specialist in Mutation Testing, Fuzzing Engineering, and Requirement Conformance Analysis. Masters systematic injection of synthetic faults, Mutation Score measurement, coverage-guided fuzzing (AFL++, libFuzzer, Atheris, Hypothesis), Test Gap Analysis, and metamorphic oracles."
---

# Mutation Testing, Fuzzing & Requirement Conformance Engineering

This skill guides the AI to conduct extreme robustness testing and deep quality validation using **Mutation Testing**, **Fuzzing Techniques**, and **Requirement Conformance Auditing**.

---

## 🧬 1. Mutation Testing

Mutation Testing evaluates the true effectiveness of a test suite by introducing targeted synthetic changes (*mutants*) into the production code. If the test suite still passes after the change, the mutant **survived** (revealing a *Test Gap* from a weak assertion). If any test fails, the mutant was **killed**.

### A. Canonical Mutation Operators
1. **AOR (Arithmetic Operator Replacement)**: Substitution of arithmetic operators (`+` for `-`, `*` for `/`).
2. **ROR (Relational Operator Replacement)**: Substitution of relational operators (`>` for `>=`, `==` for `!=`).
3. **COR (Conditional Operator Replacement)**: Inversion of logical operators (`and` for `or`).
4. **SDL (Statement Deletion)**: Removal of method calls, assignments, or entire statements.
5. **LCR (Logical Connector Replacement)**: Negation of boolean expressions (`if condition` becomes `if not condition`).

### B. Mutation Score Metric
$$\text{Mutation Score (MS)} = \frac{\text{Mutantes Mortos}}{\text{Total de Mutantes} - \text{Mutantes Equivalentes}} \times 100\%$$
- **Equivalent Mutant**: A mutant that is syntactically different but semantically identical in behavior to the original code (must be excluded from the denominator).
- **Minimum Corporate Target**: $MS \ge 85\%$ for critical components and $MS \ge 90\%$ for financial/security rules.

### C. Tooling by Language
- **Python**: `mutmut` (`mutmut run`, `mutmut results`, `mutmut show <id>`) and `Cosmic Ray`.
- **JavaScript / TypeScript**: `Stryker Mutator` (`npx stryker run`).
- **Java / Kotlin**: `PITest (PIT)`.
- **C / C++**: `Dextool Mutate` or `Mull`.

---

## 💥 2. Fuzzing Engineering (Fuzz Testing)

Fuzzing subjects the program to semi-random, malformed, or genetically generated inputs to detect security flaws, panics, memory overflows, leaks, and unexpected behavior.

### A. Types of Fuzzing
1. **Property-Based Testing**:
   - Uses contract-based input generators (e.g., `Hypothesis` in Python, `fast-check` in JS).
   - Verifies universal invariants (e.g., idempotency, inverse relations, range boundaries).
2. **Coverage-Guided Fuzzing**:
   - Instruments the code to measure basic blocks reached and evolves the inputs that discover new execution paths.
   - Tools: **libFuzzer**, **AFL++ (American Fuzzy Lop)**, **Google Atheris** (Python/C extensions).

### B. The Oracle Problem in Fuzzing
- **Basic Failure Oracle**: Detection of crashes, `NullPointerException`, division by zero, infinite loops (*Timeout*), or improper memory use (*ASan / AddressSanitizer*).
- **Metamorphic Oracle**: Validation of relational consistency properties:
  $$f(\text{entrada\_ordenada}) = f(\text{entrada})$$

---

## 🎯 3. Conformance Audit Against Initial Requirements

Tests with 100% line coverage can still violate system requirements if they validate the wrong behavior or leave acceptance criteria out.

### A. Requirements Traceability Matrix (RTM)
Every test case must be explicitly mapped to an original acceptance criterion:
```text
[REQ-01: Pagamento Pix com Desconto]
├── Teste Funcional: test_pix_discount_applied_nominal()
├── Teste de Limite (BVA): test_pix_discount_boundary_values()
├── Teste de Mutação: mutante em `discount_rate` deve ser morto
└── Teste de Fuzzing: hypothesis_pix_arbitrary_amounts_never_negative()
```

### B. Test Gap Analysis
1. Identify code sections with green execution coverage but with **surviving mutants**.
2. Create specific assertions to force the mutant's death.
3. Test whether the original requirement covers the edge case exposed by the mutant.
### C. EARS Methodology (Easy Approach to Requirements Syntax) & Parameterized Tests
To guarantee full conformance with system requirements, structure the business rules in the 4 EARS syntactic patterns before generating test code:

1. **Ubiquitous**: `The <system> shall <system response>.`
2. **Event-Driven**: `WHEN <trigger>, the <system> shall <system response>.`
3. **State-Driven**: `WHILE <in state>, the <system> shall <system response>.`
4. **Unwanted Behavior**: `IF <trigger condition>, THEN the <system> shall <system response>.`

#### Mechanical EARS → Parameterized Tests Mapping (JUnit 5 / Pytest)
Each group of EARS statements that share the same boundary operation (arrange/act) is deterministically converted into a parameterized test (`@ParameterizedTest` / `@pytest.mark.parametrize`):
- The requirement identifier (`REQ-01`, `REQ-02`) acts as the row label in the data table.
- It eliminates assertion duplication, guarantees that every requirement has an explicit test case, and guides the injection of mutations focused on the acceptance criterion.
