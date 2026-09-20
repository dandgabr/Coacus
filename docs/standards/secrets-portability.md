# Secrets and Portability

**Status:** normative
**Scope:** every canonical source, template, manifest and documentation file.
Transversal across all three artifact layers.

## Rule

### Secrets

Canonical sources reference secrets ONLY as a `{env:VAR}` placeholder (or
`${VAR}`), resolved at activation time and never stored. A plaintext
secret-shaped literal MUST NOT appear anywhere in the repository.

Placeholder forms sanctioned by the contract:

```text
{env:VAR}       ${VAR}       %VAR%       REDACTED
```

A real value is never written, never committed, and never emitted into a
generated artifact. MCP `env_vars` carries names only.

### Portability

No machine-specific absolute path may appear in a tracked file. Machine-specific
means a concrete user's home (`/home/<user>`, `/Users/<user>`, `/root`), the
author's conversion workspace under `/tmp/opencode`, a Windows user profile
(`C:\Users\<user>`), or a `file://` URL. Use repository-relative paths.

The rules apply to the prose and configuration the framework ships. Fenced code
blocks are exempt: illustrative snippets may legitimately show example paths and
token-shaped values.

## Rationale

The source repositories already violated both rules once — a template carried an
absolute path from another machine, and secret material is easy to paste into a
manifest. Convention alone does not enforce either; a validator that fails the
build before merge does.

## Enforcement

- `engine/validators/hygiene.py` scans `knowledge/`, `methodology/`, `verticals/`,
  `harnesses/` and `templates/` for absolute paths and secret patterns
  (`aws-access-key`, `github-token`, `slack-token`, `private-key`,
  `credential-assignment`) and reports them as errors during
  `python3 scripts/coacus.py validate`. The `{workspace}` token is allowed in
  import data.
- `engine/validators/evals.py` applies the same path and secret patterns to every
  scenario string.
- `engine/toon.py` rejects secret-like literals in TOON payload fields.
- `.gitleaks.toml` extends the default ruleset with narrow allowlists; the
  `secrets` job in `.github/workflows/ci.yml` runs a pinned, checksum-verified
  gitleaks scan in directory mode against the checked-out state.
- `tests/test_validators.py` covers the hygiene patterns.
