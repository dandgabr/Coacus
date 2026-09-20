---
name: framework-microprofile-jakarta
description: "Provides corporate patterns and conventions for Java servers and microservices based on Eclipse MicroProfile 6.x+ and Jakarta EE 10/11+ (JAX-RS, CDI, JSON-P/B, Config, Fault Tolerance, Health/Metrics)."
---

# MicroProfile & Jakarta EE Server Engineering

This skill guides the construction of microservices and enterprise applications in compliance with the open **Eclipse MicroProfile 6.x+** and **Jakarta EE 10/11+** specifications (Payara, Open Liberty, WildFly, Helidon).

---

## 🧭 1. Pillars of the MicroProfile Specification
1. **JAX-RS (Jakarta RESTful Web Services)**: Definition of HTTP endpoints with `@Path`, `@GET`, `@POST`, `@Produces(MediaType.APPLICATION_JSON)` annotations.
2. **CDI (Contexts and Dependency Injection)**: Life-cycle management with strict scopes (`@ApplicationScoped`, `@RequestScoped`).
3. **MicroProfile Config**: Decoupled parameterization via `microprofile-config.properties` and environment variables with `@ConfigProperty`.
4. **MicroProfile Fault Tolerance**: Native resilience with `@Timeout`, `@Retry`, `@CircuitBreaker`, `@Bulkhead`, and `@Fallback`.
5. **Health & Metrics**: Standardized liveness/readiness endpoints (`/health/live`, `/health/ready`) and open telemetry with MicroProfile Telemetry / Metrics.

---

## 🏢 2. Architectural Isolation Rules
- Keep domain rules pure and decoupled from JAX-RS transport annotations.
- Use Bean Validation (`@Valid`) at the application boundary for early rejection of invalid payloads.
- In projects that use the Boundary-Control-Entity (BCE) architecture, the boundary implements the JAX-RS resources and injects them into the business controls.
