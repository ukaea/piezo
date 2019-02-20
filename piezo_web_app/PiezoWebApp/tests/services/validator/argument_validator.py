import pytest

from PiezoWebApp.src.services.validator import argument_validator
from PiezoWebApp.src.services.validator.validation_rules import ValidationRules


class TestArgumentValidator:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.validation_rules = ValidationRules()

    @pytest.mark.parametrize("name", ["test", "name", "12ewq", "13234some_long_name!!!@"])
    def test_validate_name_validates_non_empty_strings(self, name):
        # Act
        validation_result = argument_validator.validate_name(name)
        # Assert
        assert validation_result.is_valid is True

    @pytest.mark.parametrize("name", ["", "   ", 123])
    def test_validate_name_rejects_empty_strings_and_non_string_values(self, name):
        # Act
        validation_result = argument_validator.validate_name(name)
        # Assert
        assert validation_result.is_valid is False

    @pytest.mark.parametrize("language", ["python", "PYTHON", "PythON", "Scala", "SCALA", "ScALa"])
    def test_validate_language_validates_valid_languages(self, language):
        # Act
        validation_result = argument_validator.validate_language(language)
        # Assert
        assert validation_result.is_valid is True

    @pytest.mark.parametrize("language", ["pytho", "R", "Fortran", 123, "", "  "])
    def test_validate_language_rejects_non_valid_languages(self, language):
        # Act
        validation_result = argument_validator.validate_language(language)
        # Assert
        assert validation_result.is_valid is False

    @pytest.mark.parametrize("version", ["2", "3", 2, 3])
    def test_validate_python_version_validates_2_and_3(self, version):
        # Act
        validation_result = argument_validator.validate_python_version(version)
        # Assert
        assert validation_result.is_valid is True

    @pytest.mark.parametrize("version", [1, 4, 3.7, "1", "4", " ", "", 23, 2.0])
    def test_validate_python_version_rejects_non_2_or_3(self, version):
        # Act
        validation_result = argument_validator.validate_python_version(version)
        # Assert
        assert validation_result.is_valid is False

    @pytest.mark.parametrize("path", ["/path/to/file", r"\path\to\file"])
    def test_validate_path_to_main_app_file_validates_non_empty_strings(self, path):
        # Act
        validation_result = argument_validator.validate_path_to_main_app_file(path)
        # Assert
        assert validation_result.is_valid is True

    @pytest.mark.parametrize("path", [" ", "", 123323])
    def test_validate_path_to_main_app_file_rejects_empty_strings_and_non_strings(self, path):
        # Act
        validation_result = argument_validator.validate_path_to_main_app_file(path)
        # Assert
        assert validation_result.is_valid is False

    @pytest.mark.parametrize("main_class", ["someClass", "12321"])
    def test_validate_main_class_validates_non_empty_strings(self, main_class):
        # Act
        validation_result = argument_validator.validate_main_class(main_class)
        # Assert
        assert validation_result.is_valid is True

    @pytest.mark.parametrize("main_class", [" ", "", 123323])
    def test_validate_main_class_rejects_empty_strings_and_non_strings(self, main_class):
        # Act
        validation_result = argument_validator.validate_path_to_main_app_file(main_class)
        # Assert
        assert validation_result.is_valid is False

    @pytest.mark.parametrize("cores", ["100m", 0.1, "200m", 0.2, "0.2"])
    def test_validate_driver_cores_accepts_values_in_both_cpu_and_millicpu_within_valid_range(self, cores):
        # Arrange
        validation_values = self.validation_rules.get_property_array_for_key("driver_cores")
        # Act
        validation_result = argument_validator.validate_driver_cores(cores, validation_values[0], validation_values[1])
        # Assert
        assert validation_result.is_valid is True

    @pytest.mark.parametrize("cores", ["1001m", 0.0, "200mn", 1.01, "12e13m", " ", ""])
    def test_validate_driver_cores_rejects_values_outside_valid_range_or_with_incorrect_format(self, cores):
        # Arrange
        validation_values = self.validation_rules.get_property_array_for_key("driver_cores")
        # Act
        validation_result = argument_validator.validate_driver_cores(cores, validation_values[0], validation_values[1])
        # Assert
        assert validation_result.is_valid is False

    @pytest.mark.parametrize("core_limit", ["400m", 0.4, "200m", 0.2, "0.30"])
    def test_validate_driver_core_limit_accepts_values_in_both_cpu_and_millicpu_within_valid_range(self, core_limit):
        # Arrange
        validation_values = self.validation_rules.get_property_array_for_key("driver_core_limit")
        # Act
        validation_result = \
            argument_validator.validate_driver_core_limit(core_limit, validation_values[0], validation_values[1])
        # Assert
        assert validation_result.is_valid is True

    @pytest.mark.parametrize("core_limit", ["99m", 0.0, "201mn", 0.01, 0.21, "12e13m", " ", ""])
    def test_validate_driver_core_limit_rejects_values_outside_valid_range_or_with_incorrect_format(self, core_limit):
        # Arrange
        validation_values = self.validation_rules.get_property_array_for_key("driver_core_limit")
        # Act
        validation_result = \
            argument_validator.validate_driver_core_limit(core_limit, validation_values[0], validation_values[1])
        # Assert
        assert validation_result.is_valid is False

    @pytest.mark.parametrize("memory", ["512m", 512, "1000", 1000.0, "2048m", 2048])
    def test_validate_driver_memory_accepts_values_for_megabytes_both_string_and_int_formatted(self, memory):
        # Arrange
        validation_values = self.validation_rules.get_property_array_for_key("driver_memory")
        # Act
        validation_result = \
            argument_validator.validate_driver_memory(memory, validation_values[0], validation_values[1])
        # Assert
        assert validation_result.is_valid is True

    @pytest.mark.parametrize("memory", ["200m", 200, "4096m", "4096", 4096, "  ", "20nb279", 2050.56, "3289.43", ""])
    def test_validate_driver_memory_rejects_values_for_values_outside_range_and_incorrectly_formatted(self, memory):
        # Arrange
        validation_values = self.validation_rules.get_property_array_for_key("driver_memory")
        # Act
        validation_result = \
            argument_validator.validate_driver_memory(memory, validation_values[0], validation_values[1])
        # Assert
        assert validation_result.is_valid is False

    @pytest.mark.parametrize("executors", ["1", 2, 3.0, 5, "4.0"])
    def test_validate_executors_accepts_numerical_values_within_valid_range(self, executors):
        # Arrange
        validation_values = self.validation_rules.get_property_array_for_key("executors")
        # Act
        validation_result = \
            argument_validator.validate_executors(executors, validation_values[0], validation_values[1])
        # Assert
        assert validation_result.is_valid is True

    @pytest.mark.parametrize("executors", [100, "0", " ", "", "1p", 3.3])
    def test_validate_executors_rejects_values_outside_valid_range_or_with_bad_format(self, executors):
        # Arrange
        validation_values = self.validation_rules.get_property_array_for_key("executors")
        # Act
        validation_result = \
            argument_validator.validate_executors(executors, validation_values[0], validation_values[1])
        # Assert
        assert validation_result.is_valid is False

    @pytest.mark.parametrize("executor_cores", ["1", 2, 3.0, "4", "3000m"])
    def test_validate_executor_cores_accepts_numerical_values_within_valid_range(self, executor_cores):
        # Arrange
        validation_values = self.validation_rules.get_property_array_for_key("executor_cores")
        # Act
        validation_result = \
            argument_validator.validate_executor_cores(executor_cores, validation_values[0], validation_values[1])
        # Assert
        assert validation_result.is_valid is True

    @pytest.mark.parametrize("executor_cores", [100, "0", " ", "", "1p", "5000m"])
    def test_validate_executor_cores_rejects_values_outside_valid_range_or_with_bad_format(self, executor_cores):
        # Arrange
        validation_values = self.validation_rules.get_property_array_for_key("executor_cores")
        # Act
        validation_result = \
            argument_validator.validate_executor_cores(executor_cores, validation_values[0], validation_values[1])
        # Assert
        assert validation_result.is_valid is False

    @pytest.mark.parametrize("executor_memory", ["512", 512, "2000m", 3000, 4096, "4096"])
    def test_validate_executor_memory_accepts_numerical_values_within_valid_range(self, executor_memory):
        # Arrange
        validation_values = self.validation_rules.get_property_array_for_key("executor_memory")
        # Act
        validation_result = \
            argument_validator.validate_executor_memory(executor_memory, validation_values[0], validation_values[1])
        # Assert
        assert validation_result.is_valid is True

    @pytest.mark.parametrize("executor_memory", [511, "200", " ", "", "5000", 4097, "590M"])
    def test_validate_executor_memory_rejects_values_outside_valid_range_or_with_bad_format(self, executor_memory):
        # Arrange
        validation_values = self.validation_rules.get_property_array_for_key("executor_memory")
        # Act
        validation_result = \
            argument_validator.validate_executor_memory(executor_memory, validation_values[0], validation_values[1])
        # Assert
        assert validation_result.is_valid is False
