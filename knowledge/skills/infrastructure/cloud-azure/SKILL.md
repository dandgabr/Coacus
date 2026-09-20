---
name: "cloud-azure"
description: "Acts as a specialist in architecture, engineering, and operations on Microsoft Azure, covering the Cloud Adoption Framework, the Well-Architected Framework, Compute (VMs, AKS, App Services, Azure Functions), Storage (Blob, Files, Disks), Databases (Azure SQL, Cosmos DB), Networking (VNet, ExpressRoute, Front Door), IaC (Terraform, Bicep), and FinOps."
---

# AI Skill: Microsoft Azure Architecture and Engineering Specialist

This skill guides the artificial intelligence to act as a **Microsoft Azure Cloud Specialist**, providing architecture guidelines, cloud engineering practices, Bicep/Terraform automation, resilience, enterprise governance, and financial optimization (FinOps) across the Microsoft Azure ecosystem.

---

## 🏗️ 1. Azure Architecture and Governance Frameworks

- **Azure Cloud Adoption Framework (CAF)**:
  - Adoption methodology structured in phases: *Strategy*, *Plan*, *Ready* (Landing Zones), *Adopt*, *Govern*, and *Manage*.
  - **Azure Landing Zones**: A standardized enterprise environment architecture using Management Groups, scalable Subscriptions, and centralized policies.
- **Azure Well-Architected Framework**:
  - Pillars of excellence: *Reliability*, *Security*, *Cost Optimization*, *Operational Excellence*, and *Performance Efficiency*.
- **Governance with Azure Policy & Blueprints**:
  - Enforcement of compliance rules at the Management Group / Subscription level to impose strict rules (e.g., prohibit public IPs on VMs, require disk encryption, restrict deploy regions).

---

## ⚡ 2. Compute and Serverless

- **Azure Virtual Machines & VM Scale Sets (VMSS)**:
  - Automatic scaling of VM sets with support for Availability Sets (99.95% SLA) and Availability Zones (99.99% SLA).
  - Use of Spot Virtual Machines for interruption-tolerant batch-processing workloads.
- **Containers (Azure Kubernetes Service - AKS & Container Apps)**:
  - **AKS**: Fully managed Kubernetes cluster. Support for dynamic node pools, native integration with Entra ID (Azure AD RBAC), Azure CNI Networking, KEDA (Kubernetes Event-driven Autoscaling), and the Azure Key Vault Provider for Secrets Store CSI.
  - **Azure Container Apps**: Serverless platform for containerized microservices built on Kubernetes and Dapr.
- **Serverless & Web (Azure Functions & App Services)**:
  - **Azure Functions**: Event-triggered serverless execution (Event Hubs, Service Bus, Blob Triggers, HTTP).
  - **Azure App Service**: Managed hosting for high-availability web applications with support for *Deployment Slots* for zero-downtime (blue-green) deploys.

---

## 💾 3. Storage and Databases

- **Storage**:
  - **Azure Blob Storage**: Scalable object storage for unstructured data. Access tiers: *Hot*, *Cool*, *Cold*, and *Archive*. Support for immutability control (WORM), versioning, and replication (LRS, ZRS, GRS, RA-GTRS).
  - **Azure Managed Disks**: Disks for VMs (Ultra Disk, Premium SSD v2, Standard SSD/HDD). Native encryption with Server-Side Encryption (SSE) and Customer-Managed Keys (CMK).
  - **Azure Files**: Cloud-managed file shares accessible over the SMB 3.0 and NFS 4.1 protocols.
- **Databases**:
  - **Azure SQL Database & Managed Instance**: Fully managed SQL relational database. Native intelligence features, Auto-Tuning, Hyperscale (up to 100TB), and Failover Groups for disaster recovery.
  - **Azure Cosmos DB**: Globally distributed NoSQL database with single-digit millisecond latency SLAs. Support for multiple APIs (Core/SQL, MongoDB, Cassandra, Gremlin).
  - **Azure Database for PostgreSQL / MySQL Flexible Server**: Flexible managed servers with cross-zone high availability.

---

