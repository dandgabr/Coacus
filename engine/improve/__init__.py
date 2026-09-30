"""Self-improvement subsystem (F10).

An asynchronous, opt-in, fail-open loop that reads a finished session, compresses
it into typed candidates, routes each candidate to improve-vs-create against the
existing corpus, verifies it, and stages a PROPOSAL. It never applies: promotion
is a human PR (decision D7).

Design invariants:

- The subsystem is inert unless invoked explicitly by ``scripts/coacus_improve.py``;
  it is never imported by ``generate``/``check``.
- Episodic sources are pluggable (``sources``); ``transcript`` is the portable
  default and ``ai-memory`` is an OPTIONAL enricher. Absence of any external
  source degrades to a no-op, never to a build failure (P2).
- The durable audit trail lives in the repository, not in an external store.
"""
