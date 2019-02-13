from PiezoWebApp.src.services.application_builder.validator.argument_validator import ArgumentValidator
from PiezoWebApp.src.services.application_builder.template_populator import TemplatePopulator


class ApplicationBuilder:

    def __init__(self):
        self._template_populator = TemplatePopulator()
        self._argument_validator = ArgumentValidator()



    def build_application_definition(self, request_body):
        if request_body["language"] == "Python":
            return self._template_populator.populate_python_job_template(request_body)
        if request_body["language"] == "Scala":
            return self._template_populator.populate_scala_job_template(request_body)
        raise ValueError(f"Language must be one of: {self._argument_validator.valid_languages}")





