---
name: git-conventional-commits
description: "Standardizes atomic commit authoring and version-control history with the Conventional Commits v1.0.0 specification (feat, fix, refactor, perf, test, docs, breaking changes), driven by git-diff inspection."
---

# Git Conventional Commits v1.0.0 Engineering

This skill establishes the rigorous standard for authoring commit messages and managing git history following the **Conventional Commits v1.0.0** specification.

---

## 📜 1. Canonical Message Structure

```text
<tipo>[escopo opcional]: <descrição concisa no imperativo>

[corpo opcional detalhado explicando a motivação e contexto do 'porquê']

[rodapé(s) opcional(is) para breaking changes e links de issue/PR]
```

---

## 🏷️ 2. Canonical Commit Types

| Type | Purpose and Semantic Versioning Impact | Example |
| :--- | :--- | :--- |
| **`feat`** | New feature for the user or API consumer (triggers MINOR). | `feat(auth): add passkey authentication support` |
| **`fix`** | Fix for a defect or bug affecting the user or system (triggers PATCH). | `fix(payment): prevent duplicate webhook processing` |
| **`refactor`**| Internal refactor that changes no external behavior and fixes no bug. | `refactor(orders): extract discount calculation to domain entity` |
| **`perf`** | Improvement in performance, latency, or memory use. | `perf(cache): use Redis pipeline for bulk token validation` |
| **`test`** | Addition or correction of test suites (without changing production code). | `test(fuzz): add property-based tests for currency conversion` |
| **`docs`** | Documentation-only or comment-only changes. | `docs(readme): update multi-agent orchestration instructions` |
| **`style`** | Formatting, lint, and spacing adjustments (no functional impact). | `style(linter): apply prettier formatting across components` |
| **`build`** | Changes to build systems or external dependencies (Maven, Gradle, npm). | `build(deps): bump spring-boot from 3.2.1 to 3.3.0` |
| **`ci`** | Changes to CI/CD scripts and configuration (GitHub Actions, GitLab CI). | `ci(actions): add mutation score check gate to pipeline` |
| **`chore`** | Routine maintenance tasks that modify neither src nor test code. | `chore: clean temporary cache files` |

---

## 💥 3. Breaking Changes
- Add an exclamation mark `!` right after the type/scope to signal a compatibility break (triggers MAJOR):
  ```text
  feat(api)!: change user endpoint response payload structure

  BREAKING CHANGE: The 'userId' field has been renamed to 'id' in the JSON response.
  ```

---

## 🛠️ 4. Commit Inspection and Authoring Flow
1. **Inspect the Staging Area**: Run `git diff --cached` to analyze the staged files and hunks.
2. **Classify the Nature**: Pick the correct semantic type and scope.
3. **Write the Message in Imperative Mood**: Write "add", "fix", "update" (not "added", "fixing", "fixes").