## 🌐 4. Networking, Connectivity, and Content Delivery

```text
               +-------------------------------------------------------+
               |                  Azure Cloud                          |
               | +---------------------------------------------------+ |
               | |                  Virtual Network (VNet)           | |
               | |  +--------------------+   +---------------------+ | |
               | |  | GatewaySubnet      |   | AppSubnet           | | |
               | |  | - Azure Firewall   |   | - AKS Nodes / VMs   | | |
               | |  | - Application GW   |   | - Private Endpoints | | |
               | |  +---------+----------+   +----------+----------+ | |
               | |            |                         |            | |
               | |            v                         v            | |
               | |      Public IP               Azure Key Vault /    | |
               | |                                Azure SQL Database | |
               | +---------------------------------------------------+ |
               +-------------------------------------------------------+
```

- **Azure Virtual Network (VNet) & Peering**:
  - Hub-and-Spoke VNet Topology structure.
  - **VNet Peering**: High-speed, low-latency connection between VNets in the same region or across regions (*Global VNet Peering*).
  - **Private Endpoints & Azure Private Link**: Private exposure of PaaS services (Azure Storage, SQL, Key Vault) inside the VNet, eliminating exposure to public IPs.
- **Network Security and Edge**:
  - **Azure Firewall**: Network firewall as a service with L3-L7 traffic inspection and threat intelligence.
  - **Azure Application Gateway & WAF**: Layer 7 load balancer with support for SSL Offloading and Web Application Firewall.
  - **Azure ExpressRoute**: Dedicated high-speed private connections between on-premises corporate data centers and Microsoft Azure infrastructure.

---

## 🛠️ 5. Infrastructure as Code (IaC) and DevOps

- **Bicep Language & ARM Templates**:
  - Native declarative language developed by Microsoft for fast, modular provisioning on Azure, with full same-day (*Day 0*) support for every new Azure resource.
- **Terraform (`azurerm` and `azapi` Providers)**:
  - Declarative multi-cloud provisioning. Secure remote state storage in an Azure Storage Account Blob with blob-level reader/writer locking.
- **Azure DevOps & GitHub Actions**:
  - Continuous integration and delivery (CI/CD) pipelines using passwordless authentication through **OIDC Workload Identity Federation**.

---

## 📊 6. Observability and Cost Optimization (FinOps)

- **Azure Monitor & Log Analytics**:
  - Centralized collection and analysis of diagnostic logs and metrics using KQL (Kusto Query Language).
  - **Application Insights**: Application performance management (APM) for diagnosing exceptions, response times, and distributed call tracing.
- **Azure Cost Management & FinOps**:
  - Configuration of budget alerts (*Budgets*) and automated alerts per Resource Group or Subscription.
  - Optimization with **Azure Reservations** (1- or 3-year commitments at up to 72% discount) and **Azure Savings Plans** for compute.

---

## ⚙️ Azure Engineer Decision Protocol

1. **Adopt Private Endpoints by Default**: No database, storage, or Key Vault resource should accept connections over public networks.
2. **Use Bicep or Terraform with AzAPI**: Whenever Bicep is the team's choice, modularize the infrastructure and use the `azapi` provider in Terraform when recent Azure resources are involved.
3. **Apply Azure Policies at the Root**: Establish restriction policies at the Management Group level to guarantee automatic compliance across all child Subscriptions.

---

## 🔗 Integration with Other Skills

- For Entra ID policies, Azure RBAC, PIM, and Managed Identities, see the [iam-access-azure](../../security/iam/iam-access-azure/SKILL.md) skill.
- For CI/CD pipeline automation and container management, see the [devops-engineer](../../roles/devops-engineer/SKILL.md) skill.
- For disk encryption and key management in Azure Key Vault, see the [cryptography-pqc-standards](../../security/crypto/cryptography-pqc-standards/SKILL.md) skill.
- For compliance with Cloud Security Alliance controls (CCM v4) and CIS security benchmarks on Azure cloud, see [csa-cloud-security](../../security/iam/csa-cloud-security/SKILL.md) and [cis-controls](../../security/grc/cis-controls/SKILL.md).
