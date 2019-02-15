from PiezoWebApp.src.handlers.get_logs import GetLogsHandler
from PiezoWebApp.tests.integration_tests.base_integration_test import BaseIntegrationTest


class GetLogsIntegrationTest(BaseIntegrationTest):
    def handler(self):
        return GetLogsHandler

    def standard_request_method(self):
        return "GET"
