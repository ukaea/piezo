import pytest
from PiezoWebApp.src.utils.dict_argument_helper import set_value_in_nested_dict


class TestDictArgumentHelper:

    def test_set_value_in_nested_dict_sets_value_at_top_level_when_path_has_len_one(self):
        # Arrange
        path = ["x"]
        nested_dict = {"a": 1, "b": {"c": 2}, "d": {"e": {"f": 3}}}
        value = 5
        # Act
        result = set_value_in_nested_dict(nested_dict, path, value)
        # Assert
        assert result == {"a": 1, "b": {"c": 2}, "d": {"e": {"f": 3}}, "x": 5}

    def test_set_value_in_nested_dict_sets_nested_values_for_paths_longer_than_one(self):
        # Arrange
        path = ["d", "e", "g"]
        nested_dict = {"a": 1, "b": {"c": 2}, "d": {"e": {"f": 3}}}
        value = 5
        # Act
        result = set_value_in_nested_dict(nested_dict, path, value)
        # Assert
        assert result == {"a": 1, "b": {"c": 2}, "d": {"e": {"f": 3, "g": 5}}}

    def test_set_value_in_nested_dict_throw_an_error_if_path_not_in_nested_dict(self):
        # Arrange
        path = ["x", "z", "g"]
        nested_dict = {"a": 1, "b": {"c": 2}, "d": {"e": {"f": 3}}}
        value = 5
        # Act
        with pytest.raises(KeyError):
            set_value_in_nested_dict(nested_dict, path, value)

    def test_set_value_in_nested_dict_throw_an_error_if_no_path_given(self):
        # Arrange
        path = []
        nested_dict = {"a": 1, "b": {"c": 2}, "d": {"e": {"f": 3}}}
        value = 5
        # Act
        with pytest.raises(IndexError):
            set_value_in_nested_dict(nested_dict, path, value)

