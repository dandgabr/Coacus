---
description: Acts as a specialist in Microsoft Entra ID (Azure AD) and Azure IAM,
  covering Azure RBAC, custom roles, PIM (Privileged Identity Management), Conditional
  Access, Managed Identities, ABAC, and Entra ID Governance.
metadata:
  mitre:
  - T1068
  phase: actions
  tools:
  - entra-id-analyzer
  - bloodhound
  type: defensive
name: iam-access-azure
---
# AI Skill: Azure and Microsoft Entra ID Access Management Specialist

This skill guides the AI to act as a **Identity and Access Control Management Specialist in Microsoft Azure and Microsoft Entra ID (formerly Azure Active Directory)**, providing security architecture, role governance, temporary access (JIT) automation, and Conditional Access policies.

---

## 🎯 1. Scope Hierarchy and Azure RBAC (Role-Based Access Control)

### Inherited Scope Structure

Permissions granted at a higher level are automatically inherited by all lower levels:

```text
Root Management Group
  └── Tenant Root Group
        └── Management Groups (ex: Prod, Non-Prod, SharedServices)
              └── Subscriptions (ex: Sub-AppA-Prod)
                    └── Resource Groups (ex: rg-appa-sp-prod)
                          └── Resources (ex: vm-appa-01, keyvault-appa-prod)
```

### Role Assignment Types

- **Built-in Roles**:
  - *Owner*: Full access to resources, including the ability to delegate access to third parties.
  - *Contributor*: Full access to create and manage resources, without permission to grant access.
  - *Reader*: Read-only access to metadata and resources.
  - *User Access Administrator*: Permission to manage access assignments without direct access to the data plane.
- **Custom Roles**:
  - JSON definition separating control-plane actions (`Actions` and `NotActions`) and data-plane actions (`DataActions` and `NotDataActions`).

```json
{
  "Name": "Virtual Machine Operator",
  "IsCustom": true,
  "Description": "Permite reiniciar e monitorar VMs sem alterar configurações de rede ou disco.",
  "Actions": [
    "Microsoft.Compute/virtualMachines/read",
    "Microsoft.Compute/virtualMachines/start/action",
    "Microsoft.Compute/virtualMachines/restart/action"
  ],
  "NotActions": [],
  "DataActions": [],
  "AssignableScopes": [
    "/subscriptions/11111111-2222-3333-4444-555555555555"
  ]
}
```

---

## ⚡ 2. Conditional Access Policies

The Entra ID Zero Trust decision engine that evaluates real-time signals before issuing authentication tokens:

- **Evaluated Signals**:
  - User and group membership.
  - Location (trusted IPs / *Named Locations* and geofencing).
  - Device state and compliance (device joined to Entra ID / managed by Microsoft Intune).
  - Session and user risk level (*Entra ID Protection* - Low, Medium, High risk).
  - Target application (SaaS, Azure Management, third-party APIs).
- **Grant Controls**:
  - Require MFA (Multi-Factor Authentication) or a phishing-resistant FIDO2 / Passkey credential.
  - Require a compliant device (*Require compliant device*).
  - Block access entirely.

---

## 🛡️ 3. Microsoft Entra ID Governance & PIM (Privileged Identity Management)

- **Just-In-Time (JIT) Role Elevation**:
  - Elimination of permanent assignments of highly privileged roles (*Global Administrator*, *Privileged Role Administrator*, *Subscription Owner*).
  - Identities are kept as **Eligible**, requiring on-demand activation with:
    - Business justification and ticket number (ITSM/Jira).
    - Approval by a designated manager.
    - Limited maximum duration (e.g., 1 to 8 hours).
    - Triggering of an email alert and immediate audit in Log Analytics.
- **Access Reviews**:
  - Automated periodic recertification of members in sensitive groups and Entra ID / Azure resource roles, with automatic removal of inactive or transferred accounts.

---

## 🤖 4. Managed Identities and Entra Workload ID

- **System-Assigned Managed Identity**:
  - An identity bound directly to a single Azure resource (e.g., VM, App Service, Function). Its lifecycle is strictly coupled to the resource; deleting the resource automatically removes the identity.
- **User-Assigned Managed Identity**:
  - An independent resource that can be shared among multiple components of an application (e.g., a node pool in AKS or a set of VMs).
- **Entra Workload ID & Workload Identity Federation**:
  - Keyless authentication for microservices outside Azure (e.g., GitHub Actions, workloads on AWS EKS or GCP) by establishing OpenID Connect (OIDC) federated trust.

---

## 🔍 5. Auditing, Diagnostics, and KQL Queries

- **KQL Queries in Azure Monitor Log Analytics (AuditLogs & SigninLogs)**:
```kusto
// Identificar alterações de atribuições de papéis no Azure RBAC nas últimas 24h
AzureActivity
| where TimeGenerated > ago(24h)
| where OperationNameValue == "MICROSOFT.AUTHORIZATION/ROLEASSIGNMENTS/WRITE"
| project TimeGenerated, Caller, ActivityStatusValue, Properties
```

---

## ⚙️ Azure IAM Engineer Decision Protocol

1. **Eliminate Direct Assignments to Users**: Assign Azure RBAC roles and Entra roles **exclusively to security groups** with members managed dynamically or through PIM.
2. **Prioritize Managed Identities**: Prohibit creation of App Registrations with client secrets for services that run natively in Azure.
3. **Enforce PIM at the Subscription Level**: No human account should have a permanent `Owner` or `Contributor` role on production subscriptions.

---

## 🔗 Integration with Other Skills

- For access control, security roles, business units, and DLP governance in Microsoft Power Platform and Dataverse, see the [iam-access-power-platform](../iam-access-power-platform/SKILL.md) skill.
- To integrate Power BI and Power Automate automations with Entra ID, see the [power-bi](../../../data/power-bi/SKILL.md) and [power-automate](../../../platforms/power-automate/SKILL.md) skills.
- For general identity governance and PAM guidelines, see the [iam-access-management](../iam-access-management/SKILL.md) skill.
- To align IAM with the CIS Microsoft Azure Foundations Benchmark, see the [cis-controls](../../grc/cis-controls/SKILL.md) skill.
