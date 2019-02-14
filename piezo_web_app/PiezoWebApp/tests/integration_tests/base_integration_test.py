from abc import ABCMeta, abstractmethod
import json
import logging
import mock
import tornado.testing

from PiezoWebApp.run_piezo import build_app
from PiezoWebApp.src.services.kubernetes.i_kubernetes_service import IKubernetesService


class BaseIntegrationTest(tornado.testing.AsyncHTTPTestCase, metaclass=ABCMeta):
    @property
    @abstractmethod
    def handler(self):
        pass

    @property
    @abstractmethod
    def standard_request_method(self):
        pass

    def setup(self):
        self.mock_k8s_adapter = mock.create_autospec(IKubernetesService)
        self.mock_logger = mock.create_autospec(logging.Logger)

    def get_app(self):
        application = build_app(self.mock_k8s_adapter, self.mock_logger)
        self.url = self.get_url("/api/test_handler_route")
        return application

    async def _request(self, method, body):
        json_body = json.dumps(body)
        response = await self.http_client.fetch(
            self.url,
            method=method,
            body=json_body,
            allow_nonstandard_methods=True
        )
        return response
