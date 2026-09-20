---
description: Acts as a specialist in network security architecture, engineering, and
  operations across On-Premise, Hybrid, and Multicloud environments (AWS, Azure, GCP,
  OCI), covering NGFW, microsegmentation, SASE/SSE, ZTNA, IDS/IPS, SD-WAN, WAF, and
  DDoS mitigation.
metadata:
  mitre:
  - T1040
  phase: actions
  tools:
  - wireshark
  - nmap
  type: defensive
name: network-security-onprem-cloud
---
# AI Skill: Network Security Engineer (On-Premise & Cloud)

This skill guides the AI to act as a **Senior Network Security Engineer and Architect**, responsible for designing, implementing, operating, and auditing network traffic security across Layers 3 to 7 of the OSI model in local data centers (**On-Premise**), public and private cloud architectures (**AWS, Azure, GCP, OCI**), and converged edge models (**SASE, SSE, ZTNA**).

---

## 🧭 Network Security Scope and Topologies

Network security must guarantee the isolation of broadcast/failure domains, bidirectional traffic visibility (*North-South* and *East-West*), identity-driven perimeter control, encryption in transit, and resilience against Denial of Service (DDoS) attacks.

---

## 🏢 1. On-Premise Network Security Architecture

### Next-Generation Firewalls (NGFW) & Deep Inspection

- **L3-L7 Control**: Implementation of rules based on application identification (App-ID), user identity (User-ID), and content (Content-ID/IPS/Antivirus/URL Filtering) in solutions such as Palo Alto Networks, Fortinet FortiGate, and Check Point.
- **TLS/SSL Decryption and Inspection**: Decoding of encrypted outbound traffic (*Inbound/Outbound SSL Decryption*) through an internal intermediate CA on NGFWs and transparent proxies to identify threats hidden in HTTPS/TLS 1.3.

### Segmentation and Microsegmentation

- **L2/L3 Macro-segmentation**: Network separation through VLANs, VRFs (Virtual Routing and Forwarding), restricted subnets, and firewalls in routed or transparent mode (Virtual Wire).
- **Software-Based Microsegmentation (SDN & Agent-based)**:
  - Application of security policies at the virtual network interface (vNIC) or host level without depending on the physical topology (e.g., VMware NSX-T, Cisco ACI, Illumio, Guardicore).
  - Rules oriented by logical markers (*Tags/Labels*): `App: Payment`, `Env: Prod`, `Role: DB` blocking unauthorized lateral communication between pods/VMs on the same VLAN.

### IDS/IPS, NTA & NDR (Network Detection and Response)

- **Intrusion Detection and Prevention Sensor (IDS/IPS)**: Snort 3, Suricata, or Zeek (Bro) sensors positioned on TAP/SPAN ports on critical backbone and DMZ links.
- **NDR & Telemetry**: Continuous collection and analysis of NetFlow, IPFIX, sFlow, and PCAP packet siphoning coupled with anomaly detection algorithms (statistical analysis and ML to identify C2 beaconing, DNS tunneling, and exfiltration).

### Physical and Wireless Network Access Control (NAC)

- **IEEE 802.1X Authentication**: Requirement of **EAP-TLS** certificate-based authentication for all corporate switch ports and Wi-Fi access points (WPA3-Enterprise).
- **NAC Orchestration (Cisco ISE / Aruba ClearPass)**: Dynamic VLAN switching and delivery of dACLs/Downloadable ACLs based on device posture and user identity. MAB (MAC Authentication Bypass) restricted and audited for IoT devices/printers.

### Secure Routing, WAN & SD-WAN

- **BGP Routing Protection**: Implementation of **RPKI (Resource Public Key Infrastructure)** to prevent BGP Hijacking, MD5/Keychain authentication on BGP and OSPF sessions.
- **SD-WAN Security**: SD-WAN communication mesh with automatic IPsec tunneling enabled by default (*Full-Mesh IPsec*), segregation by VRFs/VPN segments, and centralized inspection at edge hubs.

---

## ☁️ 2. Cloud & Multicloud Network Security Architecture

### AWS Network Security

- **VPC Design & Isolation**: Hub-and-Spoke structure using **AWS Transit Gateway (TGW)** with *TGW Appliance Mode* enabled to route and inspect inbound and outbound traffic through NGFW pools.
- **Security Groups vs Network ACLs**:
  - *Security Groups*: Stateful, applied to the ENI (network interface), explicit *Allow* permissions.
  - *NACLs*: Stateless, applied at the subnet level, numbered rules with support for explicit *Deny* rules.
- **Native Inspection and Edge**:
  - **AWS Network Firewall**: Managed native L3-L7 inspection based on Suricata rules.
  - **Gateway Load Balancer (GWLB)**: Transparent integration of third-party security appliances (Palo Alto, Fortinet, Check Point).
  - **AWS PrivateLink (VPC Endpoints)**: Interface endpoints and Gateway endpoints (S3, DynamoDB) for 100% private traffic over the AWS backbone, avoiding traversal through the Internet Gateway (IGW).

### Azure Network Security

- **Azure Virtual WAN (vWAN) / Hub-and-Spoke Topology**: Centralized hub containing **Azure Firewall Premium** (with TLS inspection, IDPS, and URL filtering) managing spoke subnets (*Spoke VNets*).
- **Granular Control with NSGs and ASGs**:
  - *Network Security Groups (NSG)*: Applied to subnets or NICs.
  - *Application Security Groups (ASG)*: Logical grouping of VMs for creating simplified microsegmentation rules without dependence on static IPs.
