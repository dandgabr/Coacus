# Infrastructure as Code with Azure Pipelines

Read this reference when a pipeline validates or deploys ARM templates, Bicep,
Terraform, or other infrastructure definitions.

## Keep infrastructure changes reviewable

- Confirm the selected IaC tool, deployment scope, target subscription and
  resource group, state ownership, and production-change process.
- Version infrastructure definitions with application or platform code as
  appropriate. Review changes as code and keep environment-specific values and
  credentials out of source control.
- Validate the template and preview the expected changes before deployment.
  For Bicep/ARM, Azure Resource Manager `what-if` previews changes but can have
  analysis limits; inspect the full result and resolve unknown or unexpected
  changes before proceeding.
- Separate non-production and production stages. Protect production with
  resource-level approvals or checks and an identity scoped to the required
  resources. Do not treat successful template validation as deployment
  authorization.
- After deployment, inspect deployment history and resource state, then verify
  the application or infrastructure health signal relevant to the change.

## Protect deployment identity

Use a service connection scoped to the smallest Azure resource boundary that
supports the deployment. Prefer short-lived workload identity federation or a
supported managed identity path over a stored long-lived secret. Check the
service connection's pipeline authorization and approvals independently from
the template's contents.

## Current references

- [Bicep deployment with Azure CLI](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/deploy-cli)
- [Bicep what-if](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/deploy-what-if)
- [ARM preflight validation](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/deploy-preflight)
- [Azure Pipelines security](https://learn.microsoft.com/en-us/azure/devops/pipelines/security/overview?view=azure-devops)
- [Approvals and checks](https://learn.microsoft.com/en-us/azure/devops/pipelines/process/approvals?view=azure-devops)
- [Azure Pipelines and Microsoft Entra workload identity](https://learn.microsoft.com/azure/devops/pipelines/library/add-devops-entra-service-connection?view=azure-devops)
