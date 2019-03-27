import re
import string

from PiezoWebApp.src.models.spark_job_validation_result import ValidationResult
from PiezoWebApp.src.utils.str_helper import is_str_empty


def validate(key, value, validation_rule):
    if key == "name":
        return _validate_name(key, value)
    if key in ["name", "path_to_main_app_file", "main_class", "label"]:
        return _validate_non_empty_string(key, value)
    if key in ["language", "python_version"]:
        return _validate_string_from_list(key, value, validation_rule)
    if key in ["executors", "executor_cores"]:
        return _validate_integer(key, value, validation_rule)
    if key in ["driver_cores", "driver_core_limit"]:
        return _validate_multiple_of_a_tenth(key, value, validation_rule)
    if key in ["driver_memory", "executor_memory"]:
        return _validate_byte_quantity(key, value, validation_rule)
    if key in ["arguments"]:
        return ValidationResult(True, None, value)
    raise ValueError(f"Unexpected argument {key}")


def _validate_name(key, value):
    validation_result = _validate_non_empty_string("name", value)
    if not validation_result.is_valid:
        return validation_result

    is_name_valid = True
    if len(value) == 1:
        is_name_valid = value in string.ascii_lowercase
    elif 1 < len(value) <= 29:
        match = re.match("^([a-z])([\\.\\-0-9a-z]*)?([0-9a-z])$", value)
        if match is None:
            is_name_valid = False
        for pattern in ["--", "-.", ".-", ".."]:
            if pattern in value:
                is_name_valid = False
    else:
        is_name_valid = False

    msg = None if is_name_valid else f'"{key}" input must obey naming convention: ' \
        f'see https://github.com/ukaea/piezo/wiki/WebAppUserGuide#submit-a-job'
    return ValidationResult(is_name_valid, msg, value)


def _validate_non_empty_string(key, value):
    if not isinstance(value, str):
        return ValidationResult(False, f'"{key}" input must be a string', None)
    if is_str_empty(value):
        return ValidationResult(False, f'"{key}" input cannot be empty', None)
    return ValidationResult(True, None, value)


def _validate_string_from_list(key, value, validation_rule):
    if not isinstance(value, str):
        return ValidationResult(False, f'"{key}" input must be a string', None)
    if value not in validation_rule.options:
        formatted_options = ", ".join([f'"{option}"' for option in validation_rule.options])
        return ValidationResult(False, f'"{key}" input must be one of: {formatted_options}', None)
    return ValidationResult(True, None, value)


def _validate_integer(key, value, validation_rule):
    try:
        numerical_value = int(value)
    except ValueError:
        return ValidationResult(False, f'"{key}" input must be an integer', None)
    except TypeError:
        return ValidationResult(False, f'"{key}" input must be an integer', None)

    return ValidationResult(True, None, numerical_value) \
        if validation_rule.minimum <= numerical_value <= validation_rule.maximum \
        else ValidationResult(
            False,
            f'"{key}" input must be in range [{validation_rule.minimum}, {validation_rule.maximum}]',
            None
        )


def _validate_multiple_of_a_tenth(key, value, validation_rule):
    not_a_tenth_result = ValidationResult(False, f'"{key}" input must be a multiple of 0.1', None)
    try:
        numerical_value = float(value)
    except ValueError:
        return not_a_tenth_result
    except TypeError:
        return not_a_tenth_result

    multiples_of_a_tenth = 10 * numerical_value
    if multiples_of_a_tenth % 1 != 0:
        return not_a_tenth_result

    return ValidationResult(True, None, numerical_value) \
        if validation_rule.minimum <= numerical_value <= validation_rule.maximum \
        else ValidationResult(
            False,
            f'"{key}" input must be in range [{validation_rule.minimum}, {validation_rule.maximum}]',
            None
        )


def _validate_byte_quantity(key, value, validation_rule):
    wrong_format_result = ValidationResult(
        False,
        f'"{key}" input must be a string integer value ending in "m" (e.g. "512m" for 512 megabytes)',
        None
    )
    if not isinstance(value, str):
        return wrong_format_result
    if is_str_empty(value):
        return wrong_format_result
    if value[-1] != "m":
        return wrong_format_result
    try:
        numerical_value = int(value[:-1])
    except ValueError:
        return wrong_format_result
    except TypeError:
        return wrong_format_result
    return ValidationResult(True, None, value) \
        if validation_rule.minimum <= numerical_value <= validation_rule.maximum \
        else ValidationResult(
            False,
            f'"{key}" input must be in range [{validation_rule.minimum}m, {validation_rule.maximum}m]',
            None
        )
