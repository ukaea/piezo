import pytest

from PiezoWebApp.src.utils.str_helper import str2non_negative_int


def test_str2non_negative_int_accepts_positive_integer():
    string = "42"
    integer = str2non_negative_int(string)
    assert integer == 42


def test_str2non_negative_int_accepts_zero():
    string = "0"
    integer = str2non_negative_int(string)
    assert integer == 0


def test_str2non_negative_int_throws_value_error_for_negative_integer():
    with pytest.raises(ValueError) as exception_info:
        str2non_negative_int("-42")
    assert str(exception_info.value) == "'-42' is not a non-negative integer"


def test_str2non_negative_int_throws_value_error_for_positive_float():
    with pytest.raises(ValueError):
        str2non_negative_int("42.5")


def test_str2non_negative_int_throws_value_error_for_negative_float():
    with pytest.raises(ValueError):
        str2non_negative_int("-42.5")


def test_str2non_negative_int_throws_value_error_for_empty_string():
    with pytest.raises(ValueError):
        str2non_negative_int("")


def test_str2non_negative_int_throws_type_error_for_none():
    with pytest.raises(TypeError):
        str2non_negative_int(None)
