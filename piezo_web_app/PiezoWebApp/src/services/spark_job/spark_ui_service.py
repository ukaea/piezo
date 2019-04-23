from urllib.parse import urlparse

import kubernetes

from PiezoWebApp.src.services.spark_job.i_spark_ui_service import ISparkUiService


# ONLY CHANGE CONSTANTS IF YOU KNOW WHAT YOU ARE DOING
UI_PORT = '4040'  # Port that the UI is exposed from the UI service (set by the spark operator)
RELEASE_LABEL = 'piezo'  # Identifier label to allow for easy clean up
PROXY_IMAGE = 'networkaispark/spark-ui-proxy:1.0.0'  # Docker image for spark ui proxy
PROXY_RESOURCES = {'cpu': '500m'}  # Resources limits to allocate to each proxy pod
PROBE_DELAY = 120   # Seconds before first check if proxy is running. Shuts down if not
PROBE_TIMEOUT = 5   # Seconds after check if proxy is running times out
HTTP_INGRESS_PORT = 80  # Default port for an ingress on http
HTTPS_INGRESS_PORT = 443  # Default port for an ingress on https


class SparkUiService(ISparkUiService):
    def __init__(self, configuration):
        self._k8s_url = configuration.k8s_url
        self._proxy_port = HTTPS_INGRESS_PORT if configuration.is_k8s_secure else HTTP_INGRESS_PORT

    def create_ui_proxy_body(self, job_name, namespace):
        proxy_name = f'{job_name}-ui-proxy'
        deployment_metadata = kubernetes.client.V1ObjectMeta(labels={'name': proxy_name, 'release': f'{RELEASE_LABEL}'},
                                                             name=proxy_name,
                                                             namespace=namespace)
        deployment_template_metadata = kubernetes.client.V1ObjectMeta(labels={'name': proxy_name,
                                                                              'release': f'{RELEASE_LABEL}'})
        port = kubernetes.client.V1ContainerPort(container_port=self._proxy_port)
        resources = kubernetes.client.V1ResourceRequirements(requests=PROXY_RESOURCES)
        http_get = kubernetes.client.V1HTTPGetAction(path='/', port=self._proxy_port)
        probe = kubernetes.client.V1Probe(http_get=http_get,
                                          initial_delay_seconds=PROBE_DELAY,
                                          timeout_seconds=PROBE_TIMEOUT)
        container = kubernetes.client.V1Container(name=proxy_name,
                                                  image=PROXY_IMAGE,
                                                  ports=[port],
                                                  resources=resources,
                                                  args=[f'{job_name}-ui-svc:{UI_PORT}', str(self._proxy_port)],
                                                  liveness_probe=probe)
        template_spec = kubernetes.client.V1PodSpec(containers=[container])
        deployment_template = kubernetes.client.V1PodTemplateSpec(metadata=deployment_template_metadata,
                                                                  spec=template_spec)
        deployment_spec = kubernetes.client.ExtensionsV1beta1DeploymentSpec(replicas=1, template=deployment_template)
        return kubernetes.client.ExtensionsV1beta1Deployment(api_version='extensions/v1beta1',
                                                             kind='Deployment',
                                                             metadata=deployment_metadata,
                                                             spec=deployment_spec)

    def create_ui_proxy_svc_body(self, job_name, namespace):
        proxy_name = f'{job_name}-ui-proxy'
        service_port = kubernetes.client.V1ServicePort(port=self._proxy_port, target_port=self._proxy_port)
        service_metadata = kubernetes.client.V1ObjectMeta(labels={'name': proxy_name, 'release': f'{RELEASE_LABEL}'},
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
                                                  labels={'name': service_name, 'release': f'{RELEASE_LABEL}'})
        backend = kubernetes.client.V1beta1IngressBackend(service_name=service_name, service_port=self._proxy_port)
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
        url = self._k8s_url + f'/proxy:{job_name}-ui-svc:{UI_PORT}'
        return url
