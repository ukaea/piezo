from PiezoWebApp.src.utils.str_helper import is_str_empty
from PiezoWebApp.src.models.spark_job_validation_result import ValidationResult


def validate(key, value, validation_rule):
    if key == "name":
        return _validate_name(value)
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


def _validate_name(value):
    validation_result = _validate_non_empty_string("name", value)
    if not validation_result.is_valid:
        return validation_result
    if len(value) > 200:
        return ValidationResult(False, '"name" input has a maximum length of 200 characters', None)
    # TODO composed of a-z-. and must start/end with a-z
    return ValidationResult(True, None, value)


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
