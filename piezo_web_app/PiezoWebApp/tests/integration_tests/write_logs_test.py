from tornado.testing import gen_test

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
        body = {'job_name': 'test-job', 'namespace': 'default'}
        self.mock_k8s_adapter.read_namespaced_pod_log.return_value = 'Log\nFile\nContent'
        # Act
        response_body, response_code = yield self.send_request(body)
        # Assert
        self.mock_k8s_adapter.read_namespaced_pod_log.assert_called_once_with('test-job-driver', 'default')
        self.mock_storage_adapter.set_contents_from_string.assert_called_once_with(
            'kubernetes', 'outputs/test-job/log.txt', 'Log\nFile\nContent')
        assert response_code == 200
        self.assertDictEqual(response_body, {
            'status': 'success',
            'data': {'message': 'Logs written to "outputs/test-job/log.txt" in bucket "kubernetes"'}
        })
