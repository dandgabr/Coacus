# Superpowers consultative review

On 2026-10-31, the official GitHub [latest release API](https://api.github.com/repos/obra/superpowers/releases/latest) identified `v7.0.1` as the latest non-prerelease. Its [annotated tag reference](https://api.github.com/repos/obra/superpowers/git/ref/tags/v7.0.1) resolves via [tag object `cfd50a286baea35041505ed068c878d389ca9f7f`](https://api.github.com/repos/obra/superpowers/git/tags/cfd50a286baea35041505ed068c878d389ca9f7f) to commit `2ce8aa15d05bd57213e6f746f953aafb7ded7a8b`. The API reports the tag as unsigned; this verifies the published reference, not a cryptographic signature.

This revision is a review reference, not the source commit of historical imports; `sources.lock.json` retains their actual provenance. The separate [Coacus repository action PR #127](https://github.com/dandgabr/Coacus/pull/127) security review verified the upstream tag, but did not fully review the bundled source. PR #127 is a Coacus pull request, not an upstream Superpowers pull request.

Candidate decisions are partial. Existing integrations have not been exhaustively reconciled with this revision. Do not import or apply unreviewed upstream material; review specific changes against local workflows before adopting them.
