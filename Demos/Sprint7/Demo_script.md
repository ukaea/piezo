### Items included
* Setting up a kubernetes cluster on openstack
* Monitoring with Prometheus and Grafana
* Setting up ingress rules
* Infrastructure to containerise a web app
* Deploying web app on openstack and sending commands via ingress

### Pre demo 
1. Connect to the STFC VPN
2. Ensure that you have kubectl installed and the config file for the cluster on STFC (in slack channel) saved in your `C:Users/{username}/.kube` directory as `config`
3. Run `kubectl get nodes` to ensure that `kubectl` is correctly configured to the openstack cluster. Expect to see the 3 nodes all running and ready. If don't get a response then manually set the environment variable for `KUBECONFIG` to the config file you have for the STFC cluster and retry. If experiencing issues use the config file for a local kubernetes cluster
4. 

# Setting up a kubernetes cluster on openstack
1. Mention have set up a cluster on openstack (with more resources) and continuing development there
2. Show config file in `C:\Users\taro\.kube` pointing to the STFC cluster
3. Explain how this allows control of cluster remotely
4. Run `Kubectl get nodes` to show the nodes running
5. Navigate to `https://openstack.stfc.ac.uk/project/instances/` and show the nodes running
6. Run `kubectl get pods --all-namespaces` and talk through pods showing same state as last time on local cluster

# Ingress rules and monitoring with Prometheus and Grafana
1. Explain what ingress does (allows access into the cluster and control of pods but is the only way into the cluster and all other pods remain secure)