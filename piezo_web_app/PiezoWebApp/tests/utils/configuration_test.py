# pylint: disable=R0913
import os
import tempfile

import pytest

from PiezoWebApp.src.utils.configurations import Configuration


class SampleConfigurationCreator:
    @staticmethod
    def create_configuration(log_folder_loc,
                             logging_level,
                             app_port,
                             run_environment,
                             k8s_cluster_config_file):
        template = "[Logging]\n"
        template = SampleConfigurationCreator.add_element_to_temp_file(template,
                                                                       "LogFolderLocation",
                                                                       log_folder_loc)
        template = SampleConfigurationCreator.add_element_to_temp_file(template,
                                                                       "LoggingLevel",
                                                                       logging_level)
        template += "[Application]\n"
        template = SampleConfigurationCreator.add_element_to_temp_file(template,
                                                                       "ApplicationPort",
                                                                       app_port)
        template = SampleConfigurationCreator.add_element_to_temp_file(template,
                                                                       "RunEnvironment",
                                                                       run_environment)
        template = SampleConfigurationCreator.add_element_to_temp_file(template,
                                                                       "K8sClusterConfigFile",
                                                                       k8s_cluster_config_file)

        return SampleConfigurationCreator.write_sample_configuration_file(template)

    @staticmethod
    def write_sample_configuration_file(file_content):
        temp = tempfile.NamedTemporaryFile(mode='w+', delete=False)
        temp.write(file_content)
        path = temp.name
        temp.close()
        return path

    @staticmethod
    def add_element_to_temp_file(template, key, value):
        if value:
            template += "{} = {}\n".format(key, value)
        return template

    @staticmethod
    def remove_file(file_path):
        if os.path.exists(file_path):
            os.remove(file_path)


def test_configuration_raises_when_path_is_not_correct():
    with pytest.raises(RuntimeError) as exception_info:
        path = "dummy_path"
        Configuration(path)
    assert("The configuration file dummy_path does not seem to exist."
           " Provide a configuration file" in str(exception_info.value))


def test_configuration_parses_with_arguments():
    # Arrange
    current = os.getcwd()
    configuration_path = SampleConfigurationCreator.create_configuration(current,
                                                                         "INFO",
                                                                         "8888",
                                                                         "SYSTEM",
                                                                         "Some/Path")

    # Act
    configuration = Configuration(configuration_path)

    # Assert
    assert configuration.log_folder_location == current
    assert configuration.logging_level == "INFO"
    assert configuration.app_port == 8888
    assert configuration.run_environment == "SYSTEM"
    assert configuration.k8s_cluster_config_file == "Some/Path"

    # Clean up
    SampleConfigurationCreator.remove_file(configuration_path)

