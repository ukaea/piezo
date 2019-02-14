import kubernetes
import logging
import os
import tornado

from PiezoWebApp.src.handlers.delete_job import DeleteJobHandler
from PiezoWebApp.src.handlers.get_logs import GetLogsHandler
from PiezoWebApp.src.handlers.submit_job import SubmitJobHandler
from PiezoWebApp.src.services.kubernetes.kubernetes_adapter import KubernetesAdapter
from PiezoWebApp.src.services.kubernetes.kubernetes_service import KubernetesService
from PiezoWebApp.src.utils.route_helper import format_route_specification


def build_kubernetes_adapter():
    config = kubernetes.config.load_incluster_config()
    kubernetes_adapter = KubernetesAdapter(config)
    return kubernetes_adapter


def build_logger(log_file_location, level):
    # Set  up the logger
    logger = logging.getLogger("piezo-web-app")
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    logger.setLevel(level)

    # Set up console logging
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)

    # Set up file logging
    log_file_name = "piezo-web-app.log"
    full_path = os.path.join(log_file_location, log_file_name)
    file_handler = logging.handlers.RotatingFileHandler(full_path, maxBytes=100*1024, backupCount=10)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


def build_app(k8s_adapter, logger):
    kubernetes_service = KubernetesService(k8s_adapter)
    container = dict(
        kubernetes_service=kubernetes_service,
        logger=logger
    )
    app = tornado.web.Application([
        (format_route_specification("deletejob"), DeleteJobHandler, container),
        (format_route_specification("getlogs"), GetLogsHandler, container),
        (format_route_specification("submitjob"), SubmitJobHandler, container)
     ])
    return app


if __name__ == "__main__":
    kubernetes_adapter = build_kubernetes_adapter()
    logger = build_logger()
    application = build_app(kubernetes_adapter, logger)
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
