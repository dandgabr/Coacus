---
name: program-github-actions
description: "Specialist in the GitHub Platform, GitHub Actions, and CI/CD. Covers repository governance, protection rules (Rulesets), CODEOWNERS, Pull Request flows, automation with the GitHub CLI (gh), security with GHAS (Dependabot, CodeQL, Secret Scanning), GitHub Packages (ghcr.io), GitHub Codespaces, and complete YAML workflow engineering (reusable workflows, composite actions, matrix strategies, concurrency, protected environments, OIDC authentication, and caching)."
---

# GitHub Platform, Governance & GitHub Actions CI/CD

This skill guides the artificial intelligence to act as a **Senior Specialist in the GitHub Platform and CI/CD Engineering with GitHub Actions**, spanning repository governance, advanced code security (GHAS), automation with the GitHub CLI (`gh`), and the design of resilient continuous integration and delivery pipelines.

---

## 🌿 1. Repository Governance and Structure

### 1.1 Branching Strategies
- **GitHub Flow**: The `main` branch is always stable and ready to deploy; short-lived feature branches merged via Pull Request after CI validation and reviewer approval.
- **Trunk-Based Development**: Direct commits to `main` or feature branches with a lifecycle under 24 hours, accompanied by *feature flags*.
- **GitFlow**: A structure with `main`, `develop`, `release/*`, `feature/*`, and `hotfix/*` for formal release cycles with semantic versioning.

### 1.2 Repository Rulesets and CODEOWNERS
- **Branch Protection & Rulesets**:
  - Requiring a Pull Request with at least 1 mandatory approval.
  - Blocking merges while CI status checks are failing.
  - Requiring commits signed with a GPG or SSH key.
  - Strictly blocking force pushes (`git push --force`).
- **`.github/CODEOWNERS`**:
```ini
# Fallback global
* @org-core-team

# Infraestrutura e CI/CD
.github/workflows/ @org-devops-team
terraform/ @org-devops-team

# Backend e Segurança
src/backend/ @org-backend-leads
src/backend/auth/ @org-security-team
```

---

## ⚙️ 2. GitHub Actions: Workflow Anatomy and Patterns

### 2.1 Secure CI/CD Workflow with Minimal Permissions
```yaml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
    paths-ignore: ['docs/**', '*.md']
  pull_request:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pull-requests: write
  security-events: write

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run Tests with Pytest
        run: pytest --cov=src --cov-report=xml

      - name: Run Snyk Code SAST
        uses: snyk/actions/python@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
```

### 2.2 Reusable Workflows (`workflow_call`)
```yaml
# .github/workflows/reusable-deploy.yml
name: Reusable Deploy

on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
    secrets:
      DEPLOY_KEY:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
      - name: Deploy application
        run: ./deploy.sh --env ${{ inputs.environment }}
        env:
          KEY: ${{ secrets.DEPLOY_KEY }}
```

### 2.3 OIDC Authentication with Cloud Providers (AWS / GCP / Azure)
Eliminate long-lived static credentials in `secrets`:
```yaml
jobs:
  deploy-aws:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    steps:
      - name: Configure AWS Credentials via OIDC
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/GitHubActionsDeployRole
          aws-region: us-east-1
```

---

## 🔒 3. GitHub Advanced Security (GHAS)

1. **Dependabot**:
   - `dependabot.yml` configured for daily security updates and dependency vulnerability checks.
2. **CodeQL (SAST)**:
   - Deep static analysis of source code integrated into the *Security > Code scanning* tab.
3. **Secret Scanning & Push Protection**:
   - Immediate blocking of commits containing API keys, private tokens, or credentials at push time.

---

## 💻 4. Automation with the GitHub CLI (`gh`)

```bash
# Autenticação e status
gh auth status
gh repo view --json name,description,defaultBranchRef

# Gerenciamento de Pull Requests
gh pr create --title "feat: novo endpoint de pagamentos" --body "Implementa RFC 10008" --reviewer "org-core-team"
gh pr review 123 --approve --body "LGTM!"
gh pr merge 123 --squash --delete-branch

# Disparo e inspeção de Workflows
gh workflow run ci.yml --ref main -f environment=staging
gh run list --workflow=ci.yml --limit 5
gh run watch
gh run view --log-failed
```

---

## 📦 5. GitHub Packages (ghcr.io) and Codespaces

- **GitHub Container Registry (`ghcr.io`)**: Native authentication with `GITHUB_TOKEN`, publishing and versioning of OCI images with commit SHA and semver tags.
- **GitHub Codespaces**: Configuration with `.devcontainer/devcontainer.json` for reproducible, pre-configured development environments in seconds.
