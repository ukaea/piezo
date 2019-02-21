from kubernetes.client.rest import ApiException

from PiezoWebApp.src.services.kubernetes.i_kubernetes_service import IKubernetesService
from PiezoWebApp.src.services.spark_job.manifest_populator import ManifestPopulator
from PiezoWebApp.src.services.validator.validation_rules import ValidationRules
from PiezoWebApp.src.services.validator.argument_validation_service import ArgumentValidationService

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
        self.validation_rules = ValidationRules()
        self._manifest_populator = ManifestPopulator(self.validation_rules)
        self._argument_validation_service = ArgumentValidationService(self.validation_rules)

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
        validated_body_keys = self._argument_validation_service.validate_request_keys(body)
        if validated_body_keys.is_valid is False:
            return validated_body_keys.message
        validated_body_values = self._argument_validation_service.validate_request_values(body)
        if validated_body_values.is_valid is False:
            return validated_body_values.message
        body = self._manifest_populator.build_manifest(validated_body_values.validated_value)
        namespace = body['metadata']['namespace']
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
