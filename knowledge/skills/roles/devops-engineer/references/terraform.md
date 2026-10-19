# Terraform Examples

These are conditional operational examples, not universal provider choices. Version pins inherited from the source are not verified as current by this update; resolve the selected platform documentation before use. Authorization, secrets and release verification follow the parent skill and repository standards.

## 🏗️ 1. Infrastructure as Code (IaC) with Terraform

Terraform is the industry-standard tool for declarative provisioning of multi-cloud infrastructure. Code design must prioritize modularity, immutability, and state isolation.

### 📁 Module Directory Structure
A professional architecture separates reusable modules from environment definitions (*live/environments*):

```text
terraform-architecture/
├── modules/
│   └── vpc/
│       ├── main.tf
│       ├── variables.tf
│       ├── outputs.tf
│       └── versions.tf
└── environments/
    ├── dev/
    │   ├── backend.tf
    │   ├── main.tf
    │   ├── terraform.tfvars
    │   └── variables.tf
    └── prod/
        ├── backend.tf
        ├── main.tf
        ├── terraform.tfvars
        └── variables.tf
```

### 🔒 Remote State with S3 and DynamoDB (AWS)
Remote state storage guarantees safe collaboration with concurrent *state locking*.

```hcl
# environments/prod/backend.tf
terraform {
  required_version = ">= 1.7.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.40.0"
    }
  }

  backend "s3" {
    bucket         = "company-terraform-state-prod"
    key            = "core-infra/vpc/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "company-terraform-locks-prod"
  }
}
```

### 📦 Reusable VPC Module Example

```hcl
# modules/vpc/variables.tf
variable "vpc_cidr" {
  description = "The CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"

  validation {
    condition     = can(cidrnetmask(var.vpc_cidr))
    error_message = "The vpc_cidr must be a valid CIDR block."
  }
}

variable "environment" {
  description = "Deployment environment name"
  type        = string
}

variable "public_subnet_cidrs" {
  description = "List of public subnet CIDR blocks"
  type        = list(string)
}

variable "private_subnet_cidrs" {
  description = "List of private subnet CIDR blocks"
  type        = list(string)
}

variable "availability_zones" {
  description = "List of availability zones to distribute subnets"
  type        = list(string)
}
```

```hcl
# modules/vpc/main.tf
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "vpc-${var.environment}"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name        = "igw-${var.environment}"
    Environment = var.environment
  }
}

resource "aws_subnet" "public" {
  count                   = length(var.public_subnet_cidrs)
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidrs[count.index]
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name        = "subnet-${var.environment}-public-${count.index + 1}"
    Environment = var.environment
    Type        = "Public"
  }
}

resource "aws_subnet" "private" {
  count             = length(var.private_subnet_cidrs)
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_cidrs[count.index]
  availability_zone = var.availability_zones[count.index]

  tags = {
    Name        = "subnet-${var.environment}-private-${count.index + 1}"
    Environment = var.environment
    Type        = "Private"
  }
}
```

```hcl
# modules/vpc/outputs.tf
output "vpc_id" {
  description = "Identifier of the created VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "List of IDs for public subnets"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "List of IDs for private subnets"
  value       = aws_subnet.private[*].id
}
```

### 🔄 Lifecycle and Drift Detection
1. **Validation and Formatting**:
   ```bash
   terraform fmt -recursive
   terraform validate
   ```
2. **Safe Execution in CI**:
   ```bash
   terraform plan -out=tfplan.binary
   terraform apply tfplan.binary
   ```
3. **Drift Detection on a Cron Schedule**:
   ```bash
   # Exit code 2 indicates a drift occurred
   terraform plan -detailed-exitcode -no-color
   ```

---

