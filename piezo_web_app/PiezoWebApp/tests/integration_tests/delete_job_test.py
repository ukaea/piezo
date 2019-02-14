from PiezoWebApp.src.handlers.delete_job import DeleteJobHandler
from PiezoWebApp.tests.integration_tests.base_integration_test import BaseIntegrationTest


class DeleteJobIntegrationTest(BaseIntegrationTest):
    def handler(self):
        return DeleteJobHandler

    def standard_request_method(self):
        return "DELETE"
