from PiezoWebApp.src.utils.str_helper import is_str_empty
from PiezoWebApp.src.models.spark_job_validation_result import ValidationResult


def validate(key, value, validation_rule):
    if key in ["name", "path_to_main_app_file", "main_class"]:
        return _validate_non_empty_string(key, value)
    if key in ["language", "python_version"]:
        return _validate_string_from_list(key, value, validation_rule)
    if key in ["executors", "executor_cores"]:
        return _validate_integer(key, value, validation_rule)
    if key in ["driver_cores"]:
        return _validate_multiple_of_a_tenth(key, value, validation_rule)
    if key == "driver_core_limit":
        return _validate_driver_core_limit(value, validation_rule.minimum, validation_rule.maximum)
    if key == "driver_memory":
        return _validate_driver_memory(value, validation_rule.minimum, validation_rule.maximum)
    if key == "executor_memory":
        return _validate_executor_memory(value, validation_rule.minimum, validation_rule.maximum)
    raise ValueError(f"Unexpected argument {key}")


def _validate_non_empty_string(key, value):
    if not isinstance(value, str):
        return ValidationResult(False, f'"{key}" input must be a string', None)
    if is_str_empty(value) is True:
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
    except ValueError or TypeError:
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


def _validate_driver_core_limit(value, min_value, max_value):
    format_error_msg = "Driver core limit must be a string of the form 'X' (where X is an int or float and represents" \
                       " the number of cpus to the nearest 0.1 or 'Xm' (where Xm is a string and the m " \
                       "represents millicpus). Note: 0.1 == '100m', 1 == 1000m"
    value_error_msg = f"Driver core limit = {value} outside of valid range ({min_value}, {max_value}) or " \
                      f"({str(int(min_value*1000))+'m'}, {str(int(max_value*1000))+'m'}) and be given to 0.1 cpu (100m)"
    return _validate_cores(value, min_value, max_value, format_error_msg, value_error_msg)


def _validate_driver_memory(value, min_value, max_value):
    format_error_msg = "Driver memory must be a string in the format 'Xm' where X is the number of megabytes, " \
                       "integers are also accepted but are assumed to also be megabytes."
    value_error_msg = f"Driver memory = {value} is outside of valid range " \
                      f"({str(min_value) + 'm'}, {str(max_value) + 'm'})"
    return _validate_memory(value, min_value, max_value, format_error_msg, value_error_msg)


def _validate_executor_memory(value, min_value, max_value):
    format_error_msg = "Executor memory must be a string in the format 'Xm' where X is the number of megabytes, " \
                       "integers are also accepted but are assumed to also be megabytes."
    value_error_msg = f"Executor memory = {value} is outside of valid range " \
                      f"({str(min_value) + 'm'}, {str(max_value) + 'm'})"
    return _validate_memory(value, min_value, max_value, format_error_msg, value_error_msg)


def _validate_memory(value, min_value, max_value, format_error_msg, value_error_msg):
    if isinstance(value, str):
        try:
            numerical_value = float(value[:-1]) if value[-1] == "m" else float(value)
            is_valid = min_value <= numerical_value <= max_value if numerical_value % 1 == 0 else False
        except (ValueError, IndexError):
            return ValidationResult(
                False, format_error_msg, None)
    elif isinstance(value, (float, int)):
        is_valid = min_value <= value <= max_value if value % 1 == 0 else False
        value = f"{int(value)}m"
    else:
        return ValidationResult(False, format_error_msg, None)
    if is_valid:
        return ValidationResult(True, None, value)
    return ValidationResult(False, value_error_msg, None)


def _validate_cores(value, min_value, max_value, format_error_msg, value_error_msg):
    if isinstance(value, (float, int)):
        is_valid = min_value <= value <= max_value if (value*10) % 1 == 0 else False
    elif isinstance(value, str):
        try:
            numerical_value = float(value[:-1])/1000 if value[-1] == "m" else float(value)
            is_valid = min_value <= numerical_value <= max_value if (numerical_value*10) % 1 == 0 else False
        except (ValueError, IndexError):
            return ValidationResult(False, format_error_msg, None)
    else:
        is_valid = False
    return ValidationResult(True, None, str(value)) if is_valid is True else ValidationResult(
        False, value_error_msg, None)
