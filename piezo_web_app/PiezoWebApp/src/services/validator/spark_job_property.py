from PiezoWebApp.src.services.validator.validation_rules import ValidationRules
from PiezoWebApp.src.utils.str_helper import is_str_empty


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
        # Validate numerical args
        if self.required_format in ["int", "float"]:
            if self.required_format == "int":
                formatted_value = int(value)
            else:
                formatted_value = round(float(value), 1)
            is_valid = self.min <= formatted_value <= self.max
            if is_valid is False:
                raise ValueError(f"Argument {self._key} must be between {self.min} and {self.max}")
            return formatted_value

        # Validate string args
        elif self.required_format == "string":
            formatted_value = str(value)
            if is_str_empty(formatted_value):
                raise ValueError(f"Argument {self._key} can't be empty")

            # Python version specific validation
            if self._key == "python_version":
                if value in ["2", "3"] is False:
                    raise ValueError("Python version must be either '2' or '3'")
            return formatted_value
