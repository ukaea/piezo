from tornado.testing import gen_test

from PiezoWebApp.src.handlers.tidy_jobs import TidyJobsHandler
from PiezoWebApp.tests.integration_tests.base_integration_test import BaseIntegrationTest


# str | The custom resource's group name
CRD_GROUP = 'sparkoperator.k8s.io'

# str | The custom resource's plural name. For TPRs this would be lowercase plural kind.
CRD_PLURAL = 'sparkapplications'

# str | The custom resource's version
CRD_VERSION = 'v1beta1'

NAMESPACE = 'default'


class TestTidyJobsIntegration(BaseIntegrationTest):
    @property
    def handler(self):
        return TidyJobsHandler

    @property
    def standard_request_method(self):
        return 'POST'

    @gen_test
    def test_post_successfully_writes_logs_and_deletes_completed_and_failed_jobs(self):
        # Arrange
        kubernetes_list_jobs_response = {
            "items": [
                {
                    "metadata":
                        {
                            "name": "job1",
                            "labels": {
                                "version": "2.4.0"
                            }
                        },
                    "status":
                        {
                            "applicationState":
                                {
                                    "state": "RUNNING"
                                }
                        }
                },
                {
                    "metadata":
                        {
                            "name": "job2",
                            "labels": {
                                "userLabel": "test-label",
                                "version": "2.4.0"
                            }
                        },
                    "status":
                        {
                            "applicationState":
                                {
                                    "state": "COMPLETED"
                                }
                        }
                },
                {
                    "metadata":
                        {
                            "name": "job3",
                            "labels": {
                                "userLabel": "test-label",
                                "version": "2.4.0"
                            }
                        },
                    "status":
                        {
                            "applicationState":
                                {
                                    "state": "FAILED"
                                }
                        }
                }
            ]
        }
        self.mock_k8s_adapter.list_namespaced_custom_object.return_value = kubernetes_list_jobs_response
        self.mock_k8s_adapter.delete_options.return_value = {"api_version": "version", "other_values": "values"}
        self.mock_k8s_adapter.delete_namespaced_custom_object.return_value = {'status': 200}
        # Act
        response_body, response_code = yield self.send_request_without_body()
        # Assert
        self.mock_k8s_adapter.read_namespaced_pod_log.assert_any_call('job2-driver', 'default')
        self.mock_k8s_adapter.read_namespaced_pod_log.assert_any_call('job3-driver', 'default')
        assert self.mock_k8s_adapter.read_namespaced_pod_log.call_count == 2
        self.mock_k8s_adapter.delete_namespaced_custom_object.assert_any_call(CRD_GROUP,
                                                                              CRD_VERSION,
                                                                              NAMESPACE,
                                                                              CRD_PLURAL,
                                                                              'job2',
                                                                              {
                                                                                "api_version": "version",
                                                                                "other_values": "values"
                                                                              })
        self.mock_k8s_adapter.delete_namespaced_custom_object.assert_any_call(CRD_GROUP,
                                                                              CRD_VERSION,
                                                                              NAMESPACE,
                                                                              CRD_PLURAL,
                                                                              'job3',
                                                                              {
                                                                                "api_version": "version",
                                                                                "other_values": "values"
                                                                              })
        assert self.mock_k8s_adapter.delete_namespaced_custom_object.call_count == 2
        assert response_code == 200
        self.mock_logger.debug.assert_any_call('Not processing job "job1", current status is "RUNNING"')
        self.mock_logger.debug.assert_any_call('Logs written to "outputs/job2/log.txt" in bucket "kubernetes"')
        self.mock_logger.debug.assert_any_call('Trying to delete job "job2" resulted in status: 200')
        self.mock_logger.debug.assert_any_call('Logs written to "outputs/job3/log.txt" in bucket "kubernetes"')
        self.mock_logger.debug.assert_any_call('Trying to delete job "job3" resulted in status: 200')
        self.assertDictEqual(response_body, {
            'status': 'success',
            'data': {
                'message': '3 Spark jobs found',
                'jobs_tidied': {'job2': 'COMPLETED', 'job3': 'FAILED'},
                'jobs_skipped': {'job1': 'RUNNING'},
                'jobs_failed_to_process': {}}})
