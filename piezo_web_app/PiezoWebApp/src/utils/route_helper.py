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


def is_valid_k8s_scheme_https(scheme):
    if not isinstance(scheme, str):
        raise ValueError(f'"{scheme}" not recognised as a valid scheme')
    if scheme.lower() == 'https':
        return True
    if scheme.lower() == 'http':
        return False
    raise ValueError(f'"{scheme}" not recognised as a valid scheme')
