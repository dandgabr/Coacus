# Published Artifact Verification

Use when releasing a reviewed interface or diagnosing why a deployed site behaves differently from the local candidate. Build completion and the content actually served are distinct observations.

## Identify the approved subject

Keep authored sources, review metadata, generated outputs and the deployable package distinct. Bind review to the product content and relevant runtime snapshot. Administrative promotion should not silently alter semantic content. Regenerate distribution outputs from the reviewed sources and verify their equivalence.

Record which changes invalidate a review and which evidence can be reused with a stated reason. A previous plan approval, a different source digest or sampled inspection cannot stand in for review of another revision. Preserve unknown technical measurements even when the appropriate authority authorizes release with limitations.

## Follow the delivery route already configured

Confirm the destination, source revision, build mode and relevant domain/path configuration. Preserve unrelated environments and pre-existing work. Define a rollback scoped to the release before taking a risky publication action; do not replace the provider or domain to make a check pass.

Authorization to publish persists for that destination and scope. Finish the concrete preparation and required checks without repeatedly asking the same permission. A materially different destination, destructive action or scope expansion needs separate authority. PR creation alone does not authorize merge or production deployment.

## Verify the dependency graph

Inspect the served document and the stylesheets, static/dynamic modules, registries and locale catalogs it references. A new document can import an old module under a fixed cache key. Use an appropriate revision strategy across the graph: content-addressed assets, a generated manifest or consistently propagated versions can all work.

Compare the intended revision through bytes, digests or a trustworthy manifest, and replay the important user flow at the deployed origin. An HTTP success response proves reachability, not freshness. A version query on the document alone does not identify all imported assets.

## Report completion and limits

Record the published revision, deploy result, verified assets, exercised behaviors, observations for environments that must remain unchanged, and rollback state. Distinguish an unavailable verifier from a product failure. Recover an automation session through the environment's approved lifecycle, record the interruption and resume valid evidence; never silently attach to another user's browser/profile or change the deployment target.

Provider-specific commands, browser binaries, ports, profiles and authentication belong in the environment adapter or platform reference. The verification contract remains the same across tools.
