# Golden Images Examples

These are conditional operational examples, not universal provider choices. Version pins inherited from the source are not verified as current by this update; resolve the selected platform documentation before use. Authorization, secrets and release verification follow the parent skill and repository standards.

## 🖥️ 5. Virtual Machine Management & Golden Images

Although containers dominate ephemeral workloads, **Virtual Machines (VMs)** are the foundation for hypervisors, bare-metal databases, Kubernetes clusters (control plane / worker nodes), and workloads requiring strict kernel isolation.

### 📊 Comparison: Virtual Machines vs Containers

| Characteristic | Virtual Machines (VMs) | Containers (Docker / Podman) |
| :--- | :--- | :--- |
| **Isolation** | Hypervisor (Hardware-level / Type 1 or 2) | Namespaces and cgroups (OS-level) |
| **Kernel** | Own independent kernel per VM | Shared with the Host OS |
| **Boot Time** | Seconds to minutes | Milliseconds to seconds |
| **Overhead / Footprint** | GBs of storage and dedicated RAM | MBs to GBs, sharing layers |
| **Use Cases** | Kubernetes host, legacy DBs, strict multi-tenant | Microservices, CI jobs, stateless APIs |

### 🍞 Image Baking with HashiCorp Packer (HCL2)

```hcl
# ubuntu-golden-image.pkr.hcl
packer {
  required_plugins {
    amazon = {
      version = ">= 1.2.8"
      source  = "github.com/hashicorp/amazon"
    }
  }
}

source "amazon-ebs" "ubuntu_golden" {
  ami_name      = "golden-ubuntu-2204-base-{{timestamp}}"
  instance_type = "t3.medium"
  region        = "us-east-1"

  source_ami_filter {
    filters = {
      name                = "ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"
      root-device-type    = "ebs"
      virtualization-type = "hvm"
    }
    most_recent = true
    owners      = ["099720109477"] # Canonical
  }

  ssh_username = "ubuntu"
  tags = {
    OS          = "Ubuntu 22.04"
    BaseAMI     = "GoldenImage"
    ManagedBy   = "Packer"
    Environment = "Core"
  }
}

build {
  name    = "build-golden-ami"
  sources = ["source.amazon-ebs.ubuntu_golden"]

  provisioner "shell" {
    inline = [
      "export DEBIAN_FRONTEND=noninteractive",
      "sudo apt-get update && sudo apt-get upgrade -y",
      # Ubuntu-family image (source.amazon-ebs.ubuntu_golden): `apt`, right here.
      # Another family needs its own manager and its own package names.
      "sudo apt-get install -y fail2ban auditd awscli jq curl unattended-upgrades",
      "sudo systemctl enable fail2ban auditd"
    ]
  }

  provisioner "ansible" {
    playbook_file = "./ansible/hardening-playbook.yml"
    user          = "ubuntu"
  }
}
```

### ☁️ Initial Customization via Cloud-Init

```yaml
#cloud-config
package_upgrade: true
packages:
  - curl
  - jq
  - htop
  - docker.io

users:
  - name: devops
    groups: sudo, docker
    shell: /bin/bash
    sudo: ['ALL=(ALL) NOPASSWD:ALL']
    ssh_authorized_keys:
      - ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIExampleKeyDevOpsEngineer123456

write_files:
  - path: /etc/docker/daemon.json
    content: |
      {
        "log-driver": "json-file",
        "log-opts": {
          "max-size": "100m",
          "max-file": "3"
        }
      }
    permissions: '0644'

runcmd:
  - systemctl restart docker
  - ufw default deny incoming
  - ufw default allow outgoing
  - ufw allow 22/tcp
  - ufw enable
```

---
