---
name: "iam-access-power-platform"
description: "Acts as a specialist in IAM (Identity and Access Management) for Microsoft Power Platform, Power Apps, and Dataverse, covering Security Roles, Privileges, Business Units, Teams (Owner/Access/Group), Column-Level Security, Hierarchy Security, DLP Policies, Environment Roles, Managed Environments, and ALM Security."
metadata:
  mitre:
  - T1078
  - T1098
  phase: actions
  tools:
  - power-platform-admin-center
  - pac-cli
  - dataverse-web-api
  type: defensive
---
# AI Skill: Access Management and IAM Specialist in Microsoft Power Platform, Power Apps, and Dataverse

This skill guides the AI to act as a **Identity and Access Control Management (IAM) Specialist in Microsoft Power Platform, Power Apps, and Dataverse**, providing multi-layered security architecture, privilege governance, Business Unit and Team modeling, column-level protection, DLP policies, and security for ALM pipelines.

---

## 🏛️ 1. Multi-Layered Security Architecture in Power Platform

Security in Microsoft Power Platform is structured as defense in depth divided into 5 hierarchical levels:

```text
+-----------------------------------------------------------------------+
| 1. Tenant Level (Microsoft Entra ID, Licenciamento, Conditional Access)|
+-----------------------------------------------------------------------+
                                  |
                                  v
+-----------------------------------------------------------------------+
| 2. Environment Level (Environment Admin, Maker, SysAdmin, IP Firewall)|
+-----------------------------------------------------------------------+
                                  |
                                  v
+-----------------------------------------------------------------------+
| 3. Dataverse Level (RBAC: Business Units, Teams, Security Roles)      |
+-----------------------------------------------------------------------+
                                  |
                                  v
+-----------------------------------------------------------------------+
| 4. Record Level (Ownership, Access Levels, POA Table & Sharing)       |
+-----------------------------------------------------------------------+
                                  |
                                  v
+-----------------------------------------------------------------------+
| 5. Column Level (Column Security Profiles / Field-Level Security)     |
+-----------------------------------------------------------------------+
```

### Native Environment Roles

- **Environment Admin**: Full environment administration permission (create resources, manage users, apply DLP), but does not automatically grant access to Dataverse data unless the `System Administrator` role is assigned.
- **Environment Maker**: Permission to create new resources (Canvas Apps, Model-Driven Apps, Power Automate flows, Custom Connectors), but without access to other users' data.
- **System Administrator**: Full read, write, customization, and administration access to all Dataverse data and tables in the environment.
- **System Customizer**: Permissions to customize tables, forms, and flows, but with limited access to business data compared with `System Administrator`.

---

## 🛡️ 2. Dataverse Security Model: Roles, Privileges, and Scopes

Dataverse uses a highly granular **Role-Based Access Control (RBAC)** model.

### Per-Table Privilege Matrix (Record-Level Privileges)

For each table in Dataverse, 8 fundamental privileges can be configured:

| Privilege | Technical Description |
| :--- | :--- |
| **Create** | Permission to instantiate new records in the table. |
| **Read** | Permission to query and view the record's content. |
| **Write** | Permission to update and modify attributes of an existing record. |
| **Delete** | Permission to permanently remove a record. |
| **Append** | Permission to associate the current record with another parent record (attach a child record). |
| **Append To** | Permission to allow other child records to be attached to the current record. |
| **Assign** | Permission to transfer a record's *ownership* to another user/team. |
| **Share** | Permission to grant view or write access to a record to another user while retaining ownership. |

> **Note on Append / Append To**: To create a relationship between two records (e.g., add a Note to an Account), the user must have the `Append` privilege on the Note and the `Append To` privilege on the Account.

---

### Access Levels / Depth Scopes

Privileges are associated with scope levels that determine the reach of the permission in the organizational tree:

```text
[ Global / Organization ] ──> Acesso a todos os registros do ambiente.
        |
        v
[ Deep / Parent: Child BUs ] ──> Acesso na BU do usuário e em todas as BUs filhas subordinadas.
        |
        v
[ Local / Business Unit ] ──> Acesso estrito aos registros mantidos na mesma BU do usuário.
        |
        v
[ Basic / User ] ──> Acesso exclusivo a registros pertencentes ao usuário ou compartilhados com ele/suas equipes.
        |
        v
[ None ] ──> Nenhum acesso permitido.
```

