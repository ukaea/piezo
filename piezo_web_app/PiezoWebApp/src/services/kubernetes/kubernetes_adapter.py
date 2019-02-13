import kubernetes
from kubernetes.client.rest import ApiException

from PiezoWebApp.src.services.kubernetes.i_kubernetes_adapter import IKubernetesAdapter

# str | The custom resource's group name
CRD_GROUP = 'sparkoperator.k8s.io'

# str | The custom resource's plural name. For TPRs this would be lowercase plural kind.
CRD_PLURAL = 'sparkapplications'

# str | The custom resource's version
CRD_VERSION = 'v1beta1'


class KubernetesAdapter(IKubernetesAdapter):
    def __init__(self, logger):
        self._logger = logger
        config = kubernetes.config.load_incluster_config()
        api_client = kubernetes.client.ApiClient(config)
        self._connection = kubernetes.client.CustomObjectsApi(api_client)

    def delete_job(self, job_name, namespace):
        try:
            body = kubernetes.client.V1DeleteOptions()
            api_response = self._connection.delete_namespaced_custom_object(
                CRD_GROUP,
                CRD_VERSION,
                namespace,
                CRD_PLURAL,
                job_name,
                body
            )
            return api_response.content
        except ApiException as exception:
            self._logger.error(f'API exception when trying to delete job "${job_name}" in namespace '
                               f'"${namespace}": ${exception}')

    def get_logs(self, driver_name, namespace):
        try:
            api_response = self._connection.read_namespaced_pod_log(driver_name, namespace)
            return api_response
        except ApiException as exception:
            self._logger.error(f'API exception when trying to read logs for driver "${driver_name}" in namespace '
                               f'"${namespace}": ${exception}')

    def submit_job(self, body):
        # Get the namespace from the body
        try:
            namespace = body['metadata']['namespace']
        except KeyError:
            self._logger.warning(f'Job submitted without namespace in metadata')
        # Try to submit the job
        try:
            api_response = self._connection.create_namespaced_custom_object(
                CRD_GROUP,
                CRD_VERSION,
                namespace,
                CRD_PLURAL,
                body
            )
            return api_response.content
        except ApiException as exception:
            self._logger.error(f'API exception when trying to submit job: ${exception}')

