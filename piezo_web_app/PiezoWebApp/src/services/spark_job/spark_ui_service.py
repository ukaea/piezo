from urllib.parse import urlparse

from PiezoWebApp.src.services.spark_job.i_spark_ui_service import ISparkUiService
import kubernetes


class SparkUiService(ISparkUiService):
    def __init__(self, configuration):
        self._k8s_url = configuration.k8s_url

    @staticmethod
    def create_ui_proxy_body(job_name, namespace):
        proxy_name = f'{job_name}-ui-proxy'
        deployment_metadata = kubernetes.client.V1ObjectMeta(labels={'name': proxy_name, 'release': 'piezo'},
                                                             name=proxy_name,
                                                             namespace=namespace)
        deployment_template_metadata = kubernetes.client.V1ObjectMeta(labels={'name': proxy_name, 'release': 'piezo'})
        port = kubernetes.client.V1ContainerPort(container_port=80)
        resources = kubernetes.client.V1ResourceRequirements(requests={'cpu': '500m'})
        http_get = kubernetes.client.V1HTTPGetAction(path='/', port=80)
        probe = kubernetes.client.V1Probe(http_get=http_get, initial_delay_seconds=120, timeout_seconds=5)
        container = kubernetes.client.V1Container(name=proxy_name,
                                                  image='networkaispark/spark-ui-proxy:1.0.0',
                                                  ports=[port],
                                                  resources=resources,
                                                  args=[f'{job_name}-ui-svc:4040', '80'],
                                                  liveness_probe=probe)
        template_spec = kubernetes.client.V1PodSpec(containers=[container])
        deployment_template = kubernetes.client.V1PodTemplateSpec(metadata=deployment_template_metadata,
                                                                  spec=template_spec)
        deployment_spec = kubernetes.client.ExtensionsV1beta1DeploymentSpec(replicas=1, template=deployment_template)
        return kubernetes.client.ExtensionsV1beta1Deployment(api_version='extensions/v1beta1',
                                                             kind='Deployment',
                                                             metadata=deployment_metadata,
                                                             spec=deployment_spec)

    @staticmethod
    def create_ui_proxy_svc_body(job_name, namespace):
        proxy_name = f'{job_name}-ui-proxy'
        service_port = kubernetes.client.V1ServicePort(port=80, target_port=80)
        service_metadata = kubernetes.client.V1ObjectMeta(labels={'name': proxy_name, 'release': 'piezo'},
                                                          name=proxy_name,
                                                          namespace=namespace)
        service_spec = kubernetes.client.V1ServiceSpec(ports=[service_port],
                                                       selector={'name': proxy_name},
                                                       type='NodePort')
        return kubernetes.client.V1Service(api_version='v1',
                                           kind='Service',
                                           metadata=service_metadata,
                                           spec=service_spec)

    def create_ui_proxy_ingress_body(self, job_name):
        service_name = f'{job_name}-ui-proxy'
        ingress_name = f'{service_name}-ingress'
        path = f'/'
        metadata = kubernetes.client.V1ObjectMeta(annotations={'kubernetes.io/ingress.class': 'nginx'},
                                                  name=ingress_name,
                                                  labels={'name': service_name, 'release': 'piezo'})
        backend = kubernetes.client.V1beta1IngressBackend(service_name=service_name, service_port=80)
        ingress_path = kubernetes.client.V1beta1HTTPIngressPath(backend=backend, path=path)
        http = kubernetes.client.V1beta1HTTPIngressRuleValue(paths=[ingress_path])
        host = urlparse(self._k8s_url).hostname
        rules = kubernetes.client.V1beta1IngressRule(host=host, http=http)
        spec = kubernetes.client.V1beta1IngressSpec(backend=backend, rules=[rules])
        return kubernetes.client.V1beta1Ingress(api_version='extensions/v1beta1',
                                                kind='Ingress',
                                                metadata=metadata,
                                                spec=spec)

    def create_ui_url(self, job_name):
        url = self._k8s_url + f'/proxy:{job_name}-ui-svc:4040'
        return url
