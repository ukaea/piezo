import pytest

from PiezoWebApp.src.models.validation_rule import ValidationRule
from PiezoWebApp.src.services.spark_job.validation import argument_validator


@pytest.mark.parametrize("name", ["test", "acb123", "abc.123", "abc-123", "ab-c1.23", "a"])
def test_validate_name_validates_well_formatted_strings(name):
    # Arrange
    validation_rule = ValidationRule({'classification': 'Required'})
    # Act
    validation_result = argument_validator.validate("name", name, validation_rule)
    # Assert
    assert validation_result.is_valid is True


@pytest.mark.parametrize("name", ["", "   "])
def test_validate_name_rejects_empty_strings(name):
    # Arrange
    validation_rule = ValidationRule({'classification': 'Required'})
    # Act
    validation_result = argument_validator.validate("name", name, validation_rule)
    # Assert
    assert validation_result.is_valid is False
    assert validation_result.message == '"name" input cannot be empty'


@pytest.mark.parametrize("name", [123, 3.4])
def test_validate_name_rejects_non_string_values(name):
    # Arrange
    validation_rule = ValidationRule({'classification': 'Required'})
    # Act
    validation_result = argument_validator.validate("name", name, validation_rule)
    # Assert
    assert validation_result.is_valid is False
    assert validation_result.message == '"name" input must be a string'


@pytest.mark.parametrize("name", [
    ".abc123",
    "-abc123",
    "abc123.",
    "abc123-",
    "abc..123",
    "abc.-123",
    "abc-.123",
    "abc--123",
    "abc_123",
    "Abc123",
    "123abc",
    "some_long_name!!!@13234"
])
def test_validate_name_rejects_poorly_formatted_strings(name):
    # Arrange
    validation_rule = ValidationRule({'classification': 'Required'})
    # Act
    validation_result = argument_validator.validate("name", name, validation_rule)
    # Assert
    assert validation_result.is_valid is False
    assert validation_result.message == '"name" input must obey naming convention: '\
                                        'see https://github.com/ukaea/piezo/wiki/WebAppUserGuide#submit-a-job'


def test_validate_name_allows_29_character_name():
    # Arrange
    validation_rule = ValidationRule({'classification': 'Required'})
    name = 'abcdefghijklmnopqrstuvwxyzabc'
    assert len(name) == 29
    # Act
    validation_result = argument_validator.validate("name", name, validation_rule)
    # Assert
    assert validation_result.is_valid is True


def test_validate_name_rejects_30_character_name():
    # Arrange
    validation_rule = ValidationRule({'classification': 'Required'})
    name = 'abcdefghijklmnopqrstuvwxyzabc' + 'd'
    assert len(name) == 30
    # Act
    validation_result = argument_validator.validate("name", name, validation_rule)
    # Assert
    assert validation_result.is_valid is False
    assert validation_result.message == '"name" input must obey naming convention: ' \
                                        'see https://github.com/ukaea/piezo/wiki/WebAppUserGuide#submit-a-job'


@pytest.mark.parametrize("label", ["", "   "])
def test_validate_label_rejects_empty_strings(label):
    # Arrange
    validation_rule = ValidationRule({'classification': 'Required'})
    # Act
    validation_result = argument_validator.validate("label", label, validation_rule)
    # Assert
    assert validation_result.is_valid is False
    assert validation_result.message == '"label" input cannot be empty'


@pytest.mark.parametrize("label", ["A", "a", "label", "LABEL", "LaBeL", "L-a-B-e-L", "lab-----el", "12345"])
def test_validate_label_accepts_valid_labels(label):
    # Arrange
    validation_rule = ValidationRule({'classification': 'Required'})
    # Act
    validation_result = argument_validator.validate("label", label, validation_rule)
    assert validation_result.is_valid is True


def test_validate_label_validates_label_with_63_characters():
    # Arrange
    validation_rule = ValidationRule({'classification': 'Required'})
    label = "abcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklm"
    assert len(label) == 63
    # Act
    validation_result = argument_validator.validate("label", label, validation_rule)
    assert validation_result.is_valid is True


