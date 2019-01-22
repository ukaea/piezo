* Currently run web app from inside the cluster as windows isn't playing nicely with writing the command to run a task
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


## Monitoring 
* `https://github.com/banzaicloud/spark-metrics/blob/master/PrometheusSink.md`