systemctl disable firewalld && systemctl stop firewalld

sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
./install-kubernetes-repo.sh

yum install -y docker-ce-18.06.1.ce kubelet kubeadm kubectl kubernetes-cni

systemctl enable docker && systemctl start docker
systemctl enable kubelet && systemctl start kubelet

sysctl -w net.bridge.bridge-nf-call-iptables=1
echo "net.bridge.bridge-nf-call-iptables=1" > /etc/sysctl.d/k8s.conf

swapoff -a && sed -i '/ swap / s/^/#/' /etc/fstab

./update-hosts-file.sh

#route add 10.96.0.1 gw 172.28.128.10