import unittest
import pytest
import mock

from PiezoWebApp.src.services.spark_job.validation.validation_ruleset import ValidationRuleset
from PiezoWebApp.src.services.spark_job.validation.manifest_populator import ManifestPopulator
from PiezoWebApp.src.utils.configurations import Configuration


class TestTemplatePopulator(unittest.TestCase):
    # pylint: disable=attribute-defined-outside-init
    @pytest.fixture(autouse=True)
    def setup(self):
        mock_configuration = mock.create_autospec(Configuration)
        mock_configuration.s3_endpoint = "0.0.0.0"
        mock_configuration.s3_secrets_name = "secret"
        mock_validation_ruleset = mock.create_autospec(ValidationRuleset)
        mock_validation_ruleset.get_default_value_for_key.side_effect = \
            lambda input_name: {
                'apiVersion': "sparkoperator.k8s.io/v1beta1",
                'java_agent': '/prometheus/jmx_prometheus_javaagent-0.3.1.jar',
                'kind': 'SparkApplication',
                'namespace': 'default',
                'mode': 'cluster',
                'image': 'gcr.io/spark-operator/spark:v2.4.0',
                'image_pull_policy': 'Always',
                'spark_version': '2.4.0',
                'restart_policy': 'onFailure',
                'on_failure_retries': 3,
                'on_failure_retry_interval': 10,
                'on_submission_failure_retries': 5,
                'on_submission_failure_retry_interval': 20,
                'service_account': 'spark',
                'name': None,
                'path_to_main_app_file': None,
                'language': None,
                'python_version': None,
                'main_class': None,
                'arguments': None,
                'driver_cores': 0.1,
                'driver_memory': "512m",
                'executors': 1,
                'executor_cores': 1,
                'executor_memory': "512m",
                'executor_toleration_key': 'piezoRestriction',
                'executor_toleration_operation': 'Equal',
                'executor_toleration_value': 'executors',
                'executor_toleration_effect': 'NoSchedule',
                'label': None
            }[input_name]
        self.test_populator = ManifestPopulator(mock_configuration, mock_validation_ruleset)
        self.arguments = {"name": "test",
                          "path_to_main_app_file": "/path/to/file",
                          "driver_cores": "0.1",
                          "driver_memory": "512m",
                          "executor_cores": "1",
                          "executors": "1",
                          "executor_memory": "512m",
                          "arguments": ["1000", "100"],
                          "label": "myLabel"}

    def test_build_manifest_builds_python_job_manifest_for_python_applications(self):
        # Arrange
        self.arguments["language"] = "Python"
        self.arguments["python_version"] = "2"
        # Act
        manifest = self.test_populator.build_manifest(self.arguments)
        # Assert
        self.assertDictEqual(manifest, {
            "apiVersion": "sparkoperator.k8s.io/v1beta1",
            "kind": "SparkApplication",
            "metadata": {
                "name": "test",
                "namespace": "default",
                "labels": {"userLabel": "myLabel"}
            },
            "spec": {
                "type": "Python",
                "pythonVersion": "2",
                "mode": "cluster",
                "image": "gcr.io/spark-operator/spark:v2.4.0",
                "imagePullPolicy": "Always",
                "mainApplicationFile": "/path/to/file",
                "sparkVersion": "2.4.0",
                "restartPolicy": {
                    "type": "onFailure",
                    'onFailureRetries': 3,
                    "onFailureRetryInterval": 10,
                    "onSubmissionFailureRetries": 5,
                    "onSubmissionFailureRetryInterval": 20
                },
                "hadoopConf": {"fs.s3a.endpoint": "0.0.0.0"},
                "arguments": ["1000", "100"],
                "volumes": [
                    {
                        "name": "secret",
                        "secret": {"secretName": "secret"}
                    }
                ],
                "driver": {
                    "cores": "0.1",
                    "memory": "512m",
                    "labels": {"version": "2.4.0"},
                    "serviceAccount": "spark",
                    "envSecretKeyRefs": {
                        "AWS_ACCESS_KEY_ID": {
                            "name": "secret",
                            "key": "accessKey"
                        },
                        "AWS_SECRET_ACCESS_KEY": {
                            "name": "secret",
                            "key": "secretKey"
                        }
                    }
                },
                "executor": {
                    "cores": "1",
                    "instances": "1",
                    "memory": "512m",
                    "labels": {"version": "2.4.0"},
                    'tolerations': {
                        'key': 'piezoRestriction',
                        'operator': 'Equal',
                        'value': 'executors',
                        'effect': 'NoSchedule'
                    },
                    "envSecretKeyRefs": {
                        "AWS_ACCESS_KEY_ID": {
                            "name": "secret",
                            "key": "accessKey"
                        },
                        "AWS_SECRET_ACCESS_KEY": {
                            "name": "secret",
                            "key": "secretKey"
                        }
                    }
                },
                "monitoring": {
                    "exposeDriverMetrics": True,
                    "exposeExecutorMetrics": True,
                    "prometheus": {
                        "jmxExporterJar": "/prometheus/jmx_prometheus_javaagent-0.3.1.jar",
                        "port": 8090
                    }
                }
            }
        })

    def test_build_manifest_builds_scala_job_manifest_for_scala_applications(self):
        # Arrange
        self.arguments["language"] = "Scala"
        self.arguments["main_class"] = "testClass"
        # Act
        manifest = self.test_populator.build_manifest(self.arguments)
        # Assert
        self.assertDictEqual(manifest, {
            "apiVersion": "sparkoperator.k8s.io/v1beta1",
            "kind": "SparkApplication",
            "metadata": {
                "name": "test",
                "namespace": "default",
                "labels": {"userLabel": "myLabel"}
            },
            "spec": {
                "type": "Scala",
                "mode": "cluster",
                "image": "gcr.io/spark-operator/spark:v2.4.0",
                "imagePullPolicy": "Always",
                "mainApplicationFile": "/path/to/file",
                "mainClass": "testClass",
                "sparkVersion": "2.4.0",
                "restartPolicy": {
                    "type": "onFailure",
                    'onFailureRetries': 3,
                    "onFailureRetryInterval": 10,
                    "onSubmissionFailureRetries": 5,
                    "onSubmissionFailureRetryInterval": 20
                },
                "hadoopConf": {"fs.s3a.endpoint": "0.0.0.0"},
                "arguments": ["1000", "100"],
                "volumes": [
                    {
                        "name": "secret",
                        "secret": {"secretName": "secret"}
                    }
                ],
                "driver": {
                    "cores": "0.1",
                    "memory": "512m",
                    "labels": {"version": "2.4.0"},
                    "serviceAccount": "spark",
                    "envSecretKeyRefs": {
                        "AWS_ACCESS_KEY_ID": {
                            "name": "secret",
                            "key": "accessKey"
                        },
                        "AWS_SECRET_ACCESS_KEY": {
                            "name": "secret",
                            "key": "secretKey"
                        }
                    }
                },
                "executor": {
                    "cores": "1",
                    "instances": "1",
                    "memory": "512m",
                    "labels": {"version": "2.4.0"},
                    'tolerations': {
                        'key': 'piezoRestriction',
                        'operator': 'Equal',
                        'value': 'executors',
                        'effect': 'NoSchedule'
                    },
                    "envSecretKeyRefs": {
                        "AWS_ACCESS_KEY_ID": {
                            "name": "secret",
                            "key": "accessKey"
                        },
                        "AWS_SECRET_ACCESS_KEY": {
                            "name": "secret",
                            "key": "secretKey"
                        }
                    }
                },
                "monitoring": {
                    "exposeDriverMetrics": True,
                    "exposeExecutorMetrics": True,
                    "prometheus": {
                        "jmxExporterJar": "/prometheus/jmx_prometheus_javaagent-0.3.1.jar",
                        "port": 8090
                    }
                }
            }
        })

    def test_default_manifest_returns_a_filled_in_spark_application_template_with_default_values(self):
        # Arrange
        default_manifest = self.test_populator._default_spark_application_manifest()
        # Assert
        self.assertDictEqual(default_manifest, {
            "apiVersion": "sparkoperator.k8s.io/v1beta1",
            "kind": "SparkApplication",
            "metadata": {
                "name": None,
                "namespace": "default"
            },
            "spec": {
                "mode": "cluster",
                "image": "gcr.io/spark-operator/spark:v2.4.0",
                "imagePullPolicy": "Always",
                "mainApplicationFile": None,
                "sparkVersion": "2.4.0",
                "restartPolicy": {
                    "type": "onFailure",
                    'onFailureRetries': 3,
                    "onFailureRetryInterval": 10,
                    "onSubmissionFailureRetries": 5,
                    "onSubmissionFailureRetryInterval": 20
                },
                "hadoopConf": {"fs.s3a.endpoint": "0.0.0.0"},
                "volumes": [
                    {
                        "name": "secret",
                        "secret": {"secretName": "secret"}
                    }
                ],
                "driver": {
                    "cores": 0.1,
                    "memory": "512m",
                    "labels": {"version": "2.4.0"},
                    "serviceAccount": "spark",
                    "envSecretKeyRefs": {
                        "AWS_ACCESS_KEY_ID": {
                            "name": "secret",
                            "key": "accessKey"
                        },
                        "AWS_SECRET_ACCESS_KEY": {
                            "name": "secret",
                            "key": "secretKey"
                        }
                    }
                },
                "executor": {
                    "cores": 1,
                    "instances": 1,
                    "memory": "512m",
                    "labels": {"version": "2.4.0"},
                    'tolerations': {
                        'key': 'piezoRestriction',
                        'operator': 'Equal',
                        'value': 'executors',
                        'effect': 'NoSchedule'
                    },
                    "envSecretKeyRefs": {
                        "AWS_ACCESS_KEY_ID": {
                            "name": "secret",
                            "key": "accessKey"
                        },
                        "AWS_SECRET_ACCESS_KEY": {
                            "name": "secret",
                            "key": "secretKey"
                        }
                    }
                },
                "monitoring": {
                    "exposeDriverMetrics": True,
                    "exposeExecutorMetrics": True,
                    "prometheus": {
                        "jmxExporterJar": "/prometheus/jmx_prometheus_javaagent-0.3.1.jar",
                        "port": 8090
                    }
                }
            }
        })
