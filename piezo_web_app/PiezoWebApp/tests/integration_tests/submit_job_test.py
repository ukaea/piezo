from PiezoWebApp.src.handlers.submit_job import SubmitJobHandler
from PiezoWebApp.tests.integration_tests.base_integration_test import BaseIntegrationTest


class SubmitJobIntegrationTest(BaseIntegrationTest):
    def handler(self):
        return SubmitJobHandler

    def standard_request_method(self):
        return "POST"
