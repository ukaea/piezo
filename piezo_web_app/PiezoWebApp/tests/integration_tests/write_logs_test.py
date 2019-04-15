import json
import pytest

from kubernetes.client.rest import ApiException

from tornado.testing import gen_test
from tornado.httpclient import HTTPError

from PiezoWebApp.src.handlers.write_logs_handler import WriteLogsHandler
from PiezoWebApp.tests.integration_tests.base_integration_test import BaseIntegrationTest


class TestWriteLogsToFileIntegration(BaseIntegrationTest):
    @property
    def handler(self):
        return WriteLogsHandler

    @property
    def standard_request_method(self):
        return 'POST'

    @gen_test
    def test_logs_from_k8s_written_to_storage(self):
        # Arrange
        body = {'job_name': 'test-job'}
        self.mock_k8s_adapter.read_namespaced_pod_log.return_value = 'Log\nFile\nContent'
        self.mock_storage_adapter.set_contents_from_string.return_value = 12345
        # Act
        response_body, response_code = yield self.send_request(body)
        # Assert
        self.mock_k8s_adapter.read_namespaced_pod_log.assert_called_once_with('test-job-driver', 'default')
        self.mock_storage_adapter.set_contents_from_string.assert_called_once_with(
            'kubernetes', 'outputs/test-job/log.txt', 'Log\nFile\nContent')
        assert response_code == 200
        self.assertDictEqual(response_body, {
            'status': 'success',
            'data': {'message': 'Logs written to "outputs/test-job/log.txt"'}
        })

    @gen_test
    def test_trying_to_get_status_of_non_existent_job_returns_404_with_reason(self):
        # Arrange
        body = {'job_name': 'test-spark-job'}
        self.mock_k8s_adapter.read_namespaced_pod_log.side_effect = ApiException(status=404, reason="Not Found")
        # Act
        with pytest.raises(HTTPError) as exception:
            yield self.send_request(body)
        assert exception.value.response.code == 404
        msg = json.loads(exception.value.response.body, encoding='utf-8')['data']
        assert msg == 'Kubernetes error when trying to get logs for spark job "test-spark-job": Not Found'
