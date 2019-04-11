from kubernetes.client.rest import ApiException

from PiezoWebApp.src.services.spark_job.spark_job_constants import NAMESPACE

from PiezoWebApp.tests.services.spark_job.spark_job_service_test import TestSparkJobService


class SparkJobServiceWriteLogsToFileTest(TestSparkJobService):
    def test_write_logs_to_file_logs_and_returns_kubernetes_api_exception_reason(self):
        # Arrange
        self.mock_kubernetes_adapter.read_namespaced_pod_log.side_effect = ApiException(reason='K8s Reason', status=999)
        # Act
        result = self.test_service.write_logs_to_file('test-job')
        # Assert
        expected_message = 'Kubernetes error when trying to get logs for spark job "test-job": K8s Reason'
        self.mock_logger.error.assert_called_once_with(expected_message)
        self.assertDictEqual(result, {'status': 999, 'message': expected_message})

    def test_write_logs_to_file_logs_and_returns_storage_api_exception_reason(self):
        # Arrange
        self.mock_kubernetes_adapter.read_namespaced_pod_log.return_value = 'Log\nMessage'
        self.mock_storage_service.set_contents_from_string.side_effect = ApiException(reason='S3 Reason', status=999)
        # Act
        result = self.test_service.write_logs_to_file('test-job')
        # Assert
        self.mock_kubernetes_adapter.read_namespaced_pod_log.assert_called_once_with('test-job-driver', NAMESPACE)
        expected_message = 'Got logs for job "test-job" but unable to write to "outputs/test-job/log.txt": S3 Reason'
        self.mock_logger.error.assert_called_once_with(expected_message)
        self.assertDictEqual(result, {'status': 999, 'message': expected_message})

    def test_write_logs_to_file_sets_file_contents_to_string_returned(self):
        # Arrange
        self.mock_kubernetes_adapter.read_namespaced_pod_log.return_value = 'Log\nMessage'
        # Act
        result = self.test_service.write_logs_to_file('test-job')
        # Assert
        self.mock_kubernetes_adapter.read_namespaced_pod_log.assert_called_once_with('test-job-driver', NAMESPACE)
        self.mock_storage_service.set_contents_from_string.assert_called_once_with('outputs/test-job/log.txt',
                                                                                   'Log\nMessage')
        self.assertDictEqual(result, {
            'message': f'Logs written to "outputs/test-job/log.txt"',
            'status': 200
        })
