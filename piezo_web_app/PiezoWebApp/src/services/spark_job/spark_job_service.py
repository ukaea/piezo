from kubernetes.client.rest import ApiException

from PiezoWebApp.src.models.return_status import StatusCodes
from PiezoWebApp.src.services.spark_job.i_spark_job_service import ISparkJobService
from PiezoWebApp.src.services.spark_job.spark_job_constants import CRD_GROUP
from PiezoWebApp.src.services.spark_job.spark_job_constants import CRD_PLURAL
from PiezoWebApp.src.services.spark_job.spark_job_constants import CRD_VERSION


class SparkJobService(ISparkJobService):
    def __init__(self, kubernetes_adapter, logger, manifest_populator, spark_job_namer, validation_service):
        self._kubernetes_adapter = kubernetes_adapter
        self._logger = logger
        self._manifest_populator = manifest_populator
        self._spark_job_namer = spark_job_namer
        self._validation_service = validation_service

    def delete_job(self, job_name, namespace):
        try:
            body = self._kubernetes_adapter.delete_options()
            api_response = self._kubernetes_adapter.delete_namespaced_custom_object(
                CRD_GROUP,
                CRD_VERSION,
                namespace,
                CRD_PLURAL,
                job_name,
                body
            )

            msg = f"{job_name} deleted from namespace {namespace}" if api_response['status'] == "Success"\
                else f"Trying to delete job {job_name} resulted in status: {api_response['status']}"
            return {
                'message': msg,
                'status': StatusCodes.Okay.value
            }
        except ApiException as exception:
            message = f'Kubernetes error when trying to delete job "{job_name}" in namespace '\
                f'"{namespace}": {exception.reason}'
            self._logger.error(message)
            return {
                'status': exception.status,
                'message': message
            }

    def get_job_status(self, job_name, namespace):
        try:
            api_response = self._kubernetes_adapter.get_namespaced_custom_object(
                CRD_GROUP,
                CRD_VERSION,
                namespace,
                CRD_PLURAL,
                job_name
            )
            job_status = api_response['status']['applicationState']['state']
            return {
                'message': job_status,
                'status': StatusCodes.Okay.value
            }
        except ApiException as exception:
            message = f'Kubernetes error when trying to get status of spark job "{job_name}" in ' \
                      f'namespace "{namespace}": {exception.reason}'
            self._logger.error(message)
            return {
                'status': exception.status,
                'message': message
            }
        except KeyError as exception:
            message = f'Unexpected response from Kubernetes API when trying to get status of spark job "{job_name}"' \
                      f' in namespace "{namespace}": {api_response}'
            self._logger.error(message)
            raise exception

    def get_jobs(self, label):
        try:
            api_response = self._kubernetes_adapter.list_namespaced_custom_object(
                CRD_GROUP,
                CRD_VERSION,
                'default',
                CRD_PLURAL
            )
            spark_jobs = {
                item['metadata']['name']: SparkJobService._retrieve_status(item) for item in api_response['items']
            }
            if label != "ALL":
                for item in api_response['items']:
                    try:
                        if not item['metadata']['labels']['userLabel'] == label:
                            del spark_jobs[item['metadata']['name']]
                    except KeyError:
                        del spark_jobs[item['metadata']['name']]
            return {
                'message': f"Found {len(spark_jobs)} spark jobs",
                'spark_jobs': spark_jobs,
                'status': StatusCodes.Okay.value
            }
        except ApiException as exception:
            message = f'Kubernetes error when trying to get a list of current spark jobs: {exception.reason}'
            self._logger.error(message)
            return {
                'status': exception.status,
                'message': message
            }
        except KeyError as exception:
            message = f'Unexpected response from Kubernetes API when trying to get list of spark jobs' \
                      f' : {api_response}'
            self._logger.error(message)
            raise exception

    def get_logs(self, job_name, namespace):
        try:
            driver_name = job_name + "-driver"
            api_response = self._kubernetes_adapter.read_namespaced_pod_log(driver_name, namespace)
            return {
                'message': api_response,
                'status': StatusCodes.Okay.value
            }
        except ApiException as exception:
            message = f'Kubernetes error when trying to get logs for spark job "{job_name}" in namespace '\
                f'"{namespace}": {exception.reason}'
            self._logger.error(message)
            return {
                'message': message,
                'status': exception.status
            }

    def submit_job(self, body):
        # Validate the body keys
        validated_body_keys = self._validation_service.validate_request_keys(body)
        if validated_body_keys.is_valid is False:
            return {
                'status': StatusCodes.Bad_request.value,
                'message': validated_body_keys.message
            }

        # Validate the body values
        validated_body_values = self._validation_service.validate_request_values(body)
        if validated_body_values.is_valid is False:
            return {
                'status': StatusCodes.Bad_request.value,
                'message': validated_body_values.message
            }

        # Make the job name unique
        job_name = self._spark_job_namer.rename_job(body['name'])
        validated_body_values.validated_value['name'] = job_name
        self._logger.debug(f'Renamed job "{body["name"]}" to "{job_name}"')

        # Populate the manifest
        body = self._manifest_populator.build_manifest(validated_body_values.validated_value)

        # Try to submit the job
        namespace = body['metadata']['namespace']
        try:
            self._kubernetes_adapter.create_namespaced_custom_object(
                CRD_GROUP,
                CRD_VERSION,
                namespace,
                CRD_PLURAL,
                body
            )
            result = {
                'status': StatusCodes.Okay.value,
                'message': 'Job driver created successfully',
                'job_name': job_name
            }
            return result
        except ApiException as exception:
            message = f'Kubernetes error when trying to submit job: {exception.reason}'
            self._logger.error(message)
            self._logger.error(body)
            return {
                'status': exception.status,
                'message': message
            }

    @staticmethod
    def _retrieve_status(item):
        try:
            return item['status']['applicationState']['state']
        except KeyError:
            return 'UNKNOWN'
