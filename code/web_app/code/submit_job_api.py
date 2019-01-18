from __future__ import print_function
import time
import requests
import kubernetes.client
from kubernetes.client.rest import ApiException
from kubernetes import config
from pprint import pprint

# Configure API key authorization: BearerToken
configuration = config.load_kube_config()
#configuration.api_key['authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['authorization'] = 'Bearer'

# create an instance of the API class
api_instance = kubernetes.client.CoreV1Api()
#kubernetes.client.AppsV1beta2Api(kubernetes.client.ApiClient(configuration))
namespace = 'namespace_example' # str | object name and auth scope, such as for teams and projects

include_uninitialized = True # bool | If true, partially initialized resources are included in the response. (optional)
pretty = 'pretty_example' # str | If 'true', then the output is pretty printed. (optional)
dry_run = 'dry_run_example' # str | When present, indicates that modifications should not be persisted. An invalid or unrecognized dryRun directive will result in an error response and no further processing of the request. Valid values are: - All: all dry run stages will be processed (optional)



body = str('apiVersion: \"sparkoperator.k8s.io/v1alpha1\"\n\
kind: SparkApplication\nmetadata:\n\
  name: spark-pi\n\
  namespace: default\n\
spec:\n\
  type: Scala\n\
  mode: cluster\n\
  image: \"gcr.io/spark-operator/spark:v2.4.0\"\n\
  imagePullPolicy: Always\n\
  mainClass: org.apache.spark.examples.SparkPi\n\
  mainApplicationFile: \"local:///opt/spark/examples/jars/spark-examples_2.11-2.4.0.jar\"\n\
  restartPolicy:\n\
    type: Never\n\
  driver:\n\
    cores: 0.1\n\
    coreLimit: \"200m\"\n\
    memory: \"512m\"\n\
    labels:\n\
      version: 2.4.0\n\
    serviceAccount: spark\n\
  executor:\n\
    cores: 1\n\
    instances: 2\n\
    memory: \"512m\"\n\
    labels:\n\
      version: 2.4.0')

namespace = 'default'
type_of_request = 'POST'
url = 'http://localhost:8001/apis/sparkoperator.k8s.io/v1alpha1/namespaces/default/sparkapplications'
headers = {'Content-Type': 'application/yaml'}

def run_job():
    try: 
        api_response = requests.post(url, body, headers=headers)
        print(api_response.status_code)
        print(api_response.content)
        return api_response.content
    except ApiException as e:
        print("Exception: %s\n" % e)
