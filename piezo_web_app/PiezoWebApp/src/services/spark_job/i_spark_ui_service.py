from abc import ABCMeta, abstractmethod


class ISparkUiService(metaclass=ABCMeta):
    @abstractmethod
    def get_spark_ui_url(self, job_name):
        pass

    @abstractmethod
    def expose_spark_ui(self, job_name):
        pass

    @abstractmethod
    def delete_spark_ui_components(self, job_name, body):
        pass
