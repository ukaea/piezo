import json
import pytest
from tornado.httpclient import HTTPError
from tornado.testing import gen_test
from kubernetes.client.rest import ApiException

from PiezoWebApp.src.handlers.delete_job import DeleteJobHandler
from PiezoWebApp.tests.integration_tests.base_integration_test import BaseIntegrationTest

# str | The custom resource's group name
CRD_GROUP = 'sparkoperator.k8s.io'

# str | The custom resource's plural name. For TPRs this would be lowercase plural kind.
CRD_PLURAL = 'sparkapplications'

# str | The custom resource's version
CRD_VERSION = 'v1beta1'

NAMESPACE = 'default'


class DeleteJobIntegrationTest(BaseIntegrationTest):
    @property
    def handler(self):
        return DeleteJobHandler

    @property
    def standard_request_method(self):
        return 'DELETE'

    @gen_test
    def test_success_message_is_returned_when_job_deleted_successfully(self):
        # Arrange
        body = {"job_name": "test-spark-job"}
        kubernetes_response = {'status': 'Success'}
        self.mock_k8s_adapter.delete_namespaced_custom_object.return_value = kubernetes_response
        self.mock_k8s_adapter.delete_options.return_value = {"api_version": "version", "other_values": "values"}
        self.mock_k8s_adapter.read_namespaced_pod_status.return_value = True
        # Act
        response_body, response_code = yield self.send_request(body)
        # Assert
        assert self.mock_k8s_adapter.delete_namespaced_custom_object.call_count == 1
        self.mock_k8s_adapter.delete_namespaced_custom_object.assert_called_once_with(CRD_GROUP,
                                                                                      CRD_VERSION,
                                                                                      NAMESPACE,
                                                                                      CRD_PLURAL,
                                                                                      'test-spark-job',
                                                                                      {
                                                                                          "api_version": "version",
                                                                                          "other_values": "values"
                                                                                      })
        assert response_code == 200
        self.assertDictEqual(response_body, {
            'status': 'success',
            'data': {
                'message': '"test-spark-job" deleted\nSpark ui deleted successfully for job "test-spark-job"'
            }
        })

    @gen_test
    def test_delete_requests_deletion_of_spark_ui_proxy_components(self):
        # Arrange
        body = {"job_name": "test-spark-job"}
        kubernetes_response = {'status': 'Success'}
        self.mock_k8s_adapter.delete_namespaced_custom_object.return_value = kubernetes_response
        self.mock_k8s_adapter.delete_options.return_value = {"api_version": "version", "other_values": "values"}
        self.mock_k8s_adapter.read_namespaced_pod_status.return_value = True
        # Act
        response_body, response_code = yield self.send_request(body)
        # Assert
        assert response_code == 200
        self.assertDictEqual(response_body, {
            'status': 'success',
            'data': {
                'message': '"test-spark-job" deleted\nSpark ui deleted successfully for job "test-spark-job"',
            }
        })
        self.mock_k8s_adapter.delete_namespaced_deployment.assert_called_once_with(
            "test-spark-job-ui-proxy", NAMESPACE, {"api_version": "version", "other_values": "values"})
        self.mock_k8s_adapter.delete_namespaced_service.assert_called_once_with(
            "test-spark-job-ui-proxy", NAMESPACE, {"api_version": "version", "other_values": "values"})
        self.mock_k8s_adapter.delete_namespaced_ingress.assert_called_once_with(
            "test-spark-job-ui-proxy-ingress", NAMESPACE, {"api_version": "version", "other_values": "values"})

    @gen_test
    def test_logging_records_failed_deletion_of_ui_components(self):
        # Arrange
        body = {'job_name': 'test-spark-job'}
        kubernetes_response = {'status': 'Success'}
        self.mock_k8s_adapter.delete_namespaced_custom_object.return_value = kubernetes_response
        self.mock_k8s_adapter.delete_options.return_value = {"api_version": "version", "other_values": "values"}
        self.mock_k8s_adapter.read_namespaced_pod_status.return_value = True
        self.mock_k8s_adapter.delete_namespaced_deployment.side_effect = ApiException('Failed to delete proxy')
        self.mock_k8s_adapter.delete_namespaced_service.side_effect = ApiException('Failed to delete service')
        self.mock_k8s_adapter.delete_namespaced_ingress.side_effect = ApiException('Failed to delete ingress')
        # Act
        response_body, response_code = yield self.send_request(body)
        # Assert
        assert response_code == 200
        self.assertDictEqual(response_body, {
            'status': 'success',
            'data': {
                'message': '"test-spark-job" deleted\nError deleting spark ui for job "test-spark-job", please '
                           'contact an administrator',
            }})
        self.mock_logger.error.assert_any_call('Trying to delete spark ui proxy resulted in exception: '
                                               '(Failed to delete proxy)\nReason: None\n')
        self.mock_logger.error.assert_any_call('Trying to delete spark ui service resulted in exception: '
                                               '(Failed to delete service)\nReason: None\n')
        self.mock_logger.error.assert_any_call('Trying to delete spark ui ingress resulted in exception: '
                                               '(Failed to delete ingress)\nReason: None\n')

    @gen_test
    def test_trying_to_delete_non_existent_job_returns_404_with_reason(self):
        # Arrange
        body = {'job_name': 'test-spark-job'}
        self.mock_k8s_adapter.delete_namespaced_custom_object.side_effect = ApiException(status=404, reason="Not Found")
        # Act
        with pytest.raises(HTTPError) as exception:
            yield self.send_request(body)
        assert exception.value.response.code == 404
        msg = json.loads(exception.value.response.body, encoding='utf-8')['data']
        assert msg == 'Kubernetes error when trying to delete job "test-spark-job": Not Found'
