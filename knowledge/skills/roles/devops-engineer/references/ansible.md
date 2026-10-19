# Ansible Examples

These are conditional operational examples, not universal provider choices. Version pins inherited from the source are not verified as current by this update; resolve the selected platform documentation before use. Authorization, secrets and release verification follow the parent skill and repository standards.

## ⚙️ 2. Configuration Management & Automation with Ansible

Ansible provides *agentless* automation over SSH/WinRM, guaranteeing **idempotency** in configuring operating systems and applications.

### 📐 Directory Structure and Roles

```text
ansible-project/
├── ansible.cfg
├── inventory/
│   ├── production/
│   │   ├── hosts.yml
│   │   └── group_vars/
│   │       ├── all.yml
│   │       └── webservers.yml
│   └── staging/
│       └── hosts.yml
├── roles/
│   └── webserver/
│       ├── defaults/main.yml
│       ├── tasks/main.yml
│       ├── handlers/main.yml
│       ├── templates/nginx.conf.j2
│       └── vars/main.yml
└── site.yml
```

### 🏷️ Variable Precedence and Ansible Vault
Ansible's precedence order ranges from role defaults (lowest priority) to command-line arguments (`-e`, highest priority).

To encrypt secrets:
```bash
# Encrypt a secret variable
ansible-vault encrypt_string --vault-password-file .vault_pass 'supersecretpassword' --name 'db_password'

# Run playbook with vault file
ansible-playbook -i inventory/production/hosts.yml site.yml --vault-password-file .vault_pass
```

### 📄 Idempotent Playbook and Role Example

```yaml
# inventory/production/hosts.yml
all:
  children:
    webservers:
      hosts:
        web-node-01.internal:
          ansible_host: 10.0.10.21
        web-node-02.internal:
          ansible_host: 10.0.10.22
      vars:
        http_port: 80
        server_name: api.production.internal
```

```yaml
# roles/webserver/tasks/main.yml
---
# Install and configure NGINX web server
- name: Ensure NGINX package is installed
  ansible.builtin.package:
    name: nginx
    state: present

- name: Deploy NGINX configuration from template
  ansible.builtin.template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
    owner: root
    group: root
    mode: '0644'
  notify: Restart NGINX service

- name: Ensure NGINX service is enabled and running
  ansible.builtin.service:
    name: nginx
    state: started
    enabled: true

- name: Deploy web root content
  ansible.builtin.copy:
    content: "OK - Managed by Ansible\n"
    dest: /var/www/html/healthz
    owner: www-data
    group: www-data
    mode: '0644'
```

```yaml
# roles/webserver/handlers/main.yml
---
- name: Restart NGINX service
  ansible.builtin.service:
    name: nginx
    state: restarted
```

```yaml
# site.yml
---
- name: Configure Production Web Fleet
  hosts: webservers
  become: true
  roles:
    - role: webserver
```

---

