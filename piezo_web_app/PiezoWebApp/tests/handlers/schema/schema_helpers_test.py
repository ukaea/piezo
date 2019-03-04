import pytest

from PiezoWebApp.src.models.validation_rule import ValidationRule
from PiezoWebApp.src.handlers.schema.schema_helpers import create_object_schema_from_validation_rules
from PiezoWebApp.src.handlers.schema.schema_helpers import create_object_schema_with_string_properties


def test_create_object_schema_from_validation_rules_returns_schema_with_all_optional_properties_with_none_required():
    # Arrange
    rules_dict = {
        'a': ValidationRule({'classification': 'Optional'}),
        'b': ValidationRule({'classification': 'Optional'}),
        'c': ValidationRule({'classification': 'Optional'})
    }
    # Act
    schema = create_object_schema_from_validation_rules(rules_dict)
    # Assert
    assert schema == {
        'type': 'object',
        'properties': {
            'a': {'type': 'string'},
            'b': {'type': 'string'},
            'c': {'type': 'string'}
        }
    }


def test_create_object_schema_from_validation_rules_returns_schema_with_all_conditional_properties_with_none_required():
    # Arrange
    rules_dict = {
        'a': ValidationRule({'classification': 'Conditional'}),
        'b': ValidationRule({'classification': 'Conditional'}),
        'c': ValidationRule({'classification': 'Conditional'})
    }
    # Act
    schema = create_object_schema_from_validation_rules(rules_dict)
    # Assert
    assert schema == {
        'type': 'object',
        'properties': {
            'a': {'type': 'string'},
            'b': {'type': 'string'},
            'c': {'type': 'string'}
        }
    }


def test_create_object_schema_from_validation_rules_returns_schema_with_all_required_properties_with_all_required():
    # Arrange
    rules_dict = {
        'a': ValidationRule({'classification': 'Required'}),
        'b': ValidationRule({'classification': 'Required'}),
        'c': ValidationRule({'classification': 'Required'})
    }
    # Act
    schema = create_object_schema_from_validation_rules(rules_dict)
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


def test_create_object_schema_from_validation_rules_raises_value_error_with_all_fixed():
    # Arrange
    rules_dict = {
        'a': ValidationRule({'classification': 'Fixed'}),
        'b': ValidationRule({'classification': 'Fixed'}),
        'c': ValidationRule({'classification': 'Fixed'})
    }
    # Act & Assert
    with pytest.raises(ValueError, match='No properties provided for the schema'):
        create_object_schema_from_validation_rules(rules_dict)


def test_create_object_schema_from_validation_rules_raises_value_error_with_empty_dictionary():
    # Arrange
    rules_dict = {}
    # Act & Assert
    with pytest.raises(ValueError, match='No properties provided for the schema'):
        create_object_schema_from_validation_rules(rules_dict)


def test_create_object_schema_from_validation_rules_returns_expected_schema_with_mixed_rules():
    # Arrange
    rules_dict = {
        'fixed': ValidationRule({'classification': 'Fixed'}),
        'required': ValidationRule({'classification': 'Required'}),
        'optional': ValidationRule({'classification': 'Optional'}),
        'conditional': ValidationRule({'classification': 'Conditional'})
    }
    # Act
    schema = create_object_schema_from_validation_rules(rules_dict)
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
