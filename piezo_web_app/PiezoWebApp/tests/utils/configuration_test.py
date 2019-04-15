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
                             k8s_cluster_config_file,
                             tidy_frequency,
                             s3_endpoint,
                             s3_bucket_name,
                             s3_secret_name,
                             secrets_dir,
                             temp_url_expiry_seconds):
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
        template = SampleConfigurationCreator.add_element_to_temp_file(template,
                                                                       "TidyFrequency",
                                                                       tidy_frequency)
        template += "[Storage]\n"
        template = SampleConfigurationCreator.add_element_to_temp_file(template,
                                                                       "S3Endpoint",
                                                                       s3_endpoint)
        template = SampleConfigurationCreator.add_element_to_temp_file(template,
                                                                       "S3BucketName",
                                                                       s3_bucket_name)
        template = SampleConfigurationCreator.add_element_to_temp_file(template,
                                                                       "S3KeysSecret",
                                                                       s3_secret_name)
        template = SampleConfigurationCreator.add_element_to_temp_file(template,
                                                                       "SecretsDir",
                                                                       secrets_dir)
        template = SampleConfigurationCreator.add_element_to_temp_file(template,
                                                                       "TempUrlExpirySeconds",
                                                                       temp_url_expiry_seconds)

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
                                                                         "Some/Path",
                                                                         "3600",
                                                                         "https://0.0.0.0:0",
                                                                         "test-bucket",
                                                                         "some_secret",
                                                                         "/etc/secrets/",
                                                                         "600")

    # Act
    configuration = Configuration(configuration_path)

    # Assert
    assert configuration.log_folder_location == current
    assert configuration.logging_level == "INFO"
    assert configuration.app_port == 8888
    assert configuration.run_environment == "SYSTEM"
    assert configuration.k8s_cluster_config_file == "Some/Path"
    assert configuration.tidy_frequency == 3600
    assert configuration.s3_endpoint == "https://0.0.0.0:0"
    assert configuration.s3_host == "0.0.0.0"
    assert configuration.s3_port == 0
    assert configuration.s3_bucket_name == "test-bucket"
    assert configuration.s3_secrets_name == "some_secret"
    assert configuration.secrets_dir == "/etc/secrets/"
    assert configuration.is_s3_secure is True
    assert configuration.temp_url_expiry_seconds == 600

    # Clean up
    SampleConfigurationCreator.remove_file(configuration_path)
