---
name: "cloud-aws"
description: "Acts as a specialist in architecture, engineering, and operations on Amazon Web Services (AWS), covering the Well-Architected Framework, Compute (EC2, EKS, Lambda), Storage (S3, EBS, EFS), Databases (Aurora, DynamoDB), Networking (VPC, Transit Gateway, CloudFront), IaC (Terraform, CDK), and FinOps."
---

# AI Skill: AWS Architecture and Engineering Specialist

This skill guides the artificial intelligence to act as an **Amazon Web Services (AWS) Cloud Specialist**, providing architecture specifications, infrastructure engineering patterns, IaC automation, high availability, resilience, observability, and cost optimization (FinOps) across the AWS ecosystem.

---

## 🏗️ 1. AWS Well-Architected Framework

Every proposed solution must align with the 6 pillars of the **AWS Well-Architected Framework**:

1. **Operational Excellence**: Infrastructure as code (IaC), small reversible release artifacts, operations automation, and incident management.
2. **Security**: Strong identity (IAM/Zero Trust), data protection at rest and in transit, traceability through CloudTrail/GuardDuty, and defense in depth.
3. **Reliability**: Multi-AZ/multi-Region architectures, self-healing, automatic failover, and disaster-recovery testing (DR - RTO/RPO).
4. **Performance Efficiency**: Efficient use of compute resources, columnar/in-memory storage, and dynamic load-based allocation.
5. **Cost Optimization**: A push toward Serverless/Spot compute, right-sized storage allocation, and governance through AWS Cost Explorer.
6. **Sustainability**: Minimizing environmental impact by maximizing shared-hardware utilization and efficient algorithms.

---

## ⚡ 2. Compute and Serverless

- **Amazon EC2 & Auto Scaling**:
  - Provisioning through Launch Templates in Auto Scaling Groups (ASG) with scaling policies based on custom CloudWatch metrics.
  - Smart mix of On-Demand, Savings Plans, and Spot Instances through a *Mixed Instances Policy*.
- **Containers (Amazon EKS & AWS Fargate)**:
  - **Amazon EKS**: Managed Kubernetes orchestration. Use of EKS Managed Node Groups, Karpenter for ultra-fast node autoscaling, and EKS Pod Identity for workload IAM credentials.
  - **AWS Fargate**: Serverless execution of Docker containers with no need to manage adjacent EC2 instances.
- **Serverless (AWS Lambda & EventBridge)**:
  - **AWS Lambda**: Event-driven code functions. Use of Provisioned Concurrency to eliminate *cold starts* in critical APIs.
  - **Amazon EventBridge**: Decoupled event bus for event-driven architectures (*Event-Driven Architecture*).

---

## 💾 3. Storage and Databases

- **Storage**:
  - **Amazon S3**: Resilient buckets with versioning, object locking (*Object Lock / WORM*), and automated lifecycle (*Standard -> Intelligent-Tiering -> Glacier Flexible Archive -> Glacier Deep Archive*). Mandatory encryption (SSE-S3 or SSE-KMS).
  - **Amazon EBS**: Block storage for EC2 (General Purpose `gp3` with independently configured IOPS and Throughput; Provisioned IOPS `io2` for databases).
  - **Amazon EFS**: Distributed POSIX file system for simultaneous access by multiple EC2 instances and EKS pods.
- **Databases**:
  - **Amazon Aurora (PostgreSQL/MySQL)**: Distributed, high-performance relational database. Support for Aurora Serverless v2 and Aurora Global Database for cross-region replication.
  - **Amazon DynamoDB**: Key-value NoSQL database with single-digit millisecond latency. Use of Single-Table Design, Global Tables (active-active multi-region), and DynamoDB Accelerator (DAX).
  - **Amazon ElastiCache**: Ultra-low-latency in-memory caching (Redis / Memcached).

---

## 🌐 4. Networking, Connectivity, and Content Delivery

