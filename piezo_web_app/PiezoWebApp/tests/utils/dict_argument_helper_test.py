import pytest

from PiezoWebApp.src.utils.dict_argument_helper import get_items_not_in_keys
from PiezoWebApp.src.utils.dict_argument_helper import get_keys_not_in_list
from PiezoWebApp.src.utils.dict_argument_helper import set_value_in_nested_dict


def test_get_items_not_in_keys_finds_simple_missing_key():
    # Arrange
    lst = ['a', 'b', 'c']
    dictionary = {'a': 1, 'c': 3}
    # Act
    result = get_items_not_in_keys(lst, dictionary)
    # Assert
    assert result == ['b']


def test_get_keys_not_in_list_finds_simple_missing_key():
    # Arrange
    dictionary = {'a': 1, 'b': 2, 'c': 3}
    lst = ['a', 'c']
    # Act
    result = get_keys_not_in_list(dictionary, lst)
    # Assert
    assert result == ['b']


def test_set_value_in_nested_dict_sets_value_at_top_level_when_path_has_len_one():
    # Arrange
    path = ["x"]
    nested_dict = {"a": 1, "b": {"c": 2}, "d": {"e": {"f": 3}}}
    value = 5
    # Act
    result = set_value_in_nested_dict(nested_dict, path, value)
    # Assert
    assert result == {"a": 1, "b": {"c": 2}, "d": {"e": {"f": 3}}, "x": 5}


def test_set_value_in_nested_dict_sets_nested_values_for_paths_longer_than_one():
    # Arrange
    path = ["e", "f", "i"]
    nested_dict = {"a": 1, "b": {"c": 2, "d": 3}, "e": {"f": {"g": 4, "h": 5}}}
    value = 6
    # Act
    result = set_value_in_nested_dict(nested_dict, path, value)
    # Assert
    assert result == {"a": 1, "b": {"c": 2, "d": 3}, "e": {"f": {"g": 4, "h": 5, "i": 6}}}


def test_set_value_in_nested_dict_overwrites_value_that_already_exists():
    # Arrange
    path = ["d", "e", "g"]
    nested_dict = {"a": 1, "b": {"c": 2}, "d": {"e": {"f": 3, "g": 4}}}
    value = 5
    # Act
    result = set_value_in_nested_dict(nested_dict, path, value)
    # Assert
    assert result == {"a": 1, "b": {"c": 2}, "d": {"e": {"f": 3, "g": 5}}}


def test_set_value_in_nested_dict_throw_an_error_if_path_not_in_nested_dict():
    # Arrange
    path = ["x", "z", "g"]
    nested_dict = {"a": 1, "b": {"c": 2}, "d": {"e": {"f": 3}}}
    value = 5
    # Act
    with pytest.raises(KeyError):
        set_value_in_nested_dict(nested_dict, path, value)


def test_set_value_in_nested_dict_throw_an_error_if_no_path_given():
    # Arrange
    path = []
    nested_dict = {"a": 1, "b": {"c": 2}, "d": {"e": {"f": 3}}}
    value = 5
    # Act
    with pytest.raises(IndexError):
        set_value_in_nested_dict(nested_dict, path, value)
