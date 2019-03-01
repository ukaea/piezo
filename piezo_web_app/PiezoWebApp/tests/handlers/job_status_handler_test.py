from mock import call
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
        body = {'namespace': 'test-namespace'}
        yield self.assert_request_returns_400(body)

    @gen_test
    def test_get_returns_400_when_namespace_is_missing(self):
        body = {'spark_job': 'test-driver'}
        yield self.assert_request_returns_400(body)

    @gen_test
    def test_get_returns_status_when_successful(self):
        # Arrange
        body = {'spark_job': 'test-job', 'namespace': 'test-namespace'}
        self.mock_spark_job_service.get_job_status.return_value = {
            "message": "status",
            "status": 200
        }
        # Act
        response_body, response_code = yield self.send_request(body)
        # Assert
        self.mock_spark_job_service.get_job_status.assert_called_once_with('test-job', 'test-namespace')
        self.mock_logger.debug.assert_has_calls([
            call('Trying to get status of spark job "test-job" in namespace "test-namespace".'),
            call('Getting status of spark job "test-job" in namespace "test-namespace" returned '
                 'result "200".')
        ])
        assert response_code == 200
        self.assertDictEqual(response_body, {
            'status': 'success',
            'data': {
                'message': 'status'
            }
        })
