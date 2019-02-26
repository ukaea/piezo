import pytest

from PiezoWebApp.src.config.spark_job_validation_rules import LANGUAGE_SPECIFIC_KEYS
from PiezoWebApp.src.config.spark_job_validation_rules import VALIDATION_RULES
from PiezoWebApp.src.services.spark_job.validation import argument_validator
from PiezoWebApp.src.services.spark_job.validation.validation_ruleset import ValidationRuleset


class TestArgumentValidator:
    # pylint: disable=attribute-defined-outside-init
    @pytest.fixture(autouse=True)
    def setup(self):
        self.validation_ruleset = ValidationRuleset(LANGUAGE_SPECIFIC_KEYS, VALIDATION_RULES)

    @pytest.mark.parametrize("name", ["test", "name", "12ewq", "13234some_long_name!!!@"])
    def test_validate_name_validates_non_empty_strings(self, name):
        # Arrange
        validation_rule = self.validation_ruleset.get_validation_rule_for_key("name")
        # Act
        validation_result = argument_validator.validate("name", name, validation_rule)
        # Assert
        assert validation_result.is_valid is True

    @pytest.mark.parametrize("name", ["", "   ", 123])
    def test_validate_name_rejects_empty_strings_and_non_string_values(self, name):
        # Arrange
        validation_rule = self.validation_ruleset.get_validation_rule_for_key("name")
        # Act
        validation_result = argument_validator.validate("name", name, validation_rule)
        # Assert
        assert validation_result.is_valid is False

    @pytest.mark.parametrize("language", ["Python", "Scala"])
    def test_validate_language_validates_valid_languages(self, language):
        # Arrange
        validation_rule = self.validation_ruleset.get_validation_rule_for_key("language")
        # Act
        validation_result = argument_validator.validate("language", language, validation_rule)
        # Assert
        assert validation_result.is_valid is True

    @pytest.mark.parametrize("language", ["python", "PYTHON", "PythON", "SCALA", "ScALa", "R", 123, "", "  "])
    def test_validate_language_rejects_non_valid_languages(self, language):
        # Arrange
        validation_rule = self.validation_ruleset.get_validation_rule_for_key("language")
        # Act
        validation_result = argument_validator.validate("language", language, validation_rule)
        # Assert
        assert validation_result.is_valid is False

    @pytest.mark.parametrize("version", ["2", "3"])
    def test_validate_python_version_validates_string_2_or_3(self, version):
        # Arrange
        validation_rule = self.validation_ruleset.get_validation_rule_for_key("python_version")
        # Act
        validation_result = argument_validator.validate("python_version", version, validation_rule)
        # Assert
        assert validation_result.is_valid is True

    @pytest.mark.parametrize("version", [2.0, 2, 3, 3.7, None])
    def test_validate_python_version_rejects_non_string(self, version):
        # Arrange
        validation_rule = self.validation_ruleset.get_validation_rule_for_key("python_version")
        # Act
        validation_result = argument_validator.validate("python_version", version, validation_rule)
        # Assert
        assert validation_result.is_valid is False
        assert validation_result.message == '"python_version" input must be a string'

    @pytest.mark.parametrize("version", ["1", "4", " ", "", "2.0", "3.6"])
    def test_validate_python_version_rejects_non_string(self, version):
        # Arrange
        validation_rule = self.validation_ruleset.get_validation_rule_for_key("python_version")
        # Act
        validation_result = argument_validator.validate("python_version", version, validation_rule)
        # Assert
        assert validation_result.is_valid is False
        assert validation_result.message == '"python_version" input must be one of: "2", "3"'

    @pytest.mark.parametrize("path", ["/path/to/file", r"\path\to\file"])
    def test_validate_path_to_main_app_file_validates_non_empty_strings(self, path):
        # Arrange
        validation_rule = self.validation_ruleset.get_validation_rule_for_key("path_to_main_app_file")
        # Act
        validation_result = argument_validator.validate("path_to_main_app_file", path, validation_rule)
        # Assert
        assert validation_result.is_valid is True

    @pytest.mark.parametrize("path", [" ", "", 123323])
    def test_validate_path_to_main_app_file_rejects_empty_strings_and_non_strings(self, path):
        # Arrange
        validation_rule = self.validation_ruleset.get_validation_rule_for_key("path_to_main_app_file")
        # Act
        validation_result = argument_validator.validate("path_to_main_app_file", path, validation_rule)
        # Assert
        assert validation_result.is_valid is False

    @pytest.mark.parametrize("main_class", ["someClass", "12321"])
    def test_validate_main_class_validates_non_empty_strings(self, main_class):
        # Arrange
        validation_rule = self.validation_ruleset.get_validation_rule_for_key("main_class")
        # Act
        validation_result = argument_validator.validate("main_class", main_class, validation_rule)
        # Assert
        assert validation_result.is_valid is True

    @pytest.mark.parametrize("main_class", [" ", "", 123323, None])
    def test_validate_main_class_rejects_empty_strings_and_non_strings(self, main_class):
        # Arrange
        validation_rule = self.validation_ruleset.get_validation_rule_for_key("main_class")
        # Act
        validation_result = argument_validator.validate("main_class", main_class, validation_rule)
        # Assert
        assert validation_result.is_valid is False

    @pytest.mark.parametrize("cores", ["0.1", "0.5", "1", "1.0"])
    def test_validate_driver_cores_accepts_values_within_valid_range(self, cores):
        # Arrange
        validation_rule = self.validation_ruleset.get_validation_rule_for_key("driver_cores")
        # Act
        validation_result = argument_validator.validate("driver_cores", cores, validation_rule)
        # Assert
        assert validation_result.is_valid is True

    @pytest.mark.parametrize("cores", [" ", "", None, "100m", "200mn", "12e13m"])
    def test_validate_driver_cores_rejects_empty_strings_and_non_numbers(self, cores):
        # Arrange
        validation_rule = self.validation_ruleset.get_validation_rule_for_key("driver_cores")
        # Act
        validation_result = argument_validator.validate("driver_cores", cores, validation_rule)
        # Assert
        assert validation_result.is_valid is False
        assert validation_result.message == '"driver_cores" input must be a multiple of 0.1'

    @pytest.mark.parametrize("cores", ["0.51", 0.35])
    def test_validate_driver_cores_rejects_values_not_a_multiple_of_a_tenth(self, cores):
        # Arrange
        validation_rule = self.validation_ruleset.get_validation_rule_for_key("driver_cores")
        # Act
        validation_result = argument_validator.validate("driver_cores", cores, validation_rule)
        # Assert
        assert validation_result.is_valid is False
        assert validation_result.message == '"driver_cores" input must be a multiple of 0.1'

    @pytest.mark.parametrize("cores", ["0.0", 0, "1.1", 1.1])
    def test_validate_driver_cores_rejects_values_outside_valid_range(self, cores):
        # Arrange
        validation_rule = self.validation_ruleset.get_validation_rule_for_key("driver_cores")
        # Act
        validation_result = argument_validator.validate("driver_cores", cores, validation_rule)
        # Assert
        assert validation_result.is_valid is False
        assert validation_result.message == '"driver_cores" input must be in range [0.1, 1]'

    @pytest.mark.parametrize("core_limit", ["400m", "0.4", "200m", "0.2", "0.30"])
    def test_validate_driver_core_limit_accepts_values_in_both_cpu_and_millicpu_within_valid_range(self, core_limit):
        # Arrange
        validation_rule = self.validation_ruleset.get_validation_rule_for_key("driver_core_limit")
        # Act
        validation_result = argument_validator.validate("driver_core_limit", core_limit, validation_rule)
        # Assert
        assert validation_result.is_valid is True

    @pytest.mark.parametrize("core_limit", ["99m", "0.0", "201mn", "0.01", "0.21", "12e13m", " ", ""])
    def test_validate_driver_core_limit_rejects_values_outside_valid_range_or_with_incorrect_format(self, core_limit):
        # Arrange
        validation_rule = self.validation_ruleset.get_validation_rule_for_key("driver_core_limit")
        # Act
        validation_result = argument_validator.validate("driver_core_limit", core_limit, validation_rule)
        # Assert
        assert validation_result.is_valid is False

    @pytest.mark.parametrize("memory", ["512m", "512", "1000", "1000.0", "2048m", "2048"])
    def test_validate_driver_memory_accepts_values_for_megabytes_as_string(self, memory):
        # Arrange
        validation_rule = self.validation_ruleset.get_validation_rule_for_key("driver_memory")
        # Act
        validation_result = argument_validator.validate("driver_memory", memory, validation_rule)
        # Assert
        assert validation_result.is_valid is True

    @pytest.mark.parametrize("memory", ["200m", "200", "4096m", "4096", "  ", "20nb279", "2050.56", "3289.43", ""])
    def test_validate_driver_memory_rejects_values_for_values_outside_range_and_incorrectly_formatted(self, memory):
        # Arrange
        validation_rule = self.validation_ruleset.get_validation_rule_for_key("driver_memory")
        # Act
        validation_result = argument_validator.validate("driver_memory", memory, validation_rule)
        # Assert
        assert validation_result.is_valid is False

    @pytest.mark.parametrize("executors", ["1", "2", "5"])
    def test_validate_executors_accepts_numerical_values_within_valid_range(self, executors):
        # Arrange
        validation_rule = self.validation_ruleset.get_validation_rule_for_key("executors")
        # Act
        validation_result = argument_validator.validate("executors", executors, validation_rule)
        # Assert
        assert validation_result.is_valid is True

    @pytest.mark.parametrize("executors", [" ", "", "1p", "3.3", "4.0"])
    def test_validate_executors_rejects_badly_formatted_inputs(self, executors):
        # Arrange
        validation_rule = self.validation_ruleset.get_validation_rule_for_key("executors")
        # Act
        validation_result = argument_validator.validate("executors", executors, validation_rule)
        # Assert
        assert validation_result.is_valid is False
        assert validation_result.message == '"executors" input must be an integer'

    @pytest.mark.parametrize("executors", ["100", "0", "11", "-1"])
    def test_validate_executors_rejects_values_outside_valid_range(self, executors):
        # Arrange
        validation_rule = self.validation_ruleset.get_validation_rule_for_key("executors")
        # Act
        validation_result = argument_validator.validate("executors", executors, validation_rule)
        # Assert
        assert validation_result.is_valid is False
        assert validation_result.message == '"executors" input must be in range [1, 10]'

    @pytest.mark.parametrize("executor_cores", ["1", "2", "3", "4"])
    def test_validate_executor_cores_accepts_numerical_values_within_valid_range(self, executor_cores):
        # Arrange
        validation_rule = self.validation_ruleset.get_validation_rule_for_key("executor_cores")
        # Act
        validation_result = argument_validator.validate("executor_cores", executor_cores, validation_rule)
        # Assert
        assert validation_result.is_valid is True

    @pytest.mark.parametrize("executor_cores", ["100", "0", " ", "", "1p", "5000m", "3.0"])
    def test_validate_executor_cores_rejects_values_outside_valid_range_or_with_bad_format(self, executor_cores):
        # Arrange
        validation_rule = self.validation_ruleset.get_validation_rule_for_key("executor_cores")
        # Act
        validation_result = argument_validator.validate("executor_cores", executor_cores, validation_rule)
        # Assert
        assert validation_result.is_valid is False

    @pytest.mark.parametrize("memory", ["512", "2000m", "3000", "4096"])
    def test_validate_executor_memory_accepts_numerical_values_within_valid_range(self, memory):
        # Arrange
        validation_rule = self.validation_ruleset.get_validation_rule_for_key("executor_memory")
        # Act
        validation_result = argument_validator.validate("executor_memory", memory, validation_rule)

        # Assert
        assert validation_result.is_valid is True

    @pytest.mark.parametrize("memory", ["511", "200", " ", "", "5000", "4097", "590M"])
    def test_validate_executor_memory_rejects_values_outside_valid_range_or_with_bad_format(self, memory):
        # Arrange
        validation_rule = self.validation_ruleset.get_validation_rule_for_key("executor_memory")
        # Act
        validation_result = argument_validator.validate("executor_memory", memory, validation_rule)
        # Assert
        assert validation_result.is_valid is False
