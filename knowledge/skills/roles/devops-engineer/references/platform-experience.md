# Platform Experience Examples

These are conditional operational examples, not universal provider choices. Version pins inherited from the source are not verified as current by this update; resolve the selected platform documentation before use. Authorization, secrets and release verification follow the parent skill and repository standards.

## 🛠️ 9. Platform Engineering & Developer Experience (DX)

The transition from traditional DevOps to **Platform Engineering** replaces the infrastructure ticket queue (*ticket-ops*) with the delivery of a **Platform as a Product**:

```text
[ Product Developers ]
             │
             ▼  (Self-Service / APIs / Golden Paths)
┌─────────────────────────────────────────────────────────┐
│        INTERNAL DEVELOPER PLATFORM (IDP)                │
│  ├── Backstage (Software Catalog & Templates)           │
│  ├── GitOps Engine (ArgoCD / Flux)                      │
│  ├── IaC Modules (Terraform Registry / Crossplane)      │
│  └── Telemetry Stack (OpenTelemetry / Grafana / O11y)   │
└─────────────────────────────────────────────────────────┘
             │
             ▼  (Secure Declarative Provisioning)
[ Multi-Cloud & Bare-Metal Infrastructure ]
```

### 🛣️ Golden Path Principles
1. **Paved Roads**: Offer opinionated standards where security, observability, and CI/CD are already integrated by default.
2. **Frictionless Autonomy**: Developers must be able to provision databases, messaging topics, and services without waiting for manual approvals for test and validation environments.
3. **DORA Metrics as a Compass**:
   - **Deployment Frequency**: Frequency of successful deployments to production.
   - **Lead Time for Changes**: Time between the code commit and running in production.
   - **Change Failure Rate**: Percentage of deployments that cause production incidents.
   - **Failed Deployment Recovery Time (MTTR)**: Average time to restore the service in case of degradation.

---
