from logging import Logger
from kubernetes.client.rest import ApiException
import mock
import pytest
from types import SimpleNamespace
from unittest import TestCase

from PiezoWebApp.src.services.kubernetes.i_kubernetes_adapter import IKubernetesAdapter
from PiezoWebApp.src.services.kubernetes.kubernetes_service import KubernetesService

# str | The custom resource's group name
CRD_GROUP = 'sparkoperator.k8s.io'

# str | The custom resource's plural name. For TPRs this would be lowercase plural kind.
CRD_PLURAL = 'sparkapplications'

# str | The custom resource's version
CRD_VERSION = 'v1beta1'


class KubernetesServiceTest(TestCase):
    # pylint: disable=attribute-defined-outside-init
    @pytest.fixture(autouse=True)
    def setup(self):
        self.mock_kubernetes_adapter = mock.create_autospec(IKubernetesAdapter)
        self.mock_logger = mock.create_autospec(Logger)
        self.test_service = KubernetesService(self.mock_kubernetes_adapter, self.mock_logger)

    def test_delete_job_sends_expected_arguments(self):
        # Arrange
        k8s_response = SimpleNamespace()
        k8s_response.content = "Response"
        self.mock_kubernetes_adapter.delete_options.return_value = {'test-option': None}
        self.mock_kubernetes_adapter.delete_namespaced_custom_object.return_value = k8s_response
        # Act
        result = self.test_service.delete_job('test-spark-job', 'test-namespace')
        # Assert
        assert result == "Response"
        self.mock_kubernetes_adapter.delete_namespaced_custom_object.assert_called_once_with(
            CRD_GROUP,
            CRD_VERSION,
            'test-namespace',
            CRD_PLURAL,
            'test-spark-job',
            {'test-option': None}
        )

    def test_delete_job_logs_and_returns_api_exception_reason(self):
        # Arrange
        self.mock_kubernetes_adapter.delete_namespaced_custom_object.side_effect = ApiException(reason="Reason")
        # Act
        result = self.test_service.delete_job('test-spark-job', 'test-namespace')
        # Assert
        expected_message = \
            'Kubernetes error when trying to delete job "test-spark-job" in namespace "test-namespace": Reason'
        self.mock_logger.error.assert_called_once_with(expected_message)
        assert result == expected_message

    def test_get_logs_sends_expected_arguments(self):
        # Arrange
        self.mock_kubernetes_adapter.read_namespaced_pod_log.return_value = "Response"
        # Act
        result = self.test_service.get_logs('test-driver', 'test-namespace')
        # Assert
        assert result == "Response"
        self.mock_kubernetes_adapter.read_namespaced_pod_log.assert_called_once_with('test-driver', 'test-namespace')

    def test_get_logs_logs_and_returns_api_exception_reason(self):
        # Arrange
        self.mock_kubernetes_adapter.read_namespaced_pod_log.side_effect = ApiException(reason="Reason")
        # Act
        result = self.test_service.get_logs('test-driver', 'test-namespace')
        # Assert
        expected_message = \
            'Kubernetes error when trying to get logs for driver "test-driver" in namespace "test-namespace": Reason'
        self.mock_logger.error.assert_called_once_with(expected_message)
        assert result == expected_message

    def test_submit_job_sends_expected_arguments(self):
        # Arrange
        self.mock_kubernetes_adapter.read_namespaced_pod_log.return_value = "Response"
        # Act
        result = self.test_service.get_logs('test-driver', 'test-namespace')
        # Assert
        assert result == "Response"
        self.mock_kubernetes_adapter.read_namespaced_pod_log.assert_called_once_with('test-driver', 'test-namespace')

    def test_get_logs_logs_and_returns_missing_namespace(self):
        # Arrange
        self.mock_kubernetes_adapter.create_namespaced_custom_object.side_effect = ApiException(reason="Reason")
        body = {
            'metadata': {
                'name': 'test-spark-job'
            }
        }
        # Act
        result = self.test_service.submit_job(body)
        # Assert
        expected_message = 'Job submitted without namespace in metadata'
        self.mock_logger.warning.assert_called_once_with(expected_message)
        assert result == expected_message

    def test_get_logs_logs_and_returns_api_exception_reason(self):
        # Arrange
        self.mock_kubernetes_adapter.create_namespaced_custom_object.side_effect = ApiException(reason="Reason")
        body = {
            'metadata': {
                'namespace': 'test-namespace',
                'name': 'test-spark-job'
            }
        }
        # Act
        result = self.test_service.submit_job(body)
        # Assert
        expected_message = 'Kubernetes error when trying to submit job in namespace "test-namespace": Reason'
        self.mock_logger.error.assert_called_once_with(expected_message)
        assert result == expected_message
