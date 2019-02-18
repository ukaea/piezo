from mock import call
from tornado.testing import gen_test

from PiezoWebApp.tests.handlers.base_handler_test import BaseHandlerTest
from PiezoWebApp.src.handlers.delete_job import DeleteJobHandler


class DeleteJobHandlerTest(BaseHandlerTest):
    @property
    def handler(self):
        return DeleteJobHandler

    @property
    def standard_request_method(self):
        return 'DELETE'

    @gen_test
    def test_delete_returns_400_when_job_name_is_missing(self):
        body = {'namespace': 'test-namespace'}
        yield self.assert_request_returns_400(body)

    @gen_test
    def test_delete_returns_400_when_namespace_is_missing(self):
        body = {'job_name': 'test-spark-job'}
        yield self.assert_request_returns_400(body)

    @gen_test
    def test_delete_returns_success_confirmation_when_successful(self):
        # Arrange
        body = {'job_name': 'test-spark-job', 'namespace': 'test-namespace'}
        self.mock_kubernetes_service.delete_job.return_value = \
            '{"message": "test-spark-job deleted from namespace test-namespace"}'
        # Act
        response_body, response_code = yield self.send_request(body)
        # Assert
        self.mock_kubernetes_service.delete_job.assert_called_once_with('test-spark-job', 'test-namespace')
        self.mock_logger.debug.assert_has_calls([
            call('Trying to delete job "test-spark-job" in namespace "test-namespace".'),
            call('Deleting job "test-spark-job" in namespace "test-namespace" returned result '
                 '"{"message": "test-spark-job deleted from namespace test-namespace"}".')
        ])
        assert response_code == 200
        assert response_body['status'] == 'success'
        assert response_body['data'] == '{"message": "test-spark-job deleted from namespace test-namespace"}'
