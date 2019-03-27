import json
import pytest
from tornado.httpclient import HTTPClientError
from tornado.testing import gen_test
from kubernetes.client.rest import ApiException
from PiezoWebApp.src.handlers.get_logs import GetLogsHandler
from PiezoWebApp.tests.integration_tests.base_integration_test import BaseIntegrationTest

# str | The custom resource's group name
CRD_GROUP = 'sparkoperator.k8s.io'

# str | The custom resource's plural name. For TPRs this would be lowercase plural kind.
CRD_PLURAL = 'sparkapplications'

# str | The custom resource's version
CRD_VERSION = 'v1beta1'

NAMESPACE = 'default'


class GetLogsIntegrationTest(BaseIntegrationTest):
    @property
    def handler(self):
        return GetLogsHandler

    @property
    def standard_request_method(self):
        return "GET"

    @gen_test
    def test_logs_are_returned_from_correct_spark_job(self):
        # Arrange
        body = {'job_name': 'test-spark-job'}
        kubernetes_response = 'Some logs'
        self.mock_k8s_adapter.read_namespaced_pod_log.return_value = kubernetes_response
        # Act
        response_body, response_code = yield self.send_request(body)
        # Assert
        assert self.mock_k8s_adapter.read_namespaced_pod_log.call_count == 1
        self.mock_k8s_adapter.read_namespaced_pod_log.assert_called_once_with('test-spark-job-driver', NAMESPACE)
        assert response_code == 200
        self.assertDictEqual(response_body, {
            'status': 'success',
            'data': {
                'message': 'Some logs'
            }})


    @gen_test
    def test_trying_to_get_logs_from_non_existent_spark_job_returns_404(self):
        # Arrange
        body = {'job_name': 'test-spark-job'}
        self.mock_k8s_adapter.read_namespaced_pod_log.side_effect = ApiException(status=404, reason="Not Found")
        # Act
        with pytest.raises(HTTPClientError) as exception:
            yield self.send_request(body)
        assert exception.value.response.code == 404
        msg = json.loads(exception.value.response.body, encoding='utf-8')['data']
        assert msg == 'Kubernetes error when trying to get logs for spark job "test-spark-job": Not Found'
