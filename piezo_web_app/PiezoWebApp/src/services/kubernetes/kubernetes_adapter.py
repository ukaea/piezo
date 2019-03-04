import kubernetes

from PiezoWebApp.src.services.kubernetes.i_kubernetes_adapter import IKubernetesAdapter


class KubernetesAdapter(IKubernetesAdapter):
    def __init__(self, config):
        api_client = kubernetes.client.ApiClient(config)
        self._core_connection = kubernetes.client.CoreV1Api(api_client)
        self._custom_connection = kubernetes.client.CustomObjectsApi(api_client)

    # pylint: disable=too-many-arguments
    def delete_namespaced_custom_object(self, group, version, namespace, plural, name, body):
        return self._custom_connection.delete_namespaced_custom_object(group, version, namespace, plural, name, body)

    def read_namespaced_pod_log(self, driver_name, namespace):
        return self._core_connection.read_namespaced_pod_log(driver_name, namespace)

    # pylint: disable=too-many-arguments
    def create_namespaced_custom_object(self, group, version, namespace, plural, body):
        return self._custom_connection.create_namespaced_custom_object(group, version, namespace, plural, body)

    def get_namespaced_custom_object(self, group, version, namespace, plural, name):
        return self._custom_connection.get_namespaced_custom_object(group, version, namespace, plural, name)
