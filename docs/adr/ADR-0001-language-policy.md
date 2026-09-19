# ADR-0001: Repository Language Is English

* Status: accepted (2026-09-18, user decision)
* Deciders: repository owner
* Scope: entire repository, permanent policy

## Context

Coacus unifies sources containing PT-BR content (`agente-arquitetura-si`, parts
of `skills`). International standardization requires a single language.

## Decision

All repository artifacts are written in English: docs, ADRs, SKILL.md frontmatter
and bodies, manifests, templates, code comments, commit messages, CI labels.
Legacy PT-BR content is translated to English during import (F6), never copied
verbatim. Chat interaction with the owner remains PT-BR (standing preference).

## Consequences

All PT-BR translations are delegated to the `linguistic-specialist` agent under
orchestrator governance — never done inline by the implementing agent.
Future guard: validators may flag non-English frontmatter/descriptions.
