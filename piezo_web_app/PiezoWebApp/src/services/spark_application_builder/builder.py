from PiezoWebApp.src.services.spark_application_builder.manifest_populator import ManifestPopulator
from PiezoWebApp.src.services.validator.validation_rules import ValidationRules
from PiezoWebApp.src.services.validator.argument_validation_service import ArgumentValidationService

class ApplicationBuilder:
    def __init__(self):
        self.validation_rules = ValidationRules
        self._manifest_populator = ManifestPopulator(self.validation_rules)
        self._argument_validation_service = ArgumentValidationService(self.validation_rules)


    def build_application_definition(self, request_body):
         = self._argument_validation_service.validate_arguments(request_body)

        return self._manifest_populator.build_manifest(request_body, self.validation_rules)
