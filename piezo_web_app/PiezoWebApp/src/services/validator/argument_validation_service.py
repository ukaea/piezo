from PiezoWebApp.src.services.validator.spark_job_property import SparkJobProperty
from PiezoWebApp.src.services.validator.validation_result import ValidationResult


class ArgumentValidationService:

    def __init__(self, validation_rules):
        self._validation_rules = validation_rules
        self._required_args_from_user = self._validation_rules.get_keys_of_required_args
        self._optional_args_from_user = self._validation_rules.get_keys_of_optional_args

    def validate_request_keys(self, request_body):
        # Ensure all vars needed are present
        language_validation_result = self._validate_language_requirements(request_body)
        validated_language_results = language_validation_result.validated_value

        required_args_validation_result_dict = self._check_all_required_args_are_provided(validated_language_results)
        # check for unsupported args
        unsupported_args = self._check_for_unsupported_args(request_body)
        return ArgumentValidationService._validate_request_keys_return_helper(language_validation_result,
                                                                              required_args_validation_result_dict,
                                                                              unsupported_args)

    @staticmethod
    def validate_request_values(request_body):
        validated_args_dict = ArgumentValidationService._check_provided_arg_values_are_valid(request_body)
        return validated_args_dict

    def _check_all_required_args_are_provided(self, request_body):
        required_args_validation_result_dict = \
            {key: ValidationResult(True, None, None) for key in self._required_args_from_user}
        for key in self._required_args_from_user:
            if key not in request_body:
                required_args_validation_result_dict[key] = \
                    ValidationResult(False, f"Missing required argument {key}", None)
        return required_args_validation_result_dict

    def _validate_language_requirements(self, request_body):
        try:
            language = request_body["language"].lower()
        except KeyError:
            return ValidationResult(False, "Missing required argument 'language'", None)
        valid_language_array = ["python", "scala"]
        if language not in valid_language_array:
            return ValidationResult(False, f"Invalid language provided, please use one of {valid_language_array}", None)

        if language == "python":
            request_body["language"] = "Python"
            self._required_args_from_user.append("python_version")
        elif language == "scala":
            request_body["language"] = "Scala"
            self._required_args_from_user.append("main_class")
        return ValidationResult(True, "language validated", request_body)

    def _check_provided_arg_values_are_valid(self, request_body):
        validated_dict = {}
        error_msg = "The following errors occurred when validating request body values: \n"
        all_valid = True
        for key in request_body:
            validation_response = SparkJobProperty(key, self._validation_rules).validate(request_body[key])
            if validation_response.is_valid is True:
                validated_dict[key] = validation_response.validated_value
            else:
                error_msg += validation_response.message
                all_valid = False
        return ValidationResult(all_valid, error_msg, validated_dict)

    def _check_for_unsupported_args(self, request_body):
        unsupported_args = []
        supported_args = self._required_args_from_user + self._optional_args_from_user
        for arg in request_body:
            if arg not in supported_args:
                unsupported_args.append(arg)
        return unsupported_args

    @staticmethod
    def _validate_request_keys_return_helper(language_verification_result,
                                             required_args_validation_result_dict,
                                             unsupported_args):
        all_required_present = all(
            required_args_validation_result_dict[arg].is_valid is True for arg in required_args_validation_result_dict)
        if language_verification_result.is_valid is True and all_required_present is True and not unsupported_args:
            return ValidationResult(True, "All argument keys provided are valid", None)
        else:
            error_msg = "The following errors were found: \n"
            if language_verification_result.is_valid is False:
                error_msg += language_verification_result.message + "\n"
            for arg in required_args_validation_result_dict:
                if required_args_validation_result_dict[arg].is_valid is False:
                    error_msg += required_args_validation_result_dict[arg].message + "\n"
            for arg in unsupported_args:
                error_msg += f"Unsupported argument {arg} provided \n"
        return ValidationResult(False, error_msg, None)