---

### Team Privilege Inheritance

When assigning a Security Role to a user or team, the inheritance form is configured:

- **Direct User (Basic) access level and Team privileges (default)**: The user receives privileges directly plus the privileges of the teams of which they are a member. They can create records under their own name.
- **Team privileges only**: The user obtains privileges **only** when acting as a member of a team. It prevents creating records under an individual name if there is no direct user privilege. Ideal for strict segregation of duties (*SoD - Segregation of Duties*).

---

## 🏢 3. Business Units (BUs) and Team Architecture

### Business Unit Hierarchy

- **Root Business Unit**: Created automatically with the environment. It cannot be deactivated or deleted.
- **Child Business Units**: Organizational substructures created to segregate data by department, geographic region, or business unit.
- **Matrix Business Units / Modern Hierarchy**: Support for data access across multiple BUs without moving the user's account from their primary BU.

---

### Team Types in Dataverse (Teams Architecture)

1. **Owner Teams**:
   - They can own records directly (`OwnerId`).
   - They have associated Security Roles. Any record belonging to an Owner Team is accessible to all its members according to the team's roles.

2. **Access Teams**:
   - **They do not own records** and **do not have direct Security Roles**.
   - Used for dynamic and temporary sharing of individual records using *Access Team Templates*.
   - They prevent bloat of the `PrincipalObjectAccess` (POA) security table.

3. **Group Teams (Microsoft Entra ID Group Teams)**:
   - **Entra ID Security Groups** or **Microsoft 365 Groups** bound to Dataverse Security Roles.
   - **JIT (Just-In-Time) Provisioning**: When a user joins the Entra ID group, they automatically gain access to Dataverse resources without manual role management in the Power Platform Admin Center.

```text
Entra ID Security Group ──(Sincronização Automática)──> Dataverse Group Team ──(Security Role)──> Acesso ao Dataverse
```

---

## 🔒 4. Column-Level Security and Hierarchy Security

### Column-Level Security (Column Security Profile / FLS)

When table-level privileges are not enough to protect sensitive attributes (e.g., Salary, National ID, Medical Data):

1. Enable the **IsSecured** property on the table field/column in Dataverse.
2. Create a **Column Security Profile**.
3. Define explicit **Create**, **Read**, and **Update** permissions for the field.
4. Assign the profile to users or Group Teams.

```text
Tabela: Funcionário
 ├── Nome (Acesso padrão via Security Role)
 ├── Cargo (Acesso padrão via Security Role)
 └── Salário [IsSecured = True] ──> Column Security Profile (Permissão de Leitura exclusiva do RH)
```

---

### Hierarchy Security

Extends the access model based on the leadership structure or organizational positions:

- **Manager Hierarchy**: Uses the `ParentSystemUserId` field (Manager). A manager gains read/write access to the records of their direct reports and extended read access to indirect reports up to the configured depth.
- **Position Hierarchy**: Defines position structures independent of the direct management org chart.

---

## ⚡ 5. PrincipalObjectAccess (POA) Table Management and Performance

The **POA (PrincipalObjectAccess)** table stores instances of explicit and implicit record sharing.

### Precautions and Bloat Mitigation (POA Bloat)

- **Problem**: Excessive use of the `Share` privilege across millions of individual records makes the POA table grow exponentially, degrading the performance of underlying SQL queries.
- **Dataverse IAM Best Practices**:
  - Avoid record-by-record sharing through code or manual flow.
  - Replace manual sharing with **Owner Teams** or **Access Team Templates**.
  - Use well-designed **Business Unit** hierarchies so visibility occurs naturally through scope privileges (`Business Unit` or `Parent: Child BUs`).

---

## 📱 6. Security in Power Apps (Canvas Apps vs Model-Driven Apps)

### Canvas Apps Security

- **App Sharing**: Assignment of permissions in the app (*Can View* or *Can Edit*).
- **User Context**: The Canvas App runs under the identity of the logged-in user. Sharing the application **does not grant data access**. The user must have corresponding permissions on the data source (Dataverse, SharePoint, SQL).
- **Implicitly Shared Connections**: Reusable connections (e.g., SQL with a service account). They require extreme caution to avoid inadvertent privilege escalation.

