from mock import call
from tornado.testing import gen_test

from PiezoWebApp.tests.handlers.base_handler_test import BaseHandlerTest
from PiezoWebApp.src.handlers.get_logs import GetLogsHandler


class TestGetLogsHandler(BaseHandlerTest):
    @property
    def handler(self):
        return GetLogsHandler

    @property
    def standard_request_method(self):
        return 'GET'

    @gen_test
    def test_get_returns_400_when_driver_name_is_missing(self):
        body = {'namespace': 'test-namespace'}
        yield self.assert_request_returns_400(body)

    @gen_test
    def test_get_returns_400_when_namespace_is_missing(self):
        body = {'driver_name': 'test-driver'}
        yield self.assert_request_returns_400(body)

    @gen_test
    def test_get_returns_logs_when_successful(self):
        # Arrange
        body = {'driver_name': 'test-driver', 'namespace': 'test-namespace'}
        self.mock_kubernetes_service.get_logs.return_value = '{"log": "success"}'
        # Act
        response_body, response_code = yield self.send_request(body)
        # Assert
        self.mock_kubernetes_service.get_logs.assert_called_once_with('test-driver', 'test-namespace')
        self.mock_logger.debug.assert_has_calls([
            call('Trying to delete driver "test-driver" in namespace "test-namespace".'),
            call('Getting logs from driver "test-driver" in namespace "test-namespace" returned result '
                 '"{"log": "success"}".')
        ])
        assert response_code == 200
        assert response_body['status'] == 'success'
        assert response_body['data'] == '{"log": "success"}'
