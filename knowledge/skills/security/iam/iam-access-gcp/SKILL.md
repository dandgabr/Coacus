---
description: Acts as a specialist in GCP IAM (Google Cloud Access Management), covering
  resource hierarchy, predefined/custom roles, service account impersonation,
  Workload Identity Federation, VPC Service Controls, and IAM Recommender.
metadata:
  mitre:
  - T1068
  phase: actions
  tools:
  - gcloud-cli
  - cartography
  type: defensive
name: iam-access-gcp
---
# AI Skill: Google Cloud (GCP) Access Management and IAM Specialist

This skill guides the AI to act as a **GCP IAM (Identity and Access Management) Specialist**, providing access control architecture, resource hierarchy structuring, service account management, security perimeters (VPC Service Controls), and least-privilege automation on **Google Cloud Platform (GCP)**.

---

## 🌳 1. Resource Hierarchy and IAM Policy Inheritance

### GCP Organizational Structure

Granting roles at higher nodes is inherited by all child resources without exception (there is no inheritance denial):

```text
Organization (Empresa Domain)
  ├── Folder: Producao
  │     ├── Project: prj-app-prod-01
  │     │     ├── GCS Bucket: bkt-dados-prod
  │     │     └── Compute Engine Instance: vm-app-01
  │     └── Project: prj-db-prod-01
  └── Folder: Desenvolvimento
        └── Project: prj-app-dev-01
```

### Accepted Members and Principals

- **Google Account (individual user email)**.
- **Google Group (corporate email group)** - *Recommended form of assignment for people*.
- **Service Account (application identity)**.
- **Google Workspace / Cloud Identity Domain**.
- **Special Identifiers**: `allAuthenticatedUsers` and `allUsers` (*EXTREMELY DANGEROUS*, they grant public/global access).

---

## 🎭 2. Role Types and the Least Privilege Principle

- **Basic / Primitive Roles (obsolete in production)**:
  - `roles/owner`: Full control over resources, billing, and IAM granting.
  - `roles/editor`: Permission to create, modify, and delete most resources.
  - `roles/viewer`: Read-only permission.
  - *Golden Rule*: Using primitive roles in corporate environments is forbidden because of their excessive permissiveness.
- **Predefined Roles**:
  - Google-maintained roles focused on specific functions (e.g., `roles/storage.objectViewer`, `roles/bigquery.dataEditor`, `roles/compute.instanceAdmin.v1`).
- **Custom Roles**:
  - Creation of granular roles specifying an exact list of API-level permissions (e.g., `storage.objects.get`, `bigquery.tables.getData`).

---

## 🔑 3. Service Accounts and Keyless Authentication

### Protection Against the Use of JSON Keys

- Service account keys in a `.json` file represent the main exfiltration vector in GCP.
- **Enforce Organizational Policy**:
  - The `iam.disableServiceAccountKeyCreation` constraint active at the organization level to prevent the generation of downloadable keys.

### Modern Authentication Mechanisms

- **Service Account Impersonation**:
  - Users or pipelines temporarily assume the privileges of a service account using the `roles/iam.serviceAccountTokenCreator` role through short-lived signed API calls.
- **Workload Identity (for Google Kubernetes Engine - GKE)**:
  - Direct mapping of a Kubernetes Service Account (KSA) to a GCP Service Account (GSA), eliminating credentials written into pods.
- **Workload Identity Federation**:
  - Connection of external identities (GitHub Actions, GitLab CI, AWS IAM, Azure AD) through OpenID Connect (OIDC) or SAML 2.0 to issue short-lived access tokens in GCP without using static keys.

---

## 🛡️ 4. Security Perimeters (VPC Service Controls) and Conditional IAM

- **VPC Service Controls (VPC-SC)**:
  - Creation of logical security perimeters around GCP projects and services (BigQuery, Storage, Vertex AI).
  - Prevents valid identities with sufficient IAM permissions from exfiltrating data outside the approved network perimeter or to unauthorized projects.
- **Conditional IAM Bindings**:
  - Assignment of permissions that take effect only if expressions in **CEL (Common Expression Language)** are satisfied:
```text
// Permissão válida apenas dentro do horário comercial (Fuso UTC)
request.time.getHours('UTC') >= 9 && request.time.getHours('UTC') <= 18

// Permissão restrita a requisições originadas do intervalo de IP da VPN corporativa
resource.type == "storage.googleapis.com/Bucket" &&
request.auth.access_levels["accessPolicies/12345/accessLevels/VpnAccess"]
```

---

## 📊 5. Auditing, Logging, and IAM Recommender

- **Cloud Audit Logs**:
  - *Admin Activity Logs*: Automatic, unalterable record of all IAM and configuration modifications.
  - *Data Access Logs*: Record of read/write operations on sensitive data objects (BigQuery, Cloud Storage).
- **IAM Recommender**:
  - A GCP learning engine that analyzes permission usage over the last 90 days and generates automatic recommendations to revoke unused roles or migrate from broad roles to granular roles.

---

## ⚙️ GCP IAM Engineer Decision Protocol

1. **Disable Service Account Key Creation**: Apply the `iam.disableServiceAccountKeyCreation` organizational policy.
2. **Eliminate Primitive Roles (Owner/Editor)**: Replace them with predefined or custom roles tuned by IAM Recommender analysis.
3. **Enforce Group Assignment**: Never bind roles directly to individual user email accounts; always bind to Google Groups synchronized with your IdP.

---

## 🔗 Integration with Other Skills

- To integrate GCP IAM with the Gemini Enterprise and Vertex AI ecosystem, see the [gemini-enterprise](../../../platforms/gemini-enterprise/SKILL.md) skill.
- For general identity governance and PAM guidelines, see the [iam-access-management](../iam-access-management/SKILL.md) skill.
- To align GCP with the CIS Google Cloud Computing Foundations Benchmark controls, see the [cis-controls](../../grc/cis-controls/SKILL.md) skill.
