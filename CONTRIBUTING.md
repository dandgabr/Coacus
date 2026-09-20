# Contributing to Coacus

Coacus is a generated-artifact repository. Contributions add canonical sources,
regenerate the derived artifacts, and pass the same gate CI runs. This document
is the contract; the rationale lives in [`docs/standards/`](docs/standards/).

## Before you start

- Read [`README.md`](README.md) for what the framework is.
- Read [`docs/architecture.md`](docs/architecture.md) for the layers and the
  artifact lifecycle.
- Read the standards in `docs/standards/` before changing structure. The engine is closed for
  modification; most contributions are new data files.

## The artifact lifecycle

Every artifact moves through five stages:

```text
create (templates/authoring) → validate → register (generate) → discover (single scan) → activate (SessionStart)
```

1. **Create** from the matching template in `templates/authoring/`.
2. **Validate** the canonical source contract.
3. **Register** with `python3 scripts/coacus.py generate`.
4. **Discover** through the generated `.agents/` manifests.
5. **Activate** when a harness injects the rendered bootstrap.

Never hand-edit generated output. That includes `catalog/`, `.agents/`,
`harnesses/<h>/bootstrap/`, and every `dist/` directory. Change the source and
regenerate; `check` is designed to catch exactly this.

The exact steps per artifact type are in [`docs/extending.md`](docs/extending.md).

## Local validation

Run the full gate before opening a pull request:

```bash
python3 scripts/coacus.py generate     # produce the artifacts your change implies
python3 scripts/coacus.py validate     # source + artifact contracts
python3 scripts/coacus.py check        # must report no drift
python3 -m unittest discover -s tests  # 245 deterministic tests
```

`generate` refuses to write while source validation fails. Fix `[error]` lines
first; `[warn]` lines are non-blocking (non-English markers, oversized
descriptions) but should be addressed when they concern your change.

CI runs `validate` → `check` → `completeness` → tests and **never** `generate`: regeneration in CI
would rewrite the files under comparison and mask drift. If you see a drift
failure, regenerate locally and commit.

## Repository rules

These are machine-checked by the validators and the hygiene scan:

1. **One source per artifact.** Skills: `SKILL.md`. Agents: `agent.source.md`.
   MCPs: `MCP.md`. Everything generated is generated.
2. **English only** ([english-only](docs/standards/english-only.md)). Comments,
   docs, frontmatter, commit messages. PT-BR source material is translated, not
   copied.
3. **No secrets** ([secrets-portability](docs/standards/secrets-portability.md)).
   Reference secrets only as `{env:VAR}`. Secret-shaped literals fail the build
   and the gitleaks scan.
4. **No machine-specific absolute paths** ([secrets-portability](docs/standards/secrets-portability.md)).
   Use repository-relative paths. `/home/...`, `/Users/...`, `C:\...` and similar
   are rejected.
5. **Agnostic skill bodies** ([skill-authoring](docs/standards/skill-authoring.md)).
   Canonical content names actions, never harness tool names. Tool mappings go
   in `references/<harness>-tools.md` and in `harness.json`.
6. **Docstring and JSDoc conventions.** Python modules, public functions, classes
   and public methods carry a docstring ([PEP 257](https://peps.python.org/pep-0257/));
   these are the single source of the generated `docs/reference/python-api.md`, so
   a missing docstring is also a hole in the reference. Generated JavaScript
   (`harnesses/opencode/bootstrap/*.js`) documents exported symbols with
   [JSDoc](https://jsdoc.app/) (`@param`/`@returns`). `tests/test_docstrings.py`
   enforces the Python side in CI. Verbatim third-party assets under
   `methodology/` are exempt — they are byte-identical upstream copies recorded in
   `sources.lock.json` and must not be edited.
6. **kebab-case names; third-person, trigger-oriented descriptions.**
7. **Omit `model` in canonical agent sources** ([agent-manifests](docs/standards/agent-manifests.md)).
8. **Governed parallelism** ([orchestration-governance](docs/standards/orchestration-governance.md)).
   The concurrency cap is 5, orchestrator included; hand off with TOON payloads.

## Commit style

Use [Conventional Commits](https://www.conventionalcommits.org/). The repository
history uses `feat:`, `fix:` and `ci:` with an imperative, lowercase summary.
Examples from the log:

```text
feat: import, translate and organize the full corpus (F6) (#6)
fix: harden imported code against CodeQL/Bandit findings (#7)
ci: add Bandit security scan workflow (#1)
```

Rules:

- One logical change per commit; keep generated diffs in the same commit as the
  source change that produced them.
- Reference the phase (F1–F8) in the body or summary when relevant.
- Break behavior changes and scope them with `!` and a `BREAKING CHANGE:` footer.

## Pull request flow

1. Branch from `main`.
2. Make the change; run the full local gate.
3. Stage only intended files. Commit `generate` output together with its sources.
4. Open a pull request against `main`.
5. CI runs the `ci` job (validate → check → completeness → tests) and the `secrets` job
   (pinned gitleaks in directory mode, scanning the checked-out state). A `main`
   ruleset makes **both** checks required.
6. Review the generated diff in the PR. It is the visible proof that source and
   output agree.

Because the repository squashes on merge, the gitleaks scan checks the state
that ships, not every intermediate commit. Do not rewrite or force-push a branch
under review.

## Adding an ingestion format

Handlers register themselves; the dispatcher never changes
([knowledge-ingestion](docs/standards/knowledge-ingestion.md)). Add a file under
`verticals/architecture_si/pipelines/ingest/handlers/` decorated with
`@register_converter("<ext>")`, import no sibling handler, and add a test under
`tests/test_vertical.py`. See [`docs/extending.md`](docs/extending.md).

## Reporting and security

- Bugs and feature requests go through repository issues.
- Do not open a public issue for a suspected secret or vulnerability. Report it
  privately to the maintainer, then rotate the credential.

## License

Contributions are accepted under the repository's [LICENSE](LICENSE).
