import unittest

import mock
import pytest

from PiezoWebApp.src.models.validation_rule import ValidationRule
from PiezoWebApp.src.services.spark_job.validation.validation_service import ValidationService
from PiezoWebApp.src.services.spark_job.validation.validation_ruleset import ValidationRuleset


class TestValidationService(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def setup(self):
        self.mock_validation_ruleset = mock.create_autospec(ValidationRuleset)
        self.mock_validation_ruleset.get_validation_rule_for_key.return_value = None
        self.mock_validation_ruleset.get_keys_of_required_inputs.return_value = []
        self.mock_validation_ruleset.get_keys_of_optional_inputs.return_value = []
        self.mock_validation_ruleset.get_keys_for_language.return_value = []
        self.test_service = ValidationService(self.mock_validation_ruleset)

    # validate_request_keys

    def test_validate_request_keys_passes_for_empty_rules_and_empty_body(self):
        # Arrange
        request_body = {}
        # Act
        result = self.test_service.validate_request_keys(request_body)
        # Assert
        self.mock_validation_ruleset.get_keys_of_required_inputs.assert_called_once()
        self.mock_validation_ruleset.get_keys_for_language.assert_not_called()
        self.mock_validation_ruleset.get_keys_of_optional_inputs.assert_called_once()
        assert result.is_valid is True
        assert result.message == 'All input keys provided are valid\n'

    def test_validate_request_keys_passes_for_simple_rule_and_matching_body(self):
        # Arrange
        self.mock_validation_ruleset.get_keys_of_required_inputs.return_value = ['name']
        request_body = {'name': 'example-spark-job'}
        # Act
        result = self.test_service.validate_request_keys(request_body)
        # Assert
        self.mock_validation_ruleset.get_keys_of_required_inputs.assert_called_once()
        self.mock_validation_ruleset.get_keys_for_language.assert_not_called()
        self.mock_validation_ruleset.get_keys_of_optional_inputs.assert_called_once()
        assert result.is_valid is True
        assert result.message == 'All input keys provided are valid\n'

    def test_validate_request_keys_alerts_missing_simple_key(self):
        # Arrange
        self.mock_validation_ruleset.get_keys_of_required_inputs.return_value = ['name']
        request_body = {}
        # Act
        result = self.test_service.validate_request_keys(request_body)
        # Assert
        self.mock_validation_ruleset.get_keys_of_required_inputs.assert_called_once()
        self.mock_validation_ruleset.get_keys_for_language.assert_not_called()
        self.mock_validation_ruleset.get_keys_of_optional_inputs.assert_called_once()
        assert result.is_valid is False
        assert result.message == 'The following errors were found:\nMissing required input "name"\n'

    def test_validate_request_keys_confirms_presence_of_language_specific_input(self):
        # Arrange
        self.mock_validation_ruleset.get_keys_of_required_inputs.return_value = ['name', 'language']
        self.mock_validation_ruleset.get_keys_for_language.return_value = ['example_key']
        request_body = {
            'name': 'example-spark-job',
            'language': 'example-language',
            'example_key': 'example-value'
        }
        # Act
        result = self.test_service.validate_request_keys(request_body)
        # Assert
        self.mock_validation_ruleset.get_keys_of_required_inputs.assert_called_once()
        self.mock_validation_ruleset.get_keys_for_language.assert_called_once_with('example-language')
        self.mock_validation_ruleset.get_keys_of_optional_inputs.assert_called_once()
        assert result.is_valid is True
        assert result.message == 'All input keys provided are valid\n'

    def test_validate_request_keys_alerts_absence_of_language_specific_input(self):
        # Arrange
        self.mock_validation_ruleset.get_keys_of_required_inputs.return_value = ['name', 'language']
        self.mock_validation_ruleset.get_keys_for_language.return_value = ['example_key']
        request_body = {
            'name': 'example-spark-job',
            'language': 'example-language'
        }
        # Act
        result = self.test_service.validate_request_keys(request_body)
        # Assert
        self.mock_validation_ruleset.get_keys_of_required_inputs.assert_called_once()
        self.mock_validation_ruleset.get_keys_for_language.assert_called_once_with('example-language')
        assert result.is_valid is False
        assert result.message == 'The following errors were found:\nMissing required input "example_key"\n'

    # validate_request_values

    def test_validate_request_values_confirms_main_class_is_string(self):
        # Arrange
        self.mock_validation_ruleset.get_validation_rule_for_key.side_effect = lambda key: {
            'name': None,
            'language': ValidationRule({"classification": "Required", "options": ['example-language']}),
            'main_class': None
        }[key]
        request_body = {
            'name': 'example-spark-job',
            'language': 'example-language',
            'main_class': 'main.class'
        }
        # Act
        result = self.test_service.validate_request_values(request_body)
        # Assert
        assert result.is_valid is True
        assert result.message == 'All inputs provided are valid\n'
        self.assertDictEqual(result.validated_value, request_body)

    def test_validate_request_values_alerts_for_empty_main_class(self):
        # Arrange
        self.mock_validation_ruleset.get_validation_rule_for_key.side_effect = lambda key: {
            'name': None,
            'language': ValidationRule({"classification": "Required", "options": ['example-language']}),
            'main_class': None
        }[key]
        request_body = {
            'name': 'example-spark-job',
            'language': 'example-language',
            'main_class': ' '
        }
        # Act
        result = self.test_service.validate_request_values(request_body)
        # Assert
        assert result.is_valid is False
        assert result.message == 'The following errors were found:\n"main_class" input cannot be empty\n'
        assert result.validated_value is None
