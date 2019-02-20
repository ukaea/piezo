import pytest

from PiezoWebApp.src.utils.route_helper import format_route_specification


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
