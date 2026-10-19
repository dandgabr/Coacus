# Workflow Authoring and Reuse

Use this reference when creating or changing workflow syntax, actions or reusable
workflow interfaces. Confirm current syntax in [GitHub's workflow syntax
reference](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax).

## Specify the workflow contract

Before writing YAML, record the event, eligible branches and paths, required
jobs, dependency order, outputs, permissions, concurrency behavior and expected
failure handling. Check whether the workflow runs for forks, automated update
branches, tags, schedules or manual dispatch; each event can have different
trust and token properties.

Use expressions and contexts only where needed. Validate values that originate
from event payloads before interpolating them into shell commands, action
inputs, paths or generated configuration. Prefer environment variables and
quoted shell arguments for data; do not construct executable shell source from
untrusted strings.

## Permissions and job structure

- Declare the minimum `GITHUB_TOKEN` permissions required for each job. Make
  read-only behavior explicit where supported; grant write permissions only to
  the job that needs them.
- Use `needs` to express dependencies and reserve parallel jobs for independent
  work. Use a matrix only when each dimension represents a meaningful test or
  build variation.
- Treat `if` conditions and branch/path filters as policy. Check that they do
  not skip required security checks or deployment gates.
- Give concurrency groups a scope that avoids cancelling unrelated deployments
  or reusable workflow callers.

## Reusable workflows and actions

Use a reusable workflow for a job-level process that needs a typed input,
outputs and controlled secret boundary. Use a composite action for a coherent
step sequence. Keep the caller's repository context, token permissions,
runner access, environment and artifact ownership in view; do not assume a
called workflow elevates permissions or inherits caller state implicitly.

Pin external actions and reusable workflows to a verified full commit SHA when
the repository's policy requires immutable references. Record the upstream
repository and reviewed release or source. Where a tag is retained for
readability, use policy and automation to detect movement or updates; never
present an unverified tag as a security pin.

## Validate the authored workflow

Inspect the parsed workflow, expressions and action interfaces. Check that all
referenced workflows are accessible to callers, inputs and outputs match, and
secrets are explicitly passed only where necessary. Run available local static
checks and the relevant repository tests; static validation does not prove
GitHub-side permissions, event payloads or deployment effects.
