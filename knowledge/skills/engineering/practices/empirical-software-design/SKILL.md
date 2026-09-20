---
name: empirical-software-design
description: Acts as a specialist in Empirical Software Design and incremental Tidy First-style refactoring (Kent Beck). Covers structure vs. behavior (tidying separate from change), the economics of design (real options, cost of change), coupling and cohesion, the tidyings repertoire (guard clauses, extract variable/function, inline, join/break, moving features), and the decision of When to Tidy (Now? Never? Later?).
---

# AI Skill: Empirical Software Design (Tidy First)

This skill guides the artificial intelligence to improve code design **incrementally, in small and reversible steps**, separating structure changes from behavior changes, based on the work *Tidy First? A Personal Exercise in Empirical Software Design* (Kent Beck).

---

## 🎯 1. Central Principle: Separate Structure from Behavior

- **Behavior change** = changing what the system does (new rules, features, fixes).
- **Structure change (tidying)** = changing how the code is organized **without changing its behavior** (extract function, rename, move code).
- **Never mix the two in the same commit or change**. Tidy first, then change behavior ("Tidy First?"), or tidy after ("Tidy After?"), but state explicitly which one you are doing.
- Benefit: small diffs, trivial review, reliable bisect, and minimized merge conflicts.

---

## 💰 2. The Economics of Design

Software design is, above all, an **economic exercise**: minimize total future cost.

- **Human cost ≠ today's cost**: the cost of a change includes the time of whoever reads, understands, and modifies it later. Paying a little now (tidy) can greatly reduce the cost tomorrow.
- **Real Options**: keeping flexibility has value — like a financial option, deferring irreversible decisions and simplifying reversible ones creates value. Do not centralize too early or spread prematurely.
- **`Cost(change) = Σ effort(read, understand, edit, test)`**: optimize for the future reader, not for today's writer.
- **Option vs. obligation**: every coupling creates an obligation; every well-placed abstraction creates an option. Prefer designs that increase options over the medium term.
- **Time scale**: tidyings take seconds or minutes; structural designs take days; optimize the aggregate rate of change, not each line.

---

## 🧲 3. Coupling and Cohesion (Design Theory)

- **Coupling**: how much changing one element forces others to change. Reduce coupling to reduce the cost of change.
- **Cohesion**: elements that change together should live together. Increase cohesion by grouping around reasons to change.
- **Local design rule of thumb**: prefer the design that makes the next change cheaper — judge each decision in context, empirically ("empirical software design"), without dogmas such as "fewer lines is better".
- **No universal Best Practices**: good design depends on the specific system's flow of changes. Watch where the code changes often and couple or decouple accordingly.

---

## 🧰 4. Tidyings Repertoire (catalog of micro-refactorings)

Perform tidyings in minutes, one per commit:

| Tidying | Short description |
| :--- | :--- |
| **Guard Clause** | Exit early on invalid conditions to flatten nesting. |
| **Extract Variable / Function** | Name expressions and steps to communicate intent. |
| **Inline Variable / Function** | Remove indirections with no communicative value. |
| **Join Function** | Merge functions called only once, once, together. |
| **Block Commentary** | Mark blocks with transitional comments that later become functions. |
| **Explicit Parameters** | Replace implicit params (globals/fields) with explicit parameters. |
| **Normalize Symbols** | Standardize names for the same concept (one concept, one name). |
| **New Interface (Old Implementation)** | Introduce the target interface and delegate, migrating usages gradually. |
| **Move Function/Field** | Relocate closer to the data/behaviors it changes with. |
| **Combine Similar Shapes** | Merge similar structures into one (careful: only if the cost of generalizing < keeping two). |
| **Helper Function & Helper Relation** | Extract repetition into helpers; bring the helper closer to its users. |
| **Reorder Logic (read top-down)** | Put the main case first and the details after. |
| **Extract Constant** | Magic numbers/strings become named constants. |

---

## 🤔 5. Decision: When to Tidy?

Apply the decision tree before any change:

1. **Is it worth tidying?** (cost of the tidy × future savings)
2. **Tidy now (Now), later (Later), or never (Never)?**
   - **Now**: the tidy is small (minutes) and unblocks the immediate change.
   - **Later**: necessary, but large or unsafe now — note it (TODO/issue) and do it later, as its own step.
   - **Never**: a tidy that does not pay for itself (code about to die, a stable area, deep freeze).
3. **Always ask: does this tidy move me closer to or further from the target behavior?**
4. **Limit**: tidyings optionally in a batch, but **never** mix tidy + feature in the same diff. If the tidy turns into an avalanche, cut it and do only the essentials.

---

## 🔄 6. Execution Protocol (for AI in real codebases)

1. **Read to understand where change happens**: identify the requested change point and the coupled surroundings.
2. **List candidate tidyings**: cheap, local, and change-enabling.
3. **Classify each one**: Now / Later / Never, with a short economic justification.
4. **Execute the "Now" tidyings** in separate commits (`refactor:`), behavior preserved (green tests).
5. **Implement the behavior change** in its own commit (`feat:`/`fix:`).
6. **Communicate**: in reviews, explain 1) what changes, 2) what was tidied before or after it and why.
7. **Never** use the tidy to change behavior "along the way".

---

## 🔗 Integration with Other Skills

- [clean-code-reusability](../clean-code-reusability/SKILL.md): clean code supplies the vocabulary; Tidy First supplies the *rhythm* and economics of change.
- [software-architect](../../../roles/software-architect/SKILL.md): micro tidyings feed the architect's macro decisions with real change data.
- [sast-code-review](../../../security/appsec/sast-code-review/SKILL.md): review tidyings to ensure no security control was loosened.
- [framework-testing](../../../frameworks/framework-testing/SKILL.md): green tests are the precondition for any tidy (safety net).
- [lang-python](../../../languages/lang-python/SKILL.md), [lang-java](../../../languages/lang-java/SKILL.md), [lang-typescript](../../../languages/lang-typescript/SKILL.md), [lang-go](../../../languages/lang-go/SKILL.md), [lang-csharp](../../../languages/lang-csharp/SKILL.md): apply the idiomatic tidyings of the language in use.
