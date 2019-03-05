import json
import os

from PiezoWebApp.src.models.validation_rule import ValidationRule


class ValidationRulesetParser:
    def __init__(self):
        self._validation_dict = {}

    def _parse(self, path):
        with open(path, 'rb') as rules_file:
            raw_content = json.load(rules_file)
        for rule_dict in raw_content:
            self._parse_rule(rule_dict)

    def _parse_rule(self, rule_dict):
        input_name = rule_dict['input_name']
        validation_rule = ValidationRule(rule_dict)
        self._validation_dict[input_name] = validation_rule

    def parse(self, path_to_validation_rules_file):
        if not os.path.exists(path_to_validation_rules_file):
            raise RuntimeError(f'The validation rules file "{path_to_validation_rules_file}" does not seem to exist.')

        self._parse(path_to_validation_rules_file)

        return self._validation_dict
