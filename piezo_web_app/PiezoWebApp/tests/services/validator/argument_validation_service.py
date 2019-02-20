import pytest
import mock

from PiezoWebApp.src.services.validator.argument_validation_service import ArgumentValidationService
from PiezoWebApp.src.services.validator.validation_rules import ValidationRules


class TestArgumentValidator:
    @pytest.fixture(autouse=True)
    def setup(self):
        validation_dict = {"apiVersion": [None, None, "sparkoperator.k8s.io/v1beta1", "base"],
                           "kind": [None, None, "SparkApplication", "base"],
                           "namespace": [None, None, "default", "base"],
                           "mode": [None, None, "cluster", "base"],
                           "image": [None, None, "gcr.io/spark-operator/spark:v2.4.0", "base"],
                           "image_pull_policy": [None, None, "Always", "base"],
                           "spark_version": [None, None, "2.4.0", "base"],
                           "restart_policy": [None, None, "Never", "base"],
                           "service_account": [None, None, "spark", "base"],
                           "name": [None, None, None, "required"],
                           "language": [None, None, None, "required"],
                           "path_to_main_app_file": [None, None, None, "required"],
                           "driver_cores": [0.1, 1, 0.1, "optional"],
                           "driver_core_limit": [0.2, 1.2, 0.2, "optional"],
                           "driver_memory": [512, 2048, 512, "optional"],
                           "executors": [1, 10, 1, "optional"],
                           "executor_cores": [1, 4, 1, "optional"],
                           "executor_memory": [512, 4096, 512, "optional"],
                           "main_class": [None, None, None, "conditional"],
                           "python_version": [None, None, None, "conditional"]
                           }

        mock_validation_rules = mock.create_autospec(ValidationRules)
        mock_validation_rules._validation_dict = validation_dict
        mock_validation_rules.get_keys_of_required_args = ["name", "language", "path_to_main_app_file"]
        mock_validation_rules.get_keys_of_optional_args = ["driver_cores", "driver_core_limit", "driver_memory",
                                                           "executors", "executor_cores", "executor_memory"]
        self._test_argument_validator = ArgumentValidationService(mock_validation_rules)

    def test_check_all_required_args_are_provided_returns_invalid_if_a_required_arg_is_missing(self):
        # Arrange
        request_body = {"name": "test", "language": "scala"}
        # Act
        result = self._test_argument_validator._check_all_required_args_are_provided(request_body)
        # Assert
        assert result["path_to_main_app_file"].is_valid is False
        assert result["path_to_main_app_file"].message == "Missing required argument path_to_main_app_file"
        assert result["name"].is_valid is True
        assert result["language"].is_valid is True

    @pytest.mark.parametrize("request_body", [{"language": "C++"}, {"language": "R"}, {"language": ""}])
    def test_validate_language_requirements_returns_invalid_if_not_python_or_scala(self, request_body):
        # Act
        result = self._test_argument_validator._validate_language_requirements(request_body)
        # Assert
        assert result.is_valid is False
        assert result.message == "Invalid language provided, please use one of ['python', 'scala']"

    @pytest.mark.parametrize("request_body", [{"language": "PYTHON"},
                                              {"language": "python"},
                                              {"language": "Python"},
                                              {"language": "PyThOn"}])
    def test_validate_language_requirements_adds_python_version_to_required_args_when_given_python(self, request_body):
        # Act
        result = self._test_argument_validator._validate_language_requirements(request_body)
        # Assert
        assert result.validated_value["language"] == "Python"
        assert result.message == "language validated"
        assert result.is_valid is True
        assert "python_version" in self._test_argument_validator._required_args_from_user

    @pytest.mark.parametrize("request_body", [{"language": "SCALA"},
                                              {"language": "scala"},
                                              {"language": "Scala"},
                                              {"language": "ScAlA"}])
    def test_validate_language_requirements_adds_main_class_to_required_args_when_given_scala(self, request_body):
        # Act
        result = self._test_argument_validator._validate_language_requirements(request_body)
        # Assert
        assert result.validated_value["language"] == "Scala"
        assert result.message == "language validated"
        assert result.is_valid is True
        assert "main_class" in self._test_argument_validator._required_args_from_user

    def test_check_for_unsupported_args_returns_unsupported_args(self):
        # Arrange
        request_body = {"unsupported_arg": "test", "name": "test_name"}
        # Act
        result = self._test_argument_validator._check_for_unsupported_args(request_body)
        # Assert
        assert result == ["unsupported_arg"]
