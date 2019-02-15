from abc import ABCMeta, abstractmethod


class IKubernetesAdapter(metaclass=ABCMeta):

    # pylint: disable=too-many-arguments
    @abstractmethod
    def delete_namespaced_custom_object(self, group, version, namespace, plural, name, body):
        pass

    @abstractmethod
    def read_namespaced_pod_log(self, driver_name, namespace):
        pass

    # pylint: disable=too-many-arguments
    @abstractmethod
    def create_namespaced_custom_object(self, group, version, namespace, plural, name, body):
        pass