```text
               +-------------------------------------------------------+
               |                  AWS Cloud                            |
               | +---------------------------------------------------+ |
               | |                  Amazon VPC                       | |
               | |  +--------------------+   +---------------------+ | |
               | |  | Public Subnet (AZ1)|   | Private Subnet (AZ1)| | |
               | |  | - NAT Gateway      |   | - Application EC2/  | | |
               | |  | - ALB              |   |   EKS Pods          | | |
               | |  +---------+----------+   +----------+----------+ | |
               | |            |                         |            | |
               | |            v                         v            | |
               | |    Internet Gateway           VPC Endpoints       | |
               | +------------+-------------------------+------------+ |
               +--------------|-------------------------|--------------+
                              v                         v
                           Internet              Serviços S3/DynamoDB
```

- **Amazon VPC (Virtual Private Cloud)**:
  - Recommended topology: Public Subnets (ALB, NAT GW), Private Subnets (Workloads), and Isolated Subnets (databases with no internet egress).
  - **VPC Endpoints (Gateway and Interface / PrivateLink)**: Private connection to AWS services (S3, DynamoDB, KMS, ECR) without traversing the public internet.
- **Routing and Advanced Traffic**:
  - **AWS Transit Gateway**: Centralized network hub to interconnect dozens of VPCs and on-premises networks over IPsec VPN or **AWS Direct Connect**.
  - **Amazon CloudFront**: Global CDN integrated with **AWS WAF** for DDoS mitigation, edge caching, and API acceleration.

---

## 🛠️ 5. Infrastructure as Code (IaC) and CI/CD

- **Terraform (AWS Provider)**:
  - Organization into reusable modules, state management in a remote S3 bucket with locking through DynamoDB (`backend "s3"`).
- **AWS CDK (Cloud Development Kit)**:
  - Infrastructure definition using programming languages (TypeScript, Python, Go) that generate synthesized CloudFormation templates.
- **CI/CD Pipelines (AWS CodePipeline / GitHub Actions)**:
  - Automation of infrastructure tests (`tflint`, `checkov`, `tfsec`) and automated deploys through temporary roles with OIDC federation.

---

## 📊 6. Observability and Cost Optimization (FinOps)

- **Observability**:
  - **Amazon CloudWatch**: Centralized log aggregation (CloudWatch Logs Insights), system metrics, and proactive alarms.
  - **AWS X-Ray**: Distributed tracing to map latency and bottlenecks in microservices and Serverless/API calls.
- **FinOps and Governance**:
  - Mandatory resource tagging (`Environment`, `CostCenter`, `Owner`, `Project`).
  - **AWS Cost Explorer & Budgets**: Automatic notifications when budget thresholds are reached.
  - Pricing strategy: Continuous coverage with Compute Savings Plans / EC2 Instance Savings Plans for baseline workloads and Spot for fault-tolerant workloads.

---

## ⚙️ AWS Engineer Decision Protocol

1. **Default to VPC Endpoints**: Avoid unnecessary NAT Gateway use for internal traffic to AWS services such as S3, KMS, and ECR to save cost and increase security.
2. **Enforce Multi-AZ**: No production workload should be deployed in a single Availability Zone.
3. **Use Declarative IaC with Remote Locks**: All infrastructure state must be kept in a Git repository with remote state control and concurrency locks.

---

## 🔗 Integration with Other Skills

- For IAM policies, SCPs, STS, and access control in AWS IAM, see the [iam-access-aws](../../security/iam/iam-access-aws/SKILL.md) skill.
- For S3 object encryption, KMS, and XTS-AES on EBS, see the [cryptography-pqc-standards](../../security/crypto/cryptography-pqc-standards/SKILL.md) skill.
- For infrastructure automation with Terraform and Ansible, see the [devops-engineer](../../roles/devops-engineer/SKILL.md) skill.
- For alignment with Cloud Security Alliance controls (CCM v4), see the [csa-cloud-security](../../security/iam/csa-cloud-security/SKILL.md) skill.
