from mock import call
from tornado.testing import gen_test

from PiezoWebApp.tests.handlers.base_handler_test import BaseHandlerTest
from PiezoWebApp.src.handlers.get_jobs import GetJobsHandler


class TestGetJobsHandler(BaseHandlerTest):
    @property
    def handler(self):
        return GetJobsHandler

    @property
    def standard_request_method(self):
        return 'GET'

    @gen_test
    def test_get_returns_array_of_jobs_when_successful(self):
        # Arrange
        self.mock_spark_job_service.get_jobs.return_value = {
            "message": "Found 3 spark jobs",
            "spark_jobs": {"job_1": "COMPLETED", "job_2": "RUNNING", "job_3": "PENDING"},
            "status": 200
        }
        body = {}
        # Act
        response_body, response_code = yield self.send_request(body)
        # Assert
        self.mock_spark_job_service.get_jobs.assert_called_once()
        self.mock_logger.debug.assert_has_calls([
            call('Getting list of spark applications with label "ALL" returned: "200".')
        ])
        assert response_code == 200
        self.assertDictEqual(response_body, {
            'status': 'success',
            'data': {
                'message': "Found 3 spark jobs",
                'spark_jobs': {'job_1': "COMPLETED", "job_2": "RUNNING", "job_3": "PENDING"}
            }
        })

    @gen_test
    def test_get_returns_empty_array_when_no_jobs_present(self):
        # Arrange
        self.mock_spark_job_service.get_jobs.return_value = {
            "message": "Found 0 spark jobs",
            "spark_jobs": {},
            "status": 200
        }
        body = {}
        # Act
        response_body, response_code = yield self.send_request(body)
        # Assert
        self.mock_spark_job_service.get_jobs.assert_called_once()
        self.mock_logger.debug.assert_has_calls([
            call('Getting list of spark applications with label "ALL" returned: "200".')
        ])
        assert response_code == 200
        self.assertDictEqual(response_body, {
            'status': 'success',
            'data': {
                'message': "Found 0 spark jobs",
                'spark_jobs': {}
            }
        })
