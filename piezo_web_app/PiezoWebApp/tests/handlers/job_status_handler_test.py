import json
import pytest

from mock import call
from tornado.httpclient import HTTPClientError
from tornado.testing import gen_test

from PiezoWebApp.tests.handlers.base_handler_test import BaseHandlerTest
from PiezoWebApp.src.handlers.job_status import JobStatusHandler


class TestJobStatusHandler(BaseHandlerTest):
    @property
    def handler(self):
        return JobStatusHandler

    @property
    def standard_request_method(self):
        return 'GET'

    @gen_test
    def test_get_returns_400_when_job_name_is_missing(self):
        body = {}
        yield self.assert_request_returns_400(body)

    @gen_test
    def test_get_returns_status_when_successful(self):
        # Arrange
        body = {'job_name': 'test-job'}
        self.mock_spark_job_service.get_job_status.return_value = {
            "message": "status",
            "status": 200,
            "job_status": "RUNNING",
            "created": 123456,
            "submission_attempts": 1,
            "last_submitted": 123455,
            "terminated": 1234567,
            "error_messages": ""
        }
        # Act
        response_body, response_code = yield self.send_request(body)
        # Assert
        self.mock_spark_job_service.get_job_status.assert_called_once_with('test-job')
        self.mock_logger.debug.assert_has_calls([
            call('Trying to get status of spark job "test-job".'),
            call('Getting status of spark job "test-job" returned '
                 'result "200".')
        ])
        assert response_code == 200
        self.assertDictEqual(response_body, {
            'status': 'success',
            'data': {
                'message': 'status',
                "job_status": "RUNNING",
                "created": 123456,
                "submission_attempts": 1,
                "last_submitted": 123455,
                "terminated": 1234567,
                "error_messages": ""

            }
        })

    @gen_test
    def test_get_returns_message_and_status_code_when_k8s_error(self):
        # Arrange
        body = {'job_name': 'test-job'}
        self.mock_spark_job_service.get_job_status.return_value = {
            "message": "Kubernetes error",
            "status": 404
        }
        # Act
        with pytest.raises(HTTPClientError) as error:
            yield self.send_request(body)
        assert error.value.response.code == 404
        msg = json.loads(error.value.response.body, encoding='utf-8')['data']
        assert msg == "Kubernetes error"

    @gen_test
    def test_get_returns_input_malformed_message_if_no_body_provided(self):
        # Act
        with pytest.raises(HTTPClientError) as error:
            yield self.send_request_without_body()
        assert error.value.response.code == 400
        msg = json.loads(error.value.response.body, encoding='utf-8')['data']
        assert msg == 'Input is malformed; could not decode JSON object.'
