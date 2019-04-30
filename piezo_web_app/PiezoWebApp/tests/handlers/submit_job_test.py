import json
import pytest

from mock import call
from tornado.testing import gen_test
from tornado.httpclient import HTTPError

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
        self.mock_spark_job_service.submit_job.return_value = {
            'status': StatusCodes.Bad_request.value,
            'message': 'The following errors were found:\nMissing required input \"name\"\n',
        }
        yield self.assert_request_returns_400(body)
        self.mock_logger.debug.assert_has_calls([
            call('Trying to submit job "None".'),
            call('Submitting job "None" returned status code "400".')
        ])

    @gen_test
    def test_post_returns_400_when_language_is_missing(self):
        body = {'name': 'example-spark-job', '': '/path/to/main/app.file'}
        self.mock_spark_job_service.submit_job.return_value = {
            'status': StatusCodes.Bad_request.value,
            'message': 'The following errors were found:\nMissing required input \"language\"\n',
        }
        yield self.assert_request_returns_400(body)
        self.mock_logger.debug.assert_has_calls([
            call('Trying to submit job "example-spark-job".'),
            call('Submitting job "example-spark-job" returned status code "400".')
        ])

    @gen_test
    def test_post_returns_400_when_path_to_main_app_file_is_missing(self):
        body = {'name': 'example-spark-job', 'language': 'example-language'}
        self.mock_spark_job_service.submit_job.return_value = {
            'status': StatusCodes.Bad_request.value,
            'message': 'The following errors were found:\nMissing required input \"main_app_file\"\n',
        }
        yield self.assert_request_returns_400(body)
        self.mock_logger.debug.assert_has_calls([
            call('Trying to submit job "example-spark-job".'),
            call('Submitting job "example-spark-job" returned status code "400".')
        ])

    @gen_test
    def test_post_returns_confirmation_of_submit_when_successful(self):
        # Arrange
        body = {
            'name': 'test-spark-job',
            'language': 'test-language',
            'path_to_main_app_file': '/path/to/main/app.file'
        }
        self.mock_spark_job_service.submit_job.return_value = {
            'status': StatusCodes.Okay.value,
            'message': 'Job driver created successfully',
            'driver_name': 'test-spark-job-driver',
            'spark_ui': 'some.url'
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
        assert response_body['data']['spark_ui'] == 'some.url'

    @gen_test
    def test_post_accepts_optional_inputs(self):
        # Arrange
        body = {
            'name': 'test-spark-job',
            'language': 'test-language',
            'path_to_main_app_file': '/path/to/main/app.file',
            'driver_cores': '1',
            'driver_core_limit': '1000m',
            'driver_memory': '1024m',
            'executors': '5',
            'executor_core_limit': '4000m',
            'arguments': ["arg1", "arg2", 10],
            'lable': 'my_label'
        }
        self.mock_spark_job_service.submit_job.return_value = {
            'status': StatusCodes.Okay.value,
            'message': 'Job driver created successfully',
            'driver_name': 'test-spark-job-driver',
            'spark_ui': 'some.url'
        }
        # Act
        response_body, response_code = yield self.send_request(body)
        # Assert
        self.mock_spark_job_service.submit_job.assert_called_once_with(body)
        assert response_code == 200

    @gen_test
    def test_post_returns_400_error_when_optional_string_inputs_are_not_strings(self):
        # Arrange
        body = {
            'name': 'test-spark-job',
            'language': 'test-language',
            'path_to_main_app_file': '/path/to/main/app.file',
            'driver_cores': 0.8,
            'driver_memory': 1024
        }
        self.mock_spark_job_service.submit_job.return_value = {
            'status': StatusCodes.Okay.value,
            'message': 'Job driver created successfully',
            'driver_name': 'test-spark-job-driver',
            'spark_ui': 'some.url'
        }
        # Act
        yield self.assert_request_returns_400(body)
        # Assert
        self.mock_spark_job_service.submit_job.assert_not_called()

    @gen_test
    def test_post_returns_400_error_when_optional_array_inputs_are_not_arrays(self):
        # Arrange
        body = {
            'name': 'test-spark-job',
            'language': 'test-language',
            'path_to_main_app_file': '/path/to/main/app.file',
            'arguments': 11
        }
        self.mock_spark_job_service.submit_job.return_value = {
            'status': StatusCodes.Okay.value,
            'message': 'Job driver created successfully',
            'driver_name': 'test-spark-job-driver',
            'spark_ui': 'some.url'
        }
        # Act
        yield self.assert_request_returns_400(body)
        # Assert
        self.mock_spark_job_service.submit_job.assert_not_called()

    @gen_test
    def test_post_accepts_unrecognised_input_as_string(self):
        # The handler input schema does not reject this, and so it becomes the responsibility of the validation service.
        # See integration tests for submitting jobs.
        body = {
            'name': 'example-spark-job',
            'language': 'example-language',
            'path_to_main_app_file': '/path/to/main/app.file',
            'dummy-key': 'dummy-value'
        }
        self.mock_spark_job_service.submit_job.return_value = {
            'status': StatusCodes.Okay.value,
            'message': 'Job driver created successfully',
            'driver_name': 'test-spark-job-driver',
            'spark_ui': 'some.url'
        }
        # Act
        response_body, response_code = yield self.send_request(body)
        # Assert
        self.mock_spark_job_service.submit_job.assert_called_once_with(body)
        assert response_code == 200

    @gen_test
    def test_post_accepts_unrecognised_input_as_non_string(self):
        # The handler input schema does not reject this, and so it becomes the responsibility of the validation service.
        # See integration tests for submitting jobs.
        body = {
            'name': 'example-spark-job',
            'language': 'example-language',
            'path_to_main_app_file': '/path/to/main/app.file',
            'dummy-key': 12
        }
        self.mock_spark_job_service.submit_job.return_value = {
            'status': StatusCodes.Okay.value,
            'message': 'Job driver created successfully',
            'driver_name': 'test-spark-job-driver',
            'spark_ui': 'some.url'
        }
        # Act
        response_body, response_code = yield self.send_request(body)
        # Assert
        self.mock_spark_job_service.submit_job.assert_called_once_with(body)
        assert response_code == 200

    @gen_test
    def test_post_returns_input_malformed_message_if_no_body_provided(self):
        # Act
        with pytest.raises(HTTPError) as error:
            yield self.send_request_without_body()
        assert error.value.response.code == 400
        msg = json.loads(error.value.response.body, encoding='utf-8')['data']
        assert msg == 'Input is malformed; could not decode JSON object.'
