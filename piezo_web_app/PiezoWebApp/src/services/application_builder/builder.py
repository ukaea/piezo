from PiezoWebApp.src.services.application_builder.template_populator import TemplatePopulator
from PiezoWebApp.src.services.application_builder.


class ApplicationBuilder:
    def __init__(self):
        self._template_populator = TemplatePopulator()
        self.defaults = {"driver_cores": 0.1,
                         "driver_core_limit": "200m",
                         "driver_memory": "512m",
                         "executors": 1,
                         "executors_cores": 1,
                         "executors_memory": "512m"}

    def build_application_definition(self, request_body):
        argument = self.defaults

        return self._template_populator.build_template(request_body)
