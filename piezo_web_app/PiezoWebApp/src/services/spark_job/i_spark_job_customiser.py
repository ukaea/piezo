from abc import ABCMeta, abstractmethod


class ISparkJobCustomiser(metaclass=ABCMeta):

    @abstractmethod
    def rename_job(self, base_name):
        pass
