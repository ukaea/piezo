import mock
import pytest

from PiezoWebApp.src.handlers.schema.schema_helpers import create_object_schema_from_validation_ruleset
from PiezoWebApp.src.handlers.schema.schema_helpers import create_object_schema_with_string_properties
from PiezoWebApp.src.services.spark_job.validation.validation_ruleset import ValidationRuleset


def test_create_object_schema_from_validation_ruleset_returns_correct_schema():
    # Arrange
    ruleset = mock.create_autospec(ValidationRuleset)
    ruleset.get_key_type_pairs_allowed_as_input.return_value = {
        'a': 'string',
        'b': 'string',
        'c': 'string'
    }
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


def test_create_object_schema_from_validation_ruleset_returns_expected_schema_with_mixed_rules_and_mixed_types():
    # Arrange
    ruleset = mock.create_autospec(ValidationRuleset)
    ruleset.get_key_type_pairs_allowed_as_input.return_value = {
        'required': 'string',
        'optional': 'string',
        'optional2': 'array',
        'conditional': 'string'
    }
    # Act
    schema = create_object_schema_from_validation_ruleset(ruleset)
    # Assert
    assert schema == {
        'type': 'object',
        'properties': {
            'required': {'type': 'string'},
            'optional': {'type': 'string'},
            'optional2': {'type': 'array'},
            'conditional': {'type': 'string'}
        },
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


def test_create_object_schema_creates_blank_properties_section_when_none_given():
    # Arrange
    properties = []
    # Assert
    with pytest.raises(ValueError, match='No properties provided for the schema'):
        create_object_schema_with_string_properties(properties)
