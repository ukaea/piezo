class ValidationResult:
    def __init__(self, is_valid, message, validated_value):
        self._is_valid = is_valid
        self._message = message
        self._validated_value = validated_value

    @property
    def is_valid(self):
        return self._is_valid

    @property
    def message(self):
        return self._message

    @property
    def validated_value(self):
        return self._validated_value
