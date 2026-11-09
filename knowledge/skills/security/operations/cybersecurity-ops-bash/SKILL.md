---
name: cybersecurity-ops-bash
description: "Techniques and command-line automation for defensive and offensive security operations using POSIX bash, based on Troncone & Albing's Cybersecurity Ops with bash. Covers defensive log parsing, automated integrity monitoring, network reconnaissance with native sockets, memory/process analysis, baseline drift detection, and lightweight security telemetry pipelines."
---

# Cybersecurity Operations with Bash

This skill provides practical command-line techniques, scripting patterns, and pipeline automation for security analysts, incident responders, and penetration testers using native POSIX **Bash** and core utilities.

---

## 🔍 1. Defensive Log Analysis and Anomaly Detection

Parsing high-volume web, authentication, and system logs without third-party agents:

### 1.1 Web Access Log Triage
```bash
# Identify top IP addresses generating 4xx and 5xx errors (brute force / scanning)
awk '($9 ~ /^(4|5)/) {print $1}' /var/log/nginx/access.log | \
    sort | uniq -c | sort -nr | head -n 20

# Detect potential SQL injection patterns in HTTP GET query strings
grep -Ei "(union.*select|order.*by|--|char\(|waitfor.*delay|information_schema)" /var/log/nginx/access.log
```

### 1.2 Linux Authentication Auditing
```bash
# Detect failed SSH authentication bursts (IP and attempted username)
grep "Failed password" /var/log/auth.log | \
    awk '{for(i=1;i<=NF;i++) if($i=="for") user=$(i+1); if($i=="from") ip=$(i+1)} {print ip, user}' | \
    sort | uniq -c | sort -nr | head -n 15
```

---

## 🕵️ 2. Live Host Triage and Process Telemetry

Capturing volatile host state during initial incident response:

```bash
# Verify process binaries deleted on disk but running in RAM (common in malware/injections)
ls -l /proc/*/exe 2>/dev/null | grep "\(deleted\)"

# Find hidden listening sockets using native bash /dev/tcp (without netstat/ss)
for port in {20..1024}; do
    (echo >/dev/tcp/127.0.0.1/$port) >/dev/null 2>&1 && echo "Open: $port"
done
```

### 2.1 File Integrity Baseline Verification
```bash
# Generate baseline cryptographic manifests of critical system binaries
find /bin /sbin /usr/bin /usr/sbin -type f -exec sha256sum {} + > /opt/sec/baseline.sha256

# Drift detection audit (flag modified, added, or missing binaries)
sha256sum -c /opt/sec/baseline.sha256 2>&1 | grep -v ": OK$"
```

---

## 🛡️ 3. Robust Scripting Standards for Security Tools

1. **Strict Shell Options**: Always start operational scripts with `set -euo pipefail` and `IFS=$'\n\t'` to prevent silent failures.
2. **Safe Temporary Files**: Generate temporary file descriptors via `mktemp` with immediate trap cleanup:
   ```bash
   TMPDIR=$(mktemp -d -t sec-triage.XXXXXX)
   trap 'rm -rf "$TMPDIR"' EXIT
   ```
3. **Privilege Awareness**: Validate effective user ID before running commands that require root capabilities (`[ "$EUID" -eq 0 ]`).
