from mock import call
from tornado.testing import gen_test

from PiezoWebApp.tests.handlers.base_handler_test import BaseHandlerTest
from PiezoWebApp.src.handlers.submit_job import SubmitJobHandler
from PiezoWebApp.src.models.return_status import StatusCodes


class TestSubmitJobHandler(BaseHandlerTest):
    @property
    def handler(self):
        return SubmitJobHandler

    @property
    def standard_request_method(self):
        return 'POST'

    @gen_test
    def test_post_returns_400_when_name_is_missing(self):
        body = {'language': 'example-language', 'path_to_main_app_file': '/path/to/main/app.file'}
        yield self.assert_request_returns_400(body)

    @gen_test
    def test_post_returns_400_when_language_is_missing(self):
        body = {'name': 'example-spark-job', 'path_to_main_app_file': '/path/to/main/app.file'}
        yield self.assert_request_returns_400(body)

    @gen_test
    def test_post_returns_400_when_path_to_main_app_file_is_missing(self):
        body = {'name': 'example-spark-job', 'language': 'example-language'}
        yield self.assert_request_returns_400(body)

    @gen_test
    def test_post_returns_confirmation_of_submit_when_successful(self):
        # Arrange
        body = {
            'name': 'test-spark-job',
            'language': 'test-language',
            'path_to_main_app_file': '/path/to/main/app.file'
        }
        self.mock_spark_job_service.submit_job.return_value = {
            'status': StatusCodes.Okay,
            'message': 'Job driver created successfully',
            'driver_name': 'test-spark-job-driver'
        }
        # Act
        response_body, response_code = yield self.send_request(body)
        # Assert
        self.mock_spark_job_service.submit_job.assert_called_once_with(body)
        self.mock_logger.debug.assert_has_calls([
            call('Trying to submit job "test-spark-job".'),
            call('Submitting job "test-spark-job" returned status code "200".')
        ])
        assert response_code == 200
        assert response_body['status'] == 'success'
        assert response_body['data']['message'] == 'Job driver created successfully'
        assert response_body['data']['driver_name'] == 'test-spark-job-driver'
