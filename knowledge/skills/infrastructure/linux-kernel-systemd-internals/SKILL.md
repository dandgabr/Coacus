---
name: linux-kernel-systemd-internals
description: Provides patterns for Linux kernel architecture, the systemd init subsystem, and advanced server administration based on systemd for Linux SysAdmins (David Both) and Understanding Linux Kernel Development. Covers unit management (.service, .socket, .timer, .mount), cgroups v2, journald, namespaces, kernel networking (Netfilter, eBPF, sockets), and sysctl performance tuning.
---

# Linux Kernel, systemd, and Advanced System Administration

This skill establishes the standards and practices for Linux operating-system engineering, service management through **systemd**, resource control with **cgroups v2**, and network/kernel tuning documented by **David Both**, **Lincoln Boucher**, and **Christian Benvenuti**.

---

## 🐧 1. systemd Architecture and Unit Types

```
┌─────────────────────────────────────────────────────────────┐
│                          systemd (PID 1)                    │
├──────────────┬──────────────┬──────────────┬────────────────┤
│   .service   │   .socket    │    .timer    │     .mount     │
│ (Daemons e   │ (Ativação    │ (Agendamento │ (Pontos de     │
│  Processos)  │  por Rede)   │  preciso)    │  Montagem)     │
└──────────────┴──────────────┴──────────────┴────────────────┘
```

### Anatomy of a Secure Service (`/etc/systemd/system/myapp.service`)
```ini
[Unit]
Description=Plataforma de Microsserviço de Alta Disponibilidade
After=network.target postgresql.service
Requires=postgresql.service

[Service]
Type=notify
ExecStart=/usr/local/bin/myapp --config /etc/myapp/config.yaml
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
RestartSec=5s

# Hardening e Isolamento de Segurança
User=appuser
Group=appgroup
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
PrivateTmp=true
PrivateDevices=true
ProtectKernelModules=true
ProtectKernelTunables=true
ProtectControlGroups=true
RestrictRealtime=true
MemoryMax=2G
CPUQuota=200%

[Install]
WantedBy=multi-user.target
```

---

## ⚙️ 2. Kernel Performance Tuning (`/etc/sysctl.d/99-custom.conf`)

| Sysctl Parameter | Recommended Value | Purpose |
| :--- | :--- | :--- |
| `net.core.somaxconn` | `65535` | Increases the size of the pending-connection queue for the TCP listener. |
| `net.ipv4.tcp_max_syn_backlog` | `65535` | Protects against traffic spikes and SYN floods. |
| `net.ipv4.ip_local_port_range` | `1024 65535` | Expands the ephemeral port range for outbound connections. |
| `vm.swappiness` | `10` | Avoids aggressive swap use, preserving RAM for cache. |
| `fs.file-max` | `2097152` | Global limit of open file descriptors. |
