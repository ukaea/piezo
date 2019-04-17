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
        # Act
        result = self.test_service.delete_job('test-spark-job')
        # Assert
        self.assertDictEqual(result, {'message': '"test-spark-job" deleted', 'status': 200, 'error_message': ''})
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
        # Act
        response = self.test_service.delete_job('test-spark-job')
        # Assert
        self.mock_kubernetes_adapter.delete_namespaced_deployment.assert_called_once_with('test-spark-job-ui-proxy',
                                                                                          NAMESPACE,
                                                                                          {"api_version": "version",
                                                                                           "other_values": "values"})
        self.mock_kubernetes_adapter.delete_namespaced_service.assert_called_once_with('test-spark-job-ui-proxy',
                                                                                       NAMESPACE,
                                                                                       {"api_version": "version",
                                                                                        "other_values": "values"})
        self.mock_kubernetes_adapter.delete_namespaced_ingress.assert_called_once_with(
            'test-spark-job-ui-proxy-ingress', NAMESPACE, {"api_version": "version", "other_values": "values"})
        assert response['error_message'] == ''

    def test_delete_job_logs_any_ui_services_that_are_not_deleted_nad_returns_message_to_user(self):
        # Arrange
        k8s_response = {'status': 'Success'}
        self.mock_kubernetes_adapter.delete_options.return_value = {"api_version": "version", "other_values": "values"}
        self.mock_kubernetes_adapter.delete_namespaced_custom_object.return_value = k8s_response
        self.mock_kubernetes_adapter.delete_namespaced_deployment.side_effect = ApiException('Failed to delete proxy')
        # Act
        response = self.test_service.delete_job('test-spark-job')
        # Assert
        self.mock_logger.error.assert_called_once_with('Trying to spark ui proxy resulted in exception: '
                                                       '(Failed to delete proxy)\nReason: None\n')
        assert response['error_message'] == 'Failed to delete spark ui proxy, please contact an administrator.\n'

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
