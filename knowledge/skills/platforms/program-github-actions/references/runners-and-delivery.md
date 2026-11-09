# Runners and Delivery

Use this reference when selecting execution capacity or designing a path from
source to a released or deployed artifact.

## Runner selection and operations

GitHub-hosted runners provide a managed execution environment. Self-hosted
runners add network, hardware and software control, but also add persistent
state, patching and isolation responsibilities. Do not route untrusted pull
request code to a self-hosted runner with access to credentials or internal
resources. GitHub warns that self-hosted environments can be persistently
compromised by untrusted workflow code; use separate runner groups and narrow
repository access to limit blast radius. See [secure use of GitHub
Actions](https://docs.github.com/en/actions/reference/security/secure-use).

For autoscaling, prefer ephemeral runners and remove or wipe each machine after
its job. Preserve runner logs outside the ephemeral host for diagnosis. Monitor
queue time, job duration, capacity, network access and runner updates. Consult
the [self-hosted runner reference](https://docs.github.com/en/actions/reference/runners/self-hosted-runners)
for current support and operations details.

## CI artifact flow

Model CI as source checkout, build, test, report and publish. Keep outputs
between jobs explicit. Use caches only to reuse regenerable dependencies or
intermediate data; use workflow artifacts to preserve build outputs and reports.
Do not make correctness depend on a cache hit. Keep secrets and privileged
credentials out of cache contents.

Preserve the link between source revision, workflow run and produced artifact.
Where the threat model requires stronger provenance, evaluate GitHub artifact
attestations and an associated software bill of materials (SBOM). See [workflow
artifacts](https://docs.github.com/en/actions/concepts/workflows-and-actions/workflow-artifacts).

## Deployment controls

Separate artifact creation from deployment where that improves review and
traceability. Use environments for deployment-specific variables, secrets and
protection rules; verify the actual repository plan and environment policy
supports the required controls. Prefer OpenID Connect federation to long-lived
cloud credentials when the provider and trust policy support it. Constrain
federated subject claims to the intended repository, branch, tag or environment.

Choose deployment and release strategies based on rollback capability, health
signals and acceptable exposure. A workflow's successful job is not evidence
that the live service is healthy; verify the deployed revision and relevant
health check separately.
