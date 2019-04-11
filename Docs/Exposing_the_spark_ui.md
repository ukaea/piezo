# Exposing the spark ui
The spark ui is exposed via a service spun up automatically by the spark operator. This service exposes port 4040 of the driver pod where the ui is exposed and opens up a node port with access directly to the user. 
The node port is randomly assigned between 30000 and 32700 and can be located by using `kubectl get sparkapplication {job name}` and finding the webUiPort under status.driverInfo. The spark ui can then be accessed on `host-172.16.113-146.nubes,stfc.ac.uk:{port number}`. Adding this address could be done easily as part of the return to the `jobstatus` handler.

Whilst the simpliest we want to try and avoid this method due to security issues around giving users direct access to the cluster, and potential difficulties with getting through firewalls. As such the following methods have been investigated. 

### Using the spark operator
In theory it is possible to configure the spark operator to dynamically create ingress rules to expose the spark ui from the service on a custom route. This is meant to be done by setting the value of `webUiIngress` when using helm to install the spark operator. It is meant to take a argument including a placeholder that is replaced with the name of the spark job as it is spun up. This then in theory creates a subdomain for each spark job where you can access the spark ui on `/`. Unfortunately this property doesn't seem to be working and also it would be required to find a way to dynamically add the subdomains to the users host files as the ingess rules were created. 
By setting the values in the `values` file in the helm chart it is possible to enter a string as the `webUiIngress` value. This is used as the host for the ingress rule however as mentioned later, this causes the problem that it clashes with Grafana on `/` and can only support one ui.  

### Port forwarding
It is also possible to use kubectl to port forward directly to the spark ui (`kubectl port-forward {driver pod} 4040` and then spark ui will be on `localhost:4040`) but the users won't have kubectl access to the cluster.

Port forwarding can be wrapped by the python client and used by a handler on piezo where it would accept the job name as an argument and return the spark ui. We can then use a service to expose this port and ingress rules to make it accessible outisde of the cluster but as is explained below this is limited in a way that makes it unusable.

### Ingress
Any method to get through to the spark ui is required to have an ingress rule so that the spark ui is accessible from outside the cluster. It is possible to put each ui on its own route e.g. `/jobname/{page}` by using the `rewrite-target` annotation, but any interaction will cause automatic redirection to `/{page}` taking it off the ingress rule. It is possible to have the spark ui on `/` but this would clash with the ingress rule for Grafana. It is possible to overwrite the base URL of Grafana so that it is no longer on `/`, leaving `/` clear for the ui but we would still be restricted to having access to the ui for a single job due to only having a single route for all the ingress rules. 

### Proxy
The other way to access the spark ui is to use a proxy. Running `kubectl proxy` it is then possible to access the spark ui at `http://localhost:8001/api/v1/namespaces/default/pods/{driver pod}:4040/proxy/`. We won't be running a constant proxy though as this would open up the possibility for the users to interact directly with the kubernetes api. It is also possible to proxy the service exposing the spark-ui. This is meant to be possible through the python client however this behaviour is not currently supported for the service in general. Additionally this would need to be on a new handler which would pass back the contents of the page rather than a link to the spark ui. It is possible to use the python client to proxy a single route with path but this returns a snapshot of a single page of the spark ui rather than returning the ui.
Ignoring the python client it should be possible to create a proxy for the spark ui which would be compatable with unique ingress rules. This involves using the proxy provided here: `https://github.com/aseigneurin/spark-ui-proxy` which should provide a route to the ui at `http://host-172-16-113-146.nubes.stfc.ac.uk:31924/proxy:{job ui svc}:4040`. This would be unique for each job as its name is in the URL and would not conflict with existing ingress rules. Technically here each job ingress rule is on `/` but has a unique route from `/` which makes it possible to have multiple rules together.

# Implementing the proxy method

To implement the proxy method we must first move Grafana away from `/`. This should be possible from editing the `values` file in the `prometheus-operator` helm chart although it is no immediately clear how. It is likely that it will be easier to use the seperate helm charts for prometheus and grafana as this will allow more control between the distinct ingress rules etc. See [here](https://helm.sh/docs/using_helm/#customizing-the-chart-before-installing) for instructions how to go about this.
This branch does have a working method that will expose the spark ui on a unique URL for each spark job by using a proxy. It also creates ingress rules dynamically on a jobs creation. However, this logic (currently in the kubernetes adapter class) needs neatening and clarifying. There is also no method for tidy up and when each job is created the proxy, ingress rules and service remain. As such, deletion of each of these should be included in the `delete job` method so that the cluster does not get too congested. Note the deletion of the proxy is performed by deleting the deployment rather than the pod directly. 
We also need to pass back the URL as part of the return of the submit job handler. 


### An initial attempt to move Grafana by using the prometheus-operator helm chart:

Run from the kubernetes master:
```
cat << EOF > grafana-config.yaml
routePrefix: /monitoring/
EOF
```

```
helm install -f grafana-config.yaml stable/prometheus-operator --name piezo-monitor --set prometheus.prometheusSpec.routePrefix=/prometheus/ --set prometheus.prometheusSpec.externalUrl=host-172-16-113-146.nubes.stfc.ac.uk:31924/monitoring/prometheus/
```

Ingress manifest applied during deployment:

```
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  annotations:
    kubernetes.io/ingress.class: nginx
  name: prometheus-ingress
spec:
  rules:
    - host: host-172-16-113-146.nubes.stfc.ac.uk
      http:
        paths:
          - backend:
              serviceName: piezo-monitor-prometheus-o-prometheus
              servicePort: web
            path: /prometheus/
          - backend:
              serviceName: piezo-monitor-grafana
              servicePort: service
            path: /monitoring/
```