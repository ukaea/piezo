import uuid

from kubernetes.client.rest import ApiException

from PiezoWebApp.src.services.spark_job.i_spark_job_customiser import ISparkJobCustomiser
from PiezoWebApp.src.services.spark_job.spark_job_constants import CRD_GROUP
from PiezoWebApp.src.services.spark_job.spark_job_constants import CRD_PLURAL
from PiezoWebApp.src.services.spark_job.spark_job_constants import CRD_VERSION
from PiezoWebApp.src.services.spark_job.spark_job_constants import NAMESPACE


class SparkJobCustomiser(ISparkJobCustomiser):
    def __init__(self, kubernetes_adapter):
        self._kubernetes_adapter = kubernetes_adapter
        self._max_attempts = 10

    def rename_job(self, base_name):
        counter = 0
        while counter < self._max_attempts:
            trial_job_name = self._tag_job_name_with_uuid(base_name)
            counter += 1
            if not self._does_job_exist(trial_job_name):
                break
        if counter >= self._max_attempts:
            raise RuntimeError(f'{counter} attempts to find a unique job name all failed')
        return trial_job_name

    @staticmethod
    def set_output_dir_as_first_argument(job_name, storage_service, validated_body_values):
        output_dir = f'{storage_service.protocol_route_to_bucket()}/outputs/{job_name}/'
        arguments = validated_body_values.validated_value['arguments'] if \
            'arguments' in validated_body_values.validated_value \
            else []
        arguments.insert(0, output_dir)
        validated_body_values.validated_value['arguments'] = arguments
        return validated_body_values

    def _does_job_exist(self, job_name):
        try:
            self._kubernetes_adapter.get_namespaced_custom_object(
                CRD_GROUP,
                CRD_VERSION,
                NAMESPACE,
                CRD_PLURAL,
                job_name
            )
            return True
        except ApiException:
            return False

    @staticmethod
    def _tag_job_name_with_uuid(base_name):
        # https://github.com/ukaea/piezo/wiki/WebAppDecisionRecord#job-uuid-tag-length
        uuid_tag = str(uuid.uuid4())[:5]
        return f'{base_name}-{uuid_tag}'
