### Items included
* Using labels to filter sparkapplications
* Improved return for job Status


### Pre demo
1. Connect to the STFC VPN
2. Ensure that you have kubectl installed and the config file for the cluster on STFC (in slack channel) saved in your `C:Users/{username}/.kube` directory as `config`
3. Run `kubectl get nodes` to ensure that `kubectl` is correctly configured to the openstack cluster. Expect to see the 3 nodes all running and ready. If don't get a response then manually set the environment variable for `KUBECONFIG` to the config file you have for the STFC cluster and retry. If experiencing issues use the config file for a local kubernetes cluster
(`set KUBECONFIG=C:\Users\taro\.kube\config`)
4. Pre build the docker image containing the `PiezoWebApp` by following the deployment instructions on the wiki. In particular running `package_piezo.sh` and `deploy_piezo.sh`
5. Log into minio server and ensure that the output folders are all empty but the input folder contains `wordcount.py` and `big.txt`


## Filter jobs with labels
##### POSTMAN
1. Check web app is running `Get to http://host-172-16-113-146.nubes.stfc.ac.uk:31924/piezo/`
2. Submit 3 jobs:

```
{
 "name": "spark-pi",
 "language":"Scala",
 "main_class": "org.apache.spark.examples.SparkPi",
 "path_to_main_app_file": "local:///opt/spark/examples/jars/spark-examples_2.11-2.4.0.jar",
 "label": "demo-1",
 "arguments": ["1000"]
}
```
3. Submit 2 more jobs:

```
{
 "name": "spark-pi",
 "language":"Scala",
 "main_class": "org.apache.spark.examples.SparkPi",
 "path_to_main_app_file": "local:///opt/spark/examples/jars/spark-examples_2.11-2.4.0.jar",
 "label": "demo-2",
 "arguments": ["1000"]
}
```

4. `Get to http://host-172-16-113-146.nubes.stfc.ac.uk:31924/piezo/getjobs` with no label arguments. i.e. `body: {}`

5. Repeat with `body: {"label": "demo-1"}`

6. Repeat with `body: {"label": "demo-2"}`

## Improved return for job Status
1. Submit a job:
```
{
 "name": "spark-pi",
 "language":"Scala",
 "main_class": "org.apache.spark.examples.SparkPi",
 "path_to_main_app_file": "local:///opt/spark/examples/jars/spark-examples_2.11-2.4.0.jar",
 "label": "demo",
 "arguments": ["1000"]
}
```

2. `Get request to http://host-172-16-113-146.nubes.stfc.ac.uk:31924/piezo/jobstatus`
