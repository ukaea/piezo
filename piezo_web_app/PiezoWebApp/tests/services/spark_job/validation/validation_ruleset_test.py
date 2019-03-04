import unittest

import pytest

from PiezoWebApp.src.models.validation_rule import ValidationRule
from PiezoWebApp.src.services.spark_job.validation.validation_ruleset import ValidationRuleset


class TestValidationRuleSet(unittest.TestCase):
    def test_get_default_value_for_key_raises_key_error_when_rule_not_defined(self):
        # Arrange
        validation_dict = {
            'x': ValidationRule({'classification': 'Required', 'default': '7'}),
            'y': ValidationRule({'classification': 'Optional', 'default': 'banana'})
        }
        test_ruleset = ValidationRuleset(validation_dict)
        # Act & Assert
        with pytest.raises(KeyError):
            test_ruleset.get_default_value_for_key('z')

    def test_get_default_value_for_key_returns_none_when_default_not_defined(self):
        # Arrange
        validation_dict = {
            'x': ValidationRule({'classification': 'Required'}),
            'y': ValidationRule({'classification': 'Optional', 'default': 'banana'})
        }
        test_ruleset = ValidationRuleset(validation_dict)
        # Act
        result = test_ruleset.get_default_value_for_key('x')
        # Assert
        assert result is None

    def test_get_default_value_for_key_returns_value_when_defined(self):
        # Arrange
        validation_dict = {
            'x': ValidationRule({'classification': 'Required', 'default': '7'}),
            'y': ValidationRule({'classification': 'Optional'})
        }
        test_ruleset = ValidationRuleset(validation_dict)
        # Act
        result = test_ruleset.get_default_value_for_key('x')
        # Assert
        assert result == '7'

    def test_get_keys_for_language_returns_single_conditional(self):
        # Arrange
        validation_dict = {
            'x': ValidationRule({
                'classification': 'Conditional',
                'conditional_input_name': 'language',
                'conditional_input_value': 'Test'
            })
        }
        test_ruleset = ValidationRuleset(validation_dict)
        # Act
        result = test_ruleset.get_keys_for_language('Test')
        # Assert
        assert result == ['x']

    def test_get_keys_for_language_returns_only_conditional_that_matches(self):
        # Arrange
        validation_dict = {
            'x': ValidationRule({
                'classification': 'Conditional',
                'conditional_input_name': 'language',
                'conditional_input_value': 'Other'
            }),
            'y': ValidationRule({
                'classification': 'Conditional',
                'conditional_input_name': 'language',
                'conditional_input_value': 'Test'
            }),
            'z': ValidationRule({'classification': 'Required', 'default': '7'})
        }
        test_ruleset = ValidationRuleset(validation_dict)
        # Act
        result = test_ruleset.get_keys_for_language('Test')
        # Assert
        assert result == ['y']

    def test_get_keys_for_language_returns_empty_list_when_none_match(self):
        # Arrange
        validation_dict = {
            'x': ValidationRule({
                'classification': 'Conditional',
                'conditional_input_name': 'language',
                'conditional_input_value': 'Other'
            }),
            'z': ValidationRule({'classification': 'Required', 'default': '7'})
        }
        test_ruleset = ValidationRuleset(validation_dict)
        # Act
        result = test_ruleset.get_keys_for_language('Test')
        # Assert
        assert result == []

    def test_get_keys_of_optional_inputs_returns_empty_list_when_none_optional(self):
        # Arrange
        validation_dict = {
            'x': ValidationRule({
                'classification': 'Conditional',
                'conditional_input_name': 'language',
                'conditional_input_value': 'Other'
            }),
            'y': ValidationRule({'classification': 'Fixed', 'default': 'banana'}),
            'z': ValidationRule({'classification': 'Required', 'default': '7'})
        }
        test_ruleset = ValidationRuleset(validation_dict)
        # Act
        result = test_ruleset.get_keys_of_optional_inputs()
        # Assert
        assert result == []

    def test_get_keys_of_optional_inputs_returns_single_optional_rule(self):
        # Arrange
        validation_dict = {
            'x': ValidationRule({'classification': 'Optional', 'default': '7'})
        }
        test_ruleset = ValidationRuleset(validation_dict)
        # Act
        result = test_ruleset.get_keys_of_optional_inputs()
        # Assert
        assert result == ['x']

    def test_get_keys_of_optional_inputs_returns_optional_names_from_mixture(self):
        # Arrange
        validation_dict = {
            'w': ValidationRule({
                'classification': 'Conditional',
                'conditional_input_name': 'language',
                'conditional_input_value': 'Other'
            }),
            'x': ValidationRule({'classification': 'Fixed', 'default': 'banana'}),
            'y': ValidationRule({'classification': 'Required', 'default': '7'}),
            'z': ValidationRule({'classification': 'Optional', 'default': '1.2.3'})
        }
        test_ruleset = ValidationRuleset(validation_dict)
        # Act
        result = test_ruleset.get_keys_of_optional_inputs()
        # Assert
        assert result == ['z']

    def test_get_keys_of_required_inputs_returns_empty_list_when_none_optional(self):
        # Arrange
        validation_dict = {
            'x': ValidationRule({
                'classification': 'Conditional',
                'conditional_input_name': 'language',
                'conditional_input_value': 'Other'
            }),
            'y': ValidationRule({'classification': 'Fixed', 'default': 'banana'}),
            'z': ValidationRule({'classification': 'Optional', 'default': '7'})
        }
        test_ruleset = ValidationRuleset(validation_dict)
        # Act
        result = test_ruleset.get_keys_of_required_inputs()
        # Assert
        assert result == []

    def test_get_keys_of_required_inputs_returns_single_required_rule(self):
        # Arrange
        validation_dict = {
            'x': ValidationRule({'classification': 'Required', 'default': '7'})
        }
        test_ruleset = ValidationRuleset(validation_dict)
        # Act
        result = test_ruleset.get_keys_of_required_inputs()
        # Assert
        assert result == ['x']

    def test_get_keys_of_required_inputs_returns_required_names_from_mixture(self):
        # Arrange
        validation_dict = {
            'w': ValidationRule({
                'classification': 'Conditional',
                'conditional_input_name': 'language',
                'conditional_input_value': 'Other'
            }),
            'x': ValidationRule({'classification': 'Fixed', 'default': 'banana'}),
            'y': ValidationRule({'classification': 'Required', 'default': '7'}),
            'z': ValidationRule({'classification': 'Optional', 'default': '1.2.3'})
        }
        test_ruleset = ValidationRuleset(validation_dict)
        # Act
        result = test_ruleset.get_keys_of_required_inputs()
        # Assert
        assert result == ['y']

    def test_get_validation_rule_for_key_raises_key_error_when_rule_not_defined(self):
        # Arrange
        validation_dict = {
            'x': ValidationRule({'classification': 'Required', 'default': '7'}),
            'y': ValidationRule({'classification': 'Optional', 'default': 'banana'})
        }
        test_ruleset = ValidationRuleset(validation_dict)
        # Act & Assert
        with pytest.raises(KeyError):
            test_ruleset.get_validation_rule_for_key('z')

    def test_get_validation_rule_for_key_returns_value_when_defined(self):
        # Arrange
        validation_dict = {
            'x': ValidationRule({'classification': 'Required', 'default': '7'}),
            'y': ValidationRule({'classification': 'Optional'})
        }
        test_ruleset = ValidationRuleset(validation_dict)
        # Act
        result = test_ruleset.get_validation_rule_for_key('x')
        # Assert
        assert result is validation_dict['x']
