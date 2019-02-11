from __future__ import print_function
import time
import kubernetes.client
from kubernetes import config
from kubernetes.client.rest import ApiException
from pprint import pprint

configuration = config.load_incluster_config()
api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(configuration))
name = 'spark-pi-driver'
namespace = 'default'
pretty = True # Output is printed pretty
timestamps = True # Add timestamps to beginning of each line

def go_get_logs():
    try: 
        api_response = api_instance.read_namespaced_pod_log(name, namespace, timestamps=timestamps)
        pprint(api_response)
        return(api_response)
    except ApiException as e:
        print("Exception when calling CoreV1Api->read_namespaced_pod_log: %s\n" % e)