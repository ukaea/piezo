import kubernetes

from PiezoWebApp.src.services.kubernetes.i_kubernetes_adapter import IKubernetesAdapter


class KubernetesAdapter(IKubernetesAdapter):
    def __init__(self, config):
        api_client = kubernetes.client.ApiClient(config)
        self._core_connection = kubernetes.client.CoreV1Api(api_client)
        self._custom_connection = kubernetes.client.CustomObjectsApi(api_client)
        self._extension_connection = kubernetes.client.ExtensionsV1beta1Api(api_client)
        self._v1_connection = kubernetes.client.AppsV1Api(api_client)

    # pylint: disable=too-many-arguments
    def create_namespaced_custom_object(self, group, version, namespace, plural, body):
        return self._custom_connection.create_namespaced_custom_object(group, version, namespace, plural, body)

    def create_namespaced_deployment(self, namespace, body):
        return self._extension_connection.create_namespaced_deployment(namespace, body)

    def create_namespaced_service(self, namespace, body):
        return self._core_connection.create_namespaced_service(namespace, body)

    def create_namespaced_ingress(self, namespace, body):
        return self._extension_connection.create_namespaced_ingress(namespace, body)

    # pylint: disable=too-many-arguments
    def delete_namespaced_custom_object(self, group, version, namespace, plural, name, body):
        return self._custom_connection.delete_namespaced_custom_object(group, version, namespace, plural, name, body)

    def delete_namespaced_deployment(self, name, namespace, body):
        return self._v1_connection.delete_namespaced_deployment(name, namespace, body)

    def delete_namespaced_service(self, name, namespace, body):
        return self._core_connection.delete_namespaced_service(name, namespace, body)

    def delete_namespaced_ingress(self, name, namespace, body):
        return self._extension_connection.delete_namespaced_ingress(name, namespace, body)

    # pylint: disable=too-many-arguments
    def delete_options(self,
                       api_version=None,
                       dry_run=None,
                       grace_period_seconds=None,
                       kind=None,
                       orphan_dependents=None,
                       pre_conditions=None,
                       propagation_policy=None):
        return {'api_version': api_version,
                'dry_run': dry_run,
                'grace_period_seconds': grace_period_seconds,
                'kind': kind,
                'orphan_dependents': orphan_dependents,
                'preconditions': pre_conditions,
                'propagation_policy': propagation_policy}

    def get_namespaced_custom_object(self, group, version, namespace, plural, name):
        return self._custom_connection.get_namespaced_custom_object(group, version, namespace, plural, name)

    def list_namespaced_custom_object(self, group, version, namespace, plural, **kwargs):
        return self._custom_connection.list_namespaced_custom_object(group, version, namespace, plural, **kwargs)

    def read_namespaced_pod_log(self, driver_name, namespace):
        return self._core_connection.read_namespaced_pod_log(driver_name, namespace)

    def read_namespaced_pod_status(self, name, namespace):
        return self._core_connection.read_namespaced_pod_status(name, namespace)
