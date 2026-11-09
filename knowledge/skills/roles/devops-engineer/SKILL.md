---
name: devops-engineer
description: Definitive, practical guide to DevOps and Platform Engineering covering CI/CD, Terraform, Ansible, Vagrant, Kubernetes, Virtual Machines, Backstage IDP, GitOps, Observability, and Golden Paths.
---

# 🚀 DevOps & Platform Engineering

When promoting a reviewed interface or investigating a stale published revision, use [published artifact verification](references/published-artifact-verification.md). Verify the approved subject, configured destination, dependency graph and served behavior separately from build status. Preserve existing authorization and unrelated environments; a PR-only request does not authorize merge or deployment.

The role of the **DevOps & Platform Engineer** has evolved from simple automation of deployment scripts into building robust, scalable, and resilient platforms that enable the *self-service* model for software development teams.

This guide consolidates architecture standards, essential tools, production code, and best practices for designing, implementing, and operating modern cloud-oriented infrastructure and hybrid environments.

---

## Operational responsibilities

Establish the target environment, ownership and permitted actions first. Prefer declarative, reviewable changes with explicit state isolation, observability and a tested recovery path. Select the relevant tool-specific reference only after choosing that platform; examples do not authorize provisioning or deployment.

- For infrastructure as code (iac) with terraform, consult [terraform](references/terraform.md).
- For configuration management & automation with ansible, consult [ansible](references/ansible.md).
- For local development environments with vagrant, consult [vagrant](references/vagrant.md).
- For kubernetes orchestration and operations, consult [kubernetes](references/kubernetes.md).
- For virtual machine management & golden images, consult [golden images](references/golden-images.md).
- For internal developer platform (idp) with backstage, consult [developer platform](references/developer-platform.md).
- For modern ci/cd pipelines, consult [delivery pipelines](references/delivery-pipelines.md).
- For observability and reliability engineering (sre), consult [observability](references/observability.md).
- For platform engineering & developer experience (dx), consult [platform experience](references/platform-experience.md).

## 🔗 Related Skills

- [devsecops-engineer](../../security/operations/devsecops-engineer/SKILL.md)
- [software-architect](../software-architect/SKILL.md)
- [program-github](../../platforms/program-github-actions/SKILL.md)
- [github-actions](../../platforms/program-github-actions/SKILL.md)
- [containers](../../infrastructure/program-containers/SKILL.md)
