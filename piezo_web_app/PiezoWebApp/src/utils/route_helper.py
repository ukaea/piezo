import re

from PiezoWebApp.src.utils.str_helper import is_str_empty


def format_route_specification(name):
    if is_str_empty(name):
        raise ValueError("Route name must not be empty!")
    return r'/' + name + r'(|/)'


def is_valid_pod_name(label):
    if len(label) > 1:
        match = re.match("^([0-9a-z])([\\.\\-0-9a-z]*)?([0-9a-z])$", label)
        if match is None:
            return False
        for pattern in ["--", "-.", ".-", ".."]:
            if pattern in label:
                return False
        return True
    else:
        match = re.match("^[0-9a-z]$", label)
        return match is not None

