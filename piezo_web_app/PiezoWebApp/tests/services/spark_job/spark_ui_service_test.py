from logging import Logger

import mock
import pytest

from PiezoWebApp.src.services.spark_job.spark_job_constants import NAMESPACE
from PiezoWebApp.src.services.kubernetes.i_kubernetes_adapter import IKubernetesAdapter
from PiezoWebApp.src.services.spark_job.i_spark_ui_adapter import ISparkUiAdapter
from PiezoWebApp.src.services.spark_job.spark_ui_service import SparkUiService


class TestSparkUiService:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.mock_logger = mock.create_autospec(Logger)
        self.mock_spark_ui_adapter = mock.create_autospec(ISparkUiAdapter)
        self.mock_k8s_adapter = mock.create_autospec(IKubernetesAdapter)
        self.mock_spark_ui_adapter.create_ui_url.return_value = "ui.url"
        self.test_ui_service = SparkUiService(self.mock_k8s_adapter,
                                              self.mock_spark_ui_adapter,
                                              self.mock_logger)

    def test_expose_ui_calls_spark_ui_adapter_and_k8s_adapter(self):
        # Arrange
        job_name = "test_job"
        self.mock_spark_ui_adapter.create_ui_proxy_body.return_value = "proxy_body"
        self.mock_spark_ui_adapter.create_ui_proxy_svc_body.return_value = "svc_body"
        self.mock_spark_ui_adapter.create_ui_proxy_ingress_body.return_value = "ingress_body"
        # Act
        url = self.test_ui_service.expose_spark_ui(job_name)
        # Assert
        assert url == "ui.url"
        self.mock_spark_ui_adapter.create_ui_proxy_body.assert_called_once_with("test_job", NAMESPACE)
        self.mock_spark_ui_adapter.create_ui_proxy_svc_body.assert_called_once_with("test_job", NAMESPACE)
        self.mock_spark_ui_adapter.create_ui_proxy_ingress_body.assert_called_once_with("test_job")
        self.mock_k8s_adapter.create_namespaced_deployment.assert_called_once_with(NAMESPACE, "proxy_body")
        self.mock_k8s_adapter.create_namespaced_service.assert_called_once_with(NAMESPACE, "svc_body")
        self.mock_k8s_adapter.create_namespaced_ingress.assert_called_once_with(NAMESPACE, "ingress_body")

    def test_expose_ui_accepts_name_as_none(self):
        # Arrange
        job_name = None
        self.mock_spark_ui_adapter.create_ui_proxy_body.return_value = "proxy_body"
        self.mock_spark_ui_adapter.create_ui_proxy_svc_body.return_value = "svc_body"
        self.mock_spark_ui_adapter.create_ui_proxy_ingress_body.return_value = "ingress_body"
        # Act
        url = self.test_ui_service.expose_spark_ui(job_name)
        # Assert
        assert url == "ui.url"
        self.mock_spark_ui_adapter.create_ui_proxy_body.assert_called_once_with(None, NAMESPACE)
        self.mock_spark_ui_adapter.create_ui_proxy_svc_body.assert_called_once_with(None, NAMESPACE)
        self.mock_spark_ui_adapter.create_ui_proxy_ingress_body.assert_called_once_with(None)
        self.mock_k8s_adapter.create_namespaced_deployment.assert_called_once_with(NAMESPACE, "proxy_body")
        self.mock_k8s_adapter.create_namespaced_service.assert_called_once_with(NAMESPACE, "svc_body")
        self.mock_k8s_adapter.create_namespaced_ingress.assert_called_once_with(NAMESPACE, "ingress_body")

    def test_delete_spark_ui_components_calls_k8s_adapter(self):
        # Arrange
        job_name = "test_job"
        body = "body"
        # Act
        self.test_ui_service.delete_spark_ui_components(job_name, body)
        # Assert
        self.mock_k8s_adapter.delete_namespaced_deployment.assert_called_once_with("test_job-ui-proxy", NAMESPACE, body)
        self.mock_k8s_adapter.delete_namespaced_service.assert_called_once_with("test_job-ui-proxy", NAMESPACE, body)
        self.mock_k8s_adapter.delete_namespaced_ingress.assert_called_once_with("test_job-ui-proxy-ingress",
                                                                                NAMESPACE,
                                                                                body)

    def test_delete_spark_ui_components_accepts_name_as_none(self):
        # Arrange
        job_name = None
        body = "body"
        # Act
        self.test_ui_service.delete_spark_ui_components(job_name, body)
        # Assert
        self.mock_k8s_adapter.delete_namespaced_deployment.assert_called_once_with("None-ui-proxy", NAMESPACE, body)
        self.mock_k8s_adapter.delete_namespaced_service.assert_called_once_with("None-ui-proxy", NAMESPACE, body)
        self.mock_k8s_adapter.delete_namespaced_ingress.assert_called_once_with("None-ui-proxy-ingress",
                                                                                NAMESPACE,
                                                                                body)
