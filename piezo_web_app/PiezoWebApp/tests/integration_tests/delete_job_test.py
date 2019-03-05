import json
import pytest
from tornado.httpclient import HTTPClientError
from tornado.testing import gen_test
from kubernetes.client.rest import ApiException

from PiezoWebApp.src.handlers.delete_job import DeleteJobHandler
from PiezoWebApp.tests.integration_tests.base_integration_test import BaseIntegrationTest

# str | The custom resource's group name
CRD_GROUP = 'sparkoperator.k8s.io'

# str | The custom resource's plural name. For TPRs this would be lowercase plural kind.
CRD_PLURAL = 'sparkapplications'

# str | The custom resource's version
CRD_VERSION = 'v1beta1'

DELETE_OPTIONS = {'api_version': None,
                  'dry_run': None,
                  'grace_period_seconds': None,
                  'kind': None,
                  'orphan_dependents': None,
                  'preconditions': None,
                  'propagation_policy': None}


class DeleteJobIntegrationTest(BaseIntegrationTest):
    @property
    def handler(self):
        return DeleteJobHandler

    @property
    def standard_request_method(self):
        return 'DELETE'

    @gen_test
    def test_success_message_is_returned_when_job_deleted_successfully(self):
        # Arrange
        body = {"job_name": "test-spark-job", "namespace": "default"}
        kubernetes_response = {'status': 'Success'}
        self.mock_k8s_adapter.delete_namespaced_custom_object.return_value = kubernetes_response
        # Act
        response_body, response_code = yield self.send_request(body)
        # Assert
        assert self.mock_k8s_adapter.delete_namespaced_custom_object.call_count == 1
        self.mock_k8s_adapter.delete_namespaced_custom_object.assert_called_once_with(CRD_GROUP,
                                                                                      CRD_VERSION,
                                                                                      'default',
                                                                                      CRD_PLURAL,
                                                                                      'test-spark-job',
                                                                                      DELETE_OPTIONS)
        assert response_code == 200
        self.assertDictEqual(response_body, {
            'status': 'success',
            'data': {
                'message': 'test-spark-job deleted from namespace default'
            }
        })

    @gen_test
    def test_trying_to_delete_non_existent_job_returns_404_with_reason(self):
        # Arrange
        body = {'job_name': 'test-spark-job', 'namespace': 'default'}
        self.mock_k8s_adapter.delete_namespaced_custom_object.side_effect = ApiException(status=404, reason="Not Found")
        # Act
        with pytest.raises(HTTPClientError) as exception:
            yield self.send_request(body)
        assert exception.value.response.code == 404
        msg = json.loads(exception.value.response.body, encoding='utf-8')['data']
        assert msg == 'Kubernetes error when trying to delete job "test-spark-job" in' \
                      ' namespace "default": Not Found'
