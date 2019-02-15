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
        self._required_for_app_args = ["name",
                                       "language",
                                       "path_to_main_app_file",
                                       "driver_cores",
                                       "driver_core_limit",
                                       "driver_memory",
                                       "executors",
                                       "executor_cores",
                                       "executor_memory"]
        self.validation_rules = ValidationRules()

    def validate_arguments(self, request_body):
        self._validate_language_requirements(request_body)
        try:
            self._check_all_required_args_are_provided(request_body)
        except ValueError:
            raise

        validated_args = ArgumentValidator._check_provided_args_are_valid(request_body)

        full_validated_args = ArgumentValidator._add_defaults_for_non_user_required_args(self._optional_from_user_args,
                                                                                         validated_args)
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
            self._required_for_app_args.append("pythonVersion")
        elif language == "scala":
            self._required_for_app_args.append("main_class")

    @staticmethod
    def _check_provided_args_are_valid(request_body):
        for key in request_body:
            try:
                SparkJobProperty(key).validate(request_body[key])
            except ValueError:
                raise
        return request_body

    @staticmethod
    def _add_defaults_for_non_user_required_args(all_optional_args, current_validated_args):
        args_to_add = [arg for arg in all_optional_args if arg not in current_validated_args]
        for arg in args_to_add:
            arg_default = SparkJobProperty(arg).default()
            current_validated_args[arg] = arg_default
        return current_validated_args

