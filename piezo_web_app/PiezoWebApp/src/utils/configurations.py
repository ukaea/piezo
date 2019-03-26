import os
import configparser
from urllib.parse import urlparse

from PiezoWebApp.src.utils.route_helper import is_scheme_secure
from PiezoWebApp.src.utils.str_helper import str2bool
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

        # Storage
        self._s3_endpoint = None
        self._s3_secrets_name = None
        self._secrets_dir = None
        self._is_s3_secure = None

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

    @property
    def s3_endpoint(self):
        return self._s3_endpoint

    @property
    def s3_host(self):
        parse_result = urlparse(self.s3_endpoint)
        return parse_result.hostname

    @property
    def s3_port(self):
        parse_result = urlparse(self.s3_endpoint)
        return parse_result.port

    @property
    def s3_secrets_name(self):
        return self._s3_secrets_name

    @property
    def secrets_dir(self):
        return self._secrets_dir

    @property
    def is_s3_secure(self):
        parse_result = urlparse(self.s3_endpoint)
        return is_scheme_secure(parse_result.scheme)

    def _parse(self, path):
        config = configparser.ConfigParser()
        config.read(path)
        logging = config["Logging"]
        application = config["Application"]
        storage = config["Storage"]

        # Logging
        self._log_folder_location = self.get_directory(logging, "LogFolderLocation")
        self._logging_level = logging["LoggingLevel"]

        # Application
        self._app_port = str2non_negative_int(application['ApplicationPort'])

        self._run_environment = application['RunEnvironment']
        self._k8s_cluster_config_file = application['K8sClusterConfigFile']

        # Storage
        self._s3_endpoint = storage['S3Endpoint']
        self._s3_secrets_name = storage['S3KeysSecret']
        self._secrets_dir = storage['SecretsDir']

    @staticmethod
    def get_directory(settings, key):
        directory = settings[key]
        if not os.path.isdir(directory):
            raise ValueError("The directory {} for {} does not seem to exist. "
                             "Make sure to create it".format(directory, key))
        return directory
