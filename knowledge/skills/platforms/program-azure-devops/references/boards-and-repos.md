# Azure Boards and Repos

Read this reference when planning work, connecting code changes to requirements,
or reviewing Azure Repos governance.

## Plan work at the right level

- Identify the project's process model and work-item types before editing boards
  or queries. Do not assume that every organization uses the same workflow.
- Use backlogs, boards, and iterations to represent the team's actual planning
  and flow. Use delivery plans when a cross-team schedule view is needed; keep
  ownership and priorities with the teams that perform the work.
- Link requirements, work items, code changes, builds, tests, and defects where
  the integration supports it. Verify links from the relevant work item or
  development view instead of assuming that an identifier in a title created a
  link.

## Review repository changes

- Identify the repository type, target branch, contributing groups, and policy
  owners before changing repository or branch settings.
- For important branches, use pull requests, required reviewers, build or status
  validation, and linked-work-item checks as appropriate to the team's risk and
  traceability needs.
- Limit policy bypass, force-push, policy editing, and permission management to
  the smallest trusted group. Check whether an administrator can bypass the
  policy and how emergency changes are reviewed afterward.
- Verify policies on the exact target branch. A YAML pipeline that runs is not
  proof that the branch requires that pipeline to pass.
- For GitHub repositories connected to Boards, confirm the supported service
  model and integration prerequisites before relying on automatic links.

## Current references

- [Azure Boards documentation](https://learn.microsoft.com/en-us/azure/devops/boards/?view=azure-devops)
- [Link work items to objects](https://learn.microsoft.com/en-us/azure/devops/boards/backlogs/add-link?view=azure-devops)
- [Azure Boards and GitHub links](https://learn.microsoft.com/en-us/azure/devops/boards/github/link-to-from-github?view=azure-devops)
- [Secure Azure Repos and pull requests](https://learn.microsoft.com/en-us/azure/devops/repos/git/secure-repositories-pull-requests?view=azure-devops)
- [Set and manage branch policies](https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies?view=azure-devops)
- [About pull requests and permissions](https://learn.microsoft.com/en-us/azure/devops/repos/git/about-pull-requests?view=azure-devops)
