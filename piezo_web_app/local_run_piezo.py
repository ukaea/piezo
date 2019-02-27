import logging
import os

import kubernetes
import tornado

from PiezoWebApp.src.config.spark_job_validation_rules import LANGUAGE_SPECIFIC_KEYS
from PiezoWebApp.src.config.spark_job_validation_rules import VALIDATION_RULES
from PiezoWebApp.src.handlers.delete_job import DeleteJobHandler
from PiezoWebApp.src.handlers.get_logs import GetLogsHandler
from PiezoWebApp.src.handlers.heartbeat_handler import HeartbeatHandler
from PiezoWebApp.src.handlers.submit_job import SubmitJobHandler
from PiezoWebApp.src.services.kubernetes.kubernetes_adapter import KubernetesAdapter
from PiezoWebApp.src.services.spark_job.validation.manifest_populator import ManifestPopulator
from PiezoWebApp.src.services.spark_job.validation.validation_ruleset import ValidationRuleset
from PiezoWebApp.src.services.spark_job.spark_job_service import SparkJobService
from PiezoWebApp.src.services.spark_job.validation.validation_service import ValidationService
from PiezoWebApp.src.utils.route_helper import format_route_specification


def build_kubernetes_adapter():
    config = kubernetes.config.load_kube_config(config_file=r"C:\Users\taro\.kube\openstack")
    adapter = KubernetesAdapter(config)
    return adapter


def build_logger(log_file_location, level):
    # Set  up the logger
    log = logging.getLogger("piezo-web-app")
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    log.setLevel(level)

    # Set up console logging
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    log.addHandler(console)

    # Set up file logging
    # log_file_name = "piezo-web-app.log"
    # full_path = os.path.join(log_file_location, log_file_name)
    # file_handler = logging.handlers.RotatingFileHandler(full_path, maxBytes=100*1024, backupCount=10)
    # file_handler.setFormatter(formatter)
    # log.addHandler(file_handler)
    return log


def build_container(k8s_adapter, log):
    validation_ruleset = ValidationRuleset(LANGUAGE_SPECIFIC_KEYS, VALIDATION_RULES)
    validation_service = ValidationService(validation_ruleset)
    manifest_populator = ManifestPopulator(validation_ruleset)
    spark_job_service = SparkJobService(k8s_adapter, log, manifest_populator, validation_service)
    container = dict(
        logger=log,
        spark_job_service=spark_job_service
    )
    return container


def build_app(container, use_route_stem=False):
    heartbeat_route = '/piezo(|/)' if use_route_stem else '(|/)'
    route_stem = 'piezo/' if use_route_stem else ''
    app = tornado.web.Application(
        [
            (heartbeat_route, HeartbeatHandler),
            (format_route_specification(route_stem + 'deletejob'), DeleteJobHandler, container),
            (format_route_specification(route_stem + 'getlogs'), GetLogsHandler, container),
            (format_route_specification(route_stem + 'submitjob'), SubmitJobHandler, container)
        ]
    )
    return app


if __name__ == "__main__":
    KUBERNETES_ADAPTER = build_kubernetes_adapter()
    LOGGER = build_logger("/piezo_web_app/", "INFO")
    CONTAINER = build_container(KUBERNETES_ADAPTER, LOGGER)
    APPLICATION = build_app(CONTAINER, use_route_stem=True)
    APPLICATION.listen(8887)
    tornado.ioloop.IOLoop.current().start()
