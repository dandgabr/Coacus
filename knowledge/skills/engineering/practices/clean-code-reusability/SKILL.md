---
name: "clean-code-reusability"
description: "Ensures clean, readable, redundancy-free code through the active reuse of existing components, documented according to the best practices of the technology in use."
---

# AI Skill: Clean Code & Reusability

This skill guides the artificial intelligence to secure the highest code quality in a project, focusing on readability, maintainability (Clean Code), the active elimination of redundancy by reusing existing logic (Reusability), and precise, expressive documentation.

---

## 🧭 Clean Code and Reusability Guidelines

When working under this skill, base your technical decisions on the following fundamental pillars:

### 1. Clean Code
- **Small, Focused Functions**: Keep functions small and single-purpose (Single Responsibility Principle). If a function does more than one thing, split it.
- **Significant Names**: Use descriptive, pronounceable names for variables, functions, classes, and files. Avoid obscure abbreviations and needless suffixes.
- **Clean Signatures**: Limit the number of parameters a function takes (ideally at most 2 or 3). If you need more, wrap them in a parameter object or structure.
- **Avoid Side Effects**: Functions should preferably be pure, never changing global or external state unexpectedly.
- **Clean Error Handling**: Use exceptions instead of returning error codes. Isolate `try-catch` blocks in dedicated functions when they clutter the main logic.

### 2. Redundancy Validation and Active Reuse
- **Mandatory Prior Scan**: **Before creating any new function, utility, or class**, search the codebase (through semantic search or grep) to check whether similar or identical logic already exists.
- **DRY Principle (Don't Repeat Yourself)**:
  - If you find a function that does exactly what you need, **reuse it**.
  - If you find a function that does something very similar, **refactor it** (for example, add an optional parameter or generalize the type) instead of duplicating the code.
- **Helper Centralization**: Keep utility functions in appropriate places (such as `utils/`, `helpers/`, or shared domain files) and export them clearly.
- **Duplicate Refactoring**: If your analysis finds redundant code already in the codebase, suggest or carry out its consolidation into a single shared abstraction.

### 3. Secure Clean Code & SAST
- **Zero Hardcoded Secrets**: Never place passwords, API keys, JWT tokens, or certificates directly in code. Use environment variables or secret managers (for example, HashiCorp Vault or AWS Secrets Manager).
- **Secure Error Handling**: Handle exceptions without exposing sensitive stack traces, infrastructure details, or personal data (PII) to the end user.
- **Sanitization and Validation at the Contact Point**: Apply strict validation to every external data input (prevention of SQLi, XSS, Path Traversal, and Insecure Deserialization).

### 4. Correct and Significant Documentation
- **Focus on the "Why", Not the "What"**: Avoid redundant documentation that merely restates the function signature. Focus on explaining complex business rules, non-obvious design decisions, or technical constraints.
- **Industry Standards**:
  - **TypeScript/JavaScript**: Use the **JSDoc** standard, detailing types, parameters (`@param`), return values (`@returns`), and possible exceptions (`@throws`).
  - **Python**: Use **Docstrings** following the Google style or PEP 257.
- **Moderate Inline Documentation**: Comments inside code should be rare and serve only to explain complex or temporary logic (hacks). If code needs many comments to be understood, refactor it for readability instead.

---

## ⚙️ Implementation and Review Protocol

Whenever you are asked to create, modify, or review code:

1. **Discovery Phase (Search for Reuse)**:
   - Formulate search terms for the desired functionality.
   - Run text or regex searches across the workspace to map existing functions with similar purposes.
2. **Signature Design**:
   - Design the function to stay focused and aligned with the project language's conventions.
3. **Writing and Documentation**:
   - Implement the logic without redundancy and write the appropriate documentation (JSDoc, Docstrings).
4. **Static Rule and Security Verification**:
   - Ensure compliance with lint tools (ESLint, Pylint, Flake8) and static security analysis (see [sast-code-review](../../../security/appsec/sast-code-review/SKILL.md) and [appsec-owasp-asvs](../../../security/appsec/appsec-owasp-asvs/SKILL.md)).

---

## 🔗 Integration with Other Development Skills

This skill works across the board and should be consulted by every development skill:
- [backend-developer](../../../roles/backend-developer/SKILL.md): Ensures that APIs, services, and repositories do not duplicate business and persistence rules.
- [frontend-developer](../../../roles/frontend-developer/SKILL.md): Prevents duplicate components or hooks and enforces good client-side code-organization practices.
- [software-architect](../../../roles/software-architect/SKILL.md): Helps maintain design cohesion by promoting clean, DRY abstractions.
- [sast-code-review](../../../security/appsec/sast-code-review/SKILL.md): Validates the absence of security antipatterns and vulnerabilities in clean code.
- [lang-typescript](../../../languages/lang-typescript/SKILL.md): Guides type reuse and JSDoc documentation.
- [lang-python](../../../languages/lang-python/SKILL.md): Guides PEP 8 style, correct docstring creation, and cyclomatic-complexity reduction.

> For an example of a reuse pattern (extensible dispatcher), see [`examples/reusability_patterns.md`](./examples/reusability_patterns.md). For SOLID guidelines applied to Python, see [`references/clean_code_solid_python.md`](./references/clean_code_solid_python.md).
