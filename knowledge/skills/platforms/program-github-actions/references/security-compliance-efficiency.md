# Security, Compliance and Efficiency

Use this reference when reviewing the workflow threat model, auditability or
operating cost. Resolve current platform details from official GitHub
documentation during the task.

## Untrusted events and input

Treat pull request code, issue text, branch names, commit messages, artifacts
and dispatch inputs as untrusted. Do not check out and execute fork-controlled
code in a privileged workflow, especially one triggered by
`pull_request_target`. Separate trusted metadata handling from untrusted builds;
withhold secrets and write-capable tokens from untrusted execution. Sanitize
values before they reach expressions, shell commands, file paths or generated
workflow configuration.

## Token, action and runner controls

- Grant the `GITHUB_TOKEN` only the permissions required by the specific job.
- Review third-party action source, ownership, maintenance and requested
  permissions. Pin to a full commit SHA when immutable references are required
  by the threat model or repository policy, and automate review of updates.
- Store credentials in the narrowest supported scope. Prefer short-lived
  identity federation over static credentials where available.
- Restrict self-hosted runner groups to approved repositories and workflows;
  do not treat an environment approval as isolation from code already running
  on a self-hosted host.

GitHub documents full-length commit SHA pinning and workflow threat controls in
its [secure-use reference](https://docs.github.com/en/actions/reference/security/secure-use).

## Traceability and compliance

Make the source revision, review decision, workflow run, artifact and deployment
environment traceable across the delivery path. Retain only the logs, artifacts
and attestations required by operational and regulatory needs, using their
actual configured retention. CODEOWNERS and required reviews can support
separation of duties, but verify that branch rules require the intended checks
and reviewers.

## Performance and cost

Measure queue time, runtime, cache effectiveness, artifact transfer and runner
utilization before optimizing. Reduce redundant work through path-aware triggers,
appropriate dependency caching, bounded matrices and useful concurrency
controls. Preserve required checks and security coverage; a lower bill or faster
workflow is not an improvement if it removes necessary verification. Resolve
current quotas, pricing and retention from official documentation instead of
copying fixed limits into a long-lived skill.
