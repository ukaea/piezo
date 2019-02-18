class ValidationResult:

    def __init__(self, is_valid, message, validated_value):
        self.is_valid = is_valid
        self.message = message
        self.validated_value = validated_value
