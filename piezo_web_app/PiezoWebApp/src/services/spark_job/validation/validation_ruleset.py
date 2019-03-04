from PiezoWebApp.src.models.spark_job_argument_classification import ArgumentClassification


class ValidationRuleset:
    def __init__(self, validation_dict):
        self._validation_dict = validation_dict

    def get_default_value_for_key(self, key):
        validation_rule = self._validation_dict[key]
        return validation_rule.default

    def get_key_type_pairs_allowed_as_input(self):
        # TODO variable type other than string
        return {key: 'string' for key in self._validation_dict.keys()}

    def get_keys_for_language(self, language):
        return [
            input_name
            for input_name, rule in self._validation_dict.items()
            if rule.conditional_input_name == 'language' and rule.conditional_input_value == language
        ]

    def get_keys_of_optional_inputs(self):
        return [
            input_name
            for input_name, rule in self._validation_dict.items()
            if rule.classification is ArgumentClassification.Optional
        ]

    def get_keys_of_required_inputs(self):
        return [
            input_name
            for input_name, rule in self._validation_dict.items()
            if rule.classification is ArgumentClassification.Required
        ]

    def get_validation_rule_for_key(self, input_name):
        return self._validation_dict[input_name]
