## Stories covered

* `tidyjobs` handler
* Automated tidying
* Update validation rules

## pre demo

* Pull latest version of Piezo repository
* Ensure you have `kubectl` access to the openstack kubernetes cluster
* Ensure the latest version of the web app is running (see wiki for instructions on deploying the web app)
* Ensure you have a `configuration.ini` file in the same location as `example_configuration.ini`.
update the content with (a few values may be updated in the next step):
```
[Logging]
LogFolderLocation = /
LoggingLevel = DEBUG

[Application]
ApplicationPort = 8888
RunEnvironment = K8S
K8sClusterConfigFile = C:\Users\taro\.kube\openstack
TidyFrequency = 3600

[Storage]
S3Endpoint = http://172.16.113.201:9000
S3KeysSecret = minio-keys
SecretsDir = /etc/secrets
```
* This demo will include running the web app locally so ensure you have the following files on your local machine:

- The configuration file for kubernetes cluster (in the slack channel) note it's location and add this as the value of `K8sClusterConfigFile` in `configuration.ini`
- A directory to place log files for the web app (e.g C:\temp\piezo\logging\). Set this as `LogFolderLocation` in `configuration.ini`
- A directory containing the minio secrets files (e.g.  C:\temp\piezo\secrets\) Set this as the value for `SecretsDir` in `configuration.ini`
  - This secrets directory must contain 2 files:
      `access_key` whose content is: `AKIAIOSFODNN7EXAMPLE`
      `secret_key` whose content is: `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`

- Also set the `RunEnvironment` value to `SYSTEM` in the `configuration.ini` files


* Load up `pycharm` at the route of the repository and open the file `run_piezo.py`
* Click the green arrow next to `if __name__ == "__main__":` to launch the web app.

* Log into minio: `http://host-172-16-113-201.nubes.stfc.ac.uk:9000/minio/login`
  - access key: `AKIAIOSFODNN7EXAMPLE`
  - secret key: `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`
* delete the outputs folder in the kubernetes bucket

*  Ensure you have a file `validation_rules.json` whose content and location matches `example_validation_rules.json`
* Navigate to `piezo_web_app/PiezoWebApp` and run `sh update_validation_rules.sh`

# `tidyjobs` handler

* For this we will use the web app deployed on the k8s cluster.
* send `GET` requests to `http://host-172-16-113-146.nubes.stfc.ac.uk:31924/piezo/getjobs`
json_body = `{}` to show initially no jobs running
* Log into minio and show that the kubernetes bucket has now outputs folder
* In postman initiate several spark jobs:
  `POST request to http://host-172-16-113-146.nubes.stfc.ac.uk:31924/piezo/submitjob/`

  json_body =
  ```
  {
 "name": "spark-pi",
 "language":"Scala",
 "main_class": "org.apache.spark.examples.SparkPi",
 "path_to_main_app_file": "local:///opt/spark/examples/jars/spark-examples_2.11-2.4.0.jar",
 "executors": "10",
 "label": "demo-2",
 "arguments": ["1000"]
}
```

* Periodically send `GET` requests to `http://host-172-16-113-146.nubes.stfc.ac.uk:31924/piezo/getjobs`
json_body = `{}`
This will show the jobs changing statuses

* When jobs start to complete send `POST` requests to `http://host-172-16-113-146.nubes.stfc.ac.uk:31924/piezo/tidyjobs/` no body needed
This should tidy the  jobs with `COMPLETED` or `FAILED` state, writing their logs to S3 and deleting them off the cluster.
* Check the minio browser, should have an outputs folder with a subfolder for each job containing its logs
* send `GET` requests to `http://host-172-16-113-146.nubes.stfc.ac.uk:31924/piezo/getjobs`
json_body = `{}` to show tidied jobs are gone but non-finished jobs are still present.


## Automated tidy jobs
* Mention that `tidyjobs` is called automatically in the background at a configurable time (show `configuration.ini`). Here the `TidyFrequency` value is in length of time between calls in seconds.
* Change the configuration time to something like `10` and click the green arrow next to `if __name__ == "__main__":` to launch the web app with this new config.
* Launch a few jobs again:
`POST request to http://host-172-16-113-146.nubes.stfc.ac.uk:31924/piezo/submitjob/`

json_body =
```
{
"name": "spark-pi",
"language":"Scala",
"main_class": "org.apache.spark.examples.SparkPi",
"path_to_main_app_file": "local:///opt/spark/examples/jars/spark-examples_2.11-2.4.0.jar",
"executors": "10",
"label": "demo-2",
"arguments": ["1000"]
}
```
* Should now see jobs being tidied within 10 seconds of finishing (depending on value set in config). Can keep track of this with `GET` requests to `http://host-172-16-113-146.nubes.stfc.ac.uk:31924/piezo/getjobs`
json_body = `{}` and checking for logs being created in minio.

# Update validation rules
* Will be using the web app deployed on the cluster again
* Explain how validation rules were loaded as a json file built into the docker image containing the web app. Could only be updated by redeploying the web app which involved rebuilding the docker image
* Now can be updated without touching the docker file as using a configmap.
* Launch a spark job with 15 executors:
`POST request to http://host-172-16-113-146.nubes.stfc.ac.uk:31924/piezo/submitjob/`

json_body =
```
{
"name": "spark-pi",
"language":"Scala",
"main_class": "org.apache.spark.examples.SparkPi",
"path_to_main_app_file": "local:///opt/spark/examples/jars/spark-examples_2.11-2.4.0.jar",
"executors": "15",
"label": "demo-2",
"arguments": ["1000"]
}
```
* Should fail executor limit is 10
* Now open up `validation_rules.json` and edit the value of:
```
{
  "input_name": "executors",
  "classification": "Optional",
  "default": 1,
  "minimum": 1,
  "maximum": 10
},
```
to:
```
{
  "input_name": "executors",
  "classification": "Optional",
  "default": 1,
  "minimum": 1,
  "maximum": 20
},
```
* Navigate to `piezo_web_app/PiezoWebApp` and run `sh update_validation_rules.sh`
* Now try resubmitting the job. It should now run as the maximum number of executors whould now be 20
