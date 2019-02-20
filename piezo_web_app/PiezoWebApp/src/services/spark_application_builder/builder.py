from PiezoWebApp.src.services.spark_application_builder.manifest_populator import ManifestPopulator
from PiezoWebApp.src.services.validator.validation_rules import ValidationRules
from PiezoWebApp.src.services.validator.argument_validation_service import ArgumentValidationService


class ApplicationBuilder:
    def __init__(self):
        self.validation_rules = ValidationRules
        self._manifest_populator = ManifestPopulator(self.validation_rules)
        self._argument_validation_service = ArgumentValidationService(self.validation_rules)

    def build_application_definition(self, request_body):
        request_keys_validation_response = self._argument_validation_service.validate_request_keys(request_body)
        if request_keys_validation_response.is_valid is False:
            pass
        request_values_validation_response = self._argument_validation_service.validate_request_values(request_body)
        if request_values_validation_response.is_valid is False:
            pass
        validated_body = request_values_validation_response.validated_value
        return self._manifest_populator.build_manifest(validated_body)
