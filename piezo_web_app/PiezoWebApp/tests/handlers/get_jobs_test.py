from mock import call
from tornado.testing import gen_test

from PiezoWebApp.tests.handlers.base_handler_test import BaseHandlerTest
from PiezoWebApp.src.handlers.get_jobs import GetJobsHandler


class TestGetLogsHandler(BaseHandlerTest):
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
            "message": "The following spark applications were found: [job1, job2, job3]",
            "status": 200
        }
        body = None
        # Act
        response_body, response_code = yield self.send_request(body)
        # Assert
        self.mock_spark_job_service.get_jobs.assert_called_once()
        self.mock_logger.debug.assert_has_calls([
            call('Getting list of spark applications present returned: "200".')
        ])
        assert response_code == 200
        self.assertDictEqual(response_body, {
            'status': 'success',
            'data': {
                'message': "The following spark applications were found: [job1, job2, job3]"
            }
        })

    @gen_test
    def test_get_returns_empty_array_when_no_jobs_present(self):
        # Arrange
        self.mock_spark_job_service.get_jobs.return_value = {
            "message": "The following spark applications were found: []",
            "status": 200
        }
        body = None
        # Act
        response_body, response_code = yield self.send_request(body)
        # Assert
        self.mock_spark_job_service.get_jobs.assert_called_once()
        self.mock_logger.debug.assert_has_calls([
            call('Getting list of spark applications present returned: "200".')
        ])
        assert response_code == 200
        self.assertDictEqual(response_body, {
            'status': 'success',
            'data': {
                'message': "The following spark applications were found: []"
            }
        })
