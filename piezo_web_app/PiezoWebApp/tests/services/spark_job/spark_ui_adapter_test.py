import kubernetes
import mock
import pytest

from PiezoWebApp.src.services.spark_job.spark_ui_adapter import SparkUiAdapter
from PiezoWebApp.src.utils.configurations import Configuration


class TestSparkUiAdapter:
    @pytest.fixture(autouse=True)
    def setup(self):
        mock_configuration = mock.create_autospec(Configuration)
        mock_configuration.k8s_url = 'http://0.0.0.0:0'
        mock_configuration.is_k8s_secure = False
        self.test_ui_service = SparkUiAdapter(configuration=mock_configuration)

    def test_create_ui_url_returns_url_for_proxy(self):
        # Arrange
        job_name = "test-job"
        # Act
        url = self.test_ui_service.create_ui_url(job_name)
        # Assert
        assert url == "http://0.0.0.0:0/proxy:test-job-ui-svc:4040"

    def test_create_ui_proxy_body_generates_correct_body(self):
        # Arrange
        job_name = "test-job"
        namespace = "default"
        expected_container = kubernetes.client.V1Container(name="test-job-ui-proxy",
                                                           image="networkaispark/spark-ui-proxy:1.0.0",
                                                           ports=[kubernetes.client.V1ContainerPort(80)],
                                                           resources=kubernetes.client.V1ResourceRequirements(
                                                               requests={'cpu': '500m'}),
                                                           args=['test-job-ui-svc:4040', '80'],
                                                           liveness_probe=kubernetes.client.V1Probe(
                                                               http_get=kubernetes.client.V1HTTPGetAction(
                                                                   path='/', port=80),
                                                               initial_delay_seconds=120,
                                                               timeout_seconds=5)
                                                           )
        # Act
        body = self.test_ui_service.create_ui_proxy_body(job_name, namespace)
        # Assert
        assert body.metadata.name == "test-job-ui-proxy"
        assert body.metadata.namespace == "default"
        assert body.metadata.labels == {'name': 'test-job-ui-proxy', 'release': 'piezo'}
        assert body.spec.replicas == 1
        assert body.spec.template.metadata.labels == {'name': 'test-job-ui-proxy', 'release': 'piezo'}
        assert body.spec.template.spec.containers == [expected_container]

    def test_create_ui_svc_body_generates_correct_body(self):
        # Arrange
        job_name = "test-job"
        namespace = "default"
        # Act
        body = self.test_ui_service.create_ui_proxy_svc_body(job_name, namespace)
        # Assert
        assert body.api_version == 'v1'
        assert body.kind == 'Service'
        assert body.metadata.name == 'test-job-ui-proxy'
        assert body.metadata.namespace == 'default'
        assert body.metadata.labels == {'name': 'test-job-ui-proxy', 'release': 'piezo'}
        assert body.spec.type == 'NodePort'
        assert body.spec.selector == {'name': 'test-job-ui-proxy'}
        assert body.spec.ports == [kubernetes.client.V1ServicePort(port=80, target_port=80)]

    def test_create_ui_ingress_body_generates_correct_body(self):
        # Arrange
        job_name = 'test-job'
        expected_rule = kubernetes.client.V1beta1IngressRule(
            host='0.0.0.0',
            http=kubernetes.client.V1beta1HTTPIngressRuleValue(
                paths=[
                    kubernetes.client.V1beta1HTTPIngressPath(
                        backend=kubernetes.client.V1beta1IngressBackend(
                            service_name='test-job-ui-proxy',
                            service_port=80),
                        path='/')
                    ]))
        # Act
        body = self.test_ui_service.create_ui_proxy_ingress_body(job_name)
        # Assert
        assert body.api_version == 'extensions/v1beta1'
        assert body.kind == 'Ingress'
        assert body.metadata.annotations == {'kubernetes.io/ingress.class': 'nginx'}
        assert body.metadata.name == 'test-job-ui-proxy-ingress'
        assert body.spec.backend == kubernetes.client.V1beta1IngressBackend(service_name='test-job-ui-proxy',
                                                                            service_port=80)
        assert body.spec.rules == [expected_rule]

    def test_create_ui_proxy_body_returns_body_when_name_is_none(self):
        # Arrange
        job_name = None
        namespace = "default"
        expected_container = kubernetes.client.V1Container(name="None-ui-proxy",
                                                           image="networkaispark/spark-ui-proxy:1.0.0",
                                                           ports=[kubernetes.client.V1ContainerPort(80)],
                                                           resources=kubernetes.client.V1ResourceRequirements(
                                                               requests={'cpu': '500m'}),
                                                           args=['None-ui-svc:4040', '80'],
                                                           liveness_probe=kubernetes.client.V1Probe(
                                                               http_get=kubernetes.client.V1HTTPGetAction(
                                                                   path='/', port=80),
                                                               initial_delay_seconds=120,
                                                               timeout_seconds=5)
                                                           )
        # Act
        body = self.test_ui_service.create_ui_proxy_body(job_name, namespace)
        # Assert
        assert body.metadata.name == "None-ui-proxy"
        assert body.metadata.namespace == "default"
        assert body.metadata.labels == {'name': 'None-ui-proxy', 'release': 'piezo'}
        assert body.spec.replicas == 1
        assert body.spec.template.metadata.labels == {'name': 'None-ui-proxy', 'release': 'piezo'}
        assert body.spec.template.spec.containers == [expected_container]

    def test_create_ui_ingress_body_generates_body_when_name_is_none(self):
        # Arrange
        job_name = 'test-job'
        expected_rule = kubernetes.client.V1beta1IngressRule(
            host='0.0.0.0',
            http=kubernetes.client.V1beta1HTTPIngressRuleValue(
                paths=[
                    kubernetes.client.V1beta1HTTPIngressPath(
                        backend=kubernetes.client.V1beta1IngressBackend(
                            service_name='test-job-ui-proxy',
                            service_port=80),
                        path='/')
                    ]))
        # Act
        body = self.test_ui_service.create_ui_proxy_ingress_body(job_name)
        # Assert
        assert body.api_version == 'extensions/v1beta1'
        assert body.kind == 'Ingress'
        assert body.metadata.annotations == {'kubernetes.io/ingress.class': 'nginx'}
        assert body.metadata.name == 'test-job-ui-proxy-ingress'
        assert body.spec.backend == kubernetes.client.V1beta1IngressBackend(service_name='test-job-ui-proxy',
                                                                            service_port=80)
        assert body.spec.rules == [expected_rule]

    def test_create_ui_svc_body_generates_body_when_name_is_none(self):
        # Arrange
        job_name = None
        namespace = "default"
        # Act
        body = self.test_ui_service.create_ui_proxy_svc_body(job_name, namespace)
        # Assert
        assert body.api_version == 'v1'
        assert body.kind == 'Service'
        assert body.metadata.name == 'None-ui-proxy'
        assert body.metadata.namespace == 'default'
        assert body.metadata.labels == {'name': 'None-ui-proxy', 'release': 'piezo'}
        assert body.spec.type == 'NodePort'
        assert body.spec.selector == {'name': 'None-ui-proxy'}
        assert body.spec.ports == [kubernetes.client.V1ServicePort(port=80, target_port=80)]

    def test_correct_port_is_used_for_ingress_when_scheme_is_https(self):
        # Arrange
        secure_mock_configuration = mock.create_autospec(Configuration)
        secure_mock_configuration.k8s_url = 'https://1.1.1.1:1'
        secure_mock_configuration.is_k8s_secure = True
        self.test_ui_service = SparkUiAdapter(configuration=secure_mock_configuration)
        job_name = 'test-job'
        expected_rule = kubernetes.client.V1beta1IngressRule(
            host='1.1.1.1',
            http=kubernetes.client.V1beta1HTTPIngressRuleValue(
                paths=[
                    kubernetes.client.V1beta1HTTPIngressPath(
                        backend=kubernetes.client.V1beta1IngressBackend(
                            service_name='test-job-ui-proxy',
                            service_port=443),
                        path='/')
                    ]))
        # Act
        body = self.test_ui_service.create_ui_proxy_ingress_body(job_name)
        # Assert
        assert body.spec.backend == kubernetes.client.V1beta1IngressBackend(service_name='test-job-ui-proxy',
                                                                            service_port=443)
        assert body.spec.rules == [expected_rule]

    def test_correct_port_is_used_for_svc_when_scheme_is_https(self):
        # Arrange
        secure_mock_configuration = mock.create_autospec(Configuration)
        secure_mock_configuration.k8s_url = 'https://1.1.1.1:1'
        secure_mock_configuration.is_k8s_secure = True
        self.test_ui_service = SparkUiAdapter(configuration=secure_mock_configuration)
        job_name = "test_job"
        namespace = "default"
        # Act
        body = self.test_ui_service.create_ui_proxy_svc_body(job_name, namespace)
        # Assert}
        assert body.spec.type == 'NodePort'
        assert body.spec.ports == [kubernetes.client.V1ServicePort(port=443, target_port=443)]
