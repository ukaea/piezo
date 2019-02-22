from kubernetes.client.rest import ApiException

from PiezoWebApp.src.services.spark_job.i_spark_job_service import ISparkJobService
from PiezoWebApp.src.models.return_status import StatusCodes

# str | The custom resource's group name
CRD_GROUP = 'sparkoperator.k8s.io'

# str | The custom resource's plural name. For TPRs this would be lowercase plural kind.
CRD_PLURAL = 'sparkapplications'

# str | The custom resource's version
CRD_VERSION = 'v1beta1'


class SparkJobService(ISparkJobService):
    def __init__(self, kubernetes_adapter, logger, manifest_populator, validation_service):
        self._logger = logger
        self._connection = kubernetes_adapter
        self._manifest_populator = manifest_populator
        self._argument_validation_service = validation_service

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
        # Validate the body keys
        validated_body_keys = self._argument_validation_service.validate_request_keys(body)
        if validated_body_keys.is_valid is False:
            return {
                'status': StatusCodes.Bad_request,
                'message': validated_body_keys.message
            }

        # Validate the body values
        validated_body_values = self._argument_validation_service.validate_request_values(body)
        if validated_body_values.is_valid is False:
            return {
                'status': StatusCodes.Bad_request,
                'message': validated_body_values.message
            }

        # Populate the manifest
        body = self._manifest_populator.build_manifest(validated_body_values.validated_value)

        # Try to submit the job
        namespace = body['metadata']['namespace']
        try:
            api_response = self._connection.create_namespaced_custom_object(
                CRD_GROUP,
                CRD_VERSION,
                namespace,
                CRD_PLURAL,
                body
            )
            driver_name = f'{api_response["metadata"]["name"]}-driver'
            result = {
                'status': StatusCodes.Okay,
                'message': 'Job driver created successfully',
                'driver_name': driver_name
            }
            return result
        except ApiException as exception:
            message = f'Kubernetes error when trying to submit job: {exception.reason}'
            self._logger.error(message)
            return {
                'status': exception.status,
                'message': message
            }
