from abc import ABCMeta, abstractmethod


class ISparkJobCustomiser(metaclass=ABCMeta):

    @abstractmethod
    def rename_job(self, base_name):
        pass

    @abstractmethod
    def set_output_dir_as_first_argument(self, job_name, storage_service, validated_body_values):
        pass
