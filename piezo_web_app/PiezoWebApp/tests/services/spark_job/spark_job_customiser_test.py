from unittest import TestCase

from kubernetes.client.rest import ApiException
import mock
import pytest

from PiezoWebApp.src.services.kubernetes.i_kubernetes_adapter import IKubernetesAdapter
from PiezoWebApp.src.services.spark_job.spark_job_customiser import SparkJobCustomiser


class TestSparkJobCustomiser(TestCase):
    # pylint: disable=attribute-defined-outside-init
    @pytest.fixture(autouse=True)
    def setup(self):
        self.mock_kubernetes_adapter = mock.create_autospec(IKubernetesAdapter)
        self.test_customiser = SparkJobCustomiser(self.mock_kubernetes_adapter)

    def test_rename_job_tags_names_with_uuid(self):
        # Arrange
        self.mock_kubernetes_adapter.get_namespaced_custom_object.side_effect = ApiException(status=999)
        base_name = 'test-job'
        # Act
        job_name = self.test_customiser.rename_job(base_name)
        # Assert
        self.mock_kubernetes_adapter.get_namespaced_custom_object.assert_called_once()
        regex = '^' + base_name + '-[0-9a-f]{5}$'
        self.assertRegex(job_name, regex)

    def test_rename_job_handles_one_coincidental_match(self):
        # Arrange
        self.mock_kubernetes_adapter.get_namespaced_custom_object.side_effect = [
            {'status': 'RUNNING'},
            ApiException(status=999)
        ]
        base_name = 'test-job'
        # Act
        job_name = self.test_customiser.rename_job(base_name)
        # Assert
        calls = self.mock_kubernetes_adapter.method_calls
        assert len(calls) == 2
        assert calls[0][0] == 'get_namespaced_custom_object'
        assert calls[1][0] == 'get_namespaced_custom_object'
        regex = '^' + base_name + '-[0-9a-f]{5}$'
        self.assertRegex(job_name, regex)

    def test_rename_job_raises_if_always_matching(self):
        # Arrange
        self.mock_kubernetes_adapter.get_namespaced_custom_object.return_value = {'status': 'RUNNING'}
        base_name = 'test-job'
        # Act
        with self.assertRaises(RuntimeError, msg='10 attempts to find a unique job name all failed'):
            self.test_customiser.rename_job(base_name)
        # Assert
        assert len(self.mock_kubernetes_adapter.method_calls) == 10
