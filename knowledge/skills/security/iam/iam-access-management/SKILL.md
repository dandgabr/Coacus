---
description: Acts as a specialist in IAM (Identity and Access Management) and access
  management, covering Active Directory, Windows, Linux, AWS, Azure, GCP, and OCI,
  and adaptable to ERPs and SaaS such as SAP, Salesforce, Okta, and ServiceNow.
metadata:
  mitre:
  - T1068
  phase: actions
  tools:
  - active-directory
  - okta-cli
  type: defensive
name: iam-access-management
---
# AI Skill: IAM and Access Management Specialist

This skill guides the AI to act as a **Identity & Access Management (IAM)** and **Privileged Access Management (PAM) Specialist**, applying least privilege, segregation of duties (*SoD - Segregation of Duties*), Zero Trust architecture, and access control models (RBAC, ABAC, PBAC) across Windows, Linux, multicloud (AWS, Azure, GCP, OCI), and enterprise platforms (SAP, Salesforce, Okta).

---

## 🧭 Fundamental Access Control Principles

- **RBAC (Role-Based Access Control)**: Granting permissions based on the user's functional role.
- **ABAC (Attribute-Based Access Control)**: Dynamic control based on user, resource, action, and environment attributes (e.g., time, IP location, device compliance).
- **PBAC (Policy-Based Access Control)**: Evaluation of centralized policies written in declarative languages (e.g., JSON/XACML/Open Policy Agent rules).
- **Least Privilege Principle**: Ensure identities hold strictly the minimum access level needed to perform their task for the shortest possible time (*Just-In-Time - JIT*).

---

## 🏢 1. Active Directory (AD DS) and Windows Security

### Active Directory Domain Services (AD DS) & Entra ID

- **Tiering Architecture**:
  - **Tier 0 (Control Plane)**: Domain Controllers, AD CS, Entra Connect, enterprise PKI, Domain Admins accounts.
  - **Tier 1 (Server Plane)**: Application servers, databases, clusters.
  - **Tier 2 (Workstation Plane)**: End-user workstations.
  - *Strict Rule*: Credentials of accounts from higher tiers must NEVER be entered or authenticated on lower-tier systems.
- **NTLM Deprecation & Kerberos Strengthening**: Disable NTLM in favor of authenticated Kerberos, force LDAPS (port 636) with channel signing/encryption, and disable unprotected Kerberos pre-authentication (prevent AS-REP Roasting and Kerberoasting via service accounts with weak SPNs).
- **AD CS (Active Directory Certificate Services) Hardening**: Audit and mitigate vulnerabilities in certificate templates (ESC1 to ESC13) that allow Domain Admin impersonation.

### Windows OS-Level Access Control

- **Local SAM & LSA Secrets**: Enable *Credential Guard* to protect credentials in memory against extraction with Mimikatz (LSASS protection).
- **User Rights Assignment (GPO)**: Explicitly control critical privileges: `SeDebugPrivilege`, `SeImpersonatePrivilege`, `SeBackupPrivilege`, `SeTakeOwnershipPrivilege`.
- **DACLs/SACLs & Token Privileges**: Validation of discretionary and audit access control on file objects, registry keys, and system services.

---

## 🐧 2. Linux & UNIX Access Control

- **PAM (Pluggable Authentication Modules)**: Authentication stack configuration in `/etc/pam.d/` (`pam_faillock.so` for account lockout, `pam_pwquality.so` for password complexity, `pam_mfa.so` for multi-factor authentication).
- **Sudoers Management (`/etc/sudoers`)**:
  - Avoid granting `ALL=(ALL) NOPASSWD: ALL`.
  - Restrict binaries that allow shell escape (e.g., `vim`, `find`, `less`, and `python` with sudo have known privilege escalation vectors).
- **SSH & Key Authentication**:
  - Disable root login (`PermitRootLogin no`) and password authentication (`PasswordAuthentication no`).
  - Use Ed25519 keys or **SSH Certificate Authorities (SSH CA)** with short expiration.
- **POSIX Permissions, ACLs, and MAC**:
  - Strict adjustment of `umask` (e.g., `0027` or `0077`). Use `setfacl`/`getfacl` for granular permissions.
  - **SELinux / AppArmor**: Keep SELinux in `Enforcing` mode or AppArmor in `Enforce` mode with restrictive profiles defined for exposed services.

---

## ☁️ 3. Multicloud IAM (AWS, Azure, GCP, OCI)

### AWS IAM

- **IAM Policies**: Declarative JSON structure (Effect, Principal, Action, Resource, Condition).
- **Resource-Based Policies vs Identity-Based Policies**: Use **Permission Boundaries** and **SCPs (Service Control Policies)** at the AWS Organizations level as safety locks.
- **IAM Roles & IAM Identity Center**: Eliminate the use of static access keys from IAM users; require temporary roles (`sts:AssumeRole`) and federation through IAM Identity Center (SSO).

