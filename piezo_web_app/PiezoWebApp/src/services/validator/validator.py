from PiezoWebApp.src.utils.str_helper import is_str_empty


def validate_name(value):
    if is_str_empty(value) is True:
        raise ValueError("name argument cannot be empty")
    return value


def validate_language(value):
    if str(value.lower()) not in ["python", "scala"]:
        raise ValueError("language must be either 'python' or 'Scala'")
    return value


def validate_python_version(value):
    if value in ["2", "3"] is False:
        raise ValueError("Python version must be either '2' or '3'")
    return value


def validate_path_to_main_app_file(value):
    if is_str_empty(value) is True:
        raise ValueError("path_to_main_app_file argument cannot be empty")
    return value


def validate_main_class(value):
    if is_str_empty(value) is True:
        raise ValueError("main_class argument cannot be empty")
    return value


def validate_driver_cores(value, min_value, max_value):
    if isinstance(value, str):
        numerical_value = int(value.strip("m"))
        decimal_value = numerical_value/1000
    elif isinstance(value, int) or isinstance(float):
        decimal_value = round(float(value), 1)
    else:
        raise ValueError("Driver cores must be of the form X (where X is an int or float and represents the"
                         " number of cpus or 'Xm' (where Xm is a string and the m represents millicpus). Note:"
                         "0.1 == '100m'")
    is_valid = min_value <= decimal_value <= max_value
    if is_valid is False:
        raise ValueError(f"Driver core = {value} outside of valid range ({min_value}, {max_value}) or "
                         f"({str(int(min_value*1000))+'m'}, {str(int(max_value*1000))+'m'}")
    return decimal_value


def validate_driver_memory(value, min_value, max_value):
    if isinstance(value, str):
        numerical_value = value.strip("m")
        if isinstance(numerical_value, int):
            is_valid = min_value <= numerical_value <= max_value
            if is_valid:
                return numerical_value
            raise ValueError(f"Driver memory = {value} is outside of valid range "
                             f"({str(min_value) + 'm'}, {str(max_value) + 'm'}")
    raise ValueError("Driver memory must be a string in the format 'Xm' where X is the number of megabytes")


def validate_driver_core_limit(value, min_value, max_value):
    if isinstance(value, str):
        numerical_value = int(value.strip("m"))
        decimal_value = numerical_value/1000
    elif isinstance(value, int) or isinstance(float):
        decimal_value = round(float(value), 1)
    else:
        raise ValueError("Driver core limit must be of the form X (where X is an int or float and represents the"
                         " number of cpus or 'Xm' (where Xm is a string and the m represents millicpus). Note:"
                         "0.1 == '100m'")
    is_valid = min_value <= decimal_value <= max_value
    if is_valid is False:
        raise ValueError(f"Driver core limit = {value} outside of valid range ({min_value}, {max_value}) or "
                         f"({str(int(min_value*1000))+'m'}, {str(int(max_value*1000))+'m'}")
    return decimal_value


def validate_executors(value, min_value, max_value):
    if not isinstance(value, int):
        raise ValueError(f"Executors argument must be an integer")
    is_valid = min_value <= value <= max_value
    if is_valid is True:
        return value
    raise ValueError(f"Executors = {value} outside of valid values range ({min_value}, {max_value})")


def validate_executor_cores(value, min_value, max_value):
    if isinstance(value, str):
        numerical_value = int(value.strip("m"))
        decimal_value = numerical_value/1000
    elif isinstance(value, int) or isinstance(float):
        decimal_value = round(float(value), 1)
    else:
        raise ValueError("Executor cores must be of the form X (where X is an int or float and represents the"
                         " number of cpus or 'Xm' (where Xm is a string and the m represents millicpus). Note:"
                         "0.1 == '100m'")
    is_valid = min_value <= decimal_value <= max_value
    if is_valid is False:
        raise ValueError(f"Executor cores = {value} outside of valid range ({min_value}, {max_value}) or "
                         f"({str(int(min_value*1000))+'m'}, {str(int(max_value*1000))+'m'}")
    return decimal_value


def validate_executor_memory(value, min_value, max_value):
    if isinstance(value, str):
        numerical_value = value.strip("m")
        if isinstance(numerical_value, int):
            is_valid = min_value <= numerical_value <= max_value
            if is_valid:
                return numerical_value
            raise ValueError(f"Executor memory = {value} is outside of valid range "
                             f"({str(min_value) + 'm'}, {str(max_value) + 'm'}")
    raise ValueError("Executor memory must be a string in the format 'Xm' where X is the number of megabytes")

