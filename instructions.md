# Installing a Kubernetes cluster

1. `vagrant up` 


## Helm

1. `vagrant ssh master-k8s`
5. Wait for `kubectl get pods --all-namespaces` to show `tiller` as `RUNNING`
1. Run `./install_spark_operator.sh` on master-k8s to install the spark operator
## Run an example

`kubectl apply -f spark-pi.yaml`

`kubectl get sparkapplications spark-pi -o=yaml`

`kubectl log spark-pi-driver`


## Run an example through the web API

1. Start the proxy on the host
    - `kubectl proxy`
2. In a new tab start the Api 
    - Navigate to `~/code/web_app/code/`
    - `python main.py`
3. In postman:
 get requests to `http://172.28.128.10:8888/{runexample, getlogs, deleteexample}`


## Sparkctl

`go get k8s.io/client-go/...`



