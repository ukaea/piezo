from __future__ import print_function
import time
import kubernetes.client
from kubernetes import config
from kubernetes.client.rest import ApiException
from pprint import pprint

# Configure API key authorization: BearerToken
configuration = config.load_incluster_config()
# configuration.api_key['authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['authorization'] = 'Bearer'

# create an instance of the API class
api_instance = kubernetes.client.CustomObjectsApi(kubernetes.client.ApiClient(configuration))
group = 'sparkoperator.k8s.io' # str | the custom resource's group
version = 'v1beta1' # str | the custom resource's version
namespace = 'default' # str | The custom resource's namespace
plural = 'sparkapplications' # str | the custom resource's plural name. For TPRs this would be lowercase plural kind.
name = 'spark-pi' # str | the custom object's name
body = kubernetes.client.V1DeleteOptions() # V1DeleteOptions | 
grace_period_seconds = 56 # int | The duration in seconds before the object should be deleted. Value must be non-negative integer. The value zero indicates delete immediately. If this value is nil, the default grace period for the specified type will be used. Defaults to a per object value if not specified. zero means delete immediately. (optional)
orphan_dependents = True # bool | Deprecated: please use the PropagationPolicy, this field will be deprecated in 1.7. Should the dependent objects be orphaned. If true/false, the \"orphan\" finalizer will be added to/removed from the object's finalizers list. Either this field or PropagationPolicy may be set, but not both. (optional)
# propagation_policy = 'propagation_policy_example' # str | Whether and how garbage collection will be performed. Either this field or OrphanDependents may be set, but not both. The default policy is decided by the existing finalizer set in the metadata.finalizers and the resource-specific default policy. (optional)

def delete_job():
    try: 
        api_response = api_instance.delete_namespaced_custom_object(group, version, namespace, plural, name, body, grace_period_seconds=grace_period_seconds, orphan_dependents=orphan_dependents)
        pprint(api_response)
        return(api_response)
    except ApiException as e:
        print("Exception when calling CustomObjectsApi->delete_namespaced_custom_object: %s\n" % e)