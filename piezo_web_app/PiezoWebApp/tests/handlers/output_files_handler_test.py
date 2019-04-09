import json
import pytest

from mock import call
from tornado.httpclient import HTTPError
from tornado.testing import gen_test

from PiezoWebApp.src.handlers.output_files_handler import OutputFilesHandler
from PiezoWebApp.src.models.return_status import StatusCodes

from PiezoWebApp.tests.handlers.base_handler_test import BaseHandlerTest


class TestOutputFilesHandler(BaseHandlerTest):
    @property
    def handler(self):
        return OutputFilesHandler

    @property
    def standard_request_method(self):
        return 'GET'

    @gen_test
    def test_get_returns_400_when_job_name_is_missing(self):
        body = {}
        yield self.assert_request_returns_400(body)

    @gen_test
    def test_get_returns_urls_when_successful(self):
        # Arrange
        body = {'job_name': 'test-job-abc12'}
        self.mock_spark_job_service.get_output_files_temp_urls.return_value = {
            'status': StatusCodes.Okay.value,
            'message': 'Got temporary URLs for 3 output files for job "test-job-abc12"',
            'files': {
                'log.txt': 's3://log.txt.temp.url',
                'output1.csv': 's3://output1.csv.temp.url',
                'output2.csv': 's3://output2.csv.temp.url'
            }
        }
        # Act
        response_body, response_code = yield self.send_request(body)
        # Assert
        self.mock_spark_job_service.get_output_files_temp_urls.assert_called_once_with('test-job-abc12')
        self.mock_logger.debug.assert_has_calls([
            call('Trying to get output files for spark job "test-job-abc12".'),
            call('Getting output files for spark job "test-job-abc12" returned result "200".')
        ])
        assert response_code == 200
        self.assertDictEqual(response_body, {
            'status': 'success',
            'data': {
                'message': 'Got temporary URLs for 3 output files for job "test-job-abc12"',
                'files': {
                    'log.txt': 's3://log.txt.temp.url',
                    'output1.csv': 's3://output1.csv.temp.url',
                    'output2.csv': 's3://output2.csv.temp.url'
                }
            }
        })

    @gen_test
    def test_get_returns_404_when_no_files_found(self):
        # Arrange
        body = {'job_name': 'test-job-abc12'}
        self.mock_spark_job_service.get_output_files_temp_urls.return_value = {
            'status': StatusCodes.Not_found.value,
            'message': 'Got temporary URLs for 0 output files for job "test-job-abc12"',
            'files': {}
        }
        # Act
        with pytest.raises(HTTPError) as error:
            yield self.send_request(body)
        # Assert
        self.mock_spark_job_service.get_output_files_temp_urls.assert_called_once_with('test-job-abc12')
        self.mock_logger.debug.assert_has_calls([
            call('Trying to get output files for spark job "test-job-abc12".'),
            call('Getting output files for spark job "test-job-abc12" returned result "404".')
        ])
        assert error.value.response.code == 404
        msg = json.loads(error.value.response.body, encoding='utf-8')['data']
        assert msg == 'Got temporary URLs for 0 output files for job "test-job-abc12"'
