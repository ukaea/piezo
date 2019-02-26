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
    def test_validate_python_version_rejects_string_not_in_list(self, version):
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

    @pytest.mark.parametrize("core_limit", ["0.2", "0.20", "0.6", "1", "1.2"])
    def test_validate_driver_core_limit_accepts_values_within_valid_range(self, core_limit):
        # Arrange
        validation_rule = self.validation_ruleset.get_validation_rule_for_key("driver_core_limit")
        # Act
        validation_result = argument_validator.validate("driver_core_limit", core_limit, validation_rule)
        # Assert
        assert validation_result.is_valid is True

    @pytest.mark.parametrize("core_limit", [" ", "", None, "100m", "200mn", "12e13m"])
    def test_validate_driver_core_limit_rejects_empty_strings_and_non_numbers(self, core_limit):
        # Arrange
        validation_rule = self.validation_ruleset.get_validation_rule_for_key("driver_core_limit")
        # Act
        validation_result = argument_validator.validate("driver_core_limit", core_limit, validation_rule)
        # Assert
        assert validation_result.is_valid is False
        assert validation_result.message == '"driver_core_limit" input must be a multiple of 0.1'

    @pytest.mark.parametrize("core_limit", ["0.51", 0.35])
    def test_validate_driver_core_limit_rejects_values_not_a_multiple_of_a_tenth(self, core_limit):
        # Arrange
        validation_rule = self.validation_ruleset.get_validation_rule_for_key("driver_core_limit")
        # Act
        validation_result = argument_validator.validate("driver_core_limit", core_limit, validation_rule)
        # Assert
        assert validation_result.is_valid is False
        assert validation_result.message == '"driver_core_limit" input must be a multiple of 0.1'

    @pytest.mark.parametrize("core_limit", ["0.0", 0, "0.1", 0.1, "1.3", 1.3])
    def test_validate_driver_core_limit_rejects_values_outside_valid_range(self, core_limit):
        # Arrange
        validation_rule = self.validation_ruleset.get_validation_rule_for_key("driver_core_limit")
        # Act
        validation_result = argument_validator.validate("driver_core_limit", core_limit, validation_rule)
        # Assert
        assert validation_result.is_valid is False
        assert validation_result.message == '"driver_core_limit" input must be in range [0.2, 1.2]'

    @pytest.mark.parametrize("memory", ["512m", "1000m", "2048m"])
    def test_validate_driver_memory_accepts_values_for_megabytes_as_string(self, memory):
        # Arrange
        validation_rule = self.validation_ruleset.get_validation_rule_for_key("driver_memory")
        # Act
        validation_result = argument_validator.validate("driver_memory", memory, validation_rule)
        # Assert
        assert validation_result.is_valid is True

    @pytest.mark.parametrize("memory", ["0m", "511m", "2049m", "4096m"])
    def test_validate_driver_memory_rejects_values_outside_range(self, memory):
        # Arrange
        validation_rule = self.validation_ruleset.get_validation_rule_for_key("driver_memory")
        # Act
        validation_result = argument_validator.validate("driver_memory", memory, validation_rule)
        # Assert
        assert validation_result.is_valid is False
        assert validation_result.message == '"driver_memory" input must be in range [512m, 2048m]'

    @pytest.mark.parametrize("memory", ["4096", "  ", "20nb279", "2050.56", "3289.43", "", "512M", "1g", "1G"])
    def test_validate_driver_memory_rejects_incorrectly_formatted_values(self, memory):
        # Arrange
        validation_rule = self.validation_ruleset.get_validation_rule_for_key("driver_memory")
        # Act
        validation_result = argument_validator.validate("driver_memory", memory, validation_rule)
        # Assert
        assert validation_result.is_valid is False
        assert validation_result.message == '"driver_memory" input must be a string integer value ending in "m" ' \
                                            '(e.g. "512m" for 512 megabytes)'

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

    @pytest.mark.parametrize("memory", ["512m", "1000m", "4096m"])
    def test_validate_executor_memory_values_for_megabytes_as_string(self, memory):
        # Arrange
        validation_rule = self.validation_ruleset.get_validation_rule_for_key("executor_memory")
        # Act
        validation_result = argument_validator.validate("executor_memory", memory, validation_rule)

        # Assert
        assert validation_result.is_valid is True

    @pytest.mark.parametrize("memory", ["0m", "511m", "4097m"])
    def test_validate_executor_memory_rejects_values_outside_valid_range(self, memory):
        # Arrange
        validation_rule = self.validation_ruleset.get_validation_rule_for_key("executor_memory")
        # Act
        validation_result = argument_validator.validate("executor_memory", memory, validation_rule)
        # Assert
        assert validation_result.is_valid is False
        assert validation_result.message == '"executor_memory" input must be in range [512m, 4096m]'

    @pytest.mark.parametrize("memory", ["4096", "  ", "20nb279", "2050.56", "3289.43", "", "512M", "1g", "1G"])
    def test_validate_executor_memory_rejects_incorrectly_formatted_values(self, memory):
        # Arrange
        validation_rule = self.validation_ruleset.get_validation_rule_for_key("executor_memory")
        # Act
        validation_result = argument_validator.validate("executor_memory", memory, validation_rule)
        # Assert
        assert validation_result.is_valid is False
        assert validation_result.message == '"executor_memory" input must be a string integer value ending in "m" ' \
                                            '(e.g. "512m" for 512 megabytes)'
