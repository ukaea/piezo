from PiezoWebApp.src.services.validator.validation_rules import ValidationRules
from PiezoWebApp.src.services.validator import validator


class SparkJobProperty:

    def __init__(self, key):
        self._key = key
        self._min = None
        self._max = None
        self._default = None
        self._required_format = None
        self._validation_rules = ValidationRules()
        self._parse(key)

    def _parse(self, key):
        validation_properties = self._validation_rules.get_keys_property_array(key)
        self._min = validation_properties[0]
        self._max = validation_properties[1]
        self._default = validation_properties[2]
        self._required_format = validation_properties[3]

    @property
    def default(self):
        return self._default

    @property
    def min(self):
        return self._min

    @property
    def max(self):
        return self._max

    @property
    def required_format(self):
        return self._required_format

    def validate(self, value):
        try:
            if self._key == "name":
                return validator.validate_name(value)
            elif self._key == "language":
                return validator.validate_language(value)
            elif self._key == "python_version":
                return validator.validate_python_version(value)
            elif self._key == "path_to_main_app_file":
                return validator.validate_path_to_main_app_file(value)
            elif self._key == "main_class":
                return validator.validate_main_class(value)
            elif self._key == "driver_cores":
                return validator.validate_driver_cores(value, self._min, self._max)
            elif self._key == "driver_core_limit":
                return validator.validate_driver_core_limit(value, self._min, self._max)
            elif self._key == "driver_memory":
                return validator.validate_driver_memory(value, self._min, self._max)
            elif self._key == "executors":
                return validator.validate_executors(value, self._min, self._max)
            elif self._key == "executor_cores":
                return validator.validate_executor_cores(value, self._min, self._max)
            elif self._key == "executor_memory":
                return validator.validate_executor_memory(value, self._min, self._max)
        except ValueError:
            raise
        raise ValueError(f"Unexpected argument {self._key}")
