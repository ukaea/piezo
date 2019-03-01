import json
import os

from PiezoWebApp.src.models.spark_job_argument_classification import ArgumentClassification
from PiezoWebApp.src.models.validation_rule_new import ValidationRule


class ValidationRuleset:
    def __init__(self, path_to_validation_rules_file):
        if not os.path.exists(path_to_validation_rules_file):
            raise RuntimeError(f'The validation rules file "{path_to_validation_rules_file}" does not seem to exist.')

        self._validation_dict = {}
        self._parse(path_to_validation_rules_file)

    def _parse(self, path):
        with open(path, 'rb') as f:
            raw_content = json.load(f)
        for rule_dict in raw_content:
            self._parse_rule(rule_dict)

    def _parse_rule(self, rule_dict):
        input_name = rule_dict['input_name']
        validation_rule = ValidationRule(rule_dict)
        self._validation_dict[input_name] = validation_rule

    def get_validation_rule_for_key(self, input_name):
        return self._validation_dict[input_name]

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

    def get_keys_for_language(self, language):
        if language in self._language_specific_keys:
            return self._language_specific_keys[language]
        return []
