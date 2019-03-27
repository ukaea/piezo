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
                }
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
