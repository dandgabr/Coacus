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

---

## 🧰 6. Runners, Containers and Custom Actions (Chandrasekara & Herath)

### 6.1 Jobs, runners and dependencies
Jobs run **in parallel** by default; order them with `needs: <job>`. Runners are GitHub-hosted (`ubuntu-latest`, `macos-latest`, `windows-latest`) or **self-hosted** (registered at repo, organization or enterprise level via `config.cmd`/`config.sh` plus a registration token, ideally run as a service). **Never attach a self-hosted runner to a public repository** — fork pull requests can execute arbitrary code on it.

Jobs can run **inside a container** (`container: node:...`) with **service containers** (e.g. Redis). Container-to-container reaches a service by its **label** (`REDIS_HOST: redis`); a job on the runner instead maps ports (`"6379:6379"`) and uses `localhost`. Docker container *actions* require Linux with Docker installed.

```yaml
services:
  redis:
    image: redis
    options: >-
      --health-cmd "redis-cli ping" --health-interval 10s --health-timeout 5s --health-retries 5
```

### 6.2 Artifacts, caching and passing data
Artifacts persist files across jobs (default retention 90 days) via `actions/upload-artifact`/`download-artifact`. Caching keys on a lockfile hash:

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-build-${{ hashFiles('**/package-lock.json') }}
    restore-keys: ${{ runner.os }}-build-
```

Cache limits: evicted after 7 days unused, 5 GB per repository. **Never cache secrets** — forks can restore the cache.

### 6.3 Custom actions (three types)
| Type | `runs.using` | Runners | Notes |
|---|---|---|---|
| JavaScript | `node20` | Windows/macOS/Linux | Fastest; bundle with `ncc build` |
| Composite | `composite` | Any | Combine `run` steps; each needs `shell:` |
| Docker | `docker` | **Linux only** | Any language; slower; needs Docker |

Metadata must be `action.yml` at the repository root; a JavaScript action uses `@actions/core`/`@actions/github` and exposes outputs consumed as `${{ steps.<id>.outputs.<name> }}`. To publish on the Marketplace: public repo, a single action, an unused name, and 2FA enabled.

### 6.4 Variables, secrets and version currency
- Scope `env:` at workflow, job and step level; set `$GITHUB_ENV` to export to later steps (the legacy `::set-env`/`::set-output` and `node12` are **deprecated**). Default variables include `GITHUB_RUN_ID`, `GITHUB_RUN_NUMBER`, `GITHUB_SHA`, `GITHUB_REF`, `GITHUB_ACTOR`, `GITHUB_REPOSITORY`.
- Secrets are referenced as `${{ secrets.NAME }}`, limited to 100 secrets of 64 KB, hidden from fork PRs, auto-redacted in logs, and may not use the `GITHUB_` prefix. `GITHUB_TOKEN` is auto-created and repo-scoped; use a PAT when its permissions are insufficient.
- Step conditions `success()`/`failure()`/`always()`/`cancelled()` drive rollback and cleanup steps. On Windows the default shell is PowerShell — use `${env:VAR}` (never `${VAR}`) or set `shell: bash`.

**Version currency:** resolve current action majors (`actions/checkout`, `setup-*`, `cache`, `upload-artifact`), runner images and Node runtime from GitHub before pinning them; the table and snippets above are pattern-correct but tags must be verified at authoring time.
