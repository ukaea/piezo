## Things that didn't work

* Weave and Ubuntu don't work well together. Causes many issues that aren't necessarilly all resolvable. At least not easily.
* Networking on Kubernetes is hard
* Most pre-given kubernetes set-ups require ansible installed for provisoning multiple machines simultaneously. This is important as when you create the cluster you need to generate a token on the master then use the token from each of the nodes and thenn further set-up such as installing a kubernetes operator (e.g Helm) require being back on the master node once other nodes have successfully joined. Ansible is not comnpatable with windows. Tried provisioning via a linux host machine but then have multiple issues with networking again as require all machines to talk to each other with correct permissions. 
*  Running spark independently on the cluster. Running spark without using an operator fails as other nodes don't have pull access for docker daemon. Need to have the proxy running to have permission to try and run the spark application.
* Building the docker image on each node indepently allowed the program to bypass the pull permissions but then failed as the driver can't set up worker pods. Also required spark installed all each machine to use the build docker image tool. Issue seems to be with the kubernetes DNS not being properly configured
* Networking issues remained on ubuntu with Flannel in particular were unable to properly set up helm. Also often the pods hung on joining the cluster. 
* ReadWriteMany access type, PersistentVolumes that are backed by Compute Engine persistent disks are not supported
* Creating a nfs file system across the nodes of the virtual machine to test the volume mounts to work with data from. This seems to be due to networking issues in particular IP table issues. As Ip tables have to be set to 1 (0 is their default) for kubernetes this could be an issue that is causing the problem. Error on the worker node is: `mount.nfs: access denied by server while mounting 172.28.128.10:/nfs_mnt` which is caused when running `sudo mount 172.28.128.10:/nfs_mnt /nfs_mnt`. Also get  `node1-k8s kernel: xt_physdev: using --physdev-out in the OUTPUT, FORWARD and POSTROUTING chains for non-bridged traffic is not supported anymore` when writing out the system logs


## Things that did work
* Running example spark programs with the spark operator
* Weave on Centos
* Running spark applications through Helm
* Require resonable resource allocation. Can take time to free up enough resources even to run example task with current set up of 2cpus and 2GB memory per a node. 
* Using vagrantfile to ensure Kubernetes service traffic is routed over ethp0s. This helped solve many of the networking issues
* Using ansible local to provision the master machine first and saving a join token to be read by the worker nodes which are provisioned next. (Note join tokens expire after 24 hours)
* Joining nodes is relatively easy although with old scripts (Kubernetes_with_ansible folder) often hung on joining nodes. Believe this was an issue with flannel. Nodes much also have weave applied to become ready. Need to ensure this is properly configured before joining or apply after joining
* copying `/etc/kubernetes/admin.conf` to `~/.kube/` allows all users to use kubectl as compared to having to add the configuration to the path each time loading the machine (`export KUBECONFIG=/etc/kubernetes/admin.conf`)
* Creating rbac and cluster role binding accounts can be used to control access to the cluster and ability to run programs
* By transferring the config file from master to .kube folder locally can access kubectl control of cluster from laptop
* Running kubectl proxy on the cluster can then use browser to interact with the cluster
* Running a web app from within the cluster allows control from browser via the proxy
* Can view the api paths in a browser with `http://localhost:8001/apis/sparkoperator.k8s.io`