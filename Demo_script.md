# SPrint 5 demo

1. Talk through powerpoint
3. Explain the kubernetes API and python client
4. `kubectl get pods --all-namespaces` show the tiller pod and explain the role of helm
5. Talk through `install_spark_operator.sh` and show spark operator pod in the script
7. Explain the concept of the mocked up web app and stress that it is just for investigation of what can be done and how hard it is to do.
8. Explain the config file for the kubernetes cluster has been shared with the local machine so can access the cluster from outside

8. In first window run `kubectl proxy` (note need to be within cluster as web app is running from within the cluster to avoid windows related issues)
9. In second run `python main.py`
10. `kubectl get pods --all-namespaces`
## On postman

10. `Get http://172.28.128.10:8888/runexample`
 Sends a post request with body of yaml file

## In second window
12. show driver pod being created `kubectl get pods --all-namespaces`

## On postman

13. `Get http://172.28.128.10:8888/getlogs`
    Sends get request 

## In second window
14. wait until completed `kubectl get pods --all-namespaces`
15. show logs match `kubectl logs spark-pi-driver`

## On postman

16. `Get http://172.28.128.10:8888/deleteexample` 
    sends a delete request
## In second window
17. Show the driver has been cleared up