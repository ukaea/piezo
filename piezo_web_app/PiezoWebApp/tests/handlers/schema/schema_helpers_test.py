import mock
import pytest

from PiezoWebApp.src.handlers.schema.schema_helpers import create_object_schema_from_validation_ruleset
from PiezoWebApp.src.handlers.schema.schema_helpers import create_object_schema_with_string_properties
from PiezoWebApp.src.services.spark_job.validation.validation_ruleset import ValidationRuleset


def test_create_object_schema_from_validation_ruleset_returns_schema_with_none_required():
    # Arrange
    ruleset = mock.create_autospec(ValidationRuleset)
    ruleset.get_key_type_pairs_allowed_as_input.return_value = {
        'a': 'string',
        'b': 'string',
        'c': 'string'
    }
    ruleset.get_keys_of_required_inputs.return_value = []
    # Act
    schema = create_object_schema_from_validation_ruleset(ruleset)
    # Assert
    assert schema == {
        'type': 'object',
        'properties': {
            'a': {'type': 'string'},
            'b': {'type': 'string'},
            'c': {'type': 'string'}
        }
    }


def test_create_object_schema_from_validation_ruleset_returns_schema_with_all_required():
    # Arrange
    ruleset = mock.create_autospec(ValidationRuleset)
    ruleset.get_key_type_pairs_allowed_as_input.return_value = {
        'a': 'string',
        'b': 'string',
        'c': 'string'
    }
    ruleset.get_keys_of_required_inputs.return_value = ['a', 'b', 'c']
    # Act
    schema = create_object_schema_from_validation_ruleset(ruleset)
    # Assert
    assert schema == {
        'type': 'object',
        'properties': {
            'a': {'type': 'string'},
            'b': {'type': 'string'},
            'c': {'type': 'string'}
        },
        'required': ['a', 'b', 'c']
    }


def test_create_object_schema_from_validation_ruleset_returns_expected_schema_with_mixed_rules():
    # Arrange
    ruleset = mock.create_autospec(ValidationRuleset)
    ruleset.get_key_type_pairs_allowed_as_input.return_value = {
        'required': 'string',
        'optional': 'string',
        'conditional': 'string'
    }
    ruleset.get_keys_of_required_inputs.return_value = ['required']
    # Act
    schema = create_object_schema_from_validation_ruleset(ruleset)
    # Assert
    assert schema == {
        'type': 'object',
        'properties': {
            'required': {'type': 'string'},
            'optional': {'type': 'string'},
            'conditional': {'type': 'string'}
        },
        'required': ['required']
    }


def test_create_object_schema_with_string_properties_returns_schema_with_all_properties_with_none_required():
    # Arrange
    properties = ['a', 'b', 'c']
    # Act
    schema = create_object_schema_with_string_properties(properties)
    # Assert
    assert schema == {
        'type': 'object',
        'properties': {
            'a': {'type': 'string'},
            'b': {'type': 'string'},
            'c': {'type': 'string'}
        },
    }


def test_create_object_schema_with_string_properties_returns_schema_with_all_properties_with_correct_required():
    # Arrange
    properties = ['a', 'b', 'c']
    required = ['b', 'c']
    # Act
    schema = create_object_schema_with_string_properties(properties, required)
    # Assert
    assert schema == {
        'type': 'object',
        'properties': {
            'a': {'type': 'string'},
            'b': {'type': 'string'},
            'c': {'type': 'string'}
        },
        'required': ['b', 'c']
    }


def test_create_object_schema_creates_blank_properties_section_when_none_given():
    # Arrange
    properties = []
    # Assert
    with pytest.raises(ValueError, match='No properties provided for the schema'):
        create_object_schema_with_string_properties(properties)
