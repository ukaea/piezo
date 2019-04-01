import json
from mock import call
import pytest
from tornado.httpclient import HTTPError
from tornado.testing import gen_test

from PiezoWebApp.tests.handlers.base_handler_test import BaseHandlerTest
from PiezoWebApp.src.handlers.delete_job import DeleteJobHandler


class TestDeleteJobHandler(BaseHandlerTest):
    @property
    def handler(self):
        return DeleteJobHandler

    @property
    def standard_request_method(self):
        return 'DELETE'

    @gen_test
    def test_delete_returns_400_when_job_name_is_missing(self):
        body = {}
        yield self.assert_request_returns_400(body)

    @gen_test
    def test_delete_returns_success_confirmation_when_successful(self):
        # Arrange
        body = {'job_name': 'test-spark-job'}
        self.mock_spark_job_service.delete_job.return_value = {
            "message": "test-spark-job deleted",
            'status': 200
        }
        # Act
        response_body, response_code = yield self.send_request(body)
        # Assert
        self.mock_spark_job_service.delete_job.assert_called_once_with('test-spark-job')
        self.mock_logger.debug.assert_has_calls([
            call('Trying to delete job "test-spark-job".'),
            call('Deleting job "test-spark-job" returned result "200".')
        ])
        assert response_code == 200
        self.assertDictEqual(response_body, {
            'status': 'success',
            'data': {
                'message': "test-spark-job deleted"
            }
        })

    @gen_test
    def test_delete_returns_message_and_status_code_when_k8s_error(self):
        # Arrange
        body = {'job_name': 'test-spark-job'}
        self.mock_spark_job_service.delete_job.return_value = {
            "message": "Kubernetes error",
            'status': 422
        }
        # Act
        with pytest.raises(HTTPError) as error:
            yield self.send_request(body)
        assert error.value.response.code == 422
        msg = json.loads(error.value.response.body, encoding='utf-8')['data']
        assert msg == "Kubernetes error"

    @gen_test
    def test_delete_returns_input_malformed_message_if_no_body_provided(self):
        # Act
        with pytest.raises(HTTPError) as error:
            yield self.send_request_without_body()
        assert error.value.response.code == 400
        msg = json.loads(error.value.response.body, encoding='utf-8')['data']
        assert msg == 'Input is malformed; could not decode JSON object.'
