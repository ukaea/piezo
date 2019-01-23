Vagrant.configure("2") do |config|
  config.ssh.forward_agent = true

  #   Due to a Vagrant bug, enp0 stays down on boot on CentOS 7
  #   Here, we make sure it starts on each boot
  #   See https://github.com/mitchellh/vagrant/issues/8166
  config.vm.provision :shell, run: "always", inline: <<-SHELL
    set -ex
    ifup enp0s8
  SHELL

  # Make sure Kubernetes service traffic is routed over ethp0s
  # This is only necessary because ethp0s is not the default interface
  # We can't just make ethp0s the default interface because it won't route traffic to the internet
  config.vm.provision :shell, inline: <<-SHELL
    set -exo pipefail
    my_ip="$(ip addr show enp0s8 | grep "inet " | awk '{ print $2; }' | cut -d "/" -f 1)"
    echo "10.96.0.0/12 via ${my_ip} dev enp0s8" > /etc/sysconfig/network-scripts/route-enp0s8
    # For some reason, the first restart sometimes, but not always, refuses to pick up the new route
    # Running two restarts together seems to make this more reliable...
    systemctl restart network
    systemctl restart network
    ip route list
  SHELL

  config.vm.define "master-k8s" do |control|
    control.vm.box = "gugek/scientific-linux-7"
    control.vm.box_version = "7.2.0"

    control.vm.synced_folder "code", "/home/vagrant/code"
    control.vm.network :private_network, ip: "172.28.128.10"
    control.vm.hostname = "master-k8s"

    control.vm.provider "virtualbox" do |vb|
      vb.memory = 2048
      vb.cpus = 2
    end

    control.vm.provision "ansible_local" do |ansible|
      ansible.playbook = "playbook.yml"
    end
  end

  config.vm.define "node1-k8s" do |worker1|
    worker1.vm.box = "gugek/scientific-linux-7"
    worker1.vm.box_version = "7.2.0"

    worker1.vm.synced_folder "code", "/home/vagrant/code"
    worker1.vm.network :private_network, ip: "172.28.128.11"
    worker1.vm.hostname = "node1-k8s"

    worker1.vm.provider "virtualbox" do |vb|
      vb.memory = 2048
      vb.cpus = 2
    end

    worker1.vm.provision "ansible_local" do |ansible|
      ansible.playbook = "playbook.yml"
    end
  end

  config.vm.define "node2-k8s" do |worker2|
    worker2.vm.box = "gugek/scientific-linux-7"
    worker2.vm.box_version = "7.2.0"

    worker2.vm.synced_folder "code", "/home/vagrant/code"
    worker2.vm.network :private_network, ip: "172.28.128.12"
    worker2.vm.hostname = "node2-k8s"

    worker2.vm.provider "virtualbox" do |vb|
      vb.memory = 2048
      vb.cpus = 2
    end

    worker2.vm.provision "ansible_local" do |ansible|
      ansible.playbook = "playbook.yml"
    end
  end
end
