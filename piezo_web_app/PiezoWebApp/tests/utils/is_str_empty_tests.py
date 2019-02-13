import pytest

from PiezoWebApp.src.utils.str_helper import is_str_empty


@pytest.mark.parametrize("string", ["a", "1", "This sentence is not true.", ])
def test_is_str_empty_returns_false_for_valid_strings(string):
    result = is_str_empty(string)
    assert result is False


@pytest.mark.parametrize("string", [None, "", " ", "    ", ])
def test_is_str_empty_returns_true_for_empty_strings(string):
    result = is_str_empty(string)
    assert result is True
