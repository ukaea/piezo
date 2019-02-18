from PiezoWebApp.src.services.validator.spark_job_property import SparkJobProperty
from PiezoWebApp.src.services.validator.validation_rules import ValidationRules


class ArgumentValidator:

    def __init__(self):
        self._required_from_user_args = ["name", "language", "path_to_main_app_file"]
        self._optional_from_user_args = ["driver_cores",
                                         "driver_core_limit",
                                         "driver_memory",
                                         "executors",
                                         "executor_cores",
                                         "executor_memory"]
        self.validation_rules = ValidationRules()

    def validate_arguments(self, request_body):
        # Ensure all ars needed are present
        try:
            self._validate_language_requirements(request_body)
            self._check_all_required_args_are_provided(request_body)
        except ValueError:
            raise
        # Remove unsupported args
        args_to_validate = self._remove_unsupported_args(request_body)
        # Validate remaining args
        validated_args = ArgumentValidator._check_provided_arg_values_are_valid(args_to_validate)
        # Add default values where needed
        full_validated_args = self._add_defaults_for_non_user_required_args(validated_args)
        return full_validated_args

    def _check_all_required_args_are_provided(self, request_body):
        for key in self._required_from_user_args:
            try:
                request_body[key]
            except KeyError:
                raise ValueError(f"Missing required argument: {key}")

    def _validate_language_requirements(self, request_body):
        try:
            language = request_body["language"].lower()
        except KeyError:
            raise ValueError("Missing required argument: language")
        valid_language_array = ["python", "scala"]
        if language not in valid_language_array:
            raise ValueError(f"Invalid language provided, please use one of {valid_language_array}")

        if language == "python":
            request_body["language"] = "Python"
            self._optional_from_user_args.append("python_version")
        elif language == "scala":
            request_body["language"] = "Scala"
            self._optional_from_user_args.append("main_class")

    @staticmethod
    def _check_provided_arg_values_are_valid(request_body):
        for key in request_body:
            try:
                SparkJobProperty(key).validate(request_body[key])
            except ValueError:
                raise
        return request_body

    def _add_defaults_for_non_user_required_args(self, current_validated_args):
        args_to_add = [arg for arg in self._optional_from_user_args if arg not in current_validated_args]
        for arg in args_to_add:
            arg_default = SparkJobProperty(arg).default
            current_validated_args[arg] = arg_default
        return current_validated_args

    def _remove_unsupported_args(self, request_body):
        supported_args = self._required_from_user_args + self._optional_from_user_args
        return {arg: request_body[arg] for arg in supported_args}
