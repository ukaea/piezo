### Items included
* Build formal version of web app
* Configurable use of resources
* Argument validation


### Pre demo 
1. Connect to the STFC VPN
2. Ensure that you have kubectl installed and the config file for the cluster on STFC (in slack channel) saved in your `C:Users/{username}/.kube` directory as `config`
3. Run `kubectl get nodes` to ensure that `kubectl` is correctly configured to the openstack cluster. Expect to see the 3 nodes all running and ready. If don't get a response then manually set the environment variable for `KUBECONFIG` to the config file you have for the STFC cluster and retry. If experiencing issues use the config file for a local kubernetes cluster
(`set KUBECONFIG=C:\Users\taro\.kube\config`)

### Deploy web app
* Show deployment script `spark_kube\code\web_app\openstack-deployment\app-deployment.yaml`
* Explain how code is in docker script on harbor instance on openstack
* From local machine run `kubectl apply -f app-deployment.yaml` (From correct folder as above)
* `kubectl get pods` Show app running

### Heartbeat handler
* In POSTMAN submit a GET request to `http://host-172-16-113-146.nubes.stfc.ac.uk:31924/piezo/` 

### Submitting a job (all in postman)
#### Request type = POST
#### URL = http://host-172-16-113-146.nubes.stfc.ac.uk:31924/piezo/submitjob/

* Show file `PiezoWebApp/src/config/spark_job_validation_rules.py` 
* Explain all possible parameters for job and explain difference between types

* Submit job with just the required:
    - `body = {"name": "spark-pi", "language": "Scala", "path_to_main_app_file": "local:///opt/spark/examples/jars/spark-examples_2.11-2.4.0.jar", "main_class": "org.apache.spark.examples.SparkPi"}

* Now play around with configurable options e.g executors, executor_memory, executor_cores

* Try using invalid options and show error catching 
* Also try invalid values and mising required args

* Note between each job you will have to run `kubectl delete sparkapplications --all` to avoid conflicts
