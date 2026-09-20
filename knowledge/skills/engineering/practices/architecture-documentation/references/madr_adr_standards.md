# MADR Standard (Markdown Architectural Decision Records)

Formal structure for recording architectural decisions.

## Standard Format

```markdown
# ADR [Número]: [Título da Decisão]

* **Status**: [PROPOSED | ACCEPTED | REJECTED | DEPRECATED | SUPERSEDED]
* **Decisores**: [Nomes / Papéis dos Envolvidos]
* **Data**: [AAAA-MM-DD]

## Contexto e Declaração do Problema
[Descrição do cenário técnico ou de negócio e a necessidade da decisão]

## Decision Drivers (Forças Motivadoras)
* [Driver 1: ex. Latência p99 < 50ms]
* [Driver 2: ex. Conformidade estrita com LGPD]

## Opções Consideradas
* [Opção 1: Nome da Alternativa A]
* [Opção 2: Nome da Alternativa B]
* [Opção 3: Nome da Alternativa C]

## Decisão Tomada
[Opção escolhida e justificativa técnica central]

### Consequências Positivas
* [Benefício 1]
* [Benefício 2]

### Consequências Negativas / Trade-offs
* [Impacto negativo 1 ou débito operacional assumido]
* [Trade-off mitigado]
```
