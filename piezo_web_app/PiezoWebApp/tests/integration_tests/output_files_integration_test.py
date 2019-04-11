import json
import pytest

from tornado.httpclient import HTTPError
from tornado.testing import gen_test

from PiezoWebApp.src.handlers.output_files_handler import OutputFilesHandler

from PiezoWebApp.tests.integration_tests.base_integration_test import BaseIntegrationTest


class OutputFilesIntegrationTest(BaseIntegrationTest):
    @property
    def handler(self):
        return OutputFilesHandler

    @property
    def standard_request_method(self):
        return 'GET'

    @gen_test
    def test_get_returns_urls_when_successful(self):
        # Arrange
        body = {'job_name': 'test-job-abc12'}
        self.mock_storage_adapter.get_temp_url_for_each_file.return_value = {
            'outputs/test-job-abc12/log.txt': 'http://log.txt.temp.url',
            'outputs/test-job-abc12/output1.csv': 'http://output1.csv.temp.url',
            'outputs/test-job-abc12/output2.csv': 'http://output2.csv.temp.url'
        }
        # Act
        response_body, response_code = yield self.send_request(body)
        # Assert
        self.mock_storage_adapter.get_temp_url_for_each_file.assert_called_once_with(
            'kubernetes', 'outputs/test-job-abc12/')
        assert response_code == 200
        self.assertDictEqual(response_body, {
            'status': 'success',
            'data': {
                'message': 'Got temporary URLs for 3 output files for job "test-job-abc12"',
                'files': {
                    'log.txt': 'http://log.txt.temp.url',
                    'output1.csv': 'http://output1.csv.temp.url',
                    'output2.csv': 'http://output2.csv.temp.url'
                }
            }
        })

    @gen_test
    def test_get_returns_404_when_no_files_found(self):
        # Arrange
        body = {'job_name': 'test-job-abc12'}
        self.mock_storage_adapter.get_temp_url_for_each_file.return_value = {}
        # Act
        with pytest.raises(HTTPError) as error:
            yield self.send_request(body)
        # Assert
        self.mock_storage_adapter.get_temp_url_for_each_file.assert_called_once_with(
            'kubernetes', 'outputs/test-job-abc12/')
        assert error.value.response.code == 404
        msg = json.loads(error.value.response.body, encoding='utf-8')['data']
        assert msg == 'Got temporary URLs for 0 output files for job "test-job-abc12"'
