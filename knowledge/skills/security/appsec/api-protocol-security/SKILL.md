---
name: api-protocol-security
description: Acts as a specialist in API and protocol security for REST, GraphQL, gRPC and WebSocket surfaces, covering authorization at the object level, query cost and depth limits, batching abuse, reflection hardening, message-size and rate limits, and mTLS for service-to-service calls.
metadata:
  type: defensive
  phase: weaponize
---

# API and Protocol Security (REST, GraphQL, gRPC, WebSocket)

This skill guides the AI to harden modern API protocols. The OWASP API Security Top 10 2023 (still the current edition) names the baseline risks; this skill adds the protocol-specific mechanics that generic API guidance omits.

---

## 🧭 1. Protocol-Specific Risks and Controls

### 1.1 REST
- Enforce object-level authorization on every read and write (API1 BOLA, API5 BFLA), not just at the route level.
- Use schema validation, restrict mass assignment (API3 BOPLA), paginate deterministically and cap payload sizes.
- Never expose internal identifiers or fields by default.

### 1.2 GraphQL
- Disable introspection and the in-browser IDE in production where not needed.
- Enforce **query depth, complexity and cost limits**; a deeply nested or aliased query is a denial-of-service primitive.
- **Batching** (multiple operations in one request) bypasses naive rate limiting and enables brute force; count operations per request, not requests.
- Authorize at the edge **and** the node; a check that runs only at the top level leaves nested fields exposed.

### 1.3 gRPC
- Mandatory TLS with mTLS for internal calls; validate the peer identity, not just the certificate chain.
- Authorize per method and constrain message sizes; disable server reflection in production.
- Use schema validation on every message; do not trust the generated stub as a security boundary.

### 1.4 WebSocket
- Validate the `Origin` on the upgrade, authenticate before accepting the socket, and authorize every message, not just the connection.
- Enforce message-size and rate limits; a WebSocket is a long-lived authenticated channel and inherits all the risks of one.

---

## 🛡️ 2. Cross-Cutting Controls

1. **Inventory**: an unmanaged or shadow API is an unpatched API (API9 Improper Inventory Management).
2. **Rate limiting and quotas** per identity, not per IP alone.
3. **Authentication and token hygiene**: short-lived tokens, audience restriction, sender-constrained tokens where possible.
4. **Error handling**: uniform errors that do not leak stack traces, versions or internal identifiers.
5. **Logging and alerting** on authorization failures and abnormal consumption.

---

## 🔗 3. Integration with Other Skills

- For injection and deserialization mechanics, see the [web-injection-classes](../web-injection-classes/SKILL.md) skill.
- For the API pentest checklist, see the existing [pentester-owasp-api-security-2023](../pentester-owasp-api-security-2023/SKILL.md) skill.
- For authentication protocol details, see the [auth-protocols-mfa](../../operations/auth-protocols-mfa/SKILL.md) skill.
- For gRPC and GraphQL framework conventions, see the [framework-graphql](../../../frameworks/framework-graphql/SKILL.md) and [framework-grpc](../../../frameworks/framework-grpc/SKILL.md) skills.
