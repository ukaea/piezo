from kubernetes.client.rest import ApiException

from PiezoWebApp.src.services.spark_job.spark_job_constants import CRD_GROUP
from PiezoWebApp.src.services.spark_job.spark_job_constants import CRD_PLURAL
from PiezoWebApp.src.services.spark_job.spark_job_constants import CRD_VERSION

from PiezoWebApp.tests.services.spark_job.spark_job_service_test import TestSparkJobService


class SparkJobServiceGetJobsTest(TestSparkJobService):
    def test_get_jobs_sends_expected_arguments(self):
        # Arrange
        self.mock_kubernetes_adapter.list_namespaced_custom_object.return_value = {"items": []}
        # Act
        result = self.test_service.get_jobs()
        # Assert
        self.assertDictEqual(result, {'message': 'Found 0 spark jobs', 'spark_jobs': {}, 'status': 200})
        self.mock_kubernetes_adapter.list_namespaced_custom_object.assert_called_once_with(
            CRD_GROUP, CRD_VERSION, 'default', CRD_PLURAL)

    def test_get_jobs_logs_and_returns_api_exception_reason(self):
        # Arrange
        self.mock_kubernetes_adapter.list_namespaced_custom_object.side_effect = \
            ApiException(reason="Reason", status=999)
        # Act
        result = self.test_service.get_jobs()
        # Assert
        expected_message = \
            'Kubernetes error when trying to get a list of current spark jobs: Reason'
        self.mock_logger.error.assert_called_once_with(expected_message)
        self.assertDictEqual(result, {
            'status': 999,
            'message': 'Kubernetes error when trying to get a list of current spark jobs: Reason'
        })

    def test_get_jobs_returns_status_of_jobs_when_present(self):
        # Arrange
        self.mock_kubernetes_adapter.list_namespaced_custom_object.return_value = {"items": [
            {"metadata": {"name": "job1"}, "status": {"applicationState": {"state": "RUNNING"}}}
        ]}
        # Act
        result = self.test_service.get_jobs()
        # Assert
        self.assertDictEqual(result, {'message': 'Found 1 spark jobs',
                                      'spark_jobs': {"job1": "RUNNING"},
                                      'status': 200})
        self.mock_kubernetes_adapter.list_namespaced_custom_object.assert_called_once_with(
            CRD_GROUP, CRD_VERSION, 'default', CRD_PLURAL)

    def test_get_jobs_returns_status_of_job_as_unknown_when_missing(self):
        # Arrange
        self.mock_kubernetes_adapter.list_namespaced_custom_object.return_value = {"items": [
            {"metadata": {"name": "job1"}}
        ]}
        # Act
        result = self.test_service.get_jobs()
        # Assert
        self.assertDictEqual(result, {'message': 'Found 1 spark jobs',
                                      'spark_jobs': {"job1": "UNKNOWN"},
                                      'status': 200})
        self.mock_kubernetes_adapter.list_namespaced_custom_object.assert_called_once_with(
            CRD_GROUP, CRD_VERSION, 'default', CRD_PLURAL)
