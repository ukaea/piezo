from abc import ABCMeta, abstractmethod


class ISparkJobService(metaclass=ABCMeta):

    @abstractmethod
    def delete_job(self, job_name, namespace):
        pass

    @abstractmethod
    def get_jobs(self, label):
        pass

    @abstractmethod
    def get_job_status(self, job_name, namespace):
        pass

    @abstractmethod
    def get_logs(self, job_name, namespace):
        pass

    @abstractmethod
    def submit_job(self, body):
        pass
