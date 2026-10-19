# Azure DevOps Service Model and Governance

Read this reference when selecting or reviewing an organization, collection,
project, team, or identity boundary.

## Select the service model

Establish whether the target is Azure DevOps Services or Azure DevOps Server.
Compare hosting, network reachability, identity integration, data residency,
upgrade ownership, integrations, and operational responsibilities against the
organization's requirements. Do not assume that Services and Server have the
same feature availability or administration surface. Resolve feature parity and
support details from the documentation for the exact target.

## Choose scope from collaboration and access needs

- Treat an organization or Server collection as an administrative and resource
  boundary that can contain multiple projects.
- Use projects to group related work, repositories, pipelines, test assets, and
  feeds. Use teams, area paths, and iteration paths to organize collaboration
  within a project when their access model is sufficient.
- Prefer fewer projects when teams share assets, process, and visibility. Use
  separate projects when distinct access controls, policies, or process needs
  justify the extra administration. Confirm effective permissions; a project
  boundary alone does not prove that every resource is isolated as intended.
- Map organization or collection, project, team, repository, pipeline, feed, and
  environment ownership before granting access. Prefer groups with named
  owners over scattered individual permissions.
- Before changing a broad group or inherited permission, inspect its members,
  inheritance, explicit denies, and affected resources. Explain the impact and
  confirm authorization for a live change.

## Current references

- [What is Azure DevOps?](https://learn.microsoft.com/en-us/azure/devops/user-guide/services?view=azure-devops)
- [Get started with Azure DevOps](https://learn.microsoft.com/en-us/azure/devops/get-started/?view=azure-devops)
- [About permissions and security groups](https://learn.microsoft.com/en-us/azure/devops/organizations/security/about-permissions?view=azure-devops)
- [Troubleshoot access and permission issues](https://learn.microsoft.com/en-us/azure/devops/organizations/security/troubleshoot-permissions?view=azure-devops)
- [Install and configure Azure DevOps Server](https://learn.microsoft.com/en-us/azure/devops/server/install/get-started?view=azure-devops-server)
