---
name: "program-containers"
description: "Specialist in container technologies and ecosystems (local and cloud), with mastery of OCI standards, Docker, Podman, CRI-O, Buildah, Kubernetes, secure registries, hardening, and managed cloud orchestration."
---

# 📦 AI Skill: Container Technologies (Docker, Podman, CRI-O, Buildah & Kubernetes)

This skill guides the artificial intelligence to act as a **Container Technologies Specialist**, covering the complete lifecycle of packaging, distribution, security, runtime isolation, and orchestration of containers in local, hybrid, and multi-cloud environments.

---

## 📜 1. OCI Standard (Open Container Initiative) & Image Architecture

The **Open Container Initiative (OCI)** establishes open standards for image formats, runtimes, and distribution, guaranteeing interoperability across different tools (Docker, Podman, Buildah, containerd, CRI-O).

### Fundamental Specifications
- **OCI Image Specification**: Defines the structure of a layered image file (tarballs), the JSON configuration file (execution metadata, environment variables, entrypoint), the **Manifest** (layer and config descriptor), and the **Manifest List / Image Index** (support for multiple CPU architectures, such as `amd64`, `arm64`, `riscv64`).
- **OCI Runtime Specification**: Defines the container execution environment configuration (`config.json`), the process lifecycle (create, start, stop, delete), and the interface used by low-level runtimes such as `runc`, `crun`, and `youki`.
- **OCI Distribution Specification**: Standardizes the HTTP/REST API for push, pull, authentication, cataloging, and management of blobs and manifests between container clients and Registries.

### Layer Anatomy and Storage Drivers
- **Immutability and Reuse**: Images are composed of *read-only* layers stacked via SHA256 content addressability.
- **Copy-on-Write (CoW)**: When a container is instantiated, a thin writable layer (*writable container layer*) is allocated on top. Modifications to existing files trigger a copy to the upper layer.
- **OverlayFS (overlay2)**: The default storage driver on Linux, combining `lowerdir` (read-only image layers), `upperdir` (container read-write layer), `workdir` (intermediate area), and `merged` (unified view mounted in the container filesystem).

---

## 🐳 2. Docker & Build Best Practices

**Docker** remains the most widespread development platform for creating and running containers.

### Dockerfile Best Practices
1. **Instruction Order and Layer Caching**: Place rarely changed instructions (such as OS package installation and dependency downloads) before instructions that change frequently (source-code copy).
2. **Strict Use of `.dockerignore`**: Exclude unnecessary files (`.git`, `node_modules`, `target/`, `.env`, logs, documentation) to speed up context upload and prevent secret leakage.
3. **Non-Root Execution**: Create a dedicated user with a fixed UID/GID in the container and never run the application as `root` in production.
4. **Command Combination**: Combine package installation and cache-cleanup commands in the same `RUN` instruction to prevent temporary files from remaining written in intermediate layers.

### Practical Example: Optimized Multi-Stage Build (Go Backend with Scratch/Distroless)

```dockerfile
# ==========================================
# Stage 1: Build & Compilation Environment
# ==========================================
FROM golang:1.24-alpine AS builder

# Install build dependencies and security certificates
RUN apk add --no-cache ca-certificates git tzdata

# Set working directory
WORKDIR /app

# Optimize layer caching by copying dependencies first
COPY go.mod go.sum ./
RUN go mod download && go mod verify

# Copy application source code
COPY . .

# Compile static binary without CGO dependencies
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build \
    -ldflags="-w -s -X main.version=1.0.0" \
    -trimpath \
    -o /app/server ./cmd/server

# Create a non-privileged user and group for runtime
RUN echo "nonroot:x:65532:65532:nonroot user:/:/sbin/nologin" > /etc/passwd_nonroot

# ==========================================
# Stage 2: Minimal Production Runtime
# ==========================================
FROM scratch AS production

# Copy essential runtime files from builder
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /usr/share/zoneinfo /usr/share/zoneinfo
COPY --from=builder /etc/passwd_nonroot /etc/passwd
COPY --from=builder --chown=65532:65532 /app/server /server

# Use non-privileged user
USER 65532:65532

# Expose service port
EXPOSE 8080

# Configure healthcheck (via executable or API endpoints)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD ["/server", "--healthcheck"] || exit 1

# Set production entrypoint
ENTRYPOINT ["/server"]
```

