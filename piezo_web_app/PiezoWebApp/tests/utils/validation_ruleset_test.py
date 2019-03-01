import json
import os
import tempfile

import pytest

from PiezoWebApp.src.models.spark_job_argument_classification import ArgumentClassification
from PiezoWebApp.src.utils.validation_ruleset import ValidationRuleset


class SampleValidationRulesCreator:
    @staticmethod
    def create_rules(rule_dicts):
        temp = tempfile.NamedTemporaryFile(mode='w+', delete=False)
        json.dump(rule_dicts, temp, indent=2)
        path = temp.name
        temp.close()
        return path

    @staticmethod
    def remove_file(file_path):
        if os.path.exists(file_path):
            os.remove(file_path)


def test_validation_rules_raises_when_path_is_not_correct():
    with pytest.raises(RuntimeError) as exception_info:
        path = "dummy_path"
        ValidationRuleset(path)
    assert('The validation rules file "dummy_path" does not seem to exist.' in str(exception_info.value))


def test_validation_rules_parses_with_arguments():
    # Arrange
    rules_path = SampleValidationRulesCreator.create_rules([
        {
            'input_name': 'fixed',
            'classification': 'Fixed',
            'default': 'fixed_value'
        },
        {
            'input_name': 'required_no_default',
            'classification': 'Required'
        },
        {
            'input_name': 'optional_with_range',
            'classification': 'Optional',
            'minimum': 1,
            'maximum': 10
        },
        {
            'input_name': 'conditional_with_options',
            'classification': 'Conditional',
            'options': ['option1', 'option2']
        }
    ])
    # Act
    rules = ValidationRuleset(rules_path)
    # Assert
    fixed = rules.get_validation_rule_for_key('fixed')
    assert fixed.classification is ArgumentClassification.Fixed
    assert fixed.default == 'fixed_value'
    required_no_default = rules.get_validation_rule_for_key('required_no_default')
    assert required_no_default.classification is ArgumentClassification.Required
    assert required_no_default.default is None
    optional_with_range = rules.get_validation_rule_for_key('optional_with_range')
    assert optional_with_range.classification is ArgumentClassification.Optional
    assert optional_with_range.minimum is 1
    assert optional_with_range.maximum is 10
    conditional_with_options = rules.get_validation_rule_for_key('conditional_with_options')
    assert conditional_with_options.classification is ArgumentClassification.Conditional
    assert conditional_with_options.options == ['option1', 'option2']
    # Clean up
    SampleValidationRulesCreator.remove_file(rules_path)


