import pytest

from PiezoWebApp.src.utils.route_helper import format_route_specification
from PiezoWebApp.src.utils.route_helper import is_valid_pod_name


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


@pytest.mark.parametrize("label", ["acb123"])
def test_is_valid_pod_name_returns_true_for_valid_labels(label):
    assert is_valid_pod_name(label) is True


@pytest.mark.parametrize("label", [".label"])
def test_is_valid_pod_name_returns_false_for_invalid_labels(label):
    assert is_valid_pod_name(label) is False
