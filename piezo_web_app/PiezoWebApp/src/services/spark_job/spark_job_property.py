from PiezoWebApp.src.services.spark_job.validation import argument_validator


class SparkJobProperty:

    def __init__(self, key, validation_rules):
        self._key = key
        self._min = None
        self._max = None
        self._default = None
        self._format = None
        self._validation_rules = validation_rules
        self._parse(key)

    def _parse(self, key):
        validation_properties = self._validation_rules.get_property_array_for_key(key)
        self._min = validation_properties[0]
        self._max = validation_properties[1]
        self._default = validation_properties[2]
        self._format = validation_properties[3]

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
    def format(self):
        return self._format

    @format.setter
    def format(self, new_format):
        if new_format in ["base", "required", "optional"]:
            self._format = new_format

    def validate(self, value):
        if self._key == "name":
            return argument_validator.validate_name(value)
        if self._key == "language":
            return argument_validator.validate_language(value)
        if self._key == "python_version":
            return argument_validator.validate_python_version(value)
        if self._key == "path_to_main_app_file":
            return argument_validator.validate_path_to_main_app_file(value)
        if self._key == "main_class":
            return argument_validator.validate_main_class(value)
        if self._key == "driver_cores":
            return argument_validator.validate_driver_cores(value, self._min, self._max)
        if self._key == "driver_core_limit":
            return argument_validator.validate_driver_core_limit(value, self._min, self._max)
        if self._key == "driver_memory":
            return argument_validator.validate_driver_memory(value, self._min, self._max)
        if self._key == "executors":
            return argument_validator.validate_executors(value, self._min, self._max)
        if self._key == "executor_cores":
            return argument_validator.validate_executor_cores(value, self._min, self._max)
        if self._key == "executor_memory":
            return argument_validator.validate_executor_memory(value, self._min, self._max)
        raise ValueError(f"Unexpected argument {self._key}")
