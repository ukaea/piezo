from __future__ import print_function
import time
import kubernetes.client
from kubernetes.client.rest import ApiException
from kubernetes import config
from pprint import pprint
import json

# Configure API key authorization: BearerToken
configuration = config.load_incluster_config()
# configuration = config.load_kube_config()
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['authorization'] = 'Bearer'

# create an instance of the API class
api_instance = kubernetes.client.CustomObjectsApi(kubernetes.client.ApiClient(configuration))
group = 'sparkoperator.k8s.io' # str | The custom resource's group name
version = 'v1beta1' # str | The custom resource's version
namespace = 'default' # str | The custom resource's namespace
plural = 'sparkapplications' # str | The custom resource's plural name. For TPRs this would be lowercase plural kind.
# body = str('apiVersion: \"sparkoperator.k8s.io/v1beta1\"\n\
# kind: SparkApplication\n\
#   metadata:\n\
#   name: spark-pi\n\
#   namespace: default\n\
# spec:\n\
#   type: Scala\n\
#   mode: cluster\n\
#   image: \"gcr.io/spark-operator/spark:v2.4.0\"\n\
#   imagePullPolicy: Always\n\
#   mainClass: org.apache.spark.examples.SparkPi\n\
#   mainApplicationFile: \"local:///opt/spark/examples/jars/spark-examples_2.11-2.4.0.jar\"\n\
#   sparkVersion: \"2.4.0\"\n\
#   restartPolicy:\n\
#     type: Never\n\
#   driver:\n\
#     cores: 0.1\n\
#     coreLimit: \"200m\"\n\
#     memory: \"512m\"\n\
#     labels:\n\
#       version: 2.4.0\n\
#     serviceAccount: spark\n\
#   executor:\n\
#     cores: 1\n\
#     instances: 2\n\
#     memory: \"512m\"\n\
#     labels:\n\
#       version: 2.4.0') #  The JSON schema of the Resource to create.
body = {"apiVersion": "sparkoperator.k8s.io/v1beta1",\
"kind": "SparkApplication",\
"metadata":\
  {"name": "spark-pi",\
  "namespace": "default"},\
"spec": {\
  "type": "Scala",\
  "mode": "cluster",\
  "image": "gcr.io/spark-operator/spark:v2.4.0",\
  "imagePullPolicy": "Always",\
  "mainClass": "org.apache.spark.examples.SparkPi",\
  "mainApplicationFile": "local:///opt/spark/examples/jars/spark-examples_2.11-2.4.0.jar",\
  "sparkVersion": "2.4.0",\
  "restartPolicy": {\
    "type": "Never"},\
  "driver": {\
    "cores": 0.1,\
    "coreLimit": "200m",\
    "memory": "512m",\
    "labels": {\
      "version": "2.4.0"},\
    "serviceAccount": "spark"},\
  "executor": {\
    "cores": 1,\
    "instances": 2,\
    "memory": "512m",\
    "labels": {\
      "version": "2.4.0"}}}} #  The JSON schema of the Resource to create.
pretty = True # str | If 'true', then the output is pretty printed. (optional)

def run_job():
    try: 
        api_response = api_instance.create_namespaced_custom_object(group, version, namespace, plural, body, pretty=pretty)
        pprint(api_response)
        print(api_response.status_code)
        print(api_response.content)
        return api_response.content
    except ApiException as e:
        print("Exception when calling CustomObjectsApi->create_namespaced_custom_object: %s\n" % e)


