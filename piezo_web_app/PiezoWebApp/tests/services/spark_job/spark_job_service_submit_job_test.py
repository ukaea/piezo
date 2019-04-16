from kubernetes.client.rest import ApiException
import mock

from PiezoWebApp.src.services.spark_job.spark_job_constants import CRD_GROUP
from PiezoWebApp.src.services.spark_job.spark_job_constants import CRD_PLURAL
from PiezoWebApp.src.services.spark_job.spark_job_constants import CRD_VERSION
from PiezoWebApp.src.services.spark_job.spark_job_constants import NAMESPACE
from PiezoWebApp.src.models.spark_job_validation_result import ValidationResult
from PiezoWebApp.src.models.return_status import StatusCodes

from PiezoWebApp.tests.services.spark_job.spark_job_service_test import TestSparkJobService


class SparkJobServiceSubmitJobTest(TestSparkJobService):
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
                'namespace': NAMESPACE,
                'name': 'test-spark-job-abcd1234',
                'language': 'example-language'
            }
        }
        self.mock_manifest_populator.build_manifest.return_value = manifest
        self.mock_kubernetes_adapter.create_namespaced_custom_object.return_value = {
            'metadata': {
                'namespace': NAMESPACE,
                'name': 'test-spark-job-abcd1234',
                'language': 'example-language'
            }
        }
        self.mock_spark_ui_service.create_ui_url.return_value = 'some_url'
        # Act
        result = self.test_service.submit_job(body)
        # Assert
        self.mock_kubernetes_adapter.create_namespaced_custom_object.assert_called_once_with(
            CRD_GROUP,
            CRD_VERSION,
            NAMESPACE,
            CRD_PLURAL,
            manifest
        )
        self.assertDictEqual(result, {
            'status': StatusCodes.Okay.value,
            'message': 'Job driver created successfully',
            'job_name': 'test-spark-job-abcd1234',
            'spark-ui': 'some_url'
        })

    def test_submit_job_calls_kubernetes_correctly_to_expose_ui(self):
        # Arrange
        body = {
            'name': 'test-spark-job',
            'language': 'example-language'
        }
        self.mock_validation_service.validate_request_keys.return_value = ValidationResult(True, "", None)
        self.mock_validation_service.validate_request_values.return_value = ValidationResult(True, "", body)
        self.mock_spark_job_namer.rename_job.return_value = 'test-spark-job-abcd1234'
        self.mock_spark_ui_service.create_ui_proxy_body.return_value = {'proxy': 'body'}
        self.mock_spark_ui_service.create_ui_proxy_svc_body.return_value = {'svc': 'body'}
        self.mock_spark_ui_service.create_ui_proxy_ingress_body.return_value = {'ingress': 'body'}
        self.mock_spark_ui_service.create_ui_url.return_value = "some.url"
        # Act
        response = self.test_service.submit_job(body)
        # Assert
        self.mock_spark_ui_service.create_ui_proxy_body.assert_called_once_with('test-spark-job-abcd1234', NAMESPACE)
        self.mock_spark_ui_service.create_ui_proxy_svc_body.assert_called_once_with('test-spark-job-abcd1234',
                                                                                    NAMESPACE)
        self.mock_spark_ui_service.create_ui_proxy_ingress_body.assert_called_once_with('test-spark-job-abcd1234')
        self.mock_kubernetes_adapter.create_namespaced_deployment.assert_called_once_with(NAMESPACE, {'proxy': 'body'})
        self.mock_kubernetes_adapter.create_namespaced_service.assert_called_once_with(NAMESPACE, {'svc': 'body'})
        self.mock_kubernetes_adapter.create_namespaced_ingress.assert_called_once_with(NAMESPACE, {'ingress': 'body'})
        self.mock_spark_ui_service.create_ui_url.assert_called_once_with('test-spark-job-abcd1234')
        assert response['spark-ui'] == 'some.url'

    def test_submit_job_returns_ui_url_as_unavailable_if_failure_in_setup(self):
        # Arrange
        body = {
            'name': 'test-spark-job',
            'language': 'example-language'
        }
        self.mock_validation_service.validate_request_keys.return_value = ValidationResult(True, "", None)
        self.mock_validation_service.validate_request_values.return_value = ValidationResult(True, "", body)
        self.mock_spark_job_namer.rename_job.return_value = 'test-spark-job-abcd1234'
        self.mock_spark_ui_service.create_ui_proxy_body.return_value = {'proxy': 'body'}
        self.mock_spark_ui_service.create_ui_proxy_svc_body.return_value = {'svc': 'body'}
        self.mock_spark_ui_service.create_ui_proxy_ingress_body.return_value = {'ingress': 'body'}
        self.mock_kubernetes_adapter.create_namespaced_deployment.side_effect = ApiException('Failure for proxy')
        self.mock_spark_ui_service.create_ui_url.return_value = "some.url"
        # Act
        response = self.test_service.submit_job(body)
        # Assert)
        self.mock_spark_ui_service.create_ui_url.assert_not_called()
        assert response['spark-ui'] == 'Unavailable'

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
                'namespace': NAMESPACE,
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
            NAMESPACE,
            CRD_PLURAL,
            manifest
        )
        expected_message = 'Kubernetes error when trying to submit job: Reason'
        self.mock_logger.error.assert_has_calls([
            mock.call(expected_message),
            mock.call({
                'metadata': {
                    'namespace': NAMESPACE,
                    'name': 'test-spark-job-abcd1234',
                    'language': 'example-language'
                }
            })
        ])
        self.assertDictEqual(result, {
            'status': 999,
            'message': expected_message
        })
