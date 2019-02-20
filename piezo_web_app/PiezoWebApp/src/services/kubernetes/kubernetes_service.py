from kubernetes.client.rest import ApiException

from PiezoWebApp.src.services.kubernetes.i_kubernetes_service import IKubernetesService

# str | The custom resource's group name
CRD_GROUP = 'sparkoperator.k8s.io'

# str | The custom resource's plural name. For TPRs this would be lowercase plural kind.
CRD_PLURAL = 'sparkapplications'

# str | The custom resource's version
CRD_VERSION = 'v1beta1'


class KubernetesService(IKubernetesService):
    def __init__(self, kubernetes_adapter, logger):
        self._logger = logger
        self._connection = kubernetes_adapter

    def delete_job(self, job_name, namespace):
        try:
            body = self._connection.delete_options()
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
            message = f'Kubernetes error when trying to delete job "{job_name}" in namespace '\
                f'"{namespace}": {exception.reason}'
            self._logger.error(message)
            return message

    def get_logs(self, driver_name, namespace):
        try:
            api_response = self._connection.read_namespaced_pod_log(driver_name, namespace)
            return api_response
        except ApiException as exception:
            message = f'Kubernetes error when trying to get logs for driver "{driver_name}" in namespace '\
                f'"{namespace}": {exception.reason}'
            self._logger.error(message)
            return message

    def submit_job(self, body):
        # Get the namespace from the body
        try:
            namespace = body['metadata']['namespace']
        except KeyError:
            message = 'Job submitted without namespace in metadata'
            self._logger.warning(message)
            return message
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
            message = f'Kubernetes error when trying to submit job in namespace "{namespace}": {exception.reason}'
            self._logger.error(message)
            return message