### `.dockerignore` Example
```text
.git
.gitignore
.env
.env.*
node_modules
dist
target
bin
*.md
Dockerfile*
docker-compose*.yml
tests/
coverage/
```

### Docker Networks and Volumes
- **Networks**:
  - `bridge`: Default isolated network for containers on the same host machine.
  - `host`: Eliminates the container's network isolation, using the host network interface directly.
  - `overlay`: Enables encrypted multi-host communication (used in Docker Swarm and orchestrators).
  - `none`: Fully disables network interfaces in the container.
- **Volumes**:
  - **Named Volumes**: Managed by Docker (`/var/lib/docker/volumes`), isolated from the host filesystem, and high performance.
  - **Bind Mounts**: Direct mapping of a host path into the container (ideal for local development with hot-reloading).
  - **tmpfs Mounts**: Volatile storage in RAM, ideal for temporary secrets and high-performance transient data.

### Practical Example: Complete `docker-compose.yml` with Healthchecks and Isolation

```yaml
version: "3.8"

networks:
  frontend-net:
    driver: bridge
  backend-net:
    driver: bridge
    internal: true # Isolated network without external internet access

volumes:
  postgres-data:
    driver: local

services:
  database:
    image: postgres:16-alpine
    container_name: app-postgres
    restart: unless-stopped
    environment:
      POSTGRES_DB: appdb
      POSTGRES_USER: appuser
      POSTGRES_PASSWORD: secure_database_password
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - backend-net
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U appuser -d appdb"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 10s
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 512M

  api-service:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: app-api
    restart: unless-stopped
    depends_on:
      database:
        condition: service_healthy
    environment:
      PORT: 8080
      DATABASE_URL: postgres://appuser:secure_database_password@database:5432/appdb?sslmode=disable
    ports:
      - "8080:8080"
    networks:
      - frontend-net
      - backend-net
    healthcheck:
      test: ["CMD", "/server", "--healthcheck"]
      interval: 15s
      timeout: 3s
      retries: 3
      start_period: 5s
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 256M
```

---

## 🦭 3. Podman (Pod Manager) & Daemonless Architecture

**Podman** is a daemonless container engine (*without a central daemon*) designed to run containers and pods securely with native *rootless* support.

### Key Podman Characteristics
- **Daemonless Architecture**: Uses the traditional Linux fork-exec model. Each container is a direct child process monitored by `conmon` and executed via an OCI runtime (`runc` or `crun`), eliminating the *single point of failure* of a central daemon with root privileges.
- **Rootless by Default**: Allows users without administrative privileges to run containers securely using Linux *User Namespaces* (`/etc/subuid` and `/etc/subgid`). The user is `root (UID 0)` inside the container but mapped to a regular, unprivileged UID (e.g., `UID 10001`) on the host.
- **Local Pods Concept**: Capability to create and manage groups of containers that share the same network (`localhost`), IPC, UTS namespace, and volumes, mirroring Kubernetes Pod semantics:
  ```bash
  # Create a pod with exposed port
  podman pod create --name web-pod -p 8080:80

  # Run container inside the existing pod
  podman run -d --pod web-pod --name nginx-server nginx:alpine
  ```
- **Docker Compatibility**: Full CLI compatibility via the `alias docker=podman` alias and Docker API support through the systemd service socket (`podman.socket`).
- **`podman-compose`**: Execution of Compose specifications without needing the Docker daemon.

### Native systemd Integration & Quadlets

Podman supports generating systemd units (`podman generate systemd`) and adopts **Quadlets** as the modern declarative standard for managing containers as native systemd services.

#### Quadlet File Example (`~/.config/containers/systemd/api-service.container`)
```ini
[Unit]
Description=Production API Microservice
After=network-online.target

[Container]
Image=ghcr.io/myorg/api-service:v1.0.0
ContainerName=api-microservice
AutoUpdate=registry
PublishPort=8080:8080
Environment=NODE_ENV=production
Environment=PORT=8080
Volume=/var/log/app:/app/logs:Z
Network=host
RunInit=true
SecurityLabelDisable=false

[Service]
Restart=always
TimeoutStartSec=900

[Install]
WantedBy=default.target
```

To apply and start:
```bash
systemctl --user daemon-reload
systemctl --user start api-service
systemctl --user status api-service
```

---

## 🔨 4. Buildah & Daemonless Image Building

**Buildah** is a command-line tool specialized in building OCI and Docker images with no running container daemon and no dependence on root privileges.

