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
(`set KUBECONFIG=C:\Users\taro\.kube\config`)

# Setting up a kubernetes cluster on openstack
1. Mention have set up a cluster on openstack (with more resources) and continuing development there
2. Show config file in `C:\Users\taro\.kube` pointing to the STFC cluster
3. Explain how this allows control of cluster remotely
4. Run `Kubectl get nodes` to show the nodes running
5. Navigate to `https://openstack.stfc.ac.uk/project/instances/` and show the nodes running
6. Run `kubectl get pods --all-namespaces` and talk through pods showing same state as last time on local cluster

# Ingress rules and monitoring with Prometheus and Grafana
1. Explain what ingress does (allows access into the cluster and control of pods but is the only way into the cluster and all other pods remain secure)
2. Explain used helm to install the ingress controller `helm install stable/nginx-ingress`
3. Show `~/code/ingress/...` and run `kubectl apply -f ~/code/ingress/prometheus-ingress-openstack.yaml` which defines ingress rules for accessing prometheus and Grafana
4. In your browser navigate to `http://host-172-16-113-146.nubes.stfc.ac.uk:31924/` to show Grafana
5. Also navigate to `http://host-172-16-113-146.nubes.stfc.ac.uk:31924/prometheus/graph` to show Prometheus
6. Remind about use of service to select which parts to monitor
7. Mention should be able to get spark specific metrics here but there is an error in the spark operator code so although we can scrape the pods the metrics don't exist. 

# Infrastructure to containerise a web app
1. Explain still using a basic web app which demonstrates basic principles of what we are going to achieve but will be formalised (work started by Rob)
2. Explain what we are trying to do. Run the web app from within a pod on the cluster and then control externally with ingress ruls
3. Navigate to `~/code/web_app/` (In VM due to docker requirment)
4. Show docker file and talk through copying across the code, install requirments, expose port and running the startup script
5. Mention don't need to include config in dockerimage as can get config of cluster being run in
6. Run `./containerise-openstack.sh`  (In VM due to docker requirment)
7. Mention this is pushing to a harbor instance in the openstack cloud as set up by Rob in 5.3
8. Open `openstack-deployment/app-deployment.yaml` and talk through how this produces deployment, creates service to control deployment and applies ingress rules.
9. run from local machine `kubectl apply -f app-deployment.yaml`
10. run `kubectl get pods` to show app pod created
11. In browser send get requests to `http://host-172-16-113-146.nubes.stfc.ac.uk:31924/piezo/getlogsrunexample` to run a job, 
`http://host-172-16-113-146.nubes.stfc.ac.uk:31924/piezo/getlogs` to get logs of the job and `http://host-172-16-113-146.nubes.stfc.ac.uk:31924/piezo/deleteexample` to clean up the job
