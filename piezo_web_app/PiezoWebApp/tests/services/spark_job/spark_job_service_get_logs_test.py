from kubernetes.client.rest import ApiException

from PiezoWebApp.tests.services.spark_job.spark_job_service_test import TestSparkJobService


class SparkJobServiceGetLogsTest(TestSparkJobService):
    def test_get_logs_sends_expected_arguments(self):
        # Arrange
        self.mock_kubernetes_adapter.read_namespaced_pod_log.return_value = "Response"
        # Act
        result = self.test_service.get_logs('test-job', 'test-namespace')
        # Assert
        self.assertDictEqual(result, {'message': 'Response', 'status': 200})
        self.mock_kubernetes_adapter.read_namespaced_pod_log.assert_called_once_with(
            'test-job-driver', 'test-namespace')

    def test_get_logs_logs_and_returns_api_exception_reason(self):
        # Arrange
        self.mock_kubernetes_adapter.read_namespaced_pod_log.side_effect = ApiException(reason="Reason", status=999)
        # Act
        result = self.test_service.get_logs('test-job', 'test-namespace')
        # Assert
        expected_message = \
            'Kubernetes error when trying to get logs for spark job "test-job" in namespace "test-namespace": Reason'
        self.mock_logger.error.assert_called_once_with(expected_message)
        self.assertDictEqual(result, {'status': 999, 'message': expected_message})
