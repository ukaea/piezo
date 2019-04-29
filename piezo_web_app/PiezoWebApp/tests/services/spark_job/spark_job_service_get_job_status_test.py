from kubernetes.client.rest import ApiException

from PiezoWebApp.src.services.spark_job.spark_job_constants import CRD_GROUP
from PiezoWebApp.src.services.spark_job.spark_job_constants import CRD_PLURAL
from PiezoWebApp.src.services.spark_job.spark_job_constants import CRD_VERSION
from PiezoWebApp.src.services.spark_job.spark_job_constants import NAMESPACE

from PiezoWebApp.tests.services.spark_job.spark_job_service_test import TestSparkJobService


class SparkJobServiceGetJobStatusTest(TestSparkJobService):
    def test_get_job_status_sends_expected_arguments(self):
        # Arrange
        self.mock_kubernetes_adapter.get_namespaced_custom_object.return_value = {
            'metadata': {
                'creationTimestamp': 12345},
            'status': {
                'applicationState': {'state': 'RUNNING', 'errorMessage': ''},
                'submissionAttempts': 1,
                'lastSubmissionAttemptTime': 123456,
                'terminationTime': 1234567}}
        self.mock_spark_ui_service.get_spark_ui_url.return_value = "http://1.1.1.1:1/proxy:test-job-ui-svc:4040"
        # Act
        result = self.test_service.get_job_status('test-job')
        # Assert
        self.mock_spark_ui_service.get_spark_ui_url.assert_called_once_with('test-job')
        self.assertDictEqual(result, {
            'message': 'Job status for "test-job"', 'status': 200,
            "job_status": "RUNNING",
            "created": 12345,
            "submission_attempts": 1,
            "last_submitted": 123456,
            "spark_ui": "http://1.1.1.1:1/proxy:test-job-ui-svc:4040",
            "terminated": 1234567,
            "error_messages": ''})
        self.mock_kubernetes_adapter.get_namespaced_custom_object.assert_called_once_with(
            CRD_GROUP,
            CRD_VERSION,
            NAMESPACE,
            CRD_PLURAL,
            'test-job'
        )

    def test_get_job_status_returns_status_of_job_as_unknown_when_missing(self):
        # Arrange
        self.mock_kubernetes_adapter.get_namespaced_custom_object.return_value = {'name': 'test-job'}
        self.mock_spark_ui_service.get_spark_ui_url.return_value = "http://1.1.1.1:1/proxy:test-job-ui-svc:4040"
        # Act
        result = self.test_service.get_job_status('test-job')
        # Assert
        self.mock_spark_ui_service.get_spark_ui_url.assert_called_once_with('test-job')
        self.assertDictEqual(result, {
            "status": 200,
            "message": 'Job status for "test-job"',
            "job_status": "UNKNOWN",
            "created": "UNKNOWN",
            "submission_attempts": "UNKNOWN",
            "last_submitted": "UNKNOWN",
            "spark_ui": "http://1.1.1.1:1/proxy:test-job-ui-svc:4040",
            "terminated": "UNKNOWN",
            "error_messages": "UNKNOWN"
        })
        self.mock_kubernetes_adapter.get_namespaced_custom_object.assert_called_once_with(
            CRD_GROUP,
            CRD_VERSION,
            NAMESPACE,
            CRD_PLURAL,
            'test-job'
        )

    def test_get_job_status_logs_and_returns_api_exception_reason(self):
        # Arrange
        self.mock_kubernetes_adapter.get_namespaced_custom_object.side_effect = ApiException(reason="Reason",
                                                                                             status=999)
        # Act
        result = self.test_service.get_job_status('test-job')
        # Assert
        expected_message = \
            'Kubernetes error when trying to get status of spark job "test-job": Reason'
        self.mock_logger.error.assert_called_once_with(expected_message)
        self.assertDictEqual(result, {
            'status': 999,
            'message': expected_message
        })
