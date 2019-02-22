from PiezoWebApp.src.models.spark_job_argument_classification import ArgumentClassification


class ValidationRuleset:
    def __init__(self, language_specific_keys, validation_rules):
        self._language_specific_keys = language_specific_keys
        self._validation_dict = validation_rules

    def get_validation_rule_for_key(self, key):
        return self._validation_dict[key]

    def get_keys_of_required_inputs(self):
        return [
            key for key in self._validation_dict
            if self._validation_dict[key].classification is ArgumentClassification.Required
        ]

    def get_keys_of_optional_inputs(self):
        return [
            key for key in self._validation_dict
            if self._validation_dict[key].classification is ArgumentClassification.Optional
        ]

    def get_default_value_for_key(self, key):
        validation_rule = self._validation_dict[key]
        return validation_rule.default

    def get_recognised_languages(self):
        return list(self._language_specific_keys.keys())

    def get_keys_for_language(self, language):
        if language in self._language_specific_keys:
            return self._language_specific_keys[language]
        return []
