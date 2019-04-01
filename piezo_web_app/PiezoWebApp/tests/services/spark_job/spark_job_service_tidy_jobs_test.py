from kubernetes.client.rest import ApiException

from PiezoWebApp.src.services.spark_job.spark_job_constants import CRD_GROUP
from PiezoWebApp.src.services.spark_job.spark_job_constants import CRD_PLURAL
from PiezoWebApp.src.services.spark_job.spark_job_constants import CRD_VERSION
from PiezoWebApp.src.services.spark_job.spark_job_constants import NAMESPACE

from PiezoWebApp.tests.services.spark_job.spark_job_service_test import TestSparkJobService


class SparkJobServiceGetJobStatusTest(TestSparkJobService):

    def tidy_jobs_calls_write_and_delete_with_finished_jobs(self, status):
        # Arrange
        self.mock_kubernetes_adapter.list_namespaced_custom_object.return_value = {"items": [
            {"metadata": {"name": "job"}, "status": {"applicationState": {"state": status}}}
        ]}
        self.mock_kubernetes_adapter.read_namespaced_pod_log.return_value = 'Log\nMessage'
        delete_options = {"api_version": "version", "other_values": "values"}
        self.mock_kubernetes_adapter.delete_options.return_value = delete_options
        self.mock_kubernetes_adapter.delete_namespaced_custom_object.return_value = {'status': 'Success'}
        # Act
        response = self.test_service.tidy_jobs()
        # Assert
        self.mock_kubernetes_adapter.read_namespaced_pod_log.assert_called_once_with('job-driver', NAMESPACE)
        self.mock_storage_adapter.set_contents_from_string.assert_called_once_with('kubernetes',
                                                                                   'outputs/job/log.txt',
                                                                                   'Log\nMessage')
        self.mock_kubernetes_adapter.delete_namespaced_custom_object.assert_called_once_with(CRD_GROUP,
                                                                                             CRD_VERSION,
                                                                                             NAMESPACE,
                                                                                             CRD_PLURAL,
                                                                                             'job',
                                                                                             delete_options)
        assert response == {'status': 200,
                            'message': '1 Spark jobs found',
                            'jobs_tidied': {'job': status},
                            'jobs_skipped': {},
                            'jobs_failed_to_process': {}}

    def tidy_jobs_does_not_tidy_unfinished_jobs(self, status):
        # Arrange
        self.mock_kubernetes_adapter.list_namespaced_custom_object.return_value = {"items": [
            {"metadata": {"name": "job"}, "status": {"applicationState": {"state": status}}}
        ]}
        # Act
        response = self.test_service.tidy_jobs()
        # Assert
        self.mock_kubernetes_adapter.read_namespaced_pod_log.assert_not_called()
        self.mock_storage_adapter.set_contents_from_string.assert_not_called()
        self.mock_kubernetes_adapter.delete_namespaced_custom_object.assert_not_called()
        assert response == {'status': 200,
                            'message': '1 Spark jobs found',
                            'jobs_tidied': {},
                            'jobs_skipped': {'job': status},
                            'jobs_failed_to_process': {}}
        self.mock_logger.debug.assert_any_call(f'Not processing job "job", current status is "{status}"')

    def test_completed_jobs_have_logs_written_and_are_deleted(self):
        self.tidy_jobs_calls_write_and_delete_with_finished_jobs('COMPLETED')

    def test_failed_jobs_have_logs_written_and_are_deleted(self):
        self.tidy_jobs_calls_write_and_delete_with_finished_jobs('FAILED')

    def test_pending_jobs_are_skipped(self):
        self.tidy_jobs_does_not_tidy_unfinished_jobs('PENDING')

    def test_running_jobs_are_skipped(self):
        self.tidy_jobs_does_not_tidy_unfinished_jobs('RUNNING')

    def test_succeeding_jobs_are_skipped(self):
        self.tidy_jobs_does_not_tidy_unfinished_jobs('SUCEEDED')

    def test_unknown_jobs_are_skipped(self):
        self.tidy_jobs_does_not_tidy_unfinished_jobs('UNKNOWN')

    def test_crash_loop_back_off_jobs_are_skipped(self):
        self.tidy_jobs_does_not_tidy_unfinished_jobs('CrashLoopBackOff')

    def test_tidy_jobs_skips_and_records_jobs_that_fail_to_log(self):
        # Arrange
        self.mock_kubernetes_adapter.list_namespaced_custom_object.return_value = {"items": [
            {"metadata": {"name": "job"}, "status": {"applicationState": {"state": "COMPLETED"}}}
        ]}
        self.mock_kubernetes_adapter.read_namespaced_pod_log.return_value = 'Log\nMessage'
        self.mock_storage_adapter.set_contents_from_string.side_effect = ApiException(reason='S3 Reason', status=999)
        # Act
        response = self.test_service.tidy_jobs()
        # Assert
        self.mock_kubernetes_adapter.read_namespaced_pod_log.assert_called_once_with('job-driver', NAMESPACE)
        self.mock_storage_adapter.set_contents_from_string.assert_called_once_with('kubernetes',
                                                                                   'outputs/job/log.txt',
                                                                                   'Log\nMessage')
        self.mock_kubernetes_adapter.delete_namespaced_custom_object.assert_not_called()
        assert response == {'status': 200,
                            'message': '1 Spark jobs found',
                            'jobs_tidied': {},
                            'jobs_skipped': {},
                            'jobs_failed_to_process': {
                                'job': {
                                    'job_status': 'COMPLETED',
                                    'error_message': 'Got logs for job "job" but unable to write to '
                                                     '"outputs/job/log.txt" in bucket "kubernetes": S3 Reason',
                                    'error_status_code': 999
                                }}}

    def test_tidy_jobs_skips_and_records_jobs_that_fail_to_delete(self):
        # Arrange
        self.mock_kubernetes_adapter.list_namespaced_custom_object.return_value = {"items": [
            {"metadata": {"name": "job"}, "status": {"applicationState": {"state": "COMPLETED"}}}
        ]}
        self.mock_kubernetes_adapter.read_namespaced_pod_log.return_value = 'Log\nMessage'
        delete_options = {"api_version": "version", "other_values": "values"}
        self.mock_kubernetes_adapter.delete_options.return_value = delete_options
        self.mock_kubernetes_adapter.delete_namespaced_custom_object.side_effect = ApiException(reason="Reason",
                                                                                                status=999)
        # Act
        response = self.test_service.tidy_jobs()
        # Assert
        self.mock_kubernetes_adapter.read_namespaced_pod_log.assert_called_once_with('job-driver', NAMESPACE)
        self.mock_storage_adapter.set_contents_from_string.assert_called_once_with('kubernetes',
                                                                                   'outputs/job/log.txt',
                                                                                   'Log\nMessage')
        self.mock_kubernetes_adapter.delete_namespaced_custom_object.assert_called_once_with(CRD_GROUP,
                                                                                             CRD_VERSION,
                                                                                             NAMESPACE,
                                                                                             CRD_PLURAL,
                                                                                             'job',
                                                                                             delete_options)
        assert response == {'status': 200,
                            'message': '1 Spark jobs found',
                            'jobs_tidied': {},
                            'jobs_skipped': {},
                            'jobs_failed_to_process': {
                                'job': {
                                    'job_status': 'COMPLETED',
                                    'error_message': 'Kubernetes error when trying to delete job "job": Reason',
                                    'error_status_code': 999
                                }}}
