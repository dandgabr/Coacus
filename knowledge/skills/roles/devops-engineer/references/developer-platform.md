# Developer Platform Examples

These are conditional operational examples, not universal provider choices. Version pins inherited from the source are not verified as current by this update; resolve the selected platform documentation before use. Authorization, secrets and release verification follow the parent skill and repository standards.

## 🏛️ 6. Internal Developer Platform (IDP) with Backstage

**Backstage** (developed by Spotify and maintained by the CNCF) serves as the central developer portal (IDP), aggregating a **Software Catalog**, **Software Templates (Scaffolder)**, **TechDocs**, and operational metrics.

### 📑 Software Catalog: `catalog-info.yaml`

```yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: payment-gateway-api
  description: Core microservice responsible for processing credit card and pix transactions.
  annotations:
    github.com/project-slug: company/payment-gateway-api
    backstage.io/techdocs-ref: dir:.
    argocd/app-name: payment-gateway-api-prod
    datadog/service-name: payment-gateway
    sonarqube.org/project-key: company_payment-gateway-api
  tags:
    - java
    - spring-boot
    - fintech
    - pci-dss
spec:
  type: service
  lifecycle: production
  owner: group:payments-team
  system: payment-system
  providesApis:
    - payment-v2-api
  dependsOn:
    - resource:payment-aurora-db
    - component:fraud-detection-service
```

### 🧩 Software Template (Scaffolder): `template.yaml`

```yaml
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: springboot-microservice-template
  title: Production-Ready Spring Boot Service
  description: Scaffolds a complete Spring Boot 3 service with CI/CD, Helm chart, Dockerfile and SonarQube.
spec:
  owner: group:platform-team
  type: service
  parameters:
    - title: Service Configuration
      required:
        - component_id
        - owner
      properties:
        component_id:
          title: Service Identifier
          type: string
          description: Unique kebab-case name for the repo and deployment
        owner:
          title: Owning Team
          type: string
          ui:field: OwnerPicker
          ui:options:
            allowedKinds:
              - Group

  steps:
    - id: template
      name: Fetch Skeleton Template
      action: fetch:template
      input:
        url: ./skeleton
        values:
          component_id: ${{ parameters.component_id }}
          owner: ${{ parameters.owner }}

    - id: publish
      name: Publish to GitHub
      action: publish:github
      input:
        allowedHosts: ['github.com']
        description: Service created via Backstage IDP
        repoUrl: github.com?owner=company&repo=${{ parameters.component_id }}
        defaultBranch: main

    - id: register
      name: Register in Software Catalog
      action: catalog:register
      input:
        repoContentsUrl: ${{ steps.publish.output.repoContentsUrl }}
        catalogInfoPath: '/catalog-info.yaml'

  output:
    links:
      - title: Open GitHub Repository
        url: ${{ steps.publish.output.remoteUrl }}
```

---
