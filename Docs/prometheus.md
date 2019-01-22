# Monitoring with prometheus
The following information approximately follows what can be found in this [blog](https://itnext.io/kubernetes-monitoring-with-prometheus-in-15-minutes-8e54d1de2e13)
Kubernetes allows for monitoring using prometheus and Grafana interfaces.

To install Prometheus on your working cluster run:
```
helm install stable/prometheus-operator --name prometheus-operator --namespace monitoring
```
This will install a prometheus operator than extends the kubernetes api. All the pods related to the prometheus operator are then included in the namespace monitoring.

Check that all pods are running by using the command:
```
kubectl get pods  -n monitoring
```

Once all pods are up and running you can access the prometheus dashboard by portfowarding the `prometheus-prometheus-operator-prometheus-0` pod.

To do this, on your local machine (where you want to run the dashboard) run:
```
kubectl proxy
```
Then in a new command window on the same machine, run:
```
kubectl port-forward -n monitoring prometheus-prometheus-operator-prometheus-0 9090
```
Now in a browser on your machine you should be able to navigate to `http://http:localhost:9090` where you will see the prometheus dashboard

## Linking with Grafana
Grafana provides a better looking dashboard whilst hooking into the prometheus datasource for you. To access the Grafana dashboard on your machine you once again need to use port forwarding. Once again ensure the proxy is running and then run the command:
```
kubectl port-forward $(kubectl get  pods --selector=app=grafana -n  monitoring --output=jsonpath="{.items..metadata.name}") -n monitoring  3000
```

Now navigate in your browser to `http://http:localhost:3000` where you will see ther Grafana dashboard

### Note
To run kubectl commands from outside your kubernetes cluster you first must copy the clusters config file to you local machine to do this it is easiest it use a shared folder. 
Then you can run:
`cp ~/.kube/config /shared/location/`. Then on your local machine run `mkdir ~/.kube` and copy the config file into this new directory