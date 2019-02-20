import pytest

from PiezoWebApp.src.services.validator.argument_validation_service import ArgumentValidationService


class TestArgumentValidator:
    @pytest.fixture(autouse=True)
    def setup(self):
        self._test_argument_validator = ArgumentValidationService()

    @pytest.mark.parametrize("request_body", [
                             {"name": "test", "language": "scala"},
                             {"name": "test", "path_to_main_app_file": "/path/to/app/file"},
                             {"language": "Scala", "path_to_main_app_file": "/path/to/app/file"}]
                             )
    def test_check_all_required_args_are_provided_returns_value_error_if_a_required_arg_is_missing(self, request_body):
        # Act/Assert
        with pytest.raises(ValueError):
            self._test_argument_validator._check_all_required_args_are_provided(request_body)

    @pytest.mark.parametrize("request_body", [{"language": "C++"}, {"language": "R"}, {"language": ""}])
    def test_validate_language_requirements_raises_value_error_if_arg_is_not_python_or_scala(self, request_body):
        # Act/Assert
        with pytest.raises(ValueError):
            self._test_argument_validator._validate_language_requirements(request_body)

    @pytest.mark.parametrize("request_body", [{"language": "PYTHON"},
                                              {"language": "python"},
                                              {"language": "Python"},
                                              {"language": "PyThOn"}])
    def test_validate_language_requirements_adds_python_version_to_optional_args_when_given_python(self, request_body):
        # Act
        self._test_argument_validator._validate_language_requirements(request_body)
        # Assert
        assert request_body["language"] == "Python"
        assert "python_version" in self._test_argument_validator._required_args_from_user
        assert "main_class" not in self._test_argument_validator._required_args_from_user

    @pytest.mark.parametrize("request_body", [{"language": "SCALA"},
                                              {"language": "scala"},
                                              {"language": "Scala"},
                                              {"language": "ScAlA"}])
    def test_validate_language_requirements_adds_main_class_to_optional_args_when_given_scala(self, request_body):
        # Act
        self._test_argument_validator._validate_language_requirements(request_body)
        # Assert
        assert request_body["language"] == "Scala"
        assert "main_class" in self._test_argument_validator._required_args_from_user
        assert "python_version" not in self._test_argument_validator._required_args_from_user

    def test_check_for_unsupported_args_throws_value_error_if_unsupported_argument_supplied(self):
        # Arrange
        request_body = {"unsupported_arg": "test"}
        # Act/Assert
        with pytest.raises(ValueError):
            self._test_argument_validator._check_for_unsupported_args(request_body)
