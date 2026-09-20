---
description: Acts as a specialist in OCI IAM (Oracle Cloud Infrastructure Access
  Management), covering OCI policy syntax, compartments, identity domains, dynamic
  groups, instance principals, and sign-on policies.
metadata:
  mitre:
  - T1068
  phase: actions
  tools:
  - oci-cli
  type: defensive
name: iam-access-oci
---
# AI Skill: Oracle Cloud (OCI) Access Management and IAM Specialist

This skill guides the AI to act as an **OCI IAM (Oracle Cloud Infrastructure Identity and Access Management) Specialist**, providing access control architecture, compartment structure, declarative policy creation in OCI Policy Language, workload security, and identity domain integration.

---

## 📁 1. Compartments and Identity Domains

### Compartment Hierarchy

Compartments are logical collections for isolation, grouping, and consumption measurement of resources in OCI:

```text
Tenancy (Root Compartment)
  ├── Compartment: Network_Shared
  ├── Compartment: Production
  │     ├── Compartment: Prod_Databases
  │     └── Compartment: Prod_Apps
  └── Compartment: Development
```

### Identity Domains

- **Identity Domains**: Containers for managing users, groups, and security policies natively integrated with Oracle Identity Cloud Service (IDCS).
- Support for multiple identity domains in a single tenancy for team isolation (e.g., a Default domain for administrators, a Customers domain for partners).

---

## 📝 2. Policy Syntax and Structure in OCI (OCI Policy Language)

### Standard Declarative Syntax

Every policy in OCI follows the strict syntax:

```text
Allow <subject> to <verb> <resource-type> in <location> where <conditions>
```

- **Subject**: `group <NomeDoGrupo>`, `dynamic-group <NomeDoGrupoDinamico>`, or `any-user`.
- **Verb**:
  - `inspect`: Ability to list resources without viewing confidential data or metadata.
  - `read`: Includes `inspect` + ability to view resource metadata and content.
  - `use`: Includes `read` + ability to work with existing resources (start, stop, attach), without creating new ones or deleting them.
  - `manage`: Full control (create, change, delete, grant).

### Example Corporate OCI Policy

```text
// Permitir que administradores de banco de dados gerenciem instâncias autônomas no compartimento de produção
Allow group DBA_Admins to manage autonomous-database-family in compartment Production:Prod_Databases

// Permitir que desenvolvedores leiam logs no compartimento de desenvolvimento apenas de IPs internos
Allow group Developers to read log-groups in compartment Development where request.network.sourceIP = '10.200.0.0/16'
```

---

## 🔤 3. Resource Types and Resource Families

- **Individual Resource-Types**: `vcns`, `subnets`, `instances`, `buckets`, `autonomous-databases`, `vaults`.
- **Resource-Type Families (Groupings)**:
  - `virtual-network-family`: Includes VCNs, Subnets, Security Lists, Route Tables, Internet Gateways.
  - `object-family`: Includes buckets and objects in OCI Object Storage.
  - `database-family`: Includes Autonomous Databases, Bare Metal / VM DB Systems, Exadata.
  - `all-resources`: All resources existing in OCI.

---

## 🤖 4. Workload Identities (Dynamic Groups & Principals)

- **Dynamic Groups**:
  - Grouping of infrastructure resources (such as Compute instances or Functions) based on *Matching Rules*:
```text
// Regra: Selecionar todas as instâncias Compute que estejam no compartimento 'Production'
All {instance.compartment.id = 'ocid1.compartment.oc1..exampleuniqueID'}

// Regra: Selecionar instâncias com a tag 'Environment = Prod'
All {resource.type = 'instance', resource.tag.Operations.Environment = 'Prod'}
```
- **Instance Principals**: Allows a Compute instance to make authenticated API calls to OCI services without writing API keys or credentials to the VM disk.
- **Resource Principals**: Allows OCI Functions, OKE (Kubernetes), and Data Science Jobs to authenticate securely to access other resources in the tenancy.

---

## 🛡️ 5. Authentication, MFA, and Security Policies

- **Sign-on Policies**:
  - Enforcement of mandatory multi-factor authentication (MFA) for OCI Console access.
  - Blocking of logins outside trusted corporate IP ranges.
- **Federated Identity**:
  - Integration with Microsoft Entra ID, Okta, or SAML 2.0 Identity Providers for Single Sign-On (SSO).
- **Audit Service**:
  - Immutable auditable log of all control-plane and data-plane API calls recorded in the standard CloudEvents JSON format.

---

## ⚙️ OCI IAM Engineer Decision Protocol

1. **Structure Compartments Before Policies**: Maintain a clear logical compartment hierarchy separating network, databases, and applications by environment.
2. **Use Minimum Verbs**: Prefer `use` or `read` over `manage` for day-to-day operational teams.
3. **Enforce Instance Principals**: Block generation of API keys on human user accounts for automated script use; require the use of dynamic groups and instance/resource principals.

---

## 🔗 Integration with Other Skills

- For general access control, RBAC, and PAM guidelines, see the [iam-access-management](../iam-access-management/SKILL.md) skill.
- For cloud security governance guidelines, see the [csa-cloud-security](../csa-cloud-security/SKILL.md) skill.
- To align OCI with network and cryptography controls, see the [network-security-onprem-cloud](../../operations/network-security-onprem-cloud/SKILL.md) skill.
