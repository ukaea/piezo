import pytest

from PiezoWebApp.src.utils.route_helper import format_route_specification
from PiezoWebApp.src.utils.route_helper import is_scheme_secure
from PiezoWebApp.src.utils.route_helper import is_valid_k8s_scheme_https

def test_format_route_specification_returns_flexible_route_for_appropriate_name():
    # Arrange
    name = "test"
    # Act
    route = format_route_specification(name)
    # Assert
    assert route == r'/test(|/)'


@pytest.mark.parametrize("name", ["", " ", None, ])
def test_format_route_specification_raises_value_error_if_name_empty(name):
    with pytest.raises(ValueError) as exception_info:
        format_route_specification(name)
    assert str(exception_info.value) == "Route name must not be empty!"


@pytest.mark.parametrize("scheme", ["https", "sftp", "HTTPS", "SFTP"])
def test_is_scheme_secure_returns_true_for_secure_schemes(scheme):
    assert is_scheme_secure(scheme) is True


@pytest.mark.parametrize("scheme", ["http", "ftp", "HTTP", "FTP"])
def test_is_scheme_secure_returns_false_for_insecure_schemes(scheme):
    assert is_scheme_secure(scheme) is False


@pytest.mark.parametrize("scheme", ["", " ", None, 4])
def test_is_scheme_secure_raises_value_error_for_unrecognised(scheme):
    with pytest.raises(ValueError) as exception_info:
        is_scheme_secure(scheme)
    assert str(exception_info.value) == f'"{scheme}" not recognised as a valid scheme'


@pytest.mark.parametrize("scheme", ["https", "HTTPS"])
def test_is_valid_k8s_scheme_https_returns_true_for_https_schemes(scheme):
    assert is_valid_k8s_scheme_https(scheme) is True


@pytest.mark.parametrize("scheme", ["http", "HTTP"])
def test_is_valid_k8s_scheme_https_returns_false_for_non_http(scheme):
    assert is_valid_k8s_scheme_https(scheme) is False


@pytest.mark.parametrize("scheme", ["", " ", None, 4, "ftp", "FTP", "sftp", "SFTP"])
def test_is_valid_k8s_scheme_https_raises_value_error_for_non_http_or_https(scheme):
    with pytest.raises(ValueError) as exception_info:
        is_valid_k8s_scheme_https(scheme)
    assert str(exception_info.value) == f'"{scheme}" not recognised as a valid scheme'
