from abc import ABCMeta, abstractmethod


class ISparkJobCustomiser(metaclass=ABCMeta):

    @abstractmethod
    def rename_job(self, base_name):
        pass

    @staticmethod
    @abstractmethod
    def set_output_dir_as_first_argument(job_name, storage_service, validated_body_values):
        pass
