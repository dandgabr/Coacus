# Vagrant Examples

These are conditional operational examples, not universal provider choices. Version pins inherited from the source are not verified as current by this update; resolve the selected platform documentation before use. Authorization, secrets and release verification follow the parent skill and repository standards.

## 💻 3. Local Development Environments with Vagrant

Vagrant lets you provision reproducible, portable development environments locally, integrating with hypervisors (VirtualBox, VMware, Libvirt, Hyper-V).

### ⚙️ Multi-Machine Vagrantfile with Shell and Ansible Provisioning

```ruby
# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/jammy64"
  config.vm.box_check_update = true

  # Global synced folder
  config.vm.synced_folder "./app", "/var/www/app", type: "nfs", mount_options: ["actimeo=1"]

  # Global VM provider configuration
  config.vm.provider "virtualbox" do |vb|
    vb.gui = false
    vb.linked_clone = true
  end

  # Node 1: Web Application Server
  config.vm.define "app-node" do |app|
    app.vm.hostname = "app-node.local"
    app.vm.network "private_network", ip: "192.168.56.10"
    app.vm.network "forwarded_port", guest: 80, host: 8080, auto_correct: true

    app.vm.provider "virtualbox" do |vb|
      vb.memory = "2048"
      vb.cpus = 2
    end

    # Bootstrap with shell provisioner
    app.vm.provision "shell", inline: <<-SHELL
      export DEBIAN_FRONTEND=noninteractive
      # Ubuntu-family guest (the box is Ubuntu): `apt`, right here. Not
      # copy-pasteable to another family — manager and package names both differ.
      apt-get update && apt-get install -y curl ufw git
      ufw allow 80/tcp
    SHELL

    # Configure using Ansible Local provisioner
    app.vm.provision "ansible_local" do |ansible|
      ansible.playbook = "ansible/site.yml"
      ansible.install_mode = "pip"
    end
  end

  # Node 2: Database Server
  config.vm.define "db-node" do |db|
    db.vm.hostname = "db-node.local"
    db.vm.network "private_network", ip: "192.168.56.11"

    db.vm.provider "virtualbox" do |vb|
      vb.memory = "1024"
      vb.cpus = 1
    end

    db.vm.provision "shell", inline: <<-SHELL
      # Ubuntu-family guest (the box is Ubuntu): `apt`, right here. Not
      # copy-pasteable to another family — manager and package names both differ.
      apt-get update && apt-get install -y postgresql postgresql-contrib
      systemctl enable --now postgresql
    SHELL
  end
end
```

---