### What Sets Buildah Apart
- **Isolation and Flexible Scripting**: Lets you build images using traditional shell commands (Bash/Zsh) or via Dockerfiles (`buildah bud`).
- **Absolute `FROM scratch` Construction**: Creation of images starting from a completely empty filesystem, temporarily mounting the image filesystem on the host for surgical injection of binaries and dependencies:
  ```bash
  # Initialize empty container
  new_container=$(buildah from scratch)

  # Mount container filesystem on host
  mount_point=$(buildah mount $new_container)

  # Copy compiled binary and configuration into mounted filesystem
  cp ./my-binary $mount_point/
  chmod 755 $mount_point/my-binary

  # Configure image metadata
  buildah config --entrypoint '["/my-binary"]' $new_container
  buildah config --user 65532:65532 $new_container
  buildah config --created-by "Buildah Script" $new_container

  # Commit image into local storage
  buildah commit --squash $new_container my-minimal-app:latest

  # Unmount and clean temporary container
  buildah unmount $new_container
  buildah rm $new_container
  ```
- **Granular Layer Control**: Explicit control over layer creation (`--layers=false`), enabling layer squashing, OCI annotation inclusion, and maximum reduction of the final image size.

---

## ⚡ 5. CRI-O & Native Runtimes for Kubernetes

**CRI-O** is a lightweight, optimized implementation of Kubernetes' **Container Runtime Interface (CRI)**, designed exclusively to serve as the container runtime on Kubernetes cluster nodes.

### Comparison: CRI-O vs containerd

| Criterion | CRI-O | containerd |
| :--- | :--- | :--- |
| **Primary Focus** | Kubernetes exclusively | General purpose (Kubernetes, Docker, local CLI) |
| **Feature Scope** | Only what is needed to serve the CRI | Broad (plugin support, multi-namespaces, containerd CLI) |
| **Resource Consumption** | Minimal memory and CPU footprint per node | Very low, though slightly more comprehensive |
| **Main Adopters** | Red Hat OpenShift, hardened Kubernetes clusters | EKS, GKE, AKS, standard Kubernetes distributions |
| **Supported OCI Runtimes** | `runc`, `crun` (fast C), `kata-containers` | `runc`, `crun`, `gVisor (runsc)`, `kata` |

### Production Characteristics
- **Alignment with Kubernetes Versions**: Each CRI-O version (e.g., 1.30) rigidly follows the corresponding Kubernetes version (1.30).
- **No Unnecessary Surface**: Eliminates developer CLI abstractions, focusing strictly on security, pod startup performance, and OCI compliance.

---

## ☸️ 6. Kubernetes Containers & Workloads in Production

In Kubernetes, the container is the fundamental unit of execution encapsulated inside **Pods**.

### Pod Spec Anatomy and Lifecycle
- **`initContainers`**: Containers that run sequentially before the application containers start (used for database migrations, dependency waiting, or configuration downloads).
- **`sidecarContainers`** (Native Sidecars): Supported natively from Kubernetes 1.28+ via `restartPolicy: Always` on `initContainers` for network proxies (Envoy/Istio), log collection (Fluentbit), and metric agents.
- **Resource Management (Requests & Limits)**:
  - `requests`: Minimum resources guaranteed by the Kubernetes scheduler for Pod allocation on the node.
  - `limits`: Hard limit imposed by Linux cgroups (CPU throttling when exceeded; OOMKilled if memory exceeds the limit).
  - **Quality of Service (QoS)**: `Guaranteed` (requests = limits), `Burstable` (requests < limits), `BestEffort` (no requests/limits defined).

### Hardening with Security Context & Pod Security Standards (PSS)
- **Pod Security Standards**:
  - `Privileged`: No restrictions (used for system components and CNI).
  - `Baseline`: Prevents known privilege escalation with a minimal configuration.
  - `Restricted`: Maximum hardening level (mandatory non-root, read-only filesystem, drop of all capabilities).

### Practical Example: Hardened Kubernetes Manifest (Deployment & Service)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: microservice-payment
  namespace: production
  labels:
    app.kubernetes.io/name: microservice-payment
    app.kubernetes.io/part-of: checkout-platform
