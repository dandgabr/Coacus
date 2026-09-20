---
name: "cloud-oci"
description: "Acts as a specialist in architecture, engineering, and operations on Oracle Cloud Infrastructure (OCI), covering the OCI Architecture Center, Compute (Bare Metal, VMs, OKE), Storage (Block Volumes, Object Storage), Databases (Autonomous Database, Exadata, MySQL HeatWave), Networking (VCN, DRG, FastConnect), IaC (Terraform, Resource Manager), and FinOps."
---

# AI Skill: Oracle Cloud (OCI) Architecture and Engineering Specialist

This skill guides the artificial intelligence to act as an **Oracle Cloud Infrastructure (OCI) Cloud Specialist**, providing architecture specifications for mission-critical enterprise workloads, autonomous databases, high-performance Bare Metal infrastructure, Terraform automation, distributed networking, and financial management across the OCI ecosystem.

---

## 🏗️ 1. OCI Architecture Center and Design Principles

1. **Compartment-Level Isolation and Control**:
   - Structuring **Compartments** for resource organization, IAM policies, and corporate quota limits (*Service Limits*).
2. **High Availability Architecture (Fault Domains & Availability Domains)**:
   - Distributing workloads across multiple **Availability Domains (ADs)** and **Fault Domains (FDs)** within a single region to guarantee resilience against hardware or physical rack power failures.
3. **Uncompromised Performance (Non-Overcommitted Hardware)**:
   - *Non-blocking flat network design* data-center networks and **Bare Metal** compute directly on silicon for extremely high-I/O workloads and heavy transactional databases.

---

## ⚡ 2. Compute and Containers

- **OCI Compute (Bare Metal & Virtual Machines)**:
  - **Bare Metal Instances**: Dedicated physical servers with no installed hypervisor. Raw CPU and memory performance with total isolation for Oracle Exadata and regulated environments.
  - **Virtual Machines (Flex Shapes)**: Tailored sizing of OCPUs (Oracle CPUs) and RAM (e.g., `VM.Standard3.Flex` or `VM.Standard.E5.Flex` instances), adjusting resources to the exact amount needed.
- **Containers & Serverless**:
  - **Oracle Container Engine for Kubernetes (OKE)**: Managed Kubernetes cluster with worker nodes paired to native Virtual Cloud Networks (VCNs) and integration with **OCI Web Application Firewall (WAF)**.
  - **OCI Functions**: Serverless platform based on the open-source **Fn Project**, triggered by OCI Events Service events or calls through API Gateway.

---

## 💾 3. Mission-Critical Storage and Databases

- **Storage**:
  - **OCI Block Volumes**: Block disk performance configured dynamically through **Volume Performance Units (VPUs)** (from *Lower Cost* to *Ultra High Performance* at up to 300,000 IOPS per volume). Mandatory encryption by default.
  - **OCI Object Storage**: High-durability object storage (*Standard*, *Infrequent Access*, *Archive*). Support for immutability (*Retention Rules / WORM*) and native encryption.
- **Oracle & Open Source Databases**:
  - **Oracle Autonomous Database (ATP / ADW)**: Relational database with AI-based auto-tuning, auto-patching, auto-scaling, and autonomous security.
  - **Oracle Exadata Database Service**: Dedicated or shared Exadata infrastructure on OCI cloud for maximum OLTP and Data Warehousing performance.
  - **MySQL HeatWave**: Managed MySQL service integrated with an in-memory analytics accelerator that combines OLTP and OLAP in the same database without ETL.

---

## 🌐 4. Networking and Infrastructure Connectivity

```text
               +-------------------------------------------------------+
               |                  Oracle Cloud Infrastructure          |
               | +---------------------------------------------------+ |
               | |                  Virtual Cloud Network (VCN)      | |
               | |  +--------------------+   +---------------------+ | |
               | |  | Public Subnet      |   | Private Subnet      | | |
               | |  | - Public LB        |   | - OKE Nodes / VMs   | | |
               | |  | - NAT Gateway      |   | - Autonomous DB     | | |
               | |  +---------+----------+   +----------+----------+ | |
               | |            |                         |            | |
               | |            v                         v            | |
               | |     Internet Gateway           Service Gateway    | |
               | |                                (Object Storage)   | |
               | +------------+-------------------------+------------+ |
               +--------------|-------------------------|--------------+
                              v                         v
                       Internet / User           OCI Internal Services
```

- **Virtual Cloud Network (VCN)**:
  - Creation of regional subnets (*Regional Subnets*) covering all ADs of the OCI region.
  - **Security Lists & Network Security Groups (NSGs)**: Stateful firewall rules applied at the subnet level or at the level of individual virtual network interfaces (VNICs).
- **Routing Hub and Dedicated Connectivity**:
  - **Dynamic Routing Gateway (DRG v2)**: Advanced virtual router to interconnect VCNs in the same region or cross-region (*Remote Peering*), IPSec VPNs, and **OCI FastConnect** links.
  - **Service Gateway**: Private access with no egress cost to Oracle's internal services (Object Storage, Autonomous DB, Auditing) without traversing the public internet.

---

## 🛠️ 5. Infrastructure as Code (IaC) and Management

- **Terraform (OCI Provider)**:
  - Official declarative provider covering the full set of OCI APIs. Support for Oracle Landing Zone reference-architecture modules.
- **OCI Resource Manager**:
  - Fully managed, OCI-cloud-hosted Terraform service for execution and state control (*State File*) with team governance and integration with Git repositories (GitHub, GitLab, Bitbucket).

---

## 📊 6. Observability and FinOps

- **OCI Observability & Management**:
  - **OCI Monitoring**: Real-time operational metrics and alarms via email, PagerDuty, or HTTP webhooks.
  - **OCI Logging & Logging Analytics**: Centralized log collection with an advanced search engine and intelligence for detecting operational anomalies.
  - **Application Performance Monitoring (APM)**: End-to-end distributed transaction tracing in microservice applications.
- **FinOps & Financial Optimization**:
  - **OCI Budgets & Cost Analysis**: Continuous cost monitoring with preventive alerts when budget percentages are reached.
  - **Universal Credits**: Unified purchase-credit model where credits can be flexibly allocated across any region or OCI cloud service.

---

## ⚙️ OCI Engineer Decision Protocol

1. **Prefer Regional Subnets**: Always configure regional subnets in VCNs instead of AD-specific subnets so that resources can scale freely across Availability Domains.
2. **Use the Service Gateway for Storage Traffic**: Never route Object Storage backup traffic over the public internet or NAT Gateway; always use the Service Gateway with no egress traffic cost.
3. **Move Away from Static Credentials with Instance Principals**: Configure Dynamic Groups and Instance Principals on VMs or OKE for native OCI API calls.

---

## 🔗 Integration with Other Skills

- For OCI IAM policies, dynamic groups, and policy language, see the [iam-access-oci](../../security/iam/iam-access-oci/SKILL.md) skill.
- For infrastructure automation with Terraform and Ansible, see the [devops-engineer](../../roles/devops-engineer/SKILL.md) skill.
- For OCI block volume encryption and key management in OCI Vault, see the [cryptography-pqc-standards](../../security/crypto/cryptography-pqc-standards/SKILL.md) skill.
- For compliance with Cloud Security Alliance controls (CCM v4) and CIS security benchmarks on OCI cloud, see [csa-cloud-security](../../security/iam/csa-cloud-security/SKILL.md) and [cis-controls](../../security/grc/cis-controls/SKILL.md).
