from PiezoWebApp.src.services.validator.validation_rules import ValidationRules


class SparkJobProperty:

    def __init__(self, key):
        self._key = key
        self._min = None
        self._max = None
        self._default = None
        self._format = None
        self._validation_rules = ValidationRules()
        self._parse(key)

    def _parse(self, key):
        validation_properties = self._validation_rules.get_keys_property_array(key)
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

    def validate(self, value):

        if self.format in ["int", "float"]:
            is_valid = self.min <= value <= self.max
            if is_valid is False:
                raise ValueError(f"Argument {self._key} must be between {self.min} and {self.max}")



