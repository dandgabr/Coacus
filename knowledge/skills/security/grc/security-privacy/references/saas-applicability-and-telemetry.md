# SaaS Applicability and Telemetry

Use for a product privacy review. This original Coacus procedure separates applicable law, provider behavior and observations of an implementation.

## Establish applicability

Record jurisdiction, audience, controller/operator role, processing purposes, data categories, proposed legal bases, providers, retention and unresolved facts. The label SaaS alone establishes none of these. Missing facts limit the conclusion; do not invent corporate identifiers, mandatory banners or universal footer requirements.

Classify cookies and other storage by actual purpose. Strictly necessary operations and optional analytics can require different treatment. Do not use consent indiscriminately as a legal basis. Route operational capture, withdrawal and erasure to [consent automation](../../consent-dsr-automation/SKILL.md), and consumer contracting, supplier identification and cancellation to [GRC compliance](../../security-grc-compliance/SKILL.md).

## Inspect telemetry by product and route

Record provider/product, region, documentation date, consent mode, collected fields, advertising integrations, retention and collection route. Separate browser requests, first-party proxy logs, server forwarding and downstream processing. A vendor statement about one product does not cover every integration.

For example, Google's basic and advanced consent modes have different collection behavior: advanced mode can send cookieless measurements while storage consent is denied. A denied flag, an absent cookie or a banner screenshot does not prove that no data was transmitted. Compare observed payloads and storage with the approved purpose policy. A cookieless request is neither automatically permitted nor automatically prohibited.

Do not prescribe a legacy IP-anonymization toggle without checking the actual analytics product. Provider-side IP handling does not establish that a first-party proxy, access log or advertising integration avoids processing IP addresses. Network samples also cannot prove all server-side processing.

## Sources and limits

Reviewed 2026-10-27; resolve current legal text and provider documentation before advising a specific deployment.

- [ANPD cookie guidance](https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/processo-guia-orientativo-cookies-e-protecao-de-dados-pessoais.pdf): necessary cookies, purpose and consent applicability.
- [Google consent mode](https://developers.google.com/tag-platform/security/concepts/consent-mode): basic versus advanced collection behavior.
- [Analytics regional handling](https://support.google.com/analytics/answer/12017362?hl=en): product-specific regional behavior, not certification of the surrounding system.
- [Updated LGPD text](https://www2.camara.leg.br/legin/fed/lei/2018/lei-13709-14-agosto-2018-787077-normaatualizada-pl.html): contextual rights and retention exceptions.

Consumer-law details require readable authoritative text for the relevant jurisdiction. Do not derive a detailed rule from an inaccessible source or a search excerpt alone.
