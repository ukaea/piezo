# Setup a Kubernetes cluster

This guide describes how to provision a small Kubernetes cluster on a single machine for development purposes.

## Requirements

* [Vagrant](https://www.vagrantup.com/)
* [VirtualBox](https://www.virtualbox.org/)
* At least 8GB RAM
* At least 20GB storage

## Provisioning

In a console on your local machine, navigate to the `alc-kubernetes-spark` directory and run:
```
vagrant up
```

This creates 3 Virtual Machines (VMs) running [CentOS](https://www.centos.org/) 7:
* one named `master-k8s`, configured as the Kubernetes master node
* two named `node1-k8s` and `node2-k8s`, configured as the Kubernetes worker nodes

These machines are provisioned via [Ansible](https://www.ansible.com/) and then connected via [Weave](https://www.weave.works/docs/net/latest/overview/) to produce a running Kubernetes cluster.

To confirm that the cluster is fully connected, SSH into the master VM and ask Kubelet for the cluster status:
```
vagrant ssh master-k8s
kubectl get nodes
```

The response should look like this:
```
NAME         STATUS   ROLES    AGE   VERSION
master-k8s   Ready    master   1h    v1.13.2
node1-k8s    Ready    <none>   1h    v1.13.2
node2-k8s    Ready    <none>   1h    v1.13.2
```

Nodes may take a few minutes to become ready (their status will show as `NotReady` before then) so you may need to wait a little while after first booting up the system.


## Configure for spark applications

To configure our kubernetes cluster to run spark applications we will use helm to install a spark-operator.

From within your `master-k8s` VM navigate to `~/code` and run:
```
./install_spark_operator.sh
```

To check the installation was completed successfully run `kubectl get pods --all-namespaces` and check you have a pod containing the name spark-operator that has the status `running`. Now your machine is provisioned to run spark applications as outlined in [Running_examples.md](https://github.com/ukaea/piezo/blob/master/Docs/Running_examples.md). 

The cluster can be configured further to allow extraction of metrics about the cluster and from spark applications by following the instructions in [prometheus.md](https://github.com/ukaea/piezo/blob/master/Docs/prometheus.md).

Note certain jobs will require settign up a local docker registory which can be achieved by following the instructions in [Setting_up_a_docker_registory.md](https://github.com/ukaea/piezo/blob/master/Docs/Setting_up_a_docker_registory.md)
