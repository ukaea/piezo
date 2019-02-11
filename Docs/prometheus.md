# Monitoring kubernetes with prometheus
The following information approximately follows what can be found in this [blog](https://itnext.io/kubernetes-monitoring-with-prometheus-in-15-minutes-8e54d1de2e13)
Kubernetes allows for monitoring using prometheus and Grafana interfaces.

Before installing prometheus we will first install ingress allowing us to access the prometheus dashboard outside of the kubernetes cluster.

To install the ingress controller run:
```
helm install stable/nginx-ingress
```
Once installed check the port on which ingress is exposed on a note this down. (I will refer to this as {ingress port})

Add the following line to your local machine's host file as this will allow you to access the dashboards in your browser:
```
172.28.128.10 prometheus.piezo.ac.uk
```
subsituting the Ip for whatever your cluster IP address is.


Next install Prometheus on your working cluster by first running:
```
helm install stable/prometheus-operator --name piezo-monitor --set prometheus.prometheusSpec.routePrefix=/prometheus/ --set prometheus.prometheusSpec.externalUrl=prometheus.piezo.ac.uk:{ingress port}/prometheus/ 
```
This will install a prometheus operator than extends the kubernetes api as well as providing the relevant prefix to be configured later to assign ingress rules to. All the pods related to the prometheus operator are then included in the namespace monitoring.

Check that all pods are running by using the command:
```
kubectl get pods  -n monitoring
```

Finally apply the ingress rules to access the prometheus dashboard by running:
```
kubectl apply -f ~/code/ingress/prometheus-ingress-local.yaml
```
This will also have configure ingress rules for Grafana (see below).

Once all pods are up and running and ingress rules are set you can access the prometheus dashboard navigating to `prometheus.piezo.ac.uk:{ingress port}/prometheus/graph` in your local browser.


## Linking with Grafana
Grafana provides a better looking dashboard whilst hooking into the prometheus datasource for you. Following the instructions above for prometheus will have installed all requirments for Grafana for you and will have set the ingress rules required to access the dashboard. To access the Grafana dashboard on your machine just open up a browser and navigate to: `prometheus.piezo.ac.uk:{ingress port}/` where you will see the Grafana dashboard. On your first visit you will be required to login using the credentials `username: admin`, `password: prom-operator`.


# Monitoring spark applications with prometheus
The spark application comes with a built in option to expose application, driver and executor specific metric to prometheus. To enable this you first need to ensure that when you install the spark operator you install it with the option `-enable-metrics=true`. Currently this is assigned by default.

You also need to ensure that the docker image you have running in your containers contains the relevant components to export and expsoe the metrics. In particular you need to add the prometheus JMX exported Java agent jar and add the configuration rules which can be found in `code/prometheus/conf`. This can either be achieved by using the base spark operator docker image with prometheus `gcr.io/spark-operator/spark:v2.4.0-gcs-prometheus` or by including the following code in a docker file when building your image:
```
# Setup for the Prometheus JMX exporter.
RUN mkdir -p /etc/metrics/conf
# Add the Prometheus JMX exporter Java agent jar for exposing metrics sent to the JmxSink to Prometheus.
ADD https://repo1.maven.org/maven2/io/prometheus/jmx/jmx_prometheus_javaagent/0.3.1/jmx_prometheus_javaagent-0.3.1.jar /prometheus/

COPY path_to_conf/metrics.properties /prometheus/
COPY path_to_conf/prometheus.yaml /prometheus/
```

Either way this will include the required resources in your docker image and you can tell your spark application to expose metrics by including the following in the application's yaml file:
```
  monitoring:
    exposeDriverMetrics: true
    exposeExecutorMetrics: true
    prometheus:
      jmxExporterJar: "/prometheus/jmx_prometheus_javaagent-0.3.1.jar"
      port: 8090 
```

Now the driver and exectuor metrics will be exposed on port `8090` of the relevent pods. 

Note the application specific metrics will be exposed by the spark-operator pod on port `10254` by default. This can be specified to a specific port when installing the spark operator.

## Configuring prometheus to scrape the metrics

Now that the metrics are exposed it is possible to configure prometheus to scrape these metrics and expose them on the dashboard. To do this yu first need to set up a service that will forward the metrics. 

This is defined by the following yaml file:

```
kind: Service
apiVersion: v1
metadata: # service specific information
  name: spark-monitor-service 
  labels:
    spark-role: monitor
spec:
  selector:
    test: monitor # name of a lable to match on pods. The service will then apply to all pods which contain this lable
  ports:
  - name: web
    port: 8090 # port where metrics are exposed
```

Lables can be assigned to drivers and executors by including the following lines in the applications yaml file.

```
spec:
  driver:
    labels:
      test: monitor
  executor:
    labels:
      test: monitor
```

The service are then analysed by prometheus service monitors. These have similar definitions as services and look for sevices that have the lables that match their selector. An example service monitor to monitor the above service could be:

```
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  namespace: monitoring
  name: spark-application-monitor
  labels:
    release: prometheus-operator # What is matched by the prometheus crd definition
spec:
  endpoints:
  - port: web
  selector:
    spark-role: monitor
```

Note by default the service monitor must be in the same namespace as the prometheus operator to be picked up. Also he prometheus operator has a `serviceMonitorSelector` seting that has a list of lables that must be matched with those in the metadata of the service monitor for it to be included. This can be found in the CRD definition of prometheus installed on your machine that can be accessed by running `kubectl get prometheus -o yaml --all-namespaces`. Ensuring that the selctor here is satisfied by your service monitor it should now be picked up by prometheus. 

With this correctly configured you should now find extra metrics available in the dropdown menu of the prometheus dashboard. 

### Note
To run kubectl commands from outside your kubernetes cluster you first must copy the clusters config file to you local machine to do this it is easiest it use a shared folder. 
Then you can run:
`cp ~/.kube/config /shared/location/`. Then on your local machine run `mkdir ~/.kube` and copy the config file into this new directory.