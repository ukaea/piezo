from kubernetes.client.rest import ApiException

from PiezoWebApp.src.services.spark_job.spark_job_constants import NAMESPACE


class SparkUiService:
    def __init__(self, kubernetes_adapter, spark_ui_adapter, logger):
        self._kubernetes_adapter = kubernetes_adapter
        self._spark_ui_adapter = spark_ui_adapter
        self._logger = logger

    def get_spark_ui_url(self, job_name):
        url = self._spark_ui_adapter.create_ui_url(job_name) if self.does_spark_ui_exist(job_name) else "Unavailable"
        return url

    def expose_spark_ui(self, job_name):
        proxy_body = self._spark_ui_adapter.create_ui_proxy_body(job_name, NAMESPACE)
        proxy_svc_body = self._spark_ui_adapter.create_ui_proxy_svc_body(job_name, NAMESPACE)
        proxy_ingress_body = self._spark_ui_adapter.create_ui_proxy_ingress_body(job_name)
        try:
            self._kubernetes_adapter.create_namespaced_deployment(NAMESPACE, proxy_body)
            self._kubernetes_adapter.create_namespaced_service(NAMESPACE, proxy_svc_body)
            self._kubernetes_adapter.create_namespaced_ingress(NAMESPACE, proxy_ingress_body)
            url = self._spark_ui_adapter.create_ui_url(job_name)
        except ApiException as exception:
            self._logger.error(f'Setting up spark ui failed due to error: {exception}')
            return "Unavailable"
        return url

    def delete_spark_ui_components(self, job_name, body):
        if not self.does_spark_ui_exist(job_name):
            msg = f'No need to delete Spark UI for "{job_name}": does not exist.'
            self._logger.debug(msg)
            return msg

        proxy_name = f'{job_name}-ui-proxy'
        ingress_name = f'{proxy_name}-ingress'
        error = False
        try:
            self._kubernetes_adapter.delete_namespaced_deployment(proxy_name, NAMESPACE, body)
            self._logger.debug("UI proxy deployment deleted")
        except ApiException as exception:
            self._logger.error(f'Trying to delete spark ui proxy resulted in exception: {exception}')
            error = True
        try:
            self._kubernetes_adapter.delete_namespaced_service(proxy_name, NAMESPACE, body)
            self._logger.debug("UI proxy service deleted")
        except ApiException as exception:
            self._logger.error(f'Trying to delete spark ui service resulted in exception: {exception}')
            error = True
        try:
            self._kubernetes_adapter.delete_namespaced_ingress(ingress_name, NAMESPACE, body)
            self._logger.debug("UI proxy ingress rules deleted")
        except ApiException as exception:
            self._logger.error(f'Trying to delete spark ui ingress resulted in exception: {exception}')
            error = True
        msg = f'Spark ui deleted successfully for job "{job_name}"' if error is False \
            else f'Error deleting spark ui for job "{job_name}", please contact an administrator'
        return msg

    def does_spark_ui_exist(self, job_name):
        try:
            self._kubernetes_adapter.read_namespaced_pod_status(job_name, NAMESPACE)
            return True
        except Exception:
            return False
