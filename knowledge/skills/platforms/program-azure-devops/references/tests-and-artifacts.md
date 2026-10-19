# Azure Test Plans and Artifacts

Read this reference when designing test management, package distribution, or
artifact movement between pipeline stages.

## Connect test intent to test evidence

- Identify which checks are unit, integration, system, acceptance, exploratory,
  or manual tests. Choose the Azure Test Plans features only for the test
  management needs they serve.
- Organize planned manual testing with test plans, suites, and cases where that
  model fits. Record outcomes and defects and link them to the requirements or
  work items they cover.
- Treat automated execution as a pipeline concern that publishes test results;
  confirm how the project associates those results with test cases before
  claiming that a test plan itself executes the automation.
- For audit or release decisions, identify the test run, environment,
  configuration, result, and source revision. Keep exploratory observations
  distinct from repeatable automated evidence.

## Govern packages and artifacts

- Distinguish package feeds from pipeline-run artifacts. A package feed is for
  versioned package consumption and publication; a pipeline artifact is a run
  output passed to later jobs or stages. Verify that the artifact type is
  supported by the target service model and pipeline type before designing
  cross-run or release consumption.
- Choose project or organization feed scope according to consumer boundaries.
  Separate reader, publisher, and owner responsibilities; give pipeline
  identities only the feed role needed by the job.
- Review upstream sources and who may change them. Upstream sources can cache
  package copies, so use them as an explicit dependency intake policy rather
  than an unreviewed network shortcut.
- Use feed views to expose selected package versions to consumers when that
  matches the promotion process. Verify effective access to both feeds and
  views before claiming a package is private.
- Promote or deploy the exact package/artifact that passed the required checks.
  Record its version or digest and source run; do not rebuild silently during a
  downstream deployment.

## Current references

- [Azure Test Plans documentation](https://learn.microsoft.com/en-us/azure/devops/test/?view=azure-devops)
- [Set up automated testing with Azure Test Plans](https://learn.microsoft.com/en-us/azure/devops/test/automated-testing-overview?view=azure-devops)
- [Azure Artifacts key concepts](https://learn.microsoft.com/en-us/azure/devops/artifacts/artifacts-key-concepts?view=azure-devops)
- [Azure Artifacts feed permissions](https://learn.microsoft.com/en-us/azure/devops/artifacts/feeds/feed-permissions?view=azure-devops)
- [Upstream sources](https://learn.microsoft.com/en-us/azure/devops/artifacts/concepts/upstream-sources?view=azure-devops)
- [Pipeline artifacts](https://learn.microsoft.com/en-us/azure/devops/pipelines/artifacts/pipeline-artifacts?view=azure-devops)
