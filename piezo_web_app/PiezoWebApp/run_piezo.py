import logging
import os

import kubernetes
import tornado

from PiezoWebApp.src.handlers.delete_job import DeleteJobHandler
from PiezoWebApp.src.handlers.get_jobs import GetJobsHandler
from PiezoWebApp.src.handlers.get_logs import GetLogsHandler
from PiezoWebApp.src.handlers.heartbeat_handler import HeartbeatHandler
from PiezoWebApp.src.handlers.job_status import JobStatusHandler
from PiezoWebApp.src.handlers.submit_job import SubmitJobHandler
from PiezoWebApp.src.handlers.write_logs_handler import WriteLogsHandler
from PiezoWebApp.src.services.kubernetes.kubernetes_adapter import KubernetesAdapter
from PiezoWebApp.src.services.spark_job.spark_job_namer import SparkJobNamer
from PiezoWebApp.src.services.spark_job.spark_job_service import SparkJobService
from PiezoWebApp.src.services.spark_job.validation.manifest_populator import ManifestPopulator
from PiezoWebApp.src.services.spark_job.validation.validation_ruleset import ValidationRuleset
from PiezoWebApp.src.services.spark_job.validation.validation_service import ValidationService
from PiezoWebApp.src.services.storage.adapters.boto_adapter import BotoAdapter
from PiezoWebApp.src.utils.configurations import Configuration
from PiezoWebApp.src.utils.route_helper import format_route_specification
from PiezoWebApp.src.utils.validation_ruleset_parser import ValidationRulesetParser


def build_kubernetes_adapter(configuration):
    if configuration.run_environment == "SYSTEM":
        config = kubernetes.config.load_kube_config(config_file=configuration.k8s_cluster_config_file)
    elif configuration.run_environment == "K8S":
        config = kubernetes.config.load_incluster_config()
    else:
        raise RuntimeError("Invalid running environment specified in config file")
    adapter = KubernetesAdapter(config)
    return adapter


def build_logger(configuration):
    # Set  up the logger
    log = logging.getLogger("piezo-web-app")
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    log.setLevel(configuration.logging_level)

    # Set up console logging
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    log.addHandler(console)

    # Set up file logging
    log_file_name = "piezo-web-app.log"
    full_path = os.path.join(configuration.log_folder_location, log_file_name)
    file_handler = logging.handlers.RotatingFileHandler(full_path, maxBytes=100*1024, backupCount=10)
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)
    return log


def build_container(configuration, k8s_adapter, log, storage_adapter, validation_rules_path):
    validation_rules = ValidationRulesetParser().parse(validation_rules_path)
    validation_ruleset = ValidationRuleset(validation_rules)
    validation_service = ValidationService(validation_ruleset)
    manifest_populator = ManifestPopulator(configuration, validation_ruleset)
    spark_job_namer = SparkJobNamer(k8s_adapter)
    spark_job_service = SparkJobService(
        k8s_adapter,
        log,
        manifest_populator,
        spark_job_namer,
        storage_adapter,
        validation_service
    )
    container = dict(
        logger=log,
        spark_job_service=spark_job_service,
        validation_ruleset=validation_ruleset
    )
    return container


def build_app(container, use_route_stem=False):
    heartbeat_route = '/piezo(|/)' if use_route_stem else '(|/)'
    route_stem = 'piezo/' if use_route_stem else ''
    app = tornado.web.Application(
        [
            (heartbeat_route, HeartbeatHandler),
            (format_route_specification(route_stem + 'deletejob'), DeleteJobHandler, container),
            (format_route_specification(route_stem + 'getjobs'), GetJobsHandler, container),
            (format_route_specification(route_stem + 'getlogs'), GetLogsHandler, container),
            (format_route_specification(route_stem + 'jobstatus'), JobStatusHandler, container),
            (format_route_specification(route_stem + 'submitjob'), SubmitJobHandler, container),
            (format_route_specification(route_stem + 'writelogs'), WriteLogsHandler, container)
        ]
    )
    return app


if __name__ == "__main__":
    CONFIGURATION_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'configuration.ini'))
    CONFIGURATION = Configuration(CONFIGURATION_PATH)
    VALIDATION_RULES_PATH = '/etc/configs/validation_rules.json'
    KUBERNETES_ADAPTER = build_kubernetes_adapter(CONFIGURATION)
    LOGGER = build_logger(CONFIGURATION)
    STORAGE_ADAPTER = BotoAdapter(CONFIGURATION, LOGGER)
    CONTAINER = build_container(CONFIGURATION, KUBERNETES_ADAPTER, LOGGER, STORAGE_ADAPTER, VALIDATION_RULES_PATH)
    APPLICATION = build_app(CONTAINER, use_route_stem=True)
    APPLICATION.listen(CONFIGURATION.app_port)
    tornado.ioloop.IOLoop.current().start()
