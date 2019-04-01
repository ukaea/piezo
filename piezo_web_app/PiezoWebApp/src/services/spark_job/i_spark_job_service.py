from abc import ABCMeta, abstractmethod


class ISparkJobService(metaclass=ABCMeta):

    @abstractmethod
    def delete_job(self, job_name):
        pass

    @abstractmethod
    def get_jobs(self, label):
        pass

    @abstractmethod
    def get_job_status(self, job_name):
        pass

    @abstractmethod
    def get_logs(self, job_name):
        pass

    @abstractmethod
    def submit_job(self, body):
        pass

    @abstractmethod
    def tidy_jobs(self):
        pass

    @abstractmethod
    def write_logs_to_file(self, job_name):
        pass
