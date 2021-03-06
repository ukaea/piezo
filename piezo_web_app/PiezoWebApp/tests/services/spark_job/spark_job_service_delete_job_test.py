from kubernetes.client.rest import ApiException

from PiezoWebApp.src.services.spark_job.spark_job_constants import CRD_GROUP
from PiezoWebApp.src.services.spark_job.spark_job_constants import CRD_PLURAL
from PiezoWebApp.src.services.spark_job.spark_job_constants import CRD_VERSION
from PiezoWebApp.src.services.spark_job.spark_job_constants import NAMESPACE

from PiezoWebApp.tests.services.spark_job.spark_job_service_test import TestSparkJobService


class SparkJobServiceDeleteJobTest(TestSparkJobService):
    def test_delete_job_sends_expected_arguments(self):
        # Arrange
        k8s_response = {'status': 'Success'}
        self.mock_kubernetes_adapter.delete_options.return_value = {"api_version": "version", "other_values": "values"}
        self.mock_kubernetes_adapter.delete_namespaced_custom_object.return_value = k8s_response
        self.mock_spark_ui_service.delete_spark_ui_components.return_value = 'Spark ui deleted successfully for job ' \
                                                                             '"test-spark-job"'
        # Act
        result = self.test_service.delete_job('test-spark-job')
        # Assert
        self.assertDictEqual(result, {'message': '"test-spark-job" deleted\nSpark ui deleted successfully for job '
                                                 '"test-spark-job"',
                                      'status': 200})
        self.mock_kubernetes_adapter.delete_namespaced_custom_object.assert_called_once_with(
            CRD_GROUP,
            CRD_VERSION,
            NAMESPACE,
            CRD_PLURAL,
            'test-spark-job',
            {"api_version": "version", "other_values": "values"}
        )

    def test_delete_job_sends_request_to_delete_proxy_components_for_ui(self):
        # Arrange
        k8s_response = {'status': 'Success'}
        self.mock_kubernetes_adapter.delete_options.return_value = {"api_version": "version", "other_values": "values"}
        self.mock_kubernetes_adapter.delete_namespaced_custom_object.return_value = k8s_response
        self.mock_spark_ui_service.delete_spark_ui_components.return_value = 'Spark ui deleted successfully for job' \
                                                                             ' "test-spark-job"'
        # Act
        response = self.test_service.delete_job('test-spark-job')
        # Assert
        self.mock_spark_ui_service.delete_spark_ui_components.assert_called_once_with('test-spark-job',
                                                                                      {"api_version": "version",
                                                                                       "other_values": "values"})
        assert response['message'] == '"test-spark-job" deleted\nSpark ui deleted successfully for job "test-spark-job"'

    def test_delete_job_logs_any_ui_services_that_are_not_deleted_and_returns_message_to_user(self):
        # Arrange
        k8s_response = {'status': 'Success'}
        self.mock_kubernetes_adapter.delete_options.return_value = {"api_version": "version", "other_values": "values"}
        self.mock_kubernetes_adapter.delete_namespaced_custom_object.return_value = k8s_response
        self.mock_spark_ui_service.delete_spark_ui_components.return_value = 'Error deleting spark ui for job ' \
                                                                             '"test-spark-job", please contact ' \
                                                                             'an administrator'
        # Act
        response = self.test_service.delete_job('test-spark-job')
        # Assert
        assert response['message'] == '"test-spark-job" deleted\nError deleting spark ui for job "test-spark-job",' \
                                      ' please contact an administrator'

    def test_delete_job_logs_and_returns_api_exception_reason(self):
        # Arrange
        self.mock_kubernetes_adapter.delete_namespaced_custom_object.side_effect = ApiException(
            reason="Reason",
            status=999
        )
        # Act
        result = self.test_service.delete_job('test-spark-job')
        # Assert
        expected_message = \
            'Kubernetes error when trying to delete job "test-spark-job": Reason'
        self.mock_logger.error.assert_called_once_with(expected_message)
        assert result['status'] == 999
        assert result['message'] == expected_message
