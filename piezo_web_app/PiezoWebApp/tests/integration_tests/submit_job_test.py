from PiezoWebApp.src.handlers.submit_job import SubmitJobHandler
from PiezoWebApp.tests.integration_tests.base_integration_test import *
from tornado.testing import gen_test
from types import SimpleNamespace

class TestSubmitJobIntegration(BaseIntegrationTest):
    @property
    def handler(self):
        return SubmitJobHandler

    @property
    def standard_request_method(self):
        return "POST"

    @gen_test
    def test_correct_python_job_is_submitted_correctly(self):
        # Arrange
        body = {"name": "test_python_job", "language": "Python", "path_to_main_app_file": "/path_to/file", "python_version": "2"}
        kubernetes_response = SimpleNamespace()
        kubernetes_response.content = "Application submitted successfully"
        self.mock_k8s_adapter.create_namespaced_custom_object.return_value = kubernetes_response
        # Act
        response_body, response_code = yield self.send_request(body)
        # Assert
        expected_body = {"apiVersion": "sparkoperator.k8s.io/v1beta1",
                         "kind": "SparkApplication",
                         "metadata":
                             {"name": "test_python_job",
                              "namespace": "default"},
                         "spec": {
                             "type": "Python",
                             "pythonVersion": "2",
                             "mode": "cluster",
                             "image": "gcr.io/spark-operator/spark:v2.4.0",
                             "imagePullPolicy": "Always",
                             "mainApplicationFile": "/path_to/file",
                             "sparkVersion": "2.4.0",
                             "restartPolicy": {
                                 "type": "Never"},
                             "driver": {
                                 "cores": 0.1,
                                 "coreLimit": "200m",
                                 "memory": "512m",
                                 "labels": {
                                     "version": "2.4.0"},
                                 "serviceAccount": "spark"},
                             "executor": {
                                 "cores": 1,
                                 "instances": 1,
                                 "memory": "512m",
                                 "labels": {
                                     "version": "2.4.0"}}}}
        assert self.mock_k8s_adapter.create_namespaced_custom_object.called_with(
            CRD_GROUP, CRD_VERSION, "default", CRD_PLURAL, expected_body)

