from abc import ABCMeta, abstractmethod


class ISparkUiService(metaclass=ABCMeta):
    @staticmethod
    def create_ui_proxy_body(job_name, namespace):
        pass

    @staticmethod
    def create_ui_proxy_svc_body(job_name, namespace):
        pass

    @staticmethod
    def create_ui_proxy_ingress_body(job_name):
        pass

    @abstractmethod
    def create_ui_url(self, job_name):
        pass
