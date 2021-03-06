import json
import pytest

from mock import call
from tornado.httpclient import HTTPError
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
        self.mock_spark_job_service.get_jobs.assert_called_once_with(None)
        self.mock_logger.debug.assert_has_calls([
            call('Getting list of all spark applications returned: "200".')
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
        self.mock_spark_job_service.get_jobs.assert_called_once_with(None)
        self.mock_logger.debug.assert_has_calls([
            call('Getting list of all spark applications returned: "200".')
        ])
        assert response_code == 200
        self.assertDictEqual(response_body, {
            'status': 'success',
            'data': {
                'message': "Found 0 spark jobs",
                'spark_jobs': {}
            }
        })

    @gen_test
    def test_get_accepts_label_argument(self):
        # Arrange
        self.mock_spark_job_service.get_jobs.return_value = {
            "message": "Found 2 spark jobs",
            "spark_jobs": {"job_1": "COMPLETED", "job_3": "PENDING"},
            "status": 200
        }
        body = {"label": "test-label"}
        # Act
        response_body, response_code = yield self.send_request(body)
        # Assert
        self.mock_spark_job_service.get_jobs.assert_called_once_with("test-label")
        self.mock_logger.debug.assert_has_calls([
            call('Getting list of spark applications with label "test-label" returned: "200".')
        ])
        assert response_code == 200
        self.assertDictEqual(response_body, {
            'status': 'success',
            'data': {
                'message': "Found 2 spark jobs",
                'spark_jobs': {"job_1": "COMPLETED", "job_3": "PENDING"}
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
