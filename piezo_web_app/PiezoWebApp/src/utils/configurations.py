import os
import configparser

from PiezoWebApp.src.utils.str_helper import str2non_negative_int


class Configuration:
    def __init__(self, path_to_configuration_file):
        self._path_to_configuration_file = path_to_configuration_file

        if not os.path.exists(self._path_to_configuration_file):
            raise RuntimeError("The configuration file {} does not seem to exist. "
                               "Provide a configuration file".format(self._path_to_configuration_file))

        # Logging
        self._log_folder_location = None
        self._logging_level = "NOTSET"

        # Application
        self._app_port = None
        self._run_environment = None
        self._k8s_cluster_config_file = None

        self._parse(self._path_to_configuration_file)

    @property
    def log_folder_location(self):
        return self._log_folder_location

    @property
    def logging_level(self):
        return self._logging_level

    @property
    def app_port(self):
        return self._app_port

    @property
    def run_environment(self):
        return self._run_environment

    @property
    def k8s_cluster_config_file(self):
        return self._k8s_cluster_config_file

    def _parse(self, path):
        config = configparser.ConfigParser()
        config.read(path)
        settings = config["Settings"]

        # Logging
        self._log_folder_location = self.get_directory(settings, "LogFolderLocation")
        self._logging_level = settings["LoggingLevel"]

        # Application
        self._app_port = str2non_negative_int(settings['ApplicationPort'])

        self._run_environment = settings['RunEnvironment']
        self._k8s_cluster_config_file = settings['K8sClusterConfigFile']

    @staticmethod
    def get_directory(settings, key):
        directory = settings[key]
        if not os.path.isdir(directory):
            raise ValueError("The directory {} for {} does not seem to exist. "
                             "Make sure to create it".format(directory, key))
        return directory
