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
        # Act
        result = self.test_service.get_job_status('test-job')
        # Assert
        self.assertDictEqual(result, {
            'message': 'Job status for "test-job"', 'status': 200,
            "job status": "RUNNING",
            "created": 12345,
            "submission attempts": 1,
            "last submitted": 123456,
            "terminated": 1234567,
            "error messages": ''})
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
        # Act
        result = self.test_service.get_job_status('test-job')
        # Assert
        self.assertDictEqual(result, {
            "status": 200,
            "message": 'Job status for "test-job"',
            "job status": "UNKNOWN",
            "created": "UNKNOWN",
            "submission attempts": "UNKNOWN",
            "last submitted": "UNKNOWN",
            "terminated": "UNKNOWN",
            "error messages": "UNKNOWN"
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
