from abc import ABCMeta, abstractmethod


class IKubernetesService(metaclass=ABCMeta):

    @abstractmethod
    def delete_job(self, job_name, namespace):
        pass

    @abstractmethod
    def get_logs(self, driver_name, namespace):
        pass

    @abstractmethod
    def submit_job(self, body):
        pass
