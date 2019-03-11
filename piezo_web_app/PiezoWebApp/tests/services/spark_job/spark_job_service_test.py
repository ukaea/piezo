from logging import Logger
from unittest import TestCase

from kubernetes.client.rest import ApiException
import mock
import pytest

from PiezoWebApp.src.services.kubernetes.i_kubernetes_adapter import IKubernetesAdapter
from PiezoWebApp.src.services.spark_job.i_spark_job_namer import ISparkJobNamer
from PiezoWebApp.src.services.spark_job.spark_job_service import SparkJobService
from PiezoWebApp.src.services.spark_job.validation.i_manifest_populator import IManifestPopulator
from PiezoWebApp.src.services.spark_job.validation.i_validation_service import IValidationService
from PiezoWebApp.src.models.spark_job_validation_result import ValidationResult
from PiezoWebApp.src.models.return_status import StatusCodes

# str | The custom resource's group name
CRD_GROUP = 'sparkoperator.k8s.io'

# str | The custom resource's plural name. For TPRs this would be lowercase plural kind.
CRD_PLURAL = 'sparkapplications'

# str | The custom resource's version
CRD_VERSION = 'v1beta1'


class TestSparkJobService(TestCase):
    # pylint: disable=attribute-defined-outside-init
    @pytest.fixture(autouse=True)
    def setup(self):
        self.mock_kubernetes_adapter = mock.create_autospec(IKubernetesAdapter)
        self.mock_logger = mock.create_autospec(Logger)
        self.mock_manifest_populator = mock.create_autospec(IManifestPopulator)
        self.mock_spark_job_namer = mock.create_autospec(ISparkJobNamer)
        self.mock_validation_service = mock.create_autospec(IValidationService)
        self.test_service = SparkJobService(
            self.mock_kubernetes_adapter,
            self.mock_logger,
            self.mock_manifest_populator,
            self.mock_spark_job_namer,
            self.mock_validation_service
        )

    def test_delete_job_sends_expected_arguments(self):
        # Arrange
        k8s_response = {'status': 'Success'}
        self.mock_kubernetes_adapter.delete_options.return_value = {"api_version": "version", "other_values": "values"}
        self.mock_kubernetes_adapter.delete_namespaced_custom_object.return_value = k8s_response
        # Act
        result = self.test_service.delete_job('test-spark-job', 'test-namespace')
        # Assert
        self.assertDictEqual(result, {'message': 'test-spark-job deleted from namespace test-namespace', 'status': 200})
        self.mock_kubernetes_adapter.delete_namespaced_custom_object.assert_called_once_with(
            CRD_GROUP,
            CRD_VERSION,
            'test-namespace',
            CRD_PLURAL,
            'test-spark-job',
            {"api_version": "version", "other_values": "values"}
        )

    def test_delete_job_logs_and_returns_api_exception_reason(self):
        # Arrange
        self.mock_kubernetes_adapter.delete_namespaced_custom_object.side_effect = ApiException(
            reason="Reason",
            status=999
        )
        # Act
        result = self.test_service.delete_job('test-spark-job', 'test-namespace')
        # Assert
        expected_message = \
            'Kubernetes error when trying to delete job "test-spark-job" in namespace "test-namespace": Reason'
        self.mock_logger.error.assert_called_once_with(expected_message)
        assert result['status'] == 999
        assert result['message'] == expected_message

    def test_get_jobs_sends_expected_arguments(self):
        # Arrange
        self.mock_kubernetes_adapter.list_namespaced_custom_object.return_value = {"items": []}
        # Act
        result = self.test_service.get_jobs()
        # Assert
        self.assertDictEqual(result, {'message': 'Found 0 spark jobs', 'spark_jobs': {}, 'status': 200})
        self.mock_kubernetes_adapter.list_namespaced_custom_object.assert_called_once_with(
            CRD_GROUP, CRD_VERSION, 'default', CRD_PLURAL)

    def test_get_jobs_logs_and_returns_api_exception_reason(self):
        # Arrange
        self.mock_kubernetes_adapter.list_namespaced_custom_object.side_effect = \
            ApiException(reason="Reason", status=999)
        # Act
        result = self.test_service.get_jobs()
        # Assert
        expected_message = \
            'Kubernetes error when trying to get a list of current spark jobs: Reason'
        self.mock_logger.error.assert_called_once_with(expected_message)
        self.assertDictEqual(result, {
            'status': 999,
            'message': 'Kubernetes error when trying to get a list of current spark jobs: Reason'
        })

    def test_get_logs_sends_expected_arguments(self):
        # Arrange
        self.mock_kubernetes_adapter.read_namespaced_pod_log.return_value = "Response"
        # Act
        result = self.test_service.get_logs('test-job', 'test-namespace')
        # Assert
        self.assertDictEqual(result, {'message': 'Response', 'status': 200})
        self.mock_kubernetes_adapter.read_namespaced_pod_log.assert_called_once_with(
            'test-job-driver', 'test-namespace')

    def test_get_logs_logs_and_returns_api_exception_reason(self):
        # Arrange
        self.mock_kubernetes_adapter.read_namespaced_pod_log.side_effect = ApiException(reason="Reason", status=999)
        # Act
        result = self.test_service.get_logs('test-job', 'test-namespace')
        # Assert
        expected_message = \
            'Kubernetes error when trying to get logs for spark job "test-job" in namespace "test-namespace": Reason'
        self.mock_logger.error.assert_called_once_with(expected_message)
        self.assertDictEqual(result, {
            'status': 999,
            'message': 'Kubernetes error when trying to get logs for spark job "test-job" '
                       'in namespace "test-namespace": Reason'
        })

    def test_submit_job_sends_expected_arguments(self):
        # Arrange
        body = {
            'name': 'test-spark-job',
            'language': 'example-language'
        }
        self.mock_validation_service.validate_request_keys.return_value = ValidationResult(True, "", None)
        self.mock_validation_service.validate_request_values.return_value = ValidationResult(True, "", body)
        self.mock_spark_job_namer.rename_job.return_value = 'test-spark-job-abcd1234'
        manifest = {
            'metadata': {
                'namespace': 'example-namespace',
                'name': 'test-spark-job-abcd1234',
                'language': 'example-language'
            }
        }
        self.mock_manifest_populator.build_manifest.return_value = manifest
        self.mock_kubernetes_adapter.create_namespaced_custom_object.return_value = {
            'metadata': {
                'namespace': 'example-namespace',
                'name': 'test-spark-job-abcd1234',
                'language': 'example-language'
            }
        }
        # Act
        result = self.test_service.submit_job(body)
        # Assert
        self.mock_kubernetes_adapter.create_namespaced_custom_object.assert_called_once_with(
            CRD_GROUP,
            CRD_VERSION,
            'example-namespace',
            CRD_PLURAL,
            manifest
        )
        self.assertDictEqual(result, {
            'status': StatusCodes.Okay.value,
            'message': 'Job driver created successfully',
            'job_name': 'test-spark-job-abcd1234'
        })

    def test_submit_job_returns_invalid_body_keys(self):
        # Arrange
        body = {
            'name': 'test-spark-job',
            'language': 'example-language'
        }
        self.mock_validation_service.validate_request_keys.return_value = ValidationResult(False, "Msg", None)
        # Act
        result = self.test_service.submit_job(body)
        # Assert
        self.mock_kubernetes_adapter.create_namespaced_custom_object.assert_not_called()
        self.assertDictEqual(result, {
            'status': StatusCodes.Bad_request.value,
            'message': 'Msg'
        })

    def test_submit_job_returns_invalid_body_values(self):
        # Arrange
        body = {
            'name': 'test-spark-job',
            'language': 'example-language'
        }
        self.mock_validation_service.validate_request_keys.return_value = ValidationResult(True, "", None)
        self.mock_validation_service.validate_request_values.return_value = ValidationResult(False, "Msg", None)
        # Act
        result = self.test_service.submit_job(body)
        # Assert
        self.mock_kubernetes_adapter.create_namespaced_custom_object.assert_not_called()
        self.assertDictEqual(result, {
            'status': StatusCodes.Bad_request.value,
            'message': 'Msg'
        })

    def test_submit_job_logs_and_returns_api_exception_reason(self):
        # Arrange
        body = {
            'name': 'test-spark-job',
            'language': 'example-language'
        }
        self.mock_validation_service.validate_request_keys.return_value = ValidationResult(True, "", None)
        self.mock_validation_service.validate_request_values.return_value = ValidationResult(True, "", body)
        self.mock_spark_job_namer.rename_job.return_value = 'test-spark-job-abcd1234'
        manifest = {
            'metadata': {
                'namespace': 'example-namespace',
                'name': 'test-spark-job-abcd1234',
                'language': 'example-language'
            }
        }
        self.mock_manifest_populator.build_manifest.return_value = manifest
        self.mock_kubernetes_adapter.create_namespaced_custom_object.side_effect = \
            ApiException(reason="Reason", status=999)
        # Act
        result = self.test_service.submit_job(body)
        # Assert
        self.mock_kubernetes_adapter.create_namespaced_custom_object.assert_called_once_with(
            CRD_GROUP,
            CRD_VERSION,
            'example-namespace',
            CRD_PLURAL,
            manifest
        )
        expected_message = 'Kubernetes error when trying to submit job: Reason'
        self.mock_logger.error.assert_has_calls([
            mock.call(expected_message),
            mock.call({
                'metadata': {
                    'namespace': 'example-namespace',
                    'name': 'test-spark-job-abcd1234',
                    'language': 'example-language'
                }
            })
        ])
        self.assertDictEqual(result, {
            'status': 999,
            'message': expected_message
        })

    def test_get_job_status_sends_expected_arguments(self):
        # Arrange
        self.mock_kubernetes_adapter.get_namespaced_custom_object.return_value = {
            'status': {
                'applicationState': {
                    'state': 'Running'}}}
        # Act
        result = self.test_service.get_job_status('test-job', 'test-namespace')
        # Assert
        self.assertDictEqual(result, {'message': 'Running', 'status': 200})
        self.mock_kubernetes_adapter.get_namespaced_custom_object.assert_called_once_with(
            CRD_GROUP,
            CRD_VERSION,
            'test-namespace',
            CRD_PLURAL,
            'test-job'
        )

    def test_get_job_status_logs_and_returns_api_exception_reason(self):
        # Arrange
        self.mock_kubernetes_adapter.get_namespaced_custom_object.side_effect = ApiException(reason="Reason",
                                                                                             status=999)
        # Act
        result = self.test_service.get_job_status('test-job', 'test-namespace')
        # Assert
        expected_message = \
            'Kubernetes error when trying to get status of spark job "test-job" in ' \
            'namespace "test-namespace": Reason'
        self.mock_logger.error.assert_called_once_with(expected_message)
        self.assertDictEqual(result, {
            'status': 999,
            'message': 'Kubernetes error when trying to get status of spark job "test-job" in namespace'
                       ' "test-namespace": Reason'
        })