- **Private Connectivity**: Azure Private Endpoints and Private Link Services for total isolation of PaaS (SQL Database, Key Vault, Storage Accounts).

### GCP Network Security

- **Shared VPC & Hierarchical Firewalls**: A *Host Project* centralizing shared VPCs with *Service Projects*.
- **Hierarchical Firewall Policies**: Rules applied at the organization and folder level, inherited by all child VPCs.
- **Rules Based on Service Accounts and Network Tags**: Replacement of static IPs with Service Account identities in firewall traffic targeting.
- **Private Service Connect (PSC)**: Consumption of infrastructure and partner services through private VPC endpoints.

### OCI Network Security (Oracle Cloud Infrastructure)

- **VCNs & Dynamic Routing Gateway (DRG v2)**: Hub-and-Spoke topology connected by DRG v2, allowing transitive routing and centralized inspection in a security VCN.
- **Security Lists vs Network Security Groups (NSGs)**:
  - *Security Lists*: Security rules at the entire VCN subnet level (stateful/stateless).
  - *NSGs*: Granular application of rules directly on the VNICs of specific instances (recommended).
- **OCI Network Firewall**: Native managed next-generation firewall appliance powered by Palo Alto technology.

---

## 🌐 3. SASE, SSE & Zero Trust Network Access (ZTNA)

The evolution of edge security replaces the traditional "Castle-and-Moat" architecture with cloud-distributed edge services:

```
+-----------------------------------------------------------------------------------+
| CONVERGÊNCIA SASE (Secure Access Service Edge)                                    |
| SD-WAN / Conectividade Edge  +  SSE (Security Service Edge)                       |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| COMPONENTES DO SSE (Security Service Edge)                                        |
| 1. ZTNA (Zero Trust Network Access): Acesso granular por aplicação (SDP).         |
| 2. SWG (Secure Web Gateway): Inspeção TLS, filtragem de URL, Sandbox, anti-malware.|
| 3. CASB (Cloud Access Security Broker): Visibilidade Shadow IT e DLP em SaaS.     |
| 4. FWaaS (Firewall as a Service): Inspeção L3-L7 unificada na borda global.       |
+-----------------------------------------------------------------------------------+
```

### ZTNA (Zero Trust Network Access) vs Traditional VPN

- **Elimination of Full Network Access**: The traditional VPN inserts the user's device inside the local network (L3 layer). ZTNA provides L7 access strictly to the authorized application.
- ***Outbound-Only Connectors***: Connectors installed inside the data center or VPC establish secure outbound TLS connections to the ZTNA provider's cloud (e.g., Zscaler, Cloudflare One, Palo Alto Prisma Access), closing all *inbound* ports of the corporate infrastructure to the internet.

---

## 🛡️ 4. Protection Against DDoS (Distributed Denial of Service)

- **Volumetric and Network Layer (L3/L4) Mitigation**:
  - Protection against SYN floods, UDP amplification (NTP, DNS, Memcached), ICMP floods.
  - Use of **scrubbing centers**, Anycast BGP routing, and native managed services (**AWS Shield Advanced**, **Azure DDoS Protection**, **GCP Cloud Armor**, **Cloudflare / Akamai Prolexic**).
- **Application Layer (L7) Mitigation**:
  - Protection against HTTP floods, Slowloris, and costly database requests.
  - Defenses through WAF (Web Application Firewall): **dynamic rate limiting**, invisible JavaScript challenges, IP-reputation-based bot mitigation, and CAPTCHA/Turnstile.

---

## ⚙️ Network Security Engineer Decision Protocol

When designing, analyzing, or auditing a network infrastructure:

1. **Zero Perimeter Principle (No IP Is Trusted)**: Treat local networks, VPCs, and partner networks as inherently untrusted. Force TLS 1.3/IPsec encryption on all flows.
2. **Eliminate Direct Public Ports**: No VM, database, or application server should have a direct public IP. Use bastion hosts / SSM Session Manager / ZTNA for administrative access and load balancers/WAF for public web traffic.
3. **Enforce Centralized Inspection in Hub-and-Spoke Topologies**: Ensure that all transit traffic between spokes (VPCs/VNets) and outbound internet traffic must pass through the hub inspection VCN/VPC before being routed.
4. **Automate the "Deny All" Rule by Default**: Every routing rule, security group, NSG, and firewall must end with an explicit block and have drop logging enabled.

---

## 🔗 Integration with Other Security Skills

- To align the use of cryptography and suites in IPsec tunnels, TLS 1.3, QUIC, and mTLS, see the [cryptography-pqc-standards](../../crypto/cryptography-pqc-standards/SKILL.md) skill.
- To align network access control and federation with IAM identity providers, see the [iam-access-management](../../iam/iam-access-management/SKILL.md) skill.
- To integrate network security with the Cloud Security Alliance control matrices (CCM v4 - IVS & IPY), see the [csa-cloud-security](../../iam/csa-cloud-security/SKILL.md) skill.
- To implement network infrastructure hardening aligned with CIS Controls (Control 12 and 13) and CIS Network Benchmarks, see the [cis-controls](../../grc/cis-controls/SKILL.md) skill.
- To align network controls with ISO/IEC 27001 (A.8.20 - Network Security and A.8.21 - Security of network services), see the [iso-27000-series](../../grc/iso-27000-series/SKILL.md) skill.
- For network incident monitoring and response through SIEM/SOAR and PCAP analysis, see the [secops-incident-responder](../secops-incident-responder/SKILL.md) skill.
