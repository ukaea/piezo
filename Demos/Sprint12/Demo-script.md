## Stories covered

* Spark UI
* Output dir as first argument
* S3 configuration (bucket name, ECHO)
* Performance testing
* Resilience changes

## Pre demo
1. Connect to the STFC VPN
2. Ensure that you have kubectl installed and the config file for the cluster on STFC (in slack channel) saved in your `C:Users/{username}/.kube` directory as `config`
3. Run `kubectl get nodes` to ensure that `kubectl` is correctly configured to the openstack cluster. Expect to see the 3 nodes all running and ready. If don't get a response then manually set the environment variable for `KUBECONFIG` to the config file you have for the STFC cluster and retry. If experiencing issues use the config file for a local kubernetes cluster
(`set KUBECONFIG=C:\Users\taro\.kube\config`)
* Pull latest version of Piezo repository
4. Pre build the docker image containing the `PiezoWebApp` by following the deployment instructions on the wiki. In particular running `package_piezo.sh` and `deploy_piezo.sh`
5. Log into minio server and ensure that the output folders are all empty but the input folder contains `wordcount.py` and `big.txt`
* Ensure the latest version of the web app is running (see wiki for instructions on deploying the web app)
* Ensure you have a `configuration.ini` file in the same location as `example_configuration.ini`. Content should be:
```
[Logging]
LogFolderLocation = /
LoggingLevel = DEBUG
[Application]
ApplicationPort = 8888
K8sUrl = http://host-172-16-113-146.nubes.stfc.ac.uk:31856
K8sClusterConfigFile = C:\Users\taro\.kube\openstack
TidyFrequency = 3600
[Storage]
S3Endpoint = http://172.16.113.201:9000
S3BucketName = kubernetes
S3KeysSecret = minio-keys
SecretsDir = /etc/secrets
TempUrlExpirySeconds = 600
```
* Ensure you have a `validation_rules.json` file in the same location as `example_validation_rules.json`. Content should be the same.

### Spark UI

Run a long lasting job to allow time to access the spark UI

* `POST` request to http://host-172-16-113-146.nubes.stfc.ac.uk:31856/piezo/submitjob/
json_body
```
{
	"name":"python-pi",
	"language":"Python",
	"python_version":"2",
	"path_to_main_app_file":"s3a://kubernetes/inputs/pi.py",
	"label":"test",
	"spark_ui": "true",
	"arguments": ["100000"]
}
```
* Depending on status of #134
* If not ready:
  - In browser navigate to URL returned when job is submitted: e.g. http://host-172-16-113-146.nubes.stfc.ac.uk:31856/proxy:python-pi-8344e-ui-svc:4040
* Else if ready then follow appropriate procedure to request the URL and navigate to it in a browser.

* When Spark UI loads:
  - Show DAG visualisation (progress of job)
  - Show `Event timeline` shows when each component of job started
  - Show `STAGES` page
* Explain how only created when requested and not available after the job has finished
*

### Output dir as first argument
* Show the request body for wordcount job:
```
{
	"name":"python-job",
	"language":"Python",
	"python_version":"3",
	"path_to_main_app_file":"s3a://kubernetes/inputs/wordcount.py",
	"label":"test",
	"arguments": ["s3a://kubernetes/inputs/big.txt"]
}
```
* Explain how automatically assign an output directory based on UID name where logs and output can be found
* Don't have to use but need access to other storage to retrieve outputs if not

* Submit job using above request with `POST` request to http://host-172-16-113-146.nubes.stfc.ac.uk:31856/piezo/submitjob/
* Call tidyjobs handler until the job has been completed
  - `POST` to http://host-172-16-113-145.nubes.stfc.ac.uk:31856/piezo/tidyjobs/
* Get temp url of files
* http://host-172-16-113-146.nubes.stfc.ac.uk:31856/piezo/outputfiles
* body: `{"job_name": "{name of job just run}"}`
* Login to Minio browser using the example credentials:
  - access_key = AKIAIOSFODNN7EXAMPLE
  - secret key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
* Find output dir of job just run

### S3 configuration
* Open configuration.ini
* Talk through new `S3BucketName` option

* Edit storage section to:
```
[Storage]
S3Endpoint = https://echo.stfc.ac.uk:443
S3BucketName = alc-piezo
S3KeysSecret = echo-keys
SecretsDir = /etc/secrets/
TempUrlExpirySeconds = 600
```
* Save file
* Navigate in a terminal to `/piezo_web_app/PiezoWebApp/`
* run `sh update_configs.sh`
* `POST` request to http://host-172-16-113-146.nubes.stfc.ac.uk:31856/piezo/submitjob/
json_body
```
{
	"name":"python-pi",
	"language":"Python",
	"python_version":"3",
	"path_to_main_app_file":"s3a://kubernetes/inputs/pi.py",
	"label":"test",
	"arguments": ["1000"]
}
```

### Performance testing
* Talk through current progress
* Show current Performance testing infrastructure

### Resilience changes:
Thing to mention:
* Pod priority (set on Ingress, Piezo web app, Prometheus)
* Set resource quota for web app pod
* Increase frequency of tidy jobs
* Change pod restart policy from `Never` to `onFailure`
* Only create spark UI when needed