### Model-Driven Apps Security

- **Binding to Security Roles**: The visibility and execution capability of a Model-Driven App are bound directly to the Security Roles assigned to the user. If the user's role is not associated with the App Module, the application will not appear in the portal.

---

## 🌐 7. Governance, DLP Policies, and Managed Environments

### Data Loss Prevention (DLP) Policies

Data loss prevention policies control data flow between connectors in the environment:

- **Connector Groups**:
  - **Business**: Approved corporate connectors (e.g., Dataverse, SQL Server, Office 365 Outlook).
  - **Non-Business**: Personal or general-purpose connectors (e.g., Twitter/X, personal Google Drive).
  - **Blocked**: Connectors whose use is strictly prohibited in the environment.
- **Fundamental Rule**: Connectors in the *Business* group **cannot exchange data** with connectors in the *Non-Business* group.
- **Connector Action Control & Endpoint Filtering**: Allows blocking specific actions (e.g., allow read but block write on an HTTP connector) or restricting destination domains/endpoints.

### Network Isolation and Security

- **Tenant Isolation**: Blocks inbound and outbound connections with untrusted Entra ID tenants.
- **IP Firewall**: Restricts access to Dataverse environments to authorized corporate IP ranges only.

---

## 🤖 8. IAM in ALM (Application Lifecycle Management) and Service Principals

To deploy solutions without interruptions and without depending on human accounts:

1. **Application Users in Dataverse**:
   - Creation of an *App Registration* in Microsoft Entra ID (Service Principal).
   - Registration as an **Application User** in Dataverse (does not consume a Power Apps license).
   - Assignment of custom Security Roles (e.g., *Deployment Administrator*) for executing CI/CD pipelines through Azure DevOps or GitHub Actions (`pac cli`).
2. **Environment Variables & Connection References**:
   - Maintaining production connections attached to dedicated Service Principals instead of developer accounts.

---

## ⚙️ Power Platform IAM Engineer Decision Protocol

1. **Apply the Least Privilege Principle**:
   - Never assign `System Administrator` to end users or service accounts in production.
   - Use the native `Basic User` or `App Opener` role as a base for creating custom roles.
2. **Prioritize Entra ID Group Teams**:
   - Avoid binding Security Roles directly to individual users. Centralize access management in Entra ID groups for automated governance.
3. **Avoid the POA Table**:
   - Model access through Business Units and owner teams instead of using individual record sharing (`Share`).
4. **Audit Periodically in Microsoft Purview**:
   - Enable auditing in Dataverse (*Audit Log*) to monitor changes to Security Roles, access to sensitive tables, and record deletions.

---

## 🔗 Integration with Other IAM and Cloud Skills

- For global IAM governance, RBAC/ABAC/PBAC principles, and OIDC/SAML/SCIM federation, see the [iam-access-management](../iam-access-management/SKILL.md) skill.
- For deep integration with Microsoft Entra ID, Conditional Access, PIM, and Managed Identities, see the [iam-access-azure](../iam-access-azure/SKILL.md) skill.
- For access control in multicloud environments and AWS IAM Center, see the [iam-access-aws](../iam-access-aws/SKILL.md) skill.
- For Workload Identity Federation and access control on Google Cloud, see the [iam-access-gcp](../iam-access-gcp/SKILL.md) skill.
- For compartments and IAM policies in Oracle Cloud Infrastructure, see the [iam-access-oci](../iam-access-oci/SKILL.md) skill.
- For the cloud security control matrix (CCM v4), see the [csa-cloud-security](../csa-cloud-security/SKILL.md) skill.
- For flow automation with connectors and governance in Power Automate, see the [power-automate](../../../platforms/power-automate/SKILL.md) skill.
- For frontend development and componentization in Power Apps, see the [frontend-developer](../../../roles/frontend-developer/SKILL.md) skill.
- For reuse and clean code best practices, see the [clean-code-reusability](../../../engineering/practices/clean-code-reusability/SKILL.md) skill.
