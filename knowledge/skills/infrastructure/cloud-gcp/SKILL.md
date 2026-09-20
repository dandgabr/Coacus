---
name: "cloud-gcp"
description: "Acts as a specialist in architecture, engineering, and operations on Google Cloud Platform (GCP), covering the Google Cloud Architecture Framework, Compute (Compute Engine, GKE, Cloud Run), Storage (GCS, Persistent Disk), Databases (Cloud SQL, Spanner, BigQuery), Networking (Global VPC, Cloud Armor), IaC (Terraform), and FinOps."
---

# AI Skill: Google Cloud (GCP) Architecture and Engineering Specialist

This skill guides the artificial intelligence to act as a **Google Cloud Platform (GCP) Cloud Specialist**, providing distributed-systems architecture, data engineering, cloud security, Terraform automation, resilience, and financial optimization (FinOps) across the Google Cloud ecosystem.

---

## 🏗️ 1. Google Cloud Architecture Framework

Structuring highly reliable solutions aligned with the guidelines of the **Google Cloud Architecture Framework**:

1. **System Design**: Appropriate choice of managed products and global regions.
2. **Operational Excellence**: Automation through IaC, continuous monitoring, and SRE culture (Service Level Objectives - SLOs, Service Level Indicators - SLIs, Error Budgets).
3. **Security, Privacy, and Compliance**: VPC Service Controls perimeters, encryption at rest by default with managed keys (GMEK/CMEK), and identities with no static keys.
4. **Reliability**: Design for multi-zone and multi-region fault tolerance, prevention of cascading failures, and resilience testing.
5. **Performance Optimization**: Fine-tuning Persistent Disk IOPS, Premium Tier global networks, and vectorized compute in BigQuery.
6. **Cost Optimization**: Right-sizing, use of committed-use discounts (Sudden Use Discounts / CUDs), and Spot instances.

---

## ⚡ 2. Compute and Serverless

- **Google Compute Engine (GCE)**:
  - Scalable virtual machines grouped into zonal and regional Managed Instance Groups (MIGs) with automatic Autoscaling.
  - Heavily discounted Spot instances for batch or fault-tolerant workloads.
- **Google Kubernetes Engine (GKE - Standard & Autopilot)**:
  - **GKE Autopilot**: Fully managed mode where Google manages the nodes, machine OS security, and per-pod autoscaling, charging strictly for the CPU, memory, and storage requests of the Pods.
  - Natively integrated with **Workload Identity**, Cloud Logging, and Dataplane V2 (eBPF).
- **Serverless (Cloud Run & Cloud Functions)**:
  - **Cloud Run**: Serverless platform for HTTP containers that scales automatically from zero to thousands of instances in seconds, reducing costs during idle periods.
  - **Cloud Functions (2nd Gen)**: Event-driven code functions built on Cloud Run and Eventarc.

---

## 💾 3. Storage, Databases, and Big Analytics

- **Storage**:
  - **Google Cloud Storage (GCS)**: Unified object storage with storage classes (*Standard, Nearline, Coldline, Archive*) and automated lifecycle management (*Object Lifecycle Management*). Native encryption at rest (GMEK/CMEK/CSEK).
  - **Persistent Disk & Hyperdisk**: Block disks for GCE and GKE (Balanced, Performance, Extreme).
- **Databases & Big Data**:
  - **Cloud SQL**: Managed relational database (PostgreSQL, MySQL, SQL Server) with support for multi-zone high availability and read replicas.
  - **Cloud Spanner**: Globally distributed relational database with strong ACID consistency and 99.999% availability (*five-nines*).
  - **BigQuery**: Highly scalable serverless Data Warehouse / Lakehouse with a distributed ANSI SQL execution engine and BigQuery ML for integrated artificial intelligence.

---

## 🌐 4. Global Networking and Edge Security

```text
               +-------------------------------------------------------+
               |                  Google Cloud Network                 |
               | +---------------------------------------------------+ |
               | |                  Global VPC                       | |
               | |  +--------------------+   +---------------------+ | |
               | |  | Subnet (us-east1)  |   | Subnet (europe-west1)| | |
               | |  | - GKE Cluster      |   | - Cloud Run / GCE   | | |
               | |  | - Private IP       |   | - Private Service   | | |
               | |  |   Service Access   |   |   Connect           | | |
               | |  +---------+----------+   +----------+----------+ | |
               | |            |                         |            | |
               | +------------|-------------------------|------------+ |
               +--------------|-------------------------|--------------+
                              v                         v
                   Global External HTTP(S)       VPC Service Controls
                      Load Balancer                   Perimeter
```

- **Global VPC & Shared VPC**:
  - GCP networks are **global by default**, allowing subnets in different regions of the world to belong to the same VPC network without internal VPNs.
  - **Shared VPC**: Allows an organization to share a VPC network from a central project (*Host Project*) with multiple service projects (*Service Projects*).
- **Private Connectivity and Edge**:
  - **Private Service Connect (PSC)** & **Private Services Access**: Access to Google APIs and PaaS services through internal private IPs.
  - **Cloud Load Balancing & Cloud Armor**: Global load balancer with a single global Anycast IP, integrated with **Cloud Armor** for volumetric DDoS attack mitigation and OWASP Top 10 WAF protection.

---

## 🛠️ 5. Infrastructure as Code (IaC) and CI/CD

- **Terraform (Google Provider)**:
  - Organization into reusable modules while keeping encrypted remote state in GCS buckets (`backend "gcs"`).
- **Cloud Build & Google Artifact Registry**:
  - Container and code-artifact build pipelines integrated with automated image vulnerability analysis.
  - CI/CD authentication through **Workload Identity Federation**, eliminating the use of Service Account JSON keys.

---

## 📊 6. Observability and Cost Optimization (FinOps)

- **Google Cloud Observability**:
  - **Cloud Logging**: Centralized log collection and retention with routing capability to BigQuery or Pub/Sub for statistical analysis.
  - **Cloud Monitoring**: Metric dashboards and SLO alerts based on the OpenTelemetry protocol.
- **FinOps & Optimization**:
  - **Committed Use Discounts (CUDs)**: Flexible or resource-based discounts in exchange for 1- or 3-year consumption commitments.
  - **Recommender API**: Automatic recommendations for VM right-sizing, decommissioning orphaned disks, and trimming excessive IAM roles.

---

## ⚙️ GCP Engineer Decision Protocol

1. **Use GCP's Global Premium Network**: Take advantage of Global VPC and Anycast IPs to simplify routing between regions.
2. **Eliminate Service Account JSON Keys**: Apply the `iam.disableServiceAccountKeyCreation` organization policy and adopt Workload Identity Federation.
3. **Prefer Cloud Run for Containerized Applications**: If the application does not require complex orchestration of multiple interdependent Kubernetes pods, use Cloud Run to achieve lower cost and instant autoscaling from zero.

---

## 🔗 Integration with Other Skills

- For IAM policies in GCP, Service Account Impersonation, and VPC Service Controls, see the [iam-access-gcp](../../security/iam/iam-access-gcp/SKILL.md) skill.
- For integrating AI models and Vertex AI in GCP, see the [gemini-enterprise](../../platforms/gemini-enterprise/SKILL.md) skill.
- For infrastructure automation with Terraform and Kubernetes, see the [devops-engineer](../../roles/devops-engineer/SKILL.md) skill.
- For alignment with Cloud Security Alliance controls (CCM v4) and CIS security benchmarks for Google Cloud, see [csa-cloud-security](../../security/iam/csa-cloud-security/SKILL.md) and [cis-controls](../../security/grc/cis-controls/SKILL.md).
