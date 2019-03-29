import json
import pytest

from mock import call
from tornado.httpclient import HTTPClientError
from tornado.testing import gen_test

from PiezoWebApp.tests.handlers.base_handler_test import BaseHandlerTest
from PiezoWebApp.src.handlers.tidy_jobs import TidyJobsHandler


class TestGetJobsHandler(BaseHandlerTest):
    @property
    def handler(self):
        return TidyJobsHandler

    @property
    def standard_request_method(self):
        return 'POST'

    @gen_test
    def test_get_summary_of_tidy_process_successful(self):
        # Arrange
        self.mock_spark_job_service.tidy_jobs.return_value = {
            'status': 200,
            'message': 'x Spark jobs found',
            'jobs_tidied': {'some job': 'some status'},
            'jobs_skipped': {'some job': 'some status'},
            'jobs_failed_to_process': {'some job': 'some reason'}}
        # Act
        response_body, response_code = yield self.send_request_without_body()
        # Assert
        self.mock_spark_job_service.tidy_jobs.assert_called_once_with()
        self.mock_logger.debug.assert_has_calls([
            call('Tidying spark application returned: "200".')
        ])
        assert response_code == 200
        self.assertDictEqual(response_body, {
            'status': 'success',
            'data': {
                'message': 'x Spark jobs found',
                'jobs_tidied': {'some job': 'some status'},
                'jobs_skipped': {'some job': 'some status'},
                'jobs_failed_to_process': {'some job': 'some reason'}
            }
        })
