import json
import pytest
from tornado.httpclient import HTTPClientError
from tornado.testing import gen_test
from kubernetes.client.rest import ApiException

from PiezoWebApp.src.handlers.job_status import JobStatusHandler
from PiezoWebApp.tests.integration_tests.base_integration_test import BaseIntegrationTest


# str | The custom resource's group name
CRD_GROUP = 'sparkoperator.k8s.io'

# str | The custom resource's plural name. For TPRs this would be lowercase plural kind.
CRD_PLURAL = 'sparkapplications'

# str | The custom resource's version
CRD_VERSION = 'v1beta1'

NAMESPACE = 'default'


class TestJobStatusIntegration(BaseIntegrationTest):
    @property
    def handler(self):
        return JobStatusHandler

    @property
    def standard_request_method(self):
        return 'GET'

    @gen_test
    def test_status_is_returned_from_correct_spark_job(self):
        # Arrange
        body = {'job_name': 'test-spark-job'}
        kubernetes_response = {
            'metadata': {
                'creationTimestamp': 12345},
            'status': {
                'applicationState': {'state': 'RUNNING', 'errorMessage': ''},
                'submissionAttempts': 1,
                'lastSubmissionAttemptTime': 123456,
                'terminationTime': 1234567}}
        self.mock_k8s_adapter.get_namespaced_custom_object.return_value = kubernetes_response
        # Act
        response_body, response_code = yield self.send_request(body)
        # Assert
        assert self.mock_k8s_adapter.get_namespaced_custom_object.call_count == 1
        self.mock_k8s_adapter.get_namespaced_custom_object.assert_called_once_with(CRD_GROUP,
                                                                                   CRD_VERSION,
                                                                                   NAMESPACE,
                                                                                   CRD_PLURAL,
                                                                                   'test-spark-job')
        assert response_code == 200
        self.assertDictEqual(response_body, {
            'status': 'success',
            'data': {
                "message": 'Job status for "test-spark-job"',
                "job status": "RUNNING",
                "created": 12345,
                "submission attempts": 1,
                "last submitted": 123456,
                "terminated": 1234567,
                "error messages": ''
            }})

    @gen_test
    def test_unknown_status_is_returned_when_not_specified_by_kubernetes(self):
        # Arrange
        body = {'job_name': 'test-spark-job'}
        kubernetes_response = {
            'metadata': {
                'name': 'test-spark-job',
                'namespace': 'default'
            }
        }
        self.mock_k8s_adapter.get_namespaced_custom_object.return_value = kubernetes_response
        # Act
        response_body, response_code = yield self.send_request(body)
        # Assert
        assert self.mock_k8s_adapter.get_namespaced_custom_object.call_count == 1
        self.mock_k8s_adapter.get_namespaced_custom_object.assert_called_once_with(CRD_GROUP,
                                                                                   CRD_VERSION,
                                                                                   NAMESPACE,
                                                                                   CRD_PLURAL,
                                                                                   'test-spark-job')
        assert response_code == 200
        self.assertDictEqual(response_body, {
            'status': 'success',
            'data': {
                "message": 'Job status for "test-spark-job"',
                "job status": "UNKNOWN",
                "created": "UNKNOWN",
                "submission attempts": "UNKNOWN",
                "last submitted": "UNKNOWN",
                "terminated": "UNKNOWN",
                "error messages": "UNKNOWN"
            }
        })

    @gen_test
    def test_trying_to_get_status_of_non_existent_job_returns_404_with_reason(self):
        # Arrange
        body = {'job_name': 'test-spark-job'}
        self.mock_k8s_adapter.get_namespaced_custom_object.side_effect = ApiException(status=404, reason="Not Found")
        # Act
        with pytest.raises(HTTPClientError) as exception:
            yield self.send_request(body)
        assert exception.value.response.code == 404
        msg = json.loads(exception.value.response.body, encoding='utf-8')['data']
        assert msg == 'Kubernetes error when trying to get status of spark job "test-spark-job": Not Found'