def test_validate_label_rejects_label_with_64_characters():
    # Arrange
    validation_rule = ValidationRule({'classification': 'Required'})
    label = "abcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklm" + "n"
    assert len(label) == 64
    # Act
    validation_result = argument_validator.validate("label", label, validation_rule)
    assert validation_result.is_valid is False
    assert validation_result.message == '"label" input has a maximum length of 63 characters'


@pytest.mark.parametrize("label", ["A-", "-a", "$label", "LA.BEL", "-", "lab/el"])
def test_validate_label_rejects_invalid_non_empty_labels(label):
    # Arrange
    validation_rule = ValidationRule({'classification': 'Required'})
    # Act
    validation_result = argument_validator.validate("label", label, validation_rule)
    assert validation_result.is_valid is False
    assert validation_result.message == '"label" input must obey naming convention: ' \
                                        'see https://github.com/ukaea/piezo/wiki/WebAppUserGuide#submit-a-job'


@pytest.mark.parametrize("language", ["Python", "Scala"])
def test_validate_language_validates_valid_languages(language):
    # Arrange
    validation_rule = ValidationRule({'classification': 'Required', 'options': ['Python', 'Scala']})
    # Act
    validation_result = argument_validator.validate("language", language, validation_rule)
    # Assert
    assert validation_result.is_valid is True


@pytest.mark.parametrize("language", ["python", "PYTHON", "PythON", "SCALA", "ScALa", "R", 123, "", "  "])
def test_validate_language_rejects_non_valid_languages(language):
    # Arrange
    validation_rule = ValidationRule({'classification': 'Required', 'options': ['Python', 'Scala']})
    # Act
    validation_result = argument_validator.validate("language", language, validation_rule)
    # Assert
    assert validation_result.is_valid is False


@pytest.mark.parametrize("version", ["2", "3"])
def test_validate_python_version_validates_string_2_or_3(version):
    # Arrange
    validation_rule = ValidationRule({
        'classification': 'Conditional',
        'options': ['2', '3'],
        'conditional_input_name': 'language',
        'conditional_input_value': 'Python'
    })
    # Act
    validation_result = argument_validator.validate("python_version", version, validation_rule)
    # Assert
    assert validation_result.is_valid is True


@pytest.mark.parametrize("version", [2.0, 2, 3, 3.7, None])
def test_validate_python_version_rejects_non_string(version):
    # Arrange
    validation_rule = ValidationRule({
        'classification': 'Conditional',
        'options': ['2', '3'],
        'conditional_input_name': 'language',
        'conditional_input_value': 'Python'
    })
    # Act
    validation_result = argument_validator.validate("python_version", version, validation_rule)
    # Assert
    assert validation_result.is_valid is False
    assert validation_result.message == '"python_version" input must be a string'


@pytest.mark.parametrize("version", ["1", "4", " ", "", "2.0", "3.6"])
def test_validate_python_version_rejects_string_not_in_list(version):
    # Arrange
    validation_rule = ValidationRule({
        'classification': 'Conditional',
        'options': ['2', '3'],
        'conditional_input_name': 'language',
        'conditional_input_value': 'Python'
    })
    # Act
    validation_result = argument_validator.validate("python_version", version, validation_rule)
    # Assert
    assert validation_result.is_valid is False
    assert validation_result.message == '"python_version" input must be one of: "2", "3"'


@pytest.mark.parametrize("path", ["/path/to/file", r"\path\to\file"])
def test_validate_path_to_main_app_file_validates_non_empty_strings(path):
    # Arrange
    validation_rule = ValidationRule({'classification': 'Required'})
    # Act
    validation_result = argument_validator.validate("path_to_main_app_file", path, validation_rule)
    # Assert
    assert validation_result.is_valid is True


