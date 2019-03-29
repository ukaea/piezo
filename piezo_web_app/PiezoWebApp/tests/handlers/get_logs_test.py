import json
import pytest

from mock import call
from tornado.testing import gen_test
from tornado.httpclient import HTTPError

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
        body = {}
        yield self.assert_request_returns_400(body)

    @gen_test
    def test_get_returns_logs_when_successful(self):
        # Arrange
        body = {'job_name': 'test-job'}
        self.mock_spark_job_service.get_logs.return_value = {
            "message": "logs",
            "status": 200
        }
        # Act
        response_body, response_code = yield self.send_request(body)
        # Assert
        self.mock_spark_job_service.get_logs.assert_called_once_with('test-job')
        self.mock_logger.debug.assert_has_calls([
            call('Trying to get logs from spark job "test-job".'),
            call('Getting logs from spark job "test-job" returned result "200".')
        ])
        assert response_code == 200
        self.assertDictEqual(response_body, {
            'status': 'success',
            'data': {
                'message': 'logs'
            }
        })

    @gen_test
    def test_get_returns_input_malformed_message_if_no_body_provided(self):
        # Act
        with pytest.raises(HTTPError) as error:
            yield self.send_request_without_body()
        assert error.value.response.code == 400
        msg = json.loads(error.value.response.body, encoding='utf-8')['data']
        assert msg == 'Input is malformed; could not decode JSON object.'
