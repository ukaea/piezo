import pytest
import mock

from PiezoWebApp.src.models.spark_job_argument_classification import ArgumentClassification
from PiezoWebApp.src.models.validation_rule import ValidationRule
from PiezoWebApp.src.services.spark_job.validation.validation_service import ValidationService
from PiezoWebApp.src.services.spark_job.validation.validation_ruleset import ValidationRuleset


class TestValidationService:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.mock_validation_ruleset = mock.create_autospec(ValidationRuleset)
        self.mock_validation_ruleset.get_keys_of_required_inputs.return_value = []
        self.mock_validation_ruleset.get_keys_of_optional_inputs.return_value = []
        self.test_service = ValidationService(self.mock_validation_ruleset)

    def test_validate_request_keys(self):
        # Arrange
        self.mock_validation_ruleset.get_keys_of_required_inputs = ["name", "language", "main_class"]
        request_body = {
            'name': 'example-spark-job',
            'language': 'scala',
            'main_class': 'main.class'
        }
        # Act
        result = self.test_service.validate_request_keys(request_body)
        # Assert
        assert result.is_valid is True


    def test_check_all_required_args_are_provided_returns_invalid_if_a_required_arg_is_missing(self):
        # Arrange
        request_body = {"name": "test", "language": "scala"}
        # Act
        result = self.test_service._check_all_required_args_are_provided(request_body)
        # Assert
        assert result["path_to_main_app_file"].is_valid is False
        assert result["path_to_main_app_file"].message == "Missing required argument path_to_main_app_file"
        assert result["name"].is_valid is True
        assert result["language"].is_valid is True

    @pytest.mark.parametrize("request_body", [{"language": "C++"}, {"language": "R"}, {"language": ""}])
    def test_validate_language_requirements_returns_invalid_if_not_python_or_scala(self, request_body):
        # Act
        result = self.test_service._validate_language_requirements(request_body)
        # Assert
        assert result.is_valid is False
        assert result.message == "Invalid language provided, please use one of ['python', 'scala']"

    @pytest.mark.parametrize("request_body", [{"language": "PYTHON"},
                                              {"language": "python"},
                                              {"language": "Python"},
                                              {"language": "PyThOn"}])
    def test_validate_language_requirements_adds_python_version_to_required_args_when_given_python(self, request_body):
        # Act
        result = self.test_service._validate_language_requirements(request_body)
        # Assert
        assert result.validated_value["language"] == "Python"
        assert result.message == "language validated"
        assert result.is_valid is True
        assert "python_version" in self.test_service._required_args_from_user

    @pytest.mark.parametrize("request_body", [{"language": "SCALA"},
                                              {"language": "scala"},
                                              {"language": "Scala"},
                                              {"language": "ScAlA"}])
    def test_validate_language_requirements_adds_main_class_to_required_args_when_given_scala(self, request_body):
        # Act
        result = self.test_service._validate_language_requirements(request_body)
        # Assert
        assert result.validated_value["language"] == "Scala"
        assert result.message == "language validated"
        assert result.is_valid is True
        assert "main_class" in self.test_service._required_args_from_user

    def test_check_for_unsupported_args_returns_unsupported_args(self):
        # Arrange
        request_body = {"unsupported_arg": "test", "name": "test_name"}
        # Act
        result = self.test_service._check_for_unsupported_args(request_body)
        # Assert
        assert result == ["unsupported_arg"]
