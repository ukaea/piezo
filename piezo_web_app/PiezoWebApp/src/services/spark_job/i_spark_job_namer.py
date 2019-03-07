from abc import ABCMeta, abstractmethod


class ISparkJobNamer(metaclass=ABCMeta):

    @abstractmethod
    def rename_job(self, base_name):
        pass