@pytest.mark.parametrize("path", [" ", "", 123323])
def test_validate_path_to_main_app_file_rejects_empty_strings_and_non_strings(path):
    # Arrange
    validation_rule = ValidationRule({'classification': 'Required'})
    # Act
    validation_result = argument_validator.validate("path_to_main_app_file", path, validation_rule)
    # Assert
    assert validation_result.is_valid is False


@pytest.mark.parametrize("main_class", ["someClass", "12321"])
def test_validate_main_class_validates_non_empty_strings(main_class):
    # Arrange
    validation_rule = ValidationRule({'classification': 'Required'})
    # Act
    validation_result = argument_validator.validate("main_class", main_class, validation_rule)
    # Assert
    assert validation_result.is_valid is True


@pytest.mark.parametrize("main_class", [" ", "", 123323, None])
def test_validate_main_class_rejects_empty_strings_and_non_strings(main_class):
    # Arrange
    validation_rule = ValidationRule({'classification': 'Required'})
    # Act
    validation_result = argument_validator.validate("main_class", main_class, validation_rule)
    # Assert
    assert validation_result.is_valid is False


@pytest.mark.parametrize("cores", ["0.1", "0.5", "1", "1.0"])
def test_validate_driver_cores_accepts_values_within_valid_range(cores):
    # Arrange
    validation_rule = ValidationRule({
        'classification': 'Optional',
        'default': 0.1,
        'minimum': 0.1,
        'maximum': 1
    })
    # Act
    validation_result = argument_validator.validate("driver_cores", cores, validation_rule)
    # Assert
    assert validation_result.is_valid is True


@pytest.mark.parametrize("cores", [" ", "", None, "100m", "200mn", "12e13m"])
def test_validate_driver_cores_rejects_empty_strings_and_non_numbers(cores):
    # Arrange
    validation_rule = ValidationRule({
        'classification': 'Optional',
        'default': 0.1,
        'minimum': 0.1,
        'maximum': 1
    })
    # Act
    validation_result = argument_validator.validate("driver_cores", cores, validation_rule)
    # Assert
    assert validation_result.is_valid is False
    assert validation_result.message == '"driver_cores" input must be a multiple of 0.1'


@pytest.mark.parametrize("cores", ["0.51", 0.35])
def test_validate_driver_cores_rejects_values_not_a_multiple_of_a_tenth(cores):
    # Arrange
    validation_rule = ValidationRule({
        'classification': 'Optional',
        'default': 0.1,
        'minimum': 0.1,
        'maximum': 1
    })
    # Act
    validation_result = argument_validator.validate("driver_cores", cores, validation_rule)
    # Assert
    assert validation_result.is_valid is False
    assert validation_result.message == '"driver_cores" input must be a multiple of 0.1'


@pytest.mark.parametrize("cores", ["0.0", 0, "1.1", 1.1])
def test_validate_driver_cores_rejects_values_outside_valid_range(cores):
    # Arrange
    validation_rule = ValidationRule({
        'classification': 'Optional',
        'default': 0.1,
        'minimum': 0.1,
        'maximum': 1
    })
    # Act
    validation_result = argument_validator.validate("driver_cores", cores, validation_rule)
    # Assert
    assert validation_result.is_valid is False
    assert validation_result.message == '"driver_cores" input must be in range [0.1, 1]'


@pytest.mark.parametrize("memory", ["512m", "1000m", "2048m"])
def test_validate_driver_memory_accepts_values_for_megabytes_as_string(memory):
    # Arrange
    validation_rule = ValidationRule({
        'classification': 'Optional',
        'default': '512m',
        'minimum': 512,
        'maximum': 2048
    })
    # Act
    validation_result = argument_validator.validate("driver_memory", memory, validation_rule)
    # Assert
    assert validation_result.is_valid is True


@pytest.mark.parametrize("memory", ["0m", "511m", "2049m", "4096m"])
def test_validate_driver_memory_rejects_values_outside_range(memory):
    # Arrange
    validation_rule = ValidationRule({
        'classification': 'Optional',
        'default': '512m',
        'minimum': 512,
        'maximum': 2048
    })
    # Act
    validation_result = argument_validator.validate("driver_memory", memory, validation_rule)
    # Assert
    assert validation_result.is_valid is False
    assert validation_result.message == '"driver_memory" input must be in range [512m, 2048m]'


