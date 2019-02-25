import pytest

from PiezoWebApp.src.models.validation_rule import ValidationRule
from PiezoWebApp.src.handlers.schema.schema_helpers import create_object_schema_from_validation_rules
from PiezoWebApp.src.handlers.schema.schema_helpers import create_object_schema_with_string_properties
from PiezoWebApp.src.models.spark_job_argument_classification import ArgumentClassification


def test_create_object_schema_from_validation_rules_returns_schema_with_all_optional_properties_with_none_required():
    # Arrange
    rules_dict = {
        'a': ValidationRule(ArgumentClassification.Optional, None),
        'b': ValidationRule(ArgumentClassification.Optional, None),
        'c': ValidationRule(ArgumentClassification.Optional, None)
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
        'a': ValidationRule(ArgumentClassification.Conditional, None),
        'b': ValidationRule(ArgumentClassification.Conditional, None),
        'c': ValidationRule(ArgumentClassification.Conditional, None)
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
        'a': ValidationRule(ArgumentClassification.Required, None),
        'b': ValidationRule(ArgumentClassification.Required, None),
        'c': ValidationRule(ArgumentClassification.Required, None)
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
        'a': ValidationRule(ArgumentClassification.Fixed, None),
        'b': ValidationRule(ArgumentClassification.Fixed, None),
        'c': ValidationRule(ArgumentClassification.Fixed, None)
    }
    # Act & Assert
    with pytest.raises(ValueError, message='No properties provided for the schema'):
        create_object_schema_from_validation_rules(rules_dict)


def test_create_object_schema_from_validation_rules_raises_value_error_with_empty_dictionary():
    # Arrange
    rules_dict = {}
    # Act & Assert
    with pytest.raises(ValueError, message='No properties provided for the schema'):
        create_object_schema_from_validation_rules(rules_dict)


def test_create_object_schema_from_validation_rules_returns_expected_schema_with_mixed_rules():
    # Arrange
    rules_dict = {
        'fixed': ValidationRule(ArgumentClassification.Fixed, None),
        'required': ValidationRule(ArgumentClassification.Required, None),
        'optional': ValidationRule(ArgumentClassification.Optional, None),
        'conditional': ValidationRule(ArgumentClassification.Conditional, None)
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
    with pytest.raises(ValueError, message='No properties provided for the schema'):
        create_object_schema_with_string_properties(properties)
