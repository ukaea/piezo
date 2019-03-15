from unittest.mock import patch

import json
from kubernetes.client.rest import ApiException
import pytest
from tornado.httpclient import HTTPClientError
from tornado.testing import gen_test

from PiezoWebApp.src.handlers.submit_job import SubmitJobHandler
from PiezoWebApp.tests.integration_tests.base_integration_test import BaseIntegrationTest


# str | The custom resource's group name
CRD_GROUP = 'sparkoperator.k8s.io'

# str | The custom resource's plural name. For TPRs this would be lowercase plural kind.
CRD_PLURAL = 'sparkapplications'

# str | The custom resource's version
CRD_VERSION = 'v1beta1'


class TestSubmitJobIntegration(BaseIntegrationTest):
    @property
    def handler(self):
        return SubmitJobHandler

    @property
    def standard_request_method(self):
        return 'POST'

    @gen_test
    def test_correct_python_job_is_submitted_correctly(self):
        # Arrange
        body = {
            'name': 'test_python_job',
            'language': 'Python',
            'path_to_main_app_file': '/path_to/file',
            'python_version': '2',
            'arguments': ["1000"]
        }
        self.mock_k8s_adapter.get_namespaced_custom_object.side_effect = ApiException(status=999)
        kubernetes_response = {'metadata': {'name': 'test_python_job'}}
        self.mock_k8s_adapter.create_namespaced_custom_object.return_value = kubernetes_response
        # Act
        with patch('uuid.uuid4', return_value='abcd1234-ef56-gh78-ij90'):
            response_body, response_code = yield self.send_request(body)
        # Assert
        self.mock_k8s_adapter.get_namespaced_custom_object.assert_called_once_with(
            CRD_GROUP,
            CRD_VERSION,
            'default',
            CRD_PLURAL,
            'test_python_job-abcd1'
        )
        expected_body = {
            'apiVersion': 'sparkoperator.k8s.io/v1beta1',
            'kind': 'SparkApplication',
            'metadata': {
                'name': 'test_python_job-abcd1',
                'namespace': 'default'
            },
            'spec': {
                'type': 'Python',
                'pythonVersion': '2',
                'mode': 'cluster',
                'image': 'gcr.io/spark-operator/spark:v2.4.0',
                'imagePullPolicy': 'Always',
                'mainApplicationFile': '/path_to/file',
                'sparkVersion': '2.4.0',
                'restartPolicy': {'type': 'Never'},
                'hadoopConf': {
                    'fs.s3a.endpoint': '0.0.0.0'},
                'arguments': ['1000'],
                'volumes': [
                    {
                        'name': 'secret',
                        'secret': {
                            'secretName': 'secret'}
                    }
                ],
                'driver': {
                    'cores': 0.1,
                    'memory': '512m',
                    'labels': {'version': '2.4.0'},
                    'serviceAccount': 'spark',
                    'envSecretKeyRefs': {
                        'AWS_ACCESS_KEY_ID': {
                            'name': 'secret',
                            'key': 'accessKey'},
                        'AWS_SECRET_ACCESS_KEY': {
                            'name': 'secret',
                            'key': 'secretKey'}}
                },
                'executor': {
                    'cores': 1,
                    'instances': 1,
                    'memory': '512m',
                    'labels': {'version': '2.4.0'},
                    'envSecretKeyRefs': {
                        'AWS_ACCESS_KEY_ID': {
                            'name': 'secret',
                            'key': 'accessKey'},
                        'AWS_SECRET_ACCESS_KEY': {
                            'name': 'secret',
                            'key': 'secretKey'}}
                },
                "monitoring": {
                    "exposeDriverMetrics": "true",
                    "exposeExecutorMetrics": "true",
                    "prometheus": {
                        "jmxExporterJar": "/prometheus/jmx_prometheus_javaagent-0.3.1.jar",
                        "port": 8090}
                }
            }
        }
        assert self.mock_k8s_adapter.create_namespaced_custom_object.call_count == 1
        call_args = self.mock_k8s_adapter.create_namespaced_custom_object.call_args[0]
        assert call_args[0] == CRD_GROUP
        assert call_args[1] == CRD_VERSION
        assert call_args[2] == 'default'
        assert call_args[3] == CRD_PLURAL
        self.assertDictEqual(call_args[4], expected_body)
        assert response_code == 200
        self.assertDictEqual(response_body, {
            'status': 'success',
            'data': {
                'message': 'Job driver created successfully',
                'job_name': 'test_python_job-abcd1'
            }
        })

    @gen_test
    def test_correct_scala_job_is_submitted_correctly(self):
        # Arrange
        body = {
            'name': 'test_scala_job',
            'language': 'Scala',
            'path_to_main_app_file': '/path_to/file',
            'main_class': 'main.class',
            'arguments': ["1000"]
        }
        self.mock_k8s_adapter.get_namespaced_custom_object.side_effect = ApiException(status=999)
        kubernetes_response = {'metadata': {'name': 'test_scala_job'}}
        self.mock_k8s_adapter.create_namespaced_custom_object.return_value = kubernetes_response
        # Act
        with patch('uuid.uuid4', return_value='abcd1234-ef56-gh78-ij90'):
            response_body, response_code = yield self.send_request(body)
        # Assert
        self.mock_k8s_adapter.get_namespaced_custom_object.assert_called_once_with(
            CRD_GROUP,
            CRD_VERSION,
            'default',
            CRD_PLURAL,
            'test_scala_job-abcd1'
        )
        expected_body = {
            'apiVersion': 'sparkoperator.k8s.io/v1beta1',
            'kind': 'SparkApplication',
            'metadata': {
                'name': 'test_scala_job-abcd1',
                'namespace': 'default'
            },
            'spec': {
                'type': 'Scala',
                'mainClass': 'main.class',
                'mode': 'cluster',
                'image': 'gcr.io/spark-operator/spark:v2.4.0',
                'imagePullPolicy': 'Always',
                'mainApplicationFile': '/path_to/file',
                'sparkVersion': '2.4.0',
                'restartPolicy': {'type': 'Never'},
                'hadoopConf': {
                    'fs.s3a.endpoint': '0.0.0.0'},
                'arguments': ['1000'],
                'volumes': [
                    {
                        'name': 'secret',
                        'secret': {
                            'secretName': 'secret'}
                    }
                ],
                'driver': {
                    'cores': 0.1,
                    'memory': '512m',
                    'labels': {'version': '2.4.0'},
                    'serviceAccount': 'spark',
                    'envSecretKeyRefs': {
                        'AWS_ACCESS_KEY_ID': {
                            'name': 'secret',
                            'key': 'accessKey'},
                        'AWS_SECRET_ACCESS_KEY': {
                            'name': 'secret',
                            'key': 'secretKey'}}
                },
                'executor': {
                    'cores': 1,
                    'instances': 1,
                    'memory': '512m',
                    'labels': {'version': '2.4.0'},
                    'envSecretKeyRefs': {
                        'AWS_ACCESS_KEY_ID': {
                            'name': 'secret',
                            'key': 'accessKey'},
                        'AWS_SECRET_ACCESS_KEY': {
                            'name': 'secret',
                            'key': 'secretKey'}}
                },
                "monitoring": {
                    "exposeDriverMetrics": "true",
                    "exposeExecutorMetrics": "true",
                    "prometheus": {
                        "jmxExporterJar": "/prometheus/jmx_prometheus_javaagent-0.3.1.jar",
                        "port": 8090}
                }
            }
        }
        assert self.mock_k8s_adapter.create_namespaced_custom_object.call_count == 1
        call_args = self.mock_k8s_adapter.create_namespaced_custom_object.call_args[0]
        assert call_args[0] == CRD_GROUP
        assert call_args[1] == CRD_VERSION
        assert call_args[2] == 'default'
        assert call_args[3] == CRD_PLURAL
        self.assertDictEqual(call_args[4], expected_body)
        assert response_code == 200
        self.assertDictEqual(response_body, {
            'status': 'success',
            'data': {
                'message': 'Job driver created successfully',
                'job_name': 'test_scala_job-abcd1'
            }
        })

    @gen_test
    def test_all_optional_inputs_defined_to_maximum_succeeds(self):
        # Arrange
        body = {
            'name': 'test_python_job',
            'language': 'Python',
            'path_to_main_app_file': '/path_to/file',
            'python_version': '2',
            'driver_cores': '1',
            'driver_memory': '2048m',
            'executors': '10',
            'executor_cores': '4',
            'executor_memory': '4096m',
            'label': 'my_label'
        }
        self.mock_k8s_adapter.get_namespaced_custom_object.side_effect = ApiException(status=999)
        kubernetes_response = {'metadata': {'name': 'test_python_job'}}
        self.mock_k8s_adapter.create_namespaced_custom_object.return_value = kubernetes_response
        # Act
        with patch('uuid.uuid4', return_value='abcd1234-ef56-gh78-ij90'):
            response_body, response_code = yield self.send_request(body)
        # Assert
        self.mock_k8s_adapter.get_namespaced_custom_object.assert_called_once_with(
            CRD_GROUP,
            CRD_VERSION,
            'default',
            CRD_PLURAL,
            'test_python_job-abcd1'
        )
        expected_body = {
            'apiVersion': 'sparkoperator.k8s.io/v1beta1',
            'kind': 'SparkApplication',
            'metadata': {
                'name': 'test_python_job-abcd1',
                'namespace': 'default',
                'labels': {
                    'userLabel': 'my_label'
                }
            },
            'spec': {
                'type': 'Python',
                'pythonVersion': '2',
                'mode': 'cluster',
                'image': 'gcr.io/spark-operator/spark:v2.4.0',
                'imagePullPolicy': 'Always',
                'mainApplicationFile': '/path_to/file',
                'sparkVersion': '2.4.0',
                'restartPolicy': {'type': 'Never'},
                "hadoopConf": {
                    "fs.s3a.endpoint": "0.0.0.0"},
                'volumes': [
                    {
                        'name': 'secret',
                        'secret': {
                            'secretName': 'secret'}
                    }
                ],
                'driver': {
                    'cores': 1.0,
                    'memory': '2048m',
                    'labels': {'version': '2.4.0'},
                    'serviceAccount': 'spark',
                    'envSecretKeyRefs': {
                        'AWS_ACCESS_KEY_ID': {
                            'name': 'secret',
                            'key': 'accessKey'},
                        'AWS_SECRET_ACCESS_KEY': {
                            'name': 'secret',
                            'key': 'secretKey'}}
                },
                'executor': {
                    'cores': 4,
                    'instances': 10,
                    'memory': '4096m',
                    'labels': {'version': '2.4.0'},
                    'envSecretKeyRefs': {
                        'AWS_ACCESS_KEY_ID': {
                            'name': 'secret',
                            'key': 'accessKey'},
                        'AWS_SECRET_ACCESS_KEY': {
                            'name': 'secret',
                            'key': 'secretKey'}}
                },
                "monitoring": {
                    "exposeDriverMetrics": "true",
                    "exposeExecutorMetrics": "true",
                    "prometheus": {
                        "jmxExporterJar": "/prometheus/jmx_prometheus_javaagent-0.3.1.jar",
                        "port": 8090}
                }
            }
        }
        assert self.mock_k8s_adapter.create_namespaced_custom_object.call_count == 1
        call_args = self.mock_k8s_adapter.create_namespaced_custom_object.call_args[0]
        assert call_args[0] == CRD_GROUP
        assert call_args[1] == CRD_VERSION
        assert call_args[2] == 'default'
        assert call_args[3] == CRD_PLURAL
        self.assertDictEqual(call_args[4], expected_body)
        assert response_code == 200
        self.assertDictEqual(response_body, {
            'status': 'success',
            'data': {
                'message': 'Job driver created successfully',
                'job_name': 'test_python_job-abcd1'
            }
        })

    @gen_test
    def test_all_optional_inputs_defined_to_above_maximum_returns_400_with_explanation(self):
        # Arrange
        body = {
            'name': 'test_python_job',
            'language': 'Python',
            'path_to_main_app_file': '/path_to/file',
            'python_version': '2',
            'driver_cores': '1.1',
            'driver_memory': '2049m',
            'executors': '11',
            'executor_cores': '5',
            'executor_memory': '4097m'
        }
        # Act
        with pytest.raises(HTTPClientError) as error:
            yield self.send_request(body)
        # Assert
        self.mock_k8s_adapter.get_namespaced_custom_object.assert_not_called()
        self.mock_k8s_adapter.create_namespaced_custom_object.assert_not_called()
        assert error.value.response.code == 400
        msg = json.loads(error.value.response.body, encoding='utf-8')['data']
        assert msg == "The following errors were found:\n" \
                      '"driver_cores" input must be in range [0.1, 1]\n' \
                      '"driver_memory" input must be in range [512m, 2048m]\n' \
                      '"executors" input must be in range [1, 10]\n' \
                      '"executor_cores" input must be in range [1, 4]\n' \
                      '"executor_memory" input must be in range [512m, 4096m]\n'

    @gen_test
    def test_unrecognised_input_returns_400_with_explanation(self):
        # Arrange
        body = {
            # Expected inputs
            'name': 'test_python_job',
            'language': 'Python',
            'path_to_main_app_file': '/path_to/file',
            'python_version': '2',
            # Unrecognised input
            'dummy-key': 'dummy-value'
        }
        # Act
        with pytest.raises(HTTPClientError) as error:
            yield self.send_request(body)
        # Assert
        self.mock_k8s_adapter.get_namespaced_custom_object.assert_not_called()
        self.mock_k8s_adapter.create_namespaced_custom_object.assert_not_called()
        msg = json.loads(error.value.response.body, encoding='utf-8')['data']
        assert error.value.response.code == 400
        assert msg == "The following errors were found:\n" \
                      'Unsupported input "dummy-key" provided\n'

    @gen_test
    def test_optional_inputs_in_wrong_format_returns_400_with_explanation(self):
        # Arrange
        body = {
            'name': 'test_python_job',
            'language': 'Python',
            'path_to_main_app_file': '/path_to/file',
            'python_version': '2.3',
            'driver_cores': '500m',
            'driver_memory': '1024',
            'executors': 'Maximum',
            'executor_cores': '3.5',
            'executor_memory': '2048'
        }
        # Act
        with pytest.raises(HTTPClientError) as error:
            yield self.send_request(body)
        # Assert
        self.mock_k8s_adapter.get_namespaced_custom_object.assert_not_called()
        self.mock_k8s_adapter.create_namespaced_custom_object.assert_not_called()
        assert error.value.response.code == 400
        msg = json.loads(error.value.response.body, encoding='utf-8')['data']
        assert msg == "The following errors were found:\n" \
                      '"python_version" input must be one of: "2", "3"\n' \
                      '"driver_cores" input must be a multiple of 0.1\n' \
                      '"driver_memory" input must be a string integer value ending in "m" ' \
                      '(e.g. "512m" for 512 megabytes)\n' \
                      '"executors" input must be an integer\n' \
                      '"executor_cores" input must be an integer\n' \
                      '"executor_memory" input must be a string integer value ending in "m" ' \
                      '(e.g. "512m" for 512 megabytes)\n'
