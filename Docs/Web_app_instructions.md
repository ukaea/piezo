* Currently run web app from inside the cluster
* To view the outputs of the logs readable use `view-source:http://172.28.128.10:8888/getlogs`
* Logs can be refreshed through running of the app to show the progress



## Using the web app

* Need to have a proxy running from the server so can communicate on local host

* Suggestion to use the direct api approach over the kubectl approach as more general informative responses (status codes etc)

* Can run kubectl commands through web api but causes issues with echo if running from windows

* kubernetes python client doesn't seem to be compatiable with spark operator through custom resources

* Try and understand more about the api and work out how to get logs

* Get logs of a pod  Get request to `http://localhost:8001/api/v1/namespaces/default/pods/spark-pi-driver/log` or python client equivilent `https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/CoreV1Api.md#read_namespaced_pod_log`

* Can delete a spark application by sending a delete request to `http://localhost:8001/apis/sparkoperator.k8s.io/v1alpha1/namespaces/{namespace}/sparkapplications/{name_of_application}`

Or via the python client `delete_namespaced_custom_object`

## Mounting volumes
* To mount volumes to spark driver and executors need to have spark 2.4  Can only mount volumes of type: `hostPath`, `emptyDir`, `persistentVolumeClaim`
* Need to have the mutating admission webhook (done by default when spark operator is installed but can be disabled)


## Launching the web app on the kubernetes cluster
When you run the web app on a kubernetes cluster you need to set up ingress rules to allow you to communicate with the apllication. To do this you first need to set up a base `nginx ingress controller` and then configure rules specifically to redirect connections to your pods. To initiate this controller navigate to `~/code/ingress` and run `./apply-ingress.sh`. This will launch the ingress controller and apply basic ingress rules for monitoring with prometheus. We will configure web app ingress rules when launching the app.

To launch the web app in a kubernetes pod you first need to build the code into a docker image. First ensure you have a docker registory that can be pushed and pulled from by the machine where you are going to deploy the web app. 

Navigate to `~/code/web_app/` and run `/containerise.sh`. The docker registory may need to be configured first within this file to match the docker registory that you are pushing to. Running this script will package the web app into a docker container and push the container to the registory ready to be pushed to the kubernetes cluster.

With the app packaged in a container navigate to `~/code/web_app/local_deployment` or `~/code/web_app/openstack_deployment` and run `kubectl apply -f app-deployment.yaml`. This applies the manifest file which will launch a deploment of the web app in a pod on the kubernetes cluster. Next it spins up a kubernetes service which will controll requests and services to this pod. Finally it configure ingress rules so that the web app can be controlled from your local browser on the address `http://prometheus.piezo.ac.uk:32381/piezo/{command}` (note you must add 172.28.128.10 prometheus.piezo.ac.uk to the hosts file on your local machine when doing a local deployment)


# Notes on app developmnent
* Body now seems to be requied in jsonb format as opposed to strings being allowed
* Use `configuraion = kubernetes.config.load_incluster_config()` to use the configuration file of the cluster where the code is run