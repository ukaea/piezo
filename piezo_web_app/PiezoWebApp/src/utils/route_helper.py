import re

from PiezoWebApp.src.utils.str_helper import is_str_empty


def format_route_specification(name):
    if is_str_empty(name):
        raise ValueError("Route name must not be empty!")
    return r'/' + name + r'(|/)'


def is_scheme_secure(scheme):
    if not isinstance(scheme, str):
        raise ValueError(f'"{scheme}" not recognised as a valid scheme')
    if scheme.lower() == 'https':
        return True
    if scheme.lower() == 'http':
        return False
    if scheme.lower() == 'sftp':
        return True
    if scheme.lower() == 'ftp':
        return False
    raise ValueError(f'"{scheme}" not recognised as a valid scheme')


def is_valid_pod_name(label):
    # https://github.com/ukaea/piezo/wiki/WebAppDecisionRecord#maximum-length-of-a-job-name
    if 1 < len(label) <= 29:
        match = re.match("^([a-z])([\\.\\-0-9a-z]*)?([0-9a-z])$", label)
        if match is None:
            return False
        for pattern in ["--", "-.", ".-", ".."]:
            if pattern in label:
                return False
        return True
    elif len(label) <= 1:
        match = re.match("^[a-z]$", label)
        return match is not None
    else:
        return False
