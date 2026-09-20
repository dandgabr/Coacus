# Example: ADR 0001 - Adopting Vault for Centralized Secrets Management

* **Status**: ACCEPTED
* **Decisors**: Security Architect, Architecture Documentarian
* **Date**: 2026-08-24

## Context and Problem Statement
The repository contains several services that consume database credentials, vendor API keys, and mTLS certificates. Today, secrets are passed through static environment variables, which makes access auditing harder and prevents dynamic rotation without restarting the containers.

## Decision Drivers
- Dynamic, automatic credential rotation with no downtime.
- Centralized audit trail for every secret read.
- Native integration with Kubernetes and CI/CD pipelines.

## Options Considered
1. **Option 1**: HashiCorp Vault.
2. **Option 2**: AWS Secrets Manager.
3. **Option 3**: Native Kubernetes Secrets with Sealed Secrets.

## Decision Made
We chose **Option 1: HashiCorp Vault**, because it supports multiple cloud providers agnostically and can generate temporary credentials on demand (*Just-In-Time Credentials*).

### Positive Consequences
- Temporary credentials eliminate the risk of a permanent leak.
- Structured audit logs for every secret accessed.

### Negative Consequences
- The Vault cluster must be operated and kept highly available.