spec:
  replicas: 3
  revisionHistoryLimit: 5
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: microservice-payment
  template:
    metadata:
      labels:
        app: microservice-payment
    spec:
      # Pod-level security context
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
        runAsGroup: 10001
        fsGroup: 10001
        seccompProfile:
          type: RuntimeDefault

      initContainers:
        - name: wait-for-database
          image: busybox:1.36
          command: ['sh', '-c', 'until nc -z -w 2 postgres-service.production.svc.cluster.local 5432; do echo waiting for db; sleep 2; done;']
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop: ["ALL"]
          resources:
            requests:
              cpu: 50m
              memory: 32Mi
            limits:
              cpu: 100m
              memory: 64Mi

      containers:
        - name: payment-api
          image: ghcr.io/myorg/payment-api:v2.1.0@sha256:7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 8080
              name: http-api
              protocol: TCP

          # Container-level security context (Restricted Profile)
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop:
                - ALL
                - NET_RAW

          resources:
            requests:
              cpu: 250m
              memory: 256Mi
            limits:
              cpu: 500m
              memory: 512Mi

          livenessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 15
            timeoutSeconds: 3
            failureThreshold: 3

          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
            timeoutSeconds: 2
            failureThreshold: 2

          volumeMounts:
            - name: tmp-volume
              mountPath: /tmp

      volumes:
        - name: tmp-volume
          emptyDir:
            medium: Memory
            sizeLimit: 64Mi
---
apiVersion: v1
kind: Service
metadata:
  name: payment-service
  namespace: production
spec:
  type: ClusterIP
  selector:
    app: microservice-payment
  ports:
    - name: http
      port: 80
      targetPort: 8080
      protocol: TCP
```

---

## 🏢 7. Container Registries & Versioning Strategies

Registries store, distribute, and control access to OCI container images.

### Main Production Registries
- **GitHub Container Registry (`ghcr.io`)**: Deep integration with GitHub Actions and granular permissions per organization/repository.
- **AWS Elastic Container Registry (ECR)**: Strong integration with IAM, KMS, multi-region replication, and native scanning via Amazon Inspector.
- **Azure Container Registry (ACR)**: Support for private endpoints, global geo-replication, and automated build tasks.
- **Google Artifact Registry (GAR)**: Universal registry on GCP with support for OCI, package repositories (npm, maven, python), and integration with Artifact Analysis.
- **Harbor (Self-Hosted)**: CNCF corporate open-source registry with advanced RBAC, cross-registry replication, signing via Notary/Cosign, auditing, and retention policies.

### Tagging and Immutability Strategies
1. **Avoid `:latest` in Production**: The `latest` tag is mutable and non-deterministic, making reliable rollbacks and traceability impossible.
2. **Semantic Versioning (SemVer)**: Clear tags such as `v1.2.3`, `v1.2`, and `v1`.
3. **Immutability by Git SHA / Commit**: Use of the full or abbreviated commit SHA (e.g., `sha-a1b2c3d`) tied to the CI/CD pipeline.
4. **Digest Pinning (`@sha256:...`)**: The safest format for mission-critical environments, guaranteeing that the exact signed payload is executed regardless of tag mutations.
5. **Multi-Architecture Builds**: Publishing manifest lists with Docker Buildx to support heterogeneous architectures (`linux/amd64`, `linux/arm64`).

```bash
# Multi-platform build and push using Docker Buildx
docker buildx create --name multiarch-builder --use
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t ghcr.io/myorg/api:v1.2.3 \
  -t ghcr.io/myorg/api:latest \
  --push .
