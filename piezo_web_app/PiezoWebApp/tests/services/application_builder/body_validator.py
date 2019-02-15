import pytest

from PiezoWebApp.src.services.validator import CommonPropsValidator

class TestCommonPropsValidator:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.test_common_props_validator = CommonPropsValidator()


    def test_common_props_validator_throws_an_error_when_a_required_argument_is_missing(self):
