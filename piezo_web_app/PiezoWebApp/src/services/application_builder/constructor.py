from PiezoWebApp.src.services.application_builder.template_populator import TemplatePopulator


class ApplicationBuilder:
    def __init__(self):
        self._template_populator = TemplatePopulator()

    def build_application_definition(self, request_body):
        self._template_populator.build_template(request_body)