```

---

## 🛡️ 8. Container Security, Hardening & Supply Chain

Container security requires a layered approach (*defense-in-depth*), from source code to runtime execution.

### 1. Vulnerability Scanning (Image Scanning)
- **Trivy**: Scanner for OS vulnerabilities, language package dependencies, secrets, and IaC misconfigurations.
  ```bash
  # Scan container image with failure threshold for Critical/High CVEs
  trivy image --severity HIGH,CRITICAL --exit-code 1 ghcr.io/myorg/api:v1.2.3
  ```
- **Grype**: A fast scanner developed by Anchore focused on CVEs mapped in SBOMs.

### 2. SBOM Generation (Software Bill of Materials)
- **Syft**: Creation of structured inventories of components and dependencies in standardized formats (SPDX, CycloneDX).
  ```bash
  # Generate SBOM in CycloneDX JSON format
  syft ghcr.io/myorg/api:v1.2.3 -o cyclonedx-json > sbom.json
  ```

### 3. Cryptographic Signing and Verification (Cosign / Sigstore)
- Digital signing of images in the CI/CD pipeline without manual private-key management (Keyless signing via OIDC):
  ```bash
  # Sign image using Cosign and Sigstore
  cosign sign --yes ghcr.io/myorg/api:v1.2.3

  # Verify image signature before deployment
  cosign verify --certificate-identity-regexp "https://github.com/myorg/.*" \
    --certificate-oidc-issuer "https://token.actions.githubusercontent.com" \
    ghcr.io/myorg/api:v1.2.3
  ```

### 4. Minimal Base Images and Attack Surface Reduction
- **Distroless (`gcr.io/distroless/*`)**: Contains only the application and its direct runtime dependencies, with no shells (`sh`, `bash`), package managers (`apt`, `apk`), or GNU utilities.
- **Scratch**: Empty image (0 bytes), perfect for static binaries compiled in Go, Rust, or C++.
- **Alpine**: Minimalist base (~5MB) based on musl libc and BusyBox (requires attention to glibc compatibility).

### 5. Runtime Hardening
- **Removal of Linux Capabilities**: Drop all capabilities (`drop: ["ALL"]`) and add back only the strictly necessary ones (e.g., `CAP_NET_BIND_SERVICE`).
- **Read-Only Filesystem**: Configure `readOnlyRootFilesystem: true` while mounting volatile directories (`/tmp`, `/run`) on an isolated `emptyDir`.
- **Seccomp & AppArmor/SELinux**: Restrict permitted system calls (syscalls) using the `RuntimeDefault` profile or custom profiles.

---

## ☁️ 9. Cloud Orchestration & Managed / Serverless Containers

Cloud computing offers varied abstraction models for container execution.

### 1. Managed Kubernetes Clusters
- **AWS Elastic Kubernetes Service (EKS)**: Managed control plane, integration with AWS IAM Roles for Service Accounts (IRSA), Pod Identity, and advanced autoscaling with **Karpenter**.
- **Azure Kubernetes Service (AKS)**: Native integration with Microsoft Entra ID (Azure AD), Azure CNI with Cilium, and Azure Linux Nodes.
- **Google Kubernetes Engine (GKE)**: A reference in orchestration with **Standard** and **Autopilot** modes (where Google manages nodes, autoscaling, security hardening, and bin-packing automatically).

### 2. Managed & Serverless Container Services
- **AWS ECS (Elastic Container Service)**: A proprietary orchestrator with high performance and low operational complexity, with support for EC2 nodes or **AWS Fargate** (serverless compute engine).
- **Google Cloud Run**: A Knative-based serverless platform for running event- and HTTP-request-driven containers, with *scale-to-zero* support and billing strictly per millisecond of CPU/memory consumed.
- **Azure Container Apps (ACA)**: A serverless platform for microservices built on Kubernetes, KEDA (event-driven autoscaling), Dapr, and Envoy, ideal for microservices and background workers.

---

## 📋 10. Container Engineering Checklist

When planning, building, or reviewing container-based solutions, validate:

- [ ] **Minimal Base Image**: Does the image use `scratch`, `distroless`, or `alpine` without unnecessary tools?
- [ ] **Non-Root User**: Does the container run with an unprivileged user and group (`runAsNonRoot: true`)?
- [ ] **Multi-Stage Build**: Does the Dockerfile separate the compilation environment from the final production artifact?
- [ ] **Clean Context**: Is the `.dockerignore` file present and does it block secrets, logs, and test files?
- [ ] **Immutability and Tags**: Is the image identified by a semantic version or immutable digest (no `:latest`)?
- [ ] **Vulnerability Verification**: Was the image scanned by tools such as Trivy or Grype in the CI pipeline?
- [ ] **Signing and Provenance**: Does the image have a Cosign signature and an associated SBOM?
- [ ] **Declared Healthchecks**: Are liveness, readiness, and startup probes configured with realistic tolerances?
- [ ] **Resource Limits**: Were CPU and memory `requests` and `limits` defined to avoid contention and starvation in the cluster?
- [ ] **Runtime Hardening**: Does the container run with `readOnlyRootFilesystem: true`, `allowPrivilegeEscalation: false`, and `capabilities.drop: ["ALL"]`?

---

## 🔗 Related Skills

- [devops-engineer](../../roles/devops-engineer/SKILL.md)
- [program-github](../../platforms/program-github-actions/SKILL.md)
- [github-actions](../../platforms/program-github-actions/SKILL.md)
- [devsecops-engineer](../../security/operations/devsecops-engineer/SKILL.md)
