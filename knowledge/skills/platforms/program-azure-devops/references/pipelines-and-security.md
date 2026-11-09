# Azure Pipelines and Security

Read this reference when authoring or reviewing YAML pipelines, deployment
resources, agents, or service connections.

## Model the pipeline as a resource graph

- Identify the event, repository and ref, templates, pipeline resources,
  service connections, variable groups, secure files, agent pools, artifacts,
  environments, and external services each stage can consume.
- Prefer a reviewable YAML definition for versioned pipeline behavior where it
  fits the team's workflow. Separate build, test, package, and deployment stages
  so that trust and approval boundaries are visible.
- Protect shared templates and resources. Check resource authorization and owner
  configured approvals or checks; a condition written only in YAML is not the
  same as a check enforced by the resource owner.
- For protected deployment environments, consider branch-control and required
  template checks, approvals, exclusive locks, and other gates the release
  process needs. Check the allowed fully qualified refs and behavior for an
  unknown protection state.

## Isolate untrusted work

- Treat pull-request code, contributed scripts, pipeline parameters, and
  downloaded artifacts from untrusted runs as untrusted inputs.
- Do not expose production service connections, secrets, or privileged tokens
  to untrusted validation jobs. Separate unprivileged validation from trusted
  release stages and pass only the reviewed artifact across that boundary.
- Prefer Microsoft-hosted agents for untrusted code when their clean virtual
  machine per run and platform support fit the workload. Treat self-hosted
  agents as persistent security boundaries: review cleanup, network
  reachability, identity, software installed, and which projects or pipelines
  can use the pool. Separate pools by project or sensitivity when that reduces
  lateral movement or cross-project contamination.
- Restrict agent-pool and service-connection use to intended projects and
  pipelines. Do not authorize every pipeline by default.
- Prefer Microsoft Entra workload identity federation or an applicable managed
  identity over long-lived client secrets or personal access tokens. Verify the
  federated subject, tenant, audience, resource scope, and permissions before
  relying on the connection.

## Verify the delivery evidence

Bind each deployment to the source revision, pipeline run, selected pipeline
resources, exact artifact or package digest, and target environment. Verify the
deployed revision and a health signal independently from the pipeline result.
For a failed deployment, establish the last known good artifact and recovery
path before proposing a rollback.

## Current references

- [Azure Pipelines security overview](https://learn.microsoft.com/en-us/azure/devops/pipelines/security/overview?view=azure-devops)
- [Resources in YAML pipelines](https://learn.microsoft.com/en-us/azure/devops/pipelines/process/resources?view=azure-devops)
- [Approvals and checks](https://learn.microsoft.com/en-us/azure/devops/pipelines/process/approvals?view=azure-devops)
- [Environments and deployment history](https://learn.microsoft.com/en-us/azure/devops/pipelines/process/environments?view=azure-devops)
- [Microsoft-hosted agents](https://learn.microsoft.com/en-us/azure/devops/pipelines/agents/hosted?view=azure-devops)
- [Azure Pipelines and Microsoft Entra workload identity](https://learn.microsoft.com/azure/devops/pipelines/library/add-devops-entra-service-connection?view=azure-devops)
- [Azure Pipelines YAML schema](https://learn.microsoft.com/en-us/azure/devops/pipelines/yaml-schema/?view=azure-pipelines)
