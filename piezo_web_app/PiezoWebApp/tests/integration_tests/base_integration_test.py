from abc import ABCMeta, abstractmethod
import json
import logging
import os

import mock
import pytest
import tornado.testing
from tornado.web import Application

from PiezoWebApp.run_piezo import build_container
from PiezoWebApp.src.services.kubernetes.i_kubernetes_adapter import IKubernetesAdapter
from PiezoWebApp.src.services.storage.adapters.i_storage_adapter import IStorageAdapter
from PiezoWebApp.src.utils.configurations import Configuration
from PiezoWebApp.src.utils.route_helper import format_route_specification

# str | The custom resource's group name
CRD_GROUP = 'sparkoperator.k8s.io'

# str | The custom resource's plural name. For TPRs this would be lowercase plural kind.
CRD_PLURAL = 'sparkapplications'

# str | The custom resource's version
CRD_VERSION = 'v1beta1'


class BaseIntegrationTest(tornado.testing.AsyncHTTPTestCase, metaclass=ABCMeta):
    @property
    @abstractmethod
    def handler(self):
        pass

    @property
    @abstractmethod
    def standard_request_method(self):
        pass

    # pylint: disable=attribute-defined-outside-init
    @pytest.fixture(autouse=True)
    def setup(self):
        self.mock_configuration = mock.create_autospec(Configuration)
        self.mock_configuration.s3_endpoint = "http://0.0.0.0:0"
        self.mock_configuration.s3_secrets_name = "secret"
        self.mock_configuration.secrets_dir = "/etc/secrets/"
        self.mock_k8s_adapter = mock.create_autospec(IKubernetesAdapter)
        self.mock_logger = mock.create_autospec(logging.Logger)
        self.mock_storage_adapter = mock.create_autospec(IStorageAdapter)
        self.ruleset_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'example_validation_rules.json'))

    def get_app(self):
        container = build_container(
            self.mock_configuration,
            self.mock_k8s_adapter,
            self.mock_logger,
            self.mock_storage_adapter,
            self.ruleset_path
        )
        application = Application(
            [
                (format_route_specification("testroute"), self.handler, container)
            ]
        )
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
        response_body = BaseIntegrationTest._get_body(response)
        return response_body, response.code
