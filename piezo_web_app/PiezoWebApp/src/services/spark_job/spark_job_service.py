import asyncio
from os.path import basename

from kubernetes.client.rest import ApiException

from PiezoWebApp.src.models.return_status import StatusCodes
from PiezoWebApp.src.models.spark_job_status import SparkJobStatus
from PiezoWebApp.src.models.tidied_job_status import TidiedJobStatus
from PiezoWebApp.src.services.spark_job.i_spark_job_service import ISparkJobService
from PiezoWebApp.src.services.spark_job.spark_job_constants import CRD_GROUP
from PiezoWebApp.src.services.spark_job.spark_job_constants import CRD_PLURAL
from PiezoWebApp.src.services.spark_job.spark_job_constants import CRD_VERSION
from PiezoWebApp.src.services.spark_job.spark_job_constants import NAMESPACE


class SparkJobService(ISparkJobService):
    def __init__(self,
                 kubernetes_adapter,
                 logger,
                 manifest_populator,
                 spark_job_namer,
                 storage_service,
                 validation_service):
        self._kubernetes_adapter = kubernetes_adapter
        self._logger = logger
        self._manifest_populator = manifest_populator
        self._spark_job_namer = spark_job_namer
        self._storage_service = storage_service
        self._validation_service = validation_service

    def delete_job(self, job_name):
        try:
            body = self._kubernetes_adapter.delete_options()
            api_response = self._kubernetes_adapter.delete_namespaced_custom_object(
                CRD_GROUP,
                CRD_VERSION,
                NAMESPACE,
                CRD_PLURAL,
                job_name,
                body
            )

            msg = f'"{job_name}" deleted' if api_response['status'] == "Success"\
                else f'Trying to delete job "{job_name}" resulted in status: {api_response["status"]}'
            self._logger.debug(msg)
            return {
                'message': msg,
                'status': StatusCodes.Okay.value
            }
        except ApiException as exception:
            message = f'Kubernetes error when trying to delete job "{job_name}": {exception.reason}'
            self._logger.error(message)
            return {
                'status': exception.status,
                'message': message
            }

    def get_job_status(self, job_name):
        try:
            api_response = self._kubernetes_adapter.get_namespaced_custom_object(
                CRD_GROUP,
                CRD_VERSION,
                NAMESPACE,
                CRD_PLURAL,
                job_name
            )
            status = SparkJobStatus(api_response)
            return {
                'message': f'Job status for "{job_name}"',
                'job_status': status.status,
                'created': status.creation_time,
                'submission_attempts': status.submission_attempts,
                'last_submitted': status.last_submitted,
                'terminated': status.terminated_time,
                'error_messages': status.err_msg,
                'status': StatusCodes.Okay.value
            }
        except ApiException as exception:
            message = f'Kubernetes error when trying to get status of spark job "{job_name}": {exception.reason}'
            self._logger.error(message)
            return {
                'status': exception.status,
                'message': message
            }
        except KeyError as exception:
            message = f'Unexpected response from Kubernetes API when trying to get status of spark job "{job_name}":' \
                      f' {api_response}'
            self._logger.error(message)
            raise exception

    def get_jobs(self, label):
        kwargs = {}
        if label is not None:
            # Key must match the key in the manifest populator
            kwargs['label_selector'] = f'userLabel={label}'
        try:
            api_response = self._kubernetes_adapter.list_namespaced_custom_object(
                CRD_GROUP,
                CRD_VERSION,
                NAMESPACE,
                CRD_PLURAL,
                **kwargs
            )
            spark_jobs = {
                item['metadata']['name']: SparkJobService._retrieve_status(item) for item in api_response['items']
            }
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

    def get_logs(self, job_name):
        try:
            driver_name = job_name + "-driver"
            api_response = self._kubernetes_adapter.read_namespaced_pod_log(driver_name, NAMESPACE)
            return {
                'message': api_response,
                'status': StatusCodes.Okay.value
            }
        except ApiException as exception:
            message = f'Kubernetes error when trying to get logs for spark job "{job_name}": {exception.reason}'
            self._logger.error(message)
            return {
                'message': message,
                'status': exception.status
            }

    def get_output_files_temp_urls(self, job_name):
        output_dir = self._job_output_dir_path(job_name)
        temp_urls = self._storage_service.get_temp_url_for_each_file(output_dir)
        temp_urls = {basename(file_path): temp_url for file_path, temp_url in temp_urls.items()}
        msg = f'Got temporary URLs for {len(temp_urls)} output files for job "{job_name}"'
        self._logger.debug(msg)
        status = StatusCodes.Okay if temp_urls else StatusCodes.Not_found
        return {
            'files': temp_urls,
            'message': msg,
            'status': status.value
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

        try:
            self._kubernetes_adapter.create_namespaced_custom_object(
                CRD_GROUP,
                CRD_VERSION,
                NAMESPACE,
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

    def tidy_jobs(self):
        api_response = self.get_jobs(label=None)
        if api_response['status'] != StatusCodes.Okay.value:
            return api_response
        dict_of_jobs = api_response['spark_jobs']
        loop = asyncio.get_event_loop()
        summary = loop.run_until_complete(asyncio.gather(*(
            self._write_and_delete(job, status) for job, status in dict_of_jobs.items())))
        jobs_skipped = {job.job_name: job.status for job in summary if job.tidied == "NO"}
        jobs_tidied = {job.job_name: job.status for job in summary if job.tidied == "YES"}
        jobs_failed_to_process = {
            job.job_name: {
                "job_status": job.status,
                "error_message": job.err_msg,
                "error_status_code": job.err_status
            } for job in summary if job.tidied == "FAIL"}
        return {'status': StatusCodes.Okay.value,
                'message': f'{len(dict_of_jobs)} Spark jobs found',
                'jobs_tidied': jobs_tidied,
                'jobs_skipped': jobs_skipped,
                'jobs_failed_to_process': jobs_failed_to_process}

    def write_logs_to_file(self, job_name):
        api_response = self.get_logs(job_name)
        if api_response['status'] != StatusCodes.Okay.value:
            return api_response
        try:
            file_name = f'{self._job_output_dir_path(job_name)}log.txt'
            self._storage_service.set_contents_from_string(file_name, api_response['message'])
            msg = f'Logs written to "{file_name}"'
            self._logger.debug(msg)
            return {
                'message': msg,
                'status': StatusCodes.Okay.value
            }
        except ApiException as exception:
            message = f'Got logs for job "{job_name}" but unable to write to "{file_name}": {exception.reason}'
            self._logger.error(message)
            return {
                'status': exception.status,
                'message': message
            }

    @staticmethod
    def _job_output_dir_path(job_name):
        return f'outputs/{job_name}/'

    @staticmethod
    def _retrieve_status(item):
        try:
            return item['status']['applicationState']['state']
        except KeyError:
            return 'UNKNOWN'

    async def _write_and_delete(self, job, status):
        if status in ["COMPLETED", "FAILED"]:
            write_logs_response = self.write_logs_to_file(job)
            if write_logs_response['status'] == StatusCodes.Okay.value:
                delete_response = self.delete_job(job)
                if delete_response['status'] == StatusCodes.Okay.value:
                    return TidiedJobStatus(job, status, "YES", None, None)
                else:
                    return TidiedJobStatus(job, status, "FAIL", delete_response['message'], delete_response['status'])
            else:
                return TidiedJobStatus(job,
                                       status,
                                       "FAIL",
                                       write_logs_response['message'],
                                       write_logs_response['status'])
        else:
            self._logger.debug(f'Not processing job "{job}", current status is "{status}"')
            return TidiedJobStatus(job, status, "NO", None, None)
