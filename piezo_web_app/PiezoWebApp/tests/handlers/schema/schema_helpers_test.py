import pytest

from PiezoWebApp.src.handlers.schema.schema_helpers import create_object_schema_from_validation_rules
from PiezoWebApp.src.handlers.schema.schema_helpers import create_object_schema_with_string_properties
from PiezoWebApp.src.models.spark_job_argument_classification import ArgumentClassification


def test_create_object_schema_from_validation_rules_returns_schema_with_all_optional_properties_with_none_required():
    # Arrange
    rules_dict = {
        'a': ArgumentClassification.Optional,
        'b': ArgumentClassification.Optional,
        'c': ArgumentClassification.Optional
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
        'a': ArgumentClassification.Conditional,
        'b': ArgumentClassification.Conditional,
        'c': ArgumentClassification.Conditional
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
        'a': ArgumentClassification.Required,
        'b': ArgumentClassification.Required,
        'c': ArgumentClassification.Required
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
        'a': ArgumentClassification.Fixed,
        'b': ArgumentClassification.Fixed,
        'c': ArgumentClassification.Fixed
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
        'fixed': ArgumentClassification.Fixed,
        'required': ArgumentClassification.Required,
        'optional': ArgumentClassification.Optional,
        'conditional': ArgumentClassification.Conditional
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
