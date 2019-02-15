class ArgumentValidator:

    def __init__(self):
        self._required_args = ["name", "language", "path_to_main_app_file"]
        self._optional_args = [""]

    def validate_arguments(self, request_body):
        try:
            self._check_all_required_args_are_provided(request_body)
        except ValueError:
            raise

    def _check_all_required_args_are_provided(self, request_body):
        for key in self._required_args:
            try:
                request_body[key]
            except KeyError:
                raise ValueError(f"Missing required argument: {key}")
