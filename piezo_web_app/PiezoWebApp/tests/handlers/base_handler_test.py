from abc import ABCMeta, abstractmethod
import json
import logging
import mock
import pytest
from tornado.httpclient import HTTPClientError
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application

from PiezoWebApp.src.services.spark_job.i_kubernetes_service import IKubernetesService
from PiezoWebApp.src.utils.route_helper import format_route_specification


class BaseHandlerTest(AsyncHTTPTestCase, metaclass=ABCMeta):
    @property
    @abstractmethod
    def handler(self):
        pass

    @property
    @abstractmethod
    def standard_request_method(self):
        pass

    def get_app(self):
        self.mock_kubernetes_service = mock.create_autospec(IKubernetesService)
        self.mock_logger = mock.create_autospec(logging.Logger)
        self.container = {
            'kubernetes_service': self.mock_kubernetes_service,
            'logger': self.mock_logger
        }
        application = Application([
            (format_route_specification('testroute'), self.handler, self.container),
        ])
        self.url = self.get_url(r"/testroute/")
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

    @staticmethod
    def _get_body(response):
        return json.loads(response.body, encoding='utf-8')

    async def send_request(self, body):
        response = await self._request(self.standard_request_method, body)
        response_body = BaseHandlerTest._get_body(response)
        return response_body, response.code

    async def assert_request_returns_400(self, body):
        with pytest.raises(HTTPClientError) as error:
            await self._request(self.standard_request_method, body)
        assert error.value.response.code == 400
