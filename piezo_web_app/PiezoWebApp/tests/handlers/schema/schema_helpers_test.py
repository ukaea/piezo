import pytest

from PiezoWebApp.src.handlers.schema.schema_helpers import create_object_schema_from_validation_rules
from PiezoWebApp.src.handlers.schema.schema_helpers import create_object_schema_with_string_properties
from PiezoWebApp.src.models.spark_job_argument_classification import ArgumentClassification


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
