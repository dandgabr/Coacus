---
name: program-azure-devops
description: >-
  Guides Azure DevOps Services and Server work across organization design,
  Boards, Repos, Pipelines, Test Plans, and Artifacts. Use when planning,
  securing, troubleshooting, or reviewing an Azure DevOps delivery workflow.
---

# Azure DevOps Platform Guidance

Use this skill when work crosses Azure DevOps services or depends on Azure
DevOps-specific permissions, pipeline resources, or project configuration.

## Establish the boundary

- Identify Azure DevOps Services or Azure DevOps Server and the relevant
  organization or collection, project, repository, pipeline, environment, feed,
  and Azure subscription. Confirm uncertain scope before recommending changes.
- Establish the requested outcome, who owns each resource, and whether the user
  authorized read-only inspection, a proposed configuration, or a live change.
- Check which services and integrations are actually in use. Azure Boards,
  Repos, Pipelines, Test Plans, and Artifacts can be adopted independently.
- Resolve changing product behavior from current Microsoft Learn documentation.
  Do not reuse a remembered portal path, task version, agent image, permission
  default, limit, or license rule without checking it.

## Follow the delivery path

Trace the work from its planning record through source change, review, build,
tests, package or pipeline artifact, deployment environment, and post-deployment
evidence. Keep each link specific enough to identify the work item, source
revision, pipeline run, consumed artifact, target environment, and observed
result.

- For organization, collection, project, identity, and access decisions, read
  [service model and governance](references/service-model-and-governance.md).
- For planning, work-item traceability, repositories, pull requests, and branch
  controls, read [Boards and Repos](references/boards-and-repos.md).
- For YAML pipelines, resource permissions, agents, service connections, and
  deployment gates, read [Pipelines and security](references/pipelines-and-security.md).
- For manual, exploratory, and automated test workflows and package feeds, read
  [tests and artifacts](references/tests-and-artifacts.md).
- For Bicep, ARM templates, or Terraform deployed by a pipeline, read
  [infrastructure as code](references/infrastructure-as-code.md).

## Protect production and shared state

- Prefer narrow groups and resource-level permissions. Verify effective access
  and bypass rights before changing organization, project, repository, feed,
  pipeline, agent-pool, service-connection, or environment settings.
- Keep untrusted pull-request code away from production credentials and
  persistent agents that can reach trusted networks. Separate validation from
  privileged deployment and check resource authorization independently of YAML.
- Use short-lived Microsoft Entra workload identity federation or a supported
  managed identity path when applicable. Scope the connection to the required
  subscription or resource group and authorize only the intended pipelines.
- Protect important branches with review and validation policies; protect
  production environments and pipeline resources with the checks appropriate to
  the release process.
- Deploy the artifact that passed validation. Verify its source revision and
  pipeline provenance, then check the deployed revision and a relevant live
  health signal separately from pipeline success.
- Do not create, delete, publish, grant access, change policy, or deploy in a
  live organization or Azure subscription unless the user authorized that
  operation.

## Keep neighboring domains in scope

Use [cloud-azure](../../infrastructure/cloud-azure/SKILL.md) for Azure resource
architecture, governance, and operations beyond the Azure DevOps integration.
Use [devops-engineer](../../roles/devops-engineer/SKILL.md) for provider-neutral
delivery and platform engineering practices. Use the relevant Git skill for
Git behavior that is not specific to Azure Repos.
