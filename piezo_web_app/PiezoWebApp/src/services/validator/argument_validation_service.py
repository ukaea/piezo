from PiezoWebApp.src.services.validator.spark_job_property import SparkJobProperty


class ArgumentValidationService:

    def __init__(self):
        self._required_args_from_user = ["name", "language", "path_to_main_app_file"]
        self._optional_args_from_user = ["driver_cores",
                                         "driver_core_limit",
                                         "driver_memory",
                                         "executors",
                                         "executor_cores",
                                         "executor_memory"]

    def validate_arguments(self, request_body):
        # Ensure all vars needed are present
        try:
            self._validate_language_requirements(request_body)
            self._check_all_required_args_are_provided(request_body)
        except ValueError:
            raise
        # check for unsupported args
        args_to_validate = self._check_for_unsupported_args(request_body)
        # Validate remaining args
        validated_args_dict = ArgumentValidationService._check_provided_arg_values_are_valid(args_to_validate)
        return validated_args_dict

    def _check_all_required_args_are_provided(self, request_body):
        for key in self._required_args_from_user:
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
            self._required_args_from_user.append("python_version")
        elif language == "scala":
            request_body["language"] = "Scala"
            self._required_args_from_user.append("main_class")

    @staticmethod
    def _check_provided_arg_values_are_valid(request_body):
        for key in request_body:
            try:
                request_body[key] = SparkJobProperty(key).validate(request_body[key]).validated_value
            except ValueError:
                raise
        return request_body

    def _check_for_unsupported_args(self, request_body):
        supported_args = self._required_args_from_user + self._optional_args_from_user
        for arg in request_body:
            if arg not in supported_args:
                raise ValueError(f"Argument {arg} is not a supported argument")
        return request_body
