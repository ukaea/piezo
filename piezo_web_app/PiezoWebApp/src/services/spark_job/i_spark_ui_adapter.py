from abc import ABCMeta


class ISparkUiAdapter(metaclass=ABCMeta):
    @staticmethod
    def create_ui_proxy_body(job_name, namespace):
        pass

    @staticmethod
    def create_ui_proxy_svc_body(job_name, namespace):
        pass

    @staticmethod
    def create_ui_proxy_ingress_body(job_name):
        pass

    @staticmethod
    def create_ui_url(job_name):
        pass
