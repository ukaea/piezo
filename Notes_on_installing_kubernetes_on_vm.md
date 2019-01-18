# Running a kubernetes cluster on a virtual machine

## Install kubeadm (Following steps follow procedure in setup.sh)
- Ensure swap is disable `sudo swapoff -a`
- Install docker, note the latest verified version of docker in kubernetes is 18.06
    - `sudo yum install -y yum-utils device-mapper-persistent-data lvm2`
    - `sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo` Download the docker versions
    - `sudo yum install -y docker-ce-18.06.1.ce-3.el7` Install the specific version
    - `sudo systemctl enable docker.service` Enable docker service (required to start minikube)
    - `sudo systemctl start docker.service` Start docker service (Also required to start minikube)

- To install kubeadm need to follow the steps provided on [the kubernetes website](https://kubernetes.io/docs/setup/independent/install-kubeadm/) as an outline this process involves installing the data for `kubeadm`, `kubelet` and `kubectl` and setting SELinux into permissive mode to allow containers to access the host filesystem. It may also be required to set ip tables to 1 to ensure traffic is routed correctly although this didn't seem to be a problem for me but I have included it anyway to be safe. 
    - Creating a repo for kubernetes (note the following lines should all be run together)
      `sudo bash -c 'cat <<EOF > /etc/yum.repos.d/kubernetes.repo`
      `[kubernetes]`
      `name=Kubernetes`
      `baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64`
      `enabled=1`
      `gpgcheck=1`
      `repo_gpgcheck=1`
      `gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg`
      `exclude=kube*`
      `EOF'`
- Set SELinux in permissive mode 
    - `setenforce 0`
    - `sudo sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config`
- Install kubelet, kubeadm and kubectl 
    - `sudo yum install -y kubelet kubeadm kubectl --disableexcludes=kubernetes` 
- Enable and start kubelet
    - `sudo systemctl enable kubelet`
    - `sudo systemctl start kubelet`
- To ensure iptables are set to 1
    - `sudo bash -c 'cat <<EOF >  /etc/sysctl.d/k8s.conf`
      `net.bridge.bridge-nf-call-ip6tables = 1`
      `net.bridge.bridge-nf-call-iptables = 1`
      `EOF'`
sudo sysctl --system
- Note for stability (by avoiding version skewing) need to ensure that versions of `kubelet` and `kubectl` match the version of the kubernetes control panel that you want kudeam to install for you

## Initialising a master node (Follows procedure in initialise_master.sh)
- First need to install a pod network add on, instructions found [here](https://kubernetes.io/docs/setup/independent/create-cluster-kubeadm/#pod-network)
- Choosen to use Weave on recommendation from others. 
- First need to ensure iptables set to 1
    - `sudo sysctl net.bridge.bridge-nf-call-iptables=1`
- install pod network add on (Weave)
    - `sudo kubectl apply -f "https://cloud.weave.works/k8s/net?k8s-version=$(kubectl version | base64 | tr -d '\n')"`
    - note command produces an error saying connection refused but this doesn't seem to affect the intended functionality of the command
    - optionally verify connectivity to gcr.io registries with the command: `sudo kubeadm config images pull`
- Initialise the cluster master 
    - `sudo kubeadm init`
- change access so that everyone talk to the cluster not just the root user 
    - `mkdir -p $HOME/.kube`
    - `sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config`
    - `sudo chown $(id -u):$(id -g) $HOME/.kube/config`
- Now the cluster should be up and running and you should be able to communicate with it using kubectl:
    - `kubectl cluster-info` should return cluster running with the ip address