@pytest.mark.parametrize("memory", ["4096", "  ", "20nb279", "2050.56", "3289.43", "", "512M", "1g", "1G"])
def test_validate_driver_memory_rejects_incorrectly_formatted_values(memory):
    # Arrange
    validation_rule = ValidationRule({
        'classification': 'Optional',
        'default': '512m',
        'minimum': 512,
        'maximum': 2048
    })
    # Act
    validation_result = argument_validator.validate("driver_memory", memory, validation_rule)
    # Assert
    assert validation_result.is_valid is False
    assert validation_result.message == '"driver_memory" input must be a string integer value ending in "m" ' \
                                        '(e.g. "512m" for 512 megabytes)'


@pytest.mark.parametrize("executors", ["1", "2", "5"])
def test_validate_executors_accepts_numerical_values_within_valid_range(executors):
    # Arrange
    validation_rule = ValidationRule({
        'classification': 'Optional',
        'default': 1,
        'minimum': 1,
        'maximum': 10
    })
    # Act
    validation_result = argument_validator.validate("executors", executors, validation_rule)
    # Assert
    assert validation_result.is_valid is True


@pytest.mark.parametrize("executors", [" ", "", "1p", "3.3", "4.0"])
def test_validate_executors_rejects_badly_formatted_inputs(executors):
    # Arrange
    validation_rule = ValidationRule({
        'classification': 'Optional',
        'default': 1,
        'minimum': 1,
        'maximum': 10
    })
    # Act
    validation_result = argument_validator.validate("executors", executors, validation_rule)
    # Assert
    assert validation_result.is_valid is False
    assert validation_result.message == '"executors" input must be an integer'


@pytest.mark.parametrize("executors", ["100", "0", "11", "-1"])
def test_validate_executors_rejects_values_outside_valid_range(executors):
    # Arrange
    validation_rule = ValidationRule({
        'classification': 'Optional',
        'default': 1,
        'minimum': 1,
        'maximum': 10
    })
    # Act
    validation_result = argument_validator.validate("executors", executors, validation_rule)
    # Assert
    assert validation_result.is_valid is False
    assert validation_result.message == '"executors" input must be in range [1, 10]'


@pytest.mark.parametrize("executor_cores", ["1", "2", "3", "4"])
def test_validate_executor_cores_accepts_numerical_values_within_valid_range(executor_cores):
    # Arrange
    validation_rule = ValidationRule({
        'classification': 'Optional',
        'default': 1,
        'minimum': 1,
        'maximum': 4
    })
    # Act
    validation_result = argument_validator.validate("executor_cores", executor_cores, validation_rule)
    # Assert
    assert validation_result.is_valid is True


@pytest.mark.parametrize("executor_cores", ["100", "0", " ", "", "1p", "5000m", "3.0"])
def test_validate_executor_cores_rejects_values_outside_valid_range_or_with_bad_format(executor_cores):
    # Arrange
    validation_rule = ValidationRule({
        'classification': 'Optional',
        'default': 1,
        'minimum': 1,
        'maximum': 4
    })
    # Act
    validation_result = argument_validator.validate("executor_cores", executor_cores, validation_rule)
    # Assert
    assert validation_result.is_valid is False


@pytest.mark.parametrize("memory", ["512m", "1000m", "4096m"])
def test_validate_executor_memory_values_for_megabytes_as_string(memory):
    # Arrange
    validation_rule = ValidationRule({
        'classification': 'Optional',
        'default': '512m',
        'minimum': 512,
        'maximum': 4096
    })
    # Act
    validation_result = argument_validator.validate("executor_memory", memory, validation_rule)

    # Assert
    assert validation_result.is_valid is True


