from tornado.testing import gen_test

from PiezoWebApp.src.handlers.get_jobs import GetJobsHandler
from PiezoWebApp.tests.integration_tests.base_integration_test import BaseIntegrationTest


# str | The custom resource's group name
CRD_GROUP = 'sparkoperator.k8s.io'

# str | The custom resource's plural name. For TPRs this would be lowercase plural kind.
CRD_PLURAL = 'sparkapplications'

# str | The custom resource's version
CRD_VERSION = 'v1beta1'


class TestGetJobsIntegration(BaseIntegrationTest):
    @property
    def handler(self):
        return GetJobsHandler

    @property
    def standard_request_method(self):
        return 'GET'

    @gen_test
    def test_list_of_current_jobs_is_returned_as_array(self):
        # Arrange
        body = None
        kubernetes_response = {"items": [
            {
                "metadata":
                    {"name": "job1"},
                "status":
                    {"applicationState":
                         {"state": "RUNNING"}}
            },
            {
                "metadata":
                    {"name": "job2"},
                "status":
                    {"applicationState":
                         {"state": "COMPLETED"}}
            }
        ]}
        self.mock_k8s_adapter.list_namespaced_custom_object.return_value = kubernetes_response
        # Act
        response_body, response_code = yield self.send_request(body)
        # Assert
        assert self.mock_k8s_adapter.list_namespaced_custom_object.call_count == 1
        self.mock_k8s_adapter.list_namespaced_custom_object.assert_called_once_with(CRD_GROUP,
                                                                                    CRD_VERSION,
                                                                                    'default',
                                                                                    CRD_PLURAL)
        assert response_code == 200
        self.assertDictEqual(response_body, {
            'status': 'success',
            'data': {
                "message": "Found 2 spark jobs",
                "spark_jobs": {"job1": "RUNNING", "job2": "COMPLETED"}
            }
        })
