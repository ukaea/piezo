from mock import call
from tornado.testing import gen_test

from PiezoWebApp.tests.handlers.base_handler_test import BaseHandlerTest
from PiezoWebApp.src.handlers.write_logs_handler import WriteLogsHandler


class TestWriteLogsHandler(BaseHandlerTest):
    @property
    def handler(self):
        return WriteLogsHandler

    @property
    def standard_request_method(self):
        return 'POST'

    @gen_test
    def test_post_returns_400_when_driver_name_is_missing(self):
        body = {}
        yield self.assert_request_returns_400(body)

    @gen_test
    def test_post_returns_logs_when_successful(self):
        # Arrange
        body = {'job_name': 'test-job'}
        self.mock_spark_job_service.write_logs_to_file.return_value = {
            'message': 'Job logs written to "/path/to/log.txt"',
            'status': 200
        }
        # Act
        response_body, response_code = yield self.send_request(body)
        # Assert
        self.mock_spark_job_service.write_logs_to_file.assert_called_once_with('test-job')
        self.mock_logger.debug.assert_has_calls([
            call('Trying to write logs to file for job "test-job".'),
            call('Writing logs to file for job "test-job" returned status code "200".')
        ])
        assert response_code == 200
        self.assertDictEqual(response_body, {
            'status': 'success',
            'data': {
                'message': 'Job logs written to "/path/to/log.txt"'
            }
        })