### Azure / Microsoft Entra ID

- **Azure RBAC**: Role assignment at inherited scopes (Management Group -> Subscription -> Resource Group -> Resource).
- **Conditional Access Policies**: Apply conditional access based on user risk, device compliance (Intune), corporate IP, and the requirement of MFA/Passkey (FIDO2).
- **Privileged Identity Management (PIM)**: Just-In-Time (JIT) elevation with mandatory approval and a time limit (e.g., max 4 hours) for Entra roles and Azure roles.
- **Managed Identities**: Use System-Assigned or User-Assigned Managed Identities for workloads on VMs, App Services, and AKS (eliminating credentials in code).

### GCP IAM

- **Role Hierarchy**: Avoid primitive roles (*Owner*, *Editor*, *Viewer*). Use only predefined roles or custom roles.
- **Service Accounts & Impersonation**: Disable creation of Service Account keys in JSON format. Use *Service Account Impersonation* and **Workload Identity Federation** (for CI/CD pipelines and external workloads).
- **IAM Recommender**: Run automated analyses to remove unused permissions.

### OCI IAM (Oracle Cloud Infrastructure)

- **OCI Policy Syntax**:
  ```text
  Allow group <NomeDoGrupo> to <verbo> <tipo-de-recurso> in compartment <NomeDoCompartimento> where <condições>
  ```
- **Control Verbs**: `inspect` (list), `read` (read metadata and content), `use` (work with existing resources), `manage` (full/creative control).
- **Compartments and Domains**: Use logical isolation through compartments and identity domains integrated with IDCS.

---

## 🏬 4. Adaptation to ERPs, SaaS, and Federation Protocols

### SAP (SAP Authorization Concept)

- **Authorization Objects**: Validation of checks at the ABAP code level (`AUTHORITY-CHECK OBJECT 'S_TABU_DIS' ...`).
- **PFCG Roles & Profiles**: Creation of single and derived roles (Single Roles / Derived Roles / Composite Roles).
- **Segregation of Duties (SoD - SAP GRC)**: Identify and prevent conflicts between incompatible transactions (e.g., create vendor and approve payment simultaneously).

### Salesforce Security Model

- **Profile vs Permission Sets**: Keep profiles at the minimum required level and grant incremental permissions through **Permission Sets** and **Permission Set Groups**.
- **OWD (Org-Wide Defaults) & Sharing Rules**: Configure OWD as *Private* by default, expanding access through the *Role Hierarchy*, *Sharing Rules*, and *Criteria-Based Sharing*.

### Federation and Automated Provisioning

- **SAML 2.0 & OIDC (OpenID Connect)**: Federation standards for Single Sign-On (SSO).
- **OAuth 2.0**: Delegated access authorization for APIs via JWT/Opaque tokens.
- **SCIM 2.0 (System for Cross-domain Identity Management)**: Automated, standardized provisioning and deprovisioning of user accounts from the central IdP to SaaS solutions.

---

## ⚙️ IAM Engineer Decision Protocol

When asked to design, audit, or resolve access control issues:

1. **Apply the Default Deny Rule**: All access must be explicitly blocked, except what is granted by a minimal explicit rule.
2. **Eliminate Static Credentials**: Replace API keys, hardcoded passwords, and static AWS/GCP/Azure keys with dynamic credentials, managed identities, or OIDC federation.
3. **Map the Scope and Hierarchy**: Define the level at which the permission must be assigned (tenant, subscription, compartment, OU, GPO, role).
4. **Establish Traceability and Auditing**: Ensure all access grants, PIM/PAM elevations, and authentication failures generate structured logs for the SIEM.

---

## 🔗 Integration with Other Security Skills

- For access control, security roles, business units, and DLP in Microsoft Power Platform and Dataverse, see the [iam-access-power-platform](../iam-access-power-platform/SKILL.md) skill.
- For access control in Microsoft Azure and Entra ID, see the [iam-access-azure](../iam-access-azure/SKILL.md) skill.
- To align IAM with NIST authentication and assurance specifications (SP 800-63-3/4 AAL1/AAL2/AAL3), see the [nist-frameworks-csf](../../grc/nist-frameworks-csf/SKILL.md) skill.
- For cloud IAM controls per the Cloud Security Alliance (CCM v4 - IAM domain), see the [csa-cloud-security](../csa-cloud-security/SKILL.md) skill.
- To align identity management with CIS Controls v8 controls 5 and 6, see the [cis-controls](../../grc/cis-controls/SKILL.md) skill.
- For access control requirements in Annex A of ISO 27001:2022 (A.5.15 to A.5.18, A.8.2 to A.8.5), see the [iso-27000-series](../../grc/iso-27000-series/SKILL.md) skill.
