---
name: program-github-actions
description: >-
  Designs, reviews and troubleshoots GitHub Actions workflows, runners and
  delivery pipelines. Covers workflow reuse, deployment controls, supply-chain
  security, compliance and performance. Use for CI/CD automation or workflow
  security reviews on GitHub.
---

# GitHub Actions Engineering

Use this skill to design, audit or troubleshoot GitHub Actions workflows and
their execution environment. First establish the repository's organization,
visibility, event sources, trust boundaries, deployment targets and applicable
plan or enterprise controls. Verify current platform behavior against official
GitHub documentation before prescribing a version, limit, feature availability
or billing detail.

## Workflow design

Design the workflow around the required event and outcome. Keep triggers,
permissions, job dependencies, conditions, concurrency and artifact flow
explicit. Reuse workflows or composite actions when shared ownership and
versioning justify the extra interface; define inputs, outputs and secret
passing deliberately. Avoid broad workflow-level token permissions when a
narrower job-level grant is sufficient.

Use [Workflow authoring and reuse](references/workflow-authoring-and-reuse.md)
for syntax, contexts, events, reusable workflows and custom actions.

## Execution and delivery

Select GitHub-hosted or self-hosted runners based on trust, network access,
hardware, isolation and operational ownership. Treat runner labels as routing,
not as isolation. Separate build artifacts from dependency caches, preserve
source-to-artifact traceability, and gate production deployment through
appropriate environments and identity federation.

Use [Runners and delivery](references/runners-and-delivery.md) for runner
security, CI/CD structure, artifacts, deployments, environments and OIDC.

## Security and governance

Treat workflow files, third-party actions, event payloads, artifacts and runner
state as part of the software supply chain. Minimize token and secret exposure,
validate untrusted values before using them in expressions or commands, and
never execute untrusted pull-request code on a privileged runner. Use repository
and organization policy to constrain permitted actions and runner access.

Use [Security, compliance and efficiency](references/security-compliance-efficiency.md)
for untrusted events, action references, permissions, traceability, policy and
cost controls.

## Review outcome

For an audit, report each finding with the workflow path or setting, the
triggering event or trust boundary, the impact, and a corrective action. Separate
confirmed configuration from provider behavior that was not tested. For a new
workflow, verify its YAML and expression semantics, run the repository's
available checks, and identify any provider-side or deployment behavior that
remains unverified.
