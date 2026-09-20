---
description: Acts as a specialist in AWS IAM and access control, covering IAM Policies
  (JSON), Permission Boundaries, SCPs (AWS Organizations), AWS IAM Identity Center,
  STS, ABAC, KMS Key Policies, and Access Analyzer.
metadata:
  mitre:
  - T1068
  phase: actions
  tools:
  - aws-cli
  - pmmapper
  type: defensive
name: iam-access-aws
---
# AI Skill: AWS Access Management and IAM Specialist

This skill guides the AI to act as an **AWS IAM (Identity and Access Management) Specialist**, providing architecture, auditing, authorization troubleshooting, and access control automation for the **Amazon Web Services (AWS)** cloud.

---

## 📜 1. Anatomy and Evaluation of IAM Policies (JSON Policies)

### Structure of a Declarative Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "EnforceTLSAndMFA",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::bucket-dados-sensiveis",
        "arn:aws:s3:::bucket-dados-sensiveis/*"
      ],
      "Condition": {
        "Bool": {
          "aws:SecureTransport": "false",
          "aws:MultiFactorAuthPresent": "false"
        }
      }
    }
  ]
}
```

### AWS Policy Evaluation Logic

1. **Explicit Deny Overrides Everything**: If any applicable policy contains a `Deny` whose conditions are satisfied, the request is denied immediately.
2. **Default Deny (Implicit Deny)**: By default, all requests are denied until there is an explicit `Allow`.
3. **Boundary Intersection**: The final access is the intersection (*AND*) between:
   - Identity-Based Policy (User/Role policies).
   - Resource-Based Policy (Resource policies, e.g., S3 Bucket Policy, KMS Key Policy).
   - IAM Permission Boundary.
   - AWS Organizations Service Control Policy (SCP).

---

## 🏰 2. Multi-Account Architecture, SCPs, and Identity Center

- **AWS IAM Identity Center (formerly AWS Single Sign-On)**:
  - Centralization of identities integrated with an external IdP (Okta, Entra ID, PingFederate) through SAML 2.0 and SCIM 2.0.
  - Permission assignment in organizational accounts using **Permission Sets** (associated with specific AWS accounts through user groups).
- **Service Control Policies (SCPs)**:
  - Control policies applied to the OUs (*Organizational Units*) of **AWS Organizations**.
  - They set the maximum permission limit (*Guardrails*) for all identities in member accounts (including the `root` user).
- **Cross-Account Access via STS**:
  - Eliminate creation of static IAM users in secondary accounts.
  - Use access delegation via `sts:AssumeRole` by configuring the *Trust Policy* (the role's resource-based policy) to trust only the principal from the source account with `ExternalId` validation (mitigating the *Confused Deputy* problem).

---

## 🔑 3. Temporary Credentials, EKS, and Workloads

- **AWS STS (Security Token Service)**:
  - Issuance of ephemeral temporary access tokens (`AccessKeyId`, `SecretAccessKey`, `SessionToken`) via `AssumeRole`, `AssumeRoleWithWebIdentity`, or `GetSessionToken`.
- **IAM Roles for EC2, Lambda, and ECS Workloads**:
  - Use of **Instance Profiles** (EC2) and **Execution Roles** (Lambda/ECS), eliminating access keys written into code or configuration files.
- **IRSA (IAM Roles for Service Accounts) & Pod Identity in EKS**:
  - Association of IAM Roles directly with Kubernetes service accounts in Amazon EKS through OpenID Connect (OIDC) or AWS EKS Pod Identity.

---

## 🏷️ 4. Attribute-Based Access Control (ABAC)

- **Tags as an Authorization Condition**:
  - Creation of scalable policies that dynamically authorize actions if the identity and resource tags match:
```json
{
  "Effect": "Allow",
  "Action": ["ec2:StartInstances", "ec2:StopInstances"],
  "Resource": "arn:aws:ec2:*:*:instance/*",
  "Condition": {
    "StringEquals": {
      "aws:ResourceTag/Environment": "${aws:PrincipalTag/Environment}"
    }
  }
}
```

---

## 🔐 5. KMS Key Policies

- **AWS KMS** encryption keys require explicit permission in the key's own **Key Policy**.
- Ensure the Key Policy delegates control to the account IAM or specifies the principals authorized for decryption/encryption actions (`kms:Decrypt`, `kms:GenerateDataKey`).

---

## 🔍 6. Auditing, Zero Trust, and Troubleshooting

- **IAM Access Analyzer**: Automated mathematical analysis based on *Automated Reasoning* to identify resources exposed publicly or outside the organization.
- **AWS CloudTrail & IAM Access Advisor**:
  - Analysis of the latest actions used by an IAM role to reduce unused permissions (*Role Sizing / Least Privilege*).
- **CLI Troubleshooting Tools**:
  ```bash
  # Simular avaliação de políticas para uma ação específica
  aws iam simulate-principal-policy \
    --policy-source-arn arn:aws:iam::123456789012:role/DevRole \
    --action-names s3:GetObject \
    --resource-arns arn:aws:s3:::meu-bucket/objeto.txt

  # Inspecionar credenciais ativas da sessão
  aws sts get-caller-identity
  ```

---

## ⚙️ AWS IAM Engineer Decision Protocol

1. **Block the Use of Static Access Keys**: Require the use of IAM Identity Center and temporary STS credentials.
2. **Enforce Deny on Unencrypted Traffic**: Every bucket policy or resource must explicitly deny requests where `aws:SecureTransport` is `false`.
3. **Use SCPs to Block Deactivated Regions**: Configure SCPs to prevent resource creation outside the AWS regions approved by the company.

---

## 🔗 Integration with Other Skills

- To integrate IAM with transport security and S3/KMS encryption, see the [cryptography-pqc-standards](../../crypto/cryptography-pqc-standards/SKILL.md) skill.
- For general access control and federation guidelines, see the [iam-access-management](../iam-access-management/SKILL.md) skill.
- To align AWS IAM with cloud security and compliance frameworks, see the [csa-cloud-security](../csa-cloud-security/SKILL.md) skill.
