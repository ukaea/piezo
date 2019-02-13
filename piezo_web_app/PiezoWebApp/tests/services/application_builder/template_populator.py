import pytest
from PiezoWebApp.src.services.application_builder.template_populator import TemplatePopulator


class TestTemplatePopulator:
    # pylint: disable=attribute-defined-outside-init
    @pytest.fixture(autouse=True)
    def setup(self):
        self.test_populator = TemplatePopulator()
        self.arguments = {"name": "test",
                          "path_to_main_application_file": "/path/to/file",
                          "driver_cores": 0.1,
                          "driver_core_limit": "200m",
                          "driver_memory": "512m",
                          "executor_cores": 1,
                          "executors": 1,
                          "executor_memory": "512m"}

    def test_build_template_builds_python_job_manifest_for_python_applications(self):
        # Arrange
        self.arguments["language"] = "Python"
        self.arguments["pythonVersion"] = "2"
        # Act
        manifest = self.test_populator.build_template(self.arguments)
        # Assert
        assert manifest == {"apiVersion": "sparkoperator.k8s.io/v1beta1",
                            "kind": "SparkApplication",
                            "metadata":
                                {"name": "test",
                                 "namespace": "default"},
                            "spec": {
                                "type": "Python",
                                "pythonVersion": "2",
                                "mode": "cluster",
                                "image": "gcr.io/spark-operator/spark:v2.4.0",
                                "imagePullPolicy": "Always",
                                "mainApplicationFile": "/path/to/file",
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


    def test_build_template_builds_scala_job_manifest_for_scala_applications(self):
        # Arrange
        self.arguments["language"] = "Scala"
        self.arguments["main_class"] = "testClass"
        # Act
        manifest = self.test_populator.build_template(self.arguments)
        # Assert
        assert manifest == {"apiVersion": "sparkoperator.k8s.io/v1beta1",
                            "kind": "SparkApplication",
                            "metadata":
                                {"name": "test",
                                 "namespace": "default"},
                            "spec": {
                                "type": "Scala",
                                "mode": "cluster",
                                "image": "gcr.io/spark-operator/spark:v2.4.0",
                                "imagePullPolicy": "Always",
                                "mainApplicationFile": "/path/to/file",
                                "mainClass": "testClass",
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
