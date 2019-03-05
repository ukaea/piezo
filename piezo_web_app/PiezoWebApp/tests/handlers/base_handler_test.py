from abc import ABCMeta, abstractmethod
import json
import logging
import mock
import pytest
from tornado.httpclient import HTTPClientError
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application

from PiezoWebApp.src.services.spark_job.validation.validation_ruleset import ValidationRuleset
from PiezoWebApp.src.services.spark_job.i_spark_job_service import ISparkJobService
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
        self.mock_logger = mock.create_autospec(logging.Logger)
        self.mock_spark_job_service = mock.create_autospec(ISparkJobService)
        self.mock_validation_ruleset = mock.create_autospec(ValidationRuleset)
        self.mock_validation_ruleset.get_key_type_pairs_allowed_as_input.return_value = {
            'name': 'string',
            'language': 'string',
            'path_to_main_app_file': 'string',
            'python_version': 'string',
            'main_class': 'string',
            'driver_cores': 'string',
            'driver_memory': 'string',
            'executors': 'string',
            'executor_cores': 'string',
            'executor_memory': 'string'
        }
        self.mock_validation_ruleset.get_keys_of_required_inputs.return_value = [
            'name',
            'language',
            'path_to_main_app_file'
        ]
        self.container = {
            'logger': self.mock_logger,
            'spark_job_service': self.mock_spark_job_service,
            'validation_ruleset': self.mock_validation_ruleset
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