@pytest.mark.parametrize("memory", ["0m", "511m", "4097m"])
def test_validate_executor_memory_rejects_values_outside_valid_range(memory):
    # Arrange
    validation_rule = ValidationRule({
        'classification': 'Optional',
        'default': '512m',
        'minimum': 512,
        'maximum': 4096
    })
    # Act
    validation_result = argument_validator.validate("executor_memory", memory, validation_rule)
    # Assert
    assert validation_result.is_valid is False
    assert validation_result.message == '"executor_memory" input must be in range [512m, 4096m]'


@pytest.mark.parametrize("memory", ["4096", "  ", "20nb279", "2050.56", "3289.43", "", "512M", "1g", "1G"])
def test_validate_executor_memory_rejects_incorrectly_formatted_values(memory):
    # Arrange
    validation_rule = ValidationRule({
        'classification': 'Optional',
        'default': '512m',
        'minimum': 512,
        'maximum': 4096
    })
    # Act
    validation_result = argument_validator.validate("executor_memory", memory, validation_rule)
    # Assert
    assert validation_result.is_valid is False
    assert validation_result.message == '"executor_memory" input must be a string integer value ending in "m" ' \
                                        '(e.g. "512m" for 512 megabytes)'


@pytest.mark.parametrize("label", ["someLabel", "12321"])
def test_validate_label_validates_non_empty_strings(label):
    # Arrange
    validation_rule = ValidationRule({'classification': 'Optional'})
    # Act
    validation_result = argument_validator.validate("label", label, validation_rule)
    # Assert
    assert validation_result.is_valid is True


@pytest.mark.parametrize("label", [" ", "", 123323, None])
def test_validate_label_rejects_empty_strings_and_non_strings(label):
    # Arrange
    validation_rule = ValidationRule({'classification': 'Optional'})
    # Act
    validation_result = argument_validator.validate("label", label, validation_rule)
    # Assert
    assert validation_result.is_valid is False


@pytest.mark.parametrize("driver_core_limit", ["1", "2.5", "3.2", "4"])
def test_validate_core_limit_accepts_numerical_values_within_valid_range(driver_core_limit):
    # Arrange
    validation_rule = ValidationRule({
        'classification': 'Optional',
        'default': 1,
        'minimum': 1,
        'maximum': 4
    })
    # Act
    validation_result = argument_validator.validate("driver_core_limit", driver_core_limit, validation_rule)
    # Assert
    assert validation_result.is_valid is True


def test_validate_core_limit_converts_floats_to_millicpu_values_for_manifest():
    # Arrange
    validation_rule = ValidationRule({
        'classification': 'Optional',
        'default': 1,
        'minimum': 1,
        'maximum': 4
    })
    # Act
    validation_result = argument_validator.validate("driver_core_limit", "1.2", validation_rule)
    # Assert
    assert validation_result.is_valid is True
    assert validation_result.validated_value == "1200m"


@pytest.mark.parametrize("executor_core_limit", ["0.9", "0", "4.1", "5"])
def test_validate_core_limit_rejects_values_outside_valid_range(executor_core_limit):
    # Arrange
    validation_rule = ValidationRule({
        'classification': 'Optional',
        'default': 1,
        'minimum': 1,
        'maximum': 4
    })
    # Act
    validation_result = argument_validator.validate("executor_core_limit", executor_core_limit, validation_rule)
    # Assert
    assert validation_result.is_valid is False
    assert validation_result.message == '"executor_core_limit" input must be in range [1, 4]'


@pytest.mark.parametrize("executor_core_limit", ["1.01", "1p", "2000m", ""])
def test_validate_core_limit_rejects_incorrectly_formatted_values(executor_core_limit):
    # Arrange
    validation_rule = ValidationRule({
        'classification': 'Optional',
        'default': 1,
        'minimum': 1,
        'maximum': 4
    })
    # Act
    validation_result = argument_validator.validate("executor_core_limit", executor_core_limit, validation_rule)
    # Assert
    assert validation_result.is_valid is False
    assert validation_result.message == '"executor_core_limit" input must be a multiple of 0.1'
