### Items included
* Getting job Status
* Getting job Logs
* Deleting a job
* Submitting job against S3
* Passing arguments to the spark job
* Adding labels to jobs


### Pre demo
1. Connect to the STFC VPN
2. Ensure that you have kubectl installed and the config file for the cluster on STFC (in slack channel) saved in your `C:Users/{username}/.kube` directory as `config`
3. Run `kubectl get nodes` to ensure that `kubectl` is correctly configured to the openstack cluster. Expect to see the 3 nodes all running and ready. If don't get a response then manually set the environment variable for `KUBECONFIG` to the config file you have for the STFC cluster and retry. If experiencing issues use the config file for a local kubernetes cluster
(`set KUBECONFIG=C:\Users\taro\.kube\config`)
4. Pre build the docker image containing the `PiezoWebApp` by following the deployment instructions on the wiki. In particular running `package_piezo.sh` and `deploy_piezo.sh`
5. Log into minio server and ensure that the output folders are all empty but the input folder contains `wordcount.py` and `big.txt`


## Getting job Status
##### POSTMAN
1. Check web app is running `Get to http://host-172-16-113-146.nubes.stfc.ac.uk:31924/piezo/`
2. Submit a job:

Post request to `http://host-172-16-113-146.nubes.stfc.ac.uk:31924/piezo/submitjob/`
json:
```
{
 "name": "spark-pi",
 "language":"Scala",
 "main_class": "org.apache.spark.examples.SparkPi",
 "path_to_main_app_file": "local:///opt/spark/examples/jars/spark-examples_2.11-2.4.0.jar",
 "label": "demo",
 "arguments": ["10000"]
}
```

3. Take job name from the return body
4. Send `Get` to `http://host-172-16-113-146.nubes.stfc.ac.uk:31924/piezo/jobstatus/`
json body
```
{
  "name": "{job_name}",
  "namespace": "default"
}
```
5. Repeat until completed
6. In terminal run `kubectl get pods` to show pod has run and is completed

## Get logs
1. Using previous job name send `Get` to `http://host-172-16-113-146.nubes.stfc.ac.uk:31924/piezo/getlogs/`
json body
```
{
  "name": "{job_name}",
  "namespace": "default"
}
```
2. Repeat submitting job and repeat get request whilst running to show getting logs as job Runs

## Job arguments

1. `POST` request to `http://host-172-16-113-146.nubes.stfc.ac.uk:31924/piezo/submitjob/`

2. JSON body:
 ```
 json
{
  "name": "spark-group-by",
  "language":"Scala",
  "main_class": "org.apache.spark.examples.GroupByTest",
  "path_to_main_app_file": "local:///opt/spark/examples/jars/spark-examples_2.11-2.4.0.jar",
  "label": "demo",
  "arguments": ["10", "670", "1300", "3"]
}
```

3. GET request to `http://host-172-16-113-146.nubes.stfc.ac.uk:31924/piezo/jobstatus/`
json body
```
{
  "name": "{job_name}",
  "namespace": "default"
}
```
until status is `COMPLETED`

4. GET request to `http://host-172-16-113-146.nubes.stfc.ac.uk:31924/piezo/getlogs/`
json body
```
{
  "name": "{job_name}",
  "namespace": "default"
}
```

5. Show lines:
* `Adding task set 0.0 with 10 tasks` (or replace 10 with first argument submitted)
* `Adding task set 2.0 with 3 tasks` (or replace 3 with fourth argument submitted)

## Submitting against S3
1. Submit `POST` request to `http://host-172-16-113-146.nubes.stfc.ac.uk:31924/piezo/submitjob/`
2. json body:
```
{
  "name": "wordcount2",
   "language": "Python",
   "python_version": "2",
   "path_to_main_app_file": "s3a://kubernetes/inputs/wordcount.py",
   "arguments": ["s3a://kubernetes/inputs/big.txt", "s3a://kubernetes/nonSystemTestOut"],
   "label": "s3-demo",
   "executors": "5"
}
```

3. GET request to `http://host-172-16-113-146.nubes.stfc.ac.uk:31924/piezo/jobstatus/`
json body
```
{
  "name": "{job_name}",
  "namespace": "default"
}
```
 until status is `COMPLETED`

4. GET request to `http://host-172-16-113-146.nubes.stfc.ac.uk:31924/piezo/getlogs/`
json body
```
{
  "name": "{job_name}",
  "namespace": "default"
}
```

5. Log into minio and show the `nonSystemTestOut` folder with results from job

## Get list of jobs

1. Submit `GET` request to `http://host-172-16-113-146.nubes.stfc.ac.uk:31924/piezo/getjobs`

2. Submit new job using one of above commands

3. Repeat `GET` request and show updated list

## Delete job

1. Submit `DELETE` request to `http://host-172-16-113-146.nubes.stfc.ac.uk:31924/piezo/deletejob/`
json body
```
{
  "name": "{job_name}",
  "namespace": "default"
}
```

2. Submit `GET` request to `http://host-172-16-113-146.nubes.stfc.ac.uk:31924/piezo/jobstatus/`
json body
```
{
  "name": "{job_name}",
  "namespace": "default"
}
```
 show 404 error

3. Submit `GET` request to `http://host-172-16-113-146.nubes.stfc.ac.uk:31924/piezo/getjobs` show job deleted

## Using labels

1. Explain how have used labels throughout the tasks
2. `kubectl get sparkapplications --all`
2. In a terminal run `kubectl get sparkapplications -l userLabel=demo`
3. `kubectl get sparkapplications -l userLabel=s3-demo`
