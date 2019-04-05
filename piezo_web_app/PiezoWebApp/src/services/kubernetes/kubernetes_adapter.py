import kubernetes

from PiezoWebApp.src.services.kubernetes.i_kubernetes_adapter import IKubernetesAdapter


class KubernetesAdapter(IKubernetesAdapter):
    def __init__(self, config):
        api_client = kubernetes.client.ApiClient(config)
        self._core_connection = kubernetes.client.CoreV1Api(api_client)
        self._custom_connection = kubernetes.client.CustomObjectsApi(api_client)
        self._extension_connection = kubernetes.client.ExtensionsV1beta1Api(api_client)

    # pylint: disable=too-many-arguments
    def delete_namespaced_custom_object(self, group, version, namespace, plural, name, body):
        return self._custom_connection.delete_namespaced_custom_object(group, version, namespace, plural, name, body)

    # pylint: disable=too-many-arguments
    def delete_options(self,
                       api_version=None,
                       dry_run=None,
                       grace_period_seconds=None,
                       kind=None,
                       orphan_dependents=None,
                       pre_conditions=None,
                       propagation_policy=None):
        return {'api_version': api_version,
                'dry_run': dry_run,
                'grace_period_seconds': grace_period_seconds,
                'kind': kind,
                'orphan_dependents': orphan_dependents,
                'preconditions': pre_conditions,
                'propagation_policy': propagation_policy}

    def read_namespaced_pod_log(self, driver_name, namespace):
        return self._core_connection.read_namespaced_pod_log(driver_name, namespace)

    # pylint: disable=too-many-arguments
    def create_namespaced_custom_object(self, group, version, namespace, plural, body):
        return self._custom_connection.create_namespaced_custom_object(group, version, namespace, plural, body)

    def get_namespaced_custom_object(self, group, version, namespace, plural, name):
        return self._custom_connection.get_namespaced_custom_object(group, version, namespace, plural, name)

    def list_namespaced_custom_object(self, group, version, namespace, plural, **kwargs):
        return self._custom_connection.list_namespaced_custom_object(group, version, namespace, plural, **kwargs)


    def expose_spark_ui(self, namespace, job_name):
        # spark ui proxy deployment
        proxy_name = job_name + '-ui-proxy'
        deployment_metadata = kubernetes.client.V1ObjectMeta(labels={'name': proxy_name},
                                                             name=proxy_name,
                                                             namespace=namespace)
        template_metadata = kubernetes.client.V1ObjectMeta(labels={'name': proxy_name})
        port = kubernetes.client.V1ContainerPort(container_port=80)
        resources = kubernetes.client.V1ResourceRequirements(requests={'cpu': '100m'})
        http_get = kubernetes.client.V1HTTPGetAction(path='/', port=80)
        probe = kubernetes.client.V1Probe(http_get=http_get, initial_delay_seconds=120, timeout_seconds=5)
        container = kubernetes.client.V1Container(name=proxy_name,
                                                  image='networkaispark/spark-ui-proxy:1.0.0',
                                                  ports=[port],
                                                  resources=resources,
                                                  args=[f'{job_name}-driver:4040'],
                                                  liveness_probe=probe)
        template_spec = kubernetes.client.V1PodSpec(containers=[container])
        deployment_template = kubernetes.client.V1PodTemplateSpec(metadata=template_metadata,
                                                                  spec=template_spec)
        deployment_spec = kubernetes.client.ExtensionsV1beta1DeploymentSpec(replicas=1, template=deployment_template)
        deployment_body = kubernetes.client.ExtensionsV1beta1Deployment(api_version='extensions/v1beta1',
                                                                        kind='Deployment',
                                                                        metadata=deployment_metadata,
                                                                        spec=deployment_spec)
        self._extension_connection.create_namespaced_deployment(namespace, deployment_body)

        # spark ui proxy sevice
        service_port = kubernetes.client.V1ServicePort(port=80, target_port=80)
        service_spec = kubernetes.client.V1ServiceSpec(ports=[service_port],
                                                       selector={'name': proxy_name},
                                                       type='NodePort')
        service_body = kubernetes.client.V1Service(api_version='v1',
                                                   kind='Service',
                                                   metadata=deployment_metadata,
                                                   spec=service_spec)
        self._core_connection.create_namespaced_service(namespace=namespace, body=service_body)

        # spark ui proxy ingress
        ingress_name = f'{proxy_name}-ingress'
        path = f'/{job_name}/?(.*)'
        metadata = kubernetes.client.V1ObjectMeta(annotations={'kubernetes.io/ingress.class': 'nginx', 'nginx.ingress.kubernetes.io/rewrite-target': '/$1', 'nginx.ingress.kubernetes.io/app-root': f'/{job_name}'}, name=ingress_name)
        backend = kubernetes.client.V1beta1IngressBackend(service_name=proxy_name, service_port=4040)
        ingress_path = kubernetes.client.V1beta1HTTPIngressPath(backend=backend, path=path)
        http = kubernetes.client.V1beta1HTTPIngressRuleValue(paths=[ingress_path])
        rules = kubernetes.client.V1beta1IngressRule(host=f'host-172-16-113-146.nubes.stfc.ac.uk', http=http)
        spec = kubernetes.client.V1beta1IngressSpec(backend=backend, rules=[rules])
        ingress_body = kubernetes.client.V1beta1Ingress(api_version='extensions/v1beta1', kind='Ingress', metadata=metadata, spec=spec)
        

