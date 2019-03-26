import pytest

from PiezoWebApp.src.utils.str_helper import str2bool


@pytest.mark.parametrize("string", ["true", "TRUE", "True", ])
def test_str2bool_accepts_correct_true(string):
    result = str2bool(string)
    assert result is True


@pytest.mark.parametrize("string", ["false", "FALSE", "False", ])
def test_str2bool_accepts_correct_false(string):
    result = str2bool(string)
    assert result is False


@pytest.mark.parametrize("string", ["", "maybe", ])
def test_str2bool_raises_value_error(string):
    with pytest.raises(ValueError) as exception_info:
        str2bool(string)
    assert str(exception_info.value) == "'{}' not recognised as a Boolean. Use 'True' or 'False' (case insensitive)."\
        .format(string)
