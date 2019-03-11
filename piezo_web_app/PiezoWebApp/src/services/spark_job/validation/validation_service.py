from PiezoWebApp.src.models.spark_job_validation_result import ValidationResult
from PiezoWebApp.src.services.spark_job.validation.i_validation_service import IValidationService
from PiezoWebApp.src.services.spark_job.validation.argument_validator import validate
from PiezoWebApp.src.utils.dict_argument_helper import get_set_difference


class ValidationService(IValidationService):

    def __init__(self, validation_ruleset):
        self._validation_ruleset = validation_ruleset

    def validate_request_keys(self, request_body):
        is_valid = True
        error_msg = "The following errors were found:\n"
        # Get keys required/supported
        required_keys = self._validation_ruleset.get_keys_of_required_inputs()
        if 'language' in request_body:
            language = request_body['language']
            rule = self._validation_ruleset.get_validation_rule_for_key('language')
            validation_result = validate('language', language, rule)
            if validation_result.is_valid:
                required_keys += self._validation_ruleset.get_keys_for_language(request_body['language'])
            else:
                is_valid = False
                error_msg += f'Unsupported language "{language}" provided\n'
        supported_keys = required_keys + self._validation_ruleset.get_keys_of_optional_inputs()

        # Find any discrepancies
        missing_keys = get_set_difference(required_keys, request_body)
        unsupported_keys = get_set_difference(request_body, supported_keys)

        # Group the results together
        for key in missing_keys:
            is_valid = False
            error_msg += f'Missing required input "{key}"\n'
        for key in unsupported_keys:
            is_valid = False
            error_msg += f'Unsupported input "{key}" provided\n'
        result = ValidationResult(
            is_valid,
            "All input keys provided are valid\n" if is_valid else error_msg,
            None
        )

        return result

    def validate_request_values(self, request_body):
        validated_dict = {}
        error_msg = "The following errors were found:\n"
        is_valid = True

        for key, input_value in request_body.items():
            rule_for_key = self._validation_ruleset.get_validation_rule_for_key(key)
            validation_result = validate(key, input_value, rule_for_key)
            if validation_result.is_valid is True:
                validated_dict[key] = validation_result.validated_value
            else:
                error_msg += validation_result.message + '\n'
                is_valid = False

        result = ValidationResult(
            is_valid,
            "All inputs provided are valid\n" if is_valid else error_msg,
            validated_dict if is_valid else None
        )
        return result
